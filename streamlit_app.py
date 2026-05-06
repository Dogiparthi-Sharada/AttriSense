"""Streamlit application for AttriSense workforce intelligence."""

from __future__ import annotations

import sqlite3

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from natural_language_sql import query_database_with_ai
from config import DATABASE_PATH, SQL_TABLE_NAME


RISK_COLORS = {
    "High Risk": "#d64550",
    "Medium Risk": "#f0a202",
    "Low Risk": "#1f9d75",
}


st.set_page_config(
    page_title="AttriSense",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)


st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem;}
        .hero-title {font-size: 2.4rem; font-weight: 750; color: #14213d;}
        .hero-subtitle {font-size: 1.05rem; color: #4b5563; margin-bottom: 1rem;}
        .section-note {color: #6b7280; font-size: 0.95rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=60)
def load_predictions() -> pd.DataFrame:
    """Load the prediction table that powers every dashboard view.

    Returns:
        A DataFrame containing employee records and model-generated risk scores.

    Raises:
        FileNotFoundError: If the SQLite database has not been created yet.
    """
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"{DATABASE_PATH.name} is missing. Run `python train_retention_risk_model.py` first."
        )

    with sqlite3.connect(DATABASE_PATH) as conn:
        return pd.read_sql_query(f"SELECT * FROM {SQL_TABLE_NAME}", conn)


def format_currency(value: float) -> str:
    """Format a numeric salary value as a whole-dollar string."""
    return f"${value:,.0f}"


def render_header() -> None:
    """Render the app title and one-line product positioning."""
    st.markdown('<div class="hero-title">AttriSense</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Predictive workforce intelligence for retention, risk, and executive action.</div>',
        unsafe_allow_html=True,
    )
    st.divider()


def render_kpis(df: pd.DataFrame) -> None:
    """Show the four executive metrics at the top of the dashboard.

    Args:
        df: Prediction DataFrame loaded from SQLite.
    """
    total = len(df)
    high_risk = int((df["Risk_Level"] == "High Risk").sum())
    medium_risk = int((df["Risk_Level"] == "Medium Risk").sum())
    low_risk = int((df["Risk_Level"] == "Low Risk").sum())

    col1, col2, col3, col4 = st.columns(4, gap="medium")
    col1.metric("Total workforce", f"{total:,}", "active employees")
    col2.metric("High flight risk", f"{high_risk:,}", f"{high_risk / total:.1%}")
    col3.metric("Medium risk", f"{medium_risk:,}", f"{medium_risk / total:.1%}")
    col4.metric("Low risk", f"{low_risk:,}", f"{low_risk / total:.1%}")


def render_executive_dashboard(df: pd.DataFrame) -> None:
    """Render the main executive view with KPIs, insights, and risk charts.

    Args:
        df: Prediction DataFrame loaded from SQLite.
    """
    st.subheader("Executive Dashboard")
    st.markdown(
        '<div class="section-note">A board-level view of workforce health, risk concentration, and intervention priorities.</div>',
        unsafe_allow_html=True,
    )
    render_kpis(df)
    st.divider()

    insight_col1, insight_col2, insight_col3 = st.columns(3, gap="medium")
    manufacturing = df[df["Department"] == "Manufacturing"]
    new_hire_high_risk = df[
        (df["Risk_Level"] == "High Risk") & (df["Tenure_Months"] < 6)
    ]

    insight_col1.info(
        f"Manufacturing tenure averages {manufacturing['Tenure_Months'].mean():.1f} months "
        f"across {len(manufacturing):,} employees."
    )
    insight_col2.info(
        f"Average base salary is {format_currency(df['Base_Salary'].mean())}, "
        "useful as a compensation benchmark."
    )
    insight_col3.warning(
        f"{len(new_hire_high_risk):,} early-tenure employees are already high risk."
    )

    chart_col1, chart_col2 = st.columns(2, gap="large")
    risk_counts = df["Risk_Level"].value_counts()

    with chart_col1:
        # A donut chart gives executives the risk mix at a glance.
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=risk_counts.index,
                    values=risk_counts.values,
                    hole=0.45,
                    marker={"colors": [RISK_COLORS.get(label, "#64748b") for label in risk_counts.index]},
                    textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>Employees: %{value}<extra></extra>",
                )
            ]
        )
        fig.update_layout(height=390, margin={"l": 0, "r": 0, "t": 20, "b": 0})
        st.plotly_chart(fig, width="stretch")

    with chart_col2:
        # Grouping only high-risk employees makes the operational hotspot clear.
        high_risk_by_dept = (
            df[df["Risk_Level"] == "High Risk"]
            .groupby("Department", as_index=False)
            .size()
            .rename(columns={"size": "High_Risk_Count"})
            .sort_values("High_Risk_Count", ascending=False)
        )
        fig = px.bar(
            high_risk_by_dept,
            x="Department",
            y="High_Risk_Count",
            color="Department",
            text="High_Risk_Count",
            title="High-risk employees by department",
        )
        fig.update_layout(height=390, showlegend=False, margin={"l": 0, "r": 0, "t": 45, "b": 0})
        st.plotly_chart(fig, width="stretch")

    st.subheader("Risk Profile by Department")
    risk_by_dept = pd.crosstab(df["Department"], df["Risk_Level"])
    # The stacked bar keeps each department in one visual row while showing all
    # risk bands. This is easier to compare than three separate charts.
    fig = go.Figure(
        data=[
            go.Bar(
                name=risk,
                x=risk_by_dept.index,
                y=risk_by_dept.get(risk, 0),
                marker_color=RISK_COLORS[risk],
            )
            for risk in ("High Risk", "Medium Risk", "Low Risk")
        ]
    )
    fig.update_layout(
        barmode="stack",
        xaxis_title="Department",
        yaxis_title="Employee count",
        height=420,
        hovermode="x unified",
    )
    st.plotly_chart(fig, width="stretch")


