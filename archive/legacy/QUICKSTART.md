# AttriSense Quickstart

## 1. Clone

```bash
git clone https://github.com/Dogiparthi-Sharada/AttriSense.git
cd AttriSense
```

## 2. Create a Virtual Environment

```bash
python -m venv attrisense_env
```

Windows:

```bash
attrisense_env\Scripts\activate
```

macOS/Linux:

```bash
source attrisense_env/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Dashboard

```bash
python launch_streamlit_app.py
```

Open `http://localhost:8501`.

## 5. Optional AI Features

The dashboard charts work without an API key. The AI Assistant and RAG index builder require OpenAI credentials.

```bash
copy .env.example .env
```

Set:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

## 6. Rebuild Data and Model

```bash
python generate_demo_workforce_data.py
python train_retention_risk_model.py
python build_exit_interview_vector_index.py
```

`build_exit_interview_vector_index.py` requires `OPENAI_API_KEY`.

## Troubleshooting

| Issue | Fix |
| --- | --- |
| Missing database | Run `python train_retention_risk_model.py`. |
| Missing dataset | Run `python generate_demo_workforce_data.py`. |
| AI Assistant reports missing key | Add `OPENAI_API_KEY` to `.env`. |
| Port already in use | Run `python launch_streamlit_app.py --port 8502`. |
