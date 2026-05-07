# ---------------------------------------------------------------------------
# AttriSense — production/tests/test_multilingual_rag.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Tests for the multilingual RAG hashing fallback."""

from __future__ import annotations

import math

from attrisense.multilingual_rag import HashingEmbeddings


def test_embed_query_returns_unit_vector() -> None:
    """The fallback must always return a unit-norm vector."""
    embedder = HashingEmbeddings(dimensions=128)
    vector = embedder.embed_query("hello world")
    norm = math.sqrt(sum(value * value for value in vector))
    assert abs(norm - 1.0) < 1e-6
    assert len(vector) == 128


def test_embed_documents_dimensions_match() -> None:
    """Document vectors must share the configured dimensionality."""
    embedder = HashingEmbeddings(dimensions=64)
    vectors = embedder.embed_documents(["one", "two", "three"])
    assert len(vectors) == 3
    assert all(len(vector) == 64 for vector in vectors)


def test_empty_string_returns_zero_or_unit_vector() -> None:
    """Empty input must not raise (norm protection in place)."""
    vector = HashingEmbeddings(dimensions=32).embed_query("")
    assert len(vector) == 32
