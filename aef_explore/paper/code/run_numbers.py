"""Re-derive every event-level number the manuscript uses, under both dating rules.

Writes `aef_explore/paper/numbers.json`.  Run: python run_numbers.py <s1_2020_monthly.csv>
"""
import json, sys, datetime as dt
import numpy as np, pandas as pd
import p2_model as M

P2 = "aef_explore/stage5/TB01/P2/P2_events.csv"
P2B = "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv"
OFF = "aef_explore/stage5/TB01/P2b/P2b_offset_2021.csv"
OUT = "aef_explore/paper/numbers.json"
NPROC = 32


def prorate(monthly, date, pre):
    m = date.month
    dim = (dt.date(date.year + (m == 12), m % 12 + 1, 1) - dt.date(date.year, m, 1)).days
    tot = monthly[f"{pre}_{m:02d}"] * (dim - date.day) / dim
    for k in range(m + 1, 13):
        tot = tot + monthly[f"{pre}_{k:02d}"]
    return tot


def s1_2020_table(path):
    """Build s1_post under both dating rules from the re-extracted monthly counts."""
    mon = pd.read_csv(path)
    ev = pd.read_csv(P2B)[["event_id", "radd_any", "date_upper"]]
    m = mon.merge(ev, on="event_id", how="inner")
    out = {"event_id": m["event_id"].values}
    for rule in ("radd_any", "date_upper"):
        dates = pd.to_datetime(m[rule])
        vals = np.full(len(m), np.nan)
        ok = dates.notna().values
        vals[ok] = [prorate(r, d.date(), "s1") for r, d in
                    zip(m[ok].to_dict("records"), dates[ok])]
        out["s1_post_" + rule] = vals
    return pd.DataFrame(out)


def offset_gaps(pool, res):
    """2021 gap with offset-suspect events removed, under both dating rules."""
    off = pd.read_csv(OFF)
    susp = set(off.loc[off["offset_suspect"] == 1, "event_id"])
    out = {"n_unregistered_checked": int(len(off)),
           "n_offset_suspect": int(off["offset_suspect"].sum()),
           "share": float(off["offset_suspect"].mean())}
    for rule in ("radd_any", "date_upper"):
        d, cp, s1 = M.prepare(P2, rule)
        d = d[~d["event_id"].isin(susp)]
        out[rule] = dict(n=int(len(d)),
                         gap=M.boot_ci(pool, d, "gap", cp, s1, "registered"),
                         coef_joint=M.boot_ci(pool, d, "coef_joint", cp, s1, "registered"))
    return out


def h4(pool):
    """Deferral: share of Y-unregistered events registering in Y+1 (dating-independent)."""
    t = pd.read_csv("aef_explore/stage5/TB01/P3/P3_table.csv")
    t = t.merge(pd.read_csv(P2)[["event_id", "block"]], on="event_id", how="left")
    u = t[t["reg_now"] == 0].copy()
    u = u[u["reg_next"].notna()]
    u["registered"] = u["reg_next"].astype(float)
    return dict(n=int(len(u)),
                share=M.boot_ci(pool, u, "share", "cp", "cp", "registered"))


def main(s1_path):
    res = {}
    s1_extra = s1_2020_table(s1_path)
    s1_extra.to_csv("aef_explore/paper/code/s1_post_2020_derived.csv", index=False)
    if True:
        pool = NPROC
        for year, path, extra in (("2021", P2, None), ("2020", P2B, s1_extra)):
            for rule in ("radd_any", "date_upper"):
                key = f"{year}_{rule}"
                d, cp, s1 = M.prepare(path, rule, extra)
                print("==", key, "n =", len(d), flush=True)
                res[key] = M.analyse(pool, d, cp, s1, tag=key)
                print("   gap %.2f [%.2f, %.2f]  coef %.3f [%.3f, %.3f]" % (
                    res[key]["gap"]["point"], res[key]["gap"]["lo"], res[key]["gap"]["hi"],
                    res[key]["coef_joint"]["point"], res[key]["coef_joint"]["lo"],
                    res[key]["coef_joint"]["hi"]), flush=True)
                json.dump(res, open(OUT, "w"), indent=1)
        for year, path, extra in (("2021", P2, None), ("2020", P2B, s1_extra)):
            for rule in ("date_upper", "radd_any"):
                print("== robustness", year, rule, flush=True)
                res[f"robust_{year}_{rule}"] = M.robustness(pool, path, rule, extra)
                json.dump(res, open(OUT, "w"), indent=1)
        res["offset_2021"] = offset_gaps(pool, res)
        res["h4"] = h4(pool)
        json.dump(res, open(OUT, "w"), indent=1)
    print("done")


if __name__ == "__main__":
    main(sys.argv[1])
