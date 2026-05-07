<!--
AttriSense — docs/reference/api.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# API reference

> Module-by-module signatures of the `attrisense` package. Everything is importable in isolation — `from attrisense.fairness import run_audit` works without Streamlit.

All modules live under [`production/src/attrisense/`](https://github.com/Dogiparthi-Sharada/AttriSense/tree/main/production/src/attrisense).

## `compare`

Side-by-side employee comparison.

```python
from attrisense.compare import render_comparison_panel, headline_drivers

render_comparison_panel(df, employee_id_a, employee_id_b)
headline_drivers(df, employee_id, top_n=3) -> list[tuple[str, float]]
```

## `onboarding`

Six-step interactive product tour. Uses `st.session_state` for cursor.

```python
from attrisense.onboarding import render_onboarding_tour, reset_onboarding_tour

render_onboarding_tour()    # call once per dashboard render
reset_onboarding_tour()     # called from the sidebar button
```

## `fairness`

EEOC four-fifths rule audit.

```python
from attrisense.fairness import run_audit, audit_dimension, GroupMetrics, FairnessReport

report: FairnessReport = run_audit(df, dimension="department")
report.passes_four_fifths_rule  # bool
report.di_ratio                 # float
report.groups                   # list[GroupMetrics]
report.disadvantaged_group      # str
```

`GroupMetrics` carries `name`, `selection_rate`, `positive_rate`, `calibration_error`, `count`.

## `causal_uplift`

EconML T-learner intervention picker.

```python
from attrisense.causal_uplift import compute_uplift_table, INTERVENTIONS

INTERVENTIONS  # ("salary_lift_10pct", "manager_change", "tenure_bonus_12mo")

uplift_df = compute_uplift_table(df)
# Columns: employee_id, predicted_no_treatment, predicted_<each_treatment>, recommended_intervention
```

Persisted to `data/causal_uplift.csv` for reuse.

## `multilingual_rag` {#multilingual-rag}

FAISS RAG with OpenAI / hashing fallback.

```python
from attrisense.multilingual_rag import search, build_index, HashingEmbeddings

results: list[dict] = search("compensation issues", top_k=6)
# Each dict: {text, language, theme, score, provider}

build_index(provider=None)       # auto-detect
build_index(provider="hashing")  # force fallback
build_index(provider="openai")   # force openai (raises if unreachable)
```

`HashingEmbeddings(dimensions=256)` inherits from `langchain_core.embeddings.Embeddings`.

## `nl_sql_eval`

50-question gold harness.

```python
from attrisense.nl_sql_eval import run_evaluation, EvaluationCase, EvaluationReport
from attrisense.gold_questions import GOLD_QUESTIONS

report: EvaluationReport = run_evaluation(GOLD_QUESTIONS)
report.pass_rate                # float
report.cases                    # list[EvaluationCase]
report.by_category              # dict[str, float]
```

`EvaluationCase` carries `id`, `category`, `question`, `exact_match`, `cardinality_match`, `expected_rowcount`, `generated_rowcount`, `duration_seconds`, `error`.

## `nl_sql_fallback`

Deterministic TF-IDF ranker.

```python
from attrisense.nl_sql_fallback import suggest, execute_gold_sql, Suggestion

suggestions: list[Suggestion] = suggest("how many people are at risk?", top_k=3)
# Each: {gold_id, question, expected_sql, score}

rows = execute_gold_sql(gold_id)  # runs hand-validated SQL
```

## `gold_questions`

50 hand-validated NL→SQL pairs.

```python
from attrisense.gold_questions import GoldQuestion, GOLD_QUESTIONS

GOLD_QUESTIONS  # tuple[GoldQuestion, ...] of length 50
```

`GoldQuestion` is a frozen dataclass: `id`, `category`, `question`, `expected_sql`, `expected_rowcount`, `expected_signature`.

## `slack_alert_mock`

```python
from attrisense.slack_alert_mock import render_alert_mock

render_alert_mock(df)  # renders the styled card via st.markdown
```

## `theme` {#theme}

Centralised palette + Plotly defaults.

```python
from attrisense.theme import (
    CSS, RISK_COLOR_MAP, SEQUENTIAL, CATEGORICAL,
    plotly_layout, apply_plotly_defaults,
    render_brand_header, render_disclosure,
    CANVAS, SURFACE, CYAN, INDIGO, TEAL, AMBER, CORAL,
)

st.markdown(CSS, unsafe_allow_html=True)
fig = apply_plotly_defaults(fig)
st.markdown(render_brand_header("AttriSense", "tagline"), unsafe_allow_html=True)
```

## `config`

Re-exports root `config.py` and adds:

```python
from attrisense.config import (
    DATABASE_PATH, FAISS_INDEX_DIR, OUTPUTS_DIR,
    SQL_TABLE_NAME, SHAP_FEATURE_TABLE_NAME,
    RISK_THRESHOLDS, RANDOM_SEED, DEPARTMENT_CODE_MAP,
    # additions in the production package:
    CAUSAL_UPLIFT_TABLE, MULTILINGUAL_INDEX_DIR,
    EVAL_GOLD_PATH, FAIRNESS_REPORT_PATH, EVAL_REPORT_PATH,
    SHAP_COLUMNS, SHAP_DRIVER_LABELS,
)
```

## Importing from outside Streamlit

The whole package is dashboard-agnostic. You can wire it into:

- A Jupyter notebook for offline analysis.
- A FastAPI endpoint that returns `run_audit(df)`.
- A scheduled batch job that retrains and writes a fresh fairness report.

The Streamlit dashboard is one consumer. The modules are not coupled to it.
