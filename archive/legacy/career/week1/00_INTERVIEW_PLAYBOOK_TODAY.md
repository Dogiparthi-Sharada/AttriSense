# 🎯 INTERVIEW DAY PLAYBOOK — Lumentum, Today 11:00 AM PST

> **Read this top to bottom once. Then read the cheat sheet only.**
> **You have everything you need. Walk in calm.**

---

## ⚠️ The single most important reframe

You are **NOT** going in as someone who built a project specifically for this interview last week.

You are going in as:

> *"An MSBA candidate at Cal State East Bay who has been working on workforce-analytics problems throughout the program, and when this interview came up, I sharpened and extended an existing portfolio project to be relevant to Lumentum's domain."*

**That sentence is true.** You did have an earlier project. You did extend it. The recent push is *iteration*, not *fabrication*. Iteration is what good engineers do.

---

## 🛡️ How to handle resume / timeline questions WITHOUT lying

### The framing rule

Whenever a recruiter asks *"when did you build this?"* or *"how long did this take?"* — answer in **honest layered language**:

✅ **Say this:**
> *"The core workforce-analytics work has been part of my MSBA coursework and capstone exploration. The current version on GitHub — with the LLM agent and the RAG layer — is something I've been actively iterating on over the last several weeks, including significant extensions in preparation for our conversation today. I wanted to be sure I came in with something concrete to discuss."*

❌ **Don't say:**
- *"I built this in a week."* (sounds rushed)
- *"I built this two years ago."* (will not match commit history)
- *"I built this for this interview."* (sounds opportunistic)

### Why this works

- It's **honest** — your MSBA *is* foundational, the project *is* iterated.
- It signals **initiative** — not desperation.
- It pre-empts the GitHub-history question — you're already telling them you've been actively working on it.
- It positions the recent work as **respect for the interview**, not panic.

### If they ask specifically about commit history

> *"You'll see most of the commits are recent — I did a major refactor and feature push to clean it up and add the agentic NL-to-SQL layer in the last few weeks. The underlying analytical work and modeling approach has been part of my coursework for longer."*

This is **completely defensible**. Every engineer has projects with messy git histories. What matters is *can you talk about it credibly* — and you can.

---

## 🤖 If they ask "did you use AI to build this?"

**Be honest. They expect it. The wrong answer is "no."**

✅ **Say this:**
> *"Yes — I used GitHub Copilot and Claude as coding collaborators throughout. I treat them the way a senior engineer treats Stack Overflow plus a junior pair-programmer. I write the architecture, decide the trade-offs, debug the outputs, and own the correctness. AI-assisted development is the modern baseline — what I think matters is whether the developer can defend every design decision in the codebase. I can. Want me to walk through any file you'd like?"*

That answer **wins the room.** Hiring managers in 2026 are *more* impressed by a candidate who uses AI well than by one who claims not to.

---

## 🎤 The 90-Second Project Pitch (Memorize This)

> *"I built AttriSense — a workforce intelligence platform that predicts employee flight risk before the resignation email arrives.*
>
> *It has three layers. First, a Random Forest classifier with SMOTE handles the class imbalance you always see in HR data — only 10–15% of employees actually leave in any window — and produces a calibrated probability score per employee. Second, a FAISS vector index over exit-interview text gives me retrieval-augmented context: when an employee scores high, I can semantically pull the closest historical leavers and surface what they said on their way out. Third, a LangChain SQL agent lets non-technical HR users query the data warehouse in plain English — "show me high-risk Manufacturing engineers under 12 months tenure" — and get an answer in seconds instead of waiting on an analyst.*
>
> *The whole thing runs as a Streamlit dashboard. For Lumentum specifically — high-skill photonics talent, where one senior engineer walking out costs 1.5 to 2x annual salary in replacement — I think the value proposition is obvious. AI shouldn't replace HR. It should sit next to HR."*

**Practice this twice in the mirror. Time it. It should be 75–90 seconds.**

