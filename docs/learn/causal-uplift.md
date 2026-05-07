<!--
AttriSense — docs/learn/causal-uplift.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Causal uplift — T-Learner

> *"Will a 10% raise prevent this employee from leaving?"* — a **causal** question. The Random Forest predicts who's at risk; uplift estimates **the effect of an intervention**.

## The intuition

A predictive model answers `P(leave | x)`. A causal model answers `P(leave | x, treatment) − P(leave | x, no treatment)` — the **uplift** of the treatment.

Three concrete treatment arms in AttriSense:

| Arm | Cost | Question |
|---|---|---|
| 5% raise | low | does a small raise reduce the risk? |
| 10% raise | medium | does doubling it reduce the risk twice as much? |
| Manager change | medium | does a fresh manager reset risk? |

For each employee we want the **conditional average treatment effect (CATE)** — the uplift *for this person*, not the population.

## The math, lightly

A **T-Learner** (T = "two") fits two separate models:

$$
\mu_0(x) = \mathbb{E}[Y \mid X=x, T=0] \quad \text{(no treatment)}
$$
$$
\mu_1(x) = \mathbb{E}[Y \mid X=x, T=1] \quad \text{(treatment)}
$$

CATE for individual $i$:

$$
\hat\tau(x_i) = \mu_1(x_i) - \mu_0(x_i)
$$

Other learners exist (S-Learner, X-Learner, DR-Learner, DML). T-Learner is the simplest and a fine starting point when you have enough data in both arms.

## In AttriSense

- **Library**: [EconML](https://econml.azurewebsites.net/) (`econml.metalearners.TLearner`).
- **Where**: [`production/src/attrisense/causal_uplift.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/causal_uplift.py).
- **Synthetic treatment data**: AttriSense doesn't have observed treatment data, so the demo **simulates** assignment with a known true effect. This means the causal numbers are *illustrative*, not real-world calibrated. The same pattern applies once you have real treatment logs.

## The gotcha

**Causal inference is not predictive accuracy.** A model can have great predictive AUC and produce useless CATE estimates if:

- Treatment was not randomly assigned (selection bias)
- Important confounders are unobserved
- Overlap fails (no untreated employees with this $x$, or no treated employees with this $x$)

In real deployments, you must validate **causal assumptions** before believing the uplift numbers. The dashboard shows uplift; it doesn't validate the assumptions for you.

## Try it

```python
from econml.metalearners import TLearner
from sklearn.ensemble import GradientBoostingRegressor

T_learner = TLearner(models=GradientBoostingRegressor())
T_learner.fit(Y=y, T=treatment, X=X)
cate = T_learner.effect(X)   # one number per row: the predicted uplift
```
