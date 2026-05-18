<!--
AttriSense — docs/reference/make-targets.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Make targets

> Every `make` command, what it does, and what it depends on.

All targets live in [`production/Makefile`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/Makefile). Run from inside `production/` or use `make -C production <target>`.

## Pipeline

| Target | What it does |
|---|---|
| `make pipeline` | Full rebuild: `data → train → uplift → fairness → eval` |
| `make data` | `python ../generate_demo_workforce_data.py` |
| `make train` | `python ../train_retention_risk_model.py` |
| `make uplift` | Rebuild `data/causal_uplift.csv` via `causal_uplift.compute_uplift_table()` |
| `make fairness` | Run audit, write `outputs/fairness_report.json` |
| `make eval` | Run NL→SQL gold harness, write `outputs/nl_sql_eval_report.json` |

## Run

| Target | What it does |
|---|---|
| `make run` | Start the production dashboard on a free port |
| `make run-original` | Start the original `streamlit_app.py` (port 8503 by default) |

## Tests + lint

| Target | What it does |
|---|---|
| `make test` | `pytest tests/ -v` (31 tests) |
| `make test-cov` | Coverage report to terminal + `htmlcov/` |
| `make lint` | `ruff check .` |
| `make format` | `black .` (in-place format) |
| `make typecheck` | `mypy src/attrisense` |
| `make check` | `lint + format-check + typecheck + test` (the CI bundle) |

## Docker

| Target | What it does |
|---|---|
| `make docker-build` | Build `attrisense:latest` image |
| `make docker-run` | `docker run -p 8503:8503 --env-file ../.env attrisense:latest` |
| `make docker-shell` | Interactive shell inside the image |

## Docs

| Target | What it does |
|---|---|
| `make docs-serve` | `mkdocs serve` (live-reload local docs site) |
| `make docs-build` | `mkdocs build` (writes `site/`) |

## Clean

| Target | What it does |
|---|---|
| `make clean` | Remove `.pytest_cache`, `__pycache__`, `htmlcov`, `site/` |
| `make clean-data` | Remove generated CSV / DB / model / FAISS / outputs (NOT `.env`) |
| `make clean-all` | `clean + clean-data` — pristine repo |

`clean-data` is **destructive** in the sense that you'll need to retrain. It does NOT touch `.env`, `.venv`, or git state.

## Common workflows

### Brand new clone

```bash
cd production
pip install -e ".[dev,causal]"
make pipeline
make run
```

### After pulling new changes

```bash
cd production
make test           # confirm nothing broke
make pipeline       # rebuild artifacts (skips already-built ones)
make run
```

### Before opening a PR

```bash
cd production
make check          # lint + format + typecheck + test
```

### Releasing a new version

```bash
# bump version in pyproject.toml + __init__.py
make check
make docker-build
docker tag attrisense:latest ghcr.io/yourname/attrisense:latest
docker push ghcr.io/yourname/attrisense:latest
git tag v2.0.0 && git push --tags
```

## Why a Makefile and not just `pip install -e` + manual commands

- **Discoverability** — `make help` lists everything.
- **Reproducibility** — same target works in CI, in Docker, on a new laptop.
- **Composition** — `make pipeline` chains five steps that you'd otherwise have to remember the order of.

For Windows users without Make, the targets are simple shell commands — copy-paste from the Makefile or use [`make` for Windows](https://gnuwin32.sourceforge.net/packages/make.htm) / WSL.
