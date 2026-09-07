"""P5b item 3 — H7(a) sensitivity table: the joint `clear_post` coefficient and its
0.5 deg block-bootstrap CI under every P2 robustness variant.

The P2 fitting script was not retained, so the model is rebuilt from the spec recorded in
P2/PLAN.md step 5 (`registered ~ f(clear_post) + f(s1_post) + state + month + radd_only`,
logistic, L2) and calibrated against the two coefficients P2 reports: solo 0.211 and joint
0.219 on the main variant. f = sqrt on clear_post, identity on s1_post, lambda = 1
reproduces those to 0.213 / 0.217.
"""
import numpy as np, pandas as pd, sys
from multiprocessing import Pool

CSV = "aef_explore/stage5/TB01/P2/P2_events.csv"
NBOOT = 1000
LAM = 1.0
rng_master = np.random.default_rng(20260907)


def fit(X, y, lam=LAM):
    X = np.column_stack([np.ones(len(y)), X])
    b = np.zeros(X.shape[1])
    P = lam * np.eye(X.shape[1]); P[0, 0] = 0
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


def design(d, cp_col, s1_col, reg_col):
    ok = d[cp_col].notna() & d[s1_col].notna() & d["event_month"].notna()
    d = d[ok]
    cp = np.sqrt(d[cp_col].values.astype(float))
    s1 = d[s1_col].values.astype(float)
    st = pd.get_dummies(d["state"], drop_first=True).values.astype(float)
    mo = pd.get_dummies(d["event_month"].astype(int), drop_first=True).values.astype(float)
    ro = d["radd_only"].values.astype(float)[:, None]
    X = np.column_stack([cp, s1, st, mo, ro])
    return X, d[reg_col].values.astype(float), d["block"].values


def boot_one(args):
    X, y, blocks, seed = args
    rng = np.random.default_rng(seed)
    ub = np.unique(blocks)
    idx_by_block = {b: np.where(blocks == b)[0] for b in ub}
    pick = rng.choice(ub, size=len(ub), replace=True)
    idx = np.concatenate([idx_by_block[b] for b in pick])
    return fit(X[idx], y[idx])


def run(name, X, y, blocks, pool):
    point = fit(X, y)
    seeds = rng_master.integers(0, 2**31, NBOOT)
    draws = np.array(pool.map(boot_one, [(X, y, blocks, s) for s in seeds]))
    draws = draws[np.isfinite(draws)]
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return dict(variant=name, n=len(y), coef=point, ci_lo=lo, ci_hi=hi,
                crosses_zero=bool(lo <= 0 <= hi), nboot_ok=len(draws))


def main():
    d = pd.read_csv(CSV)
    ANY, S1, S1U = "clear_post_radd_any", "s1_post_radd_any", "s1_post_date_upper"
    variants = [
        ("main (tau p90)", d, ANY, S1, "registered"),
        ("tau p85", d, ANY, S1, "reg_p85"),
        ("tau p95", d, ANY, S1, "reg_p95"),
        ("radd_high only", d[d["radd_high"].notna()], "clear_post_radd_high", S1, "registered"),
        ("date_upper", d, "clear_post_date_upper", S1U, "registered"),
        ("no radd_only", d[d["radd_only"] == 0], ANY, S1, "registered"),
        ("size < 5 ha", d[d["area_ha"] < 5], ANY, S1, "registered"),
        ("size 5-25 ha", d[(d["area_ha"] >= 5) & (d["area_ha"] < 25)], ANY, S1, "registered"),
        ("size >= 25 ha", d[d["area_ha"] >= 25], ANY, S1, "registered"),
    ]
    rows = []
    with Pool(24) as pool:
        for name, dd, cp, s1, reg in variants:
            X, y, blocks = design(dd.copy(), cp, s1, reg)
            r = run(name, X, y, blocks, pool)
            rows.append(r)
            print(f"{name:18s} n={r['n']:6d} coef={r['coef']:+.3f} "
                  f"[{r['ci_lo']:+.3f}, {r['ci_hi']:+.3f}] cross0={r['crosses_zero']}", flush=True)
    out = pd.DataFrame(rows)
    out.to_csv("aef_explore/stage5/TB01/P5b/h7a_sensitivity.csv", index=False)
    print("crossing zero:", out[out.crosses_zero]["variant"].tolist())


if __name__ == "__main__":
    main()
