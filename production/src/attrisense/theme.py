# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/theme.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Centralised theme + colour palette for AttriSense.

**Pixel Pastel** — Google Pixel / Material You inspired soft palette.
Warm cream canvas, dusty pastels, low saturation, ink-on-paper feel,
Inter typography. Charts use pastel hues that stay readable but never
shout.

Public surface (kept stable):
    CSS                       -- one big <style> block to inject once
    RISK_COLOR_MAP            -- semantic risk colours
    SEQUENTIAL                -- 5-stop perceptual ramp
    apply_plotly_defaults(fig)
    render_brand_header(title, tagline) -> str
    render_disclosure(text) -> str
"""

from __future__ import annotations

# ----------------------------------------------------------- Pixel Pastel
# Warm neutrals (cream paper)
CANVAS = "#FBF7F2"        # warm cream
SURFACE = "#FFFFFF"        # paper white card
SUBSURFACE = "#F5EFE6"     # soft sand
BORDER = "#E7DECF"         # taupe border
INK = "#2B2A28"            # near-black warm ink
TEXT = "#3D3A35"           # body text
MUTED = "#7A746B"          # caption muted
HEADING = "#1F1E1B"        # heading

# Pixel pastel accents (Material You-ish, low chroma)
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

# Semantic risk colours
RISK_COLOR_MAP = {
    "High Risk": CORAL,       # warm coral pastel for high
    "Medium Risk": BUTTER,    # butter yellow for medium
    "Low Risk": SAGE,         # sage green for low
}

# Sequential: cream → peach → coral → deep coral. Monotonic single-family
# ramp (no hue jumps), works for heatmaps and continuous scales.
SEQUENTIAL = ["#FBF7F2", "#F5E1A0", "#F5C4A0", "#F2A8A0", "#C97A6F"]

# Diverging: sage (negative / good) ↔ cream (zero) ↔ coral (positive / bad)
DIVERGING = ["#7AAA6E", "#B5D4A8", "#FBF7F2", "#F2A8A0", "#C97A6F"]

# Categorical: pixel pastel rainbow, max contrast between adjacents
CATEGORICAL = [LAVENDER, PEACH, SAGE, DUSTY_BLUE, BUTTER, ROSE, MINT, LILAC]


# Pure-black chart text override (user-mandated readability fix).
# Only readable TEXT (axis ticks, axis titles, legend labels, colorbar
# tick labels, annotations, chart title) is forced to black.
# Colors of bars/lines/markers/grid stay as designed (pastel).
CHART_TEXT = "#000000"


def plotly_layout() -> dict:
    """Default layout patches applied to every Plotly figure.

    Text-only override: every readable label is forced to BLACK so the
    charts stay legible on warm cream surfaces. Bars, markers, gridlines,
    zerolines, and tick marks keep their original pastel design colours.
    """
    axis = {
        "gridcolor": "#D9CFBC",
        "zerolinecolor": "#7A746B",
        "linecolor": "#3D3A35",
        "linewidth": 1.5,
        "tickcolor": "#3D3A35",
        "tickfont": {"color": CHART_TEXT, "size": 12,
                     "family": "'Google Sans', Inter, sans-serif"},
        "title": {"font": {"color": CHART_TEXT, "size": 13}},
        "color": CHART_TEXT,
        "showline": True,
        "mirror": False,
    }
    return {
        "font": {
            "family": "'Google Sans', Inter, ui-sans-serif, system-ui, -apple-system",
            "color": CHART_TEXT,
            "size": 13,
        },
        "title": {"font": {"size": 16, "color": CHART_TEXT}},
        "paper_bgcolor": SURFACE,
        "plot_bgcolor": SURFACE,
        "xaxis": dict(axis),
        "yaxis": dict(axis),
        "legend": {
            "orientation": "h",
            "yanchor": "top",
            "y": -0.18,
            "xanchor": "center",
            "x": 0.5,
            "bgcolor": SUBSURFACE,
            "bordercolor": BORDER,
            "borderwidth": 1,
            "font": {"color": CHART_TEXT, "size": 12},
            "title": {"font": {"color": CHART_TEXT, "size": 12}},
        },
        "coloraxis": {
            "colorbar": {
                "tickfont": {"color": CHART_TEXT, "size": 11},
                "title": {"font": {"color": CHART_TEXT, "size": 12}},
            },
        },
        "hoverlabel": {
            "font": {"color": CHART_TEXT, "size": 12},
        },
        "margin": {"t": 56, "r": 24, "b": 96, "l": 56},
        "colorway": CATEGORICAL,
    }


def apply_plotly_defaults(fig):
    """Apply layout defaults AND force every trace's text labels to black.

    Plotly's `update_layout` does not retroactively re-colour text
    already attached to existing traces (bar value labels, scatter text,
    pie labels, per-trace colorbar legends). We walk the figure once and
    force black on each trace's text — without touching marker colours.
    """
    fig.update_layout(**plotly_layout())
    # Globally hide ANY coloraxis colorbar. We never use them — bar height,
    # marker size, or stacked legend already encode the value.
    try:
        fig.update_layout(coloraxis_showscale=False)
    except Exception:
        pass
    # Walk the layout for ANY coloraxis* keys and disable each.
    try:
        layout_dict = fig.layout.to_plotly_json()
        for key in list(layout_dict.keys()):
            if key.startswith("coloraxis"):
                fig.update_layout({key: dict(showscale=False)})
    except Exception:
        pass
    # textfont / inside / outside vary by trace type. Apply per-trace defensively.
    for tr in fig.data:
        ttype = getattr(tr, "type", "")
        # Hide per-trace colorbar (heatmap, choropleth, scatter with color=).
        for attr in ("showscale",):
            try:
                setattr(tr, attr, False)
            except Exception:
                pass
        # Some traces (heatmap, scattergl) attach colorbar via marker.colorbar.
        try:
            if hasattr(tr, "marker") and tr.marker is not None:
                if hasattr(tr.marker, "showscale"):
                    tr.marker.showscale = False
        except Exception:
            pass
        if ttype in ("bar", "pie", "histogram", "funnel", "scatter", "treemap", "sunburst"):
            try:
                tr.textfont = dict(color=CHART_TEXT, size=12)
            except Exception:
                pass
        if ttype in ("bar", "pie", "histogram", "funnel"):
            try:
                tr.insidetextfont = dict(color=CHART_TEXT, size=12)
                tr.outsidetextfont = dict(color=CHART_TEXT, size=12)
            except Exception:
                pass
    # Per-trace colorbars (e.g. px.bar(color=...))
    for tr in fig.data:
        marker = getattr(tr, "marker", None)
        cb = getattr(marker, "colorbar", None) if marker is not None else None
        if cb is not None:
            try:
                tr.marker.colorbar.tickfont = dict(color=CHART_TEXT, size=11)
                existing_title = ""
                try:
                    existing_title = (tr.marker.colorbar.title.text or "")  # type: ignore
                except Exception:
                    pass
                tr.marker.colorbar.title = dict(
                    text=existing_title,
                    font=dict(color=CHART_TEXT, size=12),
                )
            except Exception:
                pass
    return fig


def pastel_table(df, *, gradient_cols=None, cmap_name="coral", fmt=None):
    """Wrap a DataFrame in a Pixel-pastel cream Styler with optional gradient.

    `gradient_cols`: list of numeric column names to apply a pastel cmap on.
    `cmap_name`: one of "coral", "sage", "lavender".
    `fmt`: optional dict of {column: format-string}.
    """
    from matplotlib.colors import LinearSegmentedColormap

    cmaps = {
        "coral": LinearSegmentedColormap.from_list(
            "coral_pastel", ["#FBF7F2", "#F5E1A0", "#F5C4A0", "#F2A8A0"]),
        "sage": LinearSegmentedColormap.from_list(
            "sage_pastel", ["#FBF7F2", "#E1ECCE", "#B5D4A8"]),
        "lavender": LinearSegmentedColormap.from_list(
            "lav_pastel", ["#FBF7F2", "#D9D5EB", "#B8B5E1"]),
    }
    cmap = cmaps.get(cmap_name, cmaps["coral"])

    sty = (
        df.style
        .set_properties(**{
            "background-color": "#FBF7F2",
            "color": "#1F1E1B",
            "font-weight": "400",
            "border": "1px solid #E7DECF",
        })
        .set_table_styles([
            {"selector": "th", "props": [
                ("background", "linear-gradient(180deg,#1B2A4E 0%,#2A3B66 100%)"),
                ("color", "#F4E9C7"),
                ("font-weight", "700"),
                ("letter-spacing", "0.3px"),
                ("border", "1px solid #14213D"),
                ("border-bottom", "2px solid #C9A96E"),
            ]},
            {"selector": "td", "props": [
                ("color", "#1F1E1B !important"),
                ("font-weight", "400 !important"),
            ]},
        ])
    )
    if gradient_cols:
        existing = [c for c in gradient_cols if c in df.columns]
        if existing:
            sty = sty.background_gradient(subset=existing, cmap=cmap)
    if fmt:
        sty = sty.format({k: v for k, v in fmt.items() if k in df.columns})
    return sty


def show_styled(st_module, styler_or_df, *, height=None):
    """Render a pandas Styler (or DataFrame) as pastel-themed HTML.

    Use this everywhere instead of ``st.dataframe(...)`` to guarantee the
    Pixel-pastel header strip wins over Streamlit's canvas-grid renderer.
    """
    import pandas as _pd

    if isinstance(styler_or_df, _pd.DataFrame):
        sty = pastel_table(styler_or_df)
    else:
        sty = styler_or_df
    try:
        sty = sty.hide(axis="index")
    except Exception:
        pass
    inner = sty.to_html()
    max_h = f"max-height:{height}px;overflow-y:auto;" if height else ""
    wrapper_css = (
        "background:#FBF7F2;border:1px solid #E7DECF;border-radius:14px;"
        "padding:8px;overflow-x:auto;" + max_h
    )
    table_css = (
        "<style>"
        ".pastel-tbl table{border-collapse:separate;border-spacing:0;width:100%;"
        "font-family:'Google Sans',Inter,sans-serif;font-size:13px;}"
        ".pastel-tbl thead tr th{background:linear-gradient(180deg,#1B2A4E 0%,#2A3B66 100%) !important;"
        "color:#F4E9C7 !important;font-weight:700 !important;letter-spacing:0.3px;"
        "border-bottom:2px solid #C9A96E !important;border-right:1px solid #14213D !important;"
        "padding:10px 12px !important;text-align:left !important;text-transform:uppercase;font-size:11.5px !important;}"
        ".pastel-tbl tbody tr td{color:#1F1E1B !important;font-weight:400 !important;"
        "padding:6px 10px !important;border-bottom:1px solid #EFE7D7 !important;}"
        ".pastel-tbl tbody tr:nth-child(even) td{background:#FCF9F4 !important;}"
        "</style>"
    )
    st_module.markdown(
        table_css + f'<div class="pastel-tbl" style="{wrapper_css}">{inner}</div>',
        unsafe_allow_html=True,
    )



CSS = f"""
<style>
:root {{
    --canvas: {CANVAS};
    --surface: {SURFACE};
    --subsurface: {SUBSURFACE};
    --border: {BORDER};
    --ink: {INK};
    --text: {TEXT};
    --muted: {MUTED};
    --heading: {HEADING};
    --lavender: {LAVENDER};
    --periwinkle: {PERIWINKLE};
    --dusty-blue: {DUSTY_BLUE};
    --sage: {SAGE};
    --mint: {MINT};
    --butter: {BUTTER};
    --peach: {PEACH};
    --coral: {CORAL};
    --rose: {ROSE};
    --lilac: {LILAC};
}}
html, body, [class*="css"] {{
    font-family: 'Google Sans', 'Inter', ui-sans-serif, system-ui, -apple-system, sans-serif;
    color: var(--text);
}}
.stApp {{
    background:
        radial-gradient(ellipse at 12% 0%, rgba(184, 181, 225, 0.30) 0%, transparent 55%),
        radial-gradient(ellipse at 88% 8%, rgba(245, 196, 160, 0.25) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 100%, rgba(181, 212, 168, 0.22) 0%, transparent 60%),
        var(--canvas) !important;
}}
.block-container {{
    padding-top: 1.4rem;
    padding-bottom: 2.4rem;
    max-width: 1340px;
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #F5EFE6 0%, #FBF7F2 100%);
    border-right: 1px solid var(--border);
}}
section[data-testid="stSidebar"] * {{
    color: var(--text) !important;
}}
section[data-testid="stSidebar"] .stButton button {{
    background: rgba(184, 181, 225, 0.18);
    color: #4A4078 !important;
    border: 1px solid rgba(184, 181, 225, 0.45);
    transition: all 0.15s ease;
}}
section[data-testid="stSidebar"] .stButton button:hover {{
    background: rgba(184, 181, 225, 0.32);
    border-color: var(--lavender);
}}
section[data-testid="stSidebar"] code {{
    background: rgba(255,255,255,0.65);
    color: #4A4078 !important;
    border: 1px solid var(--border);
    font-size: 0.78rem;
}}

