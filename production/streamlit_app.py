# ---------------------------------------------------------------------------
# AttriSense — production/streamlit_app.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""AttriSense \u2014 Workforce Intelligence dashboard.

Single-page Streamlit app that reads from `hr_enterprise.db` and adds:

- Executive KPIs and risk distribution
- SHAP global drivers
- Compare-Two-Employees side-by-side panel
- Causal uplift recommendations (EconML T-learner)
- Fairness audit (EEOC four-fifths rule, calibration drift)
- NL\u2192SQL Assistant with a graceful fallback when the LLM cannot
  produce a valid query (TF-IDF suggestions over a 50-question gold set)
- Multilingual exit-interview RAG (English / Spanish / Hindi)
- Slack/Teams alert mock
- Limitations & Ethics

Original `streamlit_app.py` is intentionally unmodified.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from dotenv import load_dotenv

_THIS_DIR = Path(__file__).resolve().parent
_SRC_DIR = _THIS_DIR / "src"
_REPO_ROOT = _THIS_DIR.parent
for _path in (_SRC_DIR, _REPO_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

# Load .env from the repo root so the AI Assistant can see OPENAI_API_KEY
# regardless of the directory Streamlit was launched from.
load_dotenv(dotenv_path=_REPO_ROOT / ".env", override=False)

from attrisense.compare import render_comparison_panel
from attrisense.config import (
    CAUSAL_UPLIFT_TABLE,
    DATABASE_PATH,
    SHAP_FEATURE_TABLE_NAME,
    SQL_TABLE_NAME,
)
from attrisense.fairness import load_report as load_fairness_report
from attrisense.fairness import run_audit
from attrisense.identity import to_review_id
from attrisense.legacy_tabs import (
    render_decision_tools,
    render_detailed_analytics,
    render_survival_and_calibration,
)


def _pseudonymize(frame: pd.DataFrame) -> pd.DataFrame:
    """Replace any ``Emp_ID`` column with a pseudonymous ``Review_ID``.

    Identification-bias mitigation: a reviewer who can recognise an
    employee id (e.g. EMP_2417 = Ravi) anchors on memory and bypasses the
    model. The dashboard therefore never displays the raw id.
    """
    if "Emp_ID" not in frame.columns:
        return frame
    out = frame.copy()
    out.insert(0, "Review_ID", out["Emp_ID"].map(to_review_id))
    out = out.drop(columns=["Emp_ID"])
    return out
from attrisense.nl_sql_eval import load_report as load_eval_report
from attrisense.nl_sql_eval import run_evaluation
from attrisense.nl_sql_fallback import execute_gold_sql, suggest
from attrisense.onboarding import render_onboarding_tour, reset_onboarding_tour
from attrisense.slack_alert_mock import render_alert_mock
from attrisense.theme import (
    CSS,
    CATEGORICAL,
    CORAL,
    BUTTER,
    SAGE,
    LAVENDER,
    PEACH,
    DUSTY_BLUE,
    MINT,
    RISK_COLOR_MAP,
    SEQUENTIAL,
    apply_plotly_defaults,
    pastel_table,
    render_brand_header,
    render_disclosure,
    show_styled,
)


st.set_page_config(
    page_title="AttriSense \u2014 Workforce Intelligence",
    page_icon="\U0001F4CA",
    layout="wide",
)

st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

@st.cache_data(ttl=300)
def load_predictions() -> pd.DataFrame:
    """Read the workforce_predictions table once per session window."""
    if not Path(DATABASE_PATH).exists():
        return pd.DataFrame()
    with sqlite3.connect(DATABASE_PATH) as connection:
        return pd.read_sql_query(f"SELECT * FROM {SQL_TABLE_NAME}", connection)


@st.cache_data(ttl=300)
def load_optional(table_name: str) -> pd.DataFrame:
    """Read any optional SQLite table or return an empty DataFrame."""
    if not Path(DATABASE_PATH).exists():
        return pd.DataFrame()
    with sqlite3.connect(DATABASE_PATH) as connection:
        exists = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        ).fetchone()
        if not exists:
            return pd.DataFrame()
        return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


# ---------------------------------------------------------------------------
# Tab renderers
# ---------------------------------------------------------------------------

