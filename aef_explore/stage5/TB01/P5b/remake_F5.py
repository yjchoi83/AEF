"""P5b -- rebuild P5 figure F5 after item 4.

Congo can no longer be shown as a 5.3 pp bar: on 2021-vintage dates the low-observation bin
holds 8 events, below the pre-registered floor of 100, so no gap is estimable. The panel now
carries the two Brazilian estimates and states the Congo position instead of drawing it.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "aef_explore/stage5/TB01/P5/figures/F5_congo_panel.png"
INK, INK2 = "#1f2328", "#57606a"
BARS = [("Brazil 2021", 34.4, 28.4, 40.2, "#12436d"),
        ("Brazil 2020", 14.1, 11.6, 16.6, "#a8560c")]

fig, ax = plt.subplots(figsize=(9.6, 5.0))
fig.subplots_adjust(left=0.11, right=0.98, top=0.85, bottom=0.16)
for i, (lab, v, lo, hi, c) in enumerate(BARS):
    ax.bar(i, v, width=0.55, color=c, zorder=2)
    ax.errorbar(i, v, yerr=[[v - lo], [hi - v]], color=INK, lw=1.8, capsize=6, zorder=3)
    ax.annotate(f"{v:.1f} pp\n[{lo:.1f}, {hi:.1f}]", (i, hi), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=10, color=INK)
ax.set_xlim(-0.6, 2.6)
ax.set_ylim(0, 47)
ax.axvspan(1.5, 2.6, color="#f4f5f6", zorder=0)
ax.annotate("Congo\n\nno estimate", (2.05, 24), ha="center", va="center", fontsize=11,
            color=INK)
ax.annotate("re-dated on RADD v20220109 (P5b item 4):\n"
            "n(clear_post ≤ 2) = 8, below the pre-registered\n"
            "floor of 100 — the gap is not estimable.\n"
            "P4's 5.3 pp rested on 2024-vintage dates,\n"
            "3.4 % of which fall in 2022.",
            (2.05, 11), ha="center", va="center", fontsize=8.6, color=INK2)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["Brazil 2021", "Brazil 2020", "Congo"], fontsize=11, color=INK)
ax.set_ylabel("registration gap, clear_post ≤ 2 vs ≥ 5 (pp)", fontsize=10, color=INK2)
ax.tick_params(colors=INK2, labelsize=10)
ax.grid(axis="y", color="#e8ebee", lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#c9ced4")
ax.set_title("F5  Effect size is region- and year-specific — and unmeasured in the Congo",
             fontsize=12.5, color=INK, loc="left")
fig.savefig(OUT, dpi=150)
print("wrote", OUT)