h1, h2, h3, h4 {{
    color: var(--heading) !important;
    font-weight: 600;
    letter-spacing: -0.01em;
}}
h2 {{ font-size: 1.4rem; }}
h3 {{ font-size: 1.15rem; }}

p, span, label, li, .stMarkdown, .stMarkdown p {{
    color: var(--text);
}}

[data-testid="stMetric"] {{
    background: linear-gradient(135deg, #FFFFFF 0%, #FAF5EE 100%);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px 22px;
    box-shadow: 0 2px 8px rgba(45, 42, 38, 0.06), inset 0 1px 0 rgba(255,255,255,0.9);
    transition: all 0.2s ease;
}}
[data-testid="stMetric"]:hover {{
    border-color: var(--lavender);
    box-shadow: 0 6px 18px rgba(184, 181, 225, 0.25);
    transform: translateY(-1px);
}}
[data-testid="stMetricLabel"] {{
    color: var(--muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.72rem;
    font-weight: 600;
}}
[data-testid="stMetricValue"] {{
    color: var(--heading) !important;
    font-weight: 600;
    font-size: 1.85rem;
}}
[data-testid="stMetricDelta"] {{
    color: #5C8B4F !important;
    font-weight: 600;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: var(--subsurface);
    padding: 6px;
    border-radius: 16px;
    border: 1px solid var(--border);
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    border-radius: 12px;
    padding: 8px 14px;
    color: var(--muted);
    font-weight: 500;
    transition: all 0.15s ease;
}}
.stTabs [data-baseweb="tab"]:hover {{
    color: var(--ink);
    background: rgba(255, 255, 255, 0.55);
}}
.stTabs [aria-selected="true"] {{
    background: #FFFFFF !important;
    color: var(--heading) !important;
    border: 1px solid var(--border);
    box-shadow: 0 2px 6px rgba(45, 42, 38, 0.08);
}}

[data-testid="stDataFrame"], [data-testid="stTable"] {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 4px;
}}
/* Force pastel header on Streamlit's data-grid (used by st.dataframe).
   Streamlit renders the grid as a canvas + div header overlay. */
[data-testid="stDataFrame"] [role="columnheader"],
[data-testid="stDataFrame"] [data-testid="StyledDataFrameRowCellHeader"],
[data-testid="stDataFrame"] [class*="ColumnHeader"],
[data-testid="stDataFrame"] [class*="Header"] {{
    background: linear-gradient(180deg, #F5EFE6 0%, #F0E8DA 100%) !important;
    color: #1F1E1B !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {CORAL} !important;
}}
[data-testid="stDataFrame"] [role="columnheader"] * {{
    color: #1F1E1B !important;
    fill: #1F1E1B !important;
}}
/* Plain st.table (HTML table) header pastel */
[data-testid="stTable"] thead tr th {{
    background: linear-gradient(180deg, #F5EFE6 0%, #F0E8DA 100%) !important;
    color: #1F1E1B !important;
    font-weight: 700 !important;
    border-bottom: 2px solid {CORAL} !important;
}}
[data-testid="stTable"] tbody tr td {{
    background-color: var(--surface) !important;
    color: var(--text) !important;
}}

div[data-testid="stAlert"], div[data-baseweb="notification"] {{
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-left: 3px solid var(--lavender) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}}

.stTextInput input, .stSelectbox div[role="combobox"], .stTextArea textarea {{
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}}
.stTextInput input:focus, .stTextArea textarea:focus {{
    border-color: var(--lavender) !important;
    box-shadow: 0 0 0 3px rgba(184, 181, 225, 0.30) !important;
}}

.stButton button {{
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text) !important;
    transition: all 0.15s ease !important;
    font-weight: 500 !important;
}}
.stButton button:hover {{
    border-color: var(--lavender) !important;
    color: #4A4078 !important;
    background: rgba(184, 181, 225, 0.10) !important;
}}
.stButton button[kind="primary"] {{
    background: linear-gradient(135deg, var(--lavender) 0%, var(--peach) 100%) !important;
    color: var(--ink) !important;
    border: none !important;
    font-weight: 600 !important;
    box-shadow: 0 3px 10px rgba(184, 181, 225, 0.40) !important;
}}
.stButton button[kind="primary"]:hover {{
    color: var(--ink) !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(245, 196, 160, 0.50) !important;
}}

div[data-testid="stCodeBlock"], pre, code {{
    background: var(--subsurface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: #5A4E3F !important;
}}

.attrisense-banner {{
    background:
        radial-gradient(circle at 0% 0%, rgba(184, 181, 225, 0.55) 0%, transparent 50%),
        radial-gradient(circle at 100% 100%, rgba(245, 196, 160, 0.55) 0%, transparent 50%),
        linear-gradient(120deg, #FFFFFF 0%, #F5EFE6 60%, #F0E7D6 100%);
    color: var(--heading);
    padding: 28px 34px;
    border-radius: 22px;
    margin-bottom: 18px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 24px rgba(184, 181, 225, 0.18);
    position: relative;
    overflow: hidden;
}}
.attrisense-banner::before {{
    content: "";
    position: absolute;
    top: -40%;
    right: -8%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(181, 212, 168, 0.45) 0%, transparent 70%);
    pointer-events: none;
}}
.attrisense-banner h1 {{
    color: var(--heading) !important;
    margin: 0;
    font-size: 2.0rem;
    letter-spacing: -0.02em;
    font-weight: 700;
    position: relative;
}}
.attrisense-banner h1 .accent {{
    background: linear-gradient(135deg, #6E58B8 0%, #C97A4A 50%, #5C8B4F 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}
.attrisense-banner p {{
    color: var(--text);
    margin: 8px 0 0 0;
    font-size: 0.98rem;
    position: relative;
}}

.attrisense-disclosure {{
    background: rgba(245, 225, 160, 0.40);
    border-left: 3px solid #C9A845;
    color: #6B5A1F;
    padding: 10px 16px;
    border-radius: 10px;
    font-size: 0.84rem;
    margin-bottom: 14px;
}}

[data-testid="stCaptionContainer"], .stCaption {{
    color: var(--muted) !important;
}}

hr {{
    border-color: var(--border);
}}

a {{
    color: #6E58B8 !important;
}}
a:hover {{
    color: #4A4078 !important;
}}
</style>
"""


def render_brand_header(title: str, tagline: str) -> str:
    """HTML for the top brand banner."""
    return (
        f'<div class="attrisense-banner">'
        f'<h1><span class="accent">{title}</span></h1>'
        f"<p>{tagline}</p>"
        f"</div>"
    )


def render_disclosure(text: str) -> str:
    """HTML for the synthetic-data disclosure ribbon."""
    return f'<div class="attrisense-disclosure">{text}</div>'
