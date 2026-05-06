"""Launch AttriSense as a publicly bound Streamlit app."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DASHBOARD = ROOT / "dashboard.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AttriSense with Streamlit.")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host/IP address for Streamlit to bind to. Defaults to 0.0.0.0 for public binding.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port for Streamlit. Defaults to 8501.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not DASHBOARD.exists():
        print(f"Could not find Streamlit dashboard at {DASHBOARD}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(DASHBOARD),
        f"--server.address={args.host}",
        f"--server.port={args.port}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    print("Starting AttriSense...")
    print(f"Local URL:   http://localhost:{args.port}")
    print(f"Public bind: http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server.")

    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
