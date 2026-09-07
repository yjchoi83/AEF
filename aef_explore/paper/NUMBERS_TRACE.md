# Numbers trace — where every figure in the manuscript comes from

Three kinds of number appear in the manuscript. **Re-derived** values are recomputed here from the event tables by `code/p2_model.py` and `code/run_numbers.py`, and are what the manuscript prints. **Package** values are carried over from an earlier TB01 package that produced them and are cited as such. **External** values come from a published product or a document outside this project.

The P2/P2b fitting script was never retained, so the first thing this package did was rebuild it (`code/p2_model.py`) from the specification in `stage5/TB01/P2/PLAN.md` step 5 and check it against the two coefficients P2 reports. Section 1 below is that check.

## 1. Reconstruction check — package value vs re-derived value

Under the **RADD-only** dating rule, i.e. exactly the setting the packages used.

| source | quantity | as published | re-derived here |
|---|---|---|---|
| P2 §5 | 2021 registration at clear_post ≤ 2 | 0.631 | **0.631** |
| P2 §5 | 2021 registration at clear_post ≥ 5 | 0.975 | **0.9752** |
| P2 §5 | 2021 gap (pp) [CI] | 34.4 [28.3, 40.3] | **34.4 [27.8, 40.3]** |
| P2 §5 | 2021 n(0–2) | 518 | **518** |
| P2 §5 | 2021 n dated | 38,303 | **38,303** |
| P2 §5 | 2021 clear_post solo coefficient | 0.211 | **0.213** |
| P2 §5 | 2021 clear_post joint coefficient [CI] | 0.219 [0.046, 0.429] | **0.217 [0.111, 0.327]** |
| P2 §5 | events with clear_post ≤ 2 and s1_post ≥ overall median | 1 | **1** |
| P2b §2 | 2020 registration at clear_post ≤ 2 | 0.842 | **0.842** |
| P2b §2 | 2020 registration at clear_post ≥ 5 | 0.982 | **0.9821** |
| P2b §2 | 2020 gap (pp) [CI] | 14.1 [11.6, 16.6] | **14.1 [11.4, 16.7]** |
| P2b §2 | 2020 n(0–2) | 1,508 | **1,508** |
| P2b §2 | 2020 H7(b)′ SAR-dense stratum | 0.626 [0.548, 0.712] | **0.626 [0.546, 0.702]** |
| P2b §2 | 2020 H7(b)′ SAR-sparse stratum | 0.883 | **0.883** |
| P2b §2 | 2020 clear_post joint coefficient [CI] | 0.387 [0.129, 0.732] | **0.318 [0.221, 0.419]** |
| P2b §1 | 2021 gap excluding offset-suspect events | 28.0 [21.6, 34.0] | **28.0 [21.6, 34.3]** |
| P2b §1 | 2021 offset-suspect share | 45.7 % (608/1,332) | **45.6 % (608/1,332)** |
| P3 | 2021-unregistered events registering in 2022 | 96.5 % [95.3, 97.5] | **96.5 [95.3, 97.4] %** |

Point estimates reproduce throughout; the bootstrap intervals do not always, and the two coefficient rows differ enough to matter. The reconstruction resamples 0.5° blocks and refits the full design each draw; P2's own procedure cannot be inspected, so the difference cannot be attributed. Where a published interval is wider than the re-derived one, **the manuscript prints the re-derived interval and the limitations section records that the earlier interval was wider**. The one substantive disagreement is the 2020 joint coefficient (published 0.387 [0.129, 0.732], re-derived 0.318 [0.221, 0.419]): same sign, same conclusion, different width.

## 2. The primary dating rule

`date_upper = min(first RADD alert inside the polygon, DETER view_date)`. This is a **post-hoc, diagnosis-driven redefinition**: it was adopted after the P5b zero-bin diagnosis showed that RADD-only dating puts the alert *after* the analyst's own observation for 83.8 % (2021) and 96.8 % (2020) of the events with no post-event clear observation (`stage5/TB01/P5b/zero_bin_stats.json`). It was not pre-registered, and every quantity is also reported under RADD-only dating as a sensitivity.

