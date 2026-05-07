# Data schema

> Four SQLite tables. ~5,000 rows in `workforce_predictions`. Inspectable via `sqlite3 hr_enterprise.db`.

## `workforce_predictions`

The primary table. One row per employee.

| Column | Type | Example | Source |
|---|---|---|---|
| `employee_id` | TEXT | `EMP_2417` | CSV |
| `department` | TEXT | `Manufacturing` | CSV |
| `tenure_months` | INTEGER | `7` | CSV |
| `base_salary` | INTEGER | `52000` | CSV |
| `manager_id` | TEXT | `MGR_38` | CSV |
| `manager_tenure_months` | INTEGER | `4` | CSV |
| `voluntary_turnover` | INTEGER | `0` or `1` | CSV (label) |
| `predicted_risk` | REAL | `0.83` | Model |
| `risk_band` | TEXT | `High Risk` | Threshold (`config.py:RISK_THRESHOLDS`) |
| `SHAP_Explained` | INTEGER | `0` or `1` | Model |
| `recommended_intervention` | TEXT | `manager_change` | EconML (`causal_uplift.py`) |

`SHAP_Explained = 1` for every high-risk employee + a risk-weighted random sample of medium/low. See [SHAP Insights](../features/shap-insights.md#shap_explained--1-not-1-for-everyone).

## `shap_feature_impact`

Long-format SHAP values. One row per (employee, feature).

| Column | Type | Example |
|---|---|---|
| `employee_id` | TEXT | `EMP_2417` |
| `feature` | TEXT | `tenure_months` |
| `shap_value` | REAL | `0.21` |

Index on `(employee_id, feature)` for fast lookup.

Only employees with `SHAP_Explained = 1` appear here — see [SHAP storage strategy](../features/shap-insights.md).

## `model_calibration`

Reliability bins, 10 rows.

| Column | Type | Example |
|---|---|---|
| `bin` | INTEGER | `5` |
| `mean_predicted` | REAL | `0.52` |
| `mean_observed` | REAL | `0.48` |
| `count` | INTEGER | `127` |

A perfectly calibrated model has `mean_predicted ≈ mean_observed` for every bin.

## `survival_curves`

Cohort survival probabilities from `lifelines.CoxPHFitter`.

| Column | Type | Example |
|---|---|---|
| `cohort` | TEXT | `Manufacturing` |
| `month` | INTEGER | `12` |
| `survival_prob` | REAL | `0.74` |

Used by the original `streamlit_app.py` Survival tab. Not yet surfaced in the production dashboard.

## Indexes

```sql
CREATE INDEX idx_pred_risk_band ON workforce_predictions(risk_band);
CREATE INDEX idx_shap_emp ON shap_feature_impact(employee_id);
CREATE INDEX idx_shap_emp_feat ON shap_feature_impact(employee_id, feature);
```

Built automatically by `train_retention_risk_model.py`.

## Read-only enforcement

The dashboard opens the DB with:

```python
sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
```

The NL→SQL evaluator additionally sets:

```sql
PRAGMA query_only = ON;
```

Even if the LLM generated `DROP TABLE`, the connection rejects it.

## Inspecting the data

```bash
sqlite3 hr_enterprise.db
sqlite> .tables
model_calibration   shap_feature_impact   survival_curves   workforce_predictions

sqlite> SELECT risk_band, COUNT(*) FROM workforce_predictions GROUP BY risk_band;
High Risk|612
Medium Risk|1834
Low Risk|2554

sqlite> SELECT * FROM shap_feature_impact WHERE employee_id = 'EMP_2417';
EMP_2417|tenure_months|0.21
EMP_2417|base_salary|0.12
...
```

## Schema migration

If you change `train_retention_risk_model.py` to add a column, **drop and rebuild** rather than `ALTER TABLE`:

```bash
rm hr_enterprise.db
python train_retention_risk_model.py
```

The DB rebuild is idempotent (~12 seconds) and avoids subtle migration bugs.