def _executive_kpis(df: pd.DataFrame) -> None:
    """Top-row metrics shown on the Executive tab."""
    high = int((df["Risk_Level"] == "High Risk").sum())
    med = int((df["Risk_Level"] == "Medium Risk").sum())
    pct_high = high / max(len(df), 1) * 100
    avg_risk = float(df["Flight_Risk_Probability"].mean())
    cols = st.columns(5)
    cols[0].metric("Total workforce", f"{len(df):,}")
    cols[1].metric("High risk", f"{high:,}", f"{pct_high:.1f}% of force",
                   delta_color="inverse")
    cols[2].metric("Medium risk", f"{med:,}")
    cols[3].metric("Avg flight-risk", f"{avg_risk:.2%}")
    cols[4].metric("Avg tenure", f"{df['Tenure_Months'].mean():.1f} mo")


def _executive_tab(df: pd.DataFrame) -> None:
    st.subheader("Executive Dashboard")
    _executive_kpis(df)

    st.markdown("---")

    # ── Row 1 ── Risk donut + Department high-risk bar ──────────────────
    risk_counts = (
        df["Risk_Level"]
        .value_counts()
        .reindex(["High Risk", "Medium Risk", "Low Risk"])
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    risk_counts.columns = ["Risk_Level", "Count"]

    dept_summary = (
        df.groupby("Department", as_index=False)
        .agg(
            employees=("Emp_ID", "count"),
            high_risk=("Risk_Level", lambda v: int((v == "High Risk").sum())),
            avg_risk=("Flight_Risk_Probability", "mean"),
            avg_salary=("Base_Salary", "mean"),
            avg_tenure=("Tenure_Months", "mean"),
        )
        .sort_values("high_risk", ascending=False)
    )
    dept_summary["high_risk_rate"] = dept_summary["high_risk"] / dept_summary["employees"]

    c1, c2 = st.columns([1, 1.3])

    with c1:
        donut = go.Figure(
            go.Pie(
                labels=risk_counts["Risk_Level"],
                values=risk_counts["Count"],
                hole=0.55,
                marker=dict(
                    colors=[RISK_COLOR_MAP[r] for r in risk_counts["Risk_Level"]],
                    line=dict(color="#FBF7F2", width=3),
                ),
                textfont=dict(color="#000000", size=13),
                hovertemplate="<b>%{label}</b><br>%{value:,} employees<br>%{percent}<extra></extra>",
            )
        )
        donut.update_layout(
            title="Workforce risk mix",
            annotations=[
                dict(
                    text=f"<b>{len(df):,}</b><br><span style='font-size:11px'>employees</span>",
                    x=0.5, y=0.5, font_size=18, showarrow=False, font_color="#000000",
                )
            ],
        )
        apply_plotly_defaults(donut)
        st.plotly_chart(donut, use_container_width=True, theme=None)

    with c2:
        bar = px.bar(
            dept_summary,
            y="Department",
            x="high_risk",
            orientation="h",
            title="High-risk headcount by department",
            text="high_risk",
            hover_data={"employees": True, "avg_risk": ":.2%", "high_risk_rate": ":.1%"},
        )
        bar.update_traces(
            marker_color=CORAL,
            marker_line_color="#7A746B",
            marker_line_width=0.5,
            textposition="outside",
            textfont_color="#000000",
        )
        bar.update_layout(
            yaxis=dict(autorange="reversed", title=None, automargin=True, tickfont=dict(size=11)),
            xaxis=dict(title="High-risk employees", automargin=True),
            margin=dict(l=180, r=40, t=60, b=50),
        )
        apply_plotly_defaults(bar)
        st.plotly_chart(bar, use_container_width=True, theme=None)

    # ── Row 2 ── Stacked dept-by-risk + Tenure scatter ───────────────────
    dept_risk = (
        df.groupby(["Department", "Risk_Level"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["High Risk", "Medium Risk", "Low Risk"], fill_value=0)
        .reset_index()
    )
    stacked = go.Figure()
    for level in ["High Risk", "Medium Risk", "Low Risk"]:
        stacked.add_trace(
            go.Bar(
                name=level,
                x=dept_risk["Department"],
                y=dept_risk[level],
                marker_color=RISK_COLOR_MAP[level],
                hovertemplate=f"<b>%{{x}}</b><br>{level}: %{{y}}<extra></extra>",
            )
        )
    stacked.update_layout(
        barmode="stack",
        title="Risk composition by department",
        xaxis_title="",
        yaxis_title="Employees",
    )
    apply_plotly_defaults(stacked)

    scatter = px.scatter(
        df,
        x="Tenure_Months",
        y="Flight_Risk_Probability",
        color="Risk_Level",
        color_discrete_map=RISK_COLOR_MAP,
        opacity=0.55,
        size_max=9,
        title="Tenure vs. flight-risk probability",
        hover_data={"Department": True, "Base_Salary": ":,.0f"},
    )
    scatter.update_traces(marker=dict(size=7, line=dict(width=0.5, color="#FBF7F2")))
    apply_plotly_defaults(scatter)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(stacked, use_container_width=True, theme=None)
    with c4:
        st.plotly_chart(scatter, use_container_width=True, theme=None)

    # ── Row 3 ── Risk histogram + Salary box ─────────────────────────────
    hist = px.histogram(
        df,
        x="Flight_Risk_Probability",
        nbins=30,
        color="Risk_Level",
        color_discrete_map=RISK_COLOR_MAP,
        title="Distribution of flight-risk probability",
    )
    hist.add_vline(x=0.50, line_dash="dash", line_color="#7A746B",
                   annotation_text="Medium gate", annotation_font_color="#000000")
    hist.add_vline(x=0.75, line_dash="dash", line_color="#7A746B",
                   annotation_text="High gate", annotation_font_color="#000000")
    apply_plotly_defaults(hist)

    box = px.box(
        df,
        x="Risk_Level",
        y="Base_Salary",
        color="Risk_Level",
        color_discrete_map=RISK_COLOR_MAP,
        title="Salary distribution by risk band",
        category_orders={"Risk_Level": ["High Risk", "Medium Risk", "Low Risk"]},
        points=False,
    )
    apply_plotly_defaults(box)

    c5, c6 = st.columns(2)
    with c5:
        st.plotly_chart(hist, use_container_width=True, theme=None)
    with c6:
        st.plotly_chart(box, use_container_width=True, theme=None)

    # ── Row 4 ── Cox 12-month survival overlay ──────────────────────────
    if "Cox_12_Month_Survival_Probability" in df.columns:
        cox_summary = (
            df.groupby("Department", as_index=False)
            .agg(
                mean_survival=("Cox_12_Month_Survival_Probability", "mean"),
                median_survival=("Cox_12_Month_Survival_Probability", "median"),
                p25=("Cox_12_Month_Survival_Probability", lambda s: s.quantile(0.25)),
                p75=("Cox_12_Month_Survival_Probability", lambda s: s.quantile(0.75)),
            )
            .sort_values("mean_survival", ascending=True)
        )
        cox = go.Figure()
        # P25-P75 IQR band
        cox.add_trace(go.Bar(
            y=cox_summary["Department"],
            x=cox_summary["p75"] - cox_summary["p25"],
            base=cox_summary["p25"],
            orientation="h",
            marker=dict(color=LAVENDER, line=dict(color="#7A746B", width=0.5)),
            name="P25 – P75 (IQR)",
            hovertemplate="<b>%{y}</b><br>P25: %{base:.0%}<br>P75: %{x:.0%} above base<extra></extra>",
        ))
        # Mean dot
        cox.add_trace(go.Scatter(
            y=cox_summary["Department"],
            x=cox_summary["mean_survival"],
            mode="markers+text",
            marker=dict(color=CORAL, size=14, line=dict(color="#1F1E1B", width=1.2)),
            text=[f"{v:.0%}" for v in cox_summary["mean_survival"]],
            textposition="middle right",
            textfont=dict(color="#000000", size=11),
            name="Mean retention",
            hovertemplate="<b>%{y}</b><br>Mean: %{x:.1%}<extra></extra>",
        ))
        cox.update_layout(
            title="12-month expected retention by department (Cox model) — IQR band + mean",
            xaxis=dict(tickformat=".0%", range=[0, 1.05], title="P(retained at 12 months)"),
            yaxis=dict(title=""),
            barmode="overlay",
        )
        apply_plotly_defaults(cox)
        st.plotly_chart(cox, use_container_width=True, theme=None)

    # ── Department leaderboard table ────────────────────────────────────
    st.markdown("#### Department leaderboard")
    leaderboard = dept_summary.copy()
    leaderboard["avg_risk"] = leaderboard["avg_risk"].round(3)
    leaderboard["avg_salary"] = leaderboard["avg_salary"].round(0)
    leaderboard["avg_tenure"] = leaderboard["avg_tenure"].round(1)
    leaderboard["high_risk_rate_%"] = (leaderboard["high_risk_rate"] * 100).round(1)
    leaderboard = leaderboard[
        ["Department", "employees", "high_risk", "high_risk_rate_%",
         "avg_risk", "avg_salary", "avg_tenure"]
    ]

    from matplotlib.colors import LinearSegmentedColormap
    cmap_coral = LinearSegmentedColormap.from_list("coral_pastel",
        ["#FBF7F2", "#F5E1A0", "#F5C4A0", "#F2A8A0"])
    cmap_sage = LinearSegmentedColormap.from_list("sage_pastel",
        ["#FBF7F2", "#E1ECCE", "#B5D4A8"])
    cmap_lav = LinearSegmentedColormap.from_list("lav_pastel",
        ["#FBF7F2", "#D9D5EB", "#B8B5E1"])

    styled = (
        leaderboard.style
        .set_properties(**{
            "background-color": "#FBF7F2",
            "color": "#1F1E1B",
            "font-weight": "600",
            "border": "1px solid #E7DECF",
        })
        .background_gradient(subset=["high_risk"], cmap=cmap_coral)
        .background_gradient(subset=["high_risk_rate_%"], cmap=cmap_coral)
        .background_gradient(subset=["avg_risk"], cmap=cmap_coral)
        .background_gradient(subset=["avg_salary"], cmap=cmap_sage)
        .background_gradient(subset=["avg_tenure"], cmap=cmap_lav)
        .background_gradient(subset=["employees"], cmap=cmap_lav)
        .format({
            "avg_risk": "{:.3f}",
            "avg_salary": "${:,.0f}",
            "avg_tenure": "{:.1f} mo",
            "high_risk_rate_%": "{:.1f}%",
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
    show_styled(st, styled)


def _shap_tab(df: pd.DataFrame) -> None:
    st.subheader("SHAP Insights")
    feature_table = load_optional(SHAP_FEATURE_TABLE_NAME)
    if feature_table.empty:
        st.info("No SHAP feature impact table. Re-run training.")
        return

    feature_table = feature_table.sort_values("Mean_ABS_SHAP", ascending=False)
    fig = px.bar(
        feature_table,
        x="Mean_ABS_SHAP",
        y="Feature",
        orientation="h",
        title="Global model drivers (mean |SHAP|)",
        text="Mean_ABS_SHAP",
    )
    fig.update_traces(
        marker_color=LAVENDER,
        marker_line_color="#7A746B",
        marker_line_width=0.5,
        texttemplate="%{text:.3f}",
        textposition="outside",
        textfont_color="#000000",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    apply_plotly_defaults(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    # ---- Per-employee primary driver mix ----
    if "Primary_Risk_Driver" in df.columns:
        driver_counts = (
            df.groupby(["Primary_Risk_Driver", "Risk_Level"])
            .size()
            .reset_index(name="Count")
        )
        driver_fig = px.bar(
            driver_counts,
            x="Primary_Risk_Driver",
            y="Count",
            color="Risk_Level",
            color_discrete_map=RISK_COLOR_MAP,
            barmode="stack",
            title="Primary risk driver across the workforce",
        )
        apply_plotly_defaults(driver_fig)
        st.plotly_chart(driver_fig, use_container_width=True, theme=None)

    # ---- Mean SHAP by department (which departments are pushed by what?) ----
    shap_cols = [c for c in df.columns if c.startswith("SHAP_") and c.endswith("_Impact")]
    if shap_cols:
        dept_shap = df.groupby("Department")[shap_cols].mean().round(3)
        dept_shap.columns = [c.replace("SHAP_", "").replace("_Impact", "")
                             for c in dept_shap.columns]
        heat = px.imshow(
            dept_shap.values,
            labels=dict(x="Driver", y="Department"),
            x=list(dept_shap.columns),
            y=list(dept_shap.index),
            color_continuous_scale=SEQUENTIAL,
            aspect="auto",
            title="Average SHAP contribution by department × driver",
        )
        heat.update_traces(showscale=False)
        heat.update_coloraxes(showscale=False)
        heat.update_layout(coloraxis_showscale=False)
        apply_plotly_defaults(heat)
        st.plotly_chart(heat, use_container_width=True, theme=None)

    st.markdown("#### Feature impact table")
    from matplotlib.colors import LinearSegmentedColormap as _LSC
    _cmap_shap = _LSC.from_list("shap_pastel",
        ["#FBF7F2", "#F5E1A0", "#F5C4A0", "#F2A8A0"])
    shap_styled = (
        feature_table.style
        .set_properties(**{
            "background-color": "#FBF7F2",
            "color": "#1F1E1B",
            "font-weight": "600",
            "border": "1px solid #E7DECF",
        })
        .background_gradient(subset=["Mean_ABS_SHAP"], cmap=_cmap_shap)
        .format({"Mean_ABS_SHAP": "{:.4f}"})
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
    show_styled(st, shap_styled)


def _compare_tab(df: pd.DataFrame) -> None:
    st.subheader("Compare Two Employees")
    render_comparison_panel(df)


def _causal_tab(df: pd.DataFrame) -> None:
    st.subheader("Causal Uplift \u2014 Recommended Interventions")
    uplift_table = load_optional(CAUSAL_UPLIFT_TABLE)
    if uplift_table.empty:
        st.info(
            "No uplift table found. Run "
            "`python -m attrisense.causal_uplift` from the repo root."
        )
        if st.button("Compute now", key="run_uplift"):
            with st.spinner("Training T-learner and scoring interventions..."):
                from attrisense.causal_uplift import compute_uplift_table

                uplift_table = compute_uplift_table()
                st.success(f"Persisted {len(uplift_table):,} uplift rows.")
                st.cache_data.clear()
                st.rerun()
        return

    cols = st.columns(3)
    cols[0].metric("Employees scored", f"{len(uplift_table):,}")
    cols[1].metric(
        "Avg risk reduction",
        f"{uplift_table['Best_Risk_Reduction'].mean():+.3f}",
    )
    cols[2].metric(
        "Top intervention",
        uplift_table["Best_Intervention"].mode().iloc[0],
    )

    fig = px.histogram(
        uplift_table,
        x="Best_Intervention",
        color="Risk_Level",
        barmode="group",
        title="Best-recommended intervention by risk band",
        color_discrete_map=RISK_COLOR_MAP,
    )
    apply_plotly_defaults(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)
    show_styled(st, pastel_table(
            _pseudonymize(uplift_table.head(50)),
            gradient_cols=["Best_Risk_Reduction"],
            cmap_name="sage",
            fmt={"Best_Risk_Reduction": "{:+.3f}"},
        ))


def _fairness_tab(df: pd.DataFrame) -> None:
    st.subheader("Fairness Audit")
    report = load_fairness_report()
    col_run, _ = st.columns([1, 4])
    with col_run:
        if st.button("Re-run audit", key="run_fairness"):
            run_audit(("Department",))
            st.cache_data.clear()
            st.success("Fairness report regenerated.")
            report = load_fairness_report()

    if not report:
        st.info("No fairness report found. Click `Re-run audit` to generate one.")
        return

    for dimension, payload in report.items():
        st.markdown(f"#### Dimension: `{dimension}`")
        st.metric(
            "Disparate-impact ratio",
            f"{payload['disparate_impact_ratio']:.3f}",
            "Pass" if payload["passes_four_fifths_rule"] else "Fail",
            delta_color="normal" if payload["passes_four_fifths_rule"] else "inverse",
        )
        show_styled(st, pastel_table(pd.DataFrame(payload["groups"])))
        for note in payload["notes"]:
            st.warning(note)


def _render_sql_result(payload: dict) -> None:
    """Render a SQL execution result dict as a Streamlit dataframe."""
    columns = payload.get("columns") or []
    rows = payload.get("rows") or []
    if not rows:
        st.info("Query returned 0 rows.")
        return
    frame = pd.DataFrame(rows, columns=columns or None)
    show_styled(st, pastel_table(_pseudonymize(frame)))


def _ai_assistant_tab(df: pd.DataFrame) -> None:
    st.subheader("AI Assistant \u2014 Ask in plain English")
    st.caption(
        "Powered by LangChain + GPT-3.5. Read-only SQL guardrails enforced. "
        "If the model cannot produce a valid query, the assistant falls "
        "back to the closest matches from a 50-question gold set."
    )

    question = st.text_input(
        "Question",
        value="How many high risk employees are in Manufacturing?",
        key="ai_question",
    )
    ask_button = st.button("Ask", key="ai_ask", type="primary")

    if ask_button and question.strip():
        sql, result = (None, "OPENAI_API_KEY is not set.")
        if os.getenv("OPENAI_API_KEY"):
            try:
                from natural_language_sql import query_database_with_ai

                with st.spinner("Generating SQL..."):
                    sql, result = query_database_with_ai(question)
            except Exception as error:  # noqa: BLE001 - surface in fallback
                sql, result = None, f"Agent error: {error}"

        if sql and isinstance(result, dict):
            st.markdown("**Generated SQL**")
            st.code(sql, language="sql")
            _render_sql_result(result)
            return

        reason = result if isinstance(result, str) else "agent returned no SQL"
        st.warning(f"Could not generate a query \u2014 {reason}")
        st.markdown("**Closest gold-set questions** (click to run a known-good query):")
        suggestions = suggest(question, top_k=3)
        if not suggestions:
            st.info(
                "No similar gold questions found. Try rephrasing using the "
                "examples in the sidebar."
            )
            return
        for index, suggestion in enumerate(suggestions):
            with st.container(border=True):
                st.markdown(
                    f"**{suggestion.question}**  \n"
                    f"Category `{suggestion.category}` \u00b7 similarity {suggestion.score:.2f}"
                )
                if st.button("Run this gold query", key=f"sugg_run_{index}"):
                    payload = execute_gold_sql(suggestion.expected_sql)
                    st.code(suggestion.expected_sql, language="sql")
                    _render_sql_result(payload)


def _eval_tab(df: pd.DataFrame) -> None:
    st.subheader("NL\u2192SQL Evaluation Harness")
    report = load_eval_report()
    col_run, _ = st.columns([1, 4])
    with col_run:
        if st.button("Run evaluation", key="run_eval"):
            with st.spinner("Running 50 gold questions..."):
                run_evaluation()
            report = load_eval_report()
            st.cache_data.clear()
            st.success("Evaluation complete.")

    if not report:
        st.info(
            "No evaluation report found. Set `OPENAI_API_KEY` in `.env` "
            "then click `Run evaluation`."
        )
        return

    if report.get("note"):
        st.warning(report["note"])

    cols = st.columns(3)
    cols[0].metric("Total questions", report["total"])
    cols[1].metric("Exact accuracy", f"{report['exact_accuracy'] * 100:.1f}%")
    cols[2].metric("Cardinality accuracy", f"{report['cardinality_accuracy'] * 100:.1f}%")

    if report["accuracy_by_category"]:
        category_frame = pd.DataFrame(report["accuracy_by_category"]).T.reset_index()
        category_frame.columns = ["category", "count", "exact_accuracy", "cardinality_accuracy"]
        fig = px.bar(
            category_frame,
            x="category",
            y="exact_accuracy",
            title="Exact-match accuracy by question category",
        )
        fig.update_traces(
            marker_color=LAVENDER,
            marker_line_color="#7A746B",
            marker_line_width=0.5,
        )
        fig.update_layout(yaxis_tickformat=".0%")
        apply_plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

    if report["cases"]:
        cases_df = pd.DataFrame(report["cases"])[
            [
                "id",
                "category",
                "question",
                "exact_match",
                "cardinality_match",
                "expected_rowcount",
                "generated_rowcount",
                "duration_seconds",
                "error",
            ]
        ]
        show_styled(st, pastel_table(
                cases_df,
                gradient_cols=["duration_seconds"],
                cmap_name="lavender",
                fmt={"duration_seconds": "{:.2f}s"},
            ))


def _multilingual_tab(df: pd.DataFrame) -> None:
    st.subheader("Multilingual Exit-Interview RAG")
    st.caption(
        "Search synthetic exit-interview text in English, Spanish, and Hindi. "
        "When `OPENAI_API_KEY` is unset, a deterministic hashing fallback is used."
    )
    query = st.text_input("Search query (any language)", value="compensation issues", key="rag_query")
    if st.button("Search", key="rag_search"):
        from attrisense.multilingual_rag import search

        with st.spinner("Embedding and searching..."):
            results = search(query, top_k=6)
        if not results:
            st.warning("No results returned.")
            return
        show_styled(st, pastel_table(pd.DataFrame(results)))


def _alert_tab(df: pd.DataFrame) -> None:
    render_alert_mock(df)


def _ethics_tab(df: pd.DataFrame) -> None:
    st.subheader("Limitations & Ethics")
    st.markdown(
        """
- Predictions are **correlational, not causal** \u2014 except for the
  Causal Uplift tab, which uses an EconML T-learner with explicit
  treatment definitions.
- All employee data is **synthetic**. Re-train on governed HR data
  before any production use.
- AttriSense is **not approved for adverse employment decisions**
  (termination, comp denial, promotion denial).
- For NYC LL144 covered uses, run an independent bias audit before
  deployment and publish the audit summary.
- Model behaviour is monitored through the Fairness Audit tab and the
  NL\u2192SQL Evaluation Harness.
"""
    )
    st.markdown("[Read the full Model Card](MODEL_CARD.md)")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _sidebar() -> None:
    """Persistent left navigation."""
    with st.sidebar:
        st.markdown("### AttriSense")
        st.caption("Workforce Intelligence")
        st.markdown("---")
        if st.button("Show onboarding tour", key="sidebar_tour", use_container_width=True):
            reset_onboarding_tour()
        st.markdown("---")
        st.caption("**Try the AI Assistant with:**")
        st.code("How many high risk employees are in Manufacturing?", language="text")
        st.code("Top 10 highest-risk employees", language="text")
        st.code("Average salary by department", language="text")
        st.markdown("---")
        st.caption("Pipeline: `make -C production train uplift fairness eval`")


def main() -> None:
    """Streamlit entry point."""
    st.markdown(
        render_brand_header(
            title="AttriSense",
            tagline="Workforce intelligence \u2014 prediction, explanation, intervention.",
        ),
        unsafe_allow_html=True,
    )
    st.markdown(
        render_disclosure(
            "Synthetic-data demonstration. Not approved for real employment "
            "decisions. See the Limitations &amp; Ethics tab and the model card."
        ),
        unsafe_allow_html=True,
    )

    _sidebar()

    df = load_predictions()
    if df.empty:
        st.error(
            "No predictions found. Run "
            "`python train_retention_risk_model.py` first."
        )
        return

    render_onboarding_tour()

    tabs = st.tabs(
        [
            "Executive",
            "Detailed Analytics",
            "Decision Tools",
            "SHAP Insights",
            "Compare",
            "Survival & Calibration",
            "Causal Uplift",
            "Fairness",
            "AI Assistant",
            "NL\u2192SQL Eval",
            "Multilingual RAG",
            "Alert Mock",
            "Ethics",
        ]
    )
    with tabs[0]:
        _executive_tab(df)
    with tabs[1]:
        render_detailed_analytics(df)
    with tabs[2]:
        render_decision_tools(df)
    with tabs[3]:
        _shap_tab(df)
    with tabs[4]:
        _compare_tab(df)
    with tabs[5]:
        render_survival_and_calibration(df)
    with tabs[6]:
        _causal_tab(df)
    with tabs[7]:
        _fairness_tab(df)
    with tabs[8]:
        _ai_assistant_tab(df)
    with tabs[9]:
        _eval_tab(df)
    with tabs[10]:
        _multilingual_tab(df)
    with tabs[11]:
        _alert_tab(df)
    with tabs[12]:
        _ethics_tab(df)


if __name__ == "__main__":
    main()
