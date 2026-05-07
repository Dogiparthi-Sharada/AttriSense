# Roadmap

> What's done, what's next, and what's deliberately not on the list.

Last updated: **May 7, 2026**.

## ✅ Shipped

### Production scaffold
- [x] Package layout under `production/src/attrisense/`
- [x] 31 pytest tests across 8 files
- [x] `pyproject.toml` with dev / causal / docs extras
- [x] `Makefile` with pipeline / run / test / docker / docs targets
- [x] Dockerfile (slim Python 3.11)
- [x] GitHub Actions CI (lint + test on push)
- [x] Pre-commit hook example

### Dashboard tabs
- [x] Executive (KPIs + risk distribution)
- [x] SHAP Insights (per-employee waterfall)
- [x] Compare (side-by-side panel) — with `SHAP_Explained` int→bool fix
- [x] Causal Uplift (EconML T-learner over 3 treatment arms)
- [x] Fairness Audit (EEOC four-fifths rule)
- [x] AI Assistant (NL→SQL with TF-IDF fallback)
- [x] NL→SQL Eval (50 gold questions)
- [x] Multilingual RAG (en/es/hi with hashing fallback)
- [x] Alert Mock (Slack/Teams card)
- [x] Ethics

### Robustness
- [x] OpenAI reachability probe → graceful fallback
- [x] Per-provider FAISS index dirs (no dimension collision)
- [x] `HashingEmbeddings(Embeddings)` correctly inherits
- [x] `.env` auto-load at app start
- [x] PRAGMA `query_only=ON` for read-only enforcement
- [x] SELECT-only SQL allow-list

### Theme + UX
- [x] Dark SaaS palette (cyan/indigo accent on slate canvas)
- [x] Plotly defaults centralised in `theme.py`
- [x] Onboarding tour (6 steps, session-state cursor)
- [x] Disclosure ribbon (synthetic-data warning)

### Docs
- [x] Comprehensive `docs/` tree (this site)
- [x] Architecture / features / design / ops / reference / ethics sections
- [x] Troubleshooting + FAQ + glossary
- [x] Model card + fairness policy + intended-use boundary

---

## 🟡 Next (in priority order)

### Hardening
- [ ] Wire `make docs-build` into CI to catch broken doc links
- [ ] Add Playwright smoke test that loads each tab in CI
- [ ] Add coverage gate (≥ 70%) on PRs
- [ ] Sign Docker image with `cosign`
- [ ] Publish image to GHCR with version tags

### Fairness
- [ ] Audit by manager dimension
- [ ] Audit by tenure-band dimension
- [ ] Add Fairlearn-based reweighting option to `train_retention_risk_model.py`
- [ ] Add an "intersectional" audit (department × tenure band)
- [ ] **Identification-bias controls** — pseudonymized `review_id` mapping table, gated reverse-lookups, audit log of every name resolution. See [fairness-policy](ethics/fairness-policy.md#employee-id-bias).

### Causal
- [ ] Replace simulated treatment with **observable** treatment column when real data is available
- [ ] Add propensity-score matching path (DR-learner / DML)
- [ ] Validate causal assumptions (overlap, no unmeasured confounding)

### NL→SQL
- [ ] Eval harness against `gpt-4` + `claude-sonnet` for comparison
- [ ] Embedding-based ranker as a third tier between TF-IDF and LLM
- [ ] Add 50 more gold questions in non-English languages

### Operations
- [ ] Streamlit Community Cloud deployment + public URL in README badges
- [ ] `secrets.example.toml` template for Streamlit Cloud
- [ ] Postgres adapter (only the connection factory needs to switch)
- [ ] Role-based access control (Executive vs HR Partner vs Manager views)
- [ ] Automatic dashboard screenshot refresh in CI (Playwright)

### Time-series
- [ ] Add `snapshot_date` column to `workforce_predictions`
- [ ] Generate multiple snapshots in `generate_demo_workforce_data.py` with realistic drift
- [ ] Add a fifth KPI tracking month-over-month risk change
- [ ] Add a calibration-drift sparkline

### Real causal
- [ ] Import historical retention-action data when available
- [ ] Switch from T-learner simulation to DR-learner / DML on observed treatment
- [ ] Validate assumptions (overlap, no unmeasured confounding, SUTVA)

### Slack integration
- [ ] Replace mock with `slack_sdk.WebClient`
- [ ] Reaction-based feedback loop (👍 / 👎 / 👀 → labelled training signal)
- [ ] Per-manager opt-in / opt-out

---

## 🔴 Deliberately not on the list

These would be wrong moves for this codebase. Documenting so contributors don't surprise themselves.

| Anti-roadmap item | Why not |
|---|---|
| **Auto-mitigate fairness failures** | Mitigation is a human decision. Auto-fixing creates the illusion of fairness without engaging the conversation. |
| **Add features that benefit a third party at the employee's expense** | Out of scope per [intended use](ethics/intended-use.md). |
| **MLflow / Weights & Biases / experiment tracking** | One trained artifact in git is enough at this scale. |
| **Airflow / Prefect / Dagster** | The pipeline is `make pipeline`. Orchestration tools are overkill. |
| **dbt** | Four tables, no transformations. A Makefile + train script is sufficient. |
| **GraphQL API** | The dashboard *is* the API. |
| **Mobile app** | Streamlit is responsive enough. Native mobile is a different project. |
| **Server-Sent Events / live updates** | The data is a snapshot. SSE adds complexity without value. |
| **A second model framework (PyTorch / TF)** | RandomForest + SHAP is the right complexity for the audit story. |
| **A "self-serve" feature for users to upload their own CSV** | Without column-level provenance, this becomes a privacy hazard. |

If a contributor PRs any of these, the maintainer will close the PR with a link to this section.

---

*Roadmap is reviewed every two weeks. PRs that align with "Next" priorities get triaged first.*
