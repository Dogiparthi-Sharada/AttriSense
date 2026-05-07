<!--
AttriSense — docs/reference/nl-sql-gold-questions.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# NL→SQL gold questions

> The 50 hand-validated NL→SQL pairs that power the [Eval Harness](../features/nl-sql-eval.md) and the [Fallback Ranker](../features/ai-assistant.md#fallback-ranker-the-offline-path).

Source: [`production/src/attrisense/gold_questions.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/gold_questions.py)

## Format

Each `GoldQuestion` is a frozen dataclass:

```python
@dataclass(frozen=True)
class GoldQuestion:
    id: int                    # stable identifier 1..50
    category: str              # one of {count, aggregate, groupby, topk, filter}
    question: str              # natural language input
    expected_sql: str          # hand-validated SQL
    expected_rowcount: int     # for cardinality_match
    expected_signature: tuple  # column types, for shape match
```

## Categories

10 questions per category × 5 categories = 50 questions.

### Count (10)

Questions that should return a single integer.

Examples:
- "How many high-risk employees are in Manufacturing?"
- "How many employees have manager tenure under 6 months?"
- "Number of employees in Engineering with risk above 0.5?"

### Aggregate (10)

Questions that should return a single numeric statistic.

Examples:
- "What is the average tenure of high-risk employees?"
- "Median salary in the Sales department?"
- "Maximum risk score across the dataset?"

### Group-by (10)

Questions that should return one row per group.

Examples:
- "Risk count by department"
- "Average salary by manager"
- "Number of high-risk employees by department"

### Top-K (10)

Questions that should return a small ordered list.

Examples:
- "Top 5 highest-risk employees"
- "10 employees with the shortest tenure"
- "Top 3 departments by average risk"

### Filter (10)

Questions that should return all matching rows.

Examples:
- "All employees in Engineering with risk above 0.8"
- "Employees whose recommended intervention is manager_change"
- "Manufacturing employees with tenure under 12 months"

## Why hand-validated SQL

Two reasons:

1. **Eval correctness** — the gold SQL is the ground truth. Without it, you can't tell if the LLM's answer is right.
2. **Safe fallback** — when the LLM is offline, the fallback ranker runs the gold SQL directly. Hand-validated = guaranteed correct = safe to execute.

Every gold question's SQL was tested against the synthetic DB and visually verified before being added.

## How to add a new gold question

1. Open [`gold_questions.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/gold_questions.py).
2. Append a new `GoldQuestion(...)` to the `GOLD_QUESTIONS` tuple.
3. Pick the right category (or add a new one — the eval supports it).
4. Run the SQL manually in `sqlite3 hr_enterprise.db` to capture `expected_rowcount`.
5. Run `make -C production eval` to confirm the harness picks it up.

## How questions are ranked in the fallback

```python
# nl_sql_fallback.py
TfidfVectorizer(ngram_range=(1, 2), lowercase=True)
   .fit_transform(["how many high risk employees are in manufacturing?", ...])

user_vec = vectorizer.transform([user_query])
similarities = cosine_similarity(user_vec, all_question_vecs).flatten()
top_3 = np.argsort(-similarities)[:3]
```

Simple, deterministic, fast. No LLM required. Vectoriser is fitted once at import time.

## Limitations of this approach

- **No paraphrase robustness** — "show me high-risk Manufacturing folks" matches "high-risk Manufacturing employees" via TF-IDF, but "people about to quit in the assembly department" matches poorly. Real systems would use embeddings here too.
- **Fixed SQL** — the fallback can't compose new queries; it can only run pre-validated ones.
- **English only** — gold questions are in English. A multilingual ranker would need translated questions.

These are acceptable tradeoffs for a fallback. The full LLM path handles paraphrases and novel queries — the fallback is the **safety net**, not the primary UX.
