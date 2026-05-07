# 07 — Live Demo Script (7 minutes)

For VP pitch, interview deep-dive, and patent-disclosure meetings.

**Setup checklist (before joining the call):**

- [ ] `streamlit run production/streamlit_app.py --server.port 8514`
- [ ] Browser zoom 90 %
- [ ] Tab #1 = AttriSense at port 8514
- [ ] Tab #2 = `06_one_pager_external.md` rendered as the "leave-behind"
- [ ] One-pager link copied to clipboard for the chat
- [ ] Demo dataset: default synthetic (5,000 employees)

---

## Timing breakdown

| Time | Surface | Talking point |
|------|---------|---------------|
| 0:00–0:30 | Banner + KPI row | "Five thousand employees, AUC 0.87, three of eleven cohorts gated. That last number is the headline." |
| 0:30–1:30 | Executive tab | Walk the 5 KPI cards → donut → dept bar (note royal-navy table headers, no colorbars). |
| 1:30–2:30 | SHAP Insights | Pick one Review_ID, show the 3 top drivers, **emphasise**: "Notice the ID is `RV-XXXXXX`. The reviewer never sees the raw employee_id." |
| 2:30–3:30 | Decision Tools → What-if Simulator | Slide salary raise 0 → 15 %, tenure +12 mo, manager change. "Note the slider only allows raises — pay cuts don't reduce flight risk; the lever is constrained to retention-positive moves." |
| 3:30–4:30 | Causal Uplift | "T-learner CATE over three arms. Qini 0.187 vs. correlation baseline 0.041 — a 4.5× lift." |
| 4:30–5:30 | Fairness | Show the per-cohort DI table; highlight a suppressed cohort. "This is fairness-as-gate, not fairness-as-flag. The recommendation literally cannot reach the manager until the gate clears." |
| 5:30–6:15 | NL→SQL Eval | Type "Top 5 departments by attrition risk in Q2"; demo the LLM answer; then **kill the network** and re-run; TF-IDF gold-question fallback answers in <800 ms. |
| 6:15–6:45 | Multilingual RAG | Spanish exit-interview snippet retrieved; provider down → 256-d hashing fallback; same render path. |
| 6:45–7:00 | Close | "Thirteen surfaces, p95 410 ms, US patent application pending. One-pager just dropped in the chat." |

---

## Anticipated Q&A (drop in 3-min reserve at the end)

| Q | A |
|---|---|
| "Why suppress instead of flag?" | "A flagged recommendation still influences the reviewer. Suppression is the only intervention that removes the bias from the decision path." |
| "What if my LLM provider is up but slow?" | "The 250 ms probe catches that; we route to fallback and log the latency reason." |
| "Is the synthetic data realistic?" | "Generator parameters published; we welcome a partner with real anonymised data to validate generalisation." |
| "Could a reviewer reverse the salt?" | "HMAC-SHA256 with monthly salt rotation; the mapping table lives in an audit-only datastore. Reviewer role does not have read access." |
| "Why T-learner not X-learner?" | "T-learner gives interpretable per-arm outcomes, which the fairness audit needs. X-learner is on the future-work list." |
| "Cost to run?" | "Commodity laptop, 16 GB RAM, no GPU, free tier of any LLM provider. Total cloud bill in the demo: $0." |

---

## Don'ts

- Don't open with the architecture diagram. Open with the headline number
  (3 of 11 cohorts gated).
- Don't show code. The demo is the artefact.
- Don't apologise for synthetic data — frame it as the responsible choice.
- Don't promise a date for paper acceptance or patent grant.
