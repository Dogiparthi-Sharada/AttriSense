# Resume Bullets — Copy-Paste Ready (v2)

> 6 ATS-optimised bullets, refreshed for the 5-modality stack.
> Tuned for **AI Engineer / ML Engineer / Data Scientist /
> People-Analytics Analyst** roles. Drop into any standard
> "Projects" section.

---

## Project entry

**AttriSense — Open-Source Workforce Intelligence Platform**  *(MSBA Capstone, 2026)*
*Tech: Python · scikit-learn · imbalanced-learn (SMOTE) · lifelines (Cox PH) · EconML (T-Learner) · LangChain · OpenAI · FAISS · Streamlit · SQLite · Plotly · Playwright · LaTeX*

- Built an end-to-end **five-modality** retention platform: a Random Forest classifier with SMOTE rebalancing on a 5,000-employee synthetic corpus (**ROC-AUC 0.91 / PR-AUC 0.74**), a **Cox proportional-hazards** survival model (concordance 0.78) for time-to-attrition, an **EconML T-Learner** for per-employee causal uplift across three intervention arms, a **multilingual RAG** layer over EN/ES/HI exit-interview text with a hashing-based local fallback when the OpenAI endpoint is unreachable, and a **NL→SQL agent** with a TF-IDF gold-question safety net (50-question gold set).

- Designed and shipped an **interactive Streamlit dashboard** (Pixel-pastel UI, dark-axis charts, 7 themed tabs) with executive KPIs, SHAP-based per-employee driver decompositions, side-by-side employee comparisons, an EEOC four-fifths fairness audit that *gates* every recommendation before display, and a Slack/Teams alert mock — reducing analyst-mediated query latency from ~2 days to **under 12 seconds**.

- Implemented an **identification-bias mitigation** layer (`production/src/attrisense/identity.py`): every dashboard view replaces raw `Emp_ID` with a salted SHA-256 **Review_ID** (`RV-NNNNNN`, salt rotatable via `ATTRISENSE_REVIEW_ID_SALT`). Reviewers can no longer anchor on memory and bypass the model.

- Engineered a **resilient RAG provider fallback**: a 250 ms DNS + TCP + HTTPS reachability probe routes every embedding call to OpenAI when the network allows it and to local hashing embeddings (256-d, MD5-bucketed) when it does not. Per-provider FAISS index directories prevent dimension collisions.

- Authored an **IEEE-format conference paper** (7 pages, 4 tables, 1 algorithm, 25 references) covering the five-modality architecture, the production-hardening lessons (SMOTE-after-split, fairness gate, provider fallback), the per-arm CATE table, and the per-department fairness audit. Compiled with the IEEEtran class; arXiv preprint pending.

- **Open-sourced** the platform (MIT) including a deterministic synthetic-data generator (`seed=42`), a 79-page beginner's guide DOCX (`outputs/AttriSense_Beginners_Guide.docx`), a 15-slide Engineering-VP pitch deck, and a `mkdocs --strict` documentation site — explicitly aligned with NYC Local Law 144 bias-audit and EU AI Act high-risk-system documentation expectations.

---

## Skills additions

- **Languages:** Python · SQL · LaTeX
- **ML / AI:** scikit-learn · imbalanced-learn (SMOTE) · SHAP · pandas · NumPy
- **Causal & survival:** lifelines (Cox PH, KM) · EconML (T-Learner) · DoWhy
- **LLM / RAG:** LangChain · OpenAI API · FAISS · TF-IDF · provider fallback design
- **Data & UI:** SQLite · PostgreSQL · Plotly · Streamlit · Pillow (programmatic diagrams)
- **MLOps:** Git · GitHub Actions · Docker · Make · pytest · Playwright (visual regression)
- **Responsible AI:** fairlearn · EEOC four-fifths · model cards · NYC Local Law 144 · EU AI Act · pseudonymization (salted hash)

---

## LinkedIn "About" section

> *"MSBA candidate at Cal State East Bay, working at the intersection
> of business framing and applied AI. Built **AttriSense**, a
> five-modality open-source workforce-intelligence platform combining
> predictive ML, Cox PH survival, EconML causal uplift, multilingual
> RAG with provider fallback, and natural-language SQL — all gated
> behind an EEOC four-fifths fairness audit and a salted-hash
> Review_ID pseudonymization layer. 7-page IEEE paper, 79-page
> beginner's guide DOCX, and a public Streamlit demo. Open to
> AI Engineering / Applied ML / People-Analytics roles."*

---

## Cover-letter opening (drop-in for AI/ML roles)

> *"I'm an MSBA candidate at Cal State East Bay focused on shipping
> applied AI for business outcomes. My recent work — **AttriSense**,
> a five-modality open-source workforce-intelligence platform —
> combines RandomForest predictive flight risk (ROC-AUC 0.91), Cox PH
> survival modelling (concordance 0.78), EconML T-Learner causal
> uplift, multilingual RAG with a local hashing fallback, and an
> NL→SQL agent with a TF-IDF safety net. Every prediction is gated by
> an EEOC four-fifths fairness audit and pseudonymised with a salted
> Review_ID before display. The system reduces HR-query latency from
> days to seconds and is documented through a 7-page IEEE-style paper
> and a 79-page beginner's guide DOCX. I'm reaching out because
> [SPECIFIC THING ABOUT THE COMPANY] suggests a team that takes both
> shipping and rigour seriously, and that's the bar I want to work
> to."*

---

## Quick interview answers tied to the bullets

**"What's the most important thing you've built?"** — point at AttriSense and use the 90-second pitch in `05_interview_pitch_90s.md`.

**"What's a number you're proud of?"** — *"PR-AUC of 0.74 on a class with 10% prevalence. PR-AUC is more sensitive to imbalance than ROC, which matters for HR data. And concordance 0.78 on the Cox PH model — that's the survival side, which most HR-attrition systems skip."*

**"What's something you wish you'd done differently?"** — *"My first version reported only accuracy. I had 89% accuracy and was thrilled. My advisor pointed out that on a 10% positive class, that's near baseline. I rebuilt the evaluation around PR-AUC, calibration error, per-bucket recall, and a per-department fairness audit. Lesson: pick the metric that matches the cost of error, not the metric that flatters you."*

**"What's a real production hardening you did?"** — *"The RAG layer originally just called OpenAI. In a corporate-firewall trial it timed out and the dashboard hung. I added a 250 ms DNS + TCP + HTTPS reachability probe, a hashing-based local fallback, and per-provider FAISS index directories so 1536-d and 256-d vectors never collide. Now the dashboard never blocks on a third-party endpoint."*

**"How do you mitigate identification bias?"** — *"Every dashboard view replaces `Emp_ID` with a salted SHA-256 Review_ID — `RV-NNNNNN`. The salt is environment-rotatable. Reviewers can no longer anchor on memory ('oh, that's Ravi') and bypass the model."*

---

## Where to put these on the resume

1. **Top of resume**, first project under "Projects."
2. **Skills line** featuring `Cox PH · EconML · RAG fallback · NL→SQL · pseudonymization` — rare on student resumes; gets ATS hits.
3. **GitHub URL** linked from the resume header.
4. **Page count: 1.** Cut older projects. AttriSense is the headline.
