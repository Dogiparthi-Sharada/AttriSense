"""Generate AttriSense documentation diagrams (Google Pixel pastel theme).

Visual language:
  - warm cream canvas (#FBF7F2) with three soft pastel washes
  - white card surfaces with a 4 px coloured accent strip on the left
  - warm dark ink (#2B2A28) for titles, taupe muted (#7A746B) for body
  - regular-weight typography, generous interior padding
  - arrows anchor to card edges (computed) — never to interior points
  - reserved 230 px header so cards never collide with the title rule

Outputs go to assets/diagrams/, outputs/diagrams/, docs/images/diagrams/.
Run with `.venv/bin/python scripts/generate_doc_diagrams.py`.
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[1]
TARGETS = [
    REPO / "assets" / "diagrams",
    REPO / "outputs" / "diagrams",
    REPO / "docs" / "images" / "diagrams",
]
for t in TARGETS:
    t.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- palette
BG = "#FBF7F2"
INK = "#2B2A28"
MUTED = "#7A746B"
LINE = "#E7DECF"
ARROW = "#9C8FB8"

# Pixel pastel accents (matches production/src/attrisense/theme.py)
LAVENDER = "#B8B5E1"
PERIWINKLE = "#A8B5E1"
DUSTY_BLUE = "#9FC2DB"
SAGE = "#B5D4A8"
MINT = "#B8E0D0"
BUTTER = "#F5E1A0"
PEACH = "#F5C4A0"
CORAL = "#F2A8A0"
ROSE = "#E8B4B8"
LILAC = "#D9B8E1"

# Soft tinted card surfaces (white-leaning pastel washes)
TINT_LAVENDER = "#F2F0FA"
TINT_PERI = "#EEF1FA"
TINT_BLUE = "#EDF5FB"
TINT_SAGE = "#EFF6EA"
TINT_MINT = "#ECF7F1"
TINT_BUTTER = "#FDF7E2"
TINT_PEACH = "#FBEEDE"
TINT_CORAL = "#FBE4DF"
TINT_ROSE = "#F8E8E9"
TINT_LILAC = "#F5EAFA"

GREEN_OK = "#5C8B4F"
RED_BAD = "#B85A4E"
AMBER = "#C9A845"

WIDTH = 1600
HEIGHT = 1000
HEADER_BOTTOM = 230


# ------------------------------------------------------------------- fonts
def _font(size: int) -> ImageFont.ImageFont:
    for c in ("DejaVuSans.ttf", "Arial.ttf"):
        try:
            return ImageFont.truetype(c, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _tsize(d, text, font):
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    return r - l, b - t


def _wrap(d, text, font, max_w):
    out = []
    for line in text.split("\n"):
        words = line.split()
        cur = ""
        for w in words:
            cand = (cur + " " + w).strip()
            if _tsize(d, cand, font)[0] <= max_w:
                cur = cand
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
        if not words:
            out.append("")
    return out


# ------------------------------------------------------------------- prims
class Card:
    """Rounded card with title + body. White surface with pastel accent strip."""

    def __init__(self, x1, y1, x2, y2, title, body, fill, accent):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.title = title
        self.body = body
        self.fill = fill
        self.accent = accent

    def cx(self): return (self.x1 + self.x2) / 2
    def cy(self): return (self.y1 + self.y2) / 2
    def left(self): return (self.x1, self.cy())
    def right(self): return (self.x2, self.cy())
    def top(self): return (self.cx(), self.y1)
    def bottom(self): return (self.cx(), self.y2)

    def draw(self, d):
        # Soft drop shadow
        for dy in (4, 3, 2):
            shade = 240 - dy * 4
            d.rounded_rectangle(
                (self.x1 + 1, self.y1 + dy, self.x2 + 1, self.y2 + dy),
                radius=18, outline=None, fill=(shade, shade - 4, shade - 12),
            )
        d.rounded_rectangle(
            (self.x1, self.y1, self.x2, self.y2),
            radius=18, fill=self.fill, outline=LINE, width=2,
        )
        # 6 px accent strip (full pastel colour, anchored on left)
        d.rounded_rectangle(
            (self.x1, self.y1, self.x1 + 8, self.y2),
            radius=4, fill=self.accent, outline=None,
        )
        pad_l = 28
        pad_t = 22
        inner_w = self.x2 - self.x1 - pad_l - 22
        title_font = _font(23)
        body_font = _font(17)
        d.text((self.x1 + pad_l, self.y1 + pad_t - 2), self.title,
               font=title_font, fill=INK)
        cur_y = self.y1 + pad_t + 24 + 12
        max_y = self.y2 - 22
        for line in _wrap(d, self.body, body_font, inner_w):
            if cur_y + 22 > max_y:
                break
            d.text((self.x1 + pad_l, cur_y), line, font=body_font, fill=MUTED)
            cur_y += 22


def _arrow(d, start, end, color=ARROW, width=3):
    x1, y1 = start
    x2, y2 = end
    d.line([start, end], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    head = 14
    a1 = (x2 - head * math.cos(angle - math.pi / 7),
          y2 - head * math.sin(angle - math.pi / 7))
    a2 = (x2 - head * math.cos(angle + math.pi / 7),
          y2 - head * math.sin(angle + math.pi / 7))
    d.polygon([end, a1, a2], fill=color)


def _label(d, text, xy, fill=MUTED, size=15):
    d.text(xy, text, font=_font(size), fill=fill)


def _pastel_glow(img):
    """Three soft pastel washes (lavender / peach / sage) on the cream
    canvas. Stays subtle so cards remain readable."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    spots = [
        ((0.00 * WIDTH, 0.00 * HEIGHT, 0.45 * WIDTH, 0.55 * HEIGHT), (184, 181, 225, 90)),  # lavender TL
        ((0.55 * WIDTH, 0.00 * HEIGHT, 1.05 * WIDTH, 0.50 * HEIGHT), (245, 196, 160, 80)),  # peach TR
        ((0.20 * WIDTH, 0.65 * HEIGHT, 0.85 * WIDTH, 1.10 * HEIGHT), (181, 212, 168, 70)),  # sage BC
    ]
    for box, color in spots:
        od.ellipse(box, fill=color)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=140))
    img.alpha_composite(overlay)


