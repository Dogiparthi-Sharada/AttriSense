<!--
AttriSense — docs/architecture/tech-stack.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Tech stack

> Every dependency in [`requirements.txt`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/requirements.txt) and [`production/pyproject.toml`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/pyproject.toml) earns its place. Here's why.

## Runtime {#scikit-learn}

| Dependency | Used for | Why this one |
|---|---|---|
| **streamlit** | Dashboard | Python-native, no JS build step, excellent for analytics. The wrong choice if you needed a public marketing site; the right choice for an internal HR analytics tool. |
| **pandas** | Data wrangling | Universal lingua franca; every analyst can read pandas. |
| **numpy** | Vector math | Transitive (everything else needs it) and direct (synthetic-data generator, hashing embeddings). |
| **scikit-learn** | Model | RandomForest + train_test_split + metrics. Canonical, audit-friendly. |
| **imbalanced-learn** | SMOTE | Standard implementation; one import, one fit_resample. |
| **shap** | Explanations | `TreeExplainer` is exact for tree ensembles — not approximation, not perturbation. |
| **lifelines** | Survival | `CoxPHFitter` is the survival-analysis equivalent of `RandomForestClassifier` — battle-tested, simple API. |
| **joblib** | Model persistence | scikit-learn's recommended serialiser; portable across Python minor versions. |
| **plotly** | Charts | Interactive (zoom, hover, legend toggles) without writing JS. The dark-theme integration is solid (see [`theme.py:plotly_layout()`](../reference/api.md#theme)). |
| **shap.plots** + **matplotlib** | SHAP waterfalls | SHAP's built-in plots are matplotlib-based; we keep them as-is rather than reimplementing. |

## AI / RAG

| Dependency | Used for | Why this one |
|---|---|---|
| **langchain** + **langchain-openai** + **langchain-community** + **langchain-text-splitters** | NL→SQL chain, embeddings | LangChain 1.0+ split the package; we install the four sub-packages explicitly to avoid the deprecation warnings. |
| **openai** | LLM client | Indirect via langchain-openai but pinned in requirements.txt for clarity. |
| **faiss-cpu** | Vector store | Local, fast, dependency-free vs. running Pinecone/Weaviate for a 12-document index. |
| **scikit-learn (TfidfVectorizer)** | NL→SQL fallback | Already installed for the model; the gold-question ranker is one extra import, not a new dependency. |

The RAG layer **always uses local FAISS** even when OpenAI is reachable — the embeddings can be remote, the index itself is local. This makes the dashboard fast and works offline once the index is built.

## Causal

| Dependency | Used for | Why this one |
|---|---|---|
| **econml** | T-learner for uplift | Microsoft Research's library; the T-learner pattern (one model per treatment arm) is the textbook approach for treatment-effect estimation when you have observational data. |

EconML pulls in `dowhy`, `numba`, `lightgbm` transitively — heavier than the rest of the stack, hence kept as an optional extra (`pip install -e ".[causal]"`).

## Production / dev

| Dependency | Used for | Why this one |
|---|---|---|
| **python-dotenv** | `.env` loading | One liner; no surprises. |
| **pytest** | Tests | Standard. 31 tests, all isolated via `conftest.py` fixtures. |
| **ruff** | Lint | Fast, opinionated, replaces flake8 + isort + parts of pylint. |
| **black** | Format | Settled debate. |
| **mypy** | Type-check | Catches stale signatures during refactors. |
| **pre-commit** | Git hooks (optional) | Stops bad code at commit time. |

## Data store

**SQLite** — chosen over Postgres because:

- **Portable** — single file, fits in the git tree, no service to start.
- **Inspectable** — `sqlite3 hr_enterprise.db` opens an interactive shell.
- **Read-only enforcement** — `PRAGMA query_only=ON` is a one-line guarantee against accidental writes from the AI Assistant.
- **Migration path** — `DATABASE_PATH` is a single constant in `config.py`. Swapping for Postgres is a connection-factory change, not a code rewrite.

For a real deployment with concurrent writers, multi-tenancy, or millions of rows, swap to Postgres or DuckDB.

## Frontend

There is no separate frontend. Streamlit + Plotly is the entire UI.

The dark theme lives in [`production/src/attrisense/theme.py`](../reference/api.md#theme) — a single CSS string injected via `st.markdown(theme.CSS, unsafe_allow_html=True)`. The Plotly figures are styled by `apply_plotly_defaults(fig)` so charts inherit the same palette without per-chart configuration.

## Container / deploy

| | |
|---|---|
| **Base image** | `python:3.11-slim` |
| **Build** | `pip install -e ".[dev,causal]"` |
| **Entrypoint** | `streamlit run streamlit_app.py --server.port 8503 --server.headless true` |
| **Size** | ~720 MB — dominated by sklearn + econml + numba |
| **CI** | GitHub Actions: lint + test on push |

For Streamlit Community Cloud, the `Dockerfile` is bypassed; only `requirements.txt` is consumed.

## What we deliberately did NOT use

| Library | Why not |
|---|---|
| XGBoost / LightGBM | RF + SHAP is more auditable; the AUC delta doesn't matter for a portfolio. |
| Pinecone / Weaviate | A 12-document multilingual index doesn't need a vector DB service. |
| FastAPI | The dashboard *is* the API. Adding an HTTP layer would be cargo-culting. |
| Pydantic models for data validation | The dataset is generated by us with a fixed schema. Pydantic would be ceremony. |
| Pytorch / TensorFlow | No deep models — by design. |
| MLflow | A single trained artifact (`.joblib`) tracked in git is sufficient at this scale. |
| dbt | Four tables, no transformations — a Makefile + `train_retention_risk_model.py` is enough. |
| Airflow / Prefect | The pipeline is `make pipeline`. No need for orchestration. |

When AttriSense outgrows any of these, swap in. Until then, **simpler wins**.
