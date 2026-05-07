<!--
AttriSense — docs/learn/nl-sql.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# NL→SQL — text-to-database

> *"Show me the high-risk employees in Manufacturing"* → `SELECT * FROM workforce_predictions WHERE department='Manufacturing' AND risk_label='High Risk'`. Done well, this is delightful. Done poorly, it's a security incident.

## The intuition

Three approaches, in order of complexity:

1. **Gold-question lookup** — match the user's question to a hand-crafted list of `(question, sql)` pairs via TF-IDF or embedding similarity. **Zero hallucination, zero LLM cost.**
2. **LLM generation with allow-list** — let an LLM produce SQL but reject anything that's not `SELECT` against an approved table set.
3. **LLM generation with sandboxed execution** — run the SQL in a read-only transaction with row-level limits.

AttriSense uses **(1) as fallback and (2) as primary**, with (3) as the sandbox for both.

## The math, lightly

TF-IDF similarity between user query $q$ and gold question $g$:

$$
\text{sim}(q, g) = \frac{\text{tfidf}(q) \cdot \text{tfidf}(g)}{\|\text{tfidf}(q)\| \, \|\text{tfidf}(g)\|}
$$

Pick the gold question with the highest similarity, return its SQL. If similarity is below a threshold, give up and say *"I don't know — try one of these examples"*.

## In AttriSense

- **Primary**: [`natural_language_sql.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/natural_language_sql.py) — LangChain SQL chain over OpenAI.
- **Fallback**: [`production/src/attrisense/nl_sql_fallback.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/nl_sql_fallback.py) — TF-IDF over the gold-question set.
- **Eval**: [`production/src/attrisense/nl_sql_eval.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/nl_sql_eval.py) — 50 gold questions across 4 categories (KPI, group, drill, trend).
- **Sandbox**:
  - SQLite connection opened with `PRAGMA query_only=ON`.
  - SQL allow-list: `SELECT` only; `INSERT/UPDATE/DELETE/DROP/PRAGMA/ATTACH` rejected.
  - Result row limit (default 200).

## The gotcha

**LLM-generated SQL is a SQL injection vector** if you don't sandbox. Without the read-only PRAGMA + allow-list, a sufficiently creative prompt can `DROP TABLE` your production database. AttriSense's sandbox is non-negotiable — never disable it.

Also: the LLM will confidently produce SQL that **runs but is wrong**. Use the eval harness (`make eval`) on every PR that touches the prompt.

## Try it

```python
from attrisense.nl_sql_fallback import answer

result = answer("show high-risk employees in manufacturing")
print(result["sql"])           # the SQL it would run
print(result["confidence"])    # similarity to nearest gold question
print(result["rows"][:5])      # the actual rows
```
