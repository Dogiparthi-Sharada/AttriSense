<!--
AttriSense — docs/features/fairness-audit.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Fairness Audit

> EEOC four-fifths rule check, calibration drift, and disparate-impact ratios — by department and (extensible) by any protected attribute.

![Fairness audit](../images/fairness.png)

## What you see

- **Disparate-impact ratio** — `(selection_rate_minority / selection_rate_majority)`. The EEOC four-fifths rule says this must be ≥ 0.80.
- **Group-level metrics table** — for each department: positive rate, selection rate, calibration error.
- **Pass/fail badge** — red banner if any group fails the four-fifths rule.
- **Recommendation block** — what to do when a group fails.

On the synthetic dataset the audit reliably reports **DI ratio = 0.20**, which **fails** the four-fifths rule. **This is intentional** — the Manufacturing department is seeded with a stronger turnover signal so the audit has something real to flag.

## What it answers

| Question | Where on the page |
|---|---|
| Is the model selecting one group at a different rate? | Disparate-impact ratio + pass/fail badge |
| Is the model equally well-calibrated across groups? | Calibration error column in the metrics table |
| Which group is most affected? | The row with the lowest selection rate is the disadvantaged group |

## Why this is non-negotiable

If you are going to use any model output in an employment decision (hiring, firing, promotion, comp), **someone is legally entitled to ask** about disparate impact. AttriSense answers that question by default, in the dashboard, with the same data the model used.

For NYC LL144 covered uses, the audit output here is the input to a formal independent bias audit. See [Fairness policy](../ethics/fairness-policy.md).

## Code path

```
production/streamlit_app.py
  └── _fairness_tab(df)
       └── fairness.run_audit(df, dimension="department")
            ├── audit_dimension(df, dimension)         ← per-group GroupMetrics
            └── FairnessReport with pass/fail
```

[`fairness.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/fairness.py) — 188 lines, 4 unit tests.

## Extending to other protected attributes

The audit is dimension-agnostic. To audit by gender, age band, ethnicity, etc.:

```python
from attrisense.fairness import run_audit

report = run_audit(df, dimension="gender_band")
# Returns FairnessReport(passes=False, di_ratio=0.62, ...)
```

The dimension column must exist in the predictions DataFrame. The synthetic dataset only carries `department` because synthetic gender data would be misleading; a real deployment imports protected attributes from the HRIS at audit time only (and never feeds them to the model — that's "fairness through unawareness", which has its own problems but is a sane default).

## EEOC four-fifths rule (what it actually says)

From the [Uniform Guidelines on Employee Selection Procedures (1978)](https://www.eeoc.gov/laws/guidance/questions-and-answers-clarify-and-provide-common-interpretation-uniform-guidelines):

> A selection rate for any race, sex, or ethnic group which is less than four-fifths (4/5) (or eighty percent) of the rate for the group with the highest rate will generally be regarded by the federal enforcement agencies as evidence of adverse impact.

In our setup: `selection` = "model flags employee as high risk". A group whose flag rate is < 80% of the highest-flagged group's rate triggers the warning.

## What to do when it fails

The dashboard shows a **mitigation recommendation** block. The general playbook:

1. **Pause** any downstream automated action on the affected group.
2. **Investigate** — is the disparity in the data, the labelling, or the model?
3. **Retrain** with reweighting, fairness constraints (Fairlearn / Aequitas), or remove the contributing feature.
4. **Re-audit** before lifting the pause.
5. **Document** the entire cycle for the audit log.

## Output artifact

`make -C production fairness` writes `outputs/fairness_report.json`:

```json
{
  "dimension": "department",
  "groups": [
    {"name": "Manufacturing", "selection_rate": 0.31, "calibration_error": 0.04},
    {"name": "Sales", "selection_rate": 0.18, "calibration_error": 0.02},
    {"name": "Engineering", "selection_rate": 0.06, "calibration_error": 0.03}
  ],
  "di_ratio": 0.20,
  "passes_four_fifths_rule": false,
  "disadvantaged_group": "Engineering",
  "recommendation": "..."
}
```

This file is consumed by the dashboard and can also be exported for compliance review.
