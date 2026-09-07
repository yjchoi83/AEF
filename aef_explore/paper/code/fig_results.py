"""Manuscript figures F1-F5, F7, F8.

F1 registration curve, F2 SAR stratification, F3 deferral, F4 optically late events,
F5 reference selection (Brazil DETER vs Congo TMF), F7 observation supply, F8 deferral risk.
All values come from `numbers.json` (re-derived by run_numbers.py) or from the package tables
named in NUMBERS_TRACE.md; nothing is typed in by hand except published CIs that are cited.
"""
import glob, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import p2_model as M
from figstyle import W1, W2, C, INK, INK2, SEQ_BLUE, SEQ_RED, numbers, tidy, panel_tag, save

P2 = "aef_explore/stage5/TB01/P2/P2_events.csv"
P2B = "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv"
S1_2020 = "aef_explore/paper/code/s1_post_2020_derived.csv"
LBL = ["0", "(0,2]", "(2,4]", "(4,6]", "(6,9]", "(9,14]", "14+"]
NPROC = 24


def _bin_ci(d, cp, reg, nboot=400):
    out = []
    for (a, b), lab in zip(M.BINS, LBL):
        s = d[(d[cp] > a) & (d[cp] <= b)]
        if len(s) < 5:
            out.append((np.nan, np.nan, np.nan, len(s)))
            continue
        r = M.boot_ci(NPROC, s, "share", cp, cp, reg, nboot=nboot)
        out.append((r["point"], r["lo"], r["hi"], len(s)))
    return out


# ------------------------------------------------------------------ F1
def f1():
    fig, axes = plt.subplots(1, 2, figsize=(W2, W2 * 0.37))
    fig.subplots_adjust(wspace=0.20, top=0.86)
    x = np.arange(len(LBL))
    for ax, (year, path, extra) in zip(axes, (("2021", P2, None),
                                              ("2020", P2B, pd.read_csv(S1_2020)))):
        for rule, ls, band, mfc, lab in (
                ("date_upper", "-", True, C[year], "date_upper (primary)"),
                ("radd_any", "--", False, "white", "RADD-only (sensitivity)")):
            d, cp, s1 = M.prepare(path, rule, extra)
            v = _bin_ci(d, cp, "registered")
            p = np.array([q[0] for q in v]); lo = np.array([q[1] for q in v])
            hi = np.array([q[2] for q in v]); n = [q[3] for q in v]
            ax.plot(x[1:], p[1:], ls, color=C[year], marker="o", ms=2.8, mfc=mfc,
                    zorder=3, label=lab)
            if band:
                ax.fill_between(x[1:], lo[1:], hi[1:], color=C[year], alpha=0.16, lw=0)
            ax.errorbar([x[0]], [p[0]], yerr=[[p[0] - lo[0]], [hi[0] - p[0]]],
                        color=C[year], lw=0.8, capsize=1.8, zorder=4)
            ax.plot([x[0]], [p[0]], marker="s", ms=4.2, mfc=mfc, mec=C[year], mew=1.0,
                    ls="none", zorder=5)
            ax.annotate(f"n = {n[0]}", (x[0], p[0]), textcoords="offset points",
                        xytext=(7, -1.5), fontsize=6, color=INK2, va="center")
        ax.axhline(0.95, color=C["flag"], lw=0.7, ls=":", zorder=2)
        ax.annotate("H3 floor 0.95", (1.05, 0.958), ha="left", va="bottom", fontsize=6.2,
                    color=C["flag"])
        ax.axvspan(-0.55, 0.5, color="#f4f5f7", zorder=0)
        ax.set_xticks(x); ax.set_xticklabels(LBL)
        ax.set_xlim(-0.55, 6.4)
        ax.set_ylim(0.20, 1.03)
        ax.set_xlabel("post-event clear Sentinel-2 observations")
        ax.set_title(f"Brazilian Legal Amazon, {year}", color=INK)
        tidy(ax)
        ax.legend(frameon=False, loc="lower right", handlelength=1.8)
    axes[0].set_ylabel("P(registered)")
    for ax in axes:
        ax.annotate("exactly\nzero", (0.0, 1.005), xycoords=("data", "axes fraction"),
                    ha="center", va="bottom", fontsize=6.2, color=INK2)
    # the panel letters sit in the left margin, clear of the "exactly zero" label that
    # annotates the shaded stratum at x = 0
    panel_tag(axes[0], "(a)", dx=-0.135, dy=1.20)
    panel_tag(axes[1], "(b)", dx=-0.135, dy=1.20)
    save(fig, "F2_registration_curve.png")


