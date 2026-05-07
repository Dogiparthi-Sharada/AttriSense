# ---------------------------------------------------------------------------
# AttriSense — generate_demo_workforce_data.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Generate a reproducible synthetic workforce dataset for AttriSense."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import DATASET_PATH, RANDOM_SEED


EMPLOYEE_COUNT = 5_000
DEPARTMENTS = ("Manufacturing", "Engineering", "Sales")
DEPARTMENT_WEIGHTS = (0.60, 0.25, 0.15)
MANAGER_POOLS = {
    "Manufacturing": range(20_100, 20_145),
    "Engineering": range(30_100, 30_124),
    "Sales": range(40_100, 40_116),
}

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

    manager_tenure_by_id = {
        manager_id: int(rng.integers(3, 72))
        for manager_ids in MANAGER_POOLS.values()
        for manager_id in manager_ids
    }

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
    df["Manager_ID"] = [
        int(rng.choice(tuple(MANAGER_POOLS[department])))
        for department in df["Department"]
    ]
    df["Manager_Tenure_Months"] = df["Manager_ID"].map(manager_tenure_by_id)

    new_manufacturing_hire = (
        (df["Department"] == "Manufacturing") & (df["Tenure_Months"] < 6)
    )
    new_manager = df["Manager_Tenure_Months"] < 12

    # The synthetic signal makes early-tenure manufacturing employees more
    # likely to leave. New manager relationships add a second signal for the
    # manager-risk rollup without requiring real HR data.
    turnover_probability = np.where(new_manufacturing_hire, 0.70, 0.10)
    turnover_probability = np.clip(
        turnover_probability + np.where(new_manager, 0.08, 0.0),
        0.02,
        0.90,
    )
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
