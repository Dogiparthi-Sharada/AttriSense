# Executive Dashboard

> The opening tab. KPI cards plus the population risk distribution. What an HR director sees first.

![Executive dashboard](../images/executive.png)

## What you see

- **KPI strip (4 cards)** — total employees, high-risk count, high-risk %, average risk.
- **Risk distribution histogram** — Plotly histogram of risk probabilities, coloured by band (Low / Medium / High).
- **Risk by department** — stacked bar showing where the risk concentrates.
- **Top 10 highest-risk employees** — a sortable table.

All four widgets read from the same cached `predictions` DataFrame — switching tabs is instant.

## What it answers

| Question | Where on the page |
|---|---|
| How many people are at high risk this period? | KPI card #2 |
| Is the risk concentrated in one department? | "Risk by department" stacked bar |
| Where do I aim my retention budget? | Top-10 table → drill into Compare or SHAP |
| Has overall risk shifted vs. last retrain? | KPI card #4 (avg risk) — compare across runs in `outputs/metrics_snapshot.txt` |

## Code path

```
production/streamlit_app.py
  └── _executive_tab(df)               ←  this function
       ├── load_predictions()          ←  cached SQLite read
       ├── plotly histogram            ←  apply_plotly_defaults(fig)
       └── plotly stacked bar          ←  CATEGORICAL palette from theme.py
```

## Risk thresholds

Defined in [`config.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/config.py#L40):

```python
RISK_THRESHOLDS = {
    "high": 0.75,
    "medium": 0.40,
}
```

Anything above 0.75 is `High Risk`, between 0.40 and 0.75 is `Medium Risk`, below 0.40 is `Low Risk`. Adjust here once and every tab updates.

## Color contract

| Band | Color | Hex | From |
|---|---|---|---|
| High Risk | Coral | `#F87171` | `theme.RISK_COLOR_MAP` |
| Medium Risk | Amber | `#FBBF24` | `theme.RISK_COLOR_MAP` |
| Low Risk | Teal | `#34D399` | `theme.RISK_COLOR_MAP` |

The same map is used everywhere risk is shown — see [theme.py](../reference/api.md#theme).

## Why no time-series

The synthetic dataset is a single snapshot. Real deployments would add a `snapshot_date` column to `workforce_predictions` and a fifth KPI tracking month-over-month risk change. Listed in [roadmap.md](../roadmap.md).
