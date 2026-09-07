"""P5b item 4, step 3 -- Congo replication under 2021-vintage dating.

Joins the re-dated patches to P4_table.csv (which carries the angular change and the
registration outcome -- neither of which dating can change), recomputes `clear_post` and
`s1_post` from the new dates under P4's proration rule, and re-runs the pre-registered
gap and the H7(a) coefficient with the same 0.5 deg block bootstrap.
"""
import datetime as dt, json, sys
import numpy as np, pandas as pd
from multiprocessing import Pool

EPOCH = dt.date(2014, 12, 31)
NBOOT = 1000
BR21_CI = (28.4, 40.2)
rng_master = np.random.default_rng(20260907)


def prorate(row, date, pre):
    """Counts strictly after `date`, with the event month prorated by days remaining."""
    m = date.month
    dim = (dt.date(date.year + (m == 12), m % 12 + 1, 1) - dt.date(date.year, m, 1)).days
    frac = (dim - date.day) / dim
    tot = getattr(row, f"{pre}_{m:02d}") * frac
    for k in range(m + 1, 13):
        tot += getattr(row, f"{pre}_{k:02d}")
    return tot


def fit(X, y, lam=1.0):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1]); P = lam * np.eye(X.shape[1]); P[0, 0] = 0
    for _ in range(80):
        p = 1 / (1 + np.exp(-X @ b))
        W = np.clip(p * (1 - p), 1e-9, None)
        try:
            step = np.linalg.solve(X.T @ (X * W[:, None]) + P, X.T @ (y - p) - P @ b)
        except np.linalg.LinAlgError:
            return np.nan
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    return b[1]


def design(d):
    cp = np.sqrt(d["clear_post"].values)
    s1 = d["s1_post"].values
    roi = (d["roi"] == "CG2").values.astype(float)[:, None]
    mo = pd.get_dummies(d["event_month"].astype(int), drop_first=True).values.astype(float)
    return np.column_stack([cp, s1, roi, mo])


def stat(d):
    lo = d[d.clear_post <= 2]["registered"].mean()
    hi = d[d.clear_post >= 5]["registered"].mean()
    return (hi - lo) * 100


def boot(args):
    d, seed, what = args
    rng = np.random.default_rng(seed)
    ub = d["block"].unique()
    idx = {b: np.where(d["block"].values == b)[0] for b in ub}
    pick = rng.choice(ub, size=len(ub), replace=True)
    dd = d.iloc[np.concatenate([idx[b] for b in pick])]
    if what == "gap":
        return stat(dd)
    return fit(design(dd), dd["registered"].values.astype(float))


def ci(d, what, pool):
    seeds = rng_master.integers(0, 2**31, NBOOT)
    v = np.array(pool.map(boot, [(d, s, what) for s in seeds]))
    v = v[np.isfinite(v)]
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main(redated_csv, out_json):
    r = pd.read_csv(redated_csv)
    p4 = pd.read_csv("aef_explore/stage5/TB01/P4/P4_table.csv")
    # match regenerated patches to the P4 event set by centroid (same deterministic recipe)
    keep = []
    for roi in ("CG1", "CG2"):
        a = r[r.roi == roi].reset_index(drop=True)
        b = p4[p4.roi == roi].reset_index(drop=True)
        d2 = ((a.lon.values[:, None] - b.lon.values[None, :]) ** 2 +
              (a.lat.values[:, None] - b.lat.values[None, :]) ** 2)
        j = d2.argmin(axis=1)
        dist = np.sqrt(d2[np.arange(len(a)), j])
        m = a.copy()
        m["p4_event_id"] = b.event_id.values[j]
        m["match_dist_deg"] = dist
        m["registered"] = b.registered.values[j]
        m["ang"] = b.ang_2020_2021_deg.values[j]
        m["radd_old"] = b.radd_any.values[j]
        m["clear_post_old"] = b.clear_post.values[j]
        keep.append(m)
    m = pd.concat(keep)
    m = m[m.match_dist_deg < 0.002]           # ~200 m
    m = m.drop_duplicates("p4_event_id", keep="first")
    out = {"patches_regenerated": int(len(r)), "matched_to_P4": int(len(m)),
           "P4_events": int(len(p4)),
           "coverage_2021_vintage": float((m.first_2021 > 0).mean()),
           "coverage_2024_vintage": float(m.radd_old.notna().mean())}

    m = m[(m.first_2021 > 0) & m.radd_old.notna()].copy()
    m["date_new"] = [EPOCH + dt.timedelta(days=int(x)) for x in m.first_2021]
    m["date_old"] = [dt.date.fromisoformat(x) for x in m.radd_old]
    m["shift_days"] = [(a - b).days for a, b in zip(m.date_new, m.date_old)]
    out["n_both_dated"] = int(len(m))
    out["shift_gt30_share"] = float((m.shift_days.abs() > 30).mean())
    out["shift_gt90_share"] = float((m.shift_days.abs() > 90).mean())
    out["shift_pct"] = [float(x) for x in np.percentile(m.shift_days, [5, 25, 50, 75, 95])]
    out["shift_median_abs"] = float(np.median(np.abs(m.shift_days)))
    out["earlier_share"] = float((m.shift_days < 0).mean())

    m["clear_post"] = [prorate(row, row.date_new, "s2") for row in m.itertuples()]
    m["s1_post"] = [prorate(row, row.date_new, "s1") for row in m.itertuples()]
    m["event_month"] = [d.month for d in m.date_new]
    m["block"] = (np.floor(m.lon / 0.5).astype(int).astype(str) + "_" +
                  np.floor(m.lat / 0.5).astype(int).astype(str))
    m = m[m.clear_post.notna() & m.s1_post.notna()]

    bins = [(-.1, 0), (0, 2), (2, 4), (4, 6), (6, 9), (9, 14), (14, 1e9)]
    out["curve"] = [{"bin": f"({a},{b}]", "n": int(((m.clear_post > a) & (m.clear_post <= b)).sum()),
                     "reg": float(m[(m.clear_post > a) & (m.clear_post <= b)]["registered"].mean())}
                    for a, b in bins]
    out["n"] = int(len(m))
    out["n_lo"] = int((m.clear_post <= 2).sum())
    out["p_lo"] = float(m[m.clear_post <= 2]["registered"].mean())
    out["p_hi"] = float(m[m.clear_post >= 5]["registered"].mean())
    out["gap_pp"] = float(stat(m))
    with Pool(24) as pool:
        out["gap_ci"] = ci(m, "gap", pool)
        out["h7a_coef"] = float(fit(design(m), m["registered"].values.astype(float)))
        out["h7a_ci"] = ci(m, "coef", pool)

    lo, hi = out["gap_ci"]
    if hi >= BR21_CI[0]:
        verdict = "replicated"
    elif lo > 0:
        verdict = "attenuated but consistent"
    else:
        verdict = "not replicated"
    out["verdict"] = verdict
    out["brazil2021_ci"] = list(BR21_CI)
    json.dump(out, open(out_json, "w"), indent=1)
    m.to_csv("aef_explore/stage5/TB01/P5b/P4b_events_redated.csv", index=False,
             columns=["p4_event_id", "roi", "lon", "lat", "area_ha", "date_old", "date_new",
                      "shift_days", "clear_post_old", "clear_post", "s1_post", "event_month",
                      "ang", "registered", "block"])
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
