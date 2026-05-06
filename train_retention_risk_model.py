"""Train the flight-risk model, explain predictions with SHAP, and publish outputs."""

from __future__ import annotations

import sqlite3

import numpy as np
import pandas as pd
import shap
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

from config import (
    DATABASE_PATH,
    DATASET_PATH,
    OUTPUTS_DIR,
    RANDOM_SEED,
    RISK_THRESHOLDS,
    SHAP_FEATURE_TABLE_NAME,
    SHAP_INSIGHTS_PATH,
    SQL_TABLE_NAME,
)


FEATURE_COLUMNS = ["Tenure_Months", "Base_Salary", "Dept_Code"]
SHAP_EXPLANATION_LIMIT = 1_200
FEATURE_METADATA = {
    "Tenure_Months": {
        "label": "Tenure",
        "shap_column": "SHAP_Tenure_Impact",
        "insight": "How employee tenure changes the model's voluntary-turnover probability.",
    },
    "Base_Salary": {
        "label": "Compensation",
        "shap_column": "SHAP_Compensation_Impact",
        "insight": "How base salary patterns influence modeled retention risk.",
    },
    "Dept_Code": {
        "label": "Department",
        "shap_column": "SHAP_Department_Impact",
        "insight": "How department-level risk patterns influence the score.",
    },
}


def categorize_risk(probability: float) -> str:
    """Convert a numeric model probability into an HR-friendly risk band.

    Args:
        probability: Model-estimated chance that an employee voluntarily leaves.

    Returns:
        One of `High Risk`, `Medium Risk`, or `Low Risk`.
    """
    if probability > RISK_THRESHOLDS["high"]:
        return "High Risk"
    if probability > RISK_THRESHOLDS["medium"]:
        return "Medium Risk"
    return "Low Risk"


def load_dataset() -> pd.DataFrame:
    """Load the synthetic workforce CSV and explain how to create it if missing."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATASET_PATH.name}. Run `python generate_demo_workforce_data.py` first."
        )
    return pd.read_csv(DATASET_PATH)


def prepare_model_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Add numeric model columns while preserving the original HR-facing fields.

    The dashboard needs department names, but the model needs numeric features.
    This helper keeps that translation in one small, auditable place.
    """
    model_df = df.copy()
    model_df["Dept_Code"] = model_df["Department"].astype("category").cat.codes
    model_df["Target"] = (model_df["Voluntary_Turnover"] == "Yes").astype(int)
    return model_df


def train_model(feature_frame: pd.DataFrame, target: pd.Series) -> RandomForestClassifier:
    """Train a balanced Random Forest model for voluntary-turnover prediction."""
    # Turnover events are intentionally rare. SMOTE balances the training set
    # so the classifier learns minority-class risk patterns instead of defaulting
    # to "everyone is safe".
    smote = SMOTE(random_state=RANDOM_SEED)
    x_resampled, y_resampled = smote.fit_resample(feature_frame, target)

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=RANDOM_SEED,
        class_weight="balanced_subsample",
        n_jobs=-1,
    )
    model.fit(x_resampled, y_resampled)
    return model


def extract_positive_class_shap_values(raw_shap_values: object) -> np.ndarray:
    """Return SHAP values for class 1, which means voluntary turnover.

    SHAP versions represent classifier outputs differently. SHAP 0.51 returns
    an array shaped `(rows, features, classes)` for this Random Forest; older
    versions may return a list with one matrix per class. This function hides
    that compatibility detail from the rest of the pipeline.
    """
    if isinstance(raw_shap_values, list):
        return np.asarray(raw_shap_values[1])

    shap_array = np.asarray(raw_shap_values)
    if shap_array.ndim == 3:
        return shap_array[:, :, 1]
    if shap_array.ndim == 2:
        return shap_array

    raise ValueError(f"Unsupported SHAP value shape: {shap_array.shape}")


def calculate_shap_values(
    model: RandomForestClassifier,
    feature_frame: pd.DataFrame,
) -> np.ndarray:
    """Calculate per-employee SHAP values for the trained model.

    Returns:
        A matrix with one row per employee and one column per model feature.
    """
    explainer = shap.TreeExplainer(model)
    raw_shap_values = explainer.shap_values(feature_frame)
    return extract_positive_class_shap_values(raw_shap_values)