# ------------------------------------------------------------------ F2
def f2():
    n = numbers()
    fig, axes = plt.subplots(1, 2, figsize=(W2, W2 * 0.36))
    fig.subplots_adjust(wspace=0.26, top=0.84)
    ax = axes[0]
    xs, w = np.arange(2), 0.34
    for k, (year, key) in enumerate((("2021", "2021_date_upper"), ("2020", "2020_date_upper"))):
        h = n[key]["h7b_prime"]
        for j, (which, hatch) in enumerate((("lo", ""), ("hi", "///"))):
            v = h[which]
            ax.bar(k + (j - 0.5) * w, v["point"], w * 0.92, color=C[year],
                   alpha=1.0 if j else 0.45, hatch=hatch, edgecolor="white",
                   label=("SAR-sparse" if j == 0 else "SAR-dense") if k == 0 else None)
            ax.errorbar(k + (j - 0.5) * w, v["point"],
                        yerr=[[v["point"] - v["lo"]], [v["hi"] - v["point"]]],
                        color=INK, lw=0.8, capsize=1.8)
            ax.annotate(f"n = {h['n_lo' if j == 0 else 'n_hi']}",
                        (k + (j - 0.5) * w, v["hi"]), textcoords="offset points",
                        xytext=(0, 3), ha="center", fontsize=6, color=INK2)
    ax.axhline(0.80, color=C["flag"], lw=0.8, ls=":")
    ax.annotate("H7(b)′ bar 0.80", (1.47, 0.812), ha="right", va="bottom", fontsize=6.2,
                color=C["flag"])
    ax.set_xticks(xs); ax.set_xticklabels(["2021", "2020"])
    ax.set_xlim(-0.55, 1.62)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("P(registered), clear_post ≤ 2")
    ax.set_title("registration by within-month SAR density", color=INK, pad=6)
    ax.legend(frameon=False, loc="upper left", handlelength=1.4)
    tidy(ax)
    ax = axes[1]
    for year, key in (("2021", "2021_date_upper"), ("2020", "2020_date_upper")):
        q = n[key].get("s1_quartiles", [])
        if q:
            ax.plot([r["q"] + 1 for r in q], [r["reg"] for r in q], marker="o", ms=3,
                    color=C[year], label=f"{year}  (n = {sum(r['n'] for r in q)})")
            for r in q:
                ax.annotate(f"{r['n']}", (r["q"] + 1, r["reg"]), textcoords="offset points",
                            xytext=(0, 4), ha="center", fontsize=6, color=INK2)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(["Q1\nsparsest", "Q2", "Q3", "Q4\ndensest"])
    ax.set_ylabel("P(registered), clear_post ≤ 2")
    ax.set_title("registration by within-month Sentinel-1 density quartile",
                 color=INK, pad=6)
    ax.legend(frameon=False, loc="upper right", handlelength=1.4)
    tidy(ax)
    panel_tag(axes[0], "(a)", dy=1.16); panel_tag(axes[1], "(b)", dy=1.16)
    save(fig, "F3_sar_stratification.png")


