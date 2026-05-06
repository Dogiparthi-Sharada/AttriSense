import sqlite3

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import DATABASE_PATH, SQL_TABLE_NAME
from natural_language_sql import query_database_with_ai

# ============= ENHANCED UI CONFIGURATION =============
st.set_page_config(
    page_title="AttriSense",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

# Custom CSS for better styling
st.markdown(
    """
<style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .insight-box {
        background-color: #f0f4ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .title-main {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============= HEADER =============
st.markdown(
    '<div class="title-main">AttriSense Workforce Intelligence</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Intelligent Workforce Intelligence & Predictive Analytics</div>',
    unsafe_allow_html=True,
)
st.divider()

# ============= LOAD DATA =============
conn = sqlite3.connect(DATABASE_PATH)
df = pd.read_sql_query(f"SELECT * FROM {SQL_TABLE_NAME}", conn)

# Calculate key metrics
total_employees = len(df)
high_risk_count = len(df[df["Risk_Level"] == "High Risk"])
medium_risk_count = len(df[df["Risk_Level"] == "Medium Risk"])
low_risk_count = len(df[df["Risk_Level"] == "Low Risk"])
high_risk_pct = high_risk_count / total_employees * 100

# ============= TABS =============
tab1, tab2, tab3 = st.tabs(
    ["📊 Executive Dashboard", "🔍 Detailed Analytics", "🤖 AI Assistant"]
)

# ============ TAB 1: EXECUTIVE DASHBOARD ============
with tab1:
    st.markdown("### Executive Summary")
    st.markdown("Real-time snapshot of workforce health and risk metrics")

    # Enhanced KPIs with descriptions
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4, gap="medium")

    with kpi_col1:
        st.metric(
            "👥 Total Workforce",
            f"{total_employees:,}",
            delta="Active Employees",
            delta_color="off",
        )
        st.markdown("_All actively tracked employees in the organization_")

    with kpi_col2:
        st.metric(
            "⚠️ High Flight Risk",
            f"{high_risk_count:,}",
            delta=f"{high_risk_pct:.1f}% of workforce",
            delta_color="inverse",
        )
        st.markdown("_Employees with >75% probability of leaving_")

    with kpi_col3:
        st.metric(
            "⏱️ Medium Risk",
            f"{medium_risk_count:,}",
            delta=f"{(medium_risk_count / total_employees * 100):.1f}% of workforce",
            delta_color="off",
        )
        st.markdown("_Requires monitoring (40-75% risk probability)_")

    with kpi_col4:
        st.metric(
            "✅ Low Risk",
            f"{low_risk_count:,}",
            delta=f"{(low_risk_count / total_employees * 100):.1f}% of workforce",
            delta_color="normal",
        )
        st.markdown("_Stable employees with low turnover risk_")

    st.divider()

    # Key Insights Section
    st.markdown("### 📈 Key Insights")

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        manufacturing_avg_tenure = df[df["Department"] == "Manufacturing"][
            "Tenure_Months"
        ].mean()
        st.info(
            f"🏭 **Manufacturing Avg Tenure**: {manufacturing_avg_tenure:.1f} months\n\n"
            f"Longest-tenured department with {len(df[df['Department'] == 'Manufacturing']):,} employees"
        )

    with insight_col2:
        avg_salary = df["Base_Salary"].mean()
        st.info(
            f"💰 **Average Salary**: ${avg_salary:,.0f}\n\n"
            "Cross-organizational compensation baseline"
        )

    with insight_col3:
        at_risk_action = len(
            df[(df["Risk_Level"] == "High Risk") & (df["Tenure_Months"] < 6)]
        )
        st.warning(
            f"🚨 **Critical Attention Needed**: {at_risk_action} employees\n\n"
            "New hires (<6 months) at high risk of leaving"
        )

    st.divider()

    # Visualizations
    st.markdown("### 📊 Core Visualizations")

    viz_col1, viz_col2 = st.columns(2, gap="large")

    # Flight Risk Distribution (Enhanced Donut)
    with viz_col1:
        st.markdown("#### Flight Risk Distribution")
        st.markdown("_Breakdown of workforce by flight risk category_")

        risk_counts = df["Risk_Level"].value_counts()
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=risk_counts.index,
                    values=risk_counts.values,
                    hole=0.4,
                    marker=dict(colors=["#EF553B", "#FFA15A", "#00CC96"]),
                    textposition="inside",
                    textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
                )
            ]
        )
        fig_donut.update_layout(
            height=400,
            showlegend=True,
            font=dict(size=12),
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_donut, width="stretch")

    # High Risk by Department (Enhanced Bar)
    with viz_col2:
        st.markdown("#### High Risk Employees by Department")
        st.markdown("_Department-level risk distribution and headcount_")

        high_risk_by_dept = (
            df[df["Risk_Level"] == "High Risk"]
            .groupby("Department")
            .size()
            .reset_index(name="Count")
        )
        total_by_dept = df.groupby("Department").size().reset_index(name="Total")
        merged = high_risk_by_dept.merge(total_by_dept, on="Department")
        merged["Percentage"] = (merged["Count"] / merged["Total"] * 100).round(1)

        fig_bar = go.Figure(
            data=[
                go.Bar(
                    x=merged["Department"],
                    y=merged["Count"],
                    marker=dict(color=["#FF6B6B", "#4ECDC4", "#45B7D1"]),
                    text=merged["Count"],
                    textposition="auto",
                    hovertemplate="<b>%{x}</b><br>High Risk: %{y}<extra></extra>",
                )
            ]
        )
        fig_bar.update_layout(
            height=400,
            xaxis_title="Department",
            yaxis_title="High Risk Employee Count",
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        st.plotly_chart(fig_bar, width="stretch")

    st.divider()

    # Risk by Department Comparison
    st.markdown("### 📍 Risk Profile by Department")
    st.markdown("_Comprehensive breakdown showing all risk categories per department_")

    risk_by_dept = pd.crosstab(df["Department"], df["Risk_Level"])
    fig_stacked = go.Figure(
        data=[
            go.Bar(
                name="High Risk",
                x=risk_by_dept.index,
                y=risk_by_dept.get("High Risk", 0),
                marker_color="#EF553B",
            ),
            go.Bar(
                name="Medium Risk",
                x=risk_by_dept.index,
                y=risk_by_dept.get("Medium Risk", 0),
                marker_color="#FFA15A",
            ),
            go.Bar(
                name="Low Risk",
                x=risk_by_dept.index,
                y=risk_by_dept.get("Low Risk", 0),
                marker_color="#00CC96",
            ),
        ]
    )
    fig_stacked.update_layout(
        barmode="stack",
        xaxis_title="Department",
        yaxis_title="Employee Count",
        height=400,
        hovermode="x unified",
    )
    st.plotly_chart(fig_stacked, width="stretch")


# ============ TAB 2: DETAILED ANALYTICS ============
with tab2:
    st.markdown("### 🔍 Deep Dive Analysis")

    analysis_type = st.selectbox(
        "Select Analysis Type",
        [
            "High Risk Employees",
            "Tenure Analysis",
            "Salary Analysis",
            "Department Comparison",
        ],
    )

    if analysis_type == "High Risk Employees":
        st.markdown("#### High-Risk Workforce - Detailed View")
        st.markdown(
            "_Employees with >75% probability of leaving - requires immediate retention action_"
        )

        high_risk_df = df[df["Risk_Level"] == "High Risk"].copy()
        high_risk_df = high_risk_df.sort_values(
            "Flight_Risk_Probability", ascending=False
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("High Risk Count", len(high_risk_df))
        with col2:
            st.metric(
                "Avg Risk Probability",
                f"{high_risk_df['Flight_Risk_Probability'].mean():.2%}",
            )
        with col3:
            st.metric(
                "Avg Tenure (Months)", f"{high_risk_df['Tenure_Months'].mean():.1f}"
            )

        st.divider()

        # Risk distribution visualization
        fig_risk_dist = px.histogram(
            high_risk_df,
            x="Flight_Risk_Probability",
            nbins=20,
            title="Distribution of Flight Risk Probability",
            labels={
                "Flight_Risk_Probability": "Risk Probability",
                "count": "Number of Employees",
            },
            color_discrete_sequence=["#EF553B"],
        )
        st.plotly_chart(fig_risk_dist, width="stretch")

        st.divider()
        st.markdown("#### Recommended Actions for High Risk Employees")

        retention_strategies = {
            ">0.90": "🔴 CRITICAL: Immediate retention interview, salary review, promotion consideration",
            "0.80-0.90": "🟠 HIGH: Retention bonus, career development plan, mentorship",
            "0.75-0.80": "🟡 MEDIUM: Regular check-ins, skill development opportunities",
        }

        for risk_range, strategy in retention_strategies.items():
            st.markdown(f"**Risk Level {risk_range}**: {strategy}")

        st.divider()
        st.markdown("#### High Risk Employee Details")
        display_df = high_risk_df[
            [
                "Emp_ID",
                "Department",
                "Tenure_Months",
                "Base_Salary",
                "Flight_Risk_Probability",
                "Risk_Level",
            ]
        ].head(20)
        st.dataframe(
            display_df.style.format(
                {
                    "Flight_Risk_Probability": "{:.2%}",
                    "Base_Salary": "${:,.0f}",
                    "Tenure_Months": "{:.1f}",
                }
            ),
            width="stretch",
        )

    elif analysis_type == "Tenure Analysis":
        st.markdown("#### Tenure-Based Workforce Analysis")
        st.markdown(
            "_Understanding employment longevity and its correlation with turnover risk_"
        )

        fig_tenure = px.scatter(
            df,
            x="Tenure_Months",
            y="Flight_Risk_Probability",
            color="Risk_Level",
            size="Base_Salary",
            hover_data=["Department"],
            title="Tenure vs Flight Risk Probability",
            color_discrete_map={
                "High Risk": "#EF553B",
                "Medium Risk": "#FFA15A",
                "Low Risk": "#00CC96",
            },
            labels={
                "Tenure_Months": "Tenure (Months)",
                "Flight_Risk_Probability": "Flight Risk Probability",
            },
        )
        fig_tenure.update_layout(height=500)
        st.plotly_chart(fig_tenure, width="stretch")

        # Tenure statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Tenure", f"{df['Tenure_Months'].mean():.1f} months")
        with col2:
            st.metric("Median Tenure", f"{df['Tenure_Months'].median():.1f} months")
        with col3:
            st.metric("Employees <6 Months", f"{len(df[df['Tenure_Months'] < 6]):,}")

    elif analysis_type == "Salary Analysis":
        st.markdown("#### Compensation & Salary Analysis")
        st.markdown("_Salary distribution and its relationship with employee retention_")

        fig_salary = px.box(
            df,
            x="Department",
            y="Base_Salary",
            color="Risk_Level",
            title="Salary Distribution by Department & Risk Level",
            color_discrete_map={
                "High Risk": "#EF553B",
                "Medium Risk": "#FFA15A",
                "Low Risk": "#00CC96",
            },
            labels={"Base_Salary": "Annual Salary ($)", "Department": "Department"},
        )
        fig_salary.update_layout(height=500)
        st.plotly_chart(fig_salary, width="stretch")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Salary", f"${df['Base_Salary'].mean():,.0f}")
        with col2:
            st.metric("Median Salary", f"${df['Base_Salary'].median():,.0f}")
        with col3:
            st.metric(
                "Salary Range",
                f"${df['Base_Salary'].max() - df['Base_Salary'].min():,.0f}",
            )

    else:  # Department Comparison
        st.markdown("#### Department-Level Metrics")
        st.markdown("_Side-by-side comparison of all departments_")

        dept_stats = (
            df.groupby("Department")
            .agg(
                {
                    "Emp_ID": "count",
                    "Flight_Risk_Probability": "mean",
                    "Base_Salary": "mean",
                    "Tenure_Months": "mean",
                }
            )
            .round(2)
        )
        dept_stats.columns = [
            "Total Employees",
            "Avg Risk Probability",
            "Avg Salary",
            "Avg Tenure (Months)",
        ]

        st.dataframe(
            dept_stats.style.format(
                {
                    "Avg Risk Probability": "{:.2%}",
                    "Avg Salary": "${:,.0f}",
                    "Avg Tenure (Months)": "{:.1f}",
                }
            ),
            width="stretch",
        )


# ============ TAB 3: AI ASSISTANT ============
with tab3:
    st.markdown("### 🤖 Natural Language Data Query Assistant")
    st.markdown(
        "Ask questions about your workforce data in plain English. Our AI will translate them to SQL and return insights."
    )

    st.divider()

    # Example questions
    st.markdown("#### 💡 Example Questions")
    example_col1, example_col2 = st.columns(2)

    with example_col1:
        st.caption("📌 Common Queries:")
        st.write("• How many high risk employees are in manufacturing?")
        st.write("• What's the average salary of employees with 12+ months tenure?")
        st.write("• Show me all medium risk employees in engineering")

    with example_col2:
        st.caption("📌 Advanced Queries:")
        st.write("• Count employees earning over $100k with high flight risk")
        st.write("• What's the average tenure in each department?")
        st.write("• Show me the highest flight risk probability employee")

    st.divider()

    user_question = st.text_input(
        "Ask a question about your workforce data:",
        placeholder="e.g., How many high risk employees are in the manufacturing department?",
    )

    if st.button("🚀 Generate SQL & Execute", width="stretch"):
        if user_question:
            with st.spinner("🔄 AI is analyzing your question and generating SQL..."):
                sql_query, result = query_database_with_ai(user_question)

                if sql_query and sql_query != "None":
                    st.success("✅ Query Executed Successfully!")

                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.markdown("#### 📝 Generated SQL Query")
                        st.code(sql_query, language="sql")

                    with col2:
                        st.markdown("#### 📊 Result")
                        result_rows = (
                            result.get("rows", [])
                            if isinstance(result, dict)
                            else result
                        )
                        result_columns = (
                            result.get("columns", [])
                            if isinstance(result, dict)
                            else None
                        )

                        if isinstance(result_rows, list) and len(result_rows) > 0:
                            # Format results nicely
                            if len(result_rows[0]) == 1:
                                st.metric("Result", result_rows[0][0])
                            else:
                                result_df = pd.DataFrame(
                                    result_rows, columns=result_columns
                                )
                                st.dataframe(result_df, width="stretch")
                        else:
                            st.write(result)
                else:
                    st.error("❌ Error executing query. Please try a different question.")
                    if result:
                        st.error(result)
        else:
            st.warning("⚠️ Please enter a question first!")

conn.close()
