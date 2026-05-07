<!--
AttriSense — CHANGELOG.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Changelog

All notable changes to AttriSense are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive `docs/` MkDocs Material site (architecture, features, design, ops, reference, ethics, learn, ASCII).
- Pastel-themed generated diagrams (`scripts/generate_doc_diagrams.py`).
- Beginner-tutorial section under `docs/learn/` covering SHAP, SMOTE, Cox PH, T-Learner, RAG, fairness, NL→SQL.
- ASCII-text mirror of every diagram under `docs/ascii/`.
- Identification-bias section in fairness policy with proposed `review_id` mapping pattern.
- Windows / PowerShell coverage in quickstart, installation, docker, and troubleshooting docs.
- Session logs under `session_logs/`.

### Changed
- Replaced original README with world-class README (badges, feature grid, diagram, ethics statement).
- Original README archived to `archive/original_readme.md` (preserved verbatim).
- Original earlier generated diagrams archived to `archive/old_diagrams/`.

## [2.0.0] — Production scaffold

### Added
- `production/` package with `compare`, `onboarding`, `fairness`, `causal_uplift`, `multilingual_rag`, `nl_sql_eval`, `nl_sql_fallback`, `slack_alert_mock`, `theme`.
- 31 pytest tests across 8 files.
- `pyproject.toml` with `dev`, `causal`, `docs` extras.
- `Makefile` with `pipeline`, `run`, `test`, `docker`, `docs` targets.
- Dockerfile (`python:3.11-slim`, non-root user).
- GitHub Actions CI (lint + test on push).
- production dashboard `production/streamlit_app.py` with dark SaaS palette.

### Fixed
- `KeyError: True` on Compare tab — `SHAP_Explained` int→bool coercion.
- Theme palette regression (white background bleeding through).
- `from __future__` duplication SyntaxError.
- `.env` not loading when run from `production/`.
- Multilingual RAG cascade failure on `openai.APIConnectionError` — added reachability probe + per-provider FAISS dirs + mid-query fallback + `HashingEmbeddings(Embeddings)` inheritance.

## [1.0.0] — Initial release

### Added
- Streamlit demo dashboard (`streamlit_app.py`) with 9 tabs.
- RandomForest + SMOTE retention model.
- SHAP TreeExplainer integration.
- Cox PH survival analysis.
- LangChain NL→SQL Q&A.
- FAISS exit-interview vector index.
- Synthetic 5,000-row HR dataset generator.
