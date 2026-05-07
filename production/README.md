# AttriSense production — Production Layer

This directory adds production-grade capabilities on top of the original
AttriSense scripts **without modifying them**. Run `streamlit run streamlit_app.py`
from the repo root for the original dashboard, or `make -C production run`
for the production dashboard.

## What's new in v2

| Capability | File |
|---|---|
| Compare-Two-Employees side-by-side SHAP | `src/attrisense/compare.py` |
| Onboarding tour | `src/attrisense/onboarding.py` |
| Fairness audit (EEOC four-fifths rule, calibration drift) | `src/attrisense/fairness.py` |
| NL→SQL eval harness (50 gold questions, exact + cardinality match) | `src/attrisense/nl_sql_eval.py` |
| Causal Uplift (EconML T-learner) | `src/attrisense/causal_uplift.py` |
| Multilingual RAG (English / Spanish / Hindi, with offline fallback) | `src/attrisense/multilingual_rag.py` |
| Slack/Teams alert mock | `src/attrisense/slack_alert_mock.py` |
| New production dashboard | `streamlit_app.py` |
| Pytest suite | `tests/` |
| GitHub Actions CI | `../.github/workflows/ci.yml` |
| Production Docker image | `Dockerfile` |
| `make` targets | `Makefile` |

## Quick start

```bash
# From the repo root, with the .venv created:
make -C production install      # editable install with [causal,dev] extras
make -C production data         # generate synthetic workforce CSV
make -C production train        # train model, write SQLite
make -C production fairness     # write outputs/fairness_report.json
make -C production uplift       # write causal_uplift_recommendations table
make -C production eval         # run NL→SQL harness (skips if no OPENAI_API_KEY)
make -C production test         # pytest
make -C production run PORT=8520
```

## Running tests + lint locally

```bash
make -C production lint
make -C production test
```

## CI

`.github/workflows/ci.yml` runs lint + tests + fairness + causal uplift on every push to `main` and `production-v2`, plus a Docker build. The NL→SQL harness skips gracefully when `OPENAI_API_KEY` is not configured.

## What is intentionally NOT here

The contents of `week1/ … week4/` and `TODAY/` are launch / career playbooks, not engineering tickets. The non-code items still pending live in `../ROADMAP.txt`.
