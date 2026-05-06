# AttriSense - Quickstart Guide

## Overview
AttriSense is an AI-powered workforce analytics platform featuring predictive workforce analytics, natural language to SQL querying, and a Streamlit dashboard.

## Prerequisites
- Python 3.8+
- OpenAI API key (for GPT-3.5-turbo and embeddings)
- Windows/Linux/Mac OS

## Installation

### 1. Clone/Download the Project
Place the project files in a directory, e.g., `AttriSense/`

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv attrisense_env

# Activate (Windows)
attrisense_env\Scripts\activate

# Activate (Linux/Mac)
source attrisense_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Data Pipeline Execution

### Step 1: Generate Synthetic HR Data
```bash
python data_generator.py
```
This creates `lumentum_synthetic_hr.csv` with 5000 synthetic employees.

### Step 2: Run Predictive Analytics
```bash
python predictive_engine.py
```
This trains a Random Forest model to predict turnover risk and saves results to `hr_enterprise.db`.

### Step 3: Build RAG Vector Database
```bash
python rag_engine.py
```
This processes exit interview text and creates FAISS vector index in `faiss_hr_index/`.

## Running the Application

### Start the Dashboard Publicly
```bash
python run_attrisense.py
```

The app binds to `0.0.0.0:8501` by default and will also be available locally at `http://localhost:8501`.

## Features

### Predictive Analytics Tab
- View workforce KPIs (total employees, high risk count, avg tenure, salary)
- Interactive charts: Flight risk distribution (donut chart), High risk by department (bar chart)
- Targeted retention interventions table with risk probability heatmap

### NL-to-SQL Assistant Tab
- Ask questions in natural language (e.g., "What is the average salary of High Risk employees in Manufacturing?")
- AI constructs and executes SQL queries against the database
- View generated SQL and results

## Troubleshooting

### Common Issues
1. **Module not found**: Ensure virtual environment is activated and dependencies are installed
2. **OpenAI API errors**: Check your API key in `.env` file
3. **Database errors**: Ensure `hr_enterprise.db` exists (run predictive_engine.py first)
4. **FAISS errors**: Ensure `faiss_hr_index/` directory exists (run rag_engine.py first)

### File Structure
```
AttriSense/
├── data_generator.py          # Generates synthetic HR data
├── predictive_engine.py       # ML model for turnover prediction
├── rag_engine.py             # Vector database for exit interviews
├── ai_sql_constructor.py     # NL-to-SQL AI agent
├── dashboard.py              # Streamlit web application
├── run_attrisense.py         # Public Streamlit launcher
├── lumentum_synthetic_hr.csv # Generated employee data
├── hr_enterprise.db          # SQLite database
├── faiss_hr_index/           # Vector database directory
├── .env                      # API keys (not in git)
└── attrisense_env/           # Virtual environment
```

## Next Steps
- Explore the dashboard tabs
- Try different natural language queries
- Modify data generation parameters in `data_generator.py`
- Experiment with different ML models in `predictive_engine.py`
