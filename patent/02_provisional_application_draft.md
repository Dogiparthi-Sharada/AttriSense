<!--
AttriSense — patent/02_provisional_application_draft.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# 02 — Provisional Patent Application (Draft)

> **DRAFT — NOT YET FILED.** Replace `__INVENTOR__`, `__ADDRESS__`,
> `__DATE__` placeholders before filing via USPTO EFS-Web. Witness signature
> recommended on the final printed copy.

---

## TITLE OF INVENTION

**Methods and Systems for Privacy-Preserving, Fairness-Gated, Causally-Validated
Workforce Attrition Risk Estimation**

---

## CROSS-REFERENCE TO RELATED APPLICATIONS

None.

---

## STATEMENT REGARDING FEDERALLY SPONSORED RESEARCH

Not applicable.

---

## INVENTOR(S)

- __INVENTOR__ (Sharada Dogiparthi), residing at __ADDRESS__, citizen of
  __COUNTRY__.

---

## FIELD OF THE INVENTION

The present invention relates generally to human-resource analytics systems,
and more particularly to computer-implemented systems and methods for
estimating employee attrition risk in a manner that is privacy preserving,
group-fair, and causally validated, while exposing the resulting risk
attributions and recommended interventions to authorised reviewers through a
graceful, provider-fallback presentation layer.

---

## BACKGROUND OF THE INVENTION

Existing employee-attrition tools fall into three categories. *Descriptive*
dashboards (e.g., Visier, Crunchr, Microsoft Viva Insights) summarise
historical exits but do not predict future risk per employee. *Predictive*
systems (e.g., IBM Kenexa, Workday Predictive Attrition) emit a per-employee
risk score but typically (i) display the score against the raw employee
identifier, exposing the system to re-identification under role-based access,
(ii) recommend interventions based on correlation with past exits rather than
on a causally estimated treatment effect, and (iii) lack a blocking fairness
review prior to recommendation issuance. As a result, recommendations may
disparately impact protected groups, recommended interventions may have no
real causal lift, and reviewers may infer protected attributes from
identifiers.

A need therefore exists for an integrated system that (a) computes attrition
risk, (b) screens recommendations through a four-fifths disparate-impact gate
before they are surfaced, (c) selects interventions by per-employee
Conditional Average Treatment Effect (CATE), (d) exposes attributions under
salted pseudonymous identifiers that prevent re-identification, and (e)
degrades gracefully when external language-model providers are unreachable.

---

## SUMMARY OF THE INVENTION

The present invention provides a computer-implemented system, method, and
non-transitory computer-readable medium for generating fairness-gated,
causally-validated attrition-risk recommendations. In one embodiment, the
system comprises:

1. a feature-engineering module configured to derive engagement, tenure,
   compensation, and managerial features from an HR datastore;
2. a calibrated retention-risk classifier configured to produce, for each
   employee record, a probability $\hat{p}$ of voluntary exit within a
   configurable horizon;
3. a fairness-gate module configured to compute, for each protected-group
   cohort, a disparate-impact ratio relative to the highest-rate cohort, and
   to suppress all downstream recommendations for any cohort whose ratio
   falls below a configurable threshold (typically 0.80, the four-fifths
   rule);
4. a causal-uplift module configured to estimate, for each employee passing
   the fairness gate, a per-arm Conditional Average Treatment Effect using a
   T-learner constructed from one outcome model per intervention arm trained
   on a historical intervention log, and to select the arm with maximum
   positive CATE;
5. an explanation module configured to compute per-employee Shapley
   attributions of the risk score and to expose them under a salted
   pseudonymous identifier of the form
   `Review_ID = "RV-" + HMAC-SHA256(salt, employee_id)[0:6]`; and
6. a presentation module configured to surface the explanation and
   recommendation only after the fairness gate has cleared, and to fall back
   to a deterministic local embedding (e.g., 256-dimension hashing vector)
   and a TF-IDF gold-question corpus when external language-model providers
   are unreachable.

---

## BRIEF DESCRIPTION OF THE DRAWINGS

- **FIG. 1** — System block diagram showing the six modules and their data
  flow.
- **FIG. 2** — Fairness-gate decision logic (flow chart).
- **FIG. 3** — Causal T-learner architecture (one outcome model per arm).
- **FIG. 4** — Salted Review_ID derivation (sequence diagram).
- **FIG. 5** — Provider-fallback router (state machine).
- **FIG. 6** — Example dashboard surface (Executive tab).
- **FIG. 7** — Example dashboard surface (SHAP per-employee tab).
- **FIG. 8** — Example dashboard surface (Fairness audit tab with gate-fail
  cohort suppression).

(See `docs/images/*.png` for image source files; `docs/images/diagrams/`
contains the architectural figures.)

---

## DETAILED DESCRIPTION OF THE EMBODIMENTS

### Section A — Feature engineering (module 1)

