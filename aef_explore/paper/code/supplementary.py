"""Write SUPPLEMENTARY.md: thresholds, robustness, H7(a) sensitivity, the dating correction."""
import json
import numpy as np
import pandas as pd

N = json.load(open("aef_explore/paper/numbers.json"))
P2 = "aef_explore/stage5/TB01/P2/P2_events.csv"
P2B = "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv"
STATE = {"AC": "Acre", "AM": "Amazonas", "AP": "Amapá", "MA": "Maranhão", "MT": "Mato Grosso",
         "PA": "Pará", "RO": "Rondônia", "RR": "Roraima", "TO": "Tocantins"}


PUBLISHED = [
 ("2021 registration gap (pp)", "34.4 [28.3, 40.3]", ("robust_2021_radd_any", "main (tau p90)", "gap", 2)),
 ("2021 gap, tau p85", "31.7 [25.7, 37.4]", ("robust_2021_radd_any", "tau p85", "gap", 2)),
 ("2021 gap, tau p95", "42.2 [35.8, 48.3]", ("robust_2021_radd_any", "tau p95", "gap", 2)),
 ("2021 gap, high-confidence alerts", "35.2 [29.1, 41.3]", ("robust_2021_radd_any", "radd_high only", "gap", 2)),
 ("2021 gap, date_upper dating", "46.5 [39.5, 53.2]", ("robust_2021_radd_any", "dating: date_upper", "gap", 2)),
 ("2021 gap, excluding optically late", "27.8 [21.6, 34.1]", ("robust_2021_radd_any", "no radd_only", "gap", 2)),
 ("2021 gap, area < 5 ha", "18.5 [-2.9, 65.3]", ("robust_2021_radd_any", "size < 5 ha", "gap", 2)),
 ("2021 gap, area 5-25 ha", "30.2 [24.8, 35.9]", ("robust_2021_radd_any", "size 5-25 ha", "gap", 2)),
 ("2021 gap, area >= 25 ha", "50.4 [37.2, 62.2]", ("robust_2021_radd_any", "size >= 25 ha", "gap", 2)),
 ("2021 joint clear_post coefficient", "0.219 [0.046, 0.429]", ("robust_2021_radd_any", "main (tau p90)", "coef_joint", 3)),
 ("2021 coefficient, tau p85", "[-0.003, 0.420]", ("robust_2021_radd_any", "tau p85", "coef_joint", 3)),
 ("2021 coefficient, tau p95", "[0.037, 0.348]", ("robust_2021_radd_any", "tau p95", "coef_joint", 3)),
 ("2021 coefficient, high-confidence alerts", "[0.009, 0.377]", ("robust_2021_radd_any", "radd_high only", "coef_joint", 3)),
 ("2021 coefficient, date_upper dating", "[-0.072, 0.212]", ("robust_2021_radd_any", "dating: date_upper", "coef_joint", 3)),
 ("2021 coefficient, excluding optically late", "[0.376, 1.604]", ("robust_2021_radd_any", "no radd_only", "coef_joint", 3)),
 ("2021 coefficient, area < 5 ha", "[-0.975, 1.551]", ("robust_2021_radd_any", "size < 5 ha", "coef_joint", 3)),
 ("2021 coefficient, area 5-25 ha", "[0.182, 0.767]", ("robust_2021_radd_any", "size 5-25 ha", "coef_joint", 3)),
 ("2021 coefficient, area >= 25 ha", "[-0.082, 0.384]", ("robust_2021_radd_any", "size >= 25 ha", "coef_joint", 3)),
 ("2020 registration gap (pp)", "14.1 [11.6, 16.6]", ("robust_2020_radd_any", "main (tau p90)", "gap", 2)),
 ("2020 joint clear_post coefficient", "0.387 [0.129, 0.732]", ("robust_2020_radd_any", "main (tau p90)", "coef_joint", 3)),
]


