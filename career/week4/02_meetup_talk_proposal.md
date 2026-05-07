# Meetup / Conference Talk Proposal

> **Targets (in priority order):**
> 1. Bay Area Women in Analytics — monthly meetup, Tue evenings
> 2. PyData San Francisco — quarterly, lighter review bar
> 3. ODSC West (Anaheim) — autumn track
> 4. SF Python — hosts applied-ML talks

---

## Talk title (3 variants — pick one based on audience)

1. **Five modalities, one dashboard: shipping AttriSense, an open-source workforce-intelligence platform** *(generalist track)*
2. **Three production lessons that aren't in the textbook: SMOTE-after-split, RAG provider fallback, and identification-bias mitigation** *(applied-ML track)*
3. **Causal uplift, survival, and fairness gating in a real (synthetic) HR dataset** *(responsible AI track)*

---

## Abstract (250 words — drop into the CFP form)

> AttriSense is an open-source, MIT-licensed workforce-intelligence
> platform built around five model modalities sharing a single
> Streamlit dashboard: RandomForest+SMOTE classification (ROC-AUC
> 0.91 / PR-AUC 0.74 on a 5,000-row synthetic corpus), Cox
> proportional-hazards survival modelling (concordance 0.78), an
> EconML T-Learner for per-employee causal uplift across three
> intervention arms, multilingual retrieval-augmented generation
> over English, Spanish, and Hindi exit-interview text with a
> hashing-based local fallback when the OpenAI endpoint is
> unreachable, and a natural-language SQL agent backed by a
> 50-question TF-IDF gold-question safety net.
>
> This talk covers three production-hardening lessons that the
> academic literature underweights: (1) SMOTE-after-split — why
> rebalancing before train/test splitting silently leaks synthetic
> neighbours into the test fold and inflates AUC by 4+ points;
> (2) Reachability-probed RAG provider fallback — why every dashboard
> that calls a third-party endpoint needs a 250 ms DNS+TCP+HTTPS
> liveness probe and a per-provider FAISS index directory before
> shipping; and (3) Identification-bias mitigation via salted-hash
> Review_ID rendering — a 25-line module that does more for
> applied fairness than any post-hoc audit, because it stops
> reviewers from anchoring on memory and overriding the model.
>
> Live demo, 7-page IEEE paper, and 79-page beginner's-guide DOCX
> all linked. Code is reproducible from a single `seed=42`. The
> walk-through is aimed at applied-ML engineers and data scientists
> who ship to non-technical stakeholders.
>
> Speaker: Sharada Dogiparthi, MSBA candidate, California State
> University, East Bay.

---

## Talk outline (30 min + 10 Q&A)

| Time | Section | Key visual |
|------|---------|------------|
| 0:00–0:03 | Why one classifier isn't enough | KPI card screenshot |
| 0:03–0:08 | Modality 1 — RandomForest + SMOTE (lesson #1: SMOTE-after-split) | AUC curve before/after |
| 0:08–0:13 | Modality 2 — Cox PH (the *when* question) | Survival-curve screenshot |
| 0:13–0:18 | Modality 3 — EconML T-Learner (causal uplift) | 3-arm uplift bar chart |
| 0:18–0:23 | Modality 4 — Multilingual RAG (lesson #2: reachability probe + fallback) | Provider-fallback flow diagram |
| 0:23–0:26 | Modality 5 — NL→SQL with TF-IDF safety net | Live typing demo |
| 0:26–0:29 | Lesson #3 — Identification bias and the Review_ID layer | `E001 → RV-771131` before/after |
| 0:29–0:30 | Fairness gate · CTA · QR to repo | Pixel pastel end card |

---

## Speaker bio (60 words)

> *Sharada Dogiparthi is an MSBA candidate at California State
> University, East Bay, and the maintainer of AttriSense — an
> open-source, MIT-licensed five-modality workforce-intelligence
> platform combining predictive ML, Cox PH survival modelling,
> EconML causal uplift, multilingual RAG, and natural-language SQL
> with EEOC fairness gating and salted-hash pseudonymization.*

---

## Submission checklist

- ☐ Abstract pasted into CFP form (≤ 250 words usually)
- ☐ Headshot uploaded (PNG, 800×800, transparent or pastel bg)
- ☐ Three slide samples attached (cover, lesson #1, lesson #3)
- ☐ Bio link points at LinkedIn, not GitHub
- ☐ Author block matches the IEEE paper exactly
- ☐ "Past speaking experience" — can be empty (CFPs welcome
  first-time speakers; just say "first conference talk")

---

## After acceptance

- LinkedIn post: *"🎤 I'll be giving my first applied-ML conference
  talk at [event] on [date] — five modalities, three production
  lessons, one open-source repo. RSVP link in comments."*
- Add the talk to the README under "Talks & Press."
- Record it. Upload unlisted to YouTube. Embed in the README.
