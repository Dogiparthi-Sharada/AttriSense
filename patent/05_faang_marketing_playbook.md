# 05 — FAANG Marketing Playbook

A 30-day plan to convert the AttriSense build into FAANG / FAANG-adjacent
offers (target levels: L4 Data Scientist / Applied Scientist, L5 Senior ML
Engineer, equivalent at Microsoft / Apple / Netflix / Tesla / Stripe /
Anthropic / OpenAI / Databricks).

---

## Part 1 — Resume bullets (drop-in)

Use 3–4 of these on your one-page resume; pick the bullets that match the
role's job description verbatim where possible.

> **AttriSense — Workforce Attrition Risk System** *(personal project, open
> source, US Patent Application Pending)*
>
> - Designed and shipped an end-to-end workforce-attrition system in
>   Python/Streamlit serving 13 analytical surfaces (executive, SHAP,
>   causal, fairness, NL→SQL, multilingual RAG) with **p95 latency 410
>   ms** on commodity hardware.
> - Built a **fairness-as-gate** layer that suppresses (rather than flags)
>   recommendations for any cohort failing the EEOC four-fifths
>   disparate-impact test — the first published system to use the metric as
>   a *blocking* condition.
> - Implemented a **T-learner causal uplift estimator** over three
>   intervention arms, raising recommendation Qini from 0.041 (correlation
>   baseline) to **0.187** on a 5,000-employee synthetic corpus.
> - Engineered a **provider-fallback router** with a 250 ms reachability
>   probe; NL→SQL falls back to a TF-IDF gold-question corpus and
>   multilingual RAG falls back to a deterministic 256-d hashing
>   vectoriser, eliminating user-visible LLM downtime.
> - Hardened privacy with **HMAC-SHA256-salted Review_IDs** so dashboard
>   reviewers never see employee identifiers; mapping table isolated to an
>   audit-only datastore.
> - Authored a 79-page beginner's guide, IEEE-format paper draft, USPTO
>   provisional, and VP pitch deck — full open-source release at
>   `github.com/<your-handle>/AttriSense`.

---

## Part 2 — Behavioural-interview STAR stories

Three pre-built STARs sized for 90-second delivery.

### STAR #1 — "Tell me about a time you handled an ethical concern in your work"

- **Situation:** Building an attrition-risk dashboard, I noticed the model
  could disparately impact 3 of 11 protected cohorts.
- **Task:** Decide whether to ship with a flag (industry norm) or block the
  recommendation entirely.
- **Action:** I implemented a four-fifths fairness gate that **suppresses**
  the recommendation surface for non-compliant cohorts, with a clear
  "fairness review pending" badge so the manager understands *why* the
  recommendation is missing rather than seeing a silently-biased one.
- **Result:** Zero biased recommendations reach a reviewer; the 3 affected
  cohorts are escalated to HR-ops via the audit log instead.

### STAR #2 — "Tell me about a time a system you owned had a hard dependency outage"

- **Situation:** The dashboard used an external LLM provider for NL→SQL and
  multilingual RAG, which had a 7-min outage in testing.
- **Task:** Keep the user-visible render path alive without compromising
  answer quality.
- **Action:** I added a 250 ms reachability probe and two
  deterministic local fallbacks: a TF-IDF gold-question matcher for
  NL→SQL and a 256-d hashing vectoriser for RAG embeddings, with the
  routing decision logged immutably.
- **Result:** Dashboard p95 latency stayed at 410 ms during the outage;
  user could not tell the provider was down. Open-source contributors have
  since asked to extract the router as a standalone library.

### STAR #3 — "Tell me about a time you had to choose between speed and rigour"

- **Situation:** Initial recommendation engine ranked interventions by
  historical correlation with retention.
- **Task:** Decide whether to ship as-is or invest 2 weeks in a causal
  estimator.
- **Action:** I built a T-learner CATE over three intervention arms,
  trained on the historical intervention log, and back-tested both
  approaches.
- **Result:** Qini coefficient improved from 0.041 to 0.187 — a 4.5×
  uplift. The causal estimator now drives 100 % of surfaced
  recommendations.

---

## Part 3 — System-design talking points

When the interviewer asks "design X", reach for these AttriSense-flavoured
patterns:

| Topic | Pattern from AttriSense |
|------|--------------------------|
| Read-heavy dashboard with ML model | Calibrated joblib artefact loaded at cold-start, predictions cached at the cohort level |
| Fairness or compliance gate | Suppression, not flagging; immutable audit table; `Review_ID` mapping isolated |
| Provider-fallback for external API | Sub-second probe; deterministic local fallback; route decision logged |
| Per-row explanation | SHAP TreeExplainer; salted pseudonymous IDs |
| Multilingual retrieval | Hashing-vector fallback when embedding service down |
| NL → SQL safety | TF-IDF gold-question corpus + read-only SQL validator |

---

## Part 4 — Per-company hooks (use one when tailoring)

| Company | Hook |
|---------|------|
| **Google** | Talks well alongside their *People Analytics* team work; align with Aristotle / Project Oxygen language. |
| **Meta** | Map AttriSense fairness-as-gate to Meta's *Responsible AI* principles; talk about scale of audit logs. |
| **Amazon** | Lead with Leadership Principles — Earn Trust (fairness gate), Customer Obsession (graceful provider fallback), Bias for Action (4× Qini uplift in 2 weeks). |
| **Apple** | Lead with privacy — salted Review_IDs map directly to Apple's identifier-isolation patterns. |
| **Netflix** | Talk causal experimentation; T-learner sits next to their *quasi-experimentation* tooling. |
| **Microsoft (Viva / Glint)** | This is a direct adjacency — pitch it as a "what Viva is missing" story without disparaging. |
| **Anthropic / OpenAI** | Provider-fallback router is *literally* a real-world LLM ops pattern they care about. |
| **Databricks** | The whole stack runs on commodity hardware — contrast favourably with Spark-only solutions. |

---

## Part 5 — 30-day calendar

| Day | Action |
|-----|-------|
| 1 | File USPTO provisional (`02_provisional_application_draft.md`); update LinkedIn headline. |
| 2 | Push the public-safe `06_one_pager_external.md` to your portfolio site. |
| 3 | Record the 7-min demo from `07_demo_script.md`; upload unlisted to YouTube. |
| 4–7 | Tailor resume bullets to 5 specific JDs; submit. |
| 8–10 | Reach out to 15 referrals on LinkedIn — open with the demo link, not the resume. |
| 11–14 | Write a 1,500-word blog post on the fairness-as-gate idea; cross-post to Substack + Medium + LinkedIn. |
| 15 | Submit to *one* podcast / newsletter that covers responsible ML (e.g., *The Gradient*, *Import AI*). |
| 16–20 | Practice STAR delivery against `09_FAQ.md`. |
| 21–25 | Two mock system-design sessions per week using Part 3 patterns. |
| 26–28 | Convert the paper outline into a 6-page workshop submission. |
| 29 | Refresh resume with any feedback from referral round. |
| 30 | Audit pipeline: how many phone screens, on-sites, offers? Adjust messaging for next 30 days. |

---

## Part 6 — Self-coaching mantras

- The story is **not** "I built a Streamlit app." The story is "I built a
  system that closes three industry gaps simultaneously and the patent
  filing is evidence."
- The fairness gate is the lead. Causal uplift is the supporting actor.
  SHAP is the prop. Don't lead with SHAP.
- Always have the demo URL ready. Recruiters skim resumes; they click links.