def _header(d, title, subtitle):
    d.text((90, 60), title, font=_font(38), fill=INK)
    d.text((90, 120), subtitle, font=_font(20), fill=MUTED)
    # Pastel gradient rule (lavender -> peach -> sage)
    rule_y = 200
    rule_x1, rule_x2 = 90, WIDTH - 90
    n = 320
    stops = [(184, 181, 225), (245, 196, 160), (181, 212, 168)]
    for i in range(n):
        t = i / (n - 1)
        if t < 0.5:
            tt = t * 2
            c1, c2 = stops[0], stops[1]
        else:
            tt = (t - 0.5) * 2
            c1, c2 = stops[1], stops[2]
        r = int(c1[0] + (c2[0] - c1[0]) * tt)
        g = int(c1[1] + (c2[1] - c1[1]) * tt)
        b = int(c1[2] + (c2[2] - c1[2]) * tt)
        x1 = rule_x1 + (rule_x2 - rule_x1) * i / n
        x2 = rule_x1 + (rule_x2 - rule_x1) * (i + 1) / n
        d.line([(x1, rule_y), (x2, rule_y)], fill=(r, g, b), width=3)


def _save(img, name):
    rgb = img.convert("RGB")
    for t in TARGETS:
        rgb.save(t / name)
    print(f"  wrote {name}")


def _new_canvas():
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG)
    _pastel_glow(img)
    return img, ImageDraw.Draw(img)


def _draw_cards(d, cards):
    for c in cards:
        c.draw(d)


