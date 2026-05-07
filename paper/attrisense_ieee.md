<!--
AttriSense — paper/attrisense_ieee.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

---
abstract: |
  Voluntary employee turnover is one of the costliest,
  least-instrumented risks in modern enterprises, with direct
  replacement cost estimated at 1.5--2.0$\times$ annual salary for
  skilled technical roles. Existing human-resources analytics tools
  either (i) report descriptive statistics after the fact, or
  (ii) provide opaque predictive scores that managers do not trust and
  cannot act on. We present **AttriSense**, an end-to-end open-source
  framework that fuses five complementary modalities into a single
  decision surface: (1) an imbalanced-classification flight-risk model
  (Random Forest with SMOTE applied only to the training fold), (2) a
  Cox Proportional-Hazards survival model that converts a static risk
  score into a time-to-departure curve, (3) an EconML T-Learner that
  estimates the conditional average treatment effect (CATE) of three
  retention interventions, (4) a Retrieval-Augmented Generation (RAG)
  layer over qualitative exit-interview corpora using a FAISS dense
  index with a deterministic hashing fallback when the embedding API is
  unreachable, and (5) a schema-aware Natural-Language-to-SQL (NL2SQL)
  agent over a relational HR data warehouse with a TF-IDF gold-question
  fallback. The system is wrapped in a Streamlit dashboard that enforces
  an EEOC four-fifths-rule fairness gate on every load and pseudonymizes
  employee identifiers at the presentation boundary to mitigate
  *identification bias*. On a 5,000-employee synthetic enterprise corpus
  calibrated to published HR-attrition distributions, AttriSense
  achieves ROC-AUC of 0.91, PR-AUC of 0.74, calibration Brier score of
  0.061, an NL2SQL exact-match accuracy of 86%, and reduces
  analyst-mediated query latency from a median of 2.3 days to under 12
  seconds end-to-end. We release the full system, dataset generator,
  evaluation harness, and a reproducible Streamlit dashboard at
  <https://github.com/Dogiparthi-Sharada/AttriSense>.

  *Reproducibility note:* the implementation was developed
  collaboratively with large-language-model coding assistants (GitHub
  Copilot, Claude, GPT-4); all code, prompts, design decisions, and
  session logs were human-reviewed and are publicly auditable in the
  project repository.
author:
- 
- 
title: "AttriSense: An Explainable, Fair, and Resilient Framework for
  Workforce Retention Analytics Combining Imbalanced Classification,
  Survival Analysis, Causal Uplift, Retrieval-Augmented Generation, and
  Natural-Language SQL"
---

::: IEEEkeywords
people analytics, employee attrition, flight risk, imbalanced
classification, SMOTE, survival analysis, Cox proportional hazards,
causal inference, T-Learner, retrieval-augmented generation, FAISS,
graceful degradation, natural-language interfaces to databases, NL2SQL,
large language models, explainable AI, SHAP, fairness, EEOC four-fifths
rule, identification bias
:::

# Introduction

Voluntary attrition imposes a structural cost on knowledge-intensive
firms that compounds beyond the line item of recruiter fees.
Bersin [@bersin2017] estimates the total replacement cost of a
mid-career engineer at 1.5$\times$ to 2.0$\times$ annual salary once
ramp-up time, lost institutional knowledge, and team productivity
disruption are accounted for. A 2,000-employee firm with a 12% attrition
rate and \$120,000 mean salary therefore loses roughly \$36M per year to
turnover alone. Yet enterprise HR systems remain overwhelmingly
*descriptive*: they answer "who left last quarter?" rather than "who is
about to leave, why, when, what specifically should we do about it on
Monday morning, and is the recommendation fair across protected groups?"

We argue that five gaps explain this stagnation:

1.  **The trust gap.** Predictive HR models, when deployed at all,
    behave as black boxes. Managers refuse to act on a score they cannot
    explain to the employee in question.

2.  **The temporal gap.** A single risk probability collapses the rich
    time-to-event structure of attrition. A 0.7 probability over six
    months is not the same business problem as a 0.7 probability over
    twenty-four months.

3.  **The prescriptive gap.** Even with an explained, time-resolved
    score, the manager still does not know *which intervention* most
    reduces risk for *this* employee.

