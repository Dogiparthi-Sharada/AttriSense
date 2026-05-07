<!--
AttriSense — career/week1/01_AI_CONTRIBUTIONS.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# `AI_CONTRIBUTIONS.md` — drop into repo root

> Paste the block below into `AI_CONTRIBUTIONS.md` at the repository
> root. It is a transparency artefact, not legalese: a recruiter,
> reviewer, or hiring manager should be able to read it in 90 seconds
> and understand exactly which parts of AttriSense were AI-assisted
> and which were human design.

---

```markdown
# AI Contributions to AttriSense

> Maintained by Sharada Dogiparthi. Last updated: May 7, 2026.

This codebase was built with active assistance from large-language-
model (LLM) coding tools (GitHub Copilot, Anthropic Claude, OpenAI
GPT-4-class models). This document declares which parts of the system
were AI-drafted, AI-reviewed, or fully human-authored, and how the
final design decisions were made.

## Decisions: 100% human

Every architectural and modelling decision is mine:

- The choice to ship **five model modalities** (RandomForest with
  SMOTE, Cox proportional-hazards survival, EconML T-Learner causal
  uplift, multilingual RAG with provider fallback, and NL→SQL with a
  TF-IDF safety net) — and the explicit decision to keep them
  *separable* so any one can be replaced without touching the rest.
- The decision to **never display raw `Emp_ID`** in the dashboard —
  reviewers anchor on memory and bypass the model. The salted
  Review_ID pattern (`RV-NNNNNN`) was my call.
- The four-fifths fairness gate as a *blocking* check, not a banner.
- The DNS + TCP + HTTPS reachability probe before every OpenAI call,
  with per-provider FAISS index directories so 1536-d and 256-d
  vectors never collide.
- The Pixel pastel theme — cream canvas, lavender/peach/sage accents,
  black-ink axes — and the regular-weight typography rule.

## Code: AI-drafted, human-reviewed

LLM tools accelerated:

- Boilerplate Streamlit layout (tab containers, metric cards, theme CSS).
- `production/src/attrisense/theme.py` Pixel pastel CSS block — drafted
  by Claude, then I reworked the gradients, axis colours, and chart
  layout overrides.
- `scripts/generate_doc_diagrams.py` Pillow drawing primitives (`Card`
  class with anchored `.left()/.right()/.top()/.bottom()`).
- `paper/build_docx.py` markdown-driven IEEE-styled DOCX generator.
- `scripts/capture_dashboard_screenshots.py` Playwright + Chrome
  channel selection.
- Refactors of `compare.py`, `slack_alert_mock.py`, and the new
  `production/src/attrisense/identity.py` (`to_review_id` salted hash)
  were proposed by an LLM and accepted after review.

## Code: 100% human-authored

- The 5,000-row synthetic-data generator (`make synthetic-data`).
- The Cox PH covariate selection in `production/scripts/train_cox_ph.py`.
- The T-Learner treatment-arm definitions (compensation, manager
  rotation, learning budget) in `production/src/attrisense/uplift.py`.
- The 50-question NL→SQL gold set under `production/data/nlsql_gold/`.
- The `paper/attrisense_ieee.tex` paper text (intro, lessons-learned,
  identification-bias subsection, all four tables, the algorithm).

## Verification

I cannot verify every line an LLM produced. I *can* verify outputs:

- Every model artefact is reproducible from `seed=42`. `make train`
  always yields the same `attrisense_model.joblib` and the same SHAP
  attributions to 6 decimal places.
- The fairness audit, calibration error, and Cox concordance are
  recomputed on every CI run from the synthetic dataset.
- The 50-question NL→SQL gold set has held-out evaluations
  (TF-IDF fallback wins on 11/50; LLM wins on the rest).
- The Pixel-pastel screenshots in `docs/images/` were captured against
  the current dashboard; they are not LLM-generated images.

## Disclosure obligations

If a downstream user runs AttriSense on real employee data, they are
responsible for their own:

- Bias audit (NYC Local Law 144 if New York-based).
- Model card / risk assessment (EU AI Act, high-risk systems).
- Pseudonymization key custody (the `ATTRISENSE_REVIEW_ID_SALT`
  environment variable should be rotated per pilot).
```

---

## Why this doc matters

Recruiters in 2026 do not ask "did you use AI?" — they assume yes.
They ask: "where, why, and how did you verify it?" This document
answers all three in under two pages, which both demonstrates
maturity and pre-empts the awkward conversation in round 3.
