"""Test the NL\u2192SQL fallback ranker."""

from __future__ import annotations

from attrisense.nl_sql_fallback import suggest


def test_suggest_returns_top_k_results() -> None:
    """Top-k must be respected and results sorted by score descending."""
    results = suggest("how many high risk employees are in manufacturing", top_k=3)
    assert 1 <= len(results) <= 3
    scores = [item.score for item in results]
    assert scores == sorted(scores, reverse=True)


def test_suggest_finds_obvious_match() -> None:
    """A near-exact phrasing should rank the corresponding gold Q first."""
    results = suggest("count employees in each department", top_k=1)
    assert results
    assert "department" in results[0].question.lower()


def test_suggest_handles_empty_query() -> None:
    """Empty queries must not raise."""
    assert suggest("", top_k=3) == []
