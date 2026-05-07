# Design decisions

> Why AttriSense looks the way it does. Each decision is captured with the alternative considered and the reason we picked one over the other.

## Product principles

| Principle | What it means in practice |
|---|---|
| **Understandable first, impressive second** | A reviewer can read the whole codebase in an afternoon. No clever tricks where boring works. |
| **Audit-friendly by default** | Every score has a SHAP explanation. Every group has a fairness check. Every NL→SQL query is logged. |
| **Synthetic data, public repo** | Zero risk of PII leak, complete reproducibility, repo can be forked for teaching. |
| **AI is optional, not load-bearing** | Tabs that need an LLM degrade gracefully. The dashboard runs offline. |
| **One source of truth per concept** | Paths in `config.py`, palette in `theme.py`, gold questions in `gold_questions.py`. |

## Why two apps {#why-two-apps}

The repo ships **both** the original `streamlit_app.py` (1,119 lines) **and** the production dashboard `production/streamlit_app.py` (510 lines).

**Why not just delete the original?**

1. The original is the **historic interview deliverable** — preserving it shows version-1 thinking.
2. It demonstrates **change discipline** — the production layer is additive, never destructive. Anyone can `diff` the two and see what was added vs. what was already there.
3. Some code paths (like the What-If Simulator) only exist in the original. Folding them into production would have been a port, not a feature.

**Why not just extend the original?**

1. The original is a **single-file app** with five tabs. Adding five more tabs would push it past 2,000 lines. Past that point, single-file becomes a liability.
2. the production package introduces a **package layout** (`production/src/attrisense/`) that the original never had. Mixing them would have made the package layout worse, not better.
3. production has **31 unit tests**. Retrofitting tests onto the original would have been a separate (multi-day) project.

The production layer is the answer to "what does this look like as a product, not a demo".

## Why SQLite, not Postgres

| Need | SQLite | Postgres |
|---|---|---|
| Portable across machines | ✅ — single file in git | ❌ — service to start |
| Inspectable by reviewer | ✅ — `sqlite3 file.db` | ⚠️ — needs running server |
| Read-only enforcement | ✅ — `PRAGMA query_only=ON` | ⚠️ — role-based |
| Concurrent writers | ❌ | ✅ |
| Multi-tenant | ❌ | ✅ |
| Millions of rows | ⚠️ | ✅ |

For a portfolio demo with one user and 5,000 rows, SQLite wins. For a real deployment, swap the connection factory in `config.py:DATABASE_PATH`.

## Why Random Forest, not XGBoost

- TreeExplainer SHAP is **exact** for RF and XGB; both work.
- RF requires no GPU, no extra installs, and trains in ~12 seconds.
- The AUC delta on this synthetic dataset is < 1pp.
- Ship the simpler thing.

If a real deployment needed every percentage point of AUC, the swap is a one-liner — `RandomForestClassifier()` → `XGBClassifier()`.

## Why SMOTE, not class weights

- `class_weight='balanced'` rescales the loss; SMOTE rebalances the data.
- On rare-event problems (~12% positive class), SMOTE gives stronger signal at training time.
- `class_weight` would be the right call if SMOTE memory cost mattered. At 5k rows, it doesn't.

## Why FAISS, not Pinecone / Weaviate

- 12 documents.
- Adding a SaaS vector DB would add a network hop, an auth boundary, and a billing line item to a portfolio demo.
- FAISS persists to two files (`.faiss` + `.pkl`) and reloads in milliseconds.

When the index grows past ~100k documents or needs metadata filtering at scale, swap to Postgres + pgvector or a managed service.

## Why a TF-IDF fallback for NL→SQL

| Failure mode | LLM behaviour | Fallback behaviour |
|---|---|---|
| No API key | Crashes | Returns 3 ranked gold questions |
| Network blocked | Crashes (we saw this happen) | Same as above |
| Rate limited | Hangs / 429 | Same as above |
| Hallucinates a column | Generates wrong SQL | TF-IDF can't hallucinate; it ranks fixed text |

The fallback is **not** a worse LLM. It's a **different product** — a guided-question UX. Both are useful; only the LLM gets to be wrong.

## Why a dark theme

Two reasons:

1. **Screenshot quality** — dark dashboards photograph well in slide decks and landing pages.
2. **Contrast hierarchy** — risk colors (cyan / amber / coral / teal) pop on a dark canvas. On a light canvas the same palette looks washed out.

The tradeoff: ~1% of users prefer light themes. For an HR-analytics portfolio demo, optimising for screenshot quality wins.

## Why no auth / RBAC

Out of scope for a portfolio demo. The roadmap notes the right way to add it (Streamlit Auth + role tags) — see [roadmap.md](../roadmap.md).

## Why no time-series

The synthetic dataset is a single snapshot. Adding `snapshot_date` and a month-over-month risk delta would require generating multiple snapshots with realistic drift — that's a project of its own. On the roadmap.

## What we got wrong (and fixed)

| Mistake | Symptom | Fix |
|---|---|---|
| `df[df["SHAP_Explained"]]` | KeyError on every tab — SQLite stores booleans as ints | `.astype(bool)` |
| `HashingEmbeddings` not inheriting from `Embeddings` | `'HashingEmbeddings' object is not callable` from FAISS | Inherit from `langchain_core.embeddings.Embeddings` |
| Single FAISS index dir | OpenAI-shaped 1536-dim index loaded with 256-dim hashing model → crash | Per-provider dirs (`openai/`, `hashing/`) |
| OpenAI exception bubbling up | Multilingual tab crash → killed Alert and Ethics tabs too | Probe-and-fallback pattern in `multilingual_rag.search()` |
| White CSS palette | "shitty white background" feedback | Rewrote `theme.py` with deep-slate canvas, cyan-indigo accent |
| `.env` not loaded | `OPENAI_API_KEY is not set` despite `.env` existing | Explicit `load_dotenv(dotenv_path=_REPO_ROOT / ".env")` at app start |

These are documented in [troubleshooting](../troubleshooting.md) so the next person doesn't trip over them.
