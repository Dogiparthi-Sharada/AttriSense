# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/nl_sql_fallback.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Graceful fallback when the LLM cannot produce a valid SQL query.

When the natural-language agent fails (no API key, parse error, blocked
tokens, network outage, ambiguous question), the dashboard should not
just print an exception. Instead it offers the user the closest matches
from the 50-question gold set so they can re-run with a known-good
phrasing.

We use a tiny, dependency-free TF-IDF cosine similarity ranker built on
top of standard library `Counter`. This keeps the fallback usable even
when `OPENAI_API_KEY` is unset and `langchain` cannot answer the
original question.
"""

from __future__ import annotations

import math
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass

from attrisense.config import DATABASE_PATH
from attrisense.gold_questions import GOLD_QUESTIONS, GoldQuestion


_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z_0-9]+")
_STOPWORDS = frozenset(
    {
        "the", "a", "an", "of", "in", "on", "for", "to", "is", "are",
        "do", "we", "have", "with", "and", "or", "show", "me", "what",
        "which", "how", "many", "by", "from",
    }
)


def _tokenise(text: str) -> list[str]:
    """Lowercase tokens with stopwords removed."""
    return [
        token.lower()
        for token in _TOKEN_RE.findall(text)
        if token.lower() not in _STOPWORDS
    ]


@dataclass(frozen=True)
class Suggestion:
    """A single fallback suggestion shown to the user."""

    question: str
    expected_sql: str
    score: float
    category: str


def _document_vectors() -> tuple[list[Counter[str]], dict[str, float]]:
    """Pre-compute TF and IDF over the gold question corpus."""
    documents = [Counter(_tokenise(question.question)) for question in GOLD_QUESTIONS]
    document_count = len(documents)
    document_frequency: Counter[str] = Counter()
    for document in documents:
        document_frequency.update(document.keys())
    idf = {
        token: math.log((document_count + 1) / (count + 1)) + 1
        for token, count in document_frequency.items()
    }
    return documents, idf


_DOCUMENTS, _IDF = _document_vectors()


def _vector(tokens: list[str]) -> dict[str, float]:
    """Build a TF-IDF vector for a tokenised query."""
    counts = Counter(tokens)
    return {
        token: count * _IDF.get(token, 1.0)
        for token, count in counts.items()
    }


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity over two sparse TF-IDF vectors."""
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[token] * b[token] for token in common)
    norm_a = math.sqrt(sum(value * value for value in a.values()))
    norm_b = math.sqrt(sum(value * value for value in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def suggest(question: str, top_k: int = 3) -> list[Suggestion]:
    """Return the closest gold questions for a free-text user input."""
    query_vector = _vector(_tokenise(question))
    scored: list[tuple[float, GoldQuestion]] = []
    for index, gold_question in enumerate(GOLD_QUESTIONS):
        document_vector = {
            token: count * _IDF.get(token, 1.0)
            for token, count in _DOCUMENTS[index].items()
        }
        score = _cosine(query_vector, document_vector)
        scored.append((score, gold_question))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        Suggestion(
            question=gold_question.question,
            expected_sql=gold_question.expected_sql,
            score=score,
            category=gold_question.category,
        )
        for score, gold_question in scored[:top_k]
        if score > 0
    ]


def execute_gold_sql(sql: str) -> dict[str, object]:
    """Run a gold SQL string against the read-only SQLite connection."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA query_only = ON")
        cursor = connection.execute(sql)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description or []]
    return {"columns": columns, "rows": rows}