def select_shap_explanation_rows(predictions: pd.DataFrame) -> pd.Index:
    """Choose employees that should receive individual SHAP explanations.

    The dashboard promise is strongest for employees who need action, so every
    high-risk employee is included first. The remaining budget is filled with a
    deterministic risk-weighted sample so global feature impact still reflects
    more than only the highest-risk segment.
    """
    high_risk_index = predictions.index[predictions["Risk_Level"] == "High Risk"]
    remaining_budget = max(SHAP_EXPLANATION_LIMIT - len(high_risk_index), 0)

    if remaining_budget == 0:
        return high_risk_index

    candidate_pool = predictions.drop(index=high_risk_index)
    sample_size = min(remaining_budget, len(candidate_pool))
    sampled_index = candidate_pool.sample(
        n=sample_size,
        weights=candidate_pool["Flight_Risk_Probability"] + 0.01,
        random_state=RANDOM_SEED,
    ).index
    return high_risk_index.union(sampled_index).sort_values()


def add_employee_explanations(
    predictions: pd.DataFrame,
    shap_values: np.ndarray,
    explained_index: pd.Index,
) -> pd.DataFrame:
    """Attach SHAP columns and primary-driver fields to each employee row."""
    explained = predictions.copy()
    shap_columns = [FEATURE_METADATA[column]["shap_column"] for column in FEATURE_COLUMNS]
    shap_frame = pd.DataFrame(shap_values, columns=shap_columns, index=explained_index)
    for column in shap_columns:
        explained[column] = np.nan
    explained.loc[explained_index, shap_columns] = shap_frame
    explained["SHAP_Explained"] = False
    explained.loc[explained_index, "SHAP_Explained"] = True

    # The largest absolute SHAP value is the strongest driver for that specific
    # employee. Positive values push the model toward higher turnover risk;
    # negative values push it toward lower turnover risk.
    shap_matrix = shap_frame.to_numpy()
    primary_indexes = np.abs(shap_matrix).argmax(axis=1)
    labels = [FEATURE_METADATA[column]["label"] for column in FEATURE_COLUMNS]
    explained["Primary_Risk_Driver"] = "Not explained"
    explained["Primary_Driver_Impact"] = np.nan
    explained.loc[explained_index, "Primary_Risk_Driver"] = [
        labels[index] for index in primary_indexes
    ]
    explained.loc[explained_index, "Primary_Driver_Impact"] = shap_matrix[
        np.arange(len(shap_frame)),
        primary_indexes,
    ]
    explained["Primary_Driver_Direction"] = "Not explained"
    explained.loc[explained_index, "Primary_Driver_Direction"] = np.where(
        explained.loc[explained_index, "Primary_Driver_Impact"] >= 0,
        "Increases risk",
        "Reduces risk",
    )
    return explained


def build_feature_impact_table(shap_values: np.ndarray, sample_size: int) -> pd.DataFrame:
    """Summarize global model drivers for dashboard-level explanation."""
    rows = []
    for index, feature_name in enumerate(FEATURE_COLUMNS):
        metadata = FEATURE_METADATA[feature_name]
        feature_values = shap_values[:, index]
        rows.append(
            {
                "Feature": metadata["label"],
                "Source_Column": feature_name,
                "Mean_ABS_SHAP": float(np.abs(feature_values).mean()),
                "Average_SHAP": float(feature_values.mean()),
                "Explained_Employee_Count": sample_size,
                "Business_Insight": metadata["insight"],
            }
        )

    return pd.DataFrame(rows).sort_values("Mean_ABS_SHAP", ascending=False)


