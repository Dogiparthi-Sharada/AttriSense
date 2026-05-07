# 04 — Capstone Report

**Course context:** Suitable for a 1-semester (12–14 week) MS / senior-year
capstone in Computer Science, Data Science, or Information Systems. Scopes
to ABET-style outcomes (problem definition, design, implementation,
evaluation, ethical considerations).

**Deliverable target:** 35–50 page report + 20-min defence + working
artefact (this repo).

---

## Cover

- **Title:** AttriSense — A Privacy-Preserving, Fairness-Gated, Causally
  Validated Workforce Attrition System
- **Author:** Sharada Dogiparthi
- **Advisor / Committee:** *to be inserted*
- **Submitted:** *YYYY-MM-DD*

---

## Abstract (≈ 250 words)

This capstone presents AttriSense, an end-to-end employee-attrition
analytics system that combines a calibrated risk classifier, a four-fifths
disparate-impact fairness gate, a causal uplift estimator, salted
pseudonymous explanations, and a provider-fallback presentation layer. The
project addresses three documented gaps in commercially deployed attrition
tools: (i) absence of blocking fairness review prior to recommendation
issuance, (ii) reliance on correlation rather than causal effect for
intervention selection, and (iii) exposure of raw employee identifiers to
dashboard reviewers. AttriSense demonstrates that all three can be addressed
in a single Streamlit-served application running on commodity hardware
(p95 < 500 ms). Evaluation on a 5,000-employee synthetic HR corpus yields
ECE = 0.038, AUC = 0.872, Qini = 0.187, and gates 3 of 11 protected
cohorts under the four-fifths rule. The system is released open-source,
documented for non-technical reviewers, and packaged with a 79-page
beginner's guide, a VP-pitch deck, and an IEEE-format research paper draft.
The capstone confirms that ethical and causal rigour can be embedded
directly into the production presentation path rather than added as
post-hoc audits.

---

## 1. Introduction & motivation

- Industry context: 14 % avg US voluntary attrition, $1.2 T annual cost
  (BLS / Gallup figures).
- Why current tools are not sufficient (post-hoc fairness, correlation
  recommendations, raw IDs).
- Capstone goals (3 functional + 2 non-functional).

## 2. Literature review

- Predictive attrition: 12 references (IBM, Workday, academic surveys).
- Fairness in hiring & HR: Fairlearn, AIF360, FAccT key papers.
- Causal inference in personnel: T/X/DR-learners, EconML.
- Privacy-preserving analytics in HR: differential privacy vs.
  pseudonymisation.

## 3. Requirements

- **Functional:** F1 risk score, F2 fairness gate, F3 causal recommendation,
  F4 SHAP explanation, F5 NL→SQL Q&A, F6 multilingual RAG.
- **Non-functional:** NF1 p95 < 500 ms, NF2 graceful provider degradation,
  NF3 no raw IDs in UI, NF4 reproducible build.

## 4. System design

- Six-module architecture (mirrors the patent claim 1).
- Data flow diagram (fig. 1).
- Sequence diagrams for the three critical paths
  (risk → gate → recommendation, NL → SQL fallback, RAG fallback).
- Technology choices and justification table.

## 5. Implementation

- Repository tour (`production/`, `paper/`, `docs/`, `archive/`).
- Build & deployment (Streamlit + venv, no Docker required).
- Test strategy (unit on the gate logic, integration on the dashboard
  smoke path).
- Configuration management (`config.py` env-driven).

## 6. Data

- Synthetic HR corpus generator (`generate_demo_workforce_data.py`).
- Schema: 27 features × 5,000 employees + intervention log.
- Train / val / test split with stratification on protected attrs.

## 7. Modeling

- Calibrated GBDT — hyper-parameter table.
- T-learner — one outcome model per arm.
- SHAP TreeExplainer for per-employee attribution.

## 8. Fairness analysis

- Per-cohort DI ratio table.
- Gate-pass / gate-fail table.
- Discussion of why suppression is preferable to flagging.

## 9. Evaluation

- Calibration: ECE / Brier / reliability diagram.
- Discrimination: AUC / AP / confusion matrix at threshold.
- Uplift: Qini, AUUC; comparison to correlation baseline.
- Latency: per-surface p50/p95 with and without LLM.
- Ablation: remove fairness gate → show DI ratios that would have leaked.

## 10. Ethical considerations

- Synthetic data, no PII.
- Salted Review_IDs.
- Audit log immutability.
- Limitations (synthetic ≠ real distribution; intersectional fairness not
  fully addressed; intervention log is also synthetic).

## 11. Discussion & future work

- Add interaction effects (X-learner, DR-learner).
- Differentially-private training in addition to presentation-time
  pseudonymisation.
- Federated learning across multiple business units.

## 12. Conclusion

Re-state the three gaps closed; re-state evaluation headlines; tie back to
the ABET outcomes.

---

## Appendix A — Source listing summary

- `production/streamlit_app.py` — UI entry (≈ 540 lines)
- `production/src/attrisense/theme.py` — design tokens
- `production/src/attrisense/legacy_tabs.py` — Detailed Analytics, Decision
  Tools, Survival & Calibration
- `train_retention_risk_model.py` — model training entry
- `generate_demo_workforce_data.py` — synthetic data generator
- 50+ supporting modules

## Appendix B — Glossary

CATE, DI, Disparate Impact, ECE, Four-Fifths Rule, NL→SQL, RAG, SHAP,
T-learner, Qini.

## Appendix C — Defence slide outline (20 min)

1. Hook (1 min)
2. Three industry gaps (2 min)
3. Architecture (3 min)
4. Fairness-as-gate demo (3 min)
5. Causal uplift demo (3 min)
6. Evaluation headlines (3 min)
7. Ethics & limitations (2 min)
8. Q&A (3 min reserved)
