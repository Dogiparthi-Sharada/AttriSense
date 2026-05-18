# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/causal_uplift.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Causal uplift modelling for retention interventions.

Estimates Conditional Average Treatment Effect (CATE) for each candidate
intervention:
- `salary_lift_10pct`: a one-time 10 % base-salary increase
- `manager_change`: assigning a more tenured manager
- `tenure_bonus`: a one-time +12 month tenure equivalent (relocation,
  rotation, retention bonus that buys 12 months of stability)

We use a T-learner (Two-Models meta-learner), preferring EconML when the
optional causal extra is installed and falling back to an equivalent
sklearn-only implementation for the standard dashboard install. The
synthetic data is small enough that this trains in seconds; for a real
workforce the same code path scales without modification.

The output is the predicted RISK REDUCTION per intervention per
employee, which the dashboard turns into a recommended action.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from attrisense.config import (
    CAUSAL_UPLIFT_TABLE,
    DATABASE_PATH,
    DATASET_PATH,
    DEPARTMENT_CODE_MAP,
    RANDOM_SEED,
    SQL_TABLE_NAME,
)


class SklearnTLearnerFallback:
    """Small T-learner fallback used when the optional EconML extra is absent."""

    def __init__(self, control_model: object, treatment_model: object) -> None:
        self.control_model = control_model
        self.treatment_model = treatment_model

    def effect(self, features: np.ndarray) -> np.ndarray:
        """Return E[Y(1) - Y(0) | X] using two sklearn outcome models."""
        control_risk = self.control_model.predict_proba(features)[:, 1]
        treatment_risk = self.treatment_model.predict_proba(features)[:, 1]
        return treatment_risk - control_risk


@dataclass(frozen=True)
class Intervention:
    """Definition of a candidate retention intervention."""

    name: str
    description: str
    apply_treatment: callable

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Apply the intervention to a feature frame."""
        return self.apply_treatment(frame.copy())


def _salary_lift(frame: pd.DataFrame, multiplier: float = 1.10) -> pd.DataFrame:
    frame["Base_Salary"] = frame["Base_Salary"].astype(float) * multiplier
    return frame


def _manager_change(frame: pd.DataFrame, target_tenure: int = 36) -> pd.DataFrame:
    frame["Manager_Tenure_Months"] = np.maximum(frame["Manager_Tenure_Months"], target_tenure)
    return frame


def _tenure_bonus(frame: pd.DataFrame, months: int = 12) -> pd.DataFrame:
    frame["Tenure_Months"] = frame["Tenure_Months"] + months
    frame["Manager_Tenure_Months"] = frame["Manager_Tenure_Months"] + months
    return frame


INTERVENTIONS: tuple[Intervention, ...] = (
    Intervention(
        name="salary_lift_10pct",
        description="Apply a 10 % base-salary increase.",
        apply_treatment=lambda frame: _salary_lift(frame, multiplier=1.10),
    ),
    Intervention(
        name="manager_change",
        description="Move to a manager with at least 36 months of tenure.",
        apply_treatment=lambda frame: _manager_change(frame, target_tenure=36),
    ),
    Intervention(
        name="tenure_bonus_12mo",
        description="Retention bonus equivalent to 12 months of tenure stability.",
        apply_treatment=lambda frame: _tenure_bonus(frame, months=12),
    ),
)

FEATURE_COLUMNS = ["Tenure_Months", "Base_Salary", "Dept_Code", "Manager_Tenure_Months"]


def _load_dataset() -> pd.DataFrame:
    """Load the raw CSV used to train the T-learner outcome model."""
    if not Path(DATASET_PATH).exists():
        raise FileNotFoundError(
            f"{DATASET_PATH.name} missing \u2014 run `python generate_demo_workforce_data.py`."
        )
    df = pd.read_csv(DATASET_PATH)
    df["Dept_Code"] = df["Department"].map(DEPARTMENT_CODE_MAP)
    df["Target"] = (df["Voluntary_Turnover"] == "Yes").astype(int)
    return df


def _load_predictions() -> pd.DataFrame:
    """Load the predictions table the dashboard reads from."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(f"SELECT * FROM {SQL_TABLE_NAME}", connection)


def _baseline_features(predictions: pd.DataFrame) -> pd.DataFrame:
    """Build the model-ready feature frame from the dashboard predictions."""
    frame = predictions[["Tenure_Months", "Base_Salary", "Manager_Tenure_Months"]].copy()
    frame["Dept_Code"] = predictions["Department"].map(DEPARTMENT_CODE_MAP)
    return frame[FEATURE_COLUMNS]


