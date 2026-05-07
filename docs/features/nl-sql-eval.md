<!--
AttriSense — docs/features/nl-sql-eval.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# NL→SQL Evaluation Harness

> A 50-question gold set + automated scorer. Tells you objectively whether the AI Assistant is working.

## What you see

- **Run-evaluation button** — kicks off the harness.
- **Pass-rate KPI** — % of gold questions that produced a correct row count + matching values.
- **Per-question table** — ID, category, question, exact_match, cardinality_match, expected vs. generated rowcount, duration, error.
- **Category breakdown** — pass rate by question type (count, aggregate, groupby, topk, filter).

## What it answers

| Question | Where |
|---|---|
| Is the LLM still working? | Pass-rate KPI |
| Is one question category broken? | Category breakdown |
| Which specific questions fail? | Per-question table — sort by `exact_match=False` |
| How fast is the chain? | `duration_seconds` column |

## The 50 gold questions

Curated in [`gold_questions.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/gold_questions.py) — 10 questions per category:

| Category | Example | Count |
|---|---|---|
| **count** | "How many high-risk employees are in Manufacturing?" | 10 |
| **aggregate** | "What is the average tenure of high-risk employees?" | 10 |
| **groupby** | "Risk count by department" | 10 |
| **topk** | "Top 5 highest-risk employees" | 10 |
| **filter** | "All employees in Engineering with risk above 0.8" | 10 |

Each gold question carries:

- `id` — stable identifier
- `category` — for breakdown
- `question` — the natural-language input
- `expected_sql` — hand-validated SQL (used by the fallback ranker)
- `expected_rowcount` — for cardinality match
- `expected_signature` — column types for shape matching

The full list is enumerated at [Gold questions](../reference/nl-sql-gold-questions.md).

## Code path

```
production/streamlit_app.py
  └── _eval_tab(df)
       └── nl_sql_eval.run_evaluation(GOLD_QUESTIONS)
            ├── For each gold question:
            │    ├── _execute(question)         ← LLM-generated SQL
            │    ├── _normalise_rows(...)       ← order-insensitive comparison
            │    └── EvaluationCase(passed=bool)
            └── EvaluationReport(pass_rate, per_case_results)
```

[`nl_sql_eval.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/nl_sql_eval.py) — 239 lines, tested by [`test_eval.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/tests/test_eval.py).

## Why two metrics (exact_match + cardinality_match)

- **`cardinality_match`** is True when the row count matches. Cheap. Catches most failures.
- **`exact_match`** is True when row count *and* values match (after normalisation — sort + lowercase + strip). Stricter. Catches off-by-one filters and column-order mistakes.

A question that scores `cardinality_match=True, exact_match=False` is suspicious — the LLM got the *shape* right but *content* wrong. That's worth investigating.

## Output artifact

`make -C production eval` writes `outputs/nl_sql_eval_report.json`:

```json
{
  "ran_at": "2026-05-07T14:32:11Z",
  "pass_rate": 0.42,
  "by_category": {
    "count": 0.7, "aggregate": 0.5, "groupby": 0.4, "topk": 0.3, "filter": 0.3
  },
  "cases": [
    {
      "id": 1, "category": "count",
      "question": "How many high-risk employees are in Manufacturing?",
      "exact_match": true, "cardinality_match": true,
      "expected_rowcount": 1, "generated_rowcount": 1,
      "duration_seconds": 0.84, "error": null
    }
  ]
}
```

The dashboard reads this file when you load the tab — re-run the harness to refresh.

## Why this is essential for any LLM feature

LLMs degrade silently. A model upgrade, a prompt tweak, or an unrelated dependency bump can drop your SQL accuracy from 80% to 30% overnight. Without a harness like this, you find out from a user complaint.

With this harness:

- Wire `make eval` into CI on a nightly schedule.
- Alert if pass-rate drops below threshold.
- Compare reports across model versions.

This is the **eval-driven development** pattern — borrowed from production LLM teams who pay the price for skipping it.

## Without an OpenAI key

The eval tab is hidden when no key is detected. The fallback TF-IDF ranker doesn't get evaluated here because it's deterministic by design — its "accuracy" is the cosine ranking, which is testable directly via [`test_nl_sql_fallback.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/tests/test_nl_sql_fallback.py).
