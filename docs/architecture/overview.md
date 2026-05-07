<!--
AttriSense — docs/architecture/overview.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Architecture overview

> AttriSense is six layers stacked on top of one Python module. Each layer has one job, one entry point, and one set of outputs. You can read the whole system end-to-end in an afternoon.

![AttriSense Architecture](../images/diagrams/architecture.png)


```
┌─────────────────────────────────────────────────────────────────────┐
│                        STREAMLIT DASHBOARD                          │
│  Executive · SHAP · Compare · Uplift · Fairness · AI · Eval · RAG   │
│  Alert · Ethics                                                     │
└─────────────────────────┬───────────────────────────────────────────┘
                          │ reads
┌─────────────────────────▼───────────────────────────────────────────┐
│                     APPLICATION LAYER  (production/src/attrisense/) │
│  compare · onboarding · fairness · causal_uplift · multilingual_rag │
│  nl_sql_eval · nl_sql_fallback · slack_alert_mock · theme           │
└──┬─────────────────────────────────┬────────────────────────────────┘
   │                                 │
   │ imports                         │ writes
   ▼                                 ▼
┌──────────────────────────┐  ┌─────────────────────────────────────┐
│   AI / RAG SERVICES      │  │   DATA / ML LAYER (root)            │
│   natural_language_sql   │  │   train_retention_risk_model        │
│   build_exit_interview…  │  │   generate_demo_workforce_data      │
│   (LangChain + OpenAI    │  │   (sklearn + SMOTE + SHAP +         │
│    + FAISS)              │  │    lifelines + joblib)              │
└──┬───────────────────────┘  └─────────────┬───────────────────────┘
   │                                        │
   │ embeds                                 │ writes
   ▼                                        ▼
┌──────────────────────────┐  ┌─────────────────────────────────────┐
│   FAISS INDEX            │  │   SQLITE DATABASE                   │
│   faiss_hr_index/        │  │   hr_enterprise.db                  │
│   faiss_hr_index_multi…  │  │   ├─ workforce_predictions          │
│                          │  │   ├─ shap_feature_impact            │
│                          │  │   ├─ model_calibration              │
│                          │  │   └─ survival_curves                │
└──────────────────────────┘  └─────────────┬───────────────────────┘
                                            │
                                            │ generated from
                                            ▼
                              ┌─────────────────────────────────────┐
                              │   SYNTHETIC CSV                     │
                              │   attrisense_synthetic_hr.csv       │
                              └─────────────────────────────────────┘
```

## The six layers

### 1. Synthetic data layer

[`generate_demo_workforce_data.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/generate_demo_workforce_data.py) generates ~5,000 employees across three departments (Engineering, Manufacturing, Sales) with deterministic seeds. The Manufacturing department is intentionally given a stronger turnover signal so the [Fairness Audit](../features/fairness-audit.md) has a real disparate-impact failure to detect.

**Output:** `attrisense_synthetic_hr.csv`

**Why synthetic:** the repo is public — no real HR data should ever live here. See [Intended Use](../ethics/intended-use.md).

### 2. ML pipeline

[`train_retention_risk_model.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/train_retention_risk_model.py) is a 486-line script that:

1. Reads the CSV, splits train/test (stratified on `voluntary_turnover`).
2. Applies **SMOTE** to balance the rare-event positive class.
3. Trains a **Random Forest** classifier (`n_estimators=300`, `max_depth=8`).
4. Computes **SHAP TreeExplainer** values for every high-risk employee + a risk-weighted sample of the rest.
5. Fits a **Cox proportional-hazards** model on `(tenure_months, voluntary_turnover)` for survival curves.
6. Computes a **calibration table** (10 bins) and writes the **Brier score**.
7. Writes everything into `hr_enterprise.db` (4 tables) and `attrisense_model.joblib`.

**Output:** `hr_enterprise.db` + `attrisense_model.joblib`. See [ML pipeline](ml-pipeline.md).

