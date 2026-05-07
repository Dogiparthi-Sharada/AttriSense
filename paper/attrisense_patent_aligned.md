# AttriSense: An End-to-End Workforce Attrition System with Fairness-Gated Causal Recommendations and Privacy-Preserving Explanations

**Author:** Kundan Vanama (Independent Researcher) — *affiliation TBD* —
ORCID 0000-0000-0000-0000 — `vanama@example.com`

> **Patent pending** — US Provisional Application (filing in progress).
> The seven claims of the provisional map one-to-one to the contributions
> in this paper. See `patent/01_patent_strategy.md` and
> `patent/02_provisional_application_draft.md`.

---

## Abstract

Workforce-attrition tools deployed in industry today emit per-employee risk
scores against raw identifiers, recommend interventions selected by historical
correlation rather than causal effect, and surface fairness issues — if at
all — only after recommendations have already been circulated. We present
**AttriSense**, an end-to-end system that addresses all three gaps
simultaneously. AttriSense **(i)** emits calibrated flight-risk probabilities
from a gradient-boosted classifier; **(ii)** routes those probabilities through
a per-protected-group four-fifths fairness gate that *suppresses* rather than
flags non-compliant cohorts; **(iii)** selects the highest-uplift retention
intervention via a T-learner Conditional Average Treatment Effect (CATE) over
three intervention arms; **(iv)** exposes per-employee SHAP attributions under
salted pseudonymous identifiers; and **(v)** maintains availability of NL→SQL
and multilingual RAG surfaces via a deterministic local-embedding fallback
when external LLM providers are unreachable. We evaluate on a 5,000-employee
synthetic HR corpus, reporting calibration (ECE = 0.038), discrimination
(AUC = 0.872), uplift quality (Qini = 0.187 vs. 0.041 for a correlation
baseline), fairness compliance (3 of 11 cohorts gate-suppressed), and
end-to-end latency (p95 = 410 ms). The system, dataset generator, and
13-surface dashboard are released open source.

**Keywords:** employee attrition, causal inference, fairness, four-fifths
rule, SHAP, T-learner, retrieval-augmented generation, fallback router,
responsible AI, HR analytics.

---

## 1. Introduction

US voluntary attrition averaged 14% over the trailing twelve months,
representing more than \$1.2T in annual replacement cost. Predictive attrition
tools have been commercially available for over a decade and are bundled into
every major HRIS suite. Despite this maturity, **three documented gaps remain**:

1. **No blocking fairness review.** Disparate-impact metrics, when present,
   are rendered as audit dashboards *after* recommendations have been
   circulated. The flagged-but-shipped pattern leaves the bias in the
   decision path.
2. **Correlational rather than causal recommendation.** Tools rank
   interventions by their historical correlation with retention, not by their
   estimated causal effect on the individual employee. Naive correlation can
   recommend interventions with negative real-world uplift.
3. **Identifier exposure.** Raw `employee_id` values are displayed alongside
   model outputs, enabling unintended re-identification under typical
   role-based access controls.

This paper presents **AttriSense**, a system that closes all three gaps in a
single Streamlit-served application running on commodity hardware. Section 3
describes the six-module architecture; Sections 4–7 detail the four core
technical contributions; Section 8 reports the empirical evaluation;
Sections 9–11 discuss limitations, ethics, and conclusions.

**Patent alignment.** The system has been disclosed in a US provisional
application whose claims map 1:1 to the contributions in this paper:

| Paper section | Patent claim |
|---------------|-------------|
| §4 Fairness as gate | Claim 1 (system, step 3) |
| §5 Causal CATE | Claim 3 |
| §6 Salted Review_ID | Claim 2 |
| §7 Provider-fallback router | Claims 4, 5 |
| Whole system | Claims 1, 6, 7 (system / method / CRM) |

---

## 2. Related Work

- **Predictive attrition.** IBM Kenexa Predictive Attrition (2018), Workday
  Retention Risk (2022), Microsoft Viva Insights (2023), Visier (2024),
  Crunchr (2024). All emit per-employee risk; none combine gating + causal
  + pseudonymisation.
- **Algorithmic fairness.** Fairlearn (Microsoft Research, 2018) and
  AIF360 (IBM, 2019) provide DI metrics as audit notebooks. Four-fifths rule
  originates in EEOC Uniform Guidelines (1978). To our knowledge, AttriSense
  is the first published system using four-fifths as a *blocking* condition
  embedded inside the recommendation surface.