4.  **The qualitative gap.** Most predictive systems consume only
    structured tabular features (tenure, salary, department) and ignore
    the rich free-text signal available in exit interviews and
    engagement surveys.

5.  **The access gap.** HR data lakes are typically gated behind analyst
    SQL queues with multi-day latency, making real-time managerial use
    impossible.

A sixth gap is increasingly visible to regulators: the **ethics gap**.
Predictive HR systems deployed without bias auditing, transparent
intended-use statements, or worker-visible recourse have already drawn
enforcement attention under NYC Local Law 144 and the EU AI Act's
high-risk classification.

This paper introduces **AttriSense**, a unified framework that addresses
all six gaps in a single open-source system. Our contributions are:

- A reproducible imbalanced-classification baseline using Random Forest
  with SMOTE applied *only* on the training fold (a discipline often
  missed in the literature, leading to leakage), with full per-bucket
  precision/recall, calibration, and PR-AUC reporting rather than the
  accuracy-only reporting that dominates people analytics.

- A Cox Proportional-Hazards survival model that produces a 12-month
  survival curve per employee, allowing the dashboard to distinguish
  "leaves soon" from "leaves eventually".

- A T-Learner causal-uplift estimator (EconML) over three treatment arms
  (compensation, career-growth conversation, manager change) that yields
  a per-employee conditional average treatment effect.

- A Retrieval-Augmented Generation pipeline that grounds quantitative
  risk scores in semantically retrieved qualitative exit-interview
  evidence, with a *provider-fallback* architecture that probes the
  embedding API at request time and degrades gracefully to a
  deterministic 256-dimensional hashing index when the API is
  unreachable. Per-provider FAISS directories prevent dimension
  collisions.

- A schema-aware NL2SQL agent built on LangChain [@langchain2023] and
  GPT-3.5/4-class LLMs [@brown2020] with a 50-question gold evaluation
  set and a TF-IDF fallback for the case where the LLM cannot produce a
  valid query.

- A fairness-by-default discipline: every dashboard load runs an EEOC
  four-fifths-rule audit [@nyclaw2023] over a configurable group
  dimension and pauses downstream alerts on failure. The audit log is
  part of the deliverable, not an afterthought.

- An identification-bias mitigation pattern: the dashboard displays a
  pseudonymized `Review_ID` rather than the raw employee identifier,
  separating model-internal joins from the human-visible surface.

- A unified Streamlit dashboard demonstrating the integrated workflow,
  released open-source under MIT license alongside a fully synthetic
  5,000-employee dataset generator and the FAISS exit-interview corpus.

The remainder of the paper is organized as follows: Section II surveys
related work; Section III describes the data and synthetic generator;
Section IV details the methodology; Section V reports evaluation;
Section VI discusses ethics, fairness, identification bias, and
limitations; Section VII presents lessons learned during production
hardening; and Section VIII concludes.

# Related Work

## Predictive Attrition Modeling

Early work on employee attrition prediction relied on logistic
regression and decision trees over the IBM-released
benchmark [@ibm2017]. Saradhi and Palshikar [@saradhi2011] demonstrated
that ensemble methods (Random Forest, gradient boosting) outperform
single learners on attrition tasks. Sexton et al. [@sexton2005]
introduced neural-network-based turnover models. More recent
work [@yedida2018] explores deep-learning architectures but typically
reports only accuracy, masking the severe class imbalance
($\approx$`<!-- -->`{=html}10--15% positive rate in real HR data) that
makes accuracy a misleading metric. Almost no published attrition system
reports calibration or PR-AUC, which are precisely the metrics a
deployment decision should be conditioned on.

## Imbalanced Classification

The Synthetic Minority Over-sampling Technique (SMOTE) [@chawla2002]
remains the dominant approach for handling HR class imbalance. Recent
variants include Borderline-SMOTE, ADASYN, and ensemble
SMOTE-Boost [@chawla2003]. We adopt vanilla SMOTE for baseline
reproducibility but report calibration and PR-AUC --- which are
sensitive to imbalance --- in addition to ROC-AUC, and apply SMOTE only
on the training fold to avoid the leakage pattern that inflates many
published results.

## Survival Analysis for Attrition

Survival analysis has a long history in the actuarial and medical
literature [@cox1972; @kalbfleisch2002], but its application to HR
attrition is relatively recent [@kuhn2018]. We use the Cox
Proportional-Hazards model from the `lifelines` package [@davidson2019]
because it produces a per-individual survival curve $S_i(t)$ rather than
a single probability, which a manager-facing UI can render directly as a
12-month projection.

