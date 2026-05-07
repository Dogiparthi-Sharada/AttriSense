<!--
AttriSense — docs/features/causal-uplift.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Causal Uplift

> The "what should I do" tab. EconML T-learner picks the intervention most likely to retain each high-risk employee.

![Causal uplift](../images/uplift.png)

## What you see

- **Intervention recommendation column** — for each high-risk employee, one of:
  - `salary_lift_10pct`
  - `manager_change`
  - `tenure_bonus_12mo`
  - `none` (no intervention has positive predicted uplift)
- **Aggregate breakdown** — bar chart of recommendation counts by intervention.
- **Per-employee uplift table** — predicted retention probability under each treatment, side-by-side with the no-treatment baseline.

## What it answers

| Question | Where on the page |
|---|---|
| If I can only afford one intervention per quarter, which employees get it? | Filter the table to recommendation = `salary_lift_10pct`, sort by uplift |
| Is salary or manager the bigger lever? | Aggregate breakdown bar chart |
| For *this* high-risk employee, which intervention has the biggest predicted impact? | Per-employee table row — compare the four columns |

## Why causal, not just correlational

Standard ML answers **"who is at risk"**.

It cannot answer **"what should I do about it"** because the historical data does not show counterfactuals — we only see one outcome per employee.

Causal inference (specifically EconML's T-learner pattern) trains **one outcome model per treatment arm**, then estimates each employee's expected outcome under each intervention.

The recommendation is the intervention with the highest **predicted uplift** (probability of retention under treatment minus probability under control).

## Code path

```
production/streamlit_app.py
  └── _causal_tab(df)
       └── causal_uplift.compute_uplift_table(df)
            ├── INTERVENTIONS tuple                 ← 3 named treatments
            ├── econml.metalearners.TLearner        ← one model per arm
            └── persisted to data/causal_uplift.csv ← reused across reruns
```

[`causal_uplift.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/causal_uplift.py) — 235 lines.

## Synthetic treatments

Real causal inference needs **observed treatment** in the historical data. The synthetic dataset doesn't have that, so:

- We **simulate** treatment assignment from observable features.
- We train T-learner outcome models on the simulated data.
- We **report uplift** as the model output, not as a real causal estimate.

This is honest demoware. A real deployment would:

1. Import `treatment_assigned` and `treatment_date` columns from the HRIS.
2. Apply propensity-score matching or doubly-robust estimation.
3. Validate the assumptions (overlap, no unmeasured confounding, SUTVA).

This is on the [roadmap](../roadmap.md).

## Known limits

- T-learner is the simplest meta-learner. X-learner / DR-learner / DML are more robust to confounding.
- Single time horizon (current period). No dynamic treatment effects.
- No interaction effects between treatments (e.g., manager change + salary lift simultaneously).

## Output sanity-check

On the 5,000-row synthetic dataset, the breakdown reliably comes out:

- `manager_change` — ~1,800 employees
- `salary_lift_10pct` — ~1,700 employees
- `tenure_bonus_12mo` — ~1,500 employees

If your numbers are wildly different, check that `data/causal_uplift.csv` was rebuilt after the most recent retrain (`make -C production uplift`).