# ============================================================== diagrams

def diagram_architecture():
    img, d = _new_canvas()
    _header(d, "AttriSense — System Architecture",
            "Six independent layers; replace any one without touching the rest")

    band_h = 105
    band_gap = 14
    top = HEADER_BOTTOM + 30
    layers = [
        ("Application", "Streamlit dashboard  ·  7 tabs  ·  Pixel pastel theme",
         TINT_ROSE, ROSE),
        ("Insights", "SHAP TreeExplainer  ·  fairness audit  ·  causal uplift",
         TINT_LILAC, LILAC),
        ("Models", "RandomForest + SMOTE  ·  Cox PH  ·  EconML T-Learner",
         TINT_LAVENDER, LAVENDER),
        ("Features", "Tenure  ·  Salary  ·  Department code  ·  Manager tenure",
         TINT_BLUE, DUSTY_BLUE),
        ("Data", "SQLite — employees · engagement_pulse · exit_interviews · predictions",
         TINT_SAGE, SAGE),
        ("Operations", "make targets  ·  Docker image  ·  pytest  ·  GitHub Actions  ·  .env",
         TINT_BUTTER, BUTTER),
    ]
    cards = []
    y = top
    for name, body, fill, accent in layers:
        cards.append(Card(120, y, WIDTH - 120, y + band_h, name, body, fill, accent))
        y += band_h + band_gap
    _draw_cards(d, cards)
    for i in range(len(cards) - 1):
        a, b = cards[i], cards[i + 1]
        x = WIDTH - 170
        _arrow(d, (x, a.y2 + 2), (x, b.y1 - 2))
    _save(img, "architecture.png")


def diagram_data_flow():
    img, d = _new_canvas()
    _header(d, "End-to-End Data Flow",
            "One employee row traced from CSV to a SHAP-explained prediction")

    cards = [
        Card(90,   280, 460,  440, "1. HRIS / CSV",
             "5,000 synthetic rows  ·  seed=42",
             TINT_SAGE, SAGE),
        Card(540,  280, 910,  440, "2. SQLite",
             "employees  +  engagement_pulse  +  exit_interviews",
             TINT_BLUE, DUSTY_BLUE),
        Card(990,  280, 1360, 440, "3. Features",
             "Tenure  ·  Salary  ·  Dept code  ·  Manager tenure",
             TINT_LAVENDER, LAVENDER),

        Card(90,   500, 460,  650, "4a. RandomForest",
             "SMOTE-balanced classifier  ·  prob of attrition",
             TINT_PEACH, PEACH),
        Card(540,  500, 910,  650, "4b. Cox PH",
             "lifelines  ·  survival curve per employee",
             TINT_PEACH, PEACH),
        Card(990,  500, 1360, 650, "4c. T-Learner",
             "EconML uplift  ·  3 treatment arms",
             TINT_PEACH, PEACH),

        Card(90,   720, 720,  890, "5. SHAP TreeExplainer",
             "Per-employee driver decomposition  →  shap_feature_impact table",
             TINT_LILAC, LILAC),
        Card(800,  720, 1510, 890, "6. Streamlit dashboard",
             "Executive  ·  SHAP  ·  Compare  ·  Uplift  ·  Fairness  ·  AI  ·  RAG",
             TINT_ROSE, ROSE),
    ]
    _draw_cards(d, cards)
    csv, sqlite, feats, rf, cox, tl, shap, dash = cards

    _arrow(d, csv.right(), sqlite.left())
    _arrow(d, sqlite.right(), feats.left())
    for m in (rf, cox, tl):
        _arrow(d, (feats.cx(), feats.y2), m.top())
    _arrow(d, rf.bottom(),  (shap.cx() - 120, shap.y1))
    _arrow(d, cox.bottom(), (shap.cx(),       shap.y1))
    _arrow(d, tl.bottom(),  (shap.cx() + 120, shap.y1))
    _arrow(d, shap.right(), dash.left())
    _save(img, "data-flow.png")