| quantity | value | key |
|---|---|---|
| 2021 events dated | **38,303** | `numbers.json:2021_date_upper.n` |
| 2021 n(clear_post ≤ 2) | **361** | `2021_date_upper.n_lo` |
| 2021 P(registered | ≤ 2) | **0.510 [0.438, 0.584]** | `2021_date_upper.p_lo` |
| 2021 P(registered | ≥ 5) | **0.9750 [0.9717, 0.9778]** | `2021_date_upper.p_hi` |
| 2021 gap (pp) | **46.5 [39.0, 53.6]** | `2021_date_upper.gap` |
| 2021 clear_post coefficient, joint with s1_post | **0.083 [0.000, 0.172]** | `2021_date_upper.coef_joint` |
| 2021 H7(b)′ SAR-dense stratum | **0.447 [0.348, 0.554] (n = 152)** | `2021_date_upper.h7b_prime.hi` |
| 2021 H7(b)′ SAR-sparse stratum | **0.555 [0.459, 0.638] (n = 209)** | `2021_date_upper.h7b_prime.lo` |
| 2021 zero bin | **0.289 (n = 38)** | `2021_date_upper.curve[0]` |
| 2020 events dated | **39,664** | `numbers.json:2020_date_upper.n` |
| 2020 n(clear_post ≤ 2) | **439** | `2020_date_upper.n_lo` |
| 2020 P(registered | ≤ 2) | **0.606 [0.541, 0.669]** | `2020_date_upper.p_lo` |
| 2020 P(registered | ≥ 5) | **0.9811 [0.9785, 0.9836]** | `2020_date_upper.p_hi` |
| 2020 gap (pp) | **37.5 [31.3, 43.9]** | `2020_date_upper.gap` |
| 2020 clear_post coefficient, joint with s1_post | **0.112 [0.010, 0.252]** | `2020_date_upper.coef_joint` |
| 2020 H7(b)′ SAR-dense stratum | **0.538 [0.436, 0.646] (n = 169)** | `2020_date_upper.h7b_prime.hi` |
| 2020 H7(b)′ SAR-sparse stratum | **0.648 [0.573, 0.714] (n = 270)** | `2020_date_upper.h7b_prime.lo` |
| 2020 zero bin | **0.500 (n = 50)** | `2020_date_upper.curve[0]` |

## 3. Package values carried over (not re-derived)

| quantity | value | package |
|---|---|---|
| 2020-unregistered events registering in 2021 | 94.0 % [92.2, 95.7] | `P3/P3_results.md` (raw 2020 deferral table not retained) |
| naive first-registration misattribution, 2020 / 2021 | 2.78 % / 3.48 % | `P3/P3_results.md` |
| two-year window residual misattribution | 0.12 % | `P3/P3_results.md` |
| clear_post AUC for non-registration, 2020 / 2021 | 0.729 / 0.712 | `P3/P3_results.md` |
| prior-year observation count AUC for deferral | 0.599 | `P5/P5_results.md` §3 |
| per-state thresholds τ | table in `SUPPLEMENTARY.md` | `P2/P2_results.md` §3–4 |
| RADD centroid-vs-polygon coverage and latency | table in `SUPPLEMENTARY.md` | `P1d/P1_RADD_correction.md` |
| Congo events, 2024-vintage dating | 4,959 dated of 5,243; n(0–2) = 202; gap 5.34 pp [2.91, 8.20] | `P4/P4_results.md` |
| Congo, 2021-vintage dating | coverage 90.4 %; 11.0 % of dates move > 30 d; n(0–2) = 8; H7(a) 0.737 [0.190, 1.349] | `P5b/p4b_stats.json` |
| zero-bin diagnosis (lag, prior-year change, December share) | see §1 of `P5b/ITEM1_zero_bin.md` | `P5b/zero_bin_stats.json` |
| 2020 offset-suspect share | 48.0 % of 1,102 unregistered events | `code/offset_2020.py` (new in P6) |

## 4. External values

| quantity | source |
|---|---|
| annual embedding, 64 dimensions, 2017– | `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` (Brown et al., 2025) |
| DETER polygons, Legal Amazon | TerraBrasilis WFS, INPE |
| RADD alerts | `projects/radar-wur/raddalert/v1`; GFW Data API `wur_radd_alerts` v20220109 |
| JRC TMF annual changes | `projects/JRC/TMF/v1_2024/AnnualChanges` |
| Sentinel-2 L2A / Sentinel-1 GRD | `COPERNICUS/S2_SR_HARMONIZED`, `COPERNICUS/S1_GRD` |

## 5. Figures

| figure | script | inputs |
|---|---|---|
| F1, F2, F3, F4, F5, F7, F8 | `code/fig_results.py` | `numbers.json`, event tables, `data/products/*.tif` |
| F6 | `code/fig_offset.py` | `code/offset_2020.csv`, DETER WFS, Earth Engine |
| M1, M2 | `code/fig_maps.py` | `data/products/*.tif`, `code/outlines.geojson` |

