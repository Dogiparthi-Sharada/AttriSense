# 🎴 Carousel Launch Day — Tuesday May 19

> Different audience than Week 2. Tech audience, not HR audience.
> Goal: technical credibility + repo stars.

---

## ⏱️ Hour-by-hour

### 8:25 AM PT
- Open AuthoredUp. Paste the carousel caption from `week2/05_linkedin_carousel_spec.md`. Bold key terms.
- Have the PDF ready to upload.

### 8:30 AM PT — POST GOES LIVE
Upload the PDF carousel + caption. Hit publish.

### 8:31 AM PT — FIRST COMMENT
```
🔗 Repo (now with SHAP explainability — added Sat over coffee):
https://github.com/Dogiparthi-Sharada/attrisense

🎬 Live demo:
https://attrisense.streamlit.app

📄 arXiv preprint:
https://arxiv.org/abs/XXXX.XXXXX

📖 Technical deep-dive on Towards Data Science:
[link]

If you're building people analytics, RAG over enterprise data, or
NL→SQL agents — I'd love to compare notes. DMs open.
```

### 8:32 AM PT — Cross-post to X

Drop a single image (slide 3 — the architecture diagram) with abbreviated text:

```
The AttriSense architecture in one image.

3 layers:
🎯 Predictive (RF + SMOTE)
🧠 RAG (FAISS over exit interviews)
💬 NL→SQL (LangChain agent)

The unlock isn't any one piece — it's how they compose. SHAP feeds
the RAG retrieval. RAG output grounds the manager rationale.

Repo: github.com/Dogiparthi-Sharada/attrisense
```

### 8:33 AM – 9:30 AM — Golden hour engagement

Same rules as Week 2:
- Reply to every comment within 5 min
- Like every comment
- Use the response bank
- Don't argue, don't oversell

This audience will ask **harder technical questions** than Week 2. Have these answers ready:

**Q: "What about XGBoost / GBM?"**
> *"Fair question — RF was the chosen baseline, RF+SMOTE on this data gave PR-AUC 0.74. XGBoost would likely give 1–3% lift. Benchmarking it for the v2 paper. Hot take: on tabular HR data of this scale, the model choice matters less than the feature engineering."*

**Q: "Why not fine-tune an LLM on the tabular data?"**
> *"Considered it. The rare-class problem actually gets worse with fine-tuned LLMs unless you've got 100K+ samples. And for explainability, RF + SHAP wins by a mile right now. If I had real Lumentum data and 6 months, I'd revisit."*

**Q: "How do you evaluate RAG output quality?"**
> *"Currently human-graded on a 30-example sample (1–5 Likert for 'is the rationale supported by the retrieved evidence?'). Mean 4.3. For production, I'd add a fact-check pass — second LLM call validates every claim. Open to better evaluation methodology if you've got pointers."*

### 11:00 AM PT — Send 5 cold-but-warm DMs

Use Template 5 from `week2/03_cold_dm_templates.md` (people building similar things). Source from:
- LangChain user gallery
- HuggingFace Spaces tagged "people-analytics"
- GitHub `topic:hr-analytics`

### 4:00 PM PT — Drop a follow-up comment

```
A few people asked about the SHAP+RAG combination — what makes it
non-obvious to me is that the SHAP attributions become the
*retrieval query*, not just the explanation. So the RAG context
is grounded in what the model actually thinks is driving the
risk, not arbitrary metadata.

That's the design choice I'm happiest with. Patent claim under
review with my university tech-transfer office.
```

> **Why this comment:** Plants the *patent-pending* signal early without overclaiming. Hiring managers love this kind of signal.

---

## 📊 What "good" looks like

Tech audience is harder to impress than HR audience but converts at higher quality:

| Metric | Below | Average | Strong |
|---|---|---|---|
| Impressions | <800 | 3,000 | 10,000 |
| Reactions | <30 | 100 | 300 |
| Comments | <8 | 25 | 60 |
| Repo stars Δ | <5 | 20 | 80 |
| New followers | <8 | 30 | 100 |
| **Real conversations** | <2 | 5 | 15 |

The **real-conversations** number is the only one that matters for the job search.

---

## 🎁 Bonus: pin the carousel

After 24 hours, **pin the carousel to your profile** as the featured post. Carousels stay relevant in feeds for ~3–5 days; pinning extends discoverability for anyone visiting your profile cold.
