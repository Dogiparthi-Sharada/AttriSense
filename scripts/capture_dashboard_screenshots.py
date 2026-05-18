# ---------------------------------------------------------------------------
# AttriSense — scripts/capture_dashboard_screenshots.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Capture AttriSense dashboard screenshots via Playwright + system Chrome.

Uses Playwright's `channel="chrome"` to drive the locally-installed
Google Chrome (no chromium download needed). Captures the landing
banner, then clicks each tab and saves a full-page PNG.

Run:
    .venv/bin/python scripts/capture_dashboard_screenshots.py [--port 8503]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[1]
OUT_DOCS = REPO / "docs" / "images"
OUT_ASSETS = REPO / "assets"

# Tabs to capture. Streamlit tab labels match `st.tabs([...])` in production/streamlit_app.py.
# (slug, tab-label-substring)
TABS = [
    ("executive",       "Executive"),
    ("analytics",       "Detailed Analytics"),
    ("decision",        "Decision Tools"),
    ("shap",            "SHAP Insights"),
    ("compare",         "Compare"),
    ("survival",        "Survival & Calibration"),
    ("causal",          "Causal Uplift"),
    ("fairness",        "Fairness"),
    ("ai_assistant",    "AI Assistant"),
    ("nl2sql",          "NL\u2192SQL Eval"),
    ("rag",             "Multilingual RAG"),
    ("alerts",          "Alert Mock"),
    ("ethics",          "Ethics"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default=8503, type=int)
    ap.add_argument("--host", default="localhost")
    args = ap.parse_args()
    base = f"http://{args.host}:{args.port}/"

    OUT_DOCS.mkdir(parents=True, exist_ok=True)
    OUT_ASSETS.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=True,
                                    args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            device_scale_factor=2,  # retina
        )
        page = ctx.new_page()
        print(f"Loading {base} …")
        page.goto(base, wait_until="networkidle", timeout=45000)
        # Streamlit takes a moment to hydrate after networkidle.
        page.wait_for_selector("[data-testid='stAppViewContainer']", timeout=20000)
        time.sleep(2.5)

        # Banner / executive (default landing tab)
        banner_path = OUT_DOCS / "banner.png"
        page.screenshot(path=str(banner_path), full_page=False)
        print(f"  wrote {banner_path.relative_to(REPO)}")

        # Capture each tab
        for slug, label in TABS:
            try:
                page.locator(f"[data-baseweb='tab']:has-text('{label}')").first.click(timeout=8000)
            except Exception as e:
                print(f"  ! could not click tab {label!r}: {e}")
                continue
            time.sleep(2.2)  # let plotly + tables render
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            target = OUT_DOCS / f"{slug}.png"
            page.screenshot(path=str(target), full_page=True)
            print(f"  wrote {target.relative_to(REPO)}")

        browser.close()
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())