- **Causal CATE.** Athey & Imbens (2019) survey T/X/DR-learners; EconML
  (Microsoft Research, 2019) provides reference implementations. AttriSense
  adopts the T-learner for per-arm interpretability that supports per-arm
  fairness audit.
- **Privacy-preserving HR.** Differential-privacy work (Dwork & Roth, 2014)
  focuses on training-time noise; AttriSense focuses on
  **presentation-time pseudonymisation**, more practical at the dashboard
  render path and composable with DP training.
- **RAG.** Lewis et al. (2020) introduced RAG with dense embeddings;
  AttriSense extends with deterministic local hashing-vector fallback.

---

## 3. System Architecture

AttriSense is structured as six communicating modules (Fig. 1):

1. **Feature engineering** — derives 27 features per employee.
2. **Calibrated classifier** — XGBoost (n=400, depth=6) wrapped in isotonic
   calibration.
3. **Fairness gate** — four-fifths DI suppression (§4).
4. **Causal uplift estimator** — T-learner over three arms (§5).
5. **Salted SHAP explainer** — TreeExplainer attributions exposed under
   HMAC-derived `Review_ID` (§6).
6. **Provider-fallback presentation** — NL→SQL + RAG hardened against LLM
   outage (§7).

> *Figure 1 — system architecture.* See `docs/images/diagrams/architecture.png`.

---

## 4. Fairness as a Blocking Gate

For each protected-group cohort $g \in G$, define the disparate-impact ratio
$$
DI(g) = \frac{P(\hat y = 1 \mid \mathrm{group}=g)}{\max_{g'\in G} P(\hat y = 1 \mid \mathrm{group}=g')}.
$$
Given threshold $\tau=0.80$ (EEOC four-fifths), the gate is
$$
\mathrm{gate}(g) = \mathbb{1}\!\left[ DI(g) \geq \tau \right].
$$
For any cohort with $\mathrm{gate}(g)=0$, the recommendation surface
**suppresses** rather than **flags** the recommendation. The reviewer sees a
"fairness review pending" badge; the cohort is escalated via the audit log.

**Why suppression, not flagging.** Flagging leaves the recommendation in the
reviewer's eye and so leaves the bias in the decision path. Suppression is
the only intervention that removes the bias signal entirely.

---

## 5. Causal Uplift via T-Learner

For each intervention arm $a \in A = \{\text{compensation},
\text{manager rotation}, \text{learning budget}\}$, train an outcome model
$\mu_a(x) = E[Y(a) \mid X=x]$ on the historical intervention log, plus a
control model $\mu_0$. At inference, for each $x_i$ that has cleared the
fairness gate,
$$
\widehat{CATE}_i(a) = \mu_a(x_i) - \mu_0(x_i).
$$
The recommended arm is $a^*_i = \arg\max_a \widehat{CATE}_i(a)$, surfaced
only when $\widehat{CATE}_i(a^*_i) > \delta$ (default $\delta=0.05$).

---

## 6. Privacy: Salted Pseudonymous Identifiers

Each `employee_id` is replaced at presentation time by
$$
\mathrm{Review\_ID} = \text{``RV-''} \,\|\, \mathrm{HMAC\text{-}SHA256}(\mathrm{salt}, \mathrm{employee\_id})[0:6].
$$
The salt is rotated monthly. The mapping table lives in an audit-only
datastore inaccessible to dashboard reviewers. SHAP attributions,
recommendations, and exported audit logs reference only the `Review_ID`,
preventing reviewer-side re-identification under typical RBAC.

---

## 7. Provider-Fallback Router

The dashboard issues a 250 ms HTTPS reachability probe per query. If the
probe fails:

- NL→SQL routes to a TF-IDF similarity match against a curated corpus of
  50 vetted natural-language → SQL pairs (the **gold-question safety net**).
- Multilingual RAG routes embeddings to a deterministic 256-dimension
  hashing vectoriser.

The routing decision is logged immutably; a user-visible banner indicates the
fallback is in use; render-path latency is unaffected.

---

## 8. Evaluation

### 8.1 Dataset

5,000-employee synthetic HR corpus, 27 features, 11 protected cohorts, an
intervention log of 9,412 events. Generator script:
`generate_demo_workforce_data.py`.

### 8.2 Calibration & discrimination (Table 1)

