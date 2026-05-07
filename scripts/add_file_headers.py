#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# AttriSense — scripts/add_file_headers.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Add a standardized MIT/author/version/date header to every .py and .md file
in the repo (skipping .venv, .git, site, logs, __pycache__, .ruff_cache,
archive, faiss_*, *.bak)."""
from __future__ import annotations

from pathlib import Path
from datetime import date
import re
import sys

REPO = Path(__file__).resolve().parents[1]
AUTHOR = "Sharada Dogiparthi"
EMAIL = "dogiparthi.sharada@gmail.com"
VERSION = "1.0.0"
TODAY = date.today().isoformat()
PROJECT = "AttriSense"

PY_HEADER = f'''# ---------------------------------------------------------------------------
# {PROJECT} — {{relpath}}
# ---------------------------------------------------------------------------
# Author : {AUTHOR} <{EMAIL}>
# Version: {VERSION}
# Date   : {TODAY}
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 {AUTHOR}. All rights reserved.
# ---------------------------------------------------------------------------
'''

MD_HEADER = f'''<!--
{PROJECT} — {{relpath}}
Author : {AUTHOR} <{EMAIL}>
Version: {VERSION}
Date   : {TODAY}
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 {AUTHOR}. All rights reserved.
-->

'''

SKIP_DIRS = {".git", ".venv", "site", "logs", "__pycache__", ".ruff_cache",
             "archive", "faiss_hr_index", "faiss_hr_index_multilingual",
             ".github", "node_modules"}
SKIP_NAMES = {"LICENSE", "LICENSE.md"}

HEADER_MARKER = f"Author : {AUTHOR}"


def should_skip(p: Path) -> bool:
    parts = set(p.relative_to(REPO).parts)
    if parts & SKIP_DIRS:
        return True
    if p.name in SKIP_NAMES:
        return True
    if p.suffix == ".bak" or ".bak." in p.name:
        return True
    return False


def add_py_header(p: Path) -> bool:
    text = p.read_text(encoding="utf-8")
    if HEADER_MARKER in text:
        return False  # already present
    rel = str(p.relative_to(REPO))
    header = PY_HEADER.format(relpath=rel)

    # Preserve shebang
    if text.startswith("#!"):
        first_nl = text.find("\n") + 1
        new = text[:first_nl] + header + text[first_nl:]
    else:
        new = header + text
    p.write_text(new, encoding="utf-8")
    return True


def add_md_header(p: Path) -> bool:
    text = p.read_text(encoding="utf-8")
    if HEADER_MARKER in text:
        return False
    rel = str(p.relative_to(REPO))
    header = MD_HEADER.format(relpath=rel)
    p.write_text(header + text, encoding="utf-8")
    return True


def main():
    py_added = py_skipped = 0
    md_added = md_skipped = 0
    for p in REPO.rglob("*"):
        if not p.is_file():
            continue
        if should_skip(p):
            continue
        try:
            if p.suffix == ".py":
                if add_py_header(p): py_added += 1
                else: py_skipped += 1
            elif p.suffix == ".md":
                if add_md_header(p): md_added += 1
                else: md_skipped += 1
        except Exception as e:
            print(f"  ! {p.relative_to(REPO)}: {e}", file=sys.stderr)
    print(f"py: added {py_added}, already-had {py_skipped}")
    print(f"md: added {md_added}, already-had {md_skipped}")


if __name__ == "__main__":
    main()
