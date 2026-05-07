# SHAP — explain any prediction

> *"The model said this employee is high-risk. **Why?**"* — SHAP answers that question, one employee at a time.

## The intuition

Imagine a black-box model that takes 4 inputs and outputs a risk score:

```
tenure=7, salary=52k, dept=Mfg, mgr_tenure=4   →   model   →   risk = 0.83
```

SHAP gives you a **decomposition**:

```
baseline (avg risk for everyone)         = 0.32
+ short tenure (7 months)                = +0.21
+ low salary (52k vs 78k median)         = +0.18
+ Manufacturing dept                     = +0.09
+ new manager (4 months)                 = +0.03
─────────────────────────────────────────────────
final risk for this employee             = 0.83
```

Every contribution sums to the final prediction. Always. That's the **only** thing SHAP guarantees, and it's why we use it.

## The math, lightly

SHAP values come from cooperative game theory (Shapley, 1953). For each feature `i`:

$$
\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! \, (|F| - |S| - 1)!}{|F|!} \, \big[ f(S \cup \{i\}) - f(S) \big]
$$

Plain English: *the average marginal contribution of feature `i` across all possible orderings of the other features*.

For tree models (Random Forest, XGBoost), `TreeExplainer` computes this **exactly** in polynomial time. For other models there's `KernelExplainer` (sampled, slower).

## In AttriSense

- **Where**: [`train_retention_risk_model.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/train_retention_risk_model.py) computes SHAP values during training and stores them in the `shap_feature_impact` table.
- **What we store**: top-K drivers per employee + a `SHAP_Explained` flag (only high-risk + a sampled subset get full SHAP, to keep the DB compact).
- **Where it surfaces**: SHAP Insights tab + Compare tab + driver cards.

## The gotcha

**SHAP explains the model, not the world.** If your model has spurious correlations, SHAP will faithfully explain those spurious correlations. SHAP says *"this prediction depended on `salary`"* — it does **not** say *"salary causes attrition"*.

For "what changes if I do X?" → use **causal uplift** ([`causal-uplift.md`](causal-uplift.md)), not SHAP.

## Try it

```python
import shap, joblib
import pandas as pd

model = joblib.load("attrisense_model.joblib")
df = pd.read_csv("attrisense_synthetic_hr.csv")
X = df[["tenure_months", "base_salary", "department_code", "manager_tenure_months"]]

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X.iloc[:5])
print(shap_values)        # one row per employee, one column per feature
```

To visualise:

```python
shap.waterfall_plot(shap.Explanation(
    values=shap_values[1][0],
    base_values=explainer.expected_value[1],
    data=X.iloc[0],
    feature_names=X.columns.tolist(),
))
```
