# TB01-P1c — Results: SAR-dated event population and the low-observation regime

> **PRE-REGISTERED GATE FAILED → STOPPED at step 2.** Steps 3–5 (post-SAR-date clear counts,
> H1′/H3 model, interval-censored check) were **not run**, as PLAN.md required. Steps 1, 2 and 6
> are reported below, plus SAR-independent descriptives.

## 1. SAR dating of the full event population (1,916 events: A 1,247 + B 669; 845 in the custom boxes)
S1 GRD IW VV+VH, both passes, 2020-07-01…2022-03-31, polygon interior mean (10 m inward buffer) at 30 m: **219,318 observations**, median **97** per event in A / **137** in B, min 91 — the ≥ 6-per-side rule never binds. Per-relative-orbit de-meaning precedes the joint z-scored single-breakpoint fit (largest mean shift).

| | A | B |
|---|---|---|
| median joint-fit R² | 0.214 | 0.198 |
| median step t | −3.94 | −6.30 |
| median VV / VH shift (dB) | −0.39 / −0.37 | −0.63 / −0.72 |
| SAR date in 2021 | 962 / 1,247 (77 %) | 587 / 669 (88 %) |

Shifts of −0.4 to −0.7 dB are far below the 2–4 dB VH drop a stand-replacing clearing gives: the polygon-mean series is dominated by speckle and track/seasonal variation, so the breakpoint search frequently picks noise.

## 2. Validation gate on the 283 P1 bracketed events — **FAIL on both criteria**

| criterion | required | observed | block-bootstrap CI |
|---|---|---|---|
| median \|SAR date − bracket midpoint\| | ≤ 20 d | **27.0 d** | [23.0, 35.0] |
| share inside [before, min(after, view_date)] | ≥ 70 % | **27.9 %** | [0.234, 0.346] |

Tightened-interval width: median 31 d (IQR 22–43), so chance agreement ≈ 9 % — the fit beats chance ~3× and is still nowhere near the bar. Signed error: median +12 d, mean −6 d; 34 % within ±15 d, 53 % within ±30 d, 69 % within ±60 d. Per region: A 26.5 d / 28.2 %, B 39.0 d / 25.8 %. Fit-quality stratification does not rescue it — the best R² quartile is still only 32 % inside.

**Robustness of the failure** (diagnostics, none pre-registered, none adopted):

| variant | median \|diff\| | share inside |
|---|---|---|
| pre-registered (VV+VH, orbit-demeaned, full window) | 27 d | 0.276 |
| VH only | 32 d | 0.205 |
| VV only | 27 d | 0.311 |
| no orbit de-meaning | 28 d | 0.251 |
| search window restricted to 2020-10…2022-01 | 24 d | 0.314 |

No variant reaches either threshold: the STOP is a property of single-breakpoint dating on polygon-mean S1 backscatter, not of one implementation choice.

## 3. Step 6 — RADD latency using **any** alert inside the polygon (min date), not the centroid

| region | coverage | median latency vs P1 bracket midpoint | share ≥ 2 months |
|---|---|---|---|
| A | **1,217 / 1,247 = 97.6 %** | **−11 d** [−18, −8] | **0.000** [0.000, 0.000] |
| B | **571 / 669 = 85.4 %** | **−7 d** [−19, −6] | **0.000** [0.000, 0.000] |

Latency uses the 283 P1 events, the only ones with an optical reference date. **This overturns P1 §5**: P1's centroid sampling gave 48 %/55 % coverage, median +35.5/+70.0 d, 29 %/59 % "≥ 2 months late". Sampling the whole polygon shows RADD covers ~90 % of DETER events and fires *before* the optical bracket midpoint. P1's RADD row was a centroid-sampling artefact and should not be cited.

## 4. SAR-independent descriptive: registration over the full DETER population
Same τ as P1 (τ_A = 11.39°, τ_B = 19.13°). All 1,916 events: **A 0.9928** [0.9823, 0.9981] (n = 1,247) · **B 0.9492** [0.9193, 0.9764] (n = 669). Roraima's un-selected population sits ~5 pp below the ceiling P1 reported (B was 31/31 = 1.000), so a low-observation regime does exist once optical-bracket selection is removed. Exploratory, **not pre-registered**: by 2021 *total* clear-obs quartile registration runs 0.950 (13–22 obs) → 0.980 (23–25) → 0.989 (26–28) → 0.995 (29–68) — monotone, and the very signal H1 was built to detect. Testing it properly needs a per-event date this gate did not deliver.

## 5. Compute / compliance
Interactive EE only (`reduceRegions` on ≤ 40 small polygons per call, `sampleRegions` on centroids); **no exports**, no continental raster passes; well under 20 EECU-h. No `data/`, shapefiles or credentials committed.
