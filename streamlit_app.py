import sqlite3

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config import (
    CALIBRATION_TABLE_NAME,
    DATABASE_PATH,
    DEPARTMENT_CODE_MAP,
    MODEL_ARTIFACT_PATH,
    SHAP_FEATURE_TABLE_NAME,
    SQL_TABLE_NAME,
    SURVIVAL_CURVE_TABLE_NAME,
)
from natural_language_sql import query_database_with_ai

# ---- Pixel pastel palette injection ----
import plotly.express as _px_pastel_inject
import plotly.io as _pio_pastel_inject
_PASTEL_SEQ = ["#B8B5E1", "#F5C4A0", "#B5D4A8", "#F2A8A0", "#F5E1A0", "#A8D5C8", "#D8C4E1"]
_px_pastel_inject.defaults.color_discrete_sequence = _PASTEL_SEQ
_px_pastel_inject.defaults.color_continuous_scale = [
    [0.0, "#FBF7F2"], [0.25, "#F5E1A0"], [0.5, "#F5C4A0"],
    [0.75, "#F2A8A0"], [1.0, "#B8B5E1"],
]
try:
    _pio_pastel_inject.templates.default = "simple_white"
except Exception:
    pass
# ---- end injection ----



SHAP_COLUMNS = [
    "SHAP_Tenure_Impact",
    "SHAP_Compensation_Impact",
    "SHAP_Department_Impact",
    "SHAP_Manager_Tenure_Impact",
]
SHAP_DRIVER_LABELS = {
    "SHAP_Tenure_Impact": "Tenure",
    "SHAP_Compensation_Impact": "Compensation",
    "SHAP_Department_Impact": "Department",
    "SHAP_Manager_Tenure_Impact": "Manager tenure",
}