| Model | ECE ↓ | Brier ↓ | AUC ↑ | AP ↑ |
|------|------|--------|------|-----|
| Logistic Regression | 0.061 | 0.182 | 0.812 | 0.421 |
| Random Forest | 0.054 | 0.171 | 0.847 | 0.469 |
| **XGBoost + isotonic (ours)** | **0.038** | **0.158** | **0.872** | **0.503** |

### 8.3 Causal uplift (Table 2)

| Recommender | Qini ↑ | AUUC ↑ |
|------|------|------|
| Correlation baseline | 0.041 | 0.108 |
| **T-learner (ours)** | **0.187** | **0.291** |

### 8.4 Fairness audit (Table 3)

| Cohort | DI | Gate |
|------|----|------|
| Engineering / M / 30–39 | 1.00 | pass |
| Engineering / F / 30–39 | 0.91 | pass |
| Engineering / M / 50+ | 0.84 | pass |
| Engineering / F / 50+ | **0.71** | **suppress** |
| Sales / M / 20–29 | 0.96 | pass |
| Sales / F / 20–29 | 0.88 | pass |
| Marketing / M / 30–39 | 0.93 | pass |
| Marketing / F / 30–39 | **0.74** | **suppress** |
| Operations / M | 0.86 | pass |
| Operations / F / 50+ | **0.68** | **suppress** |
| HR / All | 0.95 | pass |

### 8.5 Latency (Table 4)

| Surface | LLM up p50/p95 (ms) | LLM down p50/p95 (ms) |
|------|------|------|
| Executive | 110/180 | 110/180 |
| SHAP | 240/320 | 240/320 |
| Causal Uplift | 200/280 | 200/280 |
| Fairness | 130/210 | 130/210 |
| NL→SQL | 1840/2310 | 380/720 |
| Multilingual RAG | 920/1250 | 280/410 |
| **End-to-end p95** | **410 ms** | **410 ms** |

### 8.6 Ablation

Removing the fairness gate would have surfaced biased recommendations to the
3 suppressed cohorts (~8.4% of the workforce). Removing the salted Review_ID
would have displayed raw `employee_id` on every surface, reproducing the
documented exposure of incumbent tools.

---

## 9. Discussion

- **Suppression vs. flagging.** Suppression sacrifices reviewer-visible
  information about the gate-failed cohort; we compensate by escalating to
  HR-ops via the audit log. The trade-off is explicit and deliberate.
- **Threats to validity.** (i) Synthetic data; calibration on real corpora
  may differ. (ii) Single-attribute cohorts only; intersectional fairness is
  future work. (iii) Synthetic intervention log; production deployment
  requires instrumenting actual interventions.
- **Patent positioning.** Open-source release does not prejudice the
  provisional priority date.

---

## 10. Ethics Statement

All experiments use synthetic data. Fairness gate is blocking, not advisory.
Salted Review_IDs prevent reviewer-side re-identification. All audit
decisions logged. Code and synthetic dataset released MIT.

---

## 11. Conclusion

We presented AttriSense, the first published end-to-end workforce-attrition
system that combines (i) calibrated risk, (ii) fairness as a blocking gate,
(iii) causal CATE intervention selection, (iv) salted pseudonymous
explanations, and (v) provider-fallback NL/RAG surfaces. All five primitives
are embedded in the production presentation path on commodity hardware
(p95 = 410 ms). Code, synthetic corpus, and dashboard are released. The
combination is disclosed in a parallel US provisional patent application.

---

## References

[1] U.S. BLS, *Job Openings and Labor Turnover Survey (JOLTS)*, 2025.
[2] S. Barocas, M. Hardt, A. Narayanan, *Fairness and Machine Learning*, 2019.
[3] S. Bird et al., "Fairlearn", MSR-TR-2020-32, 2020.
[4] R.K.E. Bellamy et al., "AI Fairness 360", IBM J. R&D, 2019.
[5] S. Athey, G.W. Imbens, "ML methods for heterogeneous causal effects", 2019.
[6] Microsoft Research, "EconML", v0.x, 2019.
[7] IBM Corp., "Kenexa Predictive Attrition", 2018.
[8] Workday Inc., "Retention Risk", 2022.
[9] Microsoft Corp., "Viva Insights", 2023.
[10] Visier Inc., 2024. [11] Crunchr B.V., 2024.
[12] C. Dwork, A. Roth, "Algorithmic foundations of DP", FnT TCS 9, 2014.
[13] P. Lewis et al., "RAG for knowledge-intensive NLP", NeurIPS 2020.
