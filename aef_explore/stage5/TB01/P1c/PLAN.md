# TB01-P1c — PLAN (written before any computation)

**Why this package exists.** P1 failed **by design, not by refutation**: its event set was built
from paired optical images (MapBiomas Alerta before/after bracket ≤ 62 days). That criterion can
only admit events that were already well observed, so the explanatory variable was truncated
(post-event clear counts 3–37 in A, no event anywhere with 1 or 2) and P(registered) sat on a
ceiling at ~0.996. H1 could not be tested. P1c replaces the optical-bracket label with a
**SAR-derived clearing date**, which is available regardless of cloud, and so recovers the
low-observation regime that P1 structurally excluded.

## 1. Datasets and access paths (all verified in P1 unless marked NEW)

| # | Dataset | Path | Note |
|---|---|---|---|
| D1 | DETER 2021 CR+VEG | TerraBrasilis WFS `deter-amz:deter_amz` | 37,938 nationally; 1,247 (A) + 669 (B) at ≥ 1 ha |
| D2 | MapBiomas Alerta 2021 | `mapbiomas-alertas:dashboard-alerts` WFS | before/after image dates verified in P1 |
| D5 | AlphaEarth annual | EE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` | 2020, 2021 |
| D8 | Sentinel-2 L2A | EE `COPERNICUS/S2_SR_HARMONIZED`, SCL ∉ {3,8,9,10,11} | same rule as P1 |
| D9 | RADD | EE `projects/radar-wur/raddalert/v1`, `sa_*` snapshots | min Date over 2021-04…2022-06 snapshots |
| **D11 (NEW)** | **Sentinel-1 GRD** | EE `COPERNICUS/S1_GRD`, IW, VV+VH, both passes, 2020-07-01…2022-03-31 | verified: **481** images over A (ASC 4 / DESC 477, rel. orbits 39/112/141), **1,382** over B (ASC 601 / DESC 781, 10 rel. orbits) |

Regions unchanged from P1: **A** = `-56.8409, -5.7426, -55.0379, -3.9339` (200 × 200 km on the
BR-163 box A1 centre); **B** = Roraima state polygon (`prodes-legal-amz:states_legal_amazon`).
Thresholds **carried over unchanged from P1**: **τ_A = 11.39°**, **τ_B = 19.13°**.

## 2. Method, fixed in advance

**Step 1 — SAR dating (all 1,916 events).** Per polygon, 10 m inward buffer, mean of VV and VH
(dB) at 30 m for every S1 scene covering it. Mixed tracks are handled by subtracting each
**relative-orbit's own full-series mean** from that orbit's observations before fitting, so
incidence-angle offsets cannot masquerade as a step. VV and VH are then z-scored and fitted
**jointly**: for every split point with **≥ 6 observations on each side**, the two-mean (step)
model is evaluated, and the split minimising total SSE — equivalently the largest mean shift —
is taken. Recorded per event: `sar_date` (midpoint of the two acquisitions straddling the
split), `shift_vv_db`, `shift_vh_db`, `sar_r2` (1 − SSE_step/SSE_flat on the joint series),
`sar_t` (pooled two-sample t), `n_obs`.

**Step 2 — validation gate (pre-registered).** On the 283 P1 bracketed events:
**ADOPT** SAR dating iff median |sar_date − bracket midpoint| ≤ **20 days** AND ≥ **70 %** of
sar_dates fall in the tightened interval `[image_before, min(image_after, DETER view_date)]`.
Otherwise **STOP and report** — no downstream step is run.

**Step 3 — explanatory variable.** Clear S2 count at the event centroid after `sar_date` within
calendar 2021 (`clear_post`), and the total 2021 clear count. Exact per-scene acquisition dates
(one indicator band per distinct S2 date), as in P1.

**Step 4 — registration and model.** `registered = ang_mean > τ_region`, angular change =
`acos(⟨e2020, e2021⟩)` in degrees over the 10 m-inward polygon interior. Model
`registered ~ clear_post + region + month(sar_date)`, logistic, L2. All CIs are 0.5°
block-bootstrap, 1,000 draws.
- **H1′** registration at `clear_post ∈ {0,1,2}` is at least **5 pp lower** than at
  `clear_post ≥ 5`, with the bootstrap CI of the difference **excluding 0**.
- **H3** registration at `clear_post ≥ 5` is **≥ 95 %** (unchanged from P1).
- The n in the 0–2 bin is reported per region; **if the total is < 30, H1′ is reported
  UNDERPOWERED, not FAIL.**

**Step 5 — interval-censored secondary check.** Alerta-matched events with bracket length
**62–180 days** (the events P1 discarded). `clear_post` is computed at **both** interval ends
(from `image_before` and from `image_after`), giving a bracketing pair of registration curves;
report whether the sign of the 0–2 vs ≥ 5 difference agrees with step 4 at both ends.

**Step 6 — RADD.** First RADD alert (`Alert ≥ 2`, date in 2021–22) **anywhere inside the
polygon** (min over the polygon, not the centroid); coverage and median latency vs `sar_date`,
per region, with block-bootstrap CIs.

## 3. Budget and compliance

Interactive Earth Engine only — `reduceRegions` over ≤ 40 polygons per call against a
date-stacked multi-band image, and `sampleRegions` on centroids; **no `Export.*`**, no
whole-scene raster reductions. Estimated ≪ 20 EECU-hours. "Point sampling only" is read as: all
extraction is interactive sampling of small features, never an export or a continental raster
pass — the polygon-interior mean the brief specifies in step 1 is taken with `reduceRegions` on
those small features. Nothing under `data/`, no shapefiles, no credentials committed.

## 4. Outputs

`PLAN.md`, `P1c_events.csv` (one row per DETER event), `P1c_results.md` (≤ 60 lines), and a
`RESEARCH_LOG.md` progress line after each numbered step, each committed and pushed.
