# AttriSense

AttriSense is an AI-powered workforce intelligence platform that helps leaders see retention risk before it becomes resignation volume. It combines synthetic HR data generation, machine learning flight-risk scoring, natural-language SQL, and an executive Streamlit dashboard in one maintainable Python project.

Repository: https://github.com/Dogiparthi-Sharada/AttriSense

## Why It Matters

Employee attrition is expensive, noisy, and usually spotted too late. AttriSense turns workforce data into a simple operating view:

- Who is most likely to leave?
- Which departments carry the largest risk concentration?
- What interventions should HR prioritize this week?
- How can non-technical users ask questions without writing SQL?

The current repo ships with synthetic data, so it is safe to demo publicly while preserving the shape of a real enterprise workforce analytics system.

## Product Snapshot

| Capability | What it does |
| --- | --- |
| Executive dashboard | Shows total workforce, risk bands, department concentration, and action priorities. |
| Predictive model | Trains a Random Forest classifier with SMOTE balancing for turnover risk scoring. |
| Natural-language data assistant | Converts HR questions into read-only SQLite queries using LangChain and OpenAI. |
| RAG-ready exit interview index | Builds a FAISS vector store from synthetic exit interview notes. |
| Public Streamlit runner | Starts the app on `0.0.0.0` so it can be exposed by a host, VM, or deployment platform. |

## Sample Outputs

The included demo database contains `5,000` synthetic employees.

### Dashboard KPIs

| Metric | Output |
| --- | ---: |
| Total workforce | 5,000 |
| High flight risk | 491 |
| Medium risk | 171 |
| Low risk | 4,338 |
| Average salary | $104,679 |
| Average tenure | 29.82 months |

### Risk by Department

| Department | High-risk employees |
| --- | ---: |
| Manufacturing | 370 |
| Engineering | 103 |
| Sales | 18 |

### Example High-Risk Records

| Emp_ID | Department | Tenure | Salary | Risk probability | Risk level |
| ---: | --- | ---: | ---: | ---: | --- |
| 1009 | Manufacturing | 3 months | $107,927 | 1.000 | High Risk |
| 1050 | Manufacturing | 20 months | $71,247 | 1.000 | High Risk |
| 1134 | Manufacturing | 3 months | $119,481 | 1.000 | High Risk |

### AI Assistant Example

Question:

```text
How many high risk employees are in Manufacturing?
```

Typical generated SQL:

```sql
SELECT COUNT(*) AS high_risk_manufacturing
FROM workforce_predictions
WHERE Department = 'Manufacturing'
  AND Risk_Level = 'High Risk';
```

Result:

```text
370
```

## Architecture

```text
Synthetic HR data
      |
      v
data_generator.py  ->  attrisense_synthetic_hr.csv
      |
      v
predictive_engine.py  ->  hr_enterprise.db
      |
      +--> dashboard.py  ->  Streamlit executive app
      |
      +--> ai_sql_constructor.py  ->  safe read-only NL-to-SQL
      |
      +--> rag_engine.py  ->  faiss_hr_index/
```

The project intentionally stays small: one shared config module, clear pipeline stages, and a Streamlit app that reads from SQLite.

## Quick Start

```bash
git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
cd AttriSense

python -m venv attrisense_env
attrisense_env\Scripts\activate

pip install -r requirements.txt
python run_attrisense.py
```

Open:

```text
http://localhost:8501
```

By default, `run_attrisense.py` binds Streamlit to `0.0.0.0:8501`.

## Optional AI Setup

The dashboard works without an OpenAI key for analytics and charts. The AI Assistant and FAISS index builder require an API key.

```bash
copy .env.example .env
```

Then set:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

## Rebuild the Demo Pipeline

Run these commands when you want to regenerate the synthetic dataset and model outputs:

```bash
python data_generator.py
python predictive_engine.py
python rag_engine.py
python run_attrisense.py
```

`rag_engine.py` requires `OPENAI_API_KEY`. The dashboard and predictive model do not.

## Project Structure

```text
AttriSense/
├── project_config.py            # Shared paths and pipeline constants
├── data_generator.py            # Synthetic workforce data generator
├── predictive_engine.py         # Flight-risk model and SQLite publisher
├── rag_engine.py                # FAISS index builder for exit interviews
├── ai_sql_constructor.py        # Safe natural-language to SQL helper
├── dashboard.py                 # Streamlit product dashboard
├── run_attrisense.py            # Public Streamlit launcher
├── attrisense_synthetic_hr.csv  # Demo dataset
├── hr_enterprise.db             # Demo prediction database
├── faiss_hr_index/              # Demo vector index
├── .streamlit/config.toml       # Streamlit runtime config
├── .env.example                 # Environment variable template
└── requirements.txt             # Python dependencies
```

## How to Read the Code

Start here if you are new to the repo:

1. `project_config.py` defines the shared filenames and risk thresholds.
2. `data_generator.py` creates safe synthetic employee data.
3. `predictive_engine.py` trains the model and writes predictions into SQLite.
4. `dashboard.py` loads SQLite data and renders the Streamlit product.
5. `ai_sql_constructor.py` powers the optional AI Assistant with read-only SQL guardrails.
6. `run_attrisense.py` is the single command-line launcher.

Every root Python function includes a docstring, and the more complex logic has inline comments so a beginner can follow the flow without guessing.

## Production Notes

- `.env` is ignored and should never be committed.
- The included data is synthetic and safe for demos.
- The AI SQL path validates generated SQL and only runs read-only queries.
- SQLite is used for simplicity; the same table contract can move to Postgres, Snowflake, or BigQuery.
- The model is intentionally interpretable and easy to replace with richer HR features.

## Roadmap

- Add model evaluation reports and feature importance export.
- Add SHAP explanations for individual high-risk employees.
- Add role-based access for HR partners and executives.
- Add deployment manifests for Streamlit Community Cloud and container platforms.
- Add CI checks for formatting, linting, and pipeline smoke tests.

## License and Data

This repository is a portfolio/demo system. All included employee records are synthetic and should be replaced with governed HR data connectors before real-world deployment.
