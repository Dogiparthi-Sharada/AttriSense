# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/legacy_tabs.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Legacy-feature ports: Detailed Analytics, Decision Tools, Survival & Calibration.

Adapted from `archive/legacy/streamlit_app.py` to use the pastel theme,
the pseudonymous ``Review_ID`` (no raw Emp_ID anywhere), and centralised
``apply_plotly_defaults`` + ``pastel_table`` helpers.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from attrisense.identity import to_review_id
from attrisense.theme import (
    CORAL,
    LAVENDER,
    PEACH,
    RISK_COLOR_MAP,
    SAGE,
    apply_plotly_defaults,
    pastel_table,
    show_styled,
)

# Lazy import of project-level config (top-level package, not under attrisense)
import importlib
_CFG = importlib.import_module("config")
DEPARTMENT_CODE_MAP: dict[str, int] = _CFG.DEPARTMENT_CODE_MAP
MODEL_ARTIFACT_PATH: Path = _CFG.MODEL_ARTIFACT_PATH
SURVIVAL_CURVE_TABLE_NAME: str = _CFG.SURVIVAL_CURVE_TABLE_NAME
CALIBRATION_TABLE_NAME: str = _CFG.CALIBRATION_TABLE_NAME
DATABASE_PATH: Path = _CFG.DATABASE_PATH


# --------------------------------------------------------------------------- helpers


@st.cache_resource
def _load_model_artifact() -> dict[str, Any] | None:
    if not Path(MODEL_ARTIFACT_PATH).exists():
        return None
    return joblib.load(MODEL_ARTIFACT_PATH)


def _format_currency(value: float) -> str:
    return f"${value:,.0f}"


def _categorize_risk(probability: float) -> str:
    if probability > 0.75:
        return "High Risk"
    if probability > 0.40:
        return "Medium Risk"
    return "Low Risk"


def _score_scenario(
    artifact: dict[str, Any],
    employee: pd.Series,
    salary_delta_pct: int,
    tenure_extra_months: int,
    manager_change: bool,
) -> float:
    feature_columns = artifact["feature_columns"]
    model = artifact["model"]
    modified = employee.copy()
    modified["Base_Salary"] = modified["Base_Salary"] * (1 + salary_delta_pct / 100)
    modified["Tenure_Months"] = modified["Tenure_Months"] + tenure_extra_months
    if manager_change:
        modified["Manager_Tenure_Months"] = 0
    else:
        modified["Manager_Tenure_Months"] = (
            modified["Manager_Tenure_Months"] + tenure_extra_months
        )
    modified["Dept_Code"] = DEPARTMENT_CODE_MAP[modified["Department"]]
    scenario_frame = pd.DataFrame(
        [{column: modified[column] for column in feature_columns}]
    )
    return float(model.predict_proba(scenario_frame)[0][1])


def _load_optional(table: str) -> pd.DataFrame:
    if not Path(DATABASE_PATH).exists():
        return pd.DataFrame()
    with sqlite3.connect(DATABASE_PATH) as connection:
        exists = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,),
        ).fetchone()
        if not exists:
            return pd.DataFrame()
        return pd.read_sql_query(f"SELECT * FROM {table}", connection)


# --------------------------------------------------------------------------- detailed analytics


