<!--
AttriSense — docs/learn/index.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Learn — concepts behind AttriSense

> Plain-language explainers for every technique used in the dashboard. Read in order, or jump straight to whatever's confusing you.

| Tutorial | What you'll learn | Time |
|---|---|---|
| [SHAP — explain any prediction](shap.md) | Why a model said what it said, on a per-employee basis | 10 min |
| [SMOTE — handle class imbalance](smote.md) | Why oversampling minority classes works (and when it lies) | 8 min |
| [Cox PH — survival analysis](cox-ph.md) | "How long until X happens?" instead of "will X happen?" | 12 min |
| [Causal uplift — T-Learner](causal-uplift.md) | The difference between *prediction* and *intervention* | 12 min |
| [RAG — retrieval-augmented generation](rag.md) | Semantic search + LLM, with graceful fallback | 10 min |
| [Fairness — four-fifths rule](fairness.md) | EEOC's bright line, what it catches, what it misses | 10 min |
| [NL→SQL — text-to-database](nl-sql.md) | Translating English to SQL safely (read-only, allow-listed) | 8 min |

## How to read this section

Every tutorial follows the same shape:

1. **The intuition** (why this exists at all)
2. **The math, lightly** (what's actually happening)
3. **In AttriSense** (where the code lives, what it does)
4. **The gotcha** (the thing you'll get wrong on first read)
5. **Try it** (a one-liner you can paste)

If you want to read the production source instead, every tutorial links straight to it.