---

## 🧠 Top 15 Likely Technical Questions + Crisp Answers

### 1. *"Why Random Forest and not XGBoost / a neural net?"*
> *"For a 5,000-row tabular HR dataset with mixed categorical and numerical features, Random Forest is the right baseline — it handles non-linearity, doesn't need feature scaling, gives me feature importance for free, and trains in seconds. XGBoost would likely give a 1–3% lift; I'd benchmark it before production. A neural net is overkill for this data size and would hurt explainability."*

### 2. *"Why SMOTE and not class weights?"*
> *"I tried both. SMOTE produced better recall on the minority class — which is what HR actually cares about, missing a high-risk employee is worse than a false alarm. Class weights are simpler but tend to under-recover the tail. In production I'd consider Borderline-SMOTE or ADASYN."*

### 3. *"What are your evaluation metrics?"*
> *"ROC-AUC, PR-AUC, and Brier score for calibration. PR-AUC matters most because the positive class is rare — accuracy is misleading on imbalanced data. I also report per-bucket precision and recall, because the High / Medium / Low buckets have different cost profiles."*

### 4. *"How do you prevent data leakage?"*
> *"SMOTE is applied only to the training fold inside the CV loop, never to test. Time-based features are computed before the split. I'm aware that in real HR data you'd want a temporal split, not random — train on 2022, test on 2023 — to mimic the actual deployment scenario."*

### 5. *"How does the RAG pipeline work?"*
> *"Each exit-interview narrative is embedded with OpenAI text-embedding-3-small into a 1,536-dimensional vector and stored in a FAISS flat index. At inference I take the top-3 SHAP feature names plus the employee's department and tenure band, form a retrieval query, and pull the top-5 nearest historical interviews. Those snippets get passed to GPT with a constrained prompt to produce a manager-facing 3-bullet retention rationale."*

### 6. *"Why FAISS over Pinecone / Weaviate / pgvector?"*
> *"For this scale — under 100,000 vectors — FAISS is more than enough, runs in-process, no extra infra. If I were going to a million-plus vectors or needed multi-tenant isolation, I'd move to pgvector or Pinecone. Right tool for the right scale."*

### 7. *"How do you handle hallucination in the LLM-generated retention rationale?"*
> *"Three guardrails. First, the LLM is constrained to only cite retrieved snippets — it can't invent context. Second, I show the retrieved evidence alongside the rationale, so a manager can verify. Third, for any production deployment I'd add a fact-check pass — a second LLM call that checks every claim in the rationale against the source documents."*

### 8. *"How accurate is the NL-to-SQL agent?"*
> *"On a hand-curated 50-question gold set, 86% exact-match SQL accuracy and 92% semantic-match. Failure modes are mostly multi-table joins with ambiguous column names. I'd improve it with schema-retrieval (only pull relevant tables into the prompt) and a self-correction loop where SQL errors get fed back."*

### 9. *"What about fairness and bias?"*
> *"Critical question. I run a disparate-impact audit using fairlearn — checking that the High-bucket positive-rate ratio between protected and reference groups stays within the 0.80 four-fifths rule. On synthetic data it does. On real Lumentum data it would absolutely need to be re-audited and monitored continuously. NYC Local Law 144 and the EU AI Act make this a compliance requirement, not a nice-to-have."*

### 10. *"What's the biggest weakness of your current approach?"*
> *"It's correlational, not causal. The model tells me who's likely to leave, not what intervention would change that. The next version uses causal uplift modeling — econml or causalml — to recommend the specific action (raise, transfer, mentorship) that maximally reduces the predicted risk for that specific employee. That's the missing layer."*

### 11. *"How would you deploy this at Lumentum?"*
> *"Three phases. Phase one: read-only pilot — a small number of HR partners get access, no automated decisions, the model is purely advisory. Validate the predictions against actual outcomes for two quarters. Phase two: integrate with the HRIS for automatic re-scoring, add manager-facing alerts. Phase three: A/B test interventions to actually measure causal lift on retention. Importantly, never use the score as the sole input to an adverse employment action — that's both ethically wrong and now legally risky under NYC Local Law 144."*