def render_detailed_analytics(df: pd.DataFrame) -> None:
    st.subheader("Detailed Analytics")
    analysis_type = st.selectbox(
        "Select analysis",
        ["High-risk employees", "Tenure analysis", "Salary analysis", "Department comparison"],
        key="detailed_kind",
    )

    if analysis_type == "High-risk employees":
        high_risk_df = df[df["Risk_Level"] == "High Risk"].copy()
        high_risk_df = high_risk_df.sort_values("Flight_Risk_Probability", ascending=False)
        c1, c2, c3 = st.columns(3)
        c1.metric("High-risk count", f"{len(high_risk_df):,}")
        c2.metric("Avg risk probability",
                  f"{high_risk_df['Flight_Risk_Probability'].mean():.2%}")
        c3.metric("Avg tenure", f"{high_risk_df['Tenure_Months'].mean():.1f} mo")

        fig = px.histogram(
            high_risk_df,
            x="Flight_Risk_Probability",
            nbins=20,
            title="Distribution of flight-risk probability (high-risk only)",
        )
        fig.update_traces(marker_color=CORAL, marker_line_color="#7A746B",
                          marker_line_width=0.5)
        apply_plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)

        st.markdown("##### Recommended retention plays")
        st.markdown(
            "- **>0.90** — Critical: retention conversation, comp review, role redesign\n"
            "- **0.80 – 0.90** — High: retention bonus, dev plan, mentorship\n"
            "- **0.75 – 0.80** — Medium: regular 1:1s, skill development"
        )

        display_df = high_risk_df[
            ["Emp_ID", "Department", "Tenure_Months", "Base_Salary",
             "Flight_Risk_Probability", "Risk_Level"]
        ].head(20).copy()
        display_df.insert(0, "Review_ID", display_df["Emp_ID"].map(to_review_id))
        display_df = display_df.drop(columns=["Emp_ID"])
        show_styled(st, pastel_table(
                display_df,
                gradient_cols=["Flight_Risk_Probability"],
                cmap_name="coral",
                fmt={
                    "Flight_Risk_Probability": "{:.2%}",
                    "Base_Salary": "${:,.0f}",
                    "Tenure_Months": "{:.1f}",
                },
            ))

    elif analysis_type == "Tenure analysis":
        fig = px.scatter(
            df,
            x="Tenure_Months",
            y="Flight_Risk_Probability",
            color="Risk_Level",
            size="Base_Salary",
            color_discrete_map=RISK_COLOR_MAP,
            hover_data=["Department"],
            title="Tenure vs flight-risk (size = salary)",
            opacity=0.6,
        )
        apply_plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg tenure", f"{df['Tenure_Months'].mean():.1f} mo")
        c2.metric("Median tenure", f"{df['Tenure_Months'].median():.1f} mo")
        c3.metric("Employees < 6 mo", f"{int((df['Tenure_Months'] < 6).sum()):,}")

    elif analysis_type == "Salary analysis":
        fig = px.box(
            df,
            x="Department",
            y="Base_Salary",
            color="Risk_Level",
            color_discrete_map=RISK_COLOR_MAP,
            title="Salary distribution by department × risk",
            points=False,
        )
        apply_plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg salary", _format_currency(df["Base_Salary"].mean()))
        c2.metric("Median salary", _format_currency(df["Base_Salary"].median()))
        c3.metric("Salary range",
                  _format_currency(df["Base_Salary"].max() - df["Base_Salary"].min()))

    else:  # Department comparison
        dept_stats = (
            df.groupby("Department", as_index=False)
            .agg(
                employees=("Emp_ID", "count"),
                avg_risk=("Flight_Risk_Probability", "mean"),
                avg_salary=("Base_Salary", "mean"),
                avg_tenure=("Tenure_Months", "mean"),
            )
            .sort_values("avg_risk", ascending=False)
        )
        show_styled(st, pastel_table(
                dept_stats,
                gradient_cols=["avg_risk", "employees"],
                cmap_name="coral",
                fmt={
                    "avg_risk": "{:.2%}",
                    "avg_salary": "${:,.0f}",
                    "avg_tenure": "{:.1f} mo",
                },
            ))

        fig = px.bar(
            dept_stats,
            x="Department",
            y="avg_risk",
            title="Average flight-risk by department",
            text="avg_risk",
        )
        fig.update_traces(
            marker_color=PEACH,
            marker_line_color="#7A746B",
            marker_line_width=0.5,
            texttemplate="%{text:.1%}",
            textposition="outside",
            textfont_color="#000000",
        )
        fig.update_layout(yaxis_tickformat=".0%")
        apply_plotly_defaults(fig)
        st.plotly_chart(fig, use_container_width=True, theme=None)


# --------------------------------------------------------------------------- decision tools


