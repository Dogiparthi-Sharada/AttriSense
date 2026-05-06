"""Launch AttriSense as a publicly bound Streamlit app."""

from __future__ import annotations

import argparse
import subprocess
import sys

from config import DASHBOARD_PATH, DATABASE_PATH, ROOT_DIR


def parse_args() -> argparse.Namespace:
    """Read command-line options for host and port.

    Returns:
        Parsed arguments used to build the Streamlit command.
    """
    parser = argparse.ArgumentParser(description="Run AttriSense with Streamlit.")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host/IP address for Streamlit to bind to.",
    )
    parser.add_argument("--port", type=int, default=8501, help="Streamlit port.")
    return parser.parse_args()


def main() -> int:
    """Start Streamlit with production-friendly defaults.

    Returns:
        The Streamlit process exit code.
    """
    args = parse_args()

    if not DASHBOARD_PATH.exists():
        print(f"Dashboard not found: {DASHBOARD_PATH}", file=sys.stderr)
        return 1

    if not DATABASE_PATH.exists():
        print(
            f"Warning: {DATABASE_PATH.name} was not found. "
            "Run `python train_retention_risk_model.py` if the dashboard has no data.",
            file=sys.stderr,
        )

    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(DASHBOARD_PATH),
        f"--server.address={args.host}",
        f"--server.port={args.port}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]

    # Use the same Python executable that launched this script. That avoids
    # accidentally running Streamlit from a different virtual environment.
    print("Starting AttriSense")
    print(f"Local URL:   http://localhost:{args.port}")
    print(f"Public bind: http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop the server.")

    return subprocess.call(command, cwd=ROOT_DIR)


if __name__ == "__main__":
    raise SystemExit(main())