def render_deep_dive(df: pd.DataFrame) -> None:
    """Render analyst-friendly drilldowns for risk, tenure, salary, and teams.

    Args:
        df: Prediction DataFrame loaded from SQLite.
    """
    st.subheader("Detailed Analytics")
    analysis_type = st.selectbox(
        "Analysis view",
        ["High Risk Employees", "Tenure Analysis", "Salary Analysis", "Department Comparison"],
    )

    if analysis_type == "High Risk Employees":
        # Sort highest-probability employees first because they are the most
        # urgent candidates for retention action.
        high_risk_df = df[df["Risk_Level"] == "High Risk"].sort_values(
            "Flight_Risk_Probability", ascending=False
        )
        col1, col2, col3 = st.columns(3)
        col1.metric("High-risk employees", f"{len(high_risk_df):,}")
        col2.metric("Average risk probability", f"{high_risk_df['Flight_Risk_Probability'].mean():.1%}")
        col3.metric("Average tenure", f"{high_risk_df['Tenure_Months'].mean():.1f} months")

        fig = px.histogram(
            high_risk_df,
            x="Flight_Risk_Probability",
            nbins=20,
            title="Distribution of high-risk probabilities",
            labels={"Flight_Risk_Probability": "Risk probability"},
            color_discrete_sequence=[RISK_COLORS["High Risk"]],
        )
        st.plotly_chart(fig, width="stretch")

        st.markdown("#### Intervention guidance")
        st.table(
            pd.DataFrame(
                [
                    ("90%+", "Immediate retention interview, manager review, compensation check"),
                    ("80%-90%", "Career path discussion, mentorship, workload review"),
                    ("75%-80%", "Structured check-ins and engagement pulse follow-up"),
                ],
                columns=["Risk band", "Recommended action"],
            )
        )

        st.dataframe(
            high_risk_df[
                [
                    "Emp_ID",
                    "Department",
                    "Tenure_Months",
                    "Base_Salary",
                    "Flight_Risk_Probability",
                    "Risk_Level",
                ]
            ]
            .head(25)
            .style.format(
                {
                    "Flight_Risk_Probability": "{:.1%}",
                    "Base_Salary": "${:,.0f}",
                    "Tenure_Months": "{:.0f}",
                }
            ),
            width="stretch",
        )

    elif analysis_type == "Tenure Analysis":
        fig = px.scatter(
            df,
            x="Tenure_Months",
            y="Flight_Risk_Probability",
            color="Risk_Level",
            size="Base_Salary",
            hover_data=["Department"],
            color_discrete_map=RISK_COLORS,
            title="Tenure vs. flight-risk probability",
        )
        fig.update_layout(height=520)
        st.plotly_chart(fig, width="stretch")

    elif analysis_type == "Salary Analysis":
        fig = px.box(
            df,
            x="Department",
            y="Base_Salary",
            color="Risk_Level",
            color_discrete_map=RISK_COLORS,
            title="Salary distribution by department and risk level",
        )
        fig.update_layout(height=520)
        st.plotly_chart(fig, width="stretch")

    else:
        # Named aggregation keeps the output column names readable for HR users.
        dept_stats = (
            df.groupby("Department")
            .agg(
                Total_Employees=("Emp_ID", "count"),
                Avg_Risk_Probability=("Flight_Risk_Probability", "mean"),
                Avg_Salary=("Base_Salary", "mean"),
                Avg_Tenure_Months=("Tenure_Months", "mean"),
            )
            .sort_values("Total_Employees", ascending=False)
        )
        st.dataframe(
            dept_stats.style.format(
                {
                    "Avg_Risk_Probability": "{:.1%}",
                    "Avg_Salary": "${:,.0f}",
                    "Avg_Tenure_Months": "{:.1f}",
                }
            ),
            width="stretch",
        )


