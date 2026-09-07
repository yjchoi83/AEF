"""P7 item 6 -- what makes the optically late events different.

Section 4.4 left open why clearings the reference map records only in the following year
register far less often, having shown that observation scarcity explains little of it. This
script settles it.

(a) A definition check. `date_upper = min(RADD first alert, DETER view_date)` cannot bind for
    an optically late event, because its DETER date lies in the following year. Their
    `clear_post` is therefore identical under both dating rules, and the script asserts it.
(b) The comparison: polygon area, change intensity in units of the state threshold, RADD
    confidence and post-event clear observations, then a logistic model asking whether the
    registration deficit survives conditioning on observation supply, and a linear model on
    log intensity asking what the surviving deficit consists of.

All intervals are the same 0.5 deg block bootstrap used everywhere else.
"""
import json
import numpy as np
import pandas as pd
from multiprocessing import Pool
import p2_model as M

P2 = "aef_explore/stage5/TB01/P2/P2_events.csv"
P2B = "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv"
S1 = "aef_explore/paper/code/s1_post_2020_derived.csv"
NBOOT, NPROC = 1000, 32
SEED = 20260908
_S = {}


def prep(path, angcol, extra=None):
    d, cp, s1 = M.prepare(path, "date_upper", extra)
    d = d.copy()
    d["r"] = d[angcol] / d["tau_p90"]
    d["lr"] = np.log(d["r"].clip(lower=1e-3))
    d["late"] = d["radd_only"].astype(float)
    d["high_conf"] = d["radd_high"].notna().astype(float)
    d["cp"] = d[cp].astype(float)
    return d.reset_index(drop=True)


def design(d, with_supply):
    """late + [sqrt(clear_post), s1_post] + state + month + log area."""
    cols = [d["late"].values]
    if with_supply:
        cols += [np.sqrt(d["cp"].values), d["s1_post_date_upper"].values
                 if "s1_post_date_upper" in d else d["s1_post_radd_any"].values]
    cols += [pd.get_dummies(d["state"], drop_first=True).values.astype(float),
             pd.get_dummies(d["event_month"].astype(int), drop_first=True).values.astype(float),
             np.log(d["area_ha"].values)[:, None]]
    return np.column_stack(cols)


def ame(X, y, lam=1.0):
    """Average marginal effect of the first column (a 0/1 indicator), in percentage points."""
    Xd = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(Xd.shape[1])
    P = lam * np.eye(Xd.shape[1]); P[0, 0] = 0
    for _ in range(80):
        p = 1 / (1 + np.exp(-Xd @ b))
        W = np.clip(p * (1 - p), 1e-9, None)
        try:
            step = np.linalg.solve(Xd.T @ (Xd * W[:, None]) + P, Xd.T @ (y - p) - P @ b)
        except np.linalg.LinAlgError:
            return np.nan, np.nan
        b = b + step
        if np.abs(step).max() < 1e-9:
            break
    X1 = Xd.copy(); X1[:, 1] = 1.0
    X0 = Xd.copy(); X0[:, 1] = 0.0
    p1 = 1 / (1 + np.exp(-X1 @ b))
    p0 = 1 / (1 + np.exp(-X0 @ b))
    return float(b[1]), float(100 * (p0 - p1).mean())        # deficit, in points


def ols_gap(X, y):
    """Coefficient on the first column of a least-squares fit (log intensity model)."""
    Xd = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    return float(beta[1])


def _init(payload):
    _S.clear(); _S.update(payload)


def _draw(seed):
    rng = np.random.default_rng(seed)
    idx = _S["index"]
    pick = rng.choice(len(idx), size=len(idx), replace=True)
    sel = np.concatenate([idx[k] for k in pick])
    y, ylr = _S["y"][sel], _S["ylr"][sel]
    out = []
    for key in ("Xraw", "Xadj"):
        out.append(ame(_S[key][sel], y)[1])
    out.append(ols_gap(_S["Xadj"][sel], ylr))
    return out