def diagram_ml_pipeline():
    img, d = _new_canvas()
    _header(d, "ML Pipeline",
            "train_retention_risk_model.py  —  deterministic, reproducible (seed=42)")

    row1_y1, row1_y2 = 280, 430
    row2_y1, row2_y2 = 480, 630
    row3_y1, row3_y2 = 680, 840

    cards = [
        Card(90,   row1_y1, 410,  row1_y2, "Load CSV",
             "5,000 rows  ·  HR table", TINT_SAGE, SAGE),
        Card(450,  row1_y1, 770,  row1_y2, "Train / test",
             "80 / 20 stratified split", TINT_BLUE, DUSTY_BLUE),
        Card(810,  row1_y1, 1130, row1_y2, "SMOTE",
             "Balance minority class on train fold only",
             TINT_LAVENDER, LAVENDER),
        Card(1170, row1_y1, 1510, row1_y2, "RandomForest",
             "n=300  ·  max_depth=12  ·  class_weight=balanced",
             TINT_PEACH, PEACH),

        Card(90,   row2_y1, 410,  row2_y2, "Cox PH",
             "lifelines fit  ·  separate feature set",
             TINT_LAVENDER, LAVENDER),
        Card(450,  row2_y1, 770,  row2_y2, "T-Learner",
             "EconML uplift  ·  3 treatment arms",
             TINT_LAVENDER, LAVENDER),
        Card(810,  row2_y1, 1130, row2_y2, "Cross-val",
             "5-fold ROC-AUC, calibration error",
             TINT_BLUE, DUSTY_BLUE),
        Card(1170, row2_y1, 1510, row2_y2, "SHAP",
             "TreeExplainer  ·  exact attributions",
             TINT_LILAC, LILAC),

        Card(90,   row3_y1, 1510, row3_y2, "Outputs",
             "attrisense_model.joblib  ·  workforce_predictions  ·  shap_feature_impact  "
             "·  model_calibration  ·  survival_curves",
             TINT_BUTTER, BUTTER),
    ]
    _draw_cards(d, cards)
    load, split, smote, rf, cox, tl, cv, shap, outputs = cards

    _arrow(d, load.right(),  split.left())
    _arrow(d, split.right(), smote.left())
    _arrow(d, smote.right(), rf.left())

    _arrow(d, (split.cx(), split.y2), cox.top())
    _arrow(d, (split.cx() + 60, split.y2), (tl.cx() - 40, tl.y1))

    _arrow(d, (rf.cx(), rf.y2), (cv.cx(), cv.y1))
    _arrow(d, cv.right(), shap.left())

    for src in (rf, cox, tl, shap):
        _arrow(d, (src.cx(), src.y2), (src.cx(), outputs.y1 - 2))

    _save(img, "ml-pipeline.png")


