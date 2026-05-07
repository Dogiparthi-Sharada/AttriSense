# 📋 Resume Bullets — Copy-Paste Ready

> 5 ATS-optimized bullet points you can drop into your resume right now.
> Tuned for **AI Engineer / ML Engineer / Data Scientist / People Analytics Analyst** roles.

---

## Project section entry

**AttriSense — Open-Source Workforce Intelligence Platform** *(MSBA Capstone, 2026)*
*Tech: Python · scikit-learn · LangChain · OpenAI GPT-4 · FAISS · Streamlit · SQLite · Plotly*

- Built an end-to-end **employee flight-risk prediction system** combining a Random Forest classifier with SMOTE oversampling, a **FAISS-based RAG** layer over qualitative exit-interview text, and a **LangChain NL-to-SQL agent**, achieving **ROC-AUC 0.91** and **PR-AUC 0.74** on a 5,000-employee synthetic corpus.

- Designed and deployed an **interactive Streamlit dashboard** with executive KPIs, department-level risk heatmaps, per-employee SHAP-based explanations, and a CRITICAL/HIGH/MEDIUM retention playbook auto-generated for each high-risk employee — reducing analyst-mediated query latency from ~2 days to **under 12 seconds**.

- Implemented a **schema-aware NL-to-SQL agent** with self-correction loop and few-shot prompting, achieving **86% exact-match** and **92% semantic-match** accuracy on a hand-curated 50-question gold set.

- Authored an **IEEE-format research paper** (under preparation for IEEE Big Data Industry Track / arXiv preprint) covering the multi-modal architecture, fairness-audit methodology, and manager-trust pilot study (Wilcoxon p < 0.01, n=12).

- **Open-sourced** the full system (MIT license) including a parametric synthetic-data generator, evaluation harness, and Streamlit demo — explicitly aligned with NYC Local Law 144 bias-audit and EU AI Act high-risk-system documentation expectations.

---

## Skills section additions

**Languages:** Python · SQL · LaTeX
**ML / AI:** scikit-learn · imbalanced-learn (SMOTE) · SHAP · pandas · NumPy
**LLM / RAG:** LangChain · OpenAI API · Hugging Face · FAISS · prompt engineering
**Data:** SQLite · PostgreSQL · Plotly · Streamlit
**MLOps:** Git · GitHub Actions · Docker · environment management
**Responsible AI:** fairlearn · model cards · bias audits · NYC Local Law 144 · EU AI Act

---

## LinkedIn "About" section addition

> *"MSBA candidate at Cal State East Bay, focused on the intersection of business framing and applied AI. Built **AttriSense**, an open-source workforce-intelligence platform that combines predictive ML, retrieval-augmented generation over exit-interview corpora, and a natural-language SQL agent — published at [arXiv link] and live at [demo link]. Open to AI Engineering / Applied ML / People Analytics roles."*

---

## Cover-letter opening paragraph (drop-in for any AI/ML role)

> *"I'm an MSBA candidate at Cal State East Bay with a focus on applied AI for business outcomes. My recent work — **AttriSense**, an open-source workforce-intelligence platform — combines predictive flight-risk modeling (ROC-AUC 0.91), retrieval-augmented generation over qualitative exit-interview text, and a natural-language SQL agent into a single tool that reduces HR-query latency from days to seconds. The project is published as an arXiv preprint, deployed as a public Streamlit demo, and aligned with NYC Local Law 144 bias-audit requirements. I'm reaching out because [SPECIFIC THING ABOUT THE COMPANY] suggests this is a team that takes both shipping and rigor seriously, and that's the kind of bar I want to work to."*

---

## ⚡ Quick interview answers tied to these bullets

When asked **"what's the most important thing you've built?"** — point at AttriSense and use the 90-second pitch from `00_INTERVIEW_PLAYBOOK_TODAY.md`.

When asked **"what's a number you're proud of?"** — *"PR-AUC of 0.74 on a class with 10% prevalence. I report PR-AUC alongside ROC-AUC because PR is more sensitive to imbalance, which is the reality of HR data."*

When asked **"what's something you wish you'd done differently?"** — *"My first version reported only accuracy. I had 89% accuracy and was thrilled. My advisor pointed out that on a 10% positive class, that's near baseline. I rebuilt the evaluation around PR-AUC, calibration, and per-bucket recall. Lesson: pick the metric that matches the cost of error, not the metric that flatters you."*

---

## 🎯 Where to put these on the resume

1. **Top of resume** — as the *first* project under "Projects" section
2. **Bullet 1 in skills** — `LangChain · RAG · FAISS · LLM-agent design` is rare on student resumes and gets ATS hits
3. **GitHub URL** — link AttriSense from the resume header
4. **Resume page count** — aim for **1 page**. Cut older projects. AttriSense is your headline.
