<!--
AttriSense — docs/operations/configuration.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Configuration

> All knobs in one place. Most users never touch any of them.

## `config.py` — the canonical source

[`config.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/config.py) at the repo root. Every path, table name, and threshold lives here:

```python
ROOT_DIR = Path(__file__).resolve().parent

DATASET_PATH        = ROOT_DIR / "attrisense_synthetic_hr.csv"
DATABASE_PATH       = ROOT_DIR / "hr_enterprise.db"
FAISS_INDEX_DIR     = ROOT_DIR / "faiss_hr_index"
DASHBOARD_PATH      = ROOT_DIR / "streamlit_app.py"
OUTPUTS_DIR         = ROOT_DIR / "outputs"
SHAP_INSIGHTS_PATH  = OUTPUTS_DIR / "shapInsights.txt"
MODEL_ARTIFACT_PATH = ROOT_DIR / "attrisense_model.joblib"

SQL_TABLE_NAME              = "workforce_predictions"
SHAP_FEATURE_TABLE_NAME     = "shap_feature_impact"
CALIBRATION_TABLE_NAME      = "model_calibration"
SURVIVAL_CURVE_TABLE_NAME   = "survival_curves"

DEPARTMENT_CODE_MAP = {"Engineering": 0, "Manufacturing": 1, "Sales": 2}
RANDOM_SEED = 42
RISK_THRESHOLDS = {"high": 0.75, "medium": 0.40}
```

## `production/src/attrisense/config.py` — the production extension

Re-exports root config and adds a few production-only paths:

```python
from config import *  # everything from the root

CAUSAL_UPLIFT_TABLE       = ROOT_DIR / "data" / "causal_uplift.csv"
MULTILINGUAL_INDEX_DIR    = ROOT_DIR / "data" / "multilingual_index"
EVAL_GOLD_PATH            = ROOT_DIR / "production" / "src" / "attrisense" / "gold_questions.py"
FAIRNESS_REPORT_PATH      = OUTPUTS_DIR / "fairness_report.json"
EVAL_REPORT_PATH          = OUTPUTS_DIR / "nl_sql_eval_report.json"
SHAP_COLUMNS              = (...)
SHAP_DRIVER_LABELS        = {...}
```

## `.env` — runtime secrets

Lives at the repo root. Never committed (see `.gitignore` line 58).

```bash
# .env
OPENAI_API_KEY=sk-...

# Optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
```

The dashboard auto-loads this file at startup via:

```python
load_dotenv(dotenv_path=_REPO_ROOT / ".env", override=False)
```

(in [`production/streamlit_app.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/streamlit_app.py)). See [Secrets handling](secrets.md).

## `.streamlit/config.toml` — Streamlit knobs

```toml
[server]
headless = true
runOnSave = true

[theme]
# We override most theme via theme.py CSS injection,
# but these set Streamlit's fallback defaults.
base = "dark"
primaryColor = "#22D3EE"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#E2E8F0"
font = "sans serif"
```

## `production/pyproject.toml` — package metadata

```toml
[project]
name = "attrisense"
version = "2.0.0"
requires-python = ">=3.11"

[project.optional-dependencies]
dev   = ["pytest", "ruff", "black", "mypy", "pytest-cov"]
causal = ["econml"]
docs   = ["mkdocs-material", "mkdocs-glightbox"]
```

## Tuning the model

| Knob | Default | Where | Effect |
|---|---|---|---|
| `n_estimators` | 300 | `train_retention_risk_model.py` | Bias / variance / training time |
| `max_depth` | 8 | same | Overfitting risk |
| `RANDOM_SEED` | 42 | `config.py` | Reproducibility |
| Risk thresholds | 0.75 / 0.40 | `config.py` `RISK_THRESHOLDS` | Strictness of flagging |
| SMOTE k_neighbors | default (5) | same | Smoothness of synthetic minority class |

After changing any of these, retrain:

```bash
python train_retention_risk_model.py
```

Then refresh the dashboard tab — `@st.cache_data` invalidates on next reload.

## Tuning the AI

| Knob | Default | Where |
|---|---|---|
| LLM model | `gpt-3.5-turbo` | [`natural_language_sql.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/natural_language_sql.py) |
| Embedding model | `text-embedding-3-small` | `multilingual_rag.py:_try_openai_embeddings()` |
| Reachability probe timeout | 5s | same |
| Hashing fallback dimensions | 256 | `HashingEmbeddings(dimensions=256)` |
| Top-K results | 6 (RAG) / 3 (fallback) | tab handlers |
| Fallback gold questions | 50 | `gold_questions.py` |

## Tuning the theme

[`theme.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/theme.py) — every color and gradient.

To swap to a light theme: change the palette constants at the top of the file, then update `plotly_layout()` to use light backgrounds. The dashboard picks up changes on next reload — no rebuild needed.

## What you should NOT change

- `DEPARTMENT_CODE_MAP` — must stay aligned between training and inference. Changing it breaks the joblib estimator until you retrain.
- `SQL_TABLE_NAME` constants — multiple tabs assume them. Renaming requires a sweep.
- `RANDOM_SEED` — only change for legitimate experiments. The README screenshots and the gold questions all assume seed 42.
