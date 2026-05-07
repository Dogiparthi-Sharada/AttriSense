<!--
AttriSense — docs/design/trade-offs.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Trade-offs

> Every engineering choice is a trade. Here are the ones AttriSense made and what we gave up to get them.

## Synthetic data vs. real HRIS data

| What we get | What we give up |
|---|---|
| Public repo, zero PII risk | Distributions don't match a real workforce |
| Reproducibility (`RANDOM_SEED=42`) | Fairness audit results are demoware |
| Safe to demo on any laptop | "How would this score on your data?" requires a separate ingestion |

**Net:** right call for a portfolio. Wrong call for a real deployment without an explicit data-source swap.

## Random Forest vs. XGBoost / LightGBM / TabNet

| What we get | What we give up |
|---|---|
| Exact SHAP via TreeExplainer | ~1pp AUC |
| Trains in 12s on any laptop | Some marginal calibration improvement |
| Zero hyperparameter tuning rabbit hole | Best-in-class accuracy |

**Net:** for a 5k-row demo, RF is correct. For a 5M-row production system, XGBoost on GPU.

## Single-file vs. package layout

| | Single-file (`streamlit_app.py`) | Package (`production/src/attrisense/`) |
|---|---|---|
| Onboarding | Read top to bottom | Need to know the import graph |
| Tests | Hard to isolate | Module-by-module unit tests trivial |
| Reuse outside Streamlit | Hard | Easy (`from attrisense.fairness import run_audit`) |
| Lines per file | 1,119 | < 250 each |

We ship **both**. Original = single-file (preserved). production = package (production-shaped).

## SQLite vs. Postgres

| | SQLite | Postgres |
|---|---|---|
| Setup | Zero | Service + role + db |
| File size today | 4 MB | n/a |
| Concurrent writers | 1 | n |
| Inspectable | `sqlite3 db` | `psql` (more setup) |
| Write protection | `PRAGMA query_only=ON` | grants on roles |

**Net:** SQLite is the right answer until you have a second writer.

## FAISS local vs. vector DB SaaS

| | FAISS | Pinecone / Weaviate |
|---|---|---|
| 12 docs | Trivial | Overkill |
| 100k docs | Acceptable | Better |
| 10M docs | Bad | Good |
| Auth / RBAC | None (in-process) | Built-in |
| Cost | $0 | $$ per month |

**Net:** FAISS until ~100k docs OR until you need access control.

## OpenAI vs. local LLM (Llama / Mistral)

| | OpenAI | Local |
|---|---|---|
| Quality | Higher | Acceptable |
| Latency | Network round-trip | RAM-bound |
| Cost | $/query | Hardware capex |
| Privacy | Sends data to OpenAI | Local |
| Firewall-friendly | ❌ in many corp networks | ✅ |

**Net:** AttriSense uses OpenAI but **always** has a deterministic fallback (TF-IDF for NL→SQL, hashing for embeddings). The right call for a portfolio. For a real HR deployment with sensitive labels, run a local Llama-3 or Mistral via vLLM.

## Streamlit vs. FastAPI + React

| | Streamlit | FastAPI + React |
|---|---|---|
| Python-only stack | ✅ | ❌ — also need JS/TS |
| First paint | < 2s | depends |
| Custom components | Heavy | Free |
| Real-time updates | Polling | WebSockets |
| Mobile responsive | Adequate | Excellent if built right |
| Time to ship | Hours | Weeks |

**Net:** Streamlit until the UX needs custom components or real-time. Then move the dashboard to React but keep `attrisense.*` modules as the backend.

## Theme: dark vs. light

| | Dark | Light |
|---|---|---|
| Screenshot quality | Better | Worse |
| Color contrast (risk bands) | High on dark canvas | Washed out on white |
| User preference | ~99% accept | ~99% accept |
| Eye strain in dark rooms | Low | High |

**Net:** dark is the better default for a screenshot-heavy demo. A real deployment should offer a toggle (one CSS file swap).

## Tests: 31 vs. nothing vs. 200

The original demo has zero tests. the production package has 31. Could it have 200?

| | Today (31) | Hypothetical (200) |
|---|---|---|
| Coverage | ~70% | ~95% |
| Cost to write | shipped | weeks |
| Cost to maintain | low | medium |
| Catches regressions | yes | yes |

**Net:** 31 is the right cost/benefit for now. The bar to move higher: a second engineer joins the project.

## Ship-it index

For each trade above, ask: **"would I make the same call for a $1M deployment?"**

| Trade | Hold for production? |
|---|---|
| Synthetic data | ❌ — must swap to HRIS |
| RF over XGB | ⚠️ — depends on AUC delta |
| Single-file original | ❌ — keep package layout only |
| SQLite | ❌ — Postgres |
| FAISS | ✅ — until > 100k docs |
| OpenAI as primary | ⚠️ — depends on data sensitivity |
| Streamlit | ✅ — for internal tools |
| Dark theme | ⚠️ — add a toggle |
| 31 tests | ❌ — go higher with team |

The point: **today's choices are right for today's constraints**. The roadmap encodes the upgrade path.
