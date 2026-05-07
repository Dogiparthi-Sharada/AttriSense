"""Fairness audit for AttriSense.

Computes group-level metrics that hiring managers, ethics reviewers, and
NYC Local Law 144 auditors care about:

- Selection-rate parity (high-risk percentage by group)
- Disparate-impact ratio (lowest group rate / highest group rate)
- Calibration drift per group (mean predicted vs observed turnover)
- Cohort sample sizes (small groups flagged as low-confidence)

The audit is data-only \u2014 no UI, no LLM \u2014 so it can run in CI.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

from attrisense.config import (
    DATABASE_PATH,
    FAIRNESS_REPORT_PATH,
    OUTPUTS_DIR,
    SQL_TABLE_NAME,
)


# Disparate-impact ratio < 0.80 is the EEOC four-fifths rule of thumb.
DISPARATE_IMPACT_THRESHOLD = 0.80
MIN_GROUP_SAMPLE_SIZE = 30


@dataclass
class GroupMetrics:
    """Fairness metrics for one demographic / organisational group."""

    group: str
    sample_size: int
    high_risk_rate: float
    mean_predicted_probability: float
    observed_turnover_rate: float
    calibration_gap: float

    @property
    def low_confidence(self) -> bool:
        """True when the cohort is too small for reliable fairness inference."""
        return self.sample_size < MIN_GROUP_SAMPLE_SIZE


@dataclass
class FairnessReport:
    """Top-level fairness report stored to disk and shown in the dashboard."""

    dimension: str
    groups: list[GroupMetrics]
    disparate_impact_ratio: float
    passes_four_fifths_rule: bool
    notes: list[str]

    def to_dict(self) -> dict:
        """Serialise for JSON output."""
        return {
            "dimension": self.dimension,
            "disparate_impact_ratio": self.disparate_impact_ratio,
            "passes_four_fifths_rule": self.passes_four_fifths_rule,
            "notes": self.notes,
            "groups": [asdict(group) for group in self.groups],
        }


def _load_predictions() -> pd.DataFrame:
    """Read the workforce_predictions table or raise a helpful error."""
    if not Path(DATABASE_PATH).exists():
        raise FileNotFoundError(
            f"{DATABASE_PATH.name} missing \u2014 run `python train_retention_risk_model.py`."
        )
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(f"SELECT * FROM {SQL_TABLE_NAME}", connection)


def audit_dimension(df: pd.DataFrame, dimension: str) -> FairnessReport:
    """Build a FairnessReport for any categorical column in the predictions table.

    Args:
        df: The workforce_predictions DataFrame.
        dimension: A column name to slice on (e.g. "Department", "Manager_ID").
    """
    if dimension not in df.columns:
        raise KeyError(f"Column {dimension!r} is not in the predictions table.")

    groups: list[GroupMetrics] = []
    notes: list[str] = []

    # Observed turnover comes from the original CSV label, materialised back
    # into the predictions table by the training script.
    observed_column = "Voluntary_Turnover" if "Voluntary_Turnover" in df.columns else None

    for group_name, group_df in df.groupby(dimension):
        sample_size = len(group_df)
        high_risk_rate = float((group_df["Risk_Level"] == "High Risk").mean())
        mean_predicted = float(group_df["Flight_Risk_Probability"].mean())
        if observed_column:
            observed = float((group_df[observed_column] == "Yes").mean())
        else:
            observed = float("nan")
        calibration_gap = (
            float(mean_predicted - observed) if observed == observed else float("nan")
        )

        metrics = GroupMetrics(
            group=str(group_name),
            sample_size=sample_size,
            high_risk_rate=high_risk_rate,
            mean_predicted_probability=mean_predicted,
            observed_turnover_rate=observed,
            calibration_gap=calibration_gap,
        )
        groups.append(metrics)
        if metrics.low_confidence:
            notes.append(
                f"Group {metrics.group!r} has only {metrics.sample_size} rows; "
                f"fairness statistics are low-confidence."
            )

    rates = [group.high_risk_rate for group in groups if not group.low_confidence]
    if rates:
        max_rate = max(rates)
        min_rate = min(rates)
        disparate_impact_ratio = (min_rate / max_rate) if max_rate > 0 else 1.0
    else:
        disparate_impact_ratio = float("nan")
        notes.append("All groups are low-confidence; disparate-impact ratio is undefined.")

    passes = (
        disparate_impact_ratio == disparate_impact_ratio
        and disparate_impact_ratio >= DISPARATE_IMPACT_THRESHOLD
    )
    if not passes and disparate_impact_ratio == disparate_impact_ratio:
        notes.append(
            f"Disparate-impact ratio {disparate_impact_ratio:.2f} is below the "
            f"EEOC four-fifths rule threshold of {DISPARATE_IMPACT_THRESHOLD:.2f}. "
            "Investigate whether the underlying signal is acceptable."
        )

    return FairnessReport(
        dimension=dimension,
        groups=sorted(groups, key=lambda g: g.high_risk_rate, reverse=True),
        disparate_impact_ratio=disparate_impact_ratio,
        passes_four_fifths_rule=passes,
        notes=notes,
    )


def run_audit(dimensions: Iterable[str] = ("Department",)) -> dict[str, FairnessReport]:
    """Run the audit across the chosen dimensions and write a JSON report."""
    df = _load_predictions()
    reports = {dimension: audit_dimension(df, dimension) for dimension in dimensions}
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    serialisable = {dimension: report.to_dict() for dimension, report in reports.items()}
    FAIRNESS_REPORT_PATH.write_text(json.dumps(serialisable, indent=2))
    return reports


def load_report() -> dict | None:
    """Read the JSON report from disk if a previous run exists."""
    if not FAIRNESS_REPORT_PATH.exists():
        return None
    return json.loads(FAIRNESS_REPORT_PATH.read_text())


if __name__ == "__main__":
    audit_results = run_audit(("Department",))
    for dimension, report in audit_results.items():
        print(f"\n=== Fairness audit: {dimension} ===")
        print(f"Disparate-impact ratio: {report.disparate_impact_ratio:.3f}")
        print(f"Passes four-fifths rule: {report.passes_four_fifths_rule}")
        for note in report.notes:
            print(f"  - {note}")
        for group in report.groups:
            print(
                f"  {group.group:<20} n={group.sample_size:<5} "
                f"high_risk={group.high_risk_rate:.3f} "
                f"calib_gap={group.calibration_gap:+.3f}"
            )