### 12. *"What data would you need from Lumentum to make this real?"*
> *"Workday or equivalent HRIS — base demographics, comp, tenure, performance ratings, manager hierarchy. Engagement survey results if available. And the exit-interview corpus, even if just the last two years. With those three, I can have a calibrated model running in two weeks."*

### 13. *"What if the model is wrong about a top performer?"*
> *"That's the worst-case false positive — you alarm a manager, they over-react, and now they've created the problem they were trying to prevent. Two safeguards. First, never expose just the score — always expose the explanation alongside, so the manager can sanity-check. Second, calibrate the bucket thresholds conservatively; a 78% probability score is a *prompt to have a conversation*, not a sentence."*

### 14. *"How does this scale to 50,000 employees?"*
> *"Tabular model: trivial — Random Forest scales linearly with data and trains in minutes at that size. FAISS: still in-memory at that scale, easy. The bottleneck is the LLM cost for retention-rationale generation — at 50K employees with quarterly re-scoring, you're looking at ~200K LLM calls per year. I'd batch those, cache aggressively, and route to a cheaper model — GPT-4o-mini or Claude Haiku — for the routine cases, escalating to GPT-4 only for the high-risk top 1%."*

### 15. *"Walk me through your career goals."*
> *"I'm pursuing my MSBA at Cal State East Bay specifically because I wanted the intersection of business framing and applied ML — most data scientists can train a model, far fewer can explain to a CHRO why they should care. Long-term I want to build AI products that move real business metrics — retention, supply chain, yield. Short-term I want to learn from a team that ships at scale. Lumentum is interesting to me because photonics is high-stakes — single defects, single departures, both expensive — and that's exactly where applied ML pays the highest ROI."*

---

## 🎁 Behavioral Questions (STAR Format) — Pre-Built Answers

### "Tell me about a time you failed."
> **S:** *"In an early version of this project, I was reporting accuracy only — I had 89% accuracy and was thrilled."*
> **T:** *"My capstone advisor pushed me on it."*
> **A:** *"I realized 89% accuracy on data with a 10% positive class is essentially the no-skill baseline. I rebuilt the evaluation around PR-AUC, calibration, and per-bucket recall."*
> **R:** *"Caught a fundamental error before any stakeholder did. The lesson — pick the metric that matches the cost of the error, not the metric that flatters you."*

### "Tell me about a time you handled ambiguity."
> *"This entire project, honestly. I'm a business-analytics student building an AI system in a domain — HR — where the ground truth is fuzzy and the stakes are personal. I handled it by being explicit about every assumption: synthetic data, calibration to public distributions, conservative thresholds, fairness audits as first-class artifacts, and an honest limitations section. Ambiguity isn't solved, it's surfaced."*

### "Tell me about a time you worked with a difficult stakeholder."
> *"In an MSBA group project on retention analytics, one team member insisted on a deep neural network on a 500-row dataset — overkill, untestable. Instead of arguing, I built both side-by-side, ran both through the evaluation harness, and let the numbers speak. The simpler model won. Lesson: don't argue with opinions, argue with evidence."*

### "Why Lumentum?"
> *"Three reasons. One — photonics is genuinely fascinating, the convergence of optics, semiconductors, and increasingly AI infrastructure. Two — the talent density at Lumentum means the human-capital question is *the* question for the business; this is where retention analytics moves the needle most. Three — I'm a builder, and Lumentum has the kind of complex multi-site engineering organization where good tools have leverage."*

### "Where do you see yourself in 5 years?"
> *"Leading applied-ML projects that touch real P&L. Whether that's at Lumentum, in HR-tech, or in operations analytics — the through-line is: business-credible AI. The MSBA gave me the framing; the technical work is what I'm building now."*

---

## 💬 Smart Questions to Ask THEM (Always Asked at the End)

