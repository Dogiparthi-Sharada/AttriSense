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
