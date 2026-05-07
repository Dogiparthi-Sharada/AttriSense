# Twitter / X Thread — 10 tweets (publish 30 min after LinkedIn)

> **Tone:** technical, curious, no humblebrag. Tech Twitter rewards
> specificity. **Numbers, decisions, trade-offs.**

---

**Tweet 1 / 10** (the hook)

> Most HR analytics tells you *who left.*
>
> AttriSense tells you *who's about to — and what to do about it.*
>
> 5 model modalities, 1 dashboard, 1 fairness gate.
>
> Open-source, MIT.
>
> Thread 🧵👇

**Tweet 2 / 10** (modality 1: classification)

> 1️⃣ **Who is at flight risk?**
>
> RandomForest + SMOTE on a 5,000-row synthetic corpus.
>
> ROC-AUC 0.91. PR-AUC 0.74.
>
> Reporting PR-AUC, not just ROC, because the positive class is 10% —
> ROC alone flatters imbalanced models.

**Tweet 3 / 10** (modality 2: survival)

> 2️⃣ **When are they likely to leave?**
>
> Cox proportional-hazards (lifelines). Concordance 0.78.
>
> Per-employee survival curve. Not "85% risk." But "50% survival at
> day 180" — a Q3 calendar item, not a number.

**Tweet 4 / 10** (modality 3: causal uplift)

> 3️⃣ **Which intervention helps THIS person?**
>
> EconML T-Learner across three arms:
> – Compensation correction
> – Manager rotation
> – Learning budget
>
> Per-employee CATE — so retention budget isn't flat-distributed.
> Causal uplift, not flat retention spend.

**Tweet 5 / 10** (modality 4: RAG with fallback)

> 4️⃣ **What did similar leavers say?**
>
> Multilingual RAG over EN/ES/HI exit-interview text.
>
> 250 ms DNS+TCP+HTTPS reachability probe before every OpenAI call.
> Hashing fallback (256-d, MD5-bucketed) when the network blocks it.
> Per-provider FAISS dirs so 1536-d and 256-d vectors never collide.
>
> Dashboard never blocks on a 3rd-party endpoint.

**Tweet 6 / 10** (modality 5: NL→SQL)

> 5️⃣ **What does HR want to know right now?**
>
> Plain English → SQL via LangChain.
> Plus a TF-IDF gold-question fallback over a 50-question gold set —
> answers 11/50 without an LLM at all.
>
> "show me high-risk Manufacturing engineers under 12mo tenure" → 8 sec.

**Tweet 7 / 10** (the underrated layer)

> The layer I'm proudest of *isn't* a model.
>
> Every dashboard view replaces raw `Emp_ID` with a salted SHA-256
> Review_ID — `RV-NNNNNN`.
>
> Without it, reviewers anchor on memory ("oh, that's Ravi") and
> bypass the model. With it, every record looks the same.
>
> Salt is env-rotatable per pilot.

**Tweet 8 / 10** (responsibility, not just compliance)

> Every prediction is gated by an EEOC four-fifths fairness audit
> *before* it reaches the screen — not after.
>
> If the disparate-impact ratio drops below 0.80 between protected
> classes, the recommendation is suppressed and the dashboard tells
> the user why.

**Tweet 9 / 10** (the work behind the work)

> 7-page IEEE-style conference paper.
> 25 references. 4 tables. 1 algorithm.
>
> 79-page beginner's guide DOCX (cover + Word TOC + 8 chapters +
> ASCII + Pixel-pastel diagrams).
>
> mkdocs --strict passes.
>
> Because shipping the model is half the work; explaining it is the
> other half.

**Tweet 10 / 10** (the CTA)

> Live demo (no install, ~10 sec): https://attrisense.streamlit.app
>
> MIT-licensed: https://github.com/Dogiparthi-Sharada/attrisense
>
> Built as my MSBA capstone @ Cal State East Bay.
>
> Open to AI Engineering / Applied ML / People-Analytics roles.
>
> Replies open for the next 24h. Ask me anything.

---

## Posting tips

- **Schedule via Tweetdeck / X native** — 30 min after the LinkedIn
  post goes live. Keeps both audiences fresh.
- **Tweet 1 has the demo URL — DO NOT** put any other link in tweet 1.
  X downranks first-tweet links; put them in the *last* tweet.
- **Pin the thread** to your X profile for the rest of Week 2.
- **Quote-tweet your own thread on Wednesday** with a single follow-up
  ("biggest surprise from yesterday's launch: comments asking about
  X — wrote up a longer answer here: [TDS draft when ready]").