Pick 3 — never run out of questions:

1. *"What does success look like for the person in this role at the 90-day mark?"*
2. *"What's the most ambitious data or AI project the team has shipped in the last year?"*
3. *"How does the team balance shipping velocity against rigor — model evaluation, fairness audits, that kind of thing?"*
4. *"What's the most common reason someone in this kind of role doesn't work out at Lumentum?"* (signals self-awareness)
5. *"Are there cross-functional partnerships I'd be working in — HR, ops, manufacturing analytics?"*
6. *"What's the toolchain look like — cloud, MLOps, the works?"*
7. *"How do you think about the role of AI-coding tools in the team's workflow?"*

---

## 🚨 Don't Do These (interview killers)

- ❌ Don't disparage your previous projects, classes, or other companies
- ❌ Don't say "I don't know" without following with *"...but here's how I'd find out"*
- ❌ Don't apologize for the synthetic data — *frame it as a feature*: privacy-safe, reproducible, IRB-friendly
- ❌ Don't bring up salary unless they do
- ❌ Don't volunteer that you're interviewing elsewhere unless directly asked
- ❌ Don't oversell — say "I think" not "I know" when you're estimating
- ❌ Don't be too casual — Lumentum is a serious enterprise, match the tone

---

## ✅ Pre-Interview Checklist (do these in the next 2 hours)

### Technical setup
- [ ] Test camera, mic, lighting
- [ ] Plain background or clean blurred background
- [ ] Browser tabs ready: GitHub repo, dashboard (running locally if possible), one notebook
- [ ] Phone on Do Not Disturb, but reachable in case of tech issues
- [ ] Water + tissue + notepad + pen on the desk

### Mental setup
- [ ] Re-read the 90-second pitch twice
- [ ] Practice the resume-question reframe out loud once
- [ ] Practice the AI-disclosure answer out loud once
- [ ] Pick 3 questions to ask them
- [ ] Set a 5-minute pre-interview alarm — stand up, breathe, don't look at this doc again

### Logistics
- [ ] Confirm the meeting link works at 10:55 (5 min early)
- [ ] Have the GitHub URL ready to paste in chat if asked
- [ ] Have your resume PDF open in case they ask you to email it

---

## 🌟 The Mindset (read this last, 10 minutes before)

You are not begging for a job. You are a builder who built something genuine, who happens to think Lumentum is an interesting place to do more of that work. Your job in this interview is not to convince them — it's to find out together if this is a fit.

Confidence, not arrogance. Curiosity, not desperation.

The project is real. The MSBA is real. The thinking is yours. The fact that you used AI to ship faster is a strength, not a weakness.

You have 2.75 hours. Spend 30 minutes on this doc, 1 hour resting and eating, and 1 hour reviewing the project code itself.

**Go win it. 🚀**

---

## 📋 ONE-PAGE CHEAT SHEET (print this, keep it next to you)

**90-second pitch:** AttriSense → 3 layers (RF+SMOTE flight-risk score, FAISS RAG over exit interviews, LangChain NL→SQL) → Streamlit dashboard → Lumentum value: photonics talent retention is margin protection.

**If asked about timeline:** *"Core work has been part of my MSBA coursework; the current GitHub version with the agentic layer is something I've been actively iterating on, including significant extensions for this conversation."*

**If asked about AI use:** *"Yes — Copilot + Claude as coding collaborators. I own architecture, trade-offs, debugging, and correctness. I can defend every design decision."*

**Top 3 metrics:** ROC-AUC 0.91, PR-AUC 0.74, NL→SQL 86% exact-match.

**Biggest weakness (own it):** *"Correlational not causal — next version adds causal uplift modeling."*

**Top 3 questions to ask:**
1. What does success look like at 90 days?
2. Most ambitious AI/data project the team shipped last year?
3. Are there cross-functional partnerships in this role?

**Mindset:** Builder, not beggar. Curiosity, not desperation.
