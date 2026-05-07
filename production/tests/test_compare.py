"""Tests for the Compare-Two-Employees helpers."""

from __future__ import annotations

import pandas as pd

from attrisense.compare import headline_drivers


def test_headline_drivers_returns_top_k_pairs() -> None:
    """`top_k=2` must return exactly two driver strings."""
    employee = pd.Series(
        {
            "SHAP_Tenure_Impact": 0.4,
            "SHAP_Compensation_Impact": -0.1,
            "SHAP_Department_Impact": 0.05,
            "SHAP_Manager_Tenure_Impact": -0.3,
        }
    )
    drivers = headline_drivers(employee, top_k=2)
    assert len(drivers) == 2
    assert "Tenure" in drivers[0]
    assert "Manager tenure" in drivers[1]


def test_headline_drivers_handles_missing_values() -> None:
    """Missing SHAP columns must not raise."""
    drivers = headline_drivers(pd.Series({"unrelated": 1.0}), top_k=2)
    assert isinstance(drivers, list)
