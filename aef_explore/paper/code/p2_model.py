"""Reconstructed TB01 event-level model (P2 step 5), used for every number in the manuscript.

The original P2/P2b fitting script was not retained. This module rebuilds it from the
specification recorded in `aef_explore/stage5/TB01/P2/PLAN.md` step 5 --

    registered ~ f(clear_post) + f(s1_post) + state + month + radd_only,
    logistic with L2, all CIs from a 0.5 deg block bootstrap with 1,000 draws

-- and pins the free choices (f, the penalty) by reproducing the two coefficients P2 reports:
solo 0.211 and joint 0.219 on the 2021 main variant.  f = sqrt on clear_post, identity on
s1_post and lambda = 1 give 0.213 and 0.217.  Every other quantity below (bins, gaps, strata,
robustness rows) then follows from the same table and the same bootstrap, and
`paper/NUMBERS_TRACE.md` records where each re-derived value differs from the package
documents.

Dating rules
------------
`radd_any`   first RADD alert inside the polygon (P2/P2b primary)
`date_upper` min(RADD first alert, DETER view_date)  -- the manuscript's primary rule, adopted
             after the P5b zero-bin diagnosis showed the RADD-only date is systematically late
`radd_high`  first high-confidence RADD alert
"""
import json
import numpy as np
import pandas as pd
from multiprocessing import Pool

NBOOT = 1000
LAM = 1.0
BINS = [(-0.1, 0), (0, 2), (2, 4), (4, 6), (6, 9), (9, 14), (14, 1e9)]
BIN_LABELS = ["0", "0-2", "2-4", "4-6", "6-9", "9-14", "14+"]
SEED = 20260908


# ---------------------------------------------------------------- model

def logistic_fit(X, y, lam=LAM, coef_index=1):
    """L2-penalised logistic regression by Newton-Raphson; returns one coefficient."""
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1])
    P = lam * np.eye(X.shape[1])
    P[0, 0] = 0.0
    for _ in range(80):
        p = 1.0 / (1.0 + np.exp(-X @ b))
        W = np.clip(p * (1.0 - p), 1e-9, None)
        try:
            step = np.linalg.solve(X.T @ (X * W[:, None]) + P, X.T @ (y - p) - P @ b)
        except np.linalg.LinAlgError:
            return np.nan
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    return b[coef_index]


def design(d, cp, s1, with_s1=True):
    """sqrt(clear_post) [+ s1_post] + state + month + radd_only."""
    cols = [np.sqrt(d[cp].values.astype(float))]
    if with_s1:
        cols.append(d[s1].values.astype(float))
    cols.append(pd.get_dummies(d["state"], drop_first=True).values.astype(float))
    cols.append(pd.get_dummies(d["event_month"].astype(int), drop_first=True).values.astype(float))
    cols.append(d["radd_only"].values.astype(float)[:, None])
    return np.column_stack(cols)


# ---------------------------------------------------------------- statistics

def gap_pp(d, cp, reg):
    lo = d.loc[d[cp] <= 2, reg].mean()
    hi = d.loc[d[cp] >= 5, reg].mean()
    return (hi - lo) * 100.0


def curve(d, cp, reg):
    out = []
    for (a, b), lab in zip(BINS, BIN_LABELS):
        s = d[(d[cp] > a) & (d[cp] <= b)]
        out.append(dict(bin=lab, n=int(len(s)),
                        reg=float(s[reg].mean()) if len(s) else None))
    return out


def month_relative_s1(d, cp, s1):
    """s1_post expressed against the median of the event's own calendar month."""
    med = d.groupby(d["event_month"].astype(int))[s1].transform("median")
    return d[s1].values >= med.values


# The bootstrap resamples a table of tens of thousands of rows a thousand times.  Passing the
# frame through the pool for every draw dominates the runtime, so the frame is handed to each
# worker once, through the pool initialiser, and the tasks carry only a seed.
_SHARED = {}


def _init(payload):
    _SHARED.clear()
    _SHARED.update(payload)


def _draw_coef(seed):
    """Bootstrap draw for a logistic coefficient, on a design matrix built once."""
    X, y, blocks, lam = _SHARED["X"], _SHARED["y"], _SHARED["blocks"], _SHARED["lam"]
    rng = np.random.default_rng(seed)
    ub = _SHARED["ublocks"]
    idx = _SHARED["index"]
    pick = rng.choice(len(ub), size=len(ub), replace=True)
    sel = np.concatenate([idx[k] for k in pick])
    return logistic_fit(X[sel], y[sel], lam, coef_index=1)


def _draw(seed):
    return _stat((_SHARED["d"], _SHARED["kind"], _SHARED["cp"], _SHARED["s1"],
                  _SHARED["reg"], seed))


