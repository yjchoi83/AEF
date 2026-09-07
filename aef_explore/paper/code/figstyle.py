"""Shared figure style for the manuscript: RSE column widths, 300 dpi, >= 7 pt type."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MM = 1 / 25.4
W1, W2 = 90 * MM, 190 * MM          # single- and double-column widths
DPI = 300
MIN_PT = 7.0                        # smallest type the journal accepts at final size
WIDTHS_MM = (90.0, 190.0)
OUT = "aef_explore/paper/figures"
NUMBERS = "aef_explore/paper/numbers.json"

INK, INK2, GRID = "#111418", "#5b6470", "#e4e8ec"
# categorical hues, assigned in fixed order and never cycled
C = {"2021": "#12436d", "2020": "#a8560c", "congo": "#3d6b35", "alt": "#7b5ea7",
     "flag": "#a4243b", "grey": "#7c848d"}
SEQ_BLUE = ["#f2f7fb", "#cfe0ef", "#8ab4d8", "#3d7ebc", "#12436d"]
SEQ_RED = ["#fdf4f2", "#f7d3c9", "#e79c86", "#c85f3f", "#7d2b12"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 7.5,
    "axes.labelsize": 7.5, "axes.titlesize": 8, "xtick.labelsize": 7,
    "ytick.labelsize": 7, "legend.fontsize": 7, "figure.dpi": DPI,
    "savefig.dpi": DPI, "axes.linewidth": 0.6, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "lines.linewidth": 1.2, "patch.linewidth": 0.6,
    "axes.labelcolor": INK2, "text.color": INK, "xtick.color": INK2,
    "ytick.color": INK2, "axes.edgecolor": "#aab1b8",
    # NOT "tight": a tight bounding box crops the canvas, so the delivered file would be
    # narrower than the column it is drawn for and the journal would scale it back up,
    # changing every type size. Figures are saved at exactly the canvas size instead.
    "savefig.bbox": None, "savefig.pad_inches": 0.0,
})


def numbers():
    return json.load(open(NUMBERS))


def tidy(ax, grid="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=GRID, lw=0.5)
        ax.set_axisbelow(True)
    return ax


def panel_tag(ax, tag, dx=-0.02, dy=1.06):
    ax.text(dx, dy, tag, transform=ax.transAxes, fontsize=8, fontweight="bold",
            color=INK, ha="left", va="top")


def check(fig, name=""):
    """Assert the submission specification: column width, 300 dpi, and no type under 7 pt.

    Figures are drawn at final size, so the font sizes here are the printed font sizes and
    the minimum is a hard requirement rather than a guideline.
    """
    w_mm = fig.get_size_inches()[0] * 25.4
    if not any(abs(w_mm - w) < 0.6 for w in WIDTHS_MM):
        raise AssertionError(f"{name}: width {w_mm:.1f} mm is neither 90 nor 190 mm")
    if abs(fig.dpi - DPI) > 1e-6:
        raise AssertionError(f"{name}: figure dpi is {fig.dpi}, expected {DPI}")
    fig.canvas.draw()
    small = []
    for t in fig.findobj(match=lambda o: hasattr(o, "get_fontsize") and hasattr(o, "get_text")):
        if not (t.get_text() or "").strip() or not t.get_visible():
            continue
        if t.get_fontsize() < MIN_PT - 1e-9:
            small.append((round(t.get_fontsize(), 2), (t.get_text() or "")[:28]))
    if small:
        raise AssertionError(f"{name}: {len(small)} text objects under {MIN_PT} pt: "
                             f"{sorted(set(small))[:6]}")
    # nothing may sit outside the canvas: the file is saved at exactly the canvas size, so
    # anything beyond it is cropped rather than shrunk
    tb = fig.get_tightbbox(fig.canvas.get_renderer())
    w_in, h_in = fig.get_size_inches()
    over = {k: round(v, 3) for k, v in
            (("left", -tb.x0), ("bottom", -tb.y0), ("right", tb.x1 - w_in),
             ("top", tb.y1 - h_in)) if v > 0.01}
    if over:
        raise AssertionError(f"{name}: content outside the canvas (inches): {over}")
    return w_mm


def save(fig, name):
    p = f"{OUT}/{name}"
    w_mm = check(fig, name)
    fig.savefig(p, dpi=DPI, bbox_inches=None, pad_inches=0.0)
    plt.close(fig)
    from PIL import Image
    with Image.open(p) as im:
        px, dpi = im.size[0], im.info.get("dpi", (0, 0))[0]
    want = round(w_mm / 25.4 * DPI)
    if abs(px - want) > 1:
        raise AssertionError(f"{name}: saved {px} px wide, expected {want} for {w_mm:.0f} mm")
    if abs(dpi - DPI) > 0.01:
        raise AssertionError(f"{name}: saved dpi {dpi}, expected {DPI}")
    print(f"wrote {p}  ({w_mm:.0f} mm, {px} px, {DPI} dpi, min type {MIN_PT} pt)")
