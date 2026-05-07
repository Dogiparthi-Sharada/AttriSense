# Fairness — the EEOC four-fifths rule

> A 1978 US Equal Employment Opportunity Commission guideline that's still the legal bright line for adverse impact in hiring and HR decisions.

## The intuition

Imagine a model that flags 25% of Engineering employees as high-risk and 50% of Manufacturing employees. Manufacturing is being **selected at twice the rate** — that's *adverse impact* on Manufacturing.

The four-fifths rule:

$$
\text{ratio} = \frac{\min_g \text{selection\_rate}(g)}{\max_g \text{selection\_rate}(g)} \geq 0.80
$$

If the smallest group's rate is less than 80% of the largest group's rate, the rule is **violated**.

In our example: $0.25 / 0.50 = 0.50$ — fail.

## Why 80%?

Pragmatic compromise. 100% would be impossibly strict; 50% would let almost anything through. The EEOC picked 80% in 1978 and it's stuck. It's not a statistical threshold — it's a **regulatory** one.

## In AttriSense

- **Where**: [`production/src/attrisense/fairness.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/fairness.py).
- **Audit dimensions**: department (always), manager (extensible), tenure band (extensible).
- **Outputs**: `outputs/fairness_report.json` + dashboard banner + audit log row.
- **Behaviour on failure**: pause downstream alerts for the affected group until retraining + re-audit.

## The gotcha

The four-fifths rule **only catches selection-rate disparity**. It doesn't catch:

- **Calibration disparity** — the model is right 90% of the time for group A but only 70% for group B. Both groups can have identical selection rates and still be treated unfairly.
- **Error-rate disparity** — the model has a 10% false-positive rate for one group and 30% for another.
- **Intersectional disparity** — the rule passes on race and on gender separately but fails on `race × gender`.

For a real audit you need **multiple fairness lenses**, plus a decision about which one matters most for your use case. The dashboard's audit is the **technical artifact** for that conversation; it's not the conversation itself.

## Try it

```python
from attrisense.fairness import run_audit
import pandas as pd
import sqlite3

with sqlite3.connect("hr_enterprise.db") as conn:
    df = pd.read_sql("SELECT * FROM workforce_predictions", conn)

report = run_audit(df, dimension="department", threshold=0.7, label_col="risk_label")
print(report)
```

## Two layers AttriSense ships, not one

Most fairness write-ups stop at the four-fifths audit. AttriSense ships **two layers**, because the audit alone doesn't fix the bias that creeps in *after* the model produces a number.

### Layer 1 — model-side: the four-fifths *gate*

The audit is **blocking**, not advisory. If the disparate-impact ratio drops below `0.80` between protected groups on a dimension we audit, the recommendation is **suppressed** before it reaches the dashboard, and the dashboard surfaces a banner explaining why. This is implemented in [`production/src/attrisense/fairness.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/fairness.py); the gate is invoked from the executive tab and the alert tab before any score, driver, or intervention is rendered.

### Layer 2 — reviewer-side: the salted Review_ID

Even if the model and its audit are perfect, **reviewers introduce bias on the dashboard**. When a reviewer sees `Emp_ID = E001` and recognises the person ("oh, that's Ravi from Manufacturing"), they anchor on memory and silently override the model — saving the people they like, escalating the people they don't. Pure audit dashboards never catch this; the bias is in the human reading the screen, not the data.

AttriSense never displays the raw `Emp_ID`. Every dashboard view replaces it with a salted SHA-256 **Review_ID** of the form `RV-NNNNNN` (six lowercase hex chars), produced by [`production/src/attrisense/identity.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/identity.py). The salt is rotatable per pilot via the `ATTRISENSE_REVIEW_ID_SALT` environment variable, so:

- **Same employee, same pilot** → same Review_ID (so the dashboard remains coherent within a session).
- **Same employee, different pilot** → different Review_ID (so longitudinal cross-pilot tracking requires explicit consent and key custody).
- **Different employee, same pilot** → different Review_ID (collision probability negligible at HR-corpus sizes).

The reviewer can no longer anchor on memory because every record looks the same. The audit catches *model-side* disparate impact; Review_ID stops *reviewer-side* identification bias. We need both.

## What the audit does not catch

The four-fifths rule **only catches selection-rate disparity**. Even with the gate passing and Review_IDs in place, you still want to monitor:

- **Calibration disparity** — the model is right 90% of the time for group A but only 70% for group B. Selection rates can be identical and the groups can still be treated unfairly. Tracked in `outputs/calibration_by_group.json`.
- **Error-rate disparity** — false-positive rate is 10% for one group and 30% for another. Tracked in the per-department fairness audit table in the IEEE paper.
- **Intersectional disparity** — the rule passes on race and on gender separately but fails on `race × gender`. The 90-day roadmap (`career/week4/05_90_day_roadmap.md`) includes intersectional audit as a Q3 deliverable.

For a real audit you need **multiple fairness lenses**, plus a decision about which one matters most for your use case. The dashboard's audit is the **technical artefact** for that conversation; it is not the conversation itself.

## Quick definitions for the impatient reader

- **Fairness** — in this project: the property that the model's *outputs* and the dashboard's *reviewer interface* do not produce systematically different decisions for protected groups beyond what the (synthetic) data justifies. Fairness is a **system property**, not a model property — it requires both the four-fifths gate (model side) and the Review_ID layer (reviewer side).
- **Fairness audit** — the per-dimension calculation that checks the four-fifths rule on each predicted label, persisted to `outputs/fairness_report.json` and rendered in the Fairness tab. The audit is **blocking**: a fail suppresses recommendations until retraining and re-audit.
- **Disparate-impact ratio (DI)** — `min(group selection rate) / max(group selection rate)`. Pass if `DI ≥ 0.80`.
- **Selection rate** — the fraction of a group flagged High Risk by the model.
- **Protected class** — a characteristic the law restricts decisions on (race, sex, age, disability, etc.). For this synthetic project we audit Department as a stand-in; in a real pilot you would audit the actual protected attributes.