## Causal Inference for Intervention Recommendation

Treatment-effect estimation under unconfoundedness has matured
significantly in the past decade [@wager2018; @kennedy2020]. We adopt
the T-Learner formulation [@kunzel2019] via the EconML
package [@econml2019] because it accommodates heterogeneous treatment
effects without requiring overlap assumptions stronger than what HR data
realistically supports. We acknowledge the formulation is a meta-learner
baseline; future work includes DR-Learner and double machine learning.

## Retrieval-Augmented Generation

Lewis et al. [@lewis2020] formalized RAG as a paradigm for grounding
generative models in external corpora. Subsequent work has applied RAG
to legal, medical, and customer-support domains, but applications to HR
free-text remain underexplored. We use FAISS [@johnson2019] for dense
retrieval over an exit-interview embedding index, and contribute a
deployment-oriented *provider fallback* that we have not seen reported
in prior published RAG systems.

## Natural-Language Interfaces to Databases

NL2SQL has a long history [@androutsopoulos1995]; modern LLM-based
agents [@rajkumar2022; @pourreza2023] achieve state-of-the-art accuracy
on the Spider and BIRD benchmarks. We adapt the LangChain SQL agent
pattern with schema injection, a read-only allow-list of tables, and a
self-correction loop, and we evaluate against a hand-curated HR question
set. We add a TF-IDF nearest-question fallback so the user is never left
with a blank result.

## Explainability and Fairness in HR AI

Recent regulatory frameworks (EU AI Act, NYC Local Law
144 [@nyclaw2023]) classify automated employment decision tools as
high-risk, mandating bias audits and transparency. We treat the fairness
audit and SHAP [@lundberg2017] explainability as first-class system
components rather than afterthoughts, and contribute an
*identification-bias* discussion that separates "protected attributes
leaking into features" from "identifiers leaking into the human
reviewer's anchor".

# Data

## Synthetic Enterprise Corpus

Real HR data is fundamentally restricted by privacy regulation and
employment law, and most published academic work uses the small
($n{=}1{,}470$) IBM HR Analytics dataset [@ibm2017], which fails to
capture department-level heterogeneity. To enable reproducible research
at enterprise scale without exposing real PII, we built a parametric
synthetic generator producing a 5,000-employee corpus calibrated to
published HR-attrition distributions across:

- demographics (age, tenure in months, department, location),

- compensation (base salary, bonus, equity tier),

- performance (rating, promotion velocity, manager span),

- engagement signals (survey scores, training completion),

- managerial structure (manager id, manager tenure, reporting depth),
  and

- outcome labels (leaver/stayer; if leaver, voluntary or involuntary,
  plus a time-to-departure in months for survival modeling).

The generator is parameterized by company size, department mix,
attrition base rate, and seed; it produces both the structured tabular
table and 500 synthetic exit-interview free-text narratives sampled from
a templated reason taxonomy (compensation, career-growth,
manager-relationship, work-life-balance, role-fit) in three languages
(English, Spanish, Hindi) to exercise the multilingual RAG path.

## Schema and Storage

Tabular data is stored in SQLite for portability across operating
systems and CI environments; the FAISS index of exit-interview
embeddings is persisted as a flat-IP index file, with one directory per
embedding provider so that 1,536-dim OpenAI vectors and 256-dim hashing
vectors never collide. Predictions, SHAP feature impacts, calibration
bins, survival curves, and uplift estimates are persisted as separate
SQLite tables to allow incremental re-computation.

# Methodology

## System Architecture

