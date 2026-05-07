# 🔍 SHAP Implementation Guide — Optional Week 2 Upgrade

> **When to do this:** Saturday May 16 if you have ~4 hours of energy.
> **Why:** SHAP explainability is the single most-requested feature
> from any HR practitioner who looks at this project. It's also the
> headline feature for the Week 3 carousel and a strong patent angle.

---

## 🎯 What you'll add

A **per-employee feature attribution panel** in the dashboard that shows:

- The 3 top features pushing the risk score *up*
- The 3 top features pushing the risk score *down*
- A waterfall chart showing how each feature contributes to the final probability

This converts "Priya scored 0.81" into "Priya scored 0.81 because of below-band salary (+0.18), no recent promotion (+0.14), and large manager span (+0.09)."

---

## 📦 Step 1 — Install (5 min)

Add to `requirements.txt`:

```
shap==0.45.0
```

Then install:

```bash
source /global/gtsna_northeast6/vanama/python_venvs/py311/bin/activate
pip install shap==0.45.0
```

---

## 🐍 Step 2 — Add SHAP to `predictive_engine.py` (~1 hour)

Add a new function at the bottom of `predictive_engine.py`:

```python
import shap
import numpy as np

# Cache the explainer at module-level so we don't rebuild it every request
_explainer = None

def get_shap_explainer(model):
    """Lazy-init SHAP TreeExplainer. Cached so it's built once per process."""
    global _explainer
    if _explainer is None:
        _explainer = shap.TreeExplainer(model)
    return _explainer


def explain_employee(model, X_employee, feature_names, top_k=3):
    """
    Return SHAP attribution for a single employee.

    Args:
        model: trained scikit-learn classifier
        X_employee: 1-row DataFrame or 1D array of features for ONE employee
        feature_names: list of feature names in same order as X
        top_k: how many top features to surface in each direction

    Returns:
        dict with:
            - 'shap_values': raw shap values (1D array)
            - 'top_positive': list of (feature_name, shap_value) — pushing risk UP
            - 'top_negative': list of (feature_name, shap_value) — pushing risk DOWN
            - 'base_value': model's expected probability before this employee's features
    """
    explainer = get_shap_explainer(model)

    # Handle DataFrame vs array
    if hasattr(X_employee, "values"):
        X_arr = X_employee.values.reshape(1, -1)
    else:
        X_arr = np.array(X_employee).reshape(1, -1)

    # SHAP for binary classifier returns shape (n_samples, n_features, n_classes)
    # We want class 1 (the "leave" class)
    shap_values = explainer.shap_values(X_arr)
    if isinstance(shap_values, list):
        # Older SHAP API: list of arrays per class
        sv = shap_values[1][0]
    elif shap_values.ndim == 3:
        sv = shap_values[0, :, 1]
    else:
        sv = shap_values[0]

    # Pair with feature names and sort
    pairs = list(zip(feature_names, sv))
    pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)

    top_positive = [(name, float(val)) for name, val in pairs_sorted[:top_k] if val > 0]
    top_negative = [(name, float(val)) for name, val in pairs_sorted[-top_k:] if val < 0]

    base_value = explainer.expected_value
    if isinstance(base_value, (list, np.ndarray)):
        base_value = float(base_value[1] if len(base_value) > 1 else base_value[0])
    else:
        base_value = float(base_value)

    return {
        "shap_values": sv.tolist(),
        "top_positive": top_positive,
        "top_negative": top_negative,
        "base_value": base_value,
        "feature_names": list(feature_names),
    }
```

---

## 🎨 Step 3 — Add a SHAP panel to `dashboard.py` (~1.5 hours)

Find the section in `dashboard.py` that renders one employee's detail view (likely under the "High Risk Employees" tab) and add:

