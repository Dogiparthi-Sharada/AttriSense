"""Pytest configuration: makes the production package importable."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SRC_DIR = _REPO_ROOT / "production" / "src"

for path in (_SRC_DIR, _REPO_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
