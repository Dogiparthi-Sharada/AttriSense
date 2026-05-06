"""Generate a reproducible synthetic workforce dataset for AttriSense."""

from __future__ import annotations

import numpy as np
import pandas as pd

from project_config import DATASET_PATH, RANDOM_SEED


EMPLOYEE_COUNT = 5_000
DEPARTMENTS = ("Manufacturing", "Engineering", "Sales")
DEPARTMENT_WEIGHTS = (0.60, 0.25, 0.15)

EXIT_NOTES = (
    "The hiring volume is intense, and trainer availability is limited.",
    "Great team, but the manufacturing shifts are difficult to sustain.",
    "I was not fully trained on the optical assembly workflow.",
    "The floor is moving fast, and new hires need more support.",
)


def build_workforce(seed: int = RANDOM_SEED, rows: int = EMPLOYEE_COUNT) -> pd.DataFrame:
    """Create a fake-but-realistic employee table for demos.

    Args:
        seed: Random seed. Keeping this fixed makes the same demo data every run.
        rows: Number of employee rows to generate.

    Returns:
        A pandas DataFrame with demographic fields, turnover labels, and exit notes.
    """
    rng = np.random.default_rng(seed)

    # First create the stable facts about each employee. These are the same
    # kinds of fields an HRIS export would normally contain.
    df = pd.DataFrame(
        {
            "Emp_ID": range(1000, 1000 + rows),
            "Department": rng.choice(DEPARTMENTS, rows, p=DEPARTMENT_WEIGHTS),
            "Tenure_Months": rng.integers(1, 60, rows),
            "Base_Salary": rng.integers(60_000, 150_000, rows),
        }
    )

    new_manufacturing_hire = (
        (df["Department"] == "Manufacturing") & (df["Tenure_Months"] < 6)
    )

    # The synthetic signal makes early-tenure manufacturing employees more
    # likely to leave, giving the ML model a realistic pattern to learn.
    turnover_probability = np.where(new_manufacturing_hire, 0.70, 0.10)
    df["Voluntary_Turnover"] = np.where(
        rng.random(rows) < turnover_probability, "Yes", "No"
    )

    # Exit interviews are unstructured text. They give the RAG pipeline
    # something realistic to embed without using real employee statements.
    df["Exit_Interview"] = np.where(
        df["Voluntary_Turnover"] == "Yes",
        rng.choice(EXIT_NOTES, rows),
        "N/A - Active Employee",
    )
    return df


def main() -> None:
    """Generate the CSV file used by the rest of the AttriSense pipeline."""
    df = build_workforce()
    df.to_csv(DATASET_PATH, index=False)
    print(f"Generated {len(df):,} synthetic employees at {DATASET_PATH.name}.")


if __name__ == "__main__":
    main()