```python
import plotly.graph_objects as go

def render_shap_panel(model, employee_row, feature_names):
    """Render an explainability panel for a single employee."""
    from predictive_engine import explain_employee

    st.subheader("🔍 Why is this employee flagged?")

    explanation = explain_employee(model, employee_row, feature_names, top_k=3)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔴 Pushing risk UP**")
        for name, val in explanation["top_positive"]:
            st.markdown(f"• **{name}**: +{val:.3f}")

    with col2:
        st.markdown("**🟢 Pushing risk DOWN**")
        for name, val in explanation["top_negative"]:
            st.markdown(f"• **{name}**: {val:.3f}")

    # Waterfall chart
    feature_names_full = explanation["feature_names"]
    shap_vals = explanation["shap_values"]

    # Sort by absolute value, take top 8 for readability
    pairs = sorted(
        zip(feature_names_full, shap_vals),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:8]
    names = [p[0] for p in pairs]
    values = [p[1] for p in pairs]

    fig = go.Figure(go.Waterfall(
        orientation="h",
        measure=["relative"] * len(names),
        x=values,
        y=names,
        decreasing={"marker": {"color": "#00CC96"}},
        increasing={"marker": {"color": "#EF553B"}},
        text=[f"{v:+.3f}" for v in values],
        textposition="outside",
    ))
    fig.update_layout(
        title="SHAP feature contributions to flight-risk score",
        xaxis_title="Impact on probability",
        height=400,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"Base population probability: {explanation['base_value']:.3f}. "
        f"Bars show how this specific employee's features push the score above or below the baseline."
    )
```

Then call `render_shap_panel(model, selected_employee_row, feature_names)` wherever the employee detail view is rendered.

---

## 🧪 Step 4 — Test it (~30 min)

```bash
source /global/gtsna_northeast6/vanama/python_venvs/py311/bin/activate
streamlit run dashboard.py
```

Click into one high-risk employee. You should see:

- 🔴 Top 3 features pushing UP (red)
- 🟢 Top 3 features pushing DOWN (green)
- Plotly waterfall chart with mixed colors
- Base value caption

**Common gotchas:**
- If `explainer.shap_values()` is slow, cache the entire test-set explanation at startup and look up by employee ID
- If feature names mismatch, check that `feature_names` is captured **after** any one-hot encoding
- If the waterfall chart looks weird, check that the values sum correctly to (final_prob - base_prob)

---

## 📊 Step 5 — Update the README

Add a new bullet to the Features section:

```markdown
### 🔍 Per-Employee Explainability (NEW)
- SHAP TreeExplainer attributions for every prediction
- Top-3 features pushing risk up + top-3 pushing risk down
- Plotly waterfall chart of feature contributions
- Caption surfaces the population baseline for context
```

And re-screenshot the dashboard for `doc/screenshots/`.

---

## 🎯 Step 6 — Use this for the Week 3 carousel

The Week 3 LinkedIn carousel can now have a slide that says:

> *"You asked: 'Why does the model think this?'*
>
> *Now SHAP explains every prediction. Top-3 drivers up. Top-3 drivers down. Waterfall view of feature contributions."*

This is the "I shipped what you asked for" follow-up that LinkedIn's algorithm rewards generously.

---

## 🪪 Patent angle

The combination of:

1. SHAP-based per-employee feature attribution, +
2. SHAP attributions used as the *retrieval query* for RAG over exit interviews

…is the specific novel-combination claim discussed with CSUEB Tech Transfer. By implementing this *before* the patent disclosure conversation, you're strengthening the disclosure (you can demo the working system) and giving the office a more concrete case to act on.

---

## ⏱️ Time budget summary

| Step | Time |
|---|---|
| Install SHAP | 5 min |
| Add explain_employee() | 1 hr |
| Streamlit panel + waterfall | 1.5 hr |
| Test + debug | 30 min |
| README update + screenshots | 30 min |
| **Total** | **~4 hours** |

If you can't do this Saturday, push to Sunday morning. If you can't do it then either, **skip it** — the carousel can use a different angle. Don't burn out before Week 3.
