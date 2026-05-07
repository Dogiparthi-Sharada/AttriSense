# SMOTE — synthetic minority oversampling

> *"Only 18% of employees leave. The model just predicts 'stays' for everyone and gets 82% accuracy. Useless."* — SMOTE fixes that.

## The intuition

Classification models minimise overall error. If 82% of training rows are class `0` and 18% are class `1`, the model can score 82% by predicting `0` always — and learn nothing about class `1`.

SMOTE (Synthetic Minority Oversampling Technique) **synthesises new minority-class examples** by interpolating between existing ones, until both classes are balanced.

```
before:                        after SMOTE:
class 0: ████████ (4100)       class 0: ████████ (4100)
class 1: ██       (900)        class 1: ████████ (4100, ~3200 synthetic)
```

## The math, lightly

For each minority sample $x_i$:

1. Find its $k$ nearest minority neighbours (default $k = 5$).
2. Pick one neighbour $x_j$ at random.
3. Generate a synthetic sample $x_{new} = x_i + \lambda \cdot (x_j - x_i)$, with $\lambda \in [0, 1]$ random.

The synthetic sample lies on the line segment between two real minority neighbours. It's **not a duplicate** — that's the point. Plain duplication overfits; interpolation generalises.

## In AttriSense

- **Where**: [`train_retention_risk_model.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/train_retention_risk_model.py) — `imblearn.over_sampling.SMOTE` is applied to the **training fold only** (never to test).
- **Order**: split → SMOTE → fit. Critically, **never SMOTE before splitting**, or test-set leakage is guaranteed.

## The gotcha

**SMOTE can hide a fairness problem.** If the minority class is dominated by one demographic group, SMOTE inflates that group's footprint in the training data. The model now appears more accurate but is more biased toward that group's pattern.

Always run the [fairness audit](fairness.md) **after** SMOTE, never before.

Also: SMOTE doesn't help calibration. Probabilities from a SMOTE-trained model are systematically **too confident** for the minority class. If you need calibrated probabilities, run `CalibratedClassifierCV` after fitting.

## Try it

```python
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, random_state=42)

print("before:", y_tr.value_counts().to_dict())
X_tr_bal, y_tr_bal = SMOTE(random_state=42).fit_resample(X_tr, y_tr)
print("after :", y_tr_bal.value_counts().to_dict())
```
