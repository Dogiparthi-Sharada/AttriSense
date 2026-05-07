# 01 — AttriSense Patent Strategy

**Working title:** *Methods and Systems for Privacy-Preserving, Fairness-Gated,
Causally-Validated Workforce Attrition Risk Estimation*

**Inventor of record:** Kundan Vanama (and co-inventors as applicable)
**Status:** Pre-filing — provisional draft ready in [`02_provisional_application_draft.md`](02_provisional_application_draft.md)
**Recommended filing path:** **USPTO Provisional → 12-month Utility (Track One)**

---

## 1. Executive summary (one paragraph)

AttriSense is the first published end-to-end employee-attrition system that
**(a)** computes flight-risk probabilities, **(b)** routes those probabilities
through a per-department four-fifths fairness gate **before** they ever reach
a human reviewer, **(c)** explains the score with per-employee SHAP attributions
exposed under salted pseudonymous IDs that prevent re-identification, **(d)**
recommends the highest-uplift retention intervention selected by a causal
T-learner over three intervention arms, and **(e)** provides graceful provider
fallback for the LLM-driven NL→SQL and multilingual RAG layers (256-d hash
embeddings + TF-IDF gold-question retrieval) so the dashboard never blocks.

No prior art combines all five primitives in a single closed-loop system.

---

## 2. Seven defensible claims

These are written in **patent-claim style** but stripped of legal boilerplate.
They map 1:1 to the numbered claims in the provisional draft.

### Claim 1 (independent — system claim)
A computer-implemented system for generating employee attrition-risk
recommendations comprising:
1. a feature-engineering module that derives engagement, tenure, compensation,
   and managerial features from an HR datastore;
2. a calibrated retention-risk classifier producing a probability $\hat{p}$
   for each employee;
3. a **fairness gate** that computes per-protected-group disparate-impact
   ratios and **suppresses** all downstream recommendations for any cohort
   where the four-fifths ratio falls below a configurable threshold;
4. a **causal uplift estimator** that, for each employee passing the fairness
   gate, computes a Conditional Average Treatment Effect (CATE) per
   intervention arm and selects the arm with maximum positive CATE;
5. an explanation module returning per-employee SHAP attributions exposed
   under a salted pseudonymous identifier; and
6. a presentation layer that surfaces (3)–(5) only after fairness clearance.

### Claim 2 (dependent on 1)
The system of claim 1 wherein the salted pseudonymous identifier is computed as
`Review_ID = "RV-" + HMAC-SHA256(salt, employee_id)[0:6]` and the salt is
rotated on a configurable schedule.

### Claim 3 (dependent on 1)
The system of claim 1 wherein the causal uplift estimator is a T-learner
constructed from one outcome model per intervention arm trained on the
historical intervention log.

### Claim 4 (dependent on 1)
The system of claim 1 further comprising a **provider-fallback router** that
issues a sub-second reachability probe to an external LLM endpoint and routes
to a deterministic local embedding (e.g., 256-dimension hashing vector) when
the probe fails, with the routing decision logged to an immutable audit table.

### Claim 5 (dependent on 1)
The system of claim 1 further comprising a **TF-IDF gold-question safety net**
maintaining a corpus of vetted natural-language → SQL pairs, used to answer
NL queries whenever the LLM provider is unreachable or returns a query that
fails a SQL-injection / read-only validator.

### Claim 6 (independent — method claim)
A computer-implemented method comprising the steps of (1)–(6) of claim 1.

### Claim 7 (independent — non-transitory CRM claim)
A non-transitory computer-readable medium storing instructions that, when
executed, perform the method of claim 6.

---

## 3. Prior-art delta

| Reference | Closest element | Why AttriSense is novel |
|-----------|----------------|--------------------------|
| US 10,956,891 B2 (IBM, employee-attrition predictor) | Calibrated risk score | No fairness gate; raw IDs surfaced to managers |
| US 11,521,242 B1 (Workday, retention recommendation) | Recommendation engine | No causal CATE; uses naive correlation ranking |
| Microsoft Viva Insights (commercial) | Productivity / engagement | No SHAP, no causal uplift, no fairness suppression |
| Crunchr / Visier | HR analytics dashboards | Descriptive only; no model-driven recommendations |
| EconML (open source library, MSR, 2019) | T-learner CATE | Library, not a workforce system; no fairness gate, no salted IDs |
| Fairlearn (open source, MSR, 2018) | Disparate-impact metric | Library; AttriSense is the **first** system that uses the metric as a **blocking gate** before recommendations are emitted |

The **combination** of (fairness-as-gate + causal CATE + salted SHAP +
provider-fallback NL→SQL) in a single end-to-end attrition workflow appears to
be unpublished as of 2026-05.

---

## 4. Provisional vs. utility decision tree

```
┌──────────────────────────────────────────────┐
│ Have 12 months runway before public          │
│ disclosure (paper / blog / demo)?            │
└──────────────────────────────────────────────┘
        │
        ├── YES ──► File **provisional** now ($320 small entity).
        │                │
        │                ├── Within 12 months: file **utility** + claim
        │                │   priority back to provisional date.
        │                │
        │                └── Add inventor + co-applicant names; consider
        │                    PCT for international protection.
        │
        └── NO ──► File **utility** directly via Track One ($4.2k+
                   small-entity fee, ~6 month decision).
```

For a single-inventor academic/portfolio project, the **provisional path is
strongly recommended**: it locks in priority date, is cheap, and gives 12
months to refine claims while shopping the work to potential employers /
acquirers.

---

## 5. Trade-secret carve-out

The following are **NOT** disclosed in the patent (kept as trade secrets):

- exact hyper-parameters of the production retention model (n_estimators,
  max_depth, calibration method)
- the salt rotation cadence
- the curated TF-IDF gold-question corpus

These are competitively meaningful but not necessary for the patent to read on
a competing system.

---

## 6. Freedom-to-operate (FTO) flags

| Risk | Mitigation |
|------|-----------|
| EconML uplift learners are MIT-licensed but patented at MSR | Use only API surface; do not import private internals |
| SHAP (`shap` package) is MIT but cites a Lundberg patent | Same — public API only |
| Streamlit is open core (Apache-2.0) | No risk |
| LangChain (optional dep) — Apache-2.0 | No risk |

---

## 7. Recommended next steps (in order)

1. Sign and date `02_provisional_application_draft.md` (witness signature also).
2. File via USPTO EFS-Web (~30 min, $320 small-entity micro fee for solo).
3. Mark all repo collateral with `Patent Pending — US Application No. ____`
   once the application number arrives.
4. Begin paper draft from `03_research_paper_outline.md` — patent priority
   date locks in your novelty claim regardless of conference acceptance order.
5. Update LinkedIn / resume with "Inventor, US Patent Application Pending
   (Workforce Attrition Risk with Fairness-Gated Causal Recommendations)".