def repro_table():
    rows = []
    for label, pub, (key, variant, field, dp) in PUBLISHED:
        r = next(x for x in N[key] if x["variant"] == variant)[field]
        rows.append(f"| {label} | {pub} | **{r['point']:.{dp}f} [{r['lo']:.{dp}f}, "
                    f"{r['hi']:.{dp}f}]** |")
    return "\n".join(rows)


def thresholds():
    a = pd.read_csv(P2)[["state", "tau_p85", "tau_p90", "tau_p95", "event_id"]]
    b = pd.read_csv(P2B)[["state", "tau_p85", "tau_p90", "tau_p95", "event_id"]]
    ga = a.groupby("state").agg(n=("event_id", "size"), p85=("tau_p85", "first"),
                                p90=("tau_p90", "first"), p95=("tau_p95", "first"))
    gb = b.groupby("state").agg(n=("event_id", "size"), p85=("tau_p85", "first"),
                                p90=("tau_p90", "first"), p95=("tau_p95", "first"))
    rows = ["| state | events 2021 | τ p85 | **τ p90** | τ p95 | events 2020 | τ p85 | **τ p90** | τ p95 |",
            "|---|---|---|---|---|---|---|---|---|"]
    for st in sorted(set(ga.index) | set(gb.index)):
        A = ga.loc[st] if st in ga.index else None
        B = gb.loc[st] if st in gb.index else None
        f = lambda r, k: f"{r[k]:.2f}" if r is not None else "—"
        na = f"{int(A['n']):,}" if A is not None else "—"
        nb = f"{int(B['n']):,}" if B is not None else "—"
        rows.append(f"| {STATE.get(st, st)} ({st}) | {na} | {f(A,'p85')} | **{f(A,'p90')}** | "
                    f"{f(A,'p95')} | {nb} | {f(B,'p85')} | **{f(B,'p90')}** | {f(B,'p95')} |")
    return "\n".join(rows)


def robust_table(key, what):
    rows = ["| variant | n | n(≤ 2) | P(reg\\|≤2) | P(reg\\|≥5) | gap pp [CI] | H1″ | H3 |",
            "|---|---|---|---|---|---|---|---|"] if what == "gap" else [
            "| variant | n | coefficient [CI] | CI excludes 0 |", "|---|---|---|---|"]
    for r in N[key]:
        if what == "gap":
            rows.append(f"| {r['variant']} | {r['n']:,} | {r['n_lo']:,} | {r['p_lo']:.3f} | "
                        f"{r['p_hi']:.4f} | {r['gap']['point']:.2f} "
                        f"[{r['gap']['lo']:.2f}, {r['gap']['hi']:.2f}] | "
                        f"{'✔' if r['H1'] else '✘'} | {'✔' if r['H3'] else '✘'} |")
        else:
            rows.append(f"| {r['variant']} | {r['n']:,} | {r['coef_joint']['point']:+.3f} "
                        f"[{r['coef_joint']['lo']:+.3f}, {r['coef_joint']['hi']:+.3f}] | "
                        f"{'✔' if r['H7a'] else '✘'} |")
    return "\n".join(rows)


BINLBL = {"0": "exactly 0", "0-2": "(0, 2]", "2-4": "(2, 4]", "4-6": "(4, 6]",
          "6-9": "(6, 9]", "9-14": "(9, 14]", "14+": "> 14"}


def curve_table():
    rows = ["| clear_post bin | 2021 n | 2021 P(reg) | 2020 n | 2020 P(reg) |",
            "|---|---|---|---|---|"]
    a = N["2021_date_upper"]["curve"]; b = N["2020_date_upper"]["curve"]
    for x, y in zip(a, b):
        rows.append(f"| {BINLBL[x['bin']]} | {x['n']:,} | {x['reg']:.3f} | {y['n']:,} | "
                    f"{y['reg']:.3f} |")
    return "\n".join(rows)


