"""Create README images and text outputs from the real AttriSense pipeline."""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

from config import DATABASE_PATH, ROOT_DIR, SQL_TABLE_NAME


ASSETS_DIR = ROOT_DIR / "assets"
OUTPUTS_DIR = ROOT_DIR / "outputs"
SOURCE_ARCHITECTURE_PATH = ROOT_DIR / "doc" / "architecture_diagram.png"
WIDTH = 1600
HEIGHT = 980
COLORS = {
    "ink": "#111827",
    "muted": "#64748b",
    "panel": "#ffffff",
    "line": "#d1d5db",
    "bg": "#f8fafc",
    "High Risk": "#d64550",
    "Medium Risk": "#f0a202",
    "Low Risk": "#1f9d75",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a readable system font and fall back safely when unavailable.

    Args:
        size: Font size in pixels.
        bold: Whether to request a bold font face.

    Returns:
        A Pillow font object used for drawing README images.
    """
    candidates = ["arialbd.ttf", "Arial Bold.ttf"] if bold else ["arial.ttf", "Arial.ttf"]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, selected_font: ImageFont.ImageFont) -> tuple[int, int]:
    """Measure text width and height using Pillow's modern bounding-box API."""
    left, top, right, bottom = draw.textbbox((0, 0), text, font=selected_font)
    return right - left, bottom - top


def draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    center_x: int,
    y: int,
    selected_font: ImageFont.ImageFont,
    fill: str,
) -> None:
    """Draw one line of text centered around an x-coordinate."""
    width, _ = text_size(draw, text, selected_font)
    draw.text((center_x - width / 2, y), text, font=selected_font, fill=fill)


def wrap_text_to_width(
    draw: ImageDraw.ImageDraw,
    text: str,
    selected_font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    """Split text into lines that fit inside a fixed-width diagram card.

    Args:
        draw: Pillow drawing context used for accurate text measurement.
        text: Text to fit inside the card.
        selected_font: Font used to measure and draw the text.
        max_width: Maximum line width in pixels.

    Returns:
        A list of lines that can be drawn without bleeding outside the card.
    """
    words = text.split()
    lines: list[str] = []
    current_line = ""

    for word in words:
        candidate = f"{current_line} {word}".strip()
        candidate_width, _ = text_size(draw, candidate, selected_font)
        if candidate_width <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    selected_font: ImageFont.ImageFont,
    fill: str,
    max_width: int,
    line_gap: int = 8,
) -> int:
    """Draw text line by line and return the y-coordinate below the final line."""
    x, y = xy
    line_height = text_size(draw, "Ag", selected_font)[1] + line_gap
    for line in wrap_text_to_width(draw, text, selected_font, max_width):
        draw.text((x, y), line, font=selected_font, fill=fill)
        y += line_height
    return y