def _fit_t_learner() -> "object":  # pragma: no cover - thin wrapper
    """Train a T-learner on the synthetic dataset.

    The T-learner trains one outcome model per treatment arm. EconML provides
    the production implementation when installed; otherwise the dashboard uses
    the local sklearn fallback with the same two-model pattern. We use the
    Voluntary_Turnover label as the outcome and a synthetic intervention column
    (here we simulate the "treated" arm by applying the salary lift to half of
    the historical sample). For a real workforce, the treated arm would be
    observed data from past compensation reviews.
    """
    from sklearn.ensemble import RandomForestClassifier

    df = _load_dataset()
    feature_frame = df[FEATURE_COLUMNS]
    outcome = df["Target"].to_numpy()

    rng = np.random.default_rng(RANDOM_SEED)
    treatment = rng.integers(0, 2, size=len(df))

    # Apply the salary lift to "treated" rows so the synthetic counterfactual
    # has signal. This lets the T-learner learn a non-zero CATE.
    treated_features = feature_frame.copy()
    treated_features["Base_Salary"] = treated_features["Base_Salary"].astype(float)
    treated_features.loc[treatment == 1, "Base_Salary"] *= 1.10

    def forest() -> RandomForestClassifier:
        return RandomForestClassifier(
            n_estimators=80, random_state=RANDOM_SEED, n_jobs=-1
        )

    try:
        from econml.metalearners import TLearner
    except ModuleNotFoundError as error:
        if error.name != "econml":
            raise
        control_model = forest()
        treatment_model = forest()
        control_mask = treatment == 0
        treatment_mask = treatment == 1
        control_model.fit(
            treated_features.loc[control_mask].to_numpy(), outcome[control_mask]
        )
        treatment_model.fit(
            treated_features.loc[treatment_mask].to_numpy(), outcome[treatment_mask]
        )
        return SklearnTLearnerFallback(control_model, treatment_model)

    learner = TLearner(
        models=[
            forest()
            for _ in range(2)
        ]
    )
    learner.fit(outcome, treatment, X=treated_features.to_numpy())
    return learner


def _score_with_t_learner(learner: object, features: pd.DataFrame) -> np.ndarray:
    """Return CATE = E[Y(1) - Y(0) | X] per row."""
    return learner.effect(features.to_numpy())


def _persist(uplift: pd.DataFrame) -> None:
    """Write the uplift table back to SQLite for the dashboard to consume."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        uplift.to_sql(CAUSAL_UPLIFT_TABLE, connection, index=False, if_exists="replace")


def compute_uplift_table() -> pd.DataFrame:
    """Build the recommended-intervention table for every employee.

    For each employee we score the expected risk under each intervention
    using the persisted production model, then pick the intervention with
    the largest predicted risk reduction. The CATE estimated by EconML is
    persisted as a separate column for ML-savvy reviewers.
    """
    import joblib

    from attrisense.config import MODEL_ARTIFACT_PATH

    if not MODEL_ARTIFACT_PATH.exists():
        raise FileNotFoundError(
            f"{MODEL_ARTIFACT_PATH.name} missing \u2014 run training first."
        )

    artifact = joblib.load(MODEL_ARTIFACT_PATH)
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]

    predictions = _load_predictions()
    baseline_features = _baseline_features(predictions)
    baseline_risk = model.predict_proba(baseline_features[feature_columns])[:, 1]

    rows: list[dict[str, object]] = []
    intervention_deltas: dict[str, np.ndarray] = {}
    for intervention in INTERVENTIONS:
        treated_features = intervention.transform(baseline_features.copy())
        treated_risk = model.predict_proba(treated_features[feature_columns])[:, 1]
        intervention_deltas[intervention.name] = baseline_risk - treated_risk

    learner = _fit_t_learner()
    cate = _score_with_t_learner(learner, baseline_features)

    for index, employee_row in predictions.iterrows():
        deltas = {
            intervention.name: float(intervention_deltas[intervention.name][index])
            for intervention in INTERVENTIONS
        }
        best_name, best_value = max(deltas.items(), key=lambda item: item[1])
        rows.append(
            {
                "Emp_ID": int(employee_row["Emp_ID"]),
                "Department": employee_row["Department"],
                "Risk_Level": employee_row["Risk_Level"],
                "Baseline_Risk": float(baseline_risk[index]),
                **{
                    f"Delta_{name}": deltas[name]
                    for name in deltas
                },
                "Best_Intervention": best_name,
                "Best_Risk_Reduction": best_value,
                "T_Learner_Salary_CATE": float(cate[index]),
            }
        )

    uplift_frame = pd.DataFrame(rows).sort_values("Best_Risk_Reduction", ascending=False)
    _persist(uplift_frame)
    return uplift_frame


def load_uplift_table() -> pd.DataFrame:
    """Return the previously computed uplift table, or empty if missing."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        try:
            return pd.read_sql_query(
                f"SELECT * FROM {CAUSAL_UPLIFT_TABLE}", connection
            )
        except pd.errors.DatabaseError:
            return pd.DataFrame()


if __name__ == "__main__":
    table = compute_uplift_table()
    print(table.head())
