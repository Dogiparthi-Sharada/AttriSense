# ---------------------------------------------------------------------------
# AttriSense — production/tests/test_fairness.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Tests for the fairness audit module."""

from __future__ import annotations

import pandas as pd

from attrisense.fairness import audit_dimension


def _toy_frame() -> pd.DataFrame:
    """Build a tiny in-memory predictions frame for unit tests."""
    return pd.DataFrame(
        [
            {"Department": "Manufacturing", "Risk_Level": "High Risk",
             "Flight_Risk_Probability": 0.9, "Voluntary_Turnover": "Yes"},
            {"Department": "Manufacturing", "Risk_Level": "High Risk",
             "Flight_Risk_Probability": 0.8, "Voluntary_Turnover": "Yes"},
            {"Department": "Manufacturing", "Risk_Level": "Low Risk",
             "Flight_Risk_Probability": 0.1, "Voluntary_Turnover": "No"},
            {"Department": "Engineering", "Risk_Level": "Low Risk",
             "Flight_Risk_Probability": 0.05, "Voluntary_Turnover": "No"},
            {"Department": "Engineering", "Risk_Level": "Low Risk",
             "Flight_Risk_Probability": 0.1, "Voluntary_Turnover": "No"},
        ]
    )


def test_audit_returns_one_row_per_group() -> None:
    """The audit must produce one GroupMetrics row per unique department."""
    report = audit_dimension(_toy_frame(), "Department")
    departments = {group.group for group in report.groups}
    assert departments == {"Manufacturing", "Engineering"}


def test_disparate_impact_low_when_one_group_dominates() -> None:
    """A 100 %-vs-0 % high-risk split must produce a low DI ratio."""
    frame = pd.DataFrame(
        [
            *(
                {"Department": "A", "Risk_Level": "High Risk",
                 "Flight_Risk_Probability": 0.9, "Voluntary_Turnover": "Yes"}
                for _ in range(40)
            ),
            *(
                {"Department": "B", "Risk_Level": "Low Risk",
                 "Flight_Risk_Probability": 0.1, "Voluntary_Turnover": "No"}
                for _ in range(40)
            ),
        ]
    )
    report = audit_dimension(frame, "Department")
    assert report.disparate_impact_ratio == 0.0
    assert report.passes_four_fifths_rule is False


def test_low_confidence_groups_are_flagged() -> None:
    """Groups smaller than 30 rows must be marked low-confidence."""
    report = audit_dimension(_toy_frame(), "Department")
    assert all(group.low_confidence for group in report.groups)
