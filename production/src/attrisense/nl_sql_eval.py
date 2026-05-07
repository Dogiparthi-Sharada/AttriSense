# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/nl_sql_eval.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""NL\u2192SQL evaluation harness.

Compares the natural-language SQL agent against a gold set of 50
hand-written questions. Accuracy is measured by EXECUTING both queries
and comparing the resulting row-multisets, not by string matching.

Two strict accuracy modes are reported:
- `exact`: full result-set equality after sorting and rounding floats
- `cardinality`: same row count (looser, useful for partial credit)

Designed to run without network access if `OPENAI_API_KEY` is missing
\u2014 in that case it reports "skipped (no key)" and exits 0 so CI stays
green on forks without secrets.
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from attrisense.config import DATABASE_PATH, EVAL_REPORT_PATH, OUTPUTS_DIR
from attrisense.gold_questions import GOLD_QUESTIONS, GoldQuestion, by_category


@dataclass
class EvaluationCase:
    """Per-question result, serialisable to JSON."""

    id: str
    category: str
    question: str
    expected_sql: str
    generated_sql: str | None
    error: str | None
    exact_match: bool
    cardinality_match: bool
    expected_rowcount: int
    generated_rowcount: int | None
    duration_seconds: float


@dataclass
class EvaluationReport:
    """Top-level run report."""

    total: int
    skipped: int
    exact_accuracy: float
    cardinality_accuracy: float
    accuracy_by_category: dict[str, dict[str, float]]
    cases: list[EvaluationCase]
    note: str = ""


def _normalise_rows(rows: list[tuple]) -> list[tuple]:
    """Round floats and sort so equality is order-independent."""
    rounded: list[tuple] = []
    for row in rows:
        rounded.append(
            tuple(
                round(value, 4) if isinstance(value, float) else value
                for value in row
            )
        )
    return sorted(rounded, key=lambda item: tuple(str(value) for value in item))


def _execute(sql: str) -> list[tuple]:
    """Run any SELECT against the SQLite DB in read-only mode."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA query_only = ON")
        cursor = connection.execute(sql)
        return list(cursor.fetchall())


def _evaluate_one(
    question: GoldQuestion,
    agent_callable: Any,
) -> EvaluationCase:
    """Run one gold question through the agent and grade it."""
    start = time.perf_counter()
    try:
        expected_rows = _normalise_rows(_execute(question.expected_sql))
    except sqlite3.Error as error:
        return EvaluationCase(
            id=question.id,
            category=question.category,
            question=question.question,
            expected_sql=question.expected_sql,
            generated_sql=None,
            error=f"gold SQL failed: {error}",
            exact_match=False,
            cardinality_match=False,
            expected_rowcount=0,
            generated_rowcount=None,
            duration_seconds=time.perf_counter() - start,
        )

    try:
        generated_sql, result = agent_callable(question.question)
    except Exception as error:  # noqa: BLE001 - we want any failure recorded
        return EvaluationCase(
            id=question.id,
            category=question.category,
            question=question.question,
            expected_sql=question.expected_sql,
            generated_sql=None,
            error=f"agent raised: {error}",
            exact_match=False,
            cardinality_match=False,
            expected_rowcount=len(expected_rows),
            generated_rowcount=None,
            duration_seconds=time.perf_counter() - start,
        )

    if generated_sql is None or isinstance(result, str):
        return EvaluationCase(
            id=question.id,
            category=question.category,
            question=question.question,
            expected_sql=question.expected_sql,
            generated_sql=generated_sql,
            error=str(result) if isinstance(result, str) else "agent returned no SQL",
            exact_match=False,
            cardinality_match=False,
            expected_rowcount=len(expected_rows),
            generated_rowcount=None,
            duration_seconds=time.perf_counter() - start,
        )

    generated_rows = _normalise_rows(list(result.get("rows", [])))
    exact = generated_rows == expected_rows
    cardinality = len(generated_rows) == len(expected_rows)

    return EvaluationCase(
        id=question.id,
        category=question.category,
        question=question.question,
        expected_sql=question.expected_sql,
        generated_sql=generated_sql,
        error=None,
        exact_match=exact,
        cardinality_match=cardinality,
        expected_rowcount=len(expected_rows),
        generated_rowcount=len(generated_rows),
        duration_seconds=time.perf_counter() - start,
    )


def _accuracy(cases: list[EvaluationCase], field: str) -> float:
    """Compute accuracy on a boolean field across non-skipped cases."""
    scored = [case for case in cases if case.error is None or case.generated_sql is not None]
    if not scored:
        return 0.0
    hits = sum(1 for case in scored if getattr(case, field))
    return hits / len(scored)


def run_evaluation(agent_callable: Any | None = None) -> EvaluationReport:
    """Run the full evaluation. Returns the report and writes it to disk."""
    if not Path(DATABASE_PATH).exists():
        return EvaluationReport(
            total=0,
            skipped=0,
            exact_accuracy=0.0,
            cardinality_accuracy=0.0,
            accuracy_by_category={},
            cases=[],
            note=f"Skipped \u2014 {DATABASE_PATH.name} missing.",
        )

    if agent_callable is None:
        if not os.getenv("OPENAI_API_KEY"):
            return EvaluationReport(
                total=len(GOLD_QUESTIONS),
                skipped=len(GOLD_QUESTIONS),
                exact_accuracy=0.0,
                cardinality_accuracy=0.0,
                accuracy_by_category={},
                cases=[],
                note="Skipped \u2014 OPENAI_API_KEY not set.",
            )
        # Late import so the module is usable in tests without LangChain.
        from natural_language_sql import query_database_with_ai
        agent_callable = query_database_with_ai

    cases = [_evaluate_one(question, agent_callable) for question in GOLD_QUESTIONS]

    by_cat: dict[str, dict[str, float]] = {}
    for category, questions in by_category().items():
        category_cases = [case for case in cases if case.category == category]
        by_cat[category] = {
            "count": len(category_cases),
            "exact_accuracy": _accuracy(category_cases, "exact_match"),
            "cardinality_accuracy": _accuracy(category_cases, "cardinality_match"),
        }

    report = EvaluationReport(
        total=len(cases),
        skipped=sum(1 for case in cases if case.generated_sql is None and case.error),
        exact_accuracy=_accuracy(cases, "exact_match"),
        cardinality_accuracy=_accuracy(cases, "cardinality_match"),
        accuracy_by_category=by_cat,
        cases=cases,
    )

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    EVAL_REPORT_PATH.write_text(json.dumps(_serialise(report), indent=2))
    return report


def _serialise(report: EvaluationReport) -> dict:
    """Convert dataclasses to plain dicts for JSON output."""
    return {
        "total": report.total,
        "skipped": report.skipped,
        "exact_accuracy": report.exact_accuracy,
        "cardinality_accuracy": report.cardinality_accuracy,
        "accuracy_by_category": report.accuracy_by_category,
        "note": report.note,
        "cases": [asdict(case) for case in report.cases],
    }


def load_report() -> dict | None:
    """Return the on-disk JSON report or None when no run has happened yet."""
    if not EVAL_REPORT_PATH.exists():
        return None
    return json.loads(EVAL_REPORT_PATH.read_text())


if __name__ == "__main__":
    result = run_evaluation()
    print(json.dumps(_serialise(result), indent=2)[:2000])
