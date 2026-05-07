# Intended use

> The boundary. What this is for, what it isn't, and what to do when someone asks you to take it past the line.

## What AttriSense IS for

| Use case | Notes |
|---|---|
| Portfolio demonstration | The original purpose. |
| Analytics prototyping | Use the package as a starter for a real workforce-analytics service. |
| Responsible-AI training material | Fairness audit + model card + intended-use boundary are intentionally explicit. |
| HR-tech vendor evaluation | Compare your vendor's explanation surface to AttriSense's — if theirs is worse, ask why. |
| Internal early-warning tool | **Only** with a human in the loop, an independent bias audit, and a documented appeal process. |

## What AttriSense is NOT for

| Use case | Why not |
|---|---|
| Termination decisions | Correlational signal — risk does not equal cause. |
| Compensation denial | Same. Plus risk of perpetuating historic pay gaps. |
| Promotion denial | Same. |
| Hiring decisions | The model is trained on existing-employee data — it cannot generalise to candidates. |
| Background-check signal | The model has no information about the person beyond their HRIS record. |
| Anything covered by [NYC LL144](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page) | Without an independent third-party bias audit. |
| Anything that benefits a third party at the employee's expense | Including selling risk lists to insurers / lenders / etc. |

## When someone asks you to take it past the line

You will eventually be asked to. The question will be reasonable-sounding:

> *"Can we use the high-risk list to prioritise who gets the first round of layoffs?"*
> *"Can we tag high-risk employees as ineligible for the promotion track this cycle?"*
> *"Can we stop offering retention bonuses to the low-risk segment?"*

The answer is **no** for all of them. The reason is the same: a correlational risk score is being used as the **sole or primary basis** for an adverse employment action.

Practical rebuttals:

| The ask | The rebuttal |
|---|---|
| "It's just one input among many." | What weight does it get? Show the formula. If the model output is in the formula, the model output drove the decision. |
| "We already do this informally." | Then formalising it requires the bias audit and appeal process. Same standard as a third-party tool. |
| "We're a private company, we can do what we want." | At-will employment doesn't override Title VII / state-level employment law / your own ethics policy. |
| "The model is just predicting what would happen anyway." | Predictions are not destiny. Acting on them changes them. |

## The escalation path

If you are working on AttriSense (or a fork of it) and you're asked to remove the limitations or extend it past the boundary above:

1. **Refer the asker to this page**.
2. If they push back, refer to the [Model Card](model-card.md) and [Fairness Policy](fairness-policy.md).
3. If they push back on those, escalate to legal / People Ops / the ethics committee.
4. If your organisation has none of those, **stop building**.

The model card explicitly disclaims real employment-decision use. Disclaiming is the floor, not the ceiling.

## What real production-readiness looks like

A real deployment needs all of:

- [ ] Independent third-party bias audit (annual)
- [ ] Documented intended-use policy signed by legal
- [ ] Documented appeal process accessible to all flagged employees
- [ ] Documented threshold-setting process (who chose 0.75? why?)
- [ ] Documented retraining cadence
- [ ] Documented data-minimisation: only the four required features in the model
- [ ] Documented data-retention: how long are SHAP values kept? Risk scores?
- [ ] Documented access control: who can see which employees' scores?
- [ ] Documented change log (model version, training data window, threshold)
- [ ] Documented incident response: what to do when fairness breaks in production
- [ ] User-facing notice: employees know the model exists, what it does, what it doesn't do
- [ ] Manager training: managers know what scores mean and how to use them
- [ ] Periodic post-deployment evaluation: did interventions actually retain people?

The technical work is < 10% of this list. The other > 90% is policy, governance, and human process. AttriSense gives you the technical work in a defensible shape so the rest of the work has a stable foundation.

## What to read next

- [Model card](model-card.md) — the canonical disclosure.
- [Fairness policy](fairness-policy.md) — the audit + escalation policy.
- [Decisions](../design/decisions.md) — why each design choice was made.
