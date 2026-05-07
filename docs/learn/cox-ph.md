<!--
AttriSense — docs/learn/cox-ph.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Cox proportional hazards — survival analysis

> *"Will this employee leave?"* is a **classification** question. *"How long until they leave?"* is a **survival** question. Different math, different answer.

## The intuition

Survival analysis was invented to answer questions like *"how long do patients live after diagnosis?"* — where you have:

- **An event** (death, churn, attrition).
- **A time-to-event** for some observations.
- **Censored** observations: people who haven't had the event *yet* — but might tomorrow.

A classifier throws away the time information. A Cox model uses it.

## The math, lightly

The **hazard function** $h(t)$ is the instantaneous risk of the event at time $t$ given survival up to $t$.

Cox's proportional hazards model:

$$
h(t \mid x) = h_0(t) \cdot \exp(\beta_1 x_1 + \beta_2 x_2 + \dots + \beta_p x_p)
$$

Two parts:

- $h_0(t)$ — a **baseline hazard** that depends on time but not on features (left non-parametric).
- $\exp(\beta^T x)$ — a **multiplier** that depends on features but not time.

This is the **proportional hazards** assumption: hazard ratios between two individuals are constant over time. If feature $x_1$ doubles your hazard at month 1, it doubles your hazard at month 24 too.

## In AttriSense

- **Library**: [`lifelines`](https://lifelines.readthedocs.io/) (`CoxPHFitter`).
- **Features used** (not the same as the classifier — `Tenure_Months` would be cheating since it *is* the time variable):

  ```python
  SURVIVAL_FEATURE_COLUMNS = ["Base_Salary", "Dept_Code", "Manager_Tenure_Months"]
  ```

- **Output**: per-employee survival curves stored in `survival_curves`.
- **Surfaced as**: the survival sparkline on the SHAP Insights tab.

## The gotcha

The **proportional hazards assumption** rarely holds perfectly in workforce data. New hires often have a "honeymoon" hazard pattern that violates PH. Check with `lifelines.statistics.proportional_hazard_test` and split the model by tenure band if it fails.

## Try it

```python
from lifelines import CoxPHFitter
import pandas as pd

df = pd.read_csv("attrisense_synthetic_hr.csv")
df = df.rename(columns={"tenure_months": "T", "voluntary_turnover": "E"})

cph = CoxPHFitter()
cph.fit(df[["T", "E", "base_salary", "manager_tenure_months"]], duration_col="T", event_col="E")
cph.print_summary()
```
