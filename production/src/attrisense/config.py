# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/config.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Production configuration extension.

Adds production-only knobs without touching the root `config.py` so the
original dashboard contract stays stable.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the root package (config.py et al.) is importable when the
# production app is launched from any working directory.
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from config import (  # noqa: E402  (re-export root config)
    CALIBRATION_TABLE_NAME,
    DATABASE_PATH,
    DATASET_PATH,
    DEPARTMENT_CODE_MAP,
    FAISS_INDEX_DIR,
    MODEL_ARTIFACT_PATH,
    OUTPUTS_DIR,
    RANDOM_SEED,
    RISK_THRESHOLDS,
    SHAP_FEATURE_TABLE_NAME,
    SHAP_INSIGHTS_PATH,
    SQL_TABLE_NAME,
    SURVIVAL_CURVE_TABLE_NAME,
    ROOT_DIR,
)

# Production-only paths.
PRODUCTION_DIR = _ROOT / "production"
EVAL_DIR = PRODUCTION_DIR / "eval"
EVAL_GOLD_PATH = EVAL_DIR / "nl_sql_gold.json"
FAIRNESS_REPORT_PATH = OUTPUTS_DIR / "fairness_report.json"
EVAL_REPORT_PATH = OUTPUTS_DIR / "nl_sql_eval_report.json"
CAUSAL_UPLIFT_TABLE = "causal_uplift_recommendations"
MULTILINGUAL_INDEX_DIR = ROOT_DIR / "faiss_hr_index_multilingual"

# SHAP column contract (mirrors training script).
SHAP_COLUMNS = [
    "SHAP_Tenure_Impact",
    "SHAP_Compensation_Impact",
    "SHAP_Department_Impact",
    "SHAP_Manager_Tenure_Impact",
]
SHAP_DRIVER_LABELS = {
    "SHAP_Tenure_Impact": "Tenure",
    "SHAP_Compensation_Impact": "Compensation",
    "SHAP_Department_Impact": "Department",
    "SHAP_Manager_Tenure_Impact": "Manager tenure",
}

__all__ = [
    "CALIBRATION_TABLE_NAME",
    "CAUSAL_UPLIFT_TABLE",
    "DATABASE_PATH",
    "DATASET_PATH",
    "DEPARTMENT_CODE_MAP",
    "EVAL_DIR",
    "EVAL_GOLD_PATH",
    "EVAL_REPORT_PATH",
    "FAIRNESS_REPORT_PATH",
    "FAISS_INDEX_DIR",
    "MODEL_ARTIFACT_PATH",
    "MULTILINGUAL_INDEX_DIR",
    "OUTPUTS_DIR",
    "PRODUCTION_DIR",
    "RANDOM_SEED",
    "RISK_THRESHOLDS",
    "ROOT_DIR",
    "SHAP_COLUMNS",
    "SHAP_DRIVER_LABELS",
    "SHAP_FEATURE_TABLE_NAME",
    "SHAP_INSIGHTS_PATH",
    "SQL_TABLE_NAME",
    "SURVIVAL_CURVE_TABLE_NAME",
]
