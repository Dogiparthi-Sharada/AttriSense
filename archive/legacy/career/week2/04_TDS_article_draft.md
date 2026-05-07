# 📰 Towards Data Science / Medium Article Draft

> ~1,500 words. Technical depth without academic stiffness.
> Goal: a *different audience* than LinkedIn — practitioners who Google "RAG over HR data."
> Publish Wednesday May 13. Cross-link from LinkedIn that afternoon.

---

# Building AttriSense: A Multi-Modal HR-Analytics System with Predictive ML, RAG, and NL→SQL

*An MSBA capstone that became something worth open-sourcing.*

---

## Why HR Analytics Is Mostly Useless

Most HR dashboards I've seen tell you what already happened.

They report headcount. They show last quarter's attrition rate. They split it by department. The CHRO nods. The slide deck closes. Nothing changes.

What HR actually needs — and what almost no enterprise tool delivers — is **predictive, individualized, explainable signal that a frontline manager can act on by Monday morning.**

I built AttriSense as my MSBA capstone at Cal State East Bay to try to close that gap. This post walks through the design choices, the tradeoffs, and what I'd do differently next time.

The code is open source: [github.com/Dogiparthi-Sharada/attrisense](https://github.com/Dogiparthi-Sharada/attrisense). The paper is on arXiv. There's a live demo.

---

## The Three Gaps

Every conversation with a real HR practitioner during this project surfaced the same three problems:

**1. The Trust Gap.** Predictive models, when deployed, behave as black boxes. Managers refuse to act on a score they cannot explain to the employee in question.

**2. The Qualitative Gap.** Most predictive systems consume only structured tabular features (tenure, salary, performance rating) and ignore the rich free-text signal in exit interviews, 1:1 notes, and engagement surveys.

**3. The Access Gap.** HR data lakes are gated behind analyst SQL queues with multi-day latency. By the time the analyst gets back to the manager, the high-risk employee has already accepted an offer somewhere else.

AttriSense addresses all three with three cooperating subsystems: a predictive engine, a RAG layer, and a NL→SQL agent.

---

## Layer 1: The Predictive Engine

The base layer is a Random Forest classifier trained on a 5,000-employee synthetic corpus. The corpus was generated programmatically and calibrated to published HR-attrition distributions — no real PII, no compliance risk, fully reproducible.

The interesting design choice here was **how to handle the class imbalance.**

Real HR data has roughly a 10–15% positive rate (the employees who actually leave in any given window). On data that imbalanced, naïve accuracy is meaningless — a model that predicts "will stay" for everyone gets ~88% accuracy and is completely useless.

I went with **SMOTE (Synthetic Minority Over-sampling Technique)** applied only to the training fold inside the cross-validation loop. Applying SMOTE to the full dataset before splitting is one of the most common subtle mistakes in HR-attrition papers — it leaks synthetic positives into the test set and inflates every reported metric.

The trained model produces a calibrated probability $\hat{p}(\text{leave} \mid x)$ for each employee, which I bucket into High (>0.75), Medium (0.40–0.75), and Low (≤0.40).

Reported metrics (held-out test set):

- ROC-AUC: 0.91
- PR-AUC: 0.74
- Brier (calibration): 0.061

PR-AUC is more sensitive than ROC-AUC on imbalanced data, so it's the primary metric. ROC-AUC alone tends to flatter rare-class problems.

For each prediction, SHAP TreeExplainer surfaces the top-3 contributing features — and that becomes the bridge to Layer 2.

---

## Layer 2: RAG Over Exit Interviews

Here's where the project departs from typical HR-analytics work.

A 0.81 risk score by itself isn't actionable. A manager needs to know **why** the model thinks Priya is at high risk, *and* whether other employees who looked like Priya actually left and what they said about why.

So I built a Retrieval-Augmented Generation (RAG) layer over a corpus of 500 synthetic exit-interview narratives. Each narrative is embedded with OpenAI's `text-embedding-3-small` (1,536-dim) into a FAISS `IndexFlatIP` index.

The retrieval query isn't the employee's row directly — it's the **top-3 SHAP feature names plus the employee's department and tenure band.** This means the retrieval is grounded in *what the model actually thinks is driving the risk*, not in arbitrary metadata.

Top-5 nearest historical leavers are retrieved and passed to a GPT-4-class LLM with a constrained prompt:

> *"Here are the SHAP-identified risk drivers for this employee. Here are 5 semantically similar historical exit narratives. Generate a 3-bullet manager-facing rationale grounded ONLY in the retrieved evidence."*

The output looks like this for one employee:

> *"Priya Shah · Engineering, 8mo tenure · 81% risk*
>
> *• Compensation gap: 5 of 5 retrieved similar leavers cited below-market base pay as their primary reason; Priya is at the 23rd percentile of her band.*
>
> *• Career velocity: no promotion in 18 months; 4 of 5 retrieved leavers cited lack of advancement.*
>
> *• Manager span: her manager has 14 direct reports — twice the engineering median. Retrieved leavers cited reduced 1:1 quality."*

That's a Monday-morning conversation, not a number.

---

## Layer 3: NL→SQL — Talk to the Data Lake

The third gap — analyst SQL queues — is the easy one to close in 2026.

I built a LangChain SQL agent over the SQLite HR data warehouse. The agent gets the schema injected into the system prompt, a small few-shot example bank, and a self-correction loop: if the generated query raises a SQL error, the error message is fed back into the prompt for one retry.

On a hand-curated 50-question gold set:

- 86% exact-match SQL execution accuracy
- 92% semantic-match (correct answer, syntactically different SQL)

Median end-to-end latency is **11.7 seconds** versus a baseline of **2.3 days** for analyst-mediated queries.

The dashboard exposes this as a single text box: "Ask your data lake."

```
> show me high-risk Manufacturing engineers under 12 months tenure

→ 47 employees returned. Department: Manufacturing.
   Avg risk: 0.82. Avg tenure: 6.4 months. ...
```

This single feature changes who in the org can use the system. No more "I'll file a ticket with analytics and hear back next week."

---

## What I Got Wrong (and What I'd Do Differently)

Three things, ranked by severity.

### 1. The first version reported only accuracy.

I had 89% accuracy on my first model and was thrilled.

My capstone advisor pointed out — politely — that on a class with 10% prevalence, that's near-baseline. I rebuilt the evaluation around PR-AUC, calibration curves, and per-bucket recall.

The lesson: **pick the metric that matches the cost of the error, not the metric that flatters you.** I now report PR-AUC alongside ROC-AUC on every model I train.

### 2. The model is correlational, not causal.

AttriSense tells you who's likely to leave. It does *not* tell you what intervention would change that.

Predicting "Priya is 81% likely to leave" doesn't tell you whether a 7% raise, a manager change, a project rotation, or a promotion would maximally reduce that. That's a causal-inference question, not a prediction question.

The next iteration uses **causal uplift modeling** (`econml`, `causalml`) to recommend the specific intervention that maximally reduces the predicted risk for *that specific employee*. This is the missing layer.

### 3. I underestimated the need for an explicit limitations page.

The first version of the dashboard didn't surface model limitations to users. The fairness audit was buried in a notebook. The synthetic-data caveat was in the README, not in the app.

After feedback from two HR practitioners, I added an explicit **Limitations & Ethics** tab inside the Streamlit app. It says, plainly:

- This model is correlational
- It uses synthetic data; real data will need re-tuning
- It must never be the sole input to an adverse employment action
- Bias audit re-runs every retraining

This is what separates a junior data scientist from a senior one. Junior: "the model is X% accurate." Senior: "here's what the model can't do, and here are the failure modes."

---

## On Building With AI Coding Tools

This project was built collaboratively with GitHub Copilot, Claude, and GPT-4. I disclose this openly in `AI_CONTRIBUTIONS.md` in the repo and in the paper Acknowledgments.

I treat AI assistants the way a senior engineer treats Stack Overflow plus a junior pair-programmer: I write the architecture, decide the trade-offs, debug the outputs, and own the correctness. AI-assisted development is the modern baseline. What matters is whether the developer can defend every design decision in the codebase.

I can. The work is real. The thinking is mine.

If you're a hiring manager reading this and worried that AI-assisted code is somehow "less authentic" — the candidate who *won't* use AI well in 2026 is going to be the slow one on the team.

---

## Where This Goes Next

Three directions, in priority order:

1. **Causal uplift modeling.** Move from prediction to intervention recommendation.
2. **Cox survival analysis.** Time-to-event prediction (how long until they leave), not just probability.
3. **Federated training.** Multi-site enterprises (looking at you, photonics + semiconductor) need to train across sites without centralizing PII.

I'd also love to do a real IRB-approved manager-trust field study. The pilot survey (n=12) showed a meaningful trust lift from black-box scores to RAG-grounded explanations. That deserves a proper experimental design.

---

## What This Is For

I'm an MSBA candidate at Cal State East Bay. I built this because I think the intersection of business framing and applied ML is where the real leverage is — and it's underexplored.

I'm actively looking for AI/ML / Applied Data Science / People Analytics roles. Internship or full-time. If you're hiring, or if you want to break the project and tell me what to fix, my DMs are open.

The repo is here: [github.com/Dogiparthi-Sharada/attrisense](https://github.com/Dogiparthi-Sharada/attrisense). The arXiv preprint is here: [arXiv:XXXX.XXXXX]. The live demo is at [attrisense.streamlit.app](https://attrisense.streamlit.app).

Thanks for reading. AI shouldn't replace HR. It should sit next to HR.

---

*Sharada Dogiparthi is an MSBA candidate at California State University, East Bay, focused on applied AI for business outcomes. AttriSense is open-source under MIT license. Follow her on [LinkedIn](https://linkedin.com/in/...) and [GitHub](https://github.com/Dogiparthi-Sharada).*

---

## 📋 Submission notes

- **Where to publish:** Towards Data Science (highest reach for ML practitioners) → Medium publication submission via TDS editor portal. Backup: post on Medium directly under your account if TDS rejects (they reject 70% of submissions; don't take it personally).
- **Tags to use:** Machine Learning · Data Science · LLM · RAG · LangChain · HR Tech · Python · Career
- **Header image:** Use the Excalidraw architecture diagram. Keep it simple.
- **Cross-link:** From your LinkedIn post that afternoon ("just published the technical deep-dive — link in comments") and from your GitHub README as a "📖 Read the deep-dive" link.
- **Post length:** Keep at 1,500–1,800 words. Medium analytics show this is the sweet spot for completion rate.