def render_ai_assistant() -> None:
    """Render the natural-language query assistant.

    The assistant is optional: if `OPENAI_API_KEY` is missing, the underlying
    helper returns a clear message instead of crashing the dashboard.
    """
    st.subheader("AI Data Assistant")
    st.markdown(
        "Ask a plain-English question. AttriSense converts it into safe read-only SQL and returns the result."
    )

    examples = [
        "How many high risk employees are in Manufacturing?",
        "What is the average salary of High Risk employees?",
        "Show turnover risk counts by department.",
    ]
    selected_example = st.selectbox("Try an example", [""] + examples)
    user_question = st.text_input(
        "Question",
        value=selected_example,
        placeholder="Example: Show high risk employees by department",
    )

    if st.button("Generate SQL and run", width="stretch"):
        if not user_question.strip():
            st.warning("Enter a question first.")
            return

        with st.spinner("Generating a read-only SQL query..."):
            sql_query, result = query_database_with_ai(user_question)

        if not sql_query:
            st.error(result)
            return

        st.success("Query executed successfully.")
        st.code(sql_query, language="sql")

        # The SQL helper always returns a dictionary when execution succeeds.
        # Single-cell answers become KPI metrics; larger results become tables.
        rows = result.get("rows", []) if isinstance(result, dict) else []
        columns = result.get("columns", []) if isinstance(result, dict) else []
        if not rows:
            st.info("The query returned no rows.")
        elif len(rows) == 1 and len(rows[0]) == 1:
            st.metric("Result", rows[0][0])
        else:
            st.dataframe(pd.DataFrame(rows, columns=columns), width="stretch")


def main() -> None:
    """Load data and route users into the three dashboard tabs."""
    render_header()
    try:
        df = load_predictions()
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    tab1, tab2, tab3 = st.tabs(
        ["Executive Dashboard", "Detailed Analytics", "AI Assistant"]
    )
    with tab1:
        render_executive_dashboard(df)
    with tab2:
        render_deep_dive(df)
    with tab3:
        render_ai_assistant()


if __name__ == "__main__":
    main()