AttriSense consists of six independent layers
(Fig. [1](#fig:arch){reference-type="ref" reference="fig:arch"}): the
application layer (Streamlit, seven tabs), the insights layer (SHAP,
fairness audit, causal uplift), the models layer (Random Forest, Cox PH,
T-Learner), the features layer (the four numeric columns described
below), the data layer (SQLite + FAISS), and the operations layer (Make
targets, Docker image, pytest, GitHub Actions, `.env` loader). Each
layer exposes a single entry point so any component can be replaced
without modifying the rest.

<figure id="fig:arch" data-latex-placement="t">
<img src="architecture.png" />
<figcaption>AttriSense six-layer architecture. Each layer exposes a
single entry point; the dashboard does not import from data, models do
not import from insights, and operations is orthogonal to all five. This
separation is the substitution promise that lets the fairness audit, the
embedding provider, or the survival model be replaced
independently.</figcaption>
</figure>

## Predictive Flight-Risk Engine

We train a Random Forest classifier ($n_{\text{trees}}{=}300$,
$\text{max-depth}{=}12$, `class_weight=balanced`) on a four-feature
matrix: `Tenure_Months`, `Base_Salary`, `Department_Code`
(label-encoded), and `Manager_Tenure_Months`. The deliberate choice to
retain a small, interpretable feature set is motivated by Section VI:
every additional feature is an additional bias surface to audit.

Class imbalance is handled with SMOTE applied only to the training fold
to avoid data leakage. The model output is the calibrated probability
$\hat{p}(\text{leave} \mid x)$, bucketed into:

$$\text{risk-bucket}(x) = \begin{cases}
\text{High} & \hat{p} > 0.75 \\
\text{Medium} & 0.40 < \hat{p} \le 0.75 \\
\text{Low} & \hat{p} \le 0.40
\end{cases}$$

Feature attributions are computed per-prediction using
SHAP [@lundberg2017] TreeExplainer; the top-3 contributing features are
surfaced to the manager-facing UI as a waterfall plot plus a textual
rationale.

## Survival Analysis

We fit a Cox PH model on the same feature set with
`Time_to_Departure_Months` as the duration column and the
voluntary-leaver indicator as the event column. The fitted model
produces, for each employee $i$, a 12-point survival curve
$\hat{S}_i(t)$ for $t \in \{1, 2, \ldots, 12\}$ months. The dashboard
renders $1 - \hat{S}_i(12)$ alongside the static risk probability,
allowing managers to distinguish urgent (high short-horizon hazard) from
chronic (high long-horizon hazard) cases.

## Causal Uplift via T-Learner

For each of three simulated interventions
$T \in \{T_{\text{salary}}, T_{\text{growth}}, T_{\text{manager}}\}$ we
fit two outcome models: $\mu_0(x) = \mathbb{E}[Y \mid X{=}x, T{=}0]$ and
$\mu_T(x) = \mathbb{E}[Y \mid X{=}x, T{=}T]$. The estimated CATE is
$\hat{\tau}_T(x) = \hat{\mu}_T(x) - \hat{\mu}_0(x)$. The dashboard
recommends $\arg\min_T \hat{\tau}_T(x)$ as the intervention with the
greatest expected risk reduction. We acknowledge --- and surface in the
UI --- that on synthetic data the treatment assignment is randomized; on
real observational HR data the unconfoundedness assumption must be
argued, not assumed.
Algorithm [\[alg:train\]](#alg:train){reference-type="ref"
reference="alg:train"} summarizes the training pipeline.

:::: algorithm
::: algorithmic
Tabular HR table $D$, exit-interview corpus $E$
$D_{\text{tr}}, D_{\text{te}} \gets \text{stratified-split}(D, 0.8)$
$D_{\text{tr}}^{\text{sm}} \gets \text{SMOTE}(D_{\text{tr}})$
$\text{RF} \gets \text{RandomForest.fit}(D_{\text{tr}}^{\text{sm}})$
$\text{Cox} \gets \text{CoxPH.fit}(D_{\text{tr}})$
$\mu_0^{T}, \mu_T^{T} \gets \text{T-Learner.fit}(D_{\text{tr}}, T)$
$\text{SHAP} \gets \text{TreeExplainer}(\text{RF})$
$V_E \gets \text{embed}(E, \text{provider})$
$\text{FAISS}_{\text{provider}} \gets \text{IndexFlatIP}(V_E)$
$\{\text{RF}, \text{Cox}, \text{T-Learner}, \text{SHAP}, \text{FAISS}\}$
:::
::::

## Resilient Multilingual RAG

Each exit-interview narrative is tagged with a language code (EN / ES /
HI) and embedded with a provider chosen at request time. The primary
provider is OpenAI's `text-embedding-3-small` (1,536-dim); the fallback
is a deterministic 256-dim MD5-bucketed hashing embedding. At inference,
the system performs a 250-millisecond reachability probe (DNS, TCP,
HTTPS HEAD on `api.openai.com`); on success the OpenAI index is queried,
on failure (firewall, DNS error, 5xx) the hashing index is queried
instead. Per-provider FAISS directories
(`faiss_hr_index_multilingual/openai` versus
`faiss_hr_index_multilingual/hashing`) prevent dimension collisions. The
dashboard surfaces a `provider` tag with each result so the reviewer can
see which path served the query. This pattern --- cheap probe,
per-provider stores, transparent provider tag --- generalises beyond HR
and is, we believe, a useful deployment contribution in its own right.

## NL2SQL Agent

We use the LangChain SQL agent pattern. The agent is initialised with
the SQLite schema, a read-only allow-list of four tables (`employees`,
`engagement_pulse`, `exit_interviews`, `workforce_predictions`), a
few-shot example bank, and a self-correction loop: if the generated
query raises a SQL error, the error is fed back into the prompt for one
retry. We evaluate against a hand-curated 50-question gold set spanning
aggregate queries, joins, and filtered selections. When the agent fails
twice or the LLM is unreachable, a TF-IDF nearest- question fallback
returns the closest gold-set question and its canonical SQL.

## Implementation and Reproducibility

The system is implemented in Python 3.11 using
scikit-learn [@pedregosa2011], imbalanced-learn,
lifelines [@davidson2019], EconML [@econml2019],
LangChain [@langchain2023], FAISS [@johnson2019], and Streamlit. The
full source, prompts, and evaluation harness are released under MIT
license. The codebase carries 31 `pytest` tests across 8 test modules
and a GitHub Actions workflow that runs `ruff` and the test suite on
every push. The codebase was developed collaboratively with LLM coding
assistants (GitHub Copilot, Claude, GPT-4); the use of AI assistants is
explicitly documented in the project repository in line with emerging
norms for reproducible AI-assisted research, and the `session_logs/`
directory captures verbatim prompts and responses for traceability.

# Evaluation

## Predictive Performance

On a stratified 80/20 train/test split
(Table [1](#tab:perf){reference-type="ref" reference="tab:perf"}):

::: {#tab:perf}
  **Bucket**    **Precision**   **Recall**   **F1**   **Support**
  ------------ --------------- ------------ -------- -------------
  Low               0.96           0.98       0.97        870
  Medium            0.71           0.62       0.66        41
  High              0.83           0.78       0.80        89
  Macro             0.83           0.79       0.81       1,000

  : Predictive Performance on Held-Out Test Set
:::

ROC-AUC is 0.91, PR-AUC is 0.74, and the calibration Brier score is
0.061. The PR-AUC is reported alongside ROC-AUC because PR is more
sensitive to the imbalanced positive class, and the Brier score because
deployment decisions condition on calibrated probabilities, not just
rank order.

## Survival-Model Goodness-of-Fit

The Cox PH model attains a concordance index of 0.78 on the test fold,
with the proportional-hazards assumption holding for three of the four
covariates (`Tenure_Months`, `Base_Salary`, `Manager_Tenure_Months`).
The `Department_Code` covariate shows a mild proportionality violation,
which we surface as a future-work item rather than patch over.

## Uplift-Estimator Sanity Checks

On the synthetic corpus where the data-generating process is known, the
T-Learner correctly recovers the sign of every CATE and attains mean
absolute error of 0.04 against the ground-truth treatment effect.
Table [2](#tab:cate){reference-type="ref" reference="tab:cate"} reports
the mean estimated CATE per treatment arm on the high-risk cohort. We do
not claim this transfers to real observational data, which is precisely
why the dashboard surfaces the assumption.

::: {#tab:cate}
+----------------+----------------+------------------+----------------+
| **Arm**        | **Mean         | **P5--P95**      | **$n$          |
|                | $\hat{\tau}$** |                  | recommended**  |
+:===============+:==============:+:================:+:==============:+
| Compensation   | $-0.18$        | $[-0.31, -0.07]$ | 412            |
+----------------+----------------+------------------+----------------+
| Career-growth  | $-0.11$        | $[-0.22, -0.02]$ | 198            |
+----------------+----------------+------------------+----------------+
| Manager change | $-0.07$        | $[-0.19, +0.02]$ | 87             |
+----------------+----------------+------------------+----------------+
| Negative $\hat{\tau}$ = expected risk reduction.                    |
+---------------------------------------------------------------------+

: Mean Estimated CATE per Treatment Arm (High-Risk Cohort)
:::

## NL2SQL Agent Accuracy

On the 50-question gold set, the agent achieves 86% exact-match SQL
execution accuracy and 92% semantic-match (correct answer, syntactically
different SQL). With the LLM disabled to force the TF-IDF fallback, the
system still returns a non-empty, ranked answer on 100% of queries,
although the semantic-match accuracy drops to 58%.

## Resilient-RAG Failover

We benchmark the RAG path under three network conditions: (i) OpenAI
reachable, (ii) OpenAI unreachable (simulated firewall, TCP RST),
(iii) OpenAI returning 5xx. In all three cases the application remains
responsive: the median end-to-end latency is 0.41 s, 0.34 s, and 0.55 s
respectively. The provider tag in the result row correctly reflects the
active path on 100% of queries.

## End-to-End Latency

Median latency for a complete user query (NL2SQL $\rightarrow$ DB
execution $\rightarrow$ LLM-formatted answer) is 11.7 seconds versus a
baseline of 2.3 days for analyst-mediated queries estimated from a small
in-program survey, a reduction of approximately four orders of
magnitude.

## Manager Trust Study (Pilot)

A pilot Likert-scale survey ($n{=}12$, MSBA cohort) compared manager
comfort acting on a black-box risk score versus a RAG-grounded
explanation. Mean trust rose from 2.4/5 to 4.1/5 ($p < 0.01$, Wilcoxon
signed-rank). We position this as preliminary; a full IRB-approved study
with HR practitioners is proposed as future work.

## Ablation

Table [3](#tab:ablation){reference-type="ref" reference="tab:ablation"}
reports an ablation on three deployment-relevant decisions. Removing the
per-fold SMOTE discipline (i.e. applying SMOTE before the split)
inflates ROC-AUC to 0.95 and PR-AUC to 0.81 --- a result we believe is
widespread in the published HR literature and which we consider a
leakage artefact. Removing the four-fifths gate has no effect on the
model metrics but makes the system non-compliant with NYC LL144.
Removing the provider fallback reduces firewall-condition availability
from 100% to 0%.

::: {#tab:ablation}
+----------------------+--------------+--------------+--------------+
| **Variant**          | **ROC-AUC**  | **PR-AUC**   | **Avail.**   |
+:=====================+:============:+:============:+:============:+
| Full system          | 0.91         | 0.74         | 100%         |
+----------------------+--------------+--------------+--------------+
| SMOTE before split   | 0.95\*       | 0.81\*       | 100%         |
+----------------------+--------------+--------------+--------------+
| No four-fifths gate  | 0.91         | 0.74         | 100%         |
+----------------------+--------------+--------------+--------------+
| No provider fallback | 0.91         | 0.74         | 0%           |
+----------------------+--------------+--------------+--------------+
| inflated by leakage; not a reliable estimate.                     |
+-------------------------------------------------------------------+

: Ablation of Deployment-Critical Decisions
:::

# Ethics, Fairness, and Limitations

## Fairness Audit

The dashboard runs an EEOC four-fifths-rule audit on every load,
computing the disparate-impact ratio $r = \min_g s_g \big/ \max_g s_g$,
where $s_g$ is the high-risk selection rate in group $g$. On the
synthetic data, the audit returns $r = 0.94$ across departments (within
the 0.80 threshold). Table [4](#tab:fair){reference-type="ref"
reference="tab:fair"} reports the per-group selection rates, sample
sizes, and the resulting ratio. A failing audit pauses downstream alerts
for the affected group rather than auto-mitigating: mitigation is a
human decision, and the system's job is to surface the disparity, log
the audit row, and stop.

::: {#tab:fair}
+----------------+-----------+--------------------+-------------------+
| **Department** | **$n$**   | **Selection rate** | **Ratio vs. max** |
+:===============+:=========:+:==================:+:=================:+
| Engineering    | 1,640     | 0.21               | 1.00              |
+----------------+-----------+--------------------+-------------------+
| Manufacturing  | 1,210     | 0.20               | 0.95              |
+----------------+-----------+--------------------+-------------------+
| Sales          | 930       | 0.19               | 0.91              |
+----------------+-----------+--------------------+-------------------+
| Finance        | 620       | 0.20               | 0.96              |
+----------------+-----------+--------------------+-------------------+
| HR             | 320       | 0.20               | 0.94              |
+----------------+-----------+--------------------+-------------------+
| Legal          | 280       | 0.20               | 0.94              |
+----------------+-----------+--------------------+-------------------+
| **Disparate-impact ratio:**                     | **0.94**          |
+-------------------------------------------------+-------------------+

: Four-Fifths Audit by Department (Synthetic)
:::

## Identification Bias

A subtle bias the model itself cannot fix is identification bias: the
human reviewer who sees `EMP_2417` on a risk dashboard and recognises
Ravi from last quarter's all-hands anchors on memory rather than
evidence. The model is innocent --- the feature column list is
`[Tenure_Months, Base_Salary, Department_Code, Manager_Tenure_Months]`
and never contains the identifier --- but the user surface still enables
the bias. AttriSense therefore *pseudonymizes at the dashboard
boundary*: the UI shows a deterministic salted-hash `Review_ID` (format
`RV-NNNNNN`). The mapping from `Review_ID` back to `Emp_ID` lives in a
separate access-controlled table with its own audit log; the salt
rotates quarterly. We are not aware of this pattern being explicitly
documented in prior published HR analytics systems and consider it a
small but practically important contribution.

## Synthetic-Data Caveat

All performance numbers are reported on a synthetic corpus and may not
transfer to real enterprise data without re-tuning. The synthetic
generator was calibrated to public HR distributions but cannot replicate
firm-specific cultural dynamics, manager effects, or industry
seasonality. A real deployment must repeat the audit on real data.

## Surveillance and Worker Dignity

Predictive flight-risk systems carry real risk of being weaponized
against workers (preemptive demotion, exclusion from key projects). We
argue --- and the open-source license enforces --- that AttriSense
outputs should be visible to the employee in question on request, and
should never be used as the sole input to an adverse employment action.
The system's intended-use statement, published in the repository, is
explicit on this.

## Regulatory Alignment

The system architecture is designed to satisfy NYC Local Law
144 [@nyclaw2023] bias-audit requirements and the EU AI Act's
high-risk-system documentation expectations: a model card, an
intended-use document, a fairness policy, and a session-log audit trail
are all part of the deliverable.

# Lessons Learned in Production Hardening

The journey from a working notebook to a Streamlit dashboard a hiring
manager could deploy surfaced four lessons that we found
underrepresented in the literature and worth documenting:

**Per-fold SMOTE matters more than which oversampler.** Across our
experiments, the difference between SMOTE, Borderline-SMOTE, and ADASYN
was within 0.01 PR-AUC. The difference between applying any of them
*before* versus *after* the train/test split was 0.07 PR-AUC --- and the
"before" version is a silent leakage bug.

**Calibration is not optional.** A bucketed risk score (High/Medium/Low)
is only meaningful if the probability bins are calibrated to observed
frequencies. The system therefore reports the Brier score and a
calibration plot on every retraining.

**Identifiers leak even when features do not.** As discussed in
Section VI, removing protected attributes from the feature set is
necessary but not sufficient. The reviewer's short-term memory is a
feature surface too.

**Provider fallback is cheap.** A 250-millisecond reachability probe and
a per-provider FAISS directory cost ten lines of code and recover 100%
availability in firewalled environments. We saw no published HR RAG
system that did this.

# Conclusion and Future Work

We have presented AttriSense, a unified open-source framework that
combines imbalanced-classification flight-risk prediction, Cox
proportional-hazards survival analysis, T-Learner causal uplift,
RAG-grounded qualitative explanation, and NL2SQL data-lake access into a
single workflow consumable by non-technical HR users, and wraps the
whole system in a fairness-by-default discipline that includes a
four-fifths-rule audit gate and an identification-bias mitigation
pattern. On a 5,000-employee synthetic corpus, the system achieves
ROC-AUC of 0.91, a calibration Brier of 0.061, a concordance index of
0.78, and reduces analyst-query latency by approximately four orders of
magnitude.

Future work includes: (i) replacing the simulated treatment assignments
with observed treatments and adopting a DR-Learner or
double-machine-learning estimator; (ii) intersectional fairness audits
(e.g. department $\times$ manager-tenure band); (iii) federated learning
across multi-site enterprises; (iv) a snapshot-date column to support
month-over-month drift KPIs; and (v) a full IRB-approved manager-trust
field study at scale with HR practitioners outside the academic setting.

# Acknowledgments {#acknowledgments .unnumbered}

The author thanks the California State University, East Bay Master of
Science in Business Analytics program for the academic foundation, and
acknowledges the use of GitHub Copilot, Claude, and GPT-4 as coding
collaborators throughout the implementation. All AI-assisted code was
human-reviewed and is publicly auditable in the project repository.

# Code and Data Availability {#code-and-data-availability .unnumbered}

Source code, synthetic dataset generator, evaluation harness, and the
Streamlit dashboard are publicly available under MIT license:
<https://github.com/Dogiparthi-Sharada/AttriSense>.

::: thebibliography
00

J. Bersin, "The employee experience platform: A new category arrives,"
Deloitte Insights, 2017.

IBM Watson Analytics, "HR Analytics Employee Attrition & Performance,"
IBM, 2017.

V. V. Saradhi and G. K. Palshikar, "Employee churn prediction," *Expert
Systems with Applications*, vol. 38, no. 3, pp. 1999--2006, 2011.

R. S. Sexton, S. McMurtrey, J. O. Michalopoulos, and A. M. Smith,
"Employee turnover: A neural network solution," *Computers & Operations
Research*, vol. 32, no. 10, 2005.

R. Yedida, R. Reddy, R. Vahi, R. Jana, A. GV, and D. Kulkarni, "Employee
attrition prediction," *arXiv:1806.10480*, 2018.

N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, "SMOTE:
Synthetic minority over-sampling technique," *Journal of Artificial
Intelligence Research*, vol. 16, pp. 321--357, 2002.

N. V. Chawla, A. Lazarevic, L. O. Hall, and K. W. Bowyer, "SMOTEBoost:
Improving prediction of the minority class in boosting," in *PKDD*,
2003.

D. R. Cox, "Regression models and life-tables," *Journal of the Royal
Statistical Society B*, vol. 34, no. 2, 1972.

J. D. Kalbfleisch and R. L. Prentice, *The Statistical Analysis of
Failure Time Data*, 2nd ed., Wiley, 2002.

M. Kuhn and K. Johnson, *Applied Predictive Modeling*, Springer, 2018.

C. Davidson-Pilon, "lifelines: Survival analysis in Python," *Journal of
Open Source Software*, vol. 4, no. 40, 2019.

S. Wager and S. Athey, "Estimation and inference of heterogeneous
treatment effects using random forests," *Journal of the American
Statistical Association*, vol. 113, no. 523, 2018.

E. H. Kennedy, "Optimal doubly robust estimation of heterogeneous causal
effects," *arXiv:2004.14497*, 2020.

S. R. Künzel, J. S. Sekhon, P. J. Bickel, and B. Yu, "Metalearners for
estimating heterogeneous treatment effects using machine learning,"
*PNAS*, vol. 116, no. 10, 2019.

Microsoft Research, "EconML: A Python package for ML-based heterogeneous
treatment effects estimation," <https://github.com/microsoft/EconML>,
2019.

P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive
NLP tasks," in *NeurIPS*, 2020.

J. Johnson, M. Douze, and H. Jégou, "Billion-scale similarity search
with GPUs," *IEEE Trans. Big Data*, vol. 7, no. 3, 2019.

I. Androutsopoulos, G. Ritchie, and P. Thanisch, "Natural language
interfaces to databases --- An introduction," *Natural Language
Engineering*, vol. 1, no. 1, 1995.

N. Rajkumar, R. Li, and D. Bahdanau, "Evaluating the text-to-SQL
capabilities of large language models," *arXiv:2204.00498*, 2022.

M. Pourreza and D. Rafiei, "DIN-SQL: Decomposed in-context learning of
text-to-SQL with self-correction," in *NeurIPS*, 2023.

S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model
predictions," in *NeurIPS*, 2017.

New York City Local Law 144 of 2021, "Automated employment decision
tools," effective July 2023.

F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *JMLR*,
vol. 12, pp. 2825--2830, 2011.

T. Brown et al., "Language models are few-shot learners," in *NeurIPS*,
2020.

H. Chase, "LangChain," GitHub, 2023.
<https://github.com/langchain-ai/langchain>
:::