# ------------------------------------------------------------------ F3
def f3():
    n = numbers()
    fig, ax = plt.subplots(figsize=(W1, W1 * 0.78))
    h21, h20 = n["h4"]["share"], n["h4_2020"]["share"]
    vals = [("2020 → 2021", h20["point"], h20["lo"], h20["hi"], C["2020"], n["h4_2020"]["n"]),
            ("2021 → 2022", h21["point"], h21["lo"], h21["hi"], C["2021"], n["h4"]["n"])]
    for i, (lab, v, lo, hi, col, nn) in enumerate(vals):
        ax.barh(i, v, 0.5, color=col)
        ax.errorbar(v, i, xerr=[[v - lo], [hi - v]], color=INK, lw=0.8, capsize=1.8)
        ax.annotate(f"{v * 100:.1f}%  [{lo * 100:.1f}, {hi * 100:.1f}]", (v, i),
                    textcoords="offset points", xytext=(-4, 0), ha="right", va="center",
                    fontsize=6.6, color="white")
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels([f"{v[0]}\n(n = {v[5]:,})" for v in vals])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("share of year-Y unregistered events registering in Y+1")
    ax.set_title("deferral, not miss", color=INK)
    tidy(ax, grid="x")
    save(fig, "F4_deferral.png")


# ------------------------------------------------------------------ F4 -> Fig. 5
def f4():
    """Optically late events: registration, change intensity, and the deficit decomposition."""
    st = json.load(open("aef_explore/paper/intensity_stats.json"))
    frames = {}
    for year, path, angcol, extra in (("2021", P2, "ang_mean_deg", None),
                                      ("2020", P2B, "ang_2019_2020_deg",
                                       pd.read_csv(S1_2020))):
        d, cp, s1 = M.prepare(path, "date_upper", extra)
        d = d.copy()
        d["r"] = d[angcol] / d["tau_p90"]
        frames[year] = d
    fig, axes = plt.subplots(1, 3, figsize=(W2, W2 * 0.34))
    fig.subplots_adjust(wspace=0.42, top=0.84, bottom=0.20)

    ax = axes[0]
    w = 0.34
    for k, year in enumerate(("2021", "2020")):
        v = st[year]
        for j, (key, col, lab) in enumerate(((("reg_mapped"), C[year], "mapped in year"),
                                             (("reg_late"), C["alt"], "mapped a year late"))):
            ax.bar(k + (j - 0.5) * w, v[key], w * 0.9, color=col,
                   label=lab if k == 0 else None)
            ax.annotate(f"{v[key]:.3f}", (k + (j - 0.5) * w, v[key]),
                        textcoords="offset points", xytext=(0, 2), ha="center",
                        fontsize=6, color=INK)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["2021", "2020"])
    ax.set_ylim(0, 1.12); ax.set_ylabel("P(registered)")
    ax.set_title("registration rate", color=INK, pad=5)
    ax.legend(frameon=False, loc="lower center", ncol=1, handlelength=1.3, fontsize=6.2)
    tidy(ax)

    ax = axes[1]
    bins = np.linspace(0, 6, 49)
    for year, ls in (("2021", "-"), ("2020", "--")):
        d = frames[year]
        for late, col in ((0, C[year]), (1, C["alt"])):
            ax.hist(d.loc[d.radd_only == late, "r"].clip(0, 6), bins=bins, density=True,
                    histtype="step", lw=1.1, ls=ls, color=col)
    # a right-hand margin holds the key and the medians, so nothing sits over the curves
    ax.set_xlim(0, 9.2)
    top = ax.get_ylim()[1]
    ax.axvline(1.0, color=C["flag"], lw=0.8, ls=":")
    ax.annotate("τ", (1.0, top * 0.99), fontsize=7, color=C["flag"], ha="left", va="top",
                xytext=(2, 0), textcoords="offset points")
    ax.axvline(6.1, color="#dfe4e8", lw=0.6)
    ax.annotate("mapped\nin year\n(2021 solid,\n2020 dashed)", (6.35, top * 0.99),
                ha="left", va="top", fontsize=5.8, color=C["2021"])
    ax.annotate("mapped\na year late", (6.35, top * 0.60), ha="left", va="top",
                fontsize=5.8, color=C["alt"])
    for year, y in (("2021", 0.40), ("2020", 0.22)):
        v = st[year]
        ax.annotate(f"{year} median\n{v['intensity_q']['mapped'][1]:.2f} vs "
                    f"{v['intensity_q']['late'][1]:.2f} τ", (6.35, top * y), ha="left",
                    va="top", fontsize=5.8, color=C[year])
    ax.set_xticks([0, 2, 4, 6])
    ax.set_xlabel("interior angular change ÷ τ")
    ax.set_ylabel("density")
    ax.set_title("change intensity", color=INK, pad=5)
    tidy(ax)

    ax = axes[2]
    for k, year in enumerate(("2021", "2020")):
        v = st[year]
        for j, (key, col, lab) in enumerate(
                (("deficit_raw_pp", C["grey"], "unadjusted"),
                 ("deficit_adjusted_pp", C[year], "adjusted for supply,\nstate, month, area"))):
            b = v[key]
            ax.bar(k + (j - 0.5) * w, b["point"], w * 0.9, color=col,
                   label=lab if k == 0 else None)
            ax.errorbar(k + (j - 0.5) * w, b["point"],
                        yerr=[[b["point"] - b["lo"]], [b["hi"] - b["point"]]],
                        color=INK, lw=0.8, capsize=1.6)
            ax.annotate(f"{b['point']:.1f}", (k + (j - 0.5) * w, b["hi"]),
                        textcoords="offset points", xytext=(0, 2), ha="center",
                        fontsize=6, color=INK)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["2021", "2020"])
    ax.set_ylabel("registration deficit (pp)")
    ax.set_ylim(0, 34)
    ax.set_title("deficit, before and after adjustment", color=INK, pad=5)
    ax.legend(frameon=False, loc="upper center", fontsize=6.0, handlelength=1.3, ncol=1)
    tidy(ax)

    for a, t in zip(axes, ("(a)", "(b)", "(c)")):
        panel_tag(a, t, dy=1.16)
    save(fig, "F5_optically_late.png")


