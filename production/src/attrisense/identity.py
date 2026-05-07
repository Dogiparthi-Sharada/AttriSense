"""Pseudonymized identifiers for dashboard display.

The model never sees ``Emp_ID``; it is purely a join key. But a human
reviewer who recognises an ``Emp_ID`` (e.g. "EMP_2417 = Ravi") can
introduce *identification bias* into manual decisions.

This module produces a stable, deterministic pseudonym (``review_id``) for
display in the UI. The mapping is one-way for the dashboard process — to
recover the original ``Emp_ID`` from a ``review_id`` you must consult the
access-controlled mapping table maintained outside this codebase.

The pseudonym format is ``RV-NNNNNN`` (six digits, zero-padded), derived
from a SHA-256 over a salted ``Emp_ID``. The salt is read from the
``ATTRISENSE_REVIEW_ID_SALT`` environment variable so that mapping rotation
is operationally trivial.
"""
from __future__ import annotations

import hashlib
import os
from functools import lru_cache
from typing import Iterable

import pandas as pd

_DEFAULT_SALT = "attrisense:review-id:v1"


def _salt() -> str:
    return os.environ.get("ATTRISENSE_REVIEW_ID_SALT", _DEFAULT_SALT)


@lru_cache(maxsize=8192)
def to_review_id(emp_id: int | str) -> str:
    """Return a stable ``RV-NNNNNN`` review-id for the given Emp_ID."""
    h = hashlib.sha256(f"{_salt()}|{emp_id}".encode("utf-8")).hexdigest()
    # Take the first 24 bits → up to ~16.7M; mod 1_000_000 → 6 digits.
    n = int(h[:6], 16) % 1_000_000
    return f"RV-{n:06d}"


def review_id_series(emp_ids: Iterable) -> pd.Series:
    """Vectorised helper: return a Series of review_ids."""
    return pd.Series([to_review_id(e) for e in emp_ids], index=getattr(emp_ids, "index", None))
