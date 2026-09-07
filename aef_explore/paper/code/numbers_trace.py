"""Write NUMBERS_TRACE.md: every manuscript number, its source, and the re-derivation check."""
import json

N = json.load(open("aef_explore/paper/numbers.json"))
CG = json.load(open("aef_explore/stage5/TB01/P5b/p4b_stats.json"))
ZB = json.load(open("aef_explore/stage5/TB01/P5b/zero_bin_stats.json"))


def g(key, field, sub=None):
    v = N[key][field] if sub is None else N[key][field][sub]
    return v


def ci(v, k=1, pct=False):
    m = 100 if pct else 1
    return f"{v['point']*m:.{k}f} [{v['lo']*m:.{k}f}, {v['hi']*m:.{k}f}]"


# published value, re-derived value, verdict
REPRO = [
 ("P2 §5", "2021 registration at clear_post ≤ 2", "0.631", f"{g('2021_radd_any','p_lo')['point']:.3f}"),
 ("P2 §5", "2021 registration at clear_post ≥ 5", "0.975", f"{g('2021_radd_any','p_hi')['point']:.4f}"),
 ("P2 §5", "2021 gap (pp) [CI]", "34.4 [28.3, 40.3]", ci(g('2021_radd_any','gap'))),
 ("P2 §5", "2021 n(0–2)", "518", str(N['2021_radd_any']['n_lo'])),
 ("P2 §5", "2021 n dated", "38,303", f"{N['2021_radd_any']['n']:,}"),
 ("P2 §5", "2021 clear_post solo coefficient", "0.211", f"{N['2021_radd_any']['coef_solo']['point']:.3f}"),
 ("P2 §5", "2021 clear_post joint coefficient [CI]", "0.219 [0.046, 0.429]",
  ci(g('2021_radd_any','coef_joint'), 3)),
 ("P2 §5", "events with clear_post ≤ 2 and s1_post ≥ overall median", "1",
  str(N['2021_radd_any']['h7b_original_stratum_n'])),
 ("P2b §2", "2020 registration at clear_post ≤ 2", "0.842", f"{g('2020_radd_any','p_lo')['point']:.3f}"),
 ("P2b §2", "2020 registration at clear_post ≥ 5", "0.982", f"{g('2020_radd_any','p_hi')['point']:.4f}"),
 ("P2b §2", "2020 gap (pp) [CI]", "14.1 [11.6, 16.6]", ci(g('2020_radd_any','gap'))),
 ("P2b §2", "2020 n(0–2)", "1,508", f"{N['2020_radd_any']['n_lo']:,}"),
 ("P2b §2", "2020 H7(b)′ SAR-dense stratum", "0.626 [0.548, 0.712]",
  ci(N['2020_radd_any']['h7b_prime']['hi'], 3)),
 ("P2b §2", "2020 H7(b)′ SAR-sparse stratum", "0.883",
  f"{N['2020_radd_any']['h7b_prime']['lo']['point']:.3f}"),
 ("P2b §2", "2020 clear_post joint coefficient [CI]", "0.387 [0.129, 0.732]",
  ci(g('2020_radd_any','coef_joint'), 3)),
 ("P2b §1", "2021 gap excluding offset-suspect events", "28.0 [21.6, 34.0]",
  ci(N['offset_2021']['radd_any']['gap'])),
 ("P2b §1", "2021 offset-suspect share", "45.7 % (608/1,332)",
  f"{N['offset_2021']['share']*100:.1f} % ({N['offset_2021']['n_offset_suspect']:,}/"
  f"{N['offset_2021']['n_unregistered_checked']:,})"),
 ("P3", "2021-unregistered events registering in 2022", "96.5 % [95.3, 97.5]",
  ci(N['h4']['share'], 1, pct=True) + " %"),
]

PRIMARY = [("2021", "2021_date_upper"), ("2020", "2020_date_upper")]


def rows_primary():
    out = []
    for year, key in PRIMARY:
        r = N[key]
        out += [
          (f"{year} events dated", f"{r['n']:,}", f"`numbers.json:{key}.n`"),
          (f"{year} n(clear_post ≤ 2)", f"{r['n_lo']:,}", f"`{key}.n_lo`"),
          (f"{year} P(registered | ≤ 2)", ci(r['p_lo'], 3), f"`{key}.p_lo`"),
          (f"{year} P(registered | ≥ 5)", ci(r['p_hi'], 4), f"`{key}.p_hi`"),
          (f"{year} gap (pp)", ci(r['gap']), f"`{key}.gap`"),
          (f"{year} clear_post coefficient, joint with s1_post", ci(r['coef_joint'], 3),
           f"`{key}.coef_joint`"),
          (f"{year} H7(b)′ SAR-dense stratum", ci(r['h7b_prime']['hi'], 3)
           + f" (n = {r['h7b_prime']['n_hi']})", f"`{key}.h7b_prime.hi`"),
          (f"{year} H7(b)′ SAR-sparse stratum", ci(r['h7b_prime']['lo'], 3)
           + f" (n = {r['h7b_prime']['n_lo']})", f"`{key}.h7b_prime.lo`"),
          (f"{year} zero bin", f"{r['curve'][0]['reg']:.3f} (n = {r['curve'][0]['n']})",
           f"`{key}.curve[0]`"),
        ]
    return out


