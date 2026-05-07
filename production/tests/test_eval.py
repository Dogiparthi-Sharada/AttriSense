# ---------------------------------------------------------------------------
# AttriSense — production/tests/test_eval.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Tests for the gold question registry and the eval harness scaffolding."""

from __future__ import annotations

from attrisense.gold_questions import GOLD_QUESTIONS, by_category
from attrisense.nl_sql_eval import _normalise_rows


def test_gold_set_has_at_least_50_questions() -> None:
    """Marketing claims 50 gold questions; the suite must back that up."""
    assert len(GOLD_QUESTIONS) >= 50


def test_gold_set_categories_are_balanced() -> None:
    """No single category should dominate the suite."""
    bucket = by_category()
    assert set(bucket) >= {"count", "aggregate", "groupby", "topk", "filter"}
    for category, questions in bucket.items():
        assert len(questions) >= 5, category


def test_gold_question_ids_unique() -> None:
    """Question ids are used as filenames and report keys, must be unique."""
    ids = [question.id for question in GOLD_QUESTIONS]
    assert len(ids) == len(set(ids))


def test_normalise_rows_is_order_independent() -> None:
    """The normaliser must make row equality independent of ordering."""
    a = [(1, 0.1234567), (2, 0.7654321)]
    b = [(2, 0.7654321), (1, 0.1234567)]
    assert _normalise_rows(a) == _normalise_rows(b)
