"""P5b item 2, step 2 -- the two replacement map plates, drawn locally from the NPY
supply stacks so no Earth Engine work is repeated per panel.

F7  expected observation supply: mean clear Sentinel-2 observations per pixel per
    calendar month (2019-2021 mean), 2 regions x 12 months, one sequential hue.
F8  deferral risk by event month: 1 - sigmoid(b0 + b1 * ln(1 + E_m)), where E_m is the
    expected post-event clear count for an event in month m under the same proration
    rule P2 used for `clear_post`.

The link is refitted here rather than reused from P5. P5's map layer (d) used
sigmoid(2.1413 + 0.0552 * count), linear in the raw count, which is badly mis-calibrated
where it matters: it predicts 0.91 registration at one post-event clear observation, where
the data show 0.59. Logit-linear in ln(1 + clear_post) tracks the empirical curve to within
a few points across the whole range. The exactly-zero bin is excluded from the fit, being a
dating artifact rather than an observation state (item 1).
"""
import json
import numpy as np
import numpy.lib.recfunctions as rf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

P2_CSV = "aef_explore/stage5/TB01/P2/P2_events.csv"
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
REG = ["ParaBR163", "Roraima_S"]
LBL = {"ParaBR163": "Pará / BR-163", "Roraima_S": "Roraima (south)"}
OUT = "aef_explore/stage5/TB01/P5b/figures"
INK, INK2 = "#1f2328", "#57606a"
# single-hue sequential ramps (light -> dark), per the sequential-colour rule
BLUE = LinearSegmentedColormap.from_list("blue", ["#f2f7fb", "#cfe0ef", "#8ab4d8", "#3d7ebc", "#12436d"])
RED = LinearSegmentedColormap.from_list("red", ["#fdf4f2", "#f7d3c9", "#e79c86", "#c85f3f", "#7d2b12"])
SERIES = {"ParaBR163": "#12436d", "Roraima_S": "#a8560c"}


def fit_link():
    """logit P(registered) = b0 + b1 * ln(1 + clear_post), on the 2021 dated events."""
    import pandas as pd
    d = pd.read_csv(P2_CSV).dropna(subset=["clear_post_radd_any"])
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
    cal = []
    edges = [0, 1, 2, 3, 4, 6, 9, 14, 25, 50, 1e9]
    cp = d["clear_post_radd_any"].values
    for a, c in zip(edges[:-1], edges[1:]):
        m = (cp > a) & (cp <= c)
        if m.sum() > 20:
            cal.append(dict(bin=f"({a:g},{c:g}]", n=int(m.sum()),
                            emp=round(float(y[m].mean()), 3),
                            pred=round(float(1 / (1 + np.exp(-(b[0] + b[1] * np.log1p(cp[m]).mean())))), 3)))
    return float(b[0]), float(b[1]), cal


def load(tmp, name):
    a = np.load(f"{tmp}/supply_{name}.npy")
    return rf.structured_to_unstructured(a).astype(float)


def expected(sup):
    """E_m per pixel: half the event month plus every later month."""
    out = np.empty_like(sup)
    for m in range(12):
        out[..., m] = 0.5 * sup[..., m] + sup[..., m + 1:].sum(axis=2)
    return out


def risk(e, b0, b1):
    return 1.0 - 1.0 / (1.0 + np.exp(-(b0 + b1 * np.log1p(e))))


