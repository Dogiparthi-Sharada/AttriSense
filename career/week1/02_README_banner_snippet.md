<!--
AttriSense — career/week1/02_README_banner_snippet.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# README banner snippet (refreshed for v2)

> Paste this block at the very top of `README.md`, immediately under
> the project title. Replaces the v1 banner (which still mentioned
> only the 3-modality stack).

---

```markdown
# AttriSense
*Open-source workforce intelligence — five-modality retention engine, Pixel-pastel UI, EEOC-fair by default.*

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?logo=streamlit)](https://attrisense.streamlit.app)
[![arXiv](https://img.shields.io/badge/arXiv-preprint-b31b1b?logo=arxiv)](https://arxiv.org/abs/XXXX.XXXXX)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![mkdocs](https://img.shields.io/badge/docs-mkdocs--strict-blue?logo=readthedocs)](https://attrisense.readthedocs.io)
[![CI](https://img.shields.io/badge/tests-passing-2E7D32?logo=githubactions)](#)

> **🛡️ Synthetic-data notice.** AttriSense ships with a **5,000-row
> fully synthetic** dataset generated programmatically and calibrated
> against published HR-attrition distributions. **No real employee
> data, no PII, no proprietary information** is included. The system
> is designed to be re-pointed at any HRIS (Workday, BambooHR, ADP).
>
> **🪪 Identification-bias notice.** The dashboard never displays raw
> employee IDs. Every record is shown as a salted **Review_ID**
> (`RV-NNNNNN`, see `production/src/attrisense/identity.py`). Reviewers
> who would otherwise anchor on memory ("oh, that's Ravi") see a
> deterministic pseudonym instead.
>
> **🎓 Origin.** MSBA capstone at California State University, East
> Bay. Generalised into the open-source AttriSense platform.
>
> **🤖 AI-use disclosure.** Built with LLM coding tools — see
> [`AI_CONTRIBUTIONS.md`](AI_CONTRIBUTIONS.md) for line-grain
> transparency.

---

## Five modalities, one dashboard

| # | Modality | What it answers | File |
|---|----------|-----------------|------|
| 1 | **RandomForest + SMOTE** | *Who is at risk right now?* | `production/scripts/train_retention_risk_model.py` |
| 2 | **Cox PH (lifelines)** | *When are they likely to leave?* | `production/scripts/train_cox_ph.py` |
| 3 | **T-Learner (EconML)** | *Which intervention helps THIS person?* | `production/src/attrisense/uplift.py` |
| 4 | **Multilingual RAG** | *What did similar leavers say?* — EN/ES/HI, OpenAI-first with hashing fallback | `production/src/attrisense/rag.py` |
| 5 | **NL→SQL** | *Ask the data lake in plain English* — LLM + TF-IDF gold-question fallback | `production/src/attrisense/nl_sql_fallback.py` |

Every prediction is gated by an EEOC four-fifths fairness audit
(`production/src/attrisense/fairness.py`).

---

## ⚡ Evaluate this project in 5 minutes

1. **See the live app** → [attrisense.streamlit.app](https://attrisense.streamlit.app) — no install
2. **Watch the 75-second demo** → [`docs/media/demo.mp4`](docs/media/demo.mp4)
3. **Skim the architecture** → [`docs/images/diagrams/architecture.png`](docs/images/diagrams/architecture.png)
4. **Read the IEEE paper** → [`paper/attrisense_ieee.pdf`](paper/attrisense_ieee.pdf) (7 pages, 4 tables, 1 algorithm)
5. **Read the Beginner's Guide DOCX** → [`outputs/AttriSense_Beginners_Guide.docx`](outputs/AttriSense_Beginners_Guide.docx) (~79 pages, offline-ready)
6. **Read the AI-use disclosure** → [`AI_CONTRIBUTIONS.md`](AI_CONTRIBUTIONS.md)

If you'd rather run it locally:

```bash
git clone https://github.com/Dogiparthi-Sharada/attrisense.git
cd attrisense
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make train      # ~2 min, deterministic seed=42
streamlit run production/streamlit_app.py
```

---
```

The block above adds **all five modalities**, the **Review_ID
identification-bias notice**, the **fairness gate**, and points at the
**7-page IEEE PDF** + **Beginner's Guide DOCX** (both freshly built).
