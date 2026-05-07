# ---------------------------------------------------------------------------
# AttriSense — config.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Shared paths and defaults for AttriSense.

Keeping filenames in one place makes the pipeline easier to rename, test, and
deploy without hunting through every script.
"""

from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent

# File outputs shared by multiple scripts. Keeping them here prevents filename
# drift between the generator, model, dashboard, and README.
DATASET_PATH = ROOT_DIR / "attrisense_synthetic_hr.csv"
DATABASE_PATH = ROOT_DIR / "hr_enterprise.db"
FAISS_INDEX_DIR = ROOT_DIR / "faiss_hr_index"
DASHBOARD_PATH = ROOT_DIR / "streamlit_app.py"
OUTPUTS_DIR = ROOT_DIR / "outputs"
SHAP_INSIGHTS_PATH = OUTPUTS_DIR / "shapInsights.txt"
MODEL_ARTIFACT_PATH = ROOT_DIR / "attrisense_model.joblib"

# The dashboard and AI assistant both read from this SQLite table.
SQL_TABLE_NAME = "workforce_predictions"
SHAP_FEATURE_TABLE_NAME = "shap_feature_impact"
CALIBRATION_TABLE_NAME = "model_calibration"
SURVIVAL_CURVE_TABLE_NAME = "survival_curves"

# Keep department encoding explicit so training and live what-if simulation match.
DEPARTMENT_CODE_MAP = {
    "Engineering": 0,
    "Manufacturing": 1,
    "Sales": 2,
}

# A fixed seed keeps demo outputs reproducible across machines.
RANDOM_SEED = 42

# These thresholds translate model probabilities into business language.
RISK_THRESHOLDS = {
    "high": 0.75,
    "medium": 0.40,
}