def _stat(args):
    d, kind, cp, s1, reg, seed = args
    if seed is not None:
        rng = np.random.default_rng(seed)
        blocks = d["block"].values
        ub = np.unique(blocks)
        idx = {b: np.where(blocks == b)[0] for b in ub}
        pick = rng.choice(ub, size=len(ub), replace=True)
        d = d.iloc[np.concatenate([idx[b] for b in pick])]
    if kind == "gap":
        return gap_pp(d, cp, reg)
    if kind == "p_lo":
        return d.loc[d[cp] <= 2, reg].mean()
    if kind == "p_hi":
        return d.loc[d[cp] >= 5, reg].mean()
    if kind == "coef_joint":
        return logistic_fit(design(d, cp, s1, True), d[reg].values.astype(float))
    if kind == "coef_solo":
        return logistic_fit(design(d, cp, s1, False), d[reg].values.astype(float))
    if kind == "h7b_hi":
        m = month_relative_s1(d, cp, s1)
        s = d[(d[cp] <= 2) & m]
        return s[reg].mean() if len(s) else np.nan
    if kind == "h7b_lo":
        m = month_relative_s1(d, cp, s1)
        s = d[(d[cp] <= 2) & ~m]
        return s[reg].mean() if len(s) else np.nan
    if kind == "share":
        return d[reg].mean()
    raise ValueError(kind)