The feature-engineering module reads an HR datastore (in one embodiment a
relational store such as SQLite, PostgreSQL, or BigQuery) and produces a
per-employee feature vector comprising at least: tenure in months,
month-over-month engagement-survey delta, compensation percentile within
department, manager tenure in months, manager-change count over a trailing
12-month window, and span-of-control. Categorical features are encoded via
ordinal or one-hot encoding as appropriate; missing values are imputed with
median (numeric) or mode (categorical).

### Section B — Calibrated retention-risk classifier (module 2)

The classifier in the preferred embodiment is a gradient-boosted decision
tree (e.g., XGBoost) wrapped in a Platt scaler or isotonic calibrator so that
the emitted score $\hat{p} \in [0,1]$ approximates a true probability of
voluntary exit within the configurable horizon (e.g., 12 months). The
training set is the historical exit log labelled by the organisation's
authoritative HRIS. The classifier persists as a `.joblib` artefact loaded
on dashboard cold-start.

### Section C — Fairness gate (module 3)

For each protected-group cohort $g \in G$ (in one embodiment: department,
gender, ethnicity, age band), the module computes
$$
DI(g) = \frac{P(\hat{y}=1 \mid \text{group}=g)}{\max_{g' \in G} P(\hat{y}=1 \mid \text{group}=g')}.
$$
If $DI(g) < \tau$ (default $\tau=0.80$, the four-fifths rule), the
recommendation pipeline for cohort $g$ is **suppressed** — that is, the
presentation layer renders neither the recommendation nor the SHAP attribution
for any employee in $g$, displaying instead a "fairness review pending" badge.
This is the **central novelty** of the invention: prior systems flag
disparate impact post-hoc; the present invention treats it as a **blocking
gate**.

### Section D — Causal uplift estimator (module 4)

For each intervention arm $a \in A$ (in one embodiment $A = \{
\text{compensation}, \text{manager rotation}, \text{learning budget} \}$),
the module trains an outcome model $\mu_a(x) = E[Y(a) \mid X=x]$ on the
historical intervention log. At inference time, for each employee $x_i$ that
has cleared the fairness gate, the module computes
$$
\widehat{CATE}_i(a) = \mu_a(x_i) - \mu_0(x_i)
$$
where $\mu_0$ is the no-intervention outcome model. The recommended arm is
$a^*_i = \arg\max_a \widehat{CATE}_i(a)$, surfaced only when
$\widehat{CATE}_i(a^*_i) > \delta$ for a configurable minimum-uplift
threshold $\delta$ (default 0.05).

### Section E — Salted pseudonymous identifier (module 5)

Each employee's true identifier is replaced at presentation time with
$$
\text{Review\_ID} = \text{``RV-''} \, \| \, \text{HMAC-SHA256}(\text{salt}, \text{employee\_id})[0:6]
$$
The salt is rotated on a configurable schedule (in one embodiment, monthly).
The mapping table is stored in an audit-only datastore inaccessible to
dashboard reviewers. SHAP attributions, recommended interventions, and any
exported audit logs reference only the Review_ID, preventing inference of the
employee's true identity from dashboard surfaces alone.

### Section F — Provider fallback presentation (module 6)

The dashboard issues a sub-second reachability probe (e.g., a 250 ms
HTTPS HEAD) to the configured external language-model provider. If the probe
fails, the natural-language-to-SQL surface routes the query to a TF-IDF
similarity match against a curated gold-question corpus; the multilingual
retrieval-augmented generation surface routes embeddings to a deterministic
local hashing vectoriser (in one embodiment 256-dimension). The routing
decision is logged with a timestamp and routing reason to an immutable audit
table. The reviewer's render path therefore never blocks on provider
availability.

---

## CLAIMS

The seven claims in [`01_patent_strategy.md`](01_patent_strategy.md) are
incorporated here by reference and reproduced verbatim:

> **1.** A computer-implemented system for generating employee
> attrition-risk recommendations comprising: a feature-engineering module …
> *(see strategy doc for full text of claims 1–7)*

---

## ABSTRACT (≤ 150 words)

A computer-implemented system, method, and non-transitory computer-readable
medium for generating employee attrition-risk recommendations. The system
estimates per-employee flight-risk probabilities, screens those probabilities
through a per-protected-group four-fifths disparate-impact fairness gate
before any recommendation is surfaced, selects the highest-uplift retention
intervention via a causal T-learner over multiple intervention arms, and
exposes per-employee Shapley attributions under salted pseudonymous
identifiers that resist re-identification. A provider-fallback router
maintains availability of the natural-language-to-SQL and multilingual
retrieval surfaces by routing to deterministic local embeddings and a
curated TF-IDF gold-question corpus when external language-model providers
are unreachable, ensuring the reviewer's render path never blocks.

---

## SIGNATURE

Signed by inventor: ____________________________ Date: __DATE__

Witnessed by: __________________________________ Date: __DATE__
