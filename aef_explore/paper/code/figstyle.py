"""Shared figure style for the manuscript: RSE column widths, 300 dpi, >= 7 pt type."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

MM = 1 / 25.4
W1, W2 = 90 * MM, 190 * MM          # single- and double-column widths
DPI = 300
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
    "ytick.color": INK2, "axes.edgecolor": "#aab1b8", "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
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


def save(fig, name):
    p = f"{OUT}/{name}"
    fig.savefig(p, dpi=DPI)
    plt.close(fig)
    print("wrote", p)