def boot_coef_ci(nproc, d, cp, s1, reg, with_s1=True, nboot=NBOOT, seed=SEED, lam=LAM):
    """CI for the clear_post coefficient, with the design matrix built once and shared."""
    d = d.reset_index(drop=True)
    X = design(d, cp, s1, with_s1)
    y = d[reg].values.astype(float)
    blocks = d["block"].values
    ub, inv = np.unique(blocks, return_inverse=True)
    index = [np.where(inv == k)[0] for k in range(len(ub))]
    point = logistic_fit(X, y, lam, coef_index=1)
    rng = np.random.default_rng(seed)
    seeds = list(rng.integers(0, 2 ** 31, nboot))
    payload = dict(X=X, y=y, blocks=blocks, ublocks=ub, index=index, lam=lam)
    with Pool(nproc, initializer=_init, initargs=(payload,)) as pool:
        draws = np.array(pool.map(_draw_coef, seeds, chunksize=max(1, nboot // (nproc * 4))))
    draws = draws[np.isfinite(draws)]
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return dict(point=float(point), lo=float(lo), hi=float(hi), nboot=int(len(draws)))


def boot_ci(nproc, d, kind, cp, s1, reg, nboot=NBOOT, seed=SEED):
    if kind == "coef_joint":
        return boot_coef_ci(nproc, d, cp, s1, reg, True, nboot, seed)
    if kind == "coef_solo":
        return boot_coef_ci(nproc, d, cp, s1, reg, False, nboot, seed)
    point = _stat((d, kind, cp, s1, reg, None))
    rng = np.random.default_rng(seed)
    seeds = list(rng.integers(0, 2 ** 31, nboot))
    payload = dict(d=d.reset_index(drop=True), kind=kind, cp=cp, s1=s1, reg=reg)
    with Pool(nproc, initializer=_init, initargs=(payload,)) as pool:
        draws = np.array(pool.map(_draw, seeds, chunksize=max(1, nboot // (nproc * 4))))
    draws = draws[np.isfinite(draws)]
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return dict(point=float(point), lo=float(lo), hi=float(hi), nboot=int(len(draws)))


# ---------------------------------------------------------------- drivers

def prepare(path, dating, s1_extra=None):
    """Load an event table under one dating rule; returns (frame, clear_post, s1_post)."""
    d = pd.read_csv(path)
    cp = {"radd_any": "clear_post_radd_any", "date_upper": "clear_post_date_upper",
          "radd_high": "clear_post_radd_high"}[dating]
    s1 = {"radd_any": "s1_post_radd_any", "date_upper": "s1_post_date_upper",
          "radd_high": "s1_post_radd_any"}[dating]
    if s1_extra is not None and s1 not in d.columns:
        d = d.merge(s1_extra, on="event_id", how="left")
    d = d[d[cp].notna() & d[s1].notna()].copy()
    date_col = {"radd_any": "radd_any", "date_upper": "date_upper",
                "radd_high": "radd_high"}[dating]
    d["event_month"] = pd.to_datetime(d[date_col]).dt.month
    d = d[d["event_month"].notna()]
    return d, cp, s1


def analyse(pool, d, cp, s1, reg="registered", tag=""):
    # `pool` is the process count, not a Pool object (see boot_ci)
    n_lo = int((d[cp] <= 2).sum())
    res = dict(tag=tag, n=int(len(d)), n_lo=n_lo,
               curve=curve(d, cp, reg),
               p_lo=boot_ci(pool, d, "p_lo", cp, s1, reg),
               p_hi=boot_ci(pool, d, "p_hi", cp, s1, reg),
               gap=boot_ci(pool, d, "gap", cp, s1, reg),
               coef_joint=boot_ci(pool, d, "coef_joint", cp, s1, reg),
               coef_solo=dict(point=float(_stat((d, "coef_solo", cp, s1, reg, None)))),
               overall_reg=float(d[reg].mean()))
    res["H1"] = bool(res["gap"]["lo"] > 0 and res["gap"]["point"] >= 5 and n_lo >= 100)
    res["H3"] = bool(res["p_hi"]["point"] >= 0.95)
    res["H7a"] = bool(res["coef_joint"]["lo"] > 0)
    # H7(b) as originally written: absolute median split
    med = float(np.median(d[s1]))
    res["h7b_original_stratum_n"] = int(((d[cp] <= 2) & (d[s1] >= med)).sum())
    res["h7b_original_median_s1"] = med
    # H7(b)' as re-pre-registered in P2b: within-month split
    hi = boot_ci(pool, d, "h7b_hi", cp, s1, reg)
    lo = boot_ci(pool, d, "h7b_lo", cp, s1, reg)
    m = month_relative_s1(d, cp, s1)
    res["h7b_prime"] = dict(n_hi=int(((d[cp] <= 2) & m).sum()),
                            n_lo=int(((d[cp] <= 2) & ~m).sum()), hi=hi, lo=lo)
    res["H7b_prime"] = bool(hi["point"] < 0.80 and hi["hi"] < 0.85
                            and hi["point"] < lo["point"])
    # within-month S1 quartiles among low-optical events
    low = d[d[cp] <= 2].copy()
    if len(low) > 20:
        med_by_month = d.groupby(d["event_month"].astype(int))[s1].median()
        rel = low[s1].values / np.maximum(
            med_by_month.reindex(low["event_month"].astype(int)).values, 1e-6)
        q = pd.qcut(pd.Series(rel), 4, labels=False, duplicates="drop")
        res["s1_quartiles"] = [
            dict(q=int(k), n=int((q == k).sum()), reg=float(low[reg].values[(q == k).values].mean()))
            for k in sorted(pd.Series(q).dropna().unique())]
    return res


def robustness(pool, path, dating, s1_extra=None):
    d, cp, s1 = prepare(path, dating, s1_extra)
    rows = []
    alt = "radd_any" if dating == "date_upper" else "date_upper"
    variants = [("main (tau p90)", d, cp, s1, "registered"),
                ("tau p85", d, cp, s1, "reg_p85"),
                ("tau p95", d, cp, s1, "reg_p95")]
    if "clear_post_radd_high" in d.columns:
        dh = d[d["clear_post_radd_high"].notna()]
        variants.append(("radd_high only", dh, "clear_post_radd_high", s1, "registered"))
    da, cpa, s1a = prepare(path, alt, s1_extra)
    variants.append((f"dating: {alt}", da, cpa, s1a, "registered"))
    variants += [("no radd_only", d[d["radd_only"] == 0], cp, s1, "registered"),
                 ("size < 5 ha", d[d["area_ha"] < 5], cp, s1, "registered"),
                 ("size 5-25 ha", d[(d["area_ha"] >= 5) & (d["area_ha"] < 25)], cp, s1, "registered"),
                 ("size >= 25 ha", d[d["area_ha"] >= 25], cp, s1, "registered")]
    for name, dd, c, s, r in variants:
        dd = dd.copy()
        g = boot_ci(pool, dd, "gap", c, s, r)
        cj = boot_ci(pool, dd, "coef_joint", c, s, r)
        rows.append(dict(variant=name, n=int(len(dd)), n_lo=int((dd[c] <= 2).sum()),
                         p_lo=float(dd.loc[dd[c] <= 2, r].mean()),
                         p_hi=float(dd.loc[dd[c] >= 5, r].mean()),
                         gap=g, coef_joint=cj,
                         H1=bool(g["lo"] > 0 and g["point"] >= 5 and (dd[c] <= 2).sum() >= 100),
                         H3=bool(dd.loc[dd[c] >= 5, r].mean() >= 0.95),
                         H7a=bool(cj["lo"] > 0)))
        print(f"  {name:22s} n={rows[-1]['n']:6d} n_lo={rows[-1]['n_lo']:5d} "
              f"gap={g['point']:6.2f} [{g['lo']:6.2f},{g['hi']:6.2f}] "
              f"coef={cj['point']:+.3f} [{cj['lo']:+.3f},{cj['hi']:+.3f}]", flush=True)
    return rows