def diagram_fairness():
    img, d = _new_canvas()
    _header(d, "Fairness Audit  —  EEOC Four-Fifths Rule",
            "ratio = min(group selection rate) / max(group selection rate)   ≥   0.80")

    inp   = Card(60,   280, 380,  440, "Predictions",
                 "joined with the chosen group attribute",
                 TINT_SAGE, SAGE)
    rate  = Card(420,  280, 740,  440, "Selection rate",
                 "P( flagged high-risk | group ) per group",
                 TINT_BLUE, DUSTY_BLUE)
    ratio = Card(780,  280, 1100, 440, "Ratio",
                 "min(rates) / max(rates)",
                 TINT_LAVENDER, LAVENDER)
    gate  = Card(1140, 280, 1460, 440, "Four-fifths gate",
                 "ratio  ≥  0.80 ?",
                 TINT_LILAC, LILAC)

    pass_ = Card(150,  560, 720,  740, "PASS",
                 "Ship the recommendation. Append audit row: timestamp · dimension · ratio · n.",
                 TINT_SAGE, SAGE)
    fail  = Card(880,  560, 1450, 740, "FAIL",
                 "Pause downstream alerts for the affected group. Investigate. Mitigate. Re-audit.",
                 TINT_CORAL, CORAL)

    artif = Card(90, 800, 1510, 930, "Artifacts",
                 "outputs/fairness_report.json   ·   dashboard banner   "
                 "·   audit log row   ·   pause flag for alerts",
                 TINT_BUTTER, BUTTER)

    _draw_cards(d, [inp, rate, ratio, gate, pass_, fail, artif])

    _arrow(d, inp.right(),   rate.left())
    _arrow(d, rate.right(),  ratio.left())
    _arrow(d, ratio.right(), gate.left())

    _arrow(d, (gate.cx() - 80, gate.y2), pass_.top(), color=GREEN_OK)
    _arrow(d, (gate.cx() + 80, gate.y2), fail.top(),  color=RED_BAD)
    _label(d, "yes", (gate.cx() - 110, gate.y2 + 10), fill=GREEN_OK)
    _label(d, "no",  (gate.cx() + 90,  gate.y2 + 10), fill=RED_BAD)

    _arrow(d, pass_.bottom(), (pass_.cx(), artif.y1))
    _arrow(d, fail.bottom(),  (fail.cx(),  artif.y1))

    _save(img, "fairness.png")


def diagram_rag_fallback():
    img, d = _new_canvas()
    _header(d, "Multilingual RAG  —  Resilient Provider Fallback",
            "OpenAI-first, hashing-fallback when the API is unreachable")

    query  = Card(90,   340, 430,  510, "User query",
                  "EN / ES / HI exit-interview question",
                  TINT_SAGE, SAGE)
    probe  = Card(490,  340, 830,  510, "Reachability probe",
                  "DNS + TCP + HTTPS HEAD on api.openai.com  (250 ms timeout)",
                  TINT_BLUE, DUSTY_BLUE)
    openai = Card(890,  230, 1230, 390, "OpenAI embeddings",
                  "text-embedding-3-small  ·  1536 dim",
                  TINT_LAVENDER, LAVENDER)
    hash_  = Card(890,  460, 1230, 620, "Hashing embeddings",
                  "MD5-bucketed local hashing  ·  256 dim",
                  TINT_BUTTER, BUTTER)
    faiss  = Card(290,  690, 1010, 880, "FAISS index",
                  "Per-provider directory (.../openai vs .../hashing) — different dims never collide.",
                  TINT_LILAC, LILAC)
    result = Card(1070, 690, 1510, 880, "Result",
                  "top-K rows  +  language  +  provider tag",
                  TINT_PEACH, PEACH)

    _draw_cards(d, [query, probe, openai, hash_, faiss, result])

    _arrow(d, query.right(), probe.left())
    _arrow(d, (probe.x2, probe.cy() - 40), openai.left(), color=GREEN_OK)
    _arrow(d, (probe.x2, probe.cy() + 40), hash_.left(),  color=AMBER)
    _label(d, "reachable",      (probe.x2 + 6, probe.cy() - 70), fill=GREEN_OK)
    _label(d, "firewall / 5xx", (probe.x2 + 6, probe.cy() + 50), fill=AMBER)

    _arrow(d, openai.bottom(), (faiss.cx() + 120, faiss.y1))
    _arrow(d, hash_.bottom(),  (faiss.cx() - 120, faiss.y1))
    _arrow(d, faiss.right(),   result.left())
    _save(img, "rag-fallback.png")


def main():
    print("Generating Pixel pastel diagrams (Pillow, anchored arrows)…")
    diagram_architecture()
    diagram_data_flow()
    diagram_ml_pipeline()
    diagram_fairness()
    diagram_rag_fallback()
    print("\nAll diagrams written to:")
    for t in TARGETS:
        print(f"  {t}")


if __name__ == "__main__":
    main()
