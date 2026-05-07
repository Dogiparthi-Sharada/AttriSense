"""Compare-Two-Employees side-by-side panel.

Renders feature values, predicted probability, and SHAP attributions for
two employees side by side. Designed for the "why is X higher risk than
Y?" interview question.
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from attrisense.theme import CORAL, SAGE, apply_plotly_defaults, show_styled

from attrisense.config import SHAP_COLUMNS, SHAP_DRIVER_LABELS


_DISPLAY_FIELDS: tuple[tuple[str, str, str], ...] = (
    ("Department", "Department", "{}"),
    ("Tenure_Months", "Tenure (months)", "{}"),
    ("Base_Salary", "Base salary", "${:,.0f}"),
    ("Manager_ID", "Manager ID", "{}"),
    ("Manager_Tenure_Months", "Manager tenure (months)", "{}"),
    ("Flight_Risk_Probability", "Flight-risk probability", "{:.3f}"),
    ("Risk_Level", "Risk band", "{}"),
)


def _format(value: object, template: str) -> str:
    """Format a value safely, handling NaN and missing keys."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    try:
        return template.format(value)
    except (TypeError, ValueError):
        return str(value)


def _shap_table(employee: pd.Series) -> pd.DataFrame:
    """Pull SHAP impact values from an employee row, labelled for humans."""
    rows = []
    for column in SHAP_COLUMNS:
        impact = employee.get(column)
        rows.append(
            {
                "Driver": SHAP_DRIVER_LABELS[column],
                "SHAP_Impact": float(impact) if pd.notna(impact) else 0.0,
            }
        )
    return pd.DataFrame(rows)


def render_comparison_panel(df: pd.DataFrame) -> None:
    """Render the side-by-side comparison panel inside the Streamlit app."""
    st.markdown("#### Compare Two Employees")
    st.caption(
        "Pick any two employees to see how their features and SHAP risk "
        "drivers differ. Useful for explaining why one is flagged and the "
        "other is not."
    )

    if "SHAP_Explained" in df.columns:
        # SQLite stores booleans as 0/1 ints — coerce before boolean indexing
        # to avoid pandas treating it as positional integer indexing.
        explained = df[df["SHAP_Explained"].astype(bool)]
    else:
        explained = df
    if explained.empty:
        st.info("No SHAP-explained employees in the database. Re-run training.")
        return

    from attrisense.identity import to_review_id

    employee_options = explained.sort_values("Flight_Risk_Probability", ascending=False)
    label_map = {
        f"{to_review_id(row.Emp_ID)} — {row.Department} — {row.Risk_Level} ({row.Flight_Risk_Probability:.2f})":
        row.Emp_ID
        for row in employee_options.itertuples()
    }
    labels = list(label_map.keys())

    col_a, col_b = st.columns(2)
    with col_a:
        label_a = st.selectbox("Employee A", labels, index=0, key="compare_a")
    with col_b:
        default_b = 1 if len(labels) > 1 else 0
        label_b = st.selectbox("Employee B", labels, index=default_b, key="compare_b")

    emp_a = explained[explained["Emp_ID"] == label_map[label_a]].iloc[0]
    emp_b = explained[explained["Emp_ID"] == label_map[label_b]].iloc[0]

    # Feature side-by-side
    field_rows = []
    for column, label, template in _DISPLAY_FIELDS:
        field_rows.append(
            {
                "Field": label,
                "Employee A": _format(emp_a.get(column), template),
                "Employee B": _format(emp_b.get(column), template),
            }
        )
    field_df = pd.DataFrame(field_rows)
    _styled = (
        field_df.style
        .set_properties(**{
            "background-color": "#FBF7F2",
            "color": "#1F1E1B",
            "font-weight": "600",
            "border": "1px solid #E7DECF",
        })
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#F5EFE6"),
                ("color", "#1F1E1B"),
                ("font-weight", "700"),
                ("border", "1px solid #E7DECF"),
            ]},
            {"selector": "td", "props": [("color", "#1F1E1B !important")]},
        ])
    )
    show_styled(st, _styled)

    # SHAP attribution chart
    shap_a = _shap_table(emp_a).rename(columns={"SHAP_Impact": "Employee A"})
    shap_b = _shap_table(emp_b).rename(columns={"SHAP_Impact": "Employee B"})
    merged = shap_a.merge(shap_b, on="Driver")

    fig = go.Figure()
    fig.add_bar(
        x=merged["Driver"],
        y=merged["Employee A"],
        name=to_review_id(emp_a.Emp_ID),
        marker_color=CORAL,
    )
    fig.add_bar(
        x=merged["Driver"],
        y=merged["Employee B"],
        name=to_review_id(emp_b.Emp_ID),
        marker_color=SAGE,
    )
    fig.update_layout(
        barmode="group",
        title="SHAP risk-driver attribution (positive = pushes risk up)",
        height=420,
        yaxis_title="Impact on flight-risk probability",
        legend=dict(orientation="h", y=-0.2),
    )
    apply_plotly_defaults(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    delta = float(emp_a["Flight_Risk_Probability"]) - float(emp_b["Flight_Risk_Probability"])
    st.metric(
        "Probability gap (A − B)",
        f"{delta:+.3f}",
        help=(
            "Positive numbers mean Employee A is the higher-risk employee. "
            "Compare the SHAP bars above to see which features drive the gap."
        ),
    )


def headline_drivers(employee: pd.Series, top_k: int = 2) -> list[str]:
    """Return the top SHAP drivers as human-readable strings.

    Used by the Slack-alert mock and the onboarding tour.
    """
    pairs: Iterable[tuple[str, float]] = (
        (SHAP_DRIVER_LABELS[column], float(employee.get(column, 0.0) or 0.0))
        for column in SHAP_COLUMNS
    )
    sorted_pairs = sorted(pairs, key=lambda item: abs(item[1]), reverse=True)[:top_k]
    return [
        f"{label} ({impact:+.2f})"
        for label, impact in sorted_pairs
    ]