def main():
    L = ["# Numbers trace — where every figure in the manuscript comes from", "",
         "Three kinds of number appear in the manuscript. **Re-derived** values are recomputed "
         "here from the event tables by `code/p2_model.py` and `code/run_numbers.py`, and are "
         "what the manuscript prints. **Package** values are carried over from an earlier TB01 "
         "package that produced them and are cited as such. **External** values come from a "
         "published product or a document outside this project.", "",
         "The P2/P2b fitting script was never retained, so the first thing this package did was "
         "rebuild it (`code/p2_model.py`) from the specification in `stage5/TB01/P2/PLAN.md` "
         "step 5 and check it against the two coefficients P2 reports. Section 1 below is that "
         "check.", "",
         "## 1. Reconstruction check — package value vs re-derived value", "",
         "Under the **RADD-only** dating rule, i.e. exactly the setting the packages used.", "",
         "| source | quantity | as published | re-derived here |", "|---|---|---|---|"]
    for src, q, old, new in REPRO:
        L.append(f"| {src} | {q} | {old} | **{new}** |")
    L += ["",
          "Point estimates reproduce throughout; the bootstrap intervals do not always, and the "
          "two coefficient rows differ enough to matter. The reconstruction resamples 0.5° "
          "blocks and refits the full design each draw; P2's own procedure cannot be inspected, "
          "so the difference cannot be attributed. Where a published interval is wider than the "
          "re-derived one, **the manuscript prints the re-derived interval and the limitations "
          "section records that the earlier interval was wider**. The one substantive "
          "disagreement is the 2020 joint coefficient (published 0.387 [0.129, 0.732], "
          "re-derived "
          + ci(g('2020_radd_any', 'coef_joint'), 3) + "): same sign, same conclusion, different "
          "width.", "",
          "## 2. The primary dating rule", "",
          "`date_upper = min(first RADD alert inside the polygon, DETER view_date)`. This is a "
          "**post-hoc, diagnosis-driven redefinition**: it was adopted after the P5b zero-bin "
          "diagnosis showed that RADD-only dating puts the alert *after* the analyst's own "
          "observation for 83.8 % (2021) and 96.8 % (2020) of the events with no post-event "
          "clear observation "
          f"(`stage5/TB01/P5b/zero_bin_stats.json`). It was not pre-registered, and every "
          "quantity is also reported under RADD-only dating as a sensitivity.", "",
          "| quantity | value | key |", "|---|---|---|"]
    for q, v, k in rows_primary():
        L.append(f"| {q} | **{v}** | {k} |")
    L += ["",
          "## 3. Package values carried over (not re-derived)", "",
          "| quantity | value | package |", "|---|---|---|",
          f"| 2020-unregistered events registering in 2021 | 94.0 % [92.2, 95.7] | `P3/P3_results.md` (raw 2020 deferral table not retained) |",
          f"| naive first-registration misattribution, 2020 / 2021 | 2.78 % / 3.48 % | `P3/P3_results.md` |",
          f"| two-year window residual misattribution | 0.12 % | `P3/P3_results.md` |",
          f"| clear_post AUC for non-registration, 2020 / 2021 | 0.729 / 0.712 | `P3/P3_results.md` |",
          f"| prior-year observation count AUC for deferral | 0.599 | `P5/P5_results.md` §3 |",
          f"| per-state thresholds τ | table in `SUPPLEMENTARY.md` | `P2/P2_results.md` §3–4 |",
          f"| RADD centroid-vs-polygon coverage and latency | table in `SUPPLEMENTARY.md` | `P1d/P1_RADD_correction.md` |",
          f"| Congo events, 2024-vintage dating | 4,959 dated of 5,243; n(0–2) = 202; gap 5.34 pp [2.91, 8.20] | `P4/P4_results.md` |",
          f"| Congo, 2021-vintage dating | coverage {CG['coverage_2021_vintage_all']*100:.1f} %; "
          f"{CG['shift_gt30_share']*100:.1f} % of dates move > 30 d; n(0–2) = {CG['n_lo']}; "
          f"H7(a) {CG['h7a_coef']:.3f} [{CG['h7a_ci'][0]:.3f}, {CG['h7a_ci'][1]:.3f}] | `P5b/p4b_stats.json` |",
          f"| zero-bin diagnosis (lag, prior-year change, December share) | see §1 of `P5b/ITEM1_zero_bin.md` | `P5b/zero_bin_stats.json` |",
          f"| 2020 offset-suspect share | {__import__('pandas').read_csv('aef_explore/paper/code/offset_2020.csv')['offset_suspect'].mean()*100:.1f} % of "
          f"{len(__import__('pandas').read_csv('aef_explore/paper/code/offset_2020.csv')):,} unregistered events | `code/offset_2020.py` (new in P6) |",
          "",
          "## 4. External values", "",
          "| quantity | source |", "|---|---|",
          "| annual embedding, 64 dimensions, 2017– | `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` (Brown et al., 2025) |",
          "| DETER polygons, Legal Amazon | TerraBrasilis WFS, INPE |",
          "| RADD alerts | `projects/radar-wur/raddalert/v1`; GFW Data API `wur_radd_alerts` v20220109 |",
          "| JRC TMF annual changes | `projects/JRC/TMF/v1_2024/AnnualChanges` |",
          "| Sentinel-2 L2A / Sentinel-1 GRD | `COPERNICUS/S2_SR_HARMONIZED`, `COPERNICUS/S1_GRD` |",
          "",
          "## 5. Figures", "",
          "| figure | script | inputs |", "|---|---|---|",
          "| F1, F2, F3, F4, F5, F7, F8 | `code/fig_results.py` | `numbers.json`, event tables, `data/products/*.tif` |",
          "| F6 | `code/fig_offset.py` | `code/offset_2020.csv`, DETER WFS, Earth Engine |",
          "| M1, M2 | `code/fig_maps.py` | `data/products/*.tif`, `code/outlines.geojson` |",
          ""]
    open("aef_explore/paper/NUMBERS_TRACE.md", "w").write("\n".join(L) + "\n")
    print("wrote NUMBERS_TRACE.md")


if __name__ == "__main__":
    main()
