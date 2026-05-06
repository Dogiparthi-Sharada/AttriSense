# AttriSense Design Decisions

## Product Goal

AttriSense is designed to be understandable first and impressive second. The project demonstrates a production-shaped workforce intelligence system without hiding the logic behind unnecessary infrastructure.

## Architecture Principles

- Keep each pipeline stage small and executable.
- Store shared paths and constants in `project_config.py`.
- Use synthetic data by default so the project is safe to demo.
- Prefer SQLite for local reproducibility.
- Keep AI features optional so the dashboard still runs without credentials.
- Validate model and AI outputs before exposing them to users.

## Data Layer

SQLite is used as the application database because it is portable, transparent, and easy to inspect. The main table is:

```text
workforce_predictions
```

The table can later be migrated to Postgres, Snowflake, BigQuery, or a governed HR warehouse without changing the dashboard contract.

## Modeling Layer

The predictive model uses:

- Random Forest for non-linear risk patterns.
- SMOTE to balance rare turnover events.
- Simple features: tenure, salary, and department.

The feature set is intentionally modest. That makes the demo easy to audit and creates a clean path for production enhancements such as manager changes, performance signals, commute distance, engagement scores, and compensation movement.

## AI Layer

The natural-language assistant uses LangChain and OpenAI to generate SQL. It includes guardrails:

- Only `SELECT` and `WITH` queries are allowed.
- Mutating SQL operations are blocked.
- SQLite is placed in query-only mode before execution.
- Missing API keys produce clear user-facing messages.

This keeps the assistant useful for demos while protecting the database from accidental write operations.

## RAG Layer

FAISS stores embeddings for synthetic exit interview notes. The current implementation is local and simple; a production version could add metadata filters, chunk provenance, access control, and scheduled rebuilds.

## Interface Layer

Streamlit is used because it is fast, Python-native, and ideal for analytics workflows. The dashboard favors executive clarity over visual noise:

- KPI cards for risk bands.
- Department risk concentration.
- Detailed drilldowns for high-risk employees, tenure, and compensation.
- A natural-language question box for non-technical users.

## Security Notes

- `.env` is ignored by Git.
- `.env.example` documents required variables without exposing secrets.
- The included records are synthetic and should never be treated as real employee data.
- Any real deployment should add authentication, role-based access, audit logging, and approved HR data governance.

## Why This Shape Works

AttriSense is small enough for a recruiter, hiring manager, or engineer to understand in minutes, but complete enough to show product judgment: data generation, ML, AI, visualization, documentation, and deployment entry point all work together.