def boot(d):
    y = d["registered"].values.astype(float)
    ylr = d["lr"].values
    Xraw = design(d, False)[:, :1]
    Xadj = design(d, True)
    blocks = d["block"].values
    _, inv = np.unique(blocks, return_inverse=True)
    index = [np.where(inv == k)[0] for k in range(inv.max() + 1)]
    point = [ame(Xraw, y)[1], ame(Xadj, y)[1], ols_gap(Xadj, ylr)]
    rng = np.random.default_rng(SEED)
    seeds = list(rng.integers(0, 2 ** 31, NBOOT))
    with Pool(NPROC, initializer=_init,
              initargs=(dict(Xraw=Xraw, Xadj=Xadj, y=y, ylr=ylr, index=index),)) as pool:
        draws = np.array(pool.map(_draw, seeds, chunksize=8))
    lo, hi = np.nanpercentile(draws, [2.5, 97.5], axis=0)
    names = ["deficit_raw_pp", "deficit_adjusted_pp", "log_intensity_gap"]
    return {n: dict(point=float(p), lo=float(a), hi=float(b))
            for n, p, a, b in zip(names, point, lo, hi)}


def main():
    out = {}
    for year, path, angcol, extra in (("2021", P2, "ang_mean_deg", None),
                                      ("2020", P2B, "ang_2019_2020_deg", pd.read_csv(S1))):
        d = prep(path, angcol, extra)
        late, mapd = d[d.late == 1], d[d.late == 0]
        # (a) the definition check
        raw = pd.read_csv(path)
        raw = raw[raw.radd_any.notna() & (raw.radd_only == 1)]
        same = float(np.isclose(raw["clear_post_date_upper"],
                                raw["clear_post_radd_any"]).mean())
        pct = lambda s: [round(float(x), 3) for x in np.nanpercentile(s.dropna(), [25, 50, 75])]
        b = boot(d)
        out[year] = dict(
            definition_check=dict(
                share_clear_post_identical_under_both_rules=same,
                view_date_year=sorted(pd.to_datetime(raw["view_date"]).dt.year.unique().tolist()),
                median_cp_late=float(late.cp.median()), median_cp_mapped=float(mapd.cp.median())),
            n_late=int(len(late)), n_mapped=int(len(mapd)),
            reg_late=float(late.registered.mean()), reg_mapped=float(mapd.registered.mean()),
            area_q=dict(late=pct(late.area_ha), mapped=pct(mapd.area_ha)),
            intensity_q=dict(late=pct(late.r), mapped=pct(mapd.r)),
            cp_q=dict(late=pct(late.cp), mapped=pct(mapd.cp)),
            high_conf=dict(late=float(late.high_conf.mean()),
                           mapped=float(mapd.high_conf.mean())),
            share_low_bin=dict(late=float((late.cp <= 2).mean()),
                               mapped=float((mapd.cp <= 2).mean())),
            **b,
            intensity_ratio=float(np.exp(b["log_intensity_gap"]["point"])),
            intensity_ratio_ci=[float(np.exp(b["log_intensity_gap"]["lo"])),
                                float(np.exp(b["log_intensity_gap"]["hi"]))],
            share_of_deficit_left_by_supply=float(
                b["deficit_adjusted_pp"]["point"] / b["deficit_raw_pp"]["point"]))
        print(year, "raw %.1f pp, adjusted %.1f pp [%.1f, %.1f], intensity ratio %.2f" % (
            b["deficit_raw_pp"]["point"], b["deficit_adjusted_pp"]["point"],
            b["deficit_adjusted_pp"]["lo"], b["deficit_adjusted_pp"]["hi"],
            out[year]["intensity_ratio"]), flush=True)
    json.dump(out, open("aef_explore/paper/intensity_stats.json", "w"), indent=1)


if __name__ == "__main__":
    main()
