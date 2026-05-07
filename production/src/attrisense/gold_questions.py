# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/gold_questions.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Gold-standard NL\u2192SQL questions for the AttriSense evaluation harness.

Each entry contains:
- `id`: stable identifier
- `category`: one of the categories we report accuracy on
- `question`: a natural-language question a real HR partner might ask
- `expected_sql`: a hand-validated SQLite query that returns the right rows
- `expected_rowcount`: optional cardinality assertion (None = any)

We compare the agent's generated SQL by EXECUTING both queries and
comparing result sets, not by string matching, because there are many
syntactically different SQL strings that produce the same answer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoldQuestion:
    """A single NL\u2192SQL evaluation case."""

    id: str
    category: str
    question: str
    expected_sql: str
    expected_rowcount: int | None = None


GOLD_QUESTIONS: tuple[GoldQuestion, ...] = (
    # ----- Counts (10) -----
    GoldQuestion("count_total", "count", "How many employees are there in total?",
                 "SELECT COUNT(*) AS total FROM workforce_predictions"),
    GoldQuestion("count_high_risk", "count", "How many high-risk employees are there?",
                 "SELECT COUNT(*) AS high_risk FROM workforce_predictions WHERE Risk_Level = 'High Risk'"),
    GoldQuestion("count_high_risk_mfg", "count", "How many high-risk employees are in Manufacturing?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Risk_Level='High Risk' AND Department='Manufacturing'"),
    GoldQuestion("count_eng", "count", "How many engineering employees do we have?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Department='Engineering'"),
    GoldQuestion("count_sales", "count", "How many people work in Sales?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Department='Sales'"),
    GoldQuestion("count_low_risk", "count", "How many low-risk employees do we have?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Risk_Level='Low Risk'"),
    GoldQuestion("count_short_tenure", "count", "How many employees have less than 6 months of tenure?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Tenure_Months < 6"),
    GoldQuestion("count_high_paid", "count", "How many employees earn more than $120,000?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Base_Salary > 120000"),
    GoldQuestion("count_left", "count", "How many employees actually left voluntarily?",
                 "SELECT COUNT(*) AS n FROM workforce_predictions WHERE Voluntary_Turnover='Yes'"),
    GoldQuestion("count_managers", "count", "How many distinct managers are there?",
                 "SELECT COUNT(DISTINCT Manager_ID) AS n FROM workforce_predictions"),

    # ----- Aggregates (10) -----
    GoldQuestion("avg_salary", "aggregate", "What is the average base salary?",
                 "SELECT AVG(Base_Salary) AS avg_salary FROM workforce_predictions"),
    GoldQuestion("avg_tenure", "aggregate", "What is the average tenure in months?",
                 "SELECT AVG(Tenure_Months) AS avg_tenure FROM workforce_predictions"),
    GoldQuestion("avg_risk_mfg", "aggregate", "What is the average flight-risk probability in Manufacturing?",
                 "SELECT AVG(Flight_Risk_Probability) AS avg_risk FROM workforce_predictions WHERE Department='Manufacturing'"),
    GoldQuestion("max_salary_eng", "aggregate", "What is the highest salary in Engineering?",
                 "SELECT MAX(Base_Salary) AS max_salary FROM workforce_predictions WHERE Department='Engineering'"),
    GoldQuestion("min_salary_sales", "aggregate", "What is the lowest salary in Sales?",
                 "SELECT MIN(Base_Salary) AS min_salary FROM workforce_predictions WHERE Department='Sales'"),
    GoldQuestion("median_tenure_mfg", "aggregate", "What is the median tenure in Manufacturing?",
                 "SELECT Tenure_Months FROM workforce_predictions WHERE Department='Manufacturing' ORDER BY Tenure_Months LIMIT 1 OFFSET (SELECT COUNT(*) FROM workforce_predictions WHERE Department='Manufacturing')/2"),
    GoldQuestion("total_salary_high_risk", "aggregate", "What is the total salary exposure for high-risk employees?",
                 "SELECT SUM(Base_Salary) AS exposure FROM workforce_predictions WHERE Risk_Level='High Risk'"),
    GoldQuestion("avg_manager_tenure", "aggregate", "What is the average manager tenure?",
                 "SELECT AVG(Manager_Tenure_Months) AS avg_mgr_tenure FROM workforce_predictions"),
    GoldQuestion("avg_risk_overall", "aggregate", "What is the average flight-risk probability across the company?",
                 "SELECT AVG(Flight_Risk_Probability) AS avg_risk FROM workforce_predictions"),
    GoldQuestion("max_risk", "aggregate", "What is the highest flight-risk probability in the company?",
                 "SELECT MAX(Flight_Risk_Probability) AS max_risk FROM workforce_predictions"),

    # ----- Group-by (10) -----
    GoldQuestion("count_by_dept", "groupby", "How many employees are in each department?",
                 "SELECT Department, COUNT(*) AS n FROM workforce_predictions GROUP BY Department"),
    GoldQuestion("count_by_risk_level", "groupby", "How many employees are in each risk level?",
                 "SELECT Risk_Level, COUNT(*) AS n FROM workforce_predictions GROUP BY Risk_Level"),
    GoldQuestion("avg_salary_by_dept", "groupby", "What is the average salary by department?",
                 "SELECT Department, AVG(Base_Salary) AS avg_salary FROM workforce_predictions GROUP BY Department"),
    GoldQuestion("avg_tenure_by_dept", "groupby", "What is the average tenure per department?",
                 "SELECT Department, AVG(Tenure_Months) AS avg_tenure FROM workforce_predictions GROUP BY Department"),
    GoldQuestion("high_risk_by_dept", "groupby", "How many high-risk employees in each department?",
                 "SELECT Department, COUNT(*) AS n FROM workforce_predictions WHERE Risk_Level='High Risk' GROUP BY Department"),
    GoldQuestion("avg_risk_by_dept", "groupby", "What is the average flight-risk probability per department?",
                 "SELECT Department, AVG(Flight_Risk_Probability) AS avg_risk FROM workforce_predictions GROUP BY Department"),
    GoldQuestion("count_by_dept_risk", "groupby", "How many employees per department per risk level?",
                 "SELECT Department, Risk_Level, COUNT(*) AS n FROM workforce_predictions GROUP BY Department, Risk_Level"),
    GoldQuestion("salary_by_risk_level", "groupby", "What is the average salary by risk level?",
                 "SELECT Risk_Level, AVG(Base_Salary) AS avg_salary FROM workforce_predictions GROUP BY Risk_Level"),
    GoldQuestion("manager_count_by_dept", "groupby", "How many distinct managers per department?",
                 "SELECT Department, COUNT(DISTINCT Manager_ID) AS n_mgrs FROM workforce_predictions GROUP BY Department"),
    GoldQuestion("survival_by_risk", "groupby", "Average 12-month survival probability by risk level",
                 "SELECT Risk_Level, AVG(Cox_12_Month_Survival_Probability) AS avg_survival FROM workforce_predictions GROUP BY Risk_Level"),

    # ----- Top-K / Order-by (10) -----
    GoldQuestion("top10_risk", "topk", "Show me the top 10 highest-risk employees",
                 "SELECT Emp_ID, Department, Flight_Risk_Probability FROM workforce_predictions ORDER BY Flight_Risk_Probability DESC LIMIT 10"),
    GoldQuestion("top5_dept_risk", "topk", "Show me the 5 departments with the highest average flight risk",
                 "SELECT Department, AVG(Flight_Risk_Probability) AS avg_risk FROM workforce_predictions GROUP BY Department ORDER BY avg_risk DESC LIMIT 5"),
    GoldQuestion("top10_high_risk_mfg", "topk", "Show me the top 10 highest-risk Manufacturing employees",
                 "SELECT Emp_ID, Tenure_Months, Base_Salary, Flight_Risk_Probability FROM workforce_predictions WHERE Department='Manufacturing' ORDER BY Flight_Risk_Probability DESC LIMIT 10"),
    GoldQuestion("top10_short_tenure", "topk", "Top 10 shortest-tenured employees",
                 "SELECT Emp_ID, Department, Tenure_Months FROM workforce_predictions ORDER BY Tenure_Months ASC LIMIT 10"),
    GoldQuestion("top5_paid_mfg", "topk", "Top 5 highest-paid Manufacturing employees",
                 "SELECT Emp_ID, Base_Salary FROM workforce_predictions WHERE Department='Manufacturing' ORDER BY Base_Salary DESC LIMIT 5"),
    GoldQuestion("top5_managers_high_risk", "topk", "Which 5 managers have the most high-risk reports?",
                 "SELECT Manager_ID, COUNT(*) AS n FROM workforce_predictions WHERE Risk_Level='High Risk' GROUP BY Manager_ID ORDER BY n DESC LIMIT 5"),
    GoldQuestion("top5_lowest_paid", "topk", "Top 5 lowest-paid employees in the company",
                 "SELECT Emp_ID, Department, Base_Salary FROM workforce_predictions ORDER BY Base_Salary ASC LIMIT 5"),
    GoldQuestion("top10_lowest_survival", "topk", "Top 10 employees with the lowest 12-month survival probability",
                 "SELECT Emp_ID, Cox_12_Month_Survival_Probability FROM workforce_predictions ORDER BY Cox_12_Month_Survival_Probability ASC LIMIT 10"),
    GoldQuestion("top5_short_mgr_tenure", "topk", "Top 5 employees with the newest managers",
                 "SELECT Emp_ID, Manager_Tenure_Months FROM workforce_predictions ORDER BY Manager_Tenure_Months ASC LIMIT 5"),
    GoldQuestion("top10_high_risk_low_salary", "topk", "Top 10 high-risk employees who earn under $80k",
                 "SELECT Emp_ID, Department, Base_Salary, Flight_Risk_Probability FROM workforce_predictions WHERE Risk_Level='High Risk' AND Base_Salary < 80000 ORDER BY Flight_Risk_Probability DESC LIMIT 10"),

    # ----- Filter combinations (10) -----
    GoldQuestion("hr_mfg_short_tenure", "filter", "High-risk Manufacturing employees with under 12 months tenure",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='High Risk' AND Department='Manufacturing' AND Tenure_Months < 12"),
    GoldQuestion("eng_high_paid", "filter", "Engineering employees earning more than $130k",
                 "SELECT * FROM workforce_predictions WHERE Department='Engineering' AND Base_Salary > 130000"),
    GoldQuestion("hr_new_managers", "filter", "High-risk employees whose managers have been in role under 12 months",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='High Risk' AND Manager_Tenure_Months < 12"),
    GoldQuestion("low_paid_short_tenure", "filter", "Employees earning under $70k with under 6 months tenure",
                 "SELECT * FROM workforce_predictions WHERE Base_Salary < 70000 AND Tenure_Months < 6"),
    GoldQuestion("hr_long_tenure", "filter", "High-risk employees with more than 36 months of tenure",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='High Risk' AND Tenure_Months > 36"),
    GoldQuestion("medium_risk_eng", "filter", "Medium-risk Engineering employees",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='Medium Risk' AND Department='Engineering'"),
    GoldQuestion("sales_low_risk", "filter", "Low-risk Sales employees",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='Low Risk' AND Department='Sales'"),
    GoldQuestion("manufacturing_voluntary_left", "filter", "Manufacturing employees who voluntarily left",
                 "SELECT * FROM workforce_predictions WHERE Department='Manufacturing' AND Voluntary_Turnover='Yes'"),
    GoldQuestion("hr_active", "filter", "High-risk employees who are still active",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='High Risk' AND Voluntary_Turnover='No'"),
    GoldQuestion("hr_low_survival", "filter", "High-risk employees with under 0.50 12-month survival probability",
                 "SELECT * FROM workforce_predictions WHERE Risk_Level='High Risk' AND Cox_12_Month_Survival_Probability < 0.50"),
)


def by_category() -> dict[str, list[GoldQuestion]]:
    """Index gold questions by category for accuracy reporting."""
    bucket: dict[str, list[GoldQuestion]] = {}
    for question in GOLD_QUESTIONS:
        bucket.setdefault(question.category, []).append(question)
    return bucket
