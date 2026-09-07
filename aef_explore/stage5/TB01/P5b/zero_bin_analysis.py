"""P5b item 1 -- what the clear_post == 0 bin actually is.

Four diagnostics the brief asks for, on both cohorts (2021 and 2020):
  1. the distribution of (DETER view_date - RADD date)
  2. registration under the `date_upper` dating variant
  3. the prior-year angular change against tau (the pre-event-disturbance explanation)
  4. the registration curve with December events excluded
plus `clear_post` recomputed from the DETER view_date, which is what separates the three
explanations from one another.
"""
import json, datetime as dt
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GEE = "/tmp/claude-1002/-d-yj-projects-workspace-yj-Alphaearth/b067b941-d951-4d64-87ce-af50dbd6f8bb/scratchpad/zero_bin_gee.csv"
OUT = "aef_explore/stage5/TB01/P5b"
INK, INK2 = "#1f2328", "#57606a"
C21, C20 = "#12436d", "#a8560c"
BINS = [(-0.1, 0), (0, 2), (2, 4), (4, 6), (6, 9), (9, 14), (14, 1e9)]
LBL = ["0", "0-2", "2-4", "4-6", "6-9", "9-14", "14+"]


def prorate(row, date):
    m = date.month
    dim = (dt.date(date.year + (m == 12), m % 12 + 1, 1) - dt.date(date.year, m, 1)).days
    tot = row[f"m{m:02d}"] * (dim - date.day) / dim
    for k in range(m + 1, 13):
        tot += row[f"m{k:02d}"]
    return tot


def curve(d, cp="clear_post_radd_any"):
    out = []
    for (a, b), lab in zip(BINS, LBL):
        s = d[(d[cp] > a) & (d[cp] <= b)]
        out.append(dict(bin=lab, n=int(len(s)),
                        reg=float(s["registered"].mean()) if len(s) else float("nan")))
    return out


def main():
    g = pd.read_csv(GEE)
    res = {}
    cohorts = {"2021": ("aef_explore/stage5/TB01/P2/P2_events.csv", 2021),
               "2020": ("aef_explore/stage5/TB01/P2b/P2b_events_2020.csv", 2020)}
    panel = {}
    for name, (path, yr) in cohorts.items():
        d = pd.read_csv(path).dropna(subset=["clear_post_radd_any"]).copy()
        d["vd"] = pd.to_datetime(d["view_date"])
        d["rd"] = pd.to_datetime(d["radd_any"])
        d["lag"] = (d["vd"] - d["rd"]).dt.days
        z = d[d["clear_post_radd_any"] == 0].copy()
        gg = g[g.cohort.astype(str) == name].set_index("event_id")
        z = z.join(gg, on="event_id", rsuffix="_gee")
        z["cp_view"] = [prorate(r, r["vd"].date()) if r["vd"].year == yr and not
                        pd.isna(r.get("m01")) else np.nan for _, r in z.iterrows()]
        r = {}
        r["n_zero"] = int(len(z))
        r["reg_zero"] = float(z["registered"].mean())
        r["reg_all"] = float(d["registered"].mean())
        # 1. lag distribution
        r["lag_pct_zero"] = [float(x) for x in np.nanpercentile(z["lag"], [5, 25, 50, 75, 95])]
        r["lag_pct_all"] = [float(x) for x in np.nanpercentile(d["lag"].dropna(), [5, 25, 50, 75, 95])]
        r["share_radd_after_view_zero"] = float((z["lag"] < 0).mean())
        r["share_radd_after_view_all"] = float((d["lag"] < 0).mean())
        r["share_lag_lt_-90_zero"] = float((z["lag"] < -90).mean())
        # 2. date_upper
        du = z["clear_post_date_upper"]
        r["date_upper_still_zero"] = float((du == 0).mean())
        r["date_upper_median_cp"] = float(np.nanmedian(du))
        r["reg_zero_under_date_upper_bin"] = float(
            d[d["clear_post_date_upper"] == 0]["registered"].mean())
        r["n_zero_under_date_upper"] = int((d["clear_post_date_upper"] == 0).sum())
        # 3. prior-year angular change vs tau
        ok = z["ang_prior"].notna()
        r["n_ang"] = int(ok.sum())
        r["prior_gt_tau_share"] = float((z.loc[ok, "ang_prior"] > z.loc[ok, "tau_p90"]).mean())
        r["event_gt_tau_share"] = float((z.loc[ok, "ang_event"] > z.loc[ok, "tau_p90"]).mean())
        r["prior_median_deg"] = float(z.loc[ok, "ang_prior"].median())
        r["event_median_deg"] = float(z.loc[ok, "ang_event"].median())
        r["tau_median"] = float(z.loc[ok, "tau_p90"].median())
        # background rate: prior-year change over tau among all registered events is unknown,
        # so the comparison is the zero bin's own event-year rate (above) and tau's definition
        # (p90 of stable forest => 10 % of undisturbed pixels exceed tau by construction).
        r["prior_gt_tau_share_reg"] = float(
            (z.loc[ok & (z.registered == 1), "ang_prior"] > z.loc[ok & (z.registered == 1), "tau_p90"]).mean())
        r["prior_gt_tau_share_unreg"] = float(
            (z.loc[ok & (z.registered == 0), "ang_prior"] > z.loc[ok & (z.registered == 0), "tau_p90"]).mean())
        # 4. clear_post recomputed from view_date
        cv = z["cp_view"].dropna()
        r["n_cp_view"] = int(len(cv))
        r["cp_view_pct"] = [float(x) for x in np.nanpercentile(cv, [5, 25, 50, 75, 95])]
        r["cp_view_le2_share"] = float((cv <= 2).mean())
        # 5. December-excluded registration curve
        r["curve_all"] = curve(d)
        r["curve_no_dec"] = curve(d[d["event_month"] != 12])
        r["curve_no_dec_view"] = curve(d[d["vd"].dt.month != 12])
        r["n_dec"] = int((d["event_month"] == 12).sum())
        r["zero_dec_share"] = float((z["event_month"] == 12).mean())
        res[name] = r
        panel[name] = dict(z=z, d=d)
        print(name, json.dumps({k: v for k, v in r.items() if not k.startswith("curve")},
                               indent=1)[:1400], flush=True)
    json.dump(res, open(f"{OUT}/zero_bin_stats.json", "w"), indent=1)
    figure(panel, res, f"{OUT}/figures/F9_zero_bin.png")