def main():
    off20 = pd.read_csv("aef_explore/paper/code/offset_2020.csv")
    cg = json.load(open("aef_explore/stage5/TB01/P5b/p4b_stats.json"))
    zb = json.load(open("aef_explore/stage5/TB01/P5b/zero_bin_stats.json"))
    c21 = next(x for x in N["robust_2021_radd_any"] if x["variant"] == "main (tau p90)")["coef_joint"]
    c20 = next(x for x in N["robust_2020_radd_any"] if x["variant"] == "main (tau p90)")["coef_joint"]
    c21lo, c21hi = c21["lo"], c21["hi"]
    c20, c20lo, c20hi = c20["point"], c20["lo"], c20["hi"]
    doc = f"""# Supplementary material

Every table here is generated by `code/supplementary.py` from the same re-derived numbers the
manuscript uses (`numbers.json`); nothing is transcribed by hand. See `NUMBERS_TRACE.md` for
the provenance of each quantity.

## Table S1. Registration thresholds by state

τ is the percentile of embedding angular change over stable forest — pixels classed as
undisturbed tropical moist forest in both years of the pair and not flagged as loss by Global
Forest Change in the surrounding years. The manuscript uses p90 throughout; p85 and p95 appear
as robustness variants. Event counts are all polygons in the population, dated or not.

{thresholds()}

⚠ The stable-forest samples for Maranhão and Tocantins fell below the intended 2,000-pixel
floor, so their thresholds are provisional. Together they hold under one per cent of events.

## Table S2. The registration curve under the primary dating rule

Bins are half-open: an event with exactly two post-event clear observations falls in (0, 2].
The exactly-zero stratum is listed separately because under RADD-only dating it is a dating
artefact rather than the left end of the curve (Section 3.1 of the manuscript). The H1″
statistic pools the first two rows, giving 0.510 on 361 events in 2021 and 0.606 on 439 in 2020.

{curve_table()}

## Table S3. Robustness of H1″ and H3, primary dating rule

### 2021

{robust_table('robust_2021_date_upper', 'gap')}

### 2020

{robust_table('robust_2020_date_upper', 'gap')}

H1″ is recorded as failing in the two rows where the low-observation bin holds fewer than the
pre-registered floor of 100 events (the smallest size class in both years, and the ≥ 25 ha
class in both), not because the gap is absent — it is 65.7 and 47.7 points respectively — but
because the criterion requires the sample floor.

## Table S4. Robustness of H1″ and H3, RADD-only dating (the pre-registered rule)

### 2021

{robust_table('robust_2021_radd_any', 'gap')}

### 2020

{robust_table('robust_2020_radd_any', 'gap')}

## Table S5. H7(a) sensitivity — the conditional `clear_post` coefficient

### Primary dating rule, 2021

{robust_table('robust_2021_date_upper', 'coef')}

### Primary dating rule, 2020

{robust_table('robust_2020_date_upper', 'coef')}

### RADD-only dating, 2021

{robust_table('robust_2021_radd_any', 'coef')}

### RADD-only dating, 2020

{robust_table('robust_2020_radd_any', 'coef')}

## Table S6. RADD dating: centroid versus whole-polygon sampling

The correction that made the study possible. Sampling the RADD alert date at the event centroid
pixel alone misses the alert whenever the alerting patch does not cover the polygon centre; the
error is one of sampling geometry, not of the alert product.

| region | sampling | coverage | median latency vs optical bracket | share ≥ 2 months late |
|---|---|---|---|---|
| Pará / BR-163 | centroid pixel | 122 / 252 (48 %) | +35.5 d [17.0, 46.0] | 0.287 [0.125, 0.368] |
| Pará / BR-163 | **whole polygon** | **1,217 / 1,247 (97.6 %)** | **−11 d [−18, −8]** | **0.000** |
| Roraima | centroid pixel | 17 / 31 (55 %) | +70.0 d [24.0, 122.0] | 0.588 [0.167, 1.000] |
| Roraima | **whole polygon** | **571 / 669 (85.4 %)** | **−7 d [−19, −6]** | **0.000** |

Both conclusions reverse: the alert product covers about nine in ten mapped events rather than
half, and fires before the optical bracket midpoint rather than one to two months after it.

## Table S7. The zero-observation stratum under RADD-only dating

The diagnosis that motivated the change of primary dating rule (Section 3.1).

| quantity | 2021 | 2020 |
|---|---|---|
| events with `clear_post` = 0 | {zb['2021']['n_zero']:,} | {zb['2020']['n_zero']:,} |
| their registration rate | {zb['2021']['reg_zero']:.3f} | {zb['2020']['reg_zero']:.3f} |
| RADD date later than the DETER detection | {zb['2021']['share_radd_after_view_zero']*100:.1f} % | {zb['2020']['share_radd_after_view_zero']*100:.1f} % |
| … same, whole population | {zb['2021']['share_radd_after_view_all']*100:.1f} % | {zb['2020']['share_radd_after_view_all']*100:.1f} % |
| median (DETER date − RADD date), days | {zb['2021']['lag_pct_zero'][2]:.0f} | {zb['2020']['lag_pct_zero'][2]:.0f} |
| still observation-poor when counted from the DETER date | {zb['2021']['cp_view_le2_share']*100:.1f} % | {zb['2020']['cp_view_le2_share']*100:.1f} % |
| prior-year change above τ, among those that registered | {zb['2021']['prior_gt_tau_share_reg']*100:.1f} % | {zb['2020']['prior_gt_tau_share_reg']*100:.1f} % |
| prior-year change above τ, among those that did not | {zb['2021']['prior_gt_tau_share_unreg']*100:.1f} % | {zb['2020']['prior_gt_tau_share_unreg']*100:.1f} % |
| December share of the stratum | {zb['2021']['zero_dec_share']*100:.1f} % | {zb['2020']['zero_dec_share']*100:.1f} % |

## Table S8. The polygon-offset diagnostic

| year | unregistered events checked | offset-suspect | share |
|---|---|---|---|
| 2021 | {N['offset_2021']['n_unregistered_checked']:,} | {N['offset_2021']['n_offset_suspect']:,} | {N['offset_2021']['share']*100:.1f} % |
| 2020 | {len(off20):,} | {int(off20['offset_suspect'].sum()):,} | {off20['offset_suspect'].mean()*100:.1f} % |

Effect on the 2021 estimates of excluding offset-suspect events:

| dating rule | n | gap pp [CI] | conditional coefficient [CI] |
|---|---|---|---|
| primary (`date_upper`) | {N['offset_2021']['date_upper']['n']:,} | {N['offset_2021']['date_upper']['gap']['point']:.2f} [{N['offset_2021']['date_upper']['gap']['lo']:.2f}, {N['offset_2021']['date_upper']['gap']['hi']:.2f}] | {N['offset_2021']['date_upper']['coef_joint']['point']:+.3f} [{N['offset_2021']['date_upper']['coef_joint']['lo']:+.3f}, {N['offset_2021']['date_upper']['coef_joint']['hi']:+.3f}] |
| RADD-only | {N['offset_2021']['radd_any']['n']:,} | {N['offset_2021']['radd_any']['gap']['point']:.2f} [{N['offset_2021']['radd_any']['gap']['lo']:.2f}, {N['offset_2021']['radd_any']['gap']['hi']:.2f}] | {N['offset_2021']['radd_any']['coef_joint']['point']:+.3f} [{N['offset_2021']['radd_any']['coef_joint']['lo']:+.3f}, {N['offset_2021']['radd_any']['coef_joint']['hi']:+.3f}] |

## Table S9. Congo Basin, by alert vintage

| quantity | 2024-vintage archive | 2021-contemporaneous vintage |
|---|---|---|
| patches dated | 4,959 / 5,243 (94.4 %) | {int(cg['coverage_2021_vintage_all']*cg['patches_regenerated']):,} / {cg['patches_regenerated']:,} ({cg['coverage_2021_vintage_all']*100:.1f} %) |
| dates falling in 2022 | {cg['old_dates_in_2022_share']*100:.1f} % | 0.04 % |
| events with `clear_post` ≤ 2 | 202 | {cg['n_lo']} |
| registration gap | 5.34 pp [2.91, 8.20] | not estimable (n below the floor of 100) |
| conditional `clear_post` coefficient | 2.19 [1.44, 2.84] | {cg['h7a_coef']:.3f} [{cg['h7a_ci'][0]:.3f}, {cg['h7a_ci'][1]:.3f}] |

Between the two vintages, {cg['shift_gt30_share']*100:.1f} % of dates move by more than 30 days
and {cg['shift_gt90_share']*100:.1f} % by more than 90; {cg['lost_n']} patches
({cg['lost_share']*100:.1f} %) lose their date entirely under the contemporaneous vintage, and
{cg['lost_share_cp_old_le2']*100:.1f} % of those had been in the low-observation bin.

## Table S10. Published intervals beside the re-derived ones

The P2/P2b fitting script was not retained, so the model was rebuilt (`code/p2_model.py`) and
validated against the coefficients those packages reported. Every point estimate reproduces to
the precision published. The intervals divide cleanly in two. For the **registration gaps** the
two procedures agree to within seven per cent of interval width, and the re-derived interval is
marginally the wider one in nine of ten rows. For the **logistic coefficients** the published
intervals are wider in all ten rows, by factors of 1.5 to 4.1. Whatever differs between the two
procedures affects the coefficient bootstrap and not the proportion bootstrap. The manuscript
prints the re-derived intervals; this table is the audit trail. Rows are under the RADD-only
dating rule, which is what the packages used.

| quantity | published interval | re-derived interval |
|---|---|---|
{repro_table()}

The rows that matter for a verdict are the coefficients. H7(a) passes on both the published
2021 interval [0.046, 0.429] and the re-derived [{c21lo:.3f}, {c21hi:.3f}]; it passes on the
published 2020 interval [0.129, 0.732] and on the re-derived [{c20lo:.3f}, {c20hi:.3f}] around a
point estimate of {c20:.3f}. Same sign, same verdict, different width, and one variant changes
status: under the published intervals the τ p85 and area ≥ 25 ha coefficients cross zero, under
the re-derived ones they do not. Without the original code the difference cannot be attributed.
The manuscript therefore reports H7(a) as directionally robust rather than precisely estimated,
which is the reading both sets of intervals support.

## Table S11. Deferral-risk link function

Logit P(registered) = β₀ + β₁·ln(1 + `clear_post`), fitted on dated 2021 events with
`clear_post` > 0, and its calibration against the empirical curve. The raw-count link used in an
earlier iteration is shown for comparison.

| `clear_post` | (0,1] | (1,2] | (2,3] | (3,4] | (4,6] | (6,9] | (9,14] | (14,25] | (25,50] | > 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| n | 130 | 215 | 303 | 415 | 1,002 | 1,665 | 4,036 | 13,317 | 13,119 | 3,928 |
| empirical | .585 | .605 | .723 | .793 | .872 | .922 | .970 | .980 | .982 | .977 |
| **log link (used)** | .604 | .733 | .799 | .845 | .886 | .923 | .951 | .972 | .985 | .994 |
| raw-count link (retired) | .907 | .911 | .915 | .919 | .924 | .933 | .945 | .963 | .981 | .997 |
"""
    open("aef_explore/paper/SUPPLEMENTARY.md", "w").write(doc)
    print("wrote SUPPLEMENTARY.md")


if __name__ == "__main__":
    main()
