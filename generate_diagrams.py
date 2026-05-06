"""Generate simple architecture diagrams for AttriSense."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


DOC_DIR = Path(__file__).resolve().parent / "doc"
WIDTH = 1400
HEIGHT = 850


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load Arial when available and fall back to Pillow's default font."""
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    title: str,
    body: str,
    fill: str,
) -> None:
    """Draw one labeled rounded rectangle on a diagram.

    Args:
        draw: Pillow drawing context for the image.
        xy: Rectangle coordinates as `(left, top, right, bottom)`.
        title: Bold-style heading text for the box.
        body: Supporting multiline text.
        fill: Background color for the box.
    """
    draw.rounded_rectangle(xy, radius=16, fill=fill, outline="#1f2937", width=2)
    x1, y1, x2, _ = xy
    draw.text((x1 + 24, y1 + 22), title, fill="#111827", font=font(24))
    draw.multiline_text((x1 + 24, y1 + 66), body, fill="#374151", font=font(17), spacing=5)
    draw.line((x1 + 20, y1 + 56, x2 - 20, y1 + 56), fill="#9ca3af", width=1)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int]) -> None:
    """Draw a simple left-to-right arrow between two points."""
    draw.line((start, end), fill="#111827", width=4)
    x, y = end
    draw.polygon([(x, y), (x - 14, y - 8), (x - 14, y + 8)], fill="#111827")


def save_canvas(name: str, title: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Create a blank diagram canvas with a shared title/header style.

    Args:
        name: Output PNG filename inside `doc/`.
        title: Diagram title rendered at the top.

    Returns:
        The Pillow image and drawing context so caller functions can add content.
    """
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f8fafc")
    draw = ImageDraw.Draw(image)
    draw.text((70, 45), title, fill="#0f172a", font=font(38))
    draw.text(
        (72, 95),
        "A compact workforce intelligence platform: data, model, AI, and dashboard.",
        fill="#475569",
        font=font(20),
    )
    image.save(DOC_DIR / name)
    return image, draw


def architecture_diagram() -> None:
    """Generate the high-level system architecture diagram."""
    image, draw = save_canvas("architecture_diagram.png", "AttriSense Architecture")
    boxes = [
        ((90, 190, 370, 360), "Data Generator", "Synthetic HR records\nSafe public demo data", "#dbeafe"),
        ((515, 190, 795, 360), "Predictive Engine", "Random Forest + SMOTE\nFlight-risk scores", "#dcfce7"),
        ((940, 190, 1220, 360), "SQLite Database", "workforce_predictions\nDashboard-ready table", "#fef3c7"),
        ((300, 520, 580, 690), "AI SQL", "Read-only NL-to-SQL\nValidated SQL execution", "#ede9fe"),
        ((720, 520, 1000, 690), "Streamlit App", "Executive KPIs\nDrilldowns and charts", "#ffe4e6"),
    ]
    for item in boxes:
        # Each tuple already contains the rectangle coordinates and text, so
        # unpacking keeps the diagram definition compact and readable.
        box(draw, *item)
    arrow(draw, (370, 275), (515, 275))
    arrow(draw, (795, 275), (940, 275))
    arrow(draw, (1080, 360), (870, 520))
    arrow(draw, (940, 360), (470, 520))
    image.save(DOC_DIR / "architecture_diagram.png")


def execution_flow() -> None:
    """Generate the step-by-step local execution flow diagram."""
    image, draw = save_canvas("execution_flow.png", "AttriSense Execution Flow")
    steps = [
        ((110, 190, 370, 340), "1. Install", "pip install -r\nrequirements.txt", "#e0f2fe"),
        ((430, 190, 690, 340), "2. Generate", "python\ndata_generator.py", "#dcfce7"),
        ((750, 190, 1010, 340), "3. Score", "python\npredictive_engine.py", "#fef3c7"),
        ((1070, 190, 1330, 340), "4. Run", "python\nrun_attrisense.py", "#fee2e2"),
        ((430, 500, 690, 650), "Optional", "python rag_engine.py\nrequires API key", "#ede9fe"),
        ((750, 500, 1010, 650), "Explore", "Open\nlocalhost:8501", "#f3e8ff"),
    ]
    for item in steps:
        box(draw, *item)
    arrow(draw, (370, 265), (430, 265))
    arrow(draw, (690, 265), (750, 265))
    arrow(draw, (1010, 265), (1070, 265))
    arrow(draw, (560, 340), (560, 500))
    arrow(draw, (880, 340), (880, 500))
    image.save(DOC_DIR / "execution_flow.png")


def technology_stack() -> None:
    """Generate a diagram that groups the core technologies by purpose."""
    image, draw = save_canvas("technology_stack.png", "AttriSense Technology Stack")
    boxes = [
        ((120, 190, 420, 350), "Frontend", "Streamlit\nPlotly", "#e0f2fe"),
        ((550, 190, 850, 350), "Data", "pandas\nSQLite\nNumPy", "#dcfce7"),
        ((980, 190, 1280, 350), "ML", "scikit-learn\nimbalanced-learn", "#fef3c7"),
        ((335, 500, 635, 660), "AI", "LangChain\nOpenAI", "#ede9fe"),
        ((765, 500, 1065, 660), "Search", "FAISS\nEmbeddings", "#fee2e2"),
    ]
    for item in boxes:
        box(draw, *item)
    image.save(DOC_DIR / "technology_stack.png")


def main() -> None:
    """Create all documentation diagrams in the `doc/` folder."""
    DOC_DIR.mkdir(exist_ok=True)
    architecture_diagram()
    execution_flow()
    technology_stack()
    print(f"Generated diagrams in {DOC_DIR}.")


if __name__ == "__main__":
    main()
