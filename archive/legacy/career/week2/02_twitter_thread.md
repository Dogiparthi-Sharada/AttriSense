# 🐦 X / Twitter Thread — AttriSense Launch

> Post Tuesday May 12 ~12:30 PM PT (after the LinkedIn momentum is baked in).
> Pin to your profile.
> Different audience: AI builders, indie hackers, ML researchers.
> Goal: GitHub stars + technical credibility, not jobs.

---

## 🧵 The Thread (10 tweets)

### Tweet 1 (the hook)

```
Three weeks ago, Lumentum opened an interview door for me.

So I rebuilt my MSBA project for them — and shipped it as
open-source.

🧵 How AttriSense predicts employee flight risk before the
resignation email arrives — using SMOTE, FAISS, and a LangChain
SQL agent.

(repo + demo at the end)
```

### Tweet 2 (the problem)

```
The cost of attrition is brutal:

For a senior engineer, total replacement cost is 1.5–2× annual
salary once you count ramp-up time, lost institutional knowledge,
and team productivity disruption.

Yet HR analytics is overwhelmingly descriptive. We answer "who
left?" not "who's about to?"
```

### Tweet 3 (the architecture)

```
AttriSense has 3 layers:

1️⃣ Predictive engine — Random Forest + SMOTE on imbalanced HR
   data. 0–1 risk score per employee.

2️⃣ RAG layer — FAISS index over exit-interview text. Semantic
   search over qualitative signal.

3️⃣ NL→SQL agent — LangChain + GPT. Ask the data lake in English.
```

### Tweet 4 (the metrics)

```
Numbers on a 5,000-employee synthetic corpus:

• ROC-AUC: 0.91
• PR-AUC: 0.74
• Brier (calibration): 0.061
• NL→SQL: 86% exact-match on 50-question gold set
• Latency: 11.7s end-to-end (vs 2.3 days for analyst-mediated
  queries)

PR-AUC matters more than ROC-AUC here — class is rare.
```

### Tweet 5 (the design choice that mattered most)

```
Most HR-attrition papers report only accuracy. On a 10% positive
class, that's near-baseline. I learned this the hard way — my
first version was 89% accurate and I was thrilled.

If your model "works" but you can't defend the metric, you don't
have a model. You have a hallucination.
```

### Tweet 6 (RAG is the unlock)

```
The unlock is using SHAP attributions as the RAG retrieval query.

Employee scores 0.81. Top 3 SHAP drivers: below-band salary, no
promotion in 18mo, manager span 14.

Use those as the query → retrieve top-5 semantically similar
historical leavers → ground the manager rationale in real
precedent.
```

### Tweet 7 (the NL→SQL agent)

```
NL→SQL is the access unlock.

HR shouldn't file an analyst ticket to ask "show me high-risk
Manufacturing engineers under 12 months tenure."

LangChain SQL agent + schema injection + self-correction loop:
86% exact-match accuracy, 8 second latency.
```

### Tweet 8 (honest about AI use)

```
Built collaboratively with Copilot, Claude, and GPT-4.

This is the modern baseline. I disclose it openly in
AI_CONTRIBUTIONS.md. What matters: I can defend every design
decision in the codebase.

A candidate who uses AI well > one who claims not to.
```

### Tweet 9 (next steps)

```
Roadmap:

• Causal uplift modeling (causalml/econml) — predict the
  intervention, not just the leave
• Cox survival analysis — time-to-event, not just probability
• Federated training across multi-site enterprises
• Manager-trust field study (IRB)

Paper is on arXiv. Code is MIT licensed.
```

### Tweet 10 (the CTA)

```
🔗 GitHub: https://github.com/Dogiparthi-Sharada/attrisense
🎬 Live demo: https://attrisense.streamlit.app
📄 arXiv: https://arxiv.org/abs/XXXX.XXXXX

I'm an MSBA grad at @CalStateEastBay. Open to AI/ML/People
Analytics roles — DMs open.

If you build people analytics, RAG systems, or HR tech — I'd love
to learn from you.
```

---

## 🎯 Tagging strategy on X

Mention these where natural:
- `@OpenAI` `@LangChainAI` `@huggingface` `@streamlit` `@plotly`
- `@CalStateEastBay`
- `@Lumentum` (if they're on X — check first; many enterprise companies aren't very active)

---

## 📊 What "good" looks like for X

X has a *much* steeper power-law distribution than LinkedIn. Most threads die at <500 impressions. A "good" outcome:

| Metric | Below | Average | Strong | Viral |
|---|---|---|---|---|
| Impressions | <500 | 2,000 | 10,000 | 50,000+ |
| Likes | <10 | 30 | 100 | 500+ |
| Reposts | 0 | 2 | 8 | 50+ |
| Replies | 0 | 2 | 5 | 30+ |
| New followers | 0 | 5 | 20 | 100+ |

X is **lower job-yield** than LinkedIn — but **higher technical credibility**. A founder, ML researcher, or YC partner is more likely to find you here.

---

## 💡 Bonus — X-specific patterns that work

- **Numbered tweets** (1️⃣2️⃣3️⃣) outperform prose
- **The hook is everything** — first sentence must earn the click
- **One metric per tweet** — don't bury numbers in paragraphs
- **End with a clear CTA** — "DMs open" / "looking for X" / "follow for more"
- **Reply to your own thread** with extras (not in original 10) — keeps it bumped
- **Quote-tweet anyone who shares it** with a follow-up insight
