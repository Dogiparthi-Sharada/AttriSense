"""Train the flight-risk model and publish predictions to SQLite."""

from __future__ import annotations

import sqlite3

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier

from config import DATABASE_PATH, DATASET_PATH, RANDOM_SEED, RISK_THRESHOLDS, SQL_TABLE_NAME


FEATURE_COLUMNS = ["Tenure_Months", "Base_Salary", "Dept_Code"]


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


def build_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """Train a model and add flight-risk predictions to each employee row.

    Args:
        df: Raw workforce dataset from `generate_demo_workforce_data.py`.

    Returns:
        The original rows with `Flight_Risk_Probability` and `Risk_Level` added.
    """
    df = df.copy()

    # Machine-learning models need numbers, not text labels. Category codes turn
    # Manufacturing/Engineering/Sales into small integers while keeping the
    # original Department column for the dashboard.
    df["Dept_Code"] = df["Department"].astype("category").cat.codes
    df["Target"] = (df["Voluntary_Turnover"] == "Yes").astype(int)

    x = df[FEATURE_COLUMNS]
    y = df["Target"]

    # Turnover events are intentionally rare. SMOTE balances the training set
    # so the classifier learns minority-class risk patterns instead of defaulting
    # to "everyone is safe".
    smote = SMOTE(random_state=RANDOM_SEED)
    x_resampled, y_resampled = smote.fit_resample(x, y)

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=RANDOM_SEED,
        class_weight="balanced_subsample",
        n_jobs=-1,
    )
    model.fit(x_resampled, y_resampled)

    # `predict_proba` returns two columns: probability of class 0 and class 1.
    # Class 1 means voluntary turnover, so column index 1 is the flight-risk score.
    df["Flight_Risk_Probability"] = model.predict_proba(x)[:, 1]
    df["Risk_Level"] = df["Flight_Risk_Probability"].apply(categorize_risk)
    return df.drop(columns=["Dept_Code", "Target"])


def save_predictions(df: pd.DataFrame) -> None:
    """Write model outputs to SQLite so Streamlit and AI SQL can read them."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        df.to_sql(SQL_TABLE_NAME, conn, if_exists="replace", index=False)


def main() -> None:
    """Run the full modeling step from CSV input to SQLite output."""
    print("Loading workforce data...")
    predictions = build_predictions(load_dataset())
    save_predictions(predictions)
    print(
        f"Saved {len(predictions):,} employee risk scores to "
        f"{DATABASE_PATH.name}:{SQL_TABLE_NAME}."
    )


if __name__ == "__main__":
    main()
