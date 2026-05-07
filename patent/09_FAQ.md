# 09 — Defensive FAQ

A single page of pre-built answers for the three audiences who will push
back on this work: **patent reviewers**, **peer reviewers**, and **FAANG
interviewers**. Memorise the bolded answers; the prose is for context.

---

## A. Patent reviewers (USPTO examiner / attorney)

### A1. "Isn't fairness gating obvious in light of Fairlearn / AIF360?"
**No — those are libraries that report disparate impact post-hoc. The
present invention applies the metric as a *blocking* condition before
recommendations are surfaced. No prior art combines suppression with the
recommendation surface in a single workflow.**

### A2. "Aren't salted IDs just a known privacy pattern?"
**Salting alone is known. The novelty is the integration: the
HMAC-derived Review_ID is the *only* employee handle visible in the SHAP
attribution, recommendation, and audit log surfaces; the mapping table
lives in an audit-only datastore inaccessible to dashboard reviewers.
This combination is not in any cited reference.**

### A3. "T-learner is published — claim 3 fails 102."
**Claim 3 is dependent on claim 1; the novelty rests in the combination
of T-learner CATE selection *with* the fairness gate of claim 1, step 3.
EconML provides the learner; AttriSense provides the gated workflow.**

### A4. "Provider-fallback router — circuit breaker is prior art."
**Circuit breaker is general-purpose; claim 4 narrows to (a) sub-second
reachability probe, (b) deterministic local embedding fallback, (c)
immutable routing-decision log. Combined narrowness avoids 103 obviousness.**

### A5. "Is the four-fifths rule a human construct, not patentable subject matter?"
**The legal rule is unpatentable; the *system* that implements it as a
machine-readable blocking gate within a recommendation pipeline is a
practical application that integrates into a technological process —
satisfies Alice/Mayo step 2.**

---

## B. Peer reviewers (IEEE BigData / FAccT / KDD ADS)

### B1. "Synthetic data — how do we know it generalises?"
**We don't, and we say so explicitly in §10 (limitations). The synthetic
generator parameters are open-sourced; the paper invites partners with
real anonymised corpora to validate. The system patterns (gate,
salting, fallback router) are dataset-independent.**

### B2. "Why a T-learner and not X- or DR-learner?"
**T-learner gives interpretable per-arm outcome models, which the
fairness audit consumes directly. X-/DR-learner are on the future-work
list — we report on the variant that is currently shipped.**

### B3. "ECE 0.038 is fine, but Brier score?"
**Brier and reliability diagram are in Table 1; we report ECE in the
abstract because it is the most commonly understood scalar.**

### B4. "Suppression denies HR a useful signal — isn't that worse?"
**No: the cohort is escalated to HR-ops via the audit log, *and* the
manager is shown a 'fairness review pending' badge so the decision is
not silently biased. Suppression is the only way to remove the bias from
the decision path; flagging leaves the bias in.**

### B5. "Provider-fallback is engineering, not research."
**The pattern is engineering; the contribution is the observation that
the dashboard becomes a partial-availability system in any real
deployment, and the demonstration that an LLM-driven UX can be made
graceful with deterministic local fallbacks at a known accuracy cost.
We quantify the cost in Table 4.**

---

## C. FAANG interviewers

### C1. "Walk me through the system."
**Six modules, three novelties. (1) Calibrated GBDT classifier. (2)
Four-fifths fairness gate that suppresses, not flags. (3) T-learner
causal uplift over three arms. (4) HMAC-salted Review_IDs. (5) NL→SQL
with TF-IDF fallback. (6) Multilingual RAG with hashing-vector
fallback. Wrapped in Streamlit, p95 410 ms.**

### C2. "What was the hardest decision?"
**Whether to flag or suppress. Flagging is industry standard and
preserves more information, but it leaves the bias in the decision
path. Suppressing is harder to defend politically but is the only
intervention that removes the bias. I chose suppression and built the
audit-log + escalation path to compensate for the lost information.**

### C3. "Where would this break in production?"
**Three places. (1) Synthetic vs. real distribution drift on the risk
classifier. (2) Salt rotation operationally — we'd need a managed KMS
in production, not a config flag. (3) The intervention log is
synthetic; in production we'd need to instrument every actual
intervention to keep the T-learner honest.**

### C4. "Why didn't you use Spark?"
**The data fits in 16 GB RAM; Spark adds operational overhead without
benefit. If the corpus grew past 10 M employees we'd reconsider.**

### C5. "How do you know the LLM fallback isn't worse than no answer?"
**We log the routing decision and serve a banner when the deterministic
fallback is in use, so the user knows the answer is best-effort. Table
4 quantifies the answer-quality delta.**

### C6. "Tell me about a mistake."
**Initial fairness gate flagged rather than suppressed. After a
pre-mortem with myself, I realised flagging is theatre — the
recommendation is still in the manager's eye. I rewrote the gate to
suppress, added the badge, added the audit escalation. The lesson:
ethical guardrails are only effective if they're load-bearing.**