def figure(panel, res, path):
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.3))
    fig.subplots_adjust(left=0.055, right=0.985, top=0.83, bottom=0.15, wspace=0.26)
    # (a) lag
    ax = axes[0]
    bins = np.arange(-750, 400, 30)
    for name, c in (("2021", C21), ("2020", C20)):
        ax.hist(panel[name]["z"]["lag"].clip(-750, 390), bins=bins, color=c, alpha=0.6,
                density=True, label=f"{name} zero bin (n={res[name]['n_zero']})")
    ax.axvline(0, color=INK2, lw=1.2, ls="--")
    ax.annotate("←  RADD date after DETER view_date", (-740, ax.get_ylim()[1] * 0.60),
                ha="left", fontsize=8.5, color=INK2)
    ax.set_xlabel("DETER view_date − RADD date (days)", fontsize=9.5, color=INK2)
    ax.set_ylabel("density of zero-bin events", fontsize=9.5, color=INK2)
    ax.set_title("(a) the zero bin is dated late, not observed late", fontsize=10.5,
                 color=INK, loc="left")
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left")
    # (b) prior-year angular change vs tau
    ax = axes[1]
    for name, c in (("2021", C21), ("2020", C20)):
        z = panel[name]["z"]
        v = (z["ang_prior"] / z["tau_p90"]).dropna().sort_values()
        ax.plot(v.values, np.linspace(0, 1, len(v)), lw=2, color=c, label=f"{name} prior year")
        v = (z["ang_event"] / z["tau_p90"]).dropna().sort_values()
        ax.plot(v.values, np.linspace(0, 1, len(v)), lw=1.6, ls="--", color=c,
                label=f"{name} event year")
    ax.axvline(1, color=INK2, lw=1.2)
    ax.annotate("τ", (1, 0.02), fontsize=11, color=INK2, xytext=(4, 0),
                textcoords="offset points")
    ax.set_xlim(0, 3.2)
    ax.set_xlabel("angular change ÷ τ (state p90)", fontsize=9.5, color=INK2)
    ax.set_ylabel("cumulative share of zero-bin events", fontsize=9.5, color=INK2)
    ax.axhline(0.90, color="#c9ced4", lw=1.2, ls=":")
    ax.annotate("undisturbed-forest expectation", (0.05, 0.915), ha="left",
                fontsize=8, color=INK2)
    ax.set_title("(b) prior-year change vs τ: quiet in 2021, not in 2020",
                 fontsize=10.5, color=INK, loc="left")
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower right")
    # (c) registration curve, December in and out
    ax = axes[2]
    x = np.arange(len(LBL))
    for name, c in (("2021", C21), ("2020", C20)):
        for key, ls, lab in (("curve_all", "-", "all events"),
                             ("curve_no_dec", "--", "December excluded")):
            y = [b["reg"] for b in res[name][key]]
            ax.plot(x, y, ls, lw=2 if ls == "-" else 1.6, color=c, marker="o", ms=5,
                    label=f"{name}, {lab}")
    ax.set_xticks(x); ax.set_xticklabels(LBL, fontsize=9, color=INK2)
    ax.set_xlabel("post-event clear observations", fontsize=9.5, color=INK2)
    ax.set_ylabel("P(registered)", fontsize=9.5, color=INK2)
    ax.set_ylim(0.4, 1.02)
    ax.set_title("(c) the zero bin's lift survives dropping December", fontsize=10.5,
                 color=INK, loc="left")
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower right")
    for a in axes:
        a.tick_params(colors=INK2, labelsize=9)
        a.grid(axis="y", color="#e8ebee", lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            a.spines[s].set_color("#c9ced4")
    fig.suptitle("What the clear_post = 0 bin is", fontsize=13, color=INK, x=0.055,
                 ha="left", y=0.965)
    fig.savefig(path, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