def _what_if_simulator(df: pd.DataFrame) -> None:
    st.markdown("#### What-if simulator")
    artifact = _load_model_artifact()
    if artifact is None:
        st.warning(
            "Model artifact missing. Run `python train_retention_risk_model.py` first."
        )
        return
    employee_options = df.sort_values("Flight_Risk_Probability", ascending=False).head(300)
    labels = employee_options.apply(
        lambda row: (
            f"{to_review_id(int(row['Emp_ID']))} | {row['Department']} | "
            f"{row['Flight_Risk_Probability']:.1%} current"
        ),
        axis=1,
    )
    selected = st.selectbox("Employee scenario", labels, key="whatif_sel")
    review_id = selected.split(" | ")[0]
    # map back to Emp_ID
    employee_options["_rid"] = employee_options["Emp_ID"].map(
        lambda v: to_review_id(int(v))
    )
    employee = employee_options[employee_options["_rid"] == review_id].iloc[0]

    c1, c2, c3 = st.columns(3)
    salary_delta = c1.slider(
        "Salary raise (%)", 0, 30, 0,
        help="Model retention levers only — pay cuts don't reduce flight risk.",
    )
    tenure_extra = c2.slider("Tenure extension (months)", 0, 24, 0)
    manager_change = c3.checkbox("Manager change")

    new_p = _score_scenario(artifact, employee, salary_delta, tenure_extra, manager_change)
    cur_p = float(employee["Flight_Risk_Probability"])
    delta = new_p - cur_p

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Current risk", f"{cur_p:.1%}", employee["Risk_Level"])
    k2.metric("Scenario risk", f"{new_p:.1%}", f"{delta:+.1%}",
              delta_color="inverse")
    k3.metric("Scenario band", _categorize_risk(new_p))
    k4.metric("Manager tenure", f"{employee['Manager_Tenure_Months']:.0f} mo")

    if delta < -0.05:
        st.success("Scenario materially **reduces** flight risk in the model.")
    elif delta > 0.05:
        st.warning("Scenario **increases** flight risk — needs a stronger lever.")
    else:
        st.info("Scenario has a modest effect. Try combining salary + tenure levers.")


