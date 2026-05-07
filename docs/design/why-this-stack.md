<!--
AttriSense — docs/design/why-this-stack.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Why this stack

> A 60-second pitch for each major dependency.

## Streamlit

**Picked because:** Python-native, no JS build step, hot-reload on file save, ships with `st.cache_data` so DataFrame-heavy apps stay fast.

**Tradeoff:** Streamlit is opinionated. Multi-page navigation is awkward, custom components are heavy, real-time updates are clunky. For an analytics dashboard read-only against SQLite, none of that matters.

**When to outgrow:** If you need WebSockets, real-time collab, embeddable charts in someone else's site, or multi-page nav with deep links.

## scikit-learn

**Picked because:** Industry-standard, audit-friendly, perfect SHAP integration via `TreeExplainer`. No surprises.

**Tradeoff:** Slower than XGBoost / LightGBM at the margins.

**When to outgrow:** When the AUC delta starts paying for itself in retention dollars.

## SHAP

**Picked because:** TreeExplainer is **exact** for tree ensembles. The waterfall plot is recognisable to anyone who has read a SHAP paper. Per-row attributions persist trivially in SQLite.

**Tradeoff:** SHAP plots use matplotlib, which doesn't blend into Plotly dashboards perfectly. We accept this — SHAP plots' conventions matter more than visual uniformity.

**When to outgrow:** Never, for tree models. For deep learning, switch to integrated gradients or LIME.

## EconML

**Picked because:** Microsoft Research's library, T-learner is the textbook starting point for treatment-effect estimation, integrates with sklearn estimators.

**Tradeoff:** Heavy install (`numba`, `dowhy`, `lightgbm`). Optional extra in `pyproject.toml`.

**When to outgrow:** When you need DR-learner / DML / instrumental variables. EconML supports those too — same API.

## LangChain (1.0+)

**Picked because:** Standard interface across LLM providers. Tool-using agent pattern. Big enough community that any error is googleable.

**Tradeoff:** The 1.0 split into `langchain` / `langchain-openai` / `langchain-community` / `langchain-text-splitters` adds install ceremony. Frequent breaking changes.

**When to outgrow:** When the abstraction taxes get larger than the convenience benefits — typically when your prompt logic is bespoke enough that LangChain templates fight you.

## FAISS

**Picked because:** Local, fast, deterministic, persists to two files. No network dependency. Free.

**Tradeoff:** No metadata filtering at scale, no async API, no replication.

**When to outgrow:** > 100k documents, multi-tenant access control, or a need for hybrid search.

## SQLite

**Picked because:** Portable, inspectable, supports `PRAGMA query_only=ON` for read-only enforcement. The whole DB fits in git.

**Tradeoff:** Single-writer. Limited concurrency. No replication.

**When to outgrow:** Concurrent writers, multi-tenant, > 1M rows, or a need for a real BI tool downstream.

## Plotly

**Picked because:** Interactive (zoom, hover, legend toggles) without JS. Good dark-theme support. Renders identically locally and in the browser.

**Tradeoff:** Heavier than matplotlib. Slower first paint than Altair.

**When to outgrow:** When you need pixel-perfect publication graphics — switch to matplotlib + seaborn for those, keep Plotly for the dashboard.

## python-dotenv

**Picked because:** One-liner. No surprises. Standard for the Python ecosystem.

**Tradeoff:** None worth mentioning.

**When to outgrow:** Never. If you outgrow `.env`, you graduate to a real secrets manager (Vault, AWS Secrets Manager) — but `python-dotenv` still works alongside them via env vars.

## pytest + ruff + black + mypy

**Picked because:** Standard. Combined they cover lint, format, type-check, and test in four CLI tools.

**Tradeoff:** None.

**When to outgrow:** Never.

## Docker

**Picked because:** Reproducible runtime. CI artifact. Easy hand-off to ops.

**Tradeoff:** ~720 MB image. Docker build time ~3 minutes from clean.

**When to outgrow:** When you need a Kubernetes-native build path with multi-arch manifests — `Dockerfile` still works, you just add a build matrix.
