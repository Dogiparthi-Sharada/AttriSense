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
python run_attrisense.py
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
python data_generator.py
python predictive_engine.py
python rag_engine.py
```

`rag_engine.py` requires `OPENAI_API_KEY`.

## Troubleshooting

| Issue | Fix |
| --- | --- |
| Missing database | Run `python predictive_engine.py`. |
| Missing dataset | Run `python data_generator.py`. |
| AI Assistant reports missing key | Add `OPENAI_API_KEY` to `.env`. |
| Port already in use | Run `python run_attrisense.py --port 8502`. |