### 3. Data store

A single **SQLite** database (`hr_enterprise.db`) with four tables:

| Table | What it holds | Used by |
|---|---|---|
| `workforce_predictions` | Per-employee risk score, band, SHAP_Explained flag, recommended intervention | All dashboard tabs |
| `shap_feature_impact` | Per-employee, per-feature SHAP value | SHAP Insights tab |
| `model_calibration` | 10 reliability bins | Survival/Calibration tab |
| `survival_curves` | Cox cohort survival probabilities | Survival/Calibration tab |

SQLite was chosen for **portability and inspectability**, not performance — `sqlite3 hr_enterprise.db` lets a reviewer inspect every prediction by hand. See [Data schema](../reference/data-schema.md).

### 4. AI / RAG services

| Module | Purpose | Fallback |
|---|---|---|
| [`natural_language_sql.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/natural_language_sql.py) | NL→SQL via LangChain + OpenAI; PRAGMA `query_only=ON` enforced; only `SELECT/WITH` allowed | TF-IDF ranker over 50 gold questions ([`nl_sql_fallback.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/nl_sql_fallback.py)) |
| [`build_exit_interview_vector_index.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/build_exit_interview_vector_index.py) | OpenAI embeddings → FAISS index | Hashing trigrams ([`multilingual_rag.py:HashingEmbeddings`](../reference/api.md#multilingual-rag)) |

Every AI service **probes the API before committing** — see the `_try_openai_embeddings()` pattern. If the corp firewall blocks `api.openai.com`, the dashboard degrades gracefully instead of crashing the whole `main()` call.

### 5. Application layer

The `production/src/attrisense/` package is a flat collection of **single-purpose modules**. Each one is < 250 lines, fully unit-tested, and importable in isolation.

```
attrisense/
├── compare.py              # side-by-side employee comparison
├── onboarding.py           # 6-step interactive tour
├── fairness.py             # EEOC four-fifths rule audit
├── causal_uplift.py        # EconML T-learner intervention picker
├── multilingual_rag.py     # FAISS RAG with hashing fallback
├── nl_sql_eval.py          # 50-question gold harness
├── nl_sql_fallback.py      # TF-IDF cosine ranker
├── slack_alert_mock.py     # Slack/Teams alert UI mock
├── gold_questions.py       # 50 hand-validated NL→SQL pairs
├── theme.py                # dark SaaS palette + Plotly defaults
├── config.py               # paths + constants for the production layer
└── __init__.py             # version 2.0.0 marker
```

See [API reference](../reference/api.md) for module-by-module signatures.

### 6. Presentation layer

Two Streamlit apps:

| | Original | production |
|---|---|---|
| File | `streamlit_app.py` (1,119 lines) | `production/streamlit_app.py` (510 lines) |
| Tabs | 5 | 10 |
| Theme | Streamlit default | Dark SaaS palette |
| Tests | None | 31 pytest |

The production app is **additive** — original is untouched. See [Why two apps?](../design/decisions.md#why-two-apps).

## Cross-cutting concerns

| Concern | Where it lives |
|---|---|
| Configuration | `config.py` (root) re-exported by `production/src/attrisense/config.py` |
| Logging | Python `logging` module, level INFO; multilingual_rag logs warnings on fallback |
| Secrets | `.env` (git-ignored); loaded by `python-dotenv` at app startup |
| Theme + branding | `production/src/attrisense/theme.py` |
| Tests | `production/tests/` — 8 files, 31 tests |
| CI | `.github/workflows/ci.yml` — lint + test on every push |
| Container | `production/Dockerfile` — slim Python 3.11 base |

## What's next

- [Data flow](data-flow.md) — follow a single employee record from CSV to dashboard pixel
- [ML pipeline](ml-pipeline.md) — what happens inside `train_retention_risk_model.py`
- [Tech stack](tech-stack.md) — why every dependency is on the list