def plate_supply(data, path):
    vmax = 8.0
    fig = plt.figure(figsize=(13.6, 6.4))
    gs = fig.add_gridspec(3, 12, height_ratios=[1.0, 1.0, 0.95], hspace=0.18, wspace=0.06,
                          left=0.05, right=0.985, top=0.90, bottom=0.09)
    for r, name in enumerate(REG):
        sup = data[name]["sup"]
        for m in range(12):
            ax = fig.add_subplot(gs[r, m])
            ax.imshow(sup[..., m], cmap=BLUE, vmin=0, vmax=vmax, interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#d8dde3")
            if r == 0:
                ax.set_title(MON[m], fontsize=8.5, color=INK2, pad=3)
            if m == 0:
                ax.set_ylabel(LBL[name], fontsize=9, color=INK)
    ax = fig.add_subplot(gs[2, :])
    for name in REG:
        mu = np.nanmean(data[name]["sup"], axis=(0, 1))
        ax.plot(range(1, 13), mu, lw=2, color=SERIES[name], marker="o", ms=5,
                label=LBL[name], zorder=3)
        j = int(np.argmax(mu))
        ax.annotate(f"{mu[j]:.1f}", (j + 1, mu[j]), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=8.5, color=INK)
        j = int(np.argmin(mu))
        ax.annotate(f"{mu[j]:.1f}", (j + 1, mu[j]), textcoords="offset points",
                    xytext=(0, -13), ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(MON, fontsize=9, color=INK2)
    ax.set_ylabel("region-mean clear obs / month", fontsize=9, color=INK2)
    ax.set_ylim(0, 7.4)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color="#e8ebee", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c9ced4")
    ax.legend(frameon=False, fontsize=9, loc="upper left", labelcolor=INK)
    sm = plt.cm.ScalarMappable(cmap=BLUE, norm=plt.Normalize(0, vmax))
    cb = fig.colorbar(sm, ax=fig.axes[:24], location="right", fraction=0.012, pad=0.006)
    cb.set_label("clear S2 observations in month (2019-2021 mean)", fontsize=8.5, color=INK2)
    cb.ax.tick_params(labelsize=8, colors=INK2)
    cb.outline.set_visible(False)
    fig.suptitle("Expected Sentinel-2 clear-observation supply, by calendar month",
                 fontsize=13, color=INK, x=0.05, ha="left", y=0.975)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plate_risk(data, path):
    cols = [2, 5, 8, 11]  # Mar, Jun, Sep, Dec
    vmax = 0.60
    fig = plt.figure(figsize=(11.2, 7.0))
    gs = fig.add_gridspec(3, 4, height_ratios=[1.0, 1.0, 0.9], hspace=0.16, wspace=0.06,
                          left=0.07, right=0.88, top=0.90, bottom=0.08)
    for r, name in enumerate(REG):
        rk = data[name]["risk"]
        for c, m in enumerate(cols):
            ax = fig.add_subplot(gs[r, c])
            ax.imshow(rk[..., m], cmap=RED, vmin=0, vmax=vmax, interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#d8dde3")
            if r == 0:
                ax.set_title(f"event in {MON[m]}", fontsize=10, color=INK2, pad=4)
            if c == 0:
                ax.set_ylabel(LBL[name], fontsize=10, color=INK)
    ax = fig.add_subplot(gs[2, :])
    for k, name in enumerate(REG):
        mu = np.nanmean(data[name]["risk"], axis=(0, 1))
        p90 = np.nanpercentile(data[name]["risk"], 90, axis=(0, 1))
        ax.plot(range(1, 13), mu, lw=2, color=SERIES[name], marker="o", ms=5,
                label=LBL[name] + " (pixel mean)", zorder=3)
        ax.plot(range(1, 13), p90, lw=1.6, ls="--", color=SERIES[name],
                label=LBL[name] + " (pixel p90)", zorder=2)
        ax.annotate(f"{mu[-1]:.2f}", (12, mu[-1]), textcoords="offset points",
                    xytext=(-6, -12 if k else 4), ha="right", fontsize=9, color=INK)
    ax.set_xticks(range(1, 13)); ax.set_xticklabels(MON, fontsize=9, color=INK2)
    ax.set_ylabel("mean deferral risk", fontsize=9, color=INK2)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.grid(axis="y", color="#e8ebee", lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c9ced4")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", labelcolor=INK, ncol=2)
    sm = plt.cm.ScalarMappable(cmap=RED, norm=plt.Normalize(0, vmax))
    cb = fig.colorbar(sm, ax=fig.axes[:8], location="right", fraction=0.018, pad=0.01)
    cb.set_label("P(not registered in event year)", fontsize=8.5, color=INK2)
    cb.ax.tick_params(labelsize=8, colors=INK2)
    cb.outline.set_visible(False)
    fig.suptitle("Deferral risk implied by observation supply, by event month",
                 fontsize=13, color=INK, x=0.07, ha="left", y=0.975)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(tmp):
    b0, b1 = 0.0, 0.0
    b0, b1, cal = fit_link()
    print("link b0=%.4f b1=%.4f" % (b0, b1))
    data, stats = {}, {"_link": dict(b0=b0, b1=b1, calibration=cal)}
    for name in REG:
        sup = load(tmp, name)
        e = expected(sup)
        rk = risk(e, b0, b1)
        data[name] = dict(sup=sup, e=e, risk=rk)
        stats[name] = dict(
            supply_mean=[round(float(x), 3) for x in np.nanmean(sup, axis=(0, 1))],
            supply_p10=[round(float(x), 3) for x in np.nanpercentile(sup, 10, axis=(0, 1))],
            supply_p90=[round(float(x), 3) for x in np.nanpercentile(sup, 90, axis=(0, 1))],
            expected_mean=[round(float(x), 3) for x in np.nanmean(e, axis=(0, 1))],
            risk_mean=[round(float(x), 4) for x in np.nanmean(rk, axis=(0, 1))],
            risk_p90=[round(float(x), 4) for x in np.nanpercentile(rk, 90, axis=(0, 1))],
            annual_mean=round(float(np.nanmean(sup.sum(axis=2))), 2))
    plate_supply(data, f"{OUT}/F7_obs_supply.png")
    plate_risk(data, f"{OUT}/F8_deferral_risk.png")
    json.dump(stats, open("aef_explore/stage5/TB01/P5b/obs_supply_stats.json", "w"), indent=1)
    for k, v in list(stats.items())[1:]:
        print(k, "annual", v["annual_mean"], "risk Jan/Dec",
              v["risk_mean"][0], v["risk_mean"][11])


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