def build_predictions_with_explanations(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Train the model, score employees, and create SHAP explanation artifacts."""
    model_df = prepare_model_frame(df)
    feature_frame = model_df[FEATURE_COLUMNS]
    target = model_df["Target"]

    model = train_model(feature_frame, target)

    # `predict_proba` returns two columns: probability of class 0 and class 1.
    # Class 1 means voluntary turnover, so column index 1 is the flight-risk score.
    predictions = df.copy()
    predictions["Flight_Risk_Probability"] = model.predict_proba(feature_frame)[:, 1]
    predictions["Risk_Level"] = predictions["Flight_Risk_Probability"].apply(categorize_risk)

    explained_index = select_shap_explanation_rows(predictions)
    shap_values = calculate_shap_values(model, feature_frame.loc[explained_index])
    predictions = add_employee_explanations(predictions, shap_values, explained_index)
    feature_impact = build_feature_impact_table(shap_values, len(explained_index))
    return predictions, feature_impact


def build_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """Train a model and add flight-risk predictions to each employee row.

    This compatibility wrapper preserves the older public function contract for
    notebooks or scripts that only need the scored employee table.
    """
    predictions, _ = build_predictions_with_explanations(df)
    return predictions


def write_shap_insights(
    predictions: pd.DataFrame,
    feature_impact: pd.DataFrame,
) -> None:
    """Write a plain-English SHAP summary for README evidence and reviewers."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    high_risk = predictions[predictions["Risk_Level"] == "High Risk"].copy()
    explained_high_risk = high_risk[high_risk["SHAP_Explained"]]
    high_risk_driver_counts = explained_high_risk["Primary_Risk_Driver"].value_counts()
    estimated_salary_exposure = (
        high_risk["Base_Salary"] * high_risk["Flight_Risk_Probability"] * 0.5
    ).sum()

    lines = [
        "AttriSense SHAP Explainability Insights",
        "======================================",
        "",
        f"Explained employees: {len(predictions):,}",
        f"Employees with SHAP values: {int(predictions['SHAP_Explained'].sum()):,}",
        f"High-risk employees explained: {len(explained_high_risk):,}",
        f"Estimated high-risk salary exposure: ${estimated_salary_exposure:,.0f}",
        "",
        "Global model drivers by mean absolute SHAP value:",
    ]
    for _, row in feature_impact.iterrows():
        lines.append(
            f"- {row['Feature']}: {row['Mean_ABS_SHAP']:.4f} "
            f"(average direction {row['Average_SHAP']:+.4f})"
        )

    lines.extend(["", "Primary drivers among high-risk employees:"])
    for driver, count in high_risk_driver_counts.items():
        lines.append(f"- {driver}: {count:,} employees")

    lines.extend(
        [
            "",
            "Business interpretation:",
            "- SHAP makes every risk score explainable, which is required for executive trust.",
            "- Primary drivers help HR choose targeted interventions instead of generic retention actions.",
            "- Global driver ranking creates a board-ready story about the levers behind workforce risk.",
        ]
    )

    SHAP_INSIGHTS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_model_outputs(predictions: pd.DataFrame, feature_impact: pd.DataFrame) -> None:
    """Write model outputs and SHAP feature impact to SQLite."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        predictions.to_sql(SQL_TABLE_NAME, conn, if_exists="replace", index=False)
        feature_impact.to_sql(SHAP_FEATURE_TABLE_NAME, conn, if_exists="replace", index=False)


def save_predictions(df: pd.DataFrame) -> None:
    """Write model outputs to SQLite so Streamlit and AI SQL can read them."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        df.to_sql(SQL_TABLE_NAME, conn, if_exists="replace", index=False)


def main() -> None:
    """Run the full modeling step from CSV input to SQLite and SHAP outputs."""
    print("Loading workforce data...")
    predictions, feature_impact = build_predictions_with_explanations(load_dataset())
    save_model_outputs(predictions, feature_impact)
    write_shap_insights(predictions, feature_impact)
    print(
        f"Saved {len(predictions):,} employee risk scores to "
        f"{DATABASE_PATH.name}:{SQL_TABLE_NAME}."
    )
    print(
        f"Saved SHAP feature impact to {DATABASE_PATH.name}:{SHAP_FEATURE_TABLE_NAME} "
        f"and {SHAP_INSIGHTS_PATH}."
    )


if __name__ == "__main__":
    main()
