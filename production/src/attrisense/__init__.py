# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/__init__.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""AttriSense production package.

This package layers production-grade additions on top of the original
AttriSense scripts WITHOUT modifying them. Original `streamlit_app.py`,
`train_retention_risk_model.py`, and `natural_language_sql.py` continue
to work unchanged.

The production layer adds:
- Compare-Two-Employees side-by-side SHAP view
- First-time-user onboarding tour
- Fairness audit (department / manager / risk-band parity, calibration drift)
- NL\u2192SQL evaluation harness with 50 gold questions
- Causal uplift modelling (econml) for intervention recommendation
- Multilingual exit-interview RAG (English / Spanish / Hindi)
- Slack-style manager alert mock
"""

__version__ = "2.0.0"