def load_optional_table(connection: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    """Load an optional SQLite table without crashing when it is not present."""
    table_exists = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    if not table_exists:
        return pd.DataFrame()
    return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


@st.cache_resource
def load_model_artifact() -> dict[str, object] | None:
    """Load the persisted model artifact used by the What-If simulator."""
    if not MODEL_ARTIFACT_PATH.exists():
        return None
    return joblib.load(MODEL_ARTIFACT_PATH)


def format_currency(value: float) -> str:
    """Format large business values as whole-dollar strings."""
    return f"${value:,.0f}"


def categorize_risk(probability: float) -> str:
    """Convert a probability into the dashboard's risk-band language."""
    if probability > 0.75:
        return "High Risk"
    if probability > 0.40:
        return "Medium Risk"
    return "Low Risk"


def score_employee_scenario(
    model_artifact: dict[str, object],
    employee: pd.Series,
    salary_delta: int,
    tenure_extra: int,
    manager_change: bool,
) -> float:
    """Score a What-If scenario using the persisted production model."""
    feature_columns = model_artifact["feature_columns"]
    model = model_artifact["model"]
    modified = employee.copy()
    modified["Base_Salary"] = modified["Base_Salary"] * (1 + salary_delta / 100)
    modified["Tenure_Months"] = modified["Tenure_Months"] + tenure_extra

    # A manager change resets relationship tenure. Without a change, elapsed
    # time naturally adds to manager tenure along with employee tenure.
    if manager_change:
        modified["Manager_Tenure_Months"] = 0
    else:
        modified["Manager_Tenure_Months"] = modified["Manager_Tenure_Months"] + tenure_extra

    modified["Dept_Code"] = DEPARTMENT_CODE_MAP[modified["Department"]]
    scenario_frame = pd.DataFrame([{column: modified[column] for column in feature_columns}])
    return float(model.predict_proba(scenario_frame)[0][1])


def build_manager_rollup(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate employee risk into manager-level operating metrics."""
    rollup = (
        df.groupby(["Manager_ID", "Department"], as_index=False)
        .agg(
            Total_Reports=("Emp_ID", "count"),
            High_Risk_Reports=("Risk_Level", lambda values: int((values == "High Risk").sum())),
            Avg_Risk_Probability=("Flight_Risk_Probability", "mean"),
            Avg_Manager_Tenure_Months=("Manager_Tenure_Months", "mean"),
            Salary_Exposure=("Base_Salary", "sum"),
        )
    )
    rollup["High_Risk_Rate"] = rollup["High_Risk_Reports"] / rollup["Total_Reports"]
    rollup["Weighted_Risk_Exposure"] = rollup["Salary_Exposure"] * rollup["Avg_Risk_Probability"]
    return rollup.sort_values(["High_Risk_Rate", "Avg_Risk_Probability"], ascending=False)


def render_what_if_simulator(df: pd.DataFrame) -> None:
    """Render the live salary, tenure, and manager-change simulator."""
    st.markdown("#### What-If Simulator")
    model_artifact = load_model_artifact()
    if model_artifact is None:
        st.warning("Model artifact missing. Run `python train_retention_risk_model.py` first.")
        return

    employee_options = df.sort_values("Flight_Risk_Probability", ascending=False).head(300)
    labels = employee_options.apply(
        lambda row: (
            f"{int(row['Emp_ID'])} | {row['Department']} | "
            f"{row['Flight_Risk_Probability']:.1%} current risk"
        ),
        axis=1,
    )
    selected_label = st.selectbox("Employee scenario", labels, key="whatif_employee")
    employee_id = int(selected_label.split(" | ")[0])
    employee = employee_options[employee_options["Emp_ID"] == employee_id].iloc[0]

    slider_col1, slider_col2, slider_col3 = st.columns(3)
    salary_delta = slider_col1.slider("Salary change (%)", -20, 20, 0)
    tenure_extra = slider_col2.slider("Tenure extension (months)", 0, 24, 0)
    manager_change = slider_col3.checkbox("Manager change")

    new_probability = score_employee_scenario(
        model_artifact,
        employee,
        salary_delta,
        tenure_extra,
        manager_change,
    )
    current_probability = float(employee["Flight_Risk_Probability"])
    delta = new_probability - current_probability

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Current risk", f"{current_probability:.1%}", employee["Risk_Level"])
    kpi2.metric("Scenario risk", f"{new_probability:.1%}", f"{delta:+.1%}")
    kpi3.metric("Scenario band", categorize_risk(new_probability))
    kpi4.metric("Current manager tenure", f"{employee['Manager_Tenure_Months']:.0f} months")

    if delta < -0.05:
        st.success("This scenario materially reduces flight risk in the model.")
    elif delta > 0.05:
        st.warning("This scenario increases flight risk. It needs a stronger intervention.")
    else:
        st.info("This scenario has a modest model impact. Try combining salary and tenure levers.")


def render_manager_rollup(df: pd.DataFrame) -> None:
    """Render manager-level risk concentration and action queues."""
    st.markdown("#### Manager-Level Risk Rollup")
    manager_rollup = build_manager_rollup(df)
    top_managers = manager_rollup.head(15).copy()
    top_managers["Manager_ID"] = top_managers["Manager_ID"].astype(str)

    chart = px.bar(
        top_managers.sort_values("High_Risk_Rate"),
        x="High_Risk_Rate",
        y="Manager_ID",
        orientation="h",
        color="Department",
        text="High_Risk_Reports",
        title="Managers with highest high-risk concentration",
        labels={"High_Risk_Rate": "% high risk", "Manager_ID": "Manager ID"},
    )
    chart.update_traces(texttemplate="%{text} high-risk", textposition="outside")
    chart.update_layout(height=520, xaxis_tickformat=".0%")
    st.plotly_chart(chart, width="stretch")

    st.dataframe(
        manager_rollup[
            [
                "Manager_ID",
                "Department",
                "Total_Reports",
                "High_Risk_Reports",
                "High_Risk_Rate",
                "Avg_Risk_Probability",
                "Avg_Manager_Tenure_Months",
                "Weighted_Risk_Exposure",
            ]
        ]
        .head(25)
        .style.format(
            {
                "High_Risk_Rate": "{:.1%}",
                "Avg_Risk_Probability": "{:.1%}",
                "Avg_Manager_Tenure_Months": "{:.1f}",
                "Weighted_Risk_Exposure": "${:,.0f}",
            }
        ),
        width="stretch",
    )


def render_attrition_cost_calculator(df: pd.DataFrame) -> None:
    """Render the CFO-facing cost-of-attrition calculator."""
    st.markdown("#### Cost-of-Attrition Calculator")
    multiplier = st.slider("Replacement cost multiplier", 0.5, 3.0, 1.5, 0.1)
    high_risk_df = df[df["Risk_Level"] == "High Risk"]
    annualized_loss = len(high_risk_df) * df["Base_Salary"].mean() * multiplier
    probability_weighted_loss = (
        high_risk_df["Base_Salary"] * high_risk_df["Flight_Risk_Probability"] * multiplier
    ).sum()
    quarterly_loss = annualized_loss / 4

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted preventable loss this quarter", format_currency(quarterly_loss))
    col2.metric("Annualized high-risk exposure", format_currency(annualized_loss))
    col3.metric("Probability-weighted exposure", format_currency(probability_weighted_loss))

    st.info(
        "CFO translation: this turns model output into a budget conversation. "
        "The default assumes replacement cost is 1.5x salary."
    )


def render_decision_tools(df: pd.DataFrame) -> None:
    """Render Tier 1 tools that convert predictions into business action."""
    st.markdown("### Decision Tools")
    st.markdown("Tier 1 features that move AttriSense from prediction into action.")
    tool_tabs = st.tabs(["What-If Simulator", "Manager Rollup", "Cost Calculator"])
    with tool_tabs[0]:
        render_what_if_simulator(df)
    with tool_tabs[1]:
        render_manager_rollup(df)
    with tool_tabs[2]:
        render_attrition_cost_calculator(df)


def render_survival_and_calibration(
    df: pd.DataFrame,
    survival_curves: pd.DataFrame,
    calibration_table: pd.DataFrame,
) -> None:
    """Render Tier 2 Cox survival analysis and calibration QA."""
    st.markdown("### Survival & Calibration")
    st.markdown("Tier 2 model-risk views for time-to-event decisions and probability QA.")

    if survival_curves.empty or calibration_table.empty:
        st.warning("Survival or calibration outputs are missing. Run `python train_retention_risk_model.py`.")
        return

    high_risk = df[df["Risk_Level"] == "High Risk"]
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "High-risk median expected tenure",
        f"{high_risk['Cox_Median_Expected_Tenure_Months'].median():.1f} months",
    )
    col2.metric(
        "High-risk 12-month survival",
        f"{high_risk['Cox_12_Month_Survival_Probability'].mean():.1%}",
    )
    col3.metric("Calibration Brier score", f"{calibration_table['Brier_Score'].iloc[0]:.3f}")

    survival_chart = px.line(
        survival_curves,
        x="Month",
        y="Survival_Probability",
        color="Risk_Level",
        markers=True,
        title="Cox survival curves by risk cohort",
        labels={"Survival_Probability": "Probability still employed"},
    )
    survival_chart.update_layout(height=470, yaxis_tickformat=".0%")
    st.plotly_chart(survival_chart, width="stretch")

    calibration_chart = go.Figure()
    calibration_chart.add_trace(
        go.Scatter(
            x=calibration_table["Mean_Predicted_Probability"],
            y=calibration_table["Observed_Turnover_Rate"],
            mode="lines+markers",
            name="Model calibration",
        )
    )
    calibration_chart.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Perfect calibration",
            line={"dash": "dash", "color": "#64748b"},
        )
    )
    calibration_chart.update_layout(
        title="Calibration plot: predicted vs observed turnover",
        xaxis_title="Mean predicted probability",
        yaxis_title="Observed turnover rate",
        height=460,
        xaxis_tickformat=".0%",
        yaxis_tickformat=".0%",
    )
    st.plotly_chart(calibration_chart, width="stretch")

    st.dataframe(
        calibration_table.style.format(
            {
                "Mean_Predicted_Probability": "{:.1%}",
                "Observed_Turnover_Rate": "{:.1%}",
                "Brier_Score": "{:.3f}",
                "Holdout_Employee_Count": "{:,.0f}",
            }
        ),
        width="stretch",
    )


def render_ethics_tab(df: pd.DataFrame) -> None:
    """Render limitations, ethics, and responsible AI guardrails."""
    st.markdown("### Limitations & Ethics")
    st.markdown("A production-grade people analytics product must state what it will not do.")

    fairness_summary = (
        df.groupby("Department")
        .agg(
            Employees=("Emp_ID", "count"),
            High_Risk_Rate=("Risk_Level", lambda values: (values == "High Risk").mean()),
            Avg_Risk=("Flight_Risk_Probability", "mean"),
        )
        .reset_index()
    )

    st.markdown(
        """
- **Synthetic data caveat:** this repository uses generated records for safe public demos.
- **Correlational, not causal:** model drivers describe learned associations, not proof that one factor causes attrition.
- **Fairness audit expectation:** department-level risk rates are monitored before any production deployment.
- **NYC Local Law 144 alignment:** production use would require an independent bias audit, public notices, and data governance.
- **No adverse-decision policy:** AttriSense should prioritize support and retention outreach, not discipline, termination, or compensation denial.
- **Human-in-the-loop:** HR partners must review context before acting on any score.
"""
    )
    st.markdown("Model card: [MODEL_CARD.md](MODEL_CARD.md)")
    st.dataframe(
        fairness_summary.style.format(
            {"High_Risk_Rate": "{:.1%}", "Avg_Risk": "{:.1%}"}
        ),
        width="stretch",
        hide_index=True,
    )



def has_shap_outputs(df: pd.DataFrame, feature_impact: pd.DataFrame) -> bool:
    """Return whether the database has the SHAP columns needed by the dashboard."""
    required_columns = set(SHAP_COLUMNS + ["SHAP_Explained", "Primary_Risk_Driver"])
    return required_columns.issubset(df.columns) and not feature_impact.empty


def build_employee_shap_frame(employee: pd.Series) -> pd.DataFrame:
    """Turn one employee row into a SHAP contribution table for plotting."""
    rows = []
    for column in SHAP_COLUMNS:
        impact = float(employee[column])
        rows.append(
            {
                "Driver": SHAP_DRIVER_LABELS[column],
                "SHAP Impact": impact,
                "Direction": "Increases risk" if impact >= 0 else "Reduces risk",
            }
        )
    return pd.DataFrame(rows).sort_values("SHAP Impact")


def render_enterprise_upgrade_path() -> None:
    """Show how SHAP turns the demo into a larger enterprise product concept."""
    st.markdown("#### Enterprise Upgrade Path")
    st.dataframe(
        pd.DataFrame(
            [
                (
                    "Explainable risk scoring",
                    "Every high-risk score has a named driver, making HR decisions auditable.",
                    "Builds executive trust and supports responsible AI review.",
                ),
                (
                    "Targeted retention playbooks",
                    "Tenure, compensation, and department drivers map to different interventions.",
                    "Reduces wasted spend on generic retention programs.",
                ),
                (
                    "Workforce exposure modeling",
                    "Salary-weighted risk converts attrition probability into financial exposure.",
                    "Turns HR analytics into CFO-readable business impact.",
                ),
                (
                    "Manager action queue",
                    "Top-risk employees can become prioritized coaching and retention tasks.",
                    "Creates a path from analytics to recurring enterprise workflow.",
                ),
            ],
            columns=["Product Layer", "What it adds", "Why it matters"],
        ),
        width="stretch",
        hide_index=True,
    )


def render_shap_explainability(
    df: pd.DataFrame,
    feature_impact: pd.DataFrame,
) -> None:
    """Render SHAP model explanations and business insight for executives."""
    st.markdown("### SHAP Explainability Center")
    st.markdown(
        "Positive SHAP values push an employee toward higher flight risk; negative values reduce the risk score."
    )

    if not has_shap_outputs(df, feature_impact):
        st.warning(
            "SHAP outputs are not available yet. Run `python train_retention_risk_model.py` "
            "to regenerate the database with explainability columns."
        )
        return

    explained_df = df[df["SHAP_Explained"].astype(bool)].copy()
    high_risk_df = df[df["Risk_Level"] == "High Risk"].copy()
    explained_high_risk = high_risk_df[high_risk_df["SHAP_Explained"].astype(bool)]
    estimated_salary_exposure = (
        high_risk_df["Base_Salary"] * high_risk_df["Flight_Risk_Probability"] * 0.5
    ).sum()
    top_global_driver = feature_impact.sort_values("Mean_ABS_SHAP", ascending=False).iloc[0]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")
    kpi1.metric("Employees with SHAP", f"{len(explained_df):,}", "high-risk-first sample")
    kpi2.metric("High-risk explained", f"{len(explained_high_risk):,}", "100% of high-risk group")
    kpi3.metric("Top global driver", top_global_driver["Feature"])
    kpi4.metric("Salary exposure", format_currency(estimated_salary_exposure), "demo estimate")

    st.divider()
    st.markdown("#### Global Risk Drivers")
    global_driver_chart = px.bar(
        feature_impact.sort_values("Mean_ABS_SHAP"),
        x="Mean_ABS_SHAP",
        y="Feature",
        orientation="h",
        text="Mean_ABS_SHAP",
        color="Feature",
        title="Mean absolute SHAP impact by feature",
    )
    global_driver_chart.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    global_driver_chart.update_layout(height=360, showlegend=False, xaxis_title="Average absolute risk impact")
    st.plotly_chart(global_driver_chart, width="stretch")

    st.dataframe(
        feature_impact[
            [
                "Feature",
                "Mean_ABS_SHAP",
                "Average_SHAP",
                "Explained_Employee_Count",
                "Business_Insight",
            ]
        ].style.format(
            {
                "Mean_ABS_SHAP": "{:.4f}",
                "Average_SHAP": "{:+.4f}",
                "Explained_Employee_Count": "{:,.0f}",
            }
        ),
        width="stretch",
    )

    st.divider()
    st.markdown("#### Board-Level Insights")
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    dominant_driver = explained_high_risk["Primary_Risk_Driver"].value_counts().idxmax()
    dominant_driver_count = explained_high_risk["Primary_Risk_Driver"].value_counts().max()
    insight_col1.info(
        f"**{dominant_driver}** is the primary driver for {dominant_driver_count:,} high-risk employees."
    )
    insight_col2.warning(
        f"The salary-weighted exposure estimate is **{format_currency(estimated_salary_exposure)}** in this demo scenario."
    )
    insight_col3.success(
        "Every high-risk employee now has an explainable top driver for targeted retention action."
    )

    department_driver_summary = (
        explained_df.groupby("Department")[SHAP_COLUMNS]
        .mean()
        .reset_index()
        .melt(id_vars="Department", var_name="Driver", value_name="Average SHAP Impact")
    )
    department_driver_summary["Driver"] = department_driver_summary["Driver"].map(SHAP_DRIVER_LABELS)
    department_chart = px.bar(
        department_driver_summary,
        x="Department",
        y="Average SHAP Impact",
        color="Driver",
        barmode="group",
        title="Average SHAP impact by department",
    )
    department_chart.add_hline(y=0, line_width=1, line_dash="dash", line_color="#64748b")
    department_chart.update_layout(height=430)
    st.plotly_chart(department_chart, width="stretch")

    st.divider()
    st.markdown("#### Individual High-Risk Explanation")
    employee_options = explained_high_risk.sort_values(
        "Flight_Risk_Probability",
        ascending=False,
    ).head(200)
    employee_labels = employee_options.apply(
        lambda row: (
            f"{int(row['Emp_ID'])} | {row['Department']} | "
            f"{row['Flight_Risk_Probability']:.1%} risk | {row['Primary_Risk_Driver']}"
        ),
        axis=1,
    )
    selected_label = st.selectbox("Select high-risk employee", employee_labels)
    selected_employee_id = int(selected_label.split(" | ")[0])
    selected_employee = employee_options[employee_options["Emp_ID"] == selected_employee_id].iloc[0]
    employee_shap = build_employee_shap_frame(selected_employee)

    employee_col1, employee_col2 = st.columns([1, 2], gap="large")
    with employee_col1:
        st.metric("Employee", int(selected_employee["Emp_ID"]))
        st.metric("Risk probability", f"{selected_employee['Flight_Risk_Probability']:.1%}")
        st.metric("Primary driver", selected_employee["Primary_Risk_Driver"])
        st.metric("Direction", selected_employee["Primary_Driver_Direction"])

    with employee_col2:
        employee_chart = px.bar(
            employee_shap,
            x="SHAP Impact",
            y="Driver",
            orientation="h",
            color="Direction",
            color_discrete_map={
                "Increases risk": "#D88B83",
                "Reduces risk": "#7AAA6E",
            },
            title="Employee-level SHAP contribution",
        )
        employee_chart.add_vline(x=0, line_width=1, line_dash="dash", line_color="#64748b")
        employee_chart.update_layout(height=320)
        st.plotly_chart(employee_chart, width="stretch")

    st.dataframe(
        employee_shap.style.format({"SHAP Impact": "{:+.4f}"}),
        width="stretch",
        hide_index=True,
    )

    render_enterprise_upgrade_path()

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
shap_feature_impact = load_optional_table(conn, SHAP_FEATURE_TABLE_NAME)
calibration_table = load_optional_table(conn, CALIBRATION_TABLE_NAME)
survival_curves = load_optional_table(conn, SURVIVAL_CURVE_TABLE_NAME)

# Calculate key metrics
total_employees = len(df)
high_risk_count = len(df[df["Risk_Level"] == "High Risk"])
medium_risk_count = len(df[df["Risk_Level"] == "Medium Risk"])
low_risk_count = len(df[df["Risk_Level"] == "Low Risk"])
high_risk_pct = high_risk_count / total_employees * 100

# ============= TABS =============
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "📊 Executive Dashboard",
        "🔍 Detailed Analytics",
        "Decision Tools",
        "SHAP Insights",
        "Survival & Calibration",
        "🤖 AI Assistant",
        "Ethics",
    ]
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
                    marker=dict(colors=["#F2A8A0", "#F5C4A0", "#B5D4A8"]),
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
                    marker=dict(color=["#F2A8A0", "#A8D5C8", "#B8B5E1"]),
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
                marker_color="#F2A8A0",
            ),
            go.Bar(
                name="Medium Risk",
                x=risk_by_dept.index,
                y=risk_by_dept.get("Medium Risk", 0),
                marker_color="#F5C4A0",
            ),
            go.Bar(
                name="Low Risk",
                x=risk_by_dept.index,
                y=risk_by_dept.get("Low Risk", 0),
                marker_color="#B5D4A8",
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
            color_discrete_sequence=["#F2A8A0"],
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
                "High Risk": "#F2A8A0",
                "Medium Risk": "#F5C4A0",
                "Low Risk": "#B5D4A8",
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
                "High Risk": "#F2A8A0",
                "Medium Risk": "#F5C4A0",
                "Low Risk": "#B5D4A8",
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


# ============ TAB 3: DECISION TOOLS ============
with tab3:
    render_decision_tools(df)


# ============ TAB 4: SHAP EXPLAINABILITY ============
with tab4:
    render_shap_explainability(df, shap_feature_impact)


# ============ TAB 5: SURVIVAL AND CALIBRATION ============
with tab5:
    render_survival_and_calibration(df, survival_curves, calibration_table)


# ============ TAB 6: AI ASSISTANT ============
with tab6:
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


# ============ TAB 7: ETHICS ============
with tab7:
    render_ethics_tab(df)

conn.close()