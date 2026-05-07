"""Sanity tests for `attrisense.config`."""

from __future__ import annotations

from attrisense import config


def test_paths_exist_in_package() -> None:
    """Production paths must resolve to absolute paths under the repo root."""
    assert config.PRODUCTION_DIR.is_dir()
    assert config.PRODUCTION_DIR.name == "production"


def test_shap_columns_match_labels() -> None:
    """Each SHAP column must map to a human-readable driver label."""
    assert set(config.SHAP_COLUMNS) == set(config.SHAP_DRIVER_LABELS)


def test_department_code_map_keys() -> None:
    """Department map must cover the three demo departments."""
    assert {"Engineering", "Manufacturing", "Sales"} <= set(config.DEPARTMENT_CODE_MAP)


def test_risk_thresholds_ordered() -> None:
    """The high threshold must always be greater than the medium threshold."""
    assert config.RISK_THRESHOLDS["high"] > config.RISK_THRESHOLDS["medium"]