def draw_card(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    label: str,
    value: str,
    accent: str,
) -> None:
    """Draw a KPI card used in the product overview image."""
    draw.rounded_rectangle(xy, radius=24, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    x1, y1, x2, _ = xy
    draw.rectangle((x1, y1, x1 + 10, xy[3]), fill=accent)
    draw.text((x1 + 34, y1 + 28), label.upper(), font=font(20, bold=True), fill=COLORS["muted"])
    draw.text((x1 + 34, y1 + 66), value, font=font(42, bold=True), fill=COLORS["ink"])
    draw.line((x1 + 34, y1 + 126, x2 - 28, y1 + 126), fill="#e5e7eb", width=2)


def draw_header(draw: ImageDraw.ImageDraw, title: str, subtitle: str) -> None:
    """Draw a consistent image header for all generated assets."""
    draw.text((70, 50), title, font=font(48, bold=True), fill=COLORS["ink"])
    draw.text((72, 112), subtitle, font=font(24), fill=COLORS["muted"])


def draw_donut(
    draw: ImageDraw.ImageDraw,
    values: dict[str, int],
    box: tuple[int, int, int, int],
) -> None:
    """Draw a donut chart using risk-band counts.

    Args:
        draw: Pillow drawing context.
        values: Mapping of risk band to employee count.
        box: Outer chart bounds as `(left, top, right, bottom)`.
    """
    total = sum(values.values())
    start = -90
    for label, value in values.items():
        angle = 360 * value / total
        draw.pieslice(box, start, start + angle, fill=COLORS[label])
        start += angle

    x1, y1, x2, y2 = box
    inset = 76
    draw.ellipse((x1 + inset, y1 + inset, x2 - inset, y2 - inset), fill=COLORS["panel"])
    draw_centered(draw, f"{total:,}", (x1 + x2) // 2, (y1 + y2) // 2 - 22, font(42, bold=True), COLORS["ink"])
    draw_centered(draw, "employees", (x1 + x2) // 2, (y1 + y2) // 2 + 28, font(20), COLORS["muted"])


def draw_horizontal_bars(
    draw: ImageDraw.ImageDraw,
    values: dict[str, int],
    x: int,
    y: int,
    width: int,
    bar_height: int,
) -> None:
    """Draw simple horizontal bars for department high-risk concentration."""
    max_value = max(values.values()) or 1
    for index, (label, value) in enumerate(values.items()):
        top = y + index * 86
        draw.text((x, top), label, font=font(24, bold=True), fill=COLORS["ink"])
        draw.rounded_rectangle((x, top + 34, x + width, top + 34 + bar_height), radius=14, fill="#e5e7eb")
        filled_width = int(width * value / max_value)
        draw.rounded_rectangle((x, top + 34, x + filled_width, top + 34 + bar_height), radius=14, fill="#2563eb")
        draw.text((x + width + 24, top + 28), f"{value:,}", font=font(26, bold=True), fill=COLORS["ink"])


def load_metrics() -> dict[str, object]:
    """Read the SQLite prediction table and return metrics used in README assets."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        total = cursor.execute(f"SELECT COUNT(1) FROM {SQL_TABLE_NAME}").fetchone()[0]
        risk_counts = dict(
            cursor.execute(
                f"""
                SELECT Risk_Level, COUNT(1)
                FROM {SQL_TABLE_NAME}
                GROUP BY Risk_Level
                ORDER BY COUNT(1) DESC
                """
            ).fetchall()
        )
        high_risk_by_department = dict(
            cursor.execute(
                f"""
                SELECT Department, COUNT(1)
                FROM {SQL_TABLE_NAME}
                WHERE Risk_Level = 'High Risk'
                GROUP BY Department
                ORDER BY COUNT(1) DESC
                """
            ).fetchall()
        )
        avg_salary = cursor.execute(f"SELECT AVG(Base_Salary) FROM {SQL_TABLE_NAME}").fetchone()[0]
        avg_tenure = cursor.execute(f"SELECT AVG(Tenure_Months) FROM {SQL_TABLE_NAME}").fetchone()[0]
        sample_rows = cursor.execute(
            f"""
            SELECT Emp_ID, Department, Tenure_Months, Base_Salary,
                   ROUND(Flight_Risk_Probability, 3), Risk_Level
            FROM {SQL_TABLE_NAME}
            ORDER BY Flight_Risk_Probability DESC
            LIMIT 3
            """
        ).fetchall()

    return {
        "total": total,
        "risk_counts": risk_counts,
        "high_risk_by_department": high_risk_by_department,
        "avg_salary": avg_salary,
        "avg_tenure": avg_tenure,
        "sample_rows": sample_rows,
    }


def write_metrics_snapshot(metrics: dict[str, object]) -> None:
    """Save the key README numbers as a plain-text output artifact."""
    lines = [
        "AttriSense Metrics Snapshot",
        "===========================",
        f"Total workforce: {metrics['total']:,}",
        f"Average salary: ${metrics['avg_salary']:,.0f}",
        f"Average tenure: {metrics['avg_tenure']:.2f} months",
        "",
        "Risk distribution:",
    ]
    risk_counts = metrics["risk_counts"]
    for label in ("High Risk", "Medium Risk", "Low Risk"):
        lines.append(f"- {label}: {risk_counts.get(label, 0):,}")

    lines.append("")
    lines.append("High-risk employees by department:")
    for department, count in metrics["high_risk_by_department"].items():
        lines.append(f"- {department}: {count:,}")

    lines.append("")
    lines.append("Top high-risk sample rows:")
    for row in metrics["sample_rows"]:
        lines.append(
            f"- Emp_ID {row[0]} | {row[1]} | {row[2]} months | "
            f"${row[3]:,.0f} | risk {row[4]:.3f} | {row[5]}"
        )

    (OUTPUTS_DIR / "metrics_snapshot.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_pipeline_commands() -> None:
    """Run the non-API pipeline scripts and capture their terminal output."""
    commands = [
        [sys.executable, "generate_demo_workforce_data.py"],
        [sys.executable, "train_retention_risk_model.py"],
    ]

    output_blocks = ["AttriSense Pipeline Run", "======================", ""]
    for command in commands:
        output_blocks.append(f"$ {' '.join(Path(part).name if part == sys.executable else part for part in command)}")
        result = subprocess.run(command, cwd=ROOT_DIR, capture_output=True, text=True, check=False)
        if result.stdout.strip():
            output_blocks.append(result.stdout.strip())
        if result.stderr.strip():
            output_blocks.append("STDERR:")
            output_blocks.append(result.stderr.strip())
        output_blocks.append(f"exit_code={result.returncode}")
        output_blocks.append("")

    output_blocks.append(
        "Skipped optional build_exit_interview_vector_index.py in this capture because it requires OPENAI_API_KEY."
    )
    (OUTPUTS_DIR / "pipeline_run.txt").write_text("\n".join(output_blocks) + "\n", encoding="utf-8")


def create_product_overview(metrics: dict[str, object]) -> None:
    """Create the hero image embedded near the top of README.md."""
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw_header(draw, "AttriSense Product Overview", "Retention risk intelligence with real demo outputs")

    risk_counts = metrics["risk_counts"]
    total = metrics["total"]
    kpis = [
        ("Total Workforce", f"{total:,}", "#2563eb"),
        ("High Risk", f"{risk_counts.get('High Risk', 0):,}", COLORS["High Risk"]),
        ("Medium Risk", f"{risk_counts.get('Medium Risk', 0):,}", COLORS["Medium Risk"]),
        ("Low Risk", f"{risk_counts.get('Low Risk', 0):,}", COLORS["Low Risk"]),
    ]

    for index, (label, value, accent) in enumerate(kpis):
        left = 70 + index * 375
        draw_card(draw, (left, 190, left + 330, 350), label, value, accent)

    draw.rounded_rectangle((70, 410, 760, 900), radius=28, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    draw.text((110, 448), "Risk Distribution", font=font(30, bold=True), fill=COLORS["ink"])
    draw_donut(draw, {label: risk_counts.get(label, 0) for label in ("High Risk", "Medium Risk", "Low Risk")}, (145, 530, 455, 840))

    legend_x = 500
    for index, label in enumerate(("High Risk", "Medium Risk", "Low Risk")):
        top = 560 + index * 76
        draw.rounded_rectangle((legend_x, top, legend_x + 28, top + 28), radius=8, fill=COLORS[label])
        draw.text((legend_x + 44, top - 2), f"{label}: {risk_counts.get(label, 0):,}", font=font(24), fill=COLORS["ink"])

    draw.rounded_rectangle((820, 410, 1530, 900), radius=28, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    draw.text((860, 448), "High-Risk Concentration", font=font(30, bold=True), fill=COLORS["ink"])
    draw_horizontal_bars(draw, metrics["high_risk_by_department"], 860, 535, 430, 32)
    draw.text((860, 820), f"Average salary: ${metrics['avg_salary']:,.0f}", font=font(26, bold=True), fill=COLORS["ink"])
    draw.text((860, 858), f"Average tenure: {metrics['avg_tenure']:.2f} months", font=font(26, bold=True), fill=COLORS["ink"])

    image.save(ASSETS_DIR / "productOverview.png")


def create_risk_distribution(metrics: dict[str, object]) -> None:
    """Create a standalone risk distribution PNG for README.md."""
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw_header(draw, "Risk Distribution", "Model-scored retention risk across the synthetic workforce")
    risk_counts = metrics["risk_counts"]
    draw_donut(draw, {label: risk_counts.get(label, 0) for label in ("High Risk", "Medium Risk", "Low Risk")}, (165, 230, 765, 830))
    draw_horizontal_bars(draw, {label: risk_counts.get(label, 0) for label in ("Low Risk", "High Risk", "Medium Risk")}, 900, 315, 430, 44)
    image.save(ASSETS_DIR / "riskDistribution.png")


def create_department_concentration(metrics: dict[str, object]) -> None:
    """Create a department-level high-risk concentration PNG for README.md."""
    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw_header(draw, "High-Risk Employees by Department", "Where retention intervention should start")
    draw.rounded_rectangle((160, 220, 1440, 850), radius=30, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    draw_horizontal_bars(draw, metrics["high_risk_by_department"], 250, 330, 850, 54)
    draw.text((250, 730), "Manufacturing carries the largest concentration in this demo scenario.", font=font(30, bold=True), fill=COLORS["ink"])
    image.save(ASSETS_DIR / "highRiskByDepartment.png")


def create_architecture_image() -> None:
    """Create a simple architecture PNG showing how the production scripts connect."""
    if SOURCE_ARCHITECTURE_PATH.exists():
        # The hand-curated diagram in doc/ is the preferred architecture visual.
        # Copying it into assets/ keeps README links self-contained.
        shutil.copyfile(SOURCE_ARCHITECTURE_PATH, ASSETS_DIR / "architecture.png")
        return

    image = Image.new("RGB", (WIDTH, HEIGHT), COLORS["bg"])
    draw = ImageDraw.Draw(image)
    draw_header(draw, "AttriSense Architecture", "Simple pipeline, clear ownership, production-readable files")

    boxes = [
        ((90, 245, 455, 440), "Data Generator", "generate_demo_workforce_data.py", "Creates synthetic HR data", "#dbeafe"),
        ((575, 245, 940, 440), "Risk Model", "train_retention_risk_model.py", "Scores retention risk", "#dcfce7"),
        ((1060, 245, 1425, 440), "SQLite Store", "hr_enterprise.db", "Serves workforce_predictions", "#fef3c7"),
        ((340, 600, 705, 795), "SQL Assistant", "natural_language_sql.py", "Runs safe read-only AI SQL", "#ede9fe"),
        ((855, 600, 1220, 795), "Streamlit Dashboard", "streamlit_app.py", "Shows executive analytics", "#fee2e2"),
    ]

    for xy, title, filename, body, fill in boxes:
        draw.rounded_rectangle(xy, radius=22, fill=fill, outline=COLORS["line"], width=2)
        text_left = xy[0] + 28
        text_width = xy[2] - xy[0] - 56
        draw_wrapped_text(draw, (text_left, xy[1] + 30), title, font(27, bold=True), COLORS["ink"], text_width)
        next_y = draw_wrapped_text(draw, (text_left, xy[1] + 78), filename, font(18, bold=True), COLORS["muted"], text_width)
        draw_wrapped_text(draw, (text_left, next_y + 14), body, font(21), COLORS["muted"], text_width)

    for start, end in [((455, 342), (575, 342)), ((940, 342), (1060, 342)), ((1240, 440), (1038, 600)), ((1060, 440), (522, 600))]:
        draw.line((start, end), fill=COLORS["ink"], width=5)
        draw.ellipse((end[0] - 7, end[1] - 7, end[0] + 7, end[1] + 7), fill=COLORS["ink"])

    image.save(ASSETS_DIR / "architecture.png")


def create_all_images(metrics: dict[str, object]) -> None:
    """Generate every PNG used by README.md."""
    create_product_overview(metrics)
    create_risk_distribution(metrics)
    create_department_concentration(metrics)
    create_architecture_image()


def ensure_directories(paths: Iterable[Path]) -> None:
    """Create output directories if they do not already exist."""
    for path in paths:
        path.mkdir(exist_ok=True)


def parse_args() -> argparse.Namespace:
    """Read command-line options for asset generation."""
    parser = argparse.ArgumentParser(description="Create README assets and output captures.")
    parser.add_argument(
        "--skip-pipeline",
        action="store_true",
        help="Use the existing database instead of regenerating data/model outputs.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the README asset workflow end to end."""
    args = parse_args()
    ensure_directories((ASSETS_DIR, OUTPUTS_DIR))

    if not args.skip_pipeline:
        run_pipeline_commands()

    metrics = load_metrics()
    write_metrics_snapshot(metrics)
    create_all_images(metrics)
    print(f"Saved README images to {ASSETS_DIR}.")
    print(f"Saved output captures to {OUTPUTS_DIR}.")


if __name__ == "__main__":
    main()
