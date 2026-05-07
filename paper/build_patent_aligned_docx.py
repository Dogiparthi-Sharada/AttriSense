# ---------------------------------------------------------------------------
# AttriSense — paper/build_patent_aligned_docx.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Build attrisense_patent_aligned.docx — IEEE-style, python-docx only.

Calls the existing build_docx.main() with patched MD/OUT paths. No pandoc.
"""
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import build_docx as bd

bd.MD = HERE / "attrisense_patent_aligned.md"
bd.OUT = HERE / "attrisense_patent_aligned.docx"

bd.main()
print(f"wrote {bd.OUT}")
