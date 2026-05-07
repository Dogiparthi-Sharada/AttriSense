# 90-Second Interview Pitch (out-loud script)

> Read aloud 5× before the call. The numbers are real (5,000 rows
> synthetic, ROC-AUC 0.91, Cox concordance 0.78). The structure is:
> hook → why → what (5 modalities in 4 sentences) → wins → close.

---

## The pitch (90 seconds, ~250 words)

*"Quickly — what I'm most proud of is **AttriSense**, an open-source
workforce-intelligence platform I built as my MSBA capstone at
Cal State East Bay.*

*The premise is simple: HR analytics today is overwhelmingly
descriptive — it tells you who left, not who's about to. AttriSense
flips that, using **five model modalities** stitched into one
Streamlit dashboard.*

*Modality one: a RandomForest classifier with SMOTE rebalancing —
ROC-AUC 0.91, PR-AUC 0.74 on a 5,000-row synthetic corpus.*

*Modality two: Cox proportional-hazards — concordance 0.78 — so the
dashboard answers not just "who is at risk" but "when".*

*Modality three: an EconML T-Learner that estimates per-employee
causal uplift across three intervention arms — compensation,
manager rotation, learning budget — so retention budgets aren't
flat-distributed.*

*Modality four: a multilingual RAG layer over exit-interview text in
English, Spanish, and Hindi, with a hashing-based local fallback
when the OpenAI endpoint is unreachable. The reachability probe is
250 ms.*

*Modality five: a natural-language SQL agent with a TF-IDF
gold-question safety net for the top 50 HR questions.*

*Every prediction is gated by an EEOC four-fifths fairness audit
before it ever reaches the screen, and the dashboard never displays
a raw employee ID — it shows a salted SHA-256 **Review_ID**, so
reviewers can't anchor on memory and bypass the model.*

*It's MIT-licensed, there's a 7-page IEEE paper, a 79-page
beginner's guide DOCX, and a live Streamlit demo. Happy to walk
through any layer in detail."*

---

## Three follow-up answers ready to fire

**"What's the hardest production lesson?"** — *"SMOTE-after-split.
My first run did SMOTE on the full dataset before the train/test
split, which leaks synthetic neighbours from the training fold into
the test fold. Test scores were artificially great. I rewrote the
pipeline so SMOTE only touches the training fold inside each
cross-validation iteration. Test AUC dropped 4 points and the model
became honest."*

**"How do you handle the LLM going down?"** — *"Two layers. The RAG
layer has a 250 ms reachability probe and a hashing-based local
fallback at 256 dimensions, with per-provider FAISS index
directories. The NL→SQL layer has a TF-IDF gold-question fallback
that answers 11 out of 50 gold questions correctly without any
LLM at all. The dashboard never blocks on a third-party endpoint."*

**"How would you scale this?"** — *"Same five modalities, three
swaps. Replace SQLite with Postgres or Snowflake. Replace the
synthetic generator with the customer's HRIS extract. Replace the
hashing fallback with an in-VPC embedding service like Bedrock.
Everything else — the fairness gate, the Review_ID layer, the Cox
PH and T-Learner — runs unchanged."*

---

## Tone notes

- Talk in *short* sentences. Five modalities in four sentences each.
- Numbers, then qualifier. "ROC-AUC 0.91" — pause — "PR-AUC matters
  more here because the positive class is 10%."
- Always tie a metric to a *decision*. PR-AUC ⇒ pick the metric that
  matches the cost of error. Concordance ⇒ Q3 calendar item, not a
  number. Causal uplift ⇒ retention budget allocation.
- End on the people, not the tech. "Both the data and the people in
  it" — the closing line of the video script — works in the call
  too.