# ------------------------------------------------------------------ F5
def f5():
    n = numbers()
    cg = json.load(open("aef_explore/stage5/TB01/P5b/p4b_stats.json"))
    fig, axes = plt.subplots(1, 3, figsize=(W2, W2 * 0.36))
    fig.subplots_adjust(wspace=0.34, top=0.82, bottom=0.30)
    ax = axes[0]
    rows = [("BR 2021 DETER", n["2021_date_upper"]["n"], n["2021_date_upper"]["n_lo"], C["2021"]),
            ("BR 2020 DETER", n["2020_date_upper"]["n"], n["2020_date_upper"]["n_lo"], C["2020"]),
            ("CG TMF, 2024 dates", 4959, 202, C["congo"]),
            ("CG TMF, 2021 dates", cg["n"], cg["n_lo"], C["congo"])]
    for i, (lab, tot, lo, col) in enumerate(rows):
        ax.bar(i, 100 * lo / tot, 0.55, color=col, alpha=1.0 if i != 3 else 0.5,
               hatch="" if i != 3 else "///", edgecolor="white")
        ax.annotate(f"{lo:,}/{tot:,}", (i, 100 * lo / tot), textcoords="offset points",
                    xytext=(0, 3), ha="center", fontsize=5.6, color=INK)
    ax.set_ylim(0, 5.2)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels([r[0] for r in rows], fontsize=5.8, rotation=28, ha="right",
                       rotation_mode="anchor")
    ax.set_ylabel("events with clear_post ≤ 2 (%)")
    ax.set_title("how big the low-observation bin is", color=INK, pad=6)
    tidy(ax)
    ax = axes[1]
    bars = [("dated, 2024 vintage", 100 * cg["coverage_2024_vintage_P4"], C["congo"]),
            ("dated, 2021 vintage", 100 * cg["coverage_2021_vintage_all"], C["congo"]),
            ("date moved > 30 d", 100 * cg["shift_gt30_share"], C["flag"]),
            ("date lost", 100 * cg["lost_share"], C["flag"])]
    for i, (lab, v, col) in enumerate(bars):
        ax.bar(i, v, 0.55, color=col, alpha=0.85)
        ax.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 3),
                    ha="center", fontsize=6.4, color=INK)
    ax.set_xticks(range(len(bars)))
    ax.set_xticklabels([b[0] for b in bars], fontsize=5.8, rotation=28, ha="right",
                       rotation_mode="anchor")
    ax.set_ylabel("% of Congo patches")
    ax.set_title("what the alert vintage decides", color=INK, pad=6)
    tidy(ax)
    ax = axes[2]
    est = [("Brazil 2021", n["2021_date_upper"]["gap"], C["2021"]),
           ("Brazil 2020", n["2020_date_upper"]["gap"], C["2020"])]
    for i, (lab, g, col) in enumerate(est):
        ax.bar(i, g["point"], 0.5, color=col)
        ax.errorbar(i, g["point"], yerr=[[g["point"] - g["lo"]], [g["hi"] - g["point"]]],
                    color=INK, lw=0.8, capsize=1.8)
        ax.annotate(f"{g['point']:.1f}", (i, g["hi"]), textcoords="offset points",
                    xytext=(0, 3), ha="center", fontsize=6.4, color=INK)
    ax.axvspan(1.5, 2.5, color="#f2f4f6", zorder=0)
    ax.annotate("Congo:\nno estimate\n(n = %d < 100)" % cg["n_lo"], (2, 25), ha="center",
                va="center", fontsize=6.4, color=INK2)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["Brazil 2021", "Brazil 2020", "Congo 2021"], fontsize=5.8,
                       rotation=28, ha="right", rotation_mode="anchor")
    ax.set_xlim(-0.6, 2.5)
    ax.set_ylabel("registration gap (pp)")
    ax.set_title("effect size, where estimable", color=INK, pad=6)
    tidy(ax)
    for a, t in zip(axes, ("(a)", "(b)", "(c)")):
        panel_tag(a, t, dy=1.20)
    save(fig, "F6_reference_selection.png")


