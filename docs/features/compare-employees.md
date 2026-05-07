<!--
AttriSense — docs/features/compare-employees.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Compare Two Employees

> Side-by-side panel for two employees. Shows the risk delta and the top SHAP drivers for each.

![Compare](../images/compare.png)

## What you see

- **Two employee pickers** — searchable dropdowns of all employee IDs.
- **Side-by-side cards** — risk score, band, tenure, salary, department, manager.
- **Headline drivers list** — top 3 SHAP features per employee, with sign + magnitude.
- **Delta** — direct numeric difference in risk score.

## What it answers

| Question | Where on the page |
|---|---|
| Why is Alex flagged but Sam isn't? | Headline drivers — different feature contributions explain the gap |
| Two equally-risky people — what's different about them? | Drivers list shows different reasons for the same score |
| Is the model treating two similar employees similarly? | Eyeball check — same dept, same tenure, similar score? |

## Code path

```
production/streamlit_app.py
  └── _compare_tab(df)
       └── compare.render_comparison_panel(df, emp_a, emp_b)
            ├── compare.headline_drivers(df, emp_id, top_n=3)
            └── render two side-by-side st.column blocks
```

[`compare.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/compare.py) — 154 lines, fully unit-tested.

## The bug we fixed

Early version raised `KeyError` on every tab. Root cause:

```python
# Wrong: SQLite stores booleans as 0/1 ints — boolean indexing fails
explained = df[df["SHAP_Explained"]]
```

```python
# Right: cast first
explained = df[df["SHAP_Explained"].astype(bool)]
```

The fix lives in [`compare.py:headline_drivers()`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/compare.py) and is regression-tested by [`test_compare.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/tests/test_compare.py).

## Why a separate tab vs. modal in SHAP

Comparing two people requires **picking two**. A modal flow would force the user to remember the first selection while making the second. A dedicated tab with two pickers side-by-side is the common-sense interaction.