def _manager_rollup(df: pd.DataFrame) -> None:
    st.markdown("#### Manager-level risk rollup")
    rollup = (
        df.groupby(["Manager_ID", "Department"], as_index=False)
        .agg(
            Total_Reports=("Emp_ID", "count"),
            High_Risk_Reports=("Risk_Level",
                               lambda v: int((v == "High Risk").sum())),
            Avg_Risk_Probability=("Flight_Risk_Probability", "mean"),
            Avg_Manager_Tenure_Months=("Manager_Tenure_Months", "mean"),
            Salary_Exposure=("Base_Salary", "sum"),
        )
    )
    rollup["High_Risk_Rate"] = rollup["High_Risk_Reports"] / rollup["Total_Reports"]
    rollup["Weighted_Risk_Exposure"] = (
        rollup["Salary_Exposure"] * rollup["Avg_Risk_Probability"]
    )
    rollup = rollup.sort_values(
        ["High_Risk_Rate", "Avg_Risk_Probability"], ascending=False
    )
    rollup["Manager_RID"] = rollup["Manager_ID"].map(
        lambda v: f"MGR-{int(v):05d}"
    )

    top = rollup.head(15).copy()
    fig = px.bar(
        top.sort_values("High_Risk_Rate"),
        x="High_Risk_Rate",
        y="Manager_RID",
        orientation="h",
        color="Department",
        text="High_Risk_Reports",
        title="Managers with highest high-risk concentration",
        labels={"High_Risk_Rate": "% high risk", "Manager_RID": "Manager"},
    )
    fig.update_traces(texttemplate="%{text} high-risk", textposition="outside",
                      textfont_color="#000000")
    fig.update_layout(xaxis_tickformat=".0%", height=520)
    apply_plotly_defaults(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    table_df = rollup[
        ["Manager_RID", "Department", "Total_Reports", "High_Risk_Reports",
         "High_Risk_Rate", "Avg_Risk_Probability", "Avg_Manager_Tenure_Months",
         "Weighted_Risk_Exposure"]
    ].head(25)
    show_styled(st, pastel_table(
            table_df,
            gradient_cols=["High_Risk_Rate", "Weighted_Risk_Exposure"],
            cmap_name="coral",
            fmt={
                "High_Risk_Rate": "{:.1%}",
                "Avg_Risk_Probability": "{:.1%}",
                "Avg_Manager_Tenure_Months": "{:.1f}",
                "Weighted_Risk_Exposure": "${:,.0f}",
            },
        ))


def _cost_calculator(df: pd.DataFrame) -> None:
    st.markdown("#### Cost-of-attrition calculator")
    multiplier = st.slider("Replacement cost multiplier", 0.5, 3.0, 1.5, 0.1,
                           key="cost_mult")
    high_risk = df[df["Risk_Level"] == "High Risk"]
    annual_loss = len(high_risk) * df["Base_Salary"].mean() * multiplier
    pwl = (
        high_risk["Base_Salary"]
        * high_risk["Flight_Risk_Probability"]
        * multiplier
    ).sum()
    quarterly = annual_loss / 4

    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted preventable loss (quarter)", _format_currency(quarterly))
    c2.metric("Annualised high-risk exposure", _format_currency(annual_loss))
    c3.metric("Probability-weighted exposure", _format_currency(pwl))
    st.info(
        "CFO translation: turns the model into a budget conversation. "
        "Default replacement cost = 1.5× salary."
    )


def render_decision_tools(df: pd.DataFrame) -> None:
    st.subheader("Decision Tools")
    st.caption("Tier 1 features that move predictions into action.")
    sub_tabs = st.tabs(["What-if simulator", "Manager rollup", "Cost calculator"])
    with sub_tabs[0]:
        _what_if_simulator(df)
    with sub_tabs[1]:
        _manager_rollup(df)
    with sub_tabs[2]:
        _cost_calculator(df)


# --------------------------------------------------------------------------- survival & calibration


def render_survival_and_calibration(df: pd.DataFrame) -> None:
    st.subheader("Survival & Calibration")
    st.caption("Tier 2 model-risk views for time-to-event decisions and probability QA.")

    survival_curves = _load_optional(SURVIVAL_CURVE_TABLE_NAME)
    calibration_table = _load_optional(CALIBRATION_TABLE_NAME)
    if survival_curves.empty or calibration_table.empty:
        st.warning(
            "Survival or calibration outputs are missing. "
            "Run `python train_retention_risk_model.py`."
        )
        return

    high_risk = df[df["Risk_Level"] == "High Risk"]
    c1, c2, c3 = st.columns(3)
    c1.metric(
        "High-risk median expected tenure",
        f"{high_risk['Cox_Median_Expected_Tenure_Months'].median():.1f} mo",
    )
    c2.metric(
        "High-risk 12-month survival",
        f"{high_risk['Cox_12_Month_Survival_Probability'].mean():.1%}",
    )
    c3.metric(
        "Calibration Brier score",
        f"{calibration_table['Brier_Score'].iloc[0]:.3f}",
    )

    survival_fig = px.line(
        survival_curves,
        x="Month",
        y="Survival_Probability",
        color="Risk_Level",
        color_discrete_map=RISK_COLOR_MAP,
        markers=True,
        title="Cox survival curves by risk cohort",
        labels={"Survival_Probability": "P(still employed)"},
    )
    survival_fig.update_layout(yaxis_tickformat=".0%", height=460)
    apply_plotly_defaults(survival_fig)
    st.plotly_chart(survival_fig, use_container_width=True, theme=None)

    calib_fig = go.Figure()
    calib_fig.add_trace(
        go.Scatter(
            x=calibration_table["Mean_Predicted_Probability"],
            y=calibration_table["Observed_Turnover_Rate"],
            mode="lines+markers",
            name="Model calibration",
            line=dict(color=CORAL, width=3),
            marker=dict(color=CORAL, size=10, line=dict(color="#1F1E1B", width=1)),
        )
    )
    calib_fig.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Perfect calibration",
            line=dict(dash="dash", color="#7A746B"),
        )
    )
    calib_fig.update_layout(
        title="Calibration plot — predicted vs observed turnover",
        xaxis_title="Mean predicted probability",
        yaxis_title="Observed turnover rate",
        xaxis_tickformat=".0%",
        yaxis_tickformat=".0%",
        height=460,
    )
    apply_plotly_defaults(calib_fig)
    st.plotly_chart(calib_fig, use_container_width=True, theme=None)

    show_styled(st, pastel_table(
            calibration_table,
            gradient_cols=["Brier_Score"],
            cmap_name="coral",
            fmt={
                "Mean_Predicted_Probability": "{:.1%}",
                "Observed_Turnover_Rate": "{:.1%}",
                "Brier_Score": "{:.3f}",
                "Holdout_Employee_Count": "{:,.0f}",
            },
        ))