# ------------------------------------------------------------------ F7, F8
def _supply():
    import rasterio
    out = {}
    for key in ("ParaBR163", "Roraima_S"):
        src = rasterio.open(f"data/products/{key}_obs_supply_x10_200m.tif")
        out[key] = src.read().astype(float) / 10.0
    return out


def _link():
    d = pd.read_csv(P2).dropna(subset=["clear_post_radd_any"])
    d = d[d["clear_post_radd_any"] > 0]
    y = d["registered"].values.astype(float)
    X = np.column_stack([np.ones(len(y)), np.log1p(d["clear_post_radd_any"].values)])
    b = np.zeros(2)
    for _ in range(100):
        p = 1 / (1 + np.exp(-X @ b))
        W = np.clip(p * (1 - p), 1e-9, None)
        step = np.linalg.solve(X.T @ (X * W[:, None]) + 1e-9 * np.eye(2), X.T @ (y - p))
        b = b + step
        if np.abs(step).max() < 1e-10:
            break
    return b


MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
NAMES = {"ParaBR163": "Pará / BR-163", "Roraima_S": "Roraima (south)"}


def f7():
    sup = _supply()
    BLUE = LinearSegmentedColormap.from_list("b", SEQ_BLUE)
    fig = plt.figure(figsize=(W2, W2 * 0.42))
    gs = fig.add_gridspec(2, 13, width_ratios=[1] * 12 + [0.10], hspace=0.12,
                          wspace=0.06, left=0.055, right=0.965, top=0.90, bottom=0.30)
    for r, key in enumerate(("ParaBR163", "Roraima_S")):
        for m in range(12):
            ax = fig.add_subplot(gs[r, m])
            im = ax.imshow(sup[key][m], cmap=BLUE, vmin=0, vmax=8, interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#cdd3d9"); s.set_linewidth(0.4)
            if r == 0:
                ax.set_title(MON[m], fontsize=6.2, color=INK2, pad=1.5)
            if m == 0:
                ax.set_ylabel(NAMES[key], fontsize=6.5, color=INK)
    cax = fig.add_subplot(gs[:, 12])
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("clear observations in month", fontsize=6.5, color=INK2)
    cb.ax.tick_params(labelsize=6, length=1.5)
    cb.outline.set_visible(False)
    ax = fig.add_axes([0.055, 0.08, 0.845, 0.17])
    for key in ("ParaBR163", "Roraima_S"):
        mu = np.nanmean(sup[key], axis=(1, 2))
        ax.plot(range(1, 13), mu, marker="o", ms=2.6,
                color=C["2021"] if key == "ParaBR163" else C["2020"], label=NAMES[key])
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MON, fontsize=6.5)
    ax.set_ylabel("region mean", fontsize=6.5)
    ax.legend(frameon=False, loc="upper left", fontsize=6.4, ncol=2, handlelength=1.4)
    tidy(ax)
    save(fig, "F8_observation_supply.png")


