<!--
AttriSense — docs/architecture/data-flow.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Data flow

Follow a single employee record from CSV creation to dashboard pixel.

![End-to-end data flow](../images/diagrams/data-flow.png)


## The journey of employee `EMP_2417`

### Step 1 — Generated

[`generate_demo_workforce_data.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/generate_demo_workforce_data.py) uses NumPy with `RANDOM_SEED=42` to produce one row per employee:

```csv
employee_id,department,tenure_months,base_salary,manager_id,manager_tenure_months,voluntary_turnover,exit_notes
EMP_2417,Manufacturing,7,52000,MGR_38,4,1,"My manager kept changing priorities every week."
```

Department-specific distributions are seeded so:

- **Manufacturing** has shorter median tenure and lower base salary → higher synthetic turnover.
- **Engineering** has the longest tenure + highest salary → lowest turnover.
- **Sales** sits in the middle.

This skew is deliberate — it gives the [Fairness Audit](../features/fairness-audit.md) a real disparate-impact failure to detect.

### Step 2 — Trained

[`train_retention_risk_model.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/train_retention_risk_model.py) reads the CSV, encodes departments via `DEPARTMENT_CODE_MAP` ([`config.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/config.py#L33)), applies SMOTE, fits a Random Forest, and produces:

- **Risk probability** for `EMP_2417` → `0.83` → bucketed into `High Risk` (threshold 0.75).
- **SHAP values** for `EMP_2417` (because high risk):
  - `tenure_months = 7` → +0.21 (short tenure pushes risk up)
  - `base_salary = 52000` → +0.12 (low for the dept)
  - `department = Manufacturing` → +0.08
  - `manager_tenure_months = 4` → +0.05
- **Recommended intervention** — joined in from `causal_uplift.py`: `manager_change` (highest predicted uplift).

### Step 3 — Stored

A single SQLite write fans out to four tables:

```sql
INSERT INTO workforce_predictions VALUES (
  'EMP_2417', 'Manufacturing', 7, 52000, 'MGR_38', 4,
  0.83, 'High Risk', 1, 'manager_change'
);

INSERT INTO shap_feature_impact VALUES
  ('EMP_2417', 'tenure_months', 0.21),
  ('EMP_2417', 'base_salary', 0.12),
  ('EMP_2417', 'department_code', 0.08),
  ('EMP_2417', 'manager_tenure_months', 0.05);

-- model_calibration and survival_curves are aggregate tables, not per-employee.
```

`SHAP_Explained = 1` is set for every high-risk employee plus a risk-weighted sample of medium/low — so reviewers always have a SHAP waterfall to look at.

### Step 4 — Loaded

The Streamlit app opens the SQLite file in **read-only mode** (`PRAGMA query_only=ON`) and pulls the predictions table into a pandas DataFrame on app start. The DataFrame is cached via `@st.cache_data` so subsequent tab switches are instant.

```python
def load_predictions() -> pd.DataFrame:
    with sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True) as conn:
        return pd.read_sql_query(
            f"SELECT * FROM {SQL_TABLE_NAME}", conn
        )
```

### Step 5 — Rendered

Each dashboard tab queries the same DataFrame:

| Tab | What it does with `EMP_2417` |
|---|---|
| Executive | Counts him in the High-Risk KPI; he appears as a red dot in the risk-distribution histogram |
| SHAP Insights | His row appears in the high-risk table; clicking it shows the waterfall above |
| Compare | If selected, his side-by-side card shows tenure 7mo, salary $52k, drivers list |
| Causal Uplift | His row shows `manager_change` as the recommended intervention |
| Fairness | Manufacturing's high-risk concentration drives the 0.20 disparate-impact ratio |
| AI Assistant | "Show me high-risk Manufacturing employees" → SQL → his row in the result |
| Alert Mock | If alerts are toggled on for his manager, he appears in the digest |

## End-to-end timing (synthetic dataset, ~5k rows)

| Stage | Time | Hardware |
|---|---|---|
| Generate CSV | ~0.5s | any laptop |
| Train + SHAP + survival | ~12s | M1 Air |
| Build FAISS index (OpenAI) | ~3s + network | depends |
| Build FAISS index (hashing fallback) | ~0.2s | any |
| Cold dashboard start | ~2s | any |
| Tab switch (cached) | < 100ms | any |

## When the data flow breaks

| Failure | Symptom | Fix |
|---|---|---|
| CSV missing | Train script raises `FileNotFoundError` | `python generate_demo_workforce_data.py` |
| DB missing | Dashboard shows `OperationalError: no such table` | `python train_retention_risk_model.py` |
| FAISS index missing | RAG tab silently rebuilds | Wait ~3s on first query |
| OpenAI unreachable | `multilingual_rag` falls back to hashing | No action — see [troubleshooting](../troubleshooting.md#openai-connection-error) |
| SHAP column missing | Compare tab shows empty drivers list | Retrain with current `train_retention_risk_model.py` |