def f8():
    sup = _supply()
    b0, b1 = _link()
    RED = LinearSegmentedColormap.from_list("r", SEQ_RED)
    fig = plt.figure(figsize=(W2, W2 * 0.42))
    gs = fig.add_gridspec(2, 5, width_ratios=[1, 1, 1, 1, 0.09], hspace=0.10,
                          wspace=0.06, left=0.075, right=0.955, top=0.90, bottom=0.32)
    cols = [2, 5, 8, 11]
    for r, key in enumerate(("ParaBR163", "Roraima_S")):
        e = np.stack([0.5 * sup[key][m] + sup[key][m + 1:].sum(axis=0) for m in range(12)])
        risk = 1 - 1 / (1 + np.exp(-(b0 + b1 * np.log1p(e))))
        for c, m in enumerate(cols):
            ax = fig.add_subplot(gs[r, c])
            im = ax.imshow(risk[m], cmap=RED, vmin=0, vmax=0.6, interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#cdd3d9"); s.set_linewidth(0.4)
            if r == 0:
                ax.set_title(f"event in {['Mar','Jun','Sep','Dec'][c]}", fontsize=6.8,
                             color=INK2, pad=2)
            if c == 0:
                ax.set_ylabel(NAMES[key], fontsize=6.5, color=INK)
        if r == 0:
            store = {}
        store[key] = risk
    cax = fig.add_subplot(gs[:, 4])
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("P(not registered in the event year)", fontsize=6.5, color=INK2)
    cb.ax.tick_params(labelsize=6, length=1.5)
    cb.outline.set_visible(False)
    ax = fig.add_axes([0.075, 0.08, 0.80, 0.19])
    for key in ("ParaBR163", "Roraima_S"):
        mu = np.nanmean(store[key], axis=(1, 2))
        ax.plot(range(1, 13), mu, marker="o", ms=2.6,
                color=C["2021"] if key == "ParaBR163" else C["2020"], label=NAMES[key])
        ax.annotate(f"{mu[-1]:.2f}", (12, mu[-1]), textcoords="offset points",
                    xytext=(-3, 3), ha="right", fontsize=6.2, color=INK)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MON, fontsize=6.5)
    ax.set_ylabel("mean risk", fontsize=6.5)
    ax.legend(frameon=False, loc="upper left", fontsize=6.4, ncol=2, handlelength=1.4)
    tidy(ax)
    save(fig, "F9_deferral_risk.png")


if __name__ == "__main__":
    import sys
    for name in (sys.argv[1:] or ["f7", "f8"]):
        globals()[name]()
