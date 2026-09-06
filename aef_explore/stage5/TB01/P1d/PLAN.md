# TB01-P1d — PLAN (written before any computation)

**Why this package exists.** P1 was selected by optical brackets and hit a registration ceiling;
P1c pre-registered SAR dating and **failed its gate** (median |SAR − bracket midpoint| 27.0 d vs
≤ 20 required; 27.9 % inside the tightened interval). But P1c step 6 found the dating source that
P1 had mis-sampled: RADD, read over the **whole polygon** instead of the centroid, covers 97.6 %
(A) / 85.4 % (B) of DETER events and fires *before* the optical bracket midpoint (−11 d / −7 d).
P1d formalises RADD as the event date and runs the low-observation test H1′ on it.

## 1. Datasets and access paths (all verified in P1/P1c)

| # | Dataset | Path | Note |
|---|---|---|---|
| D1 | DETER 2021 CR+VEG ≥ 1 ha | TerraBrasilis WFS `deter-amz:deter_amz` | 1,247 (A) + 669 (B) = **1,916** events, already extracted |
| D2 | MapBiomas Alerta 2021 | `mapbiomas-alertas:dashboard-alerts` WFS | 283 bracketed events, for step 2 only |
| D5 | AlphaEarth annual | EE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2020, 2021 | polygon-interior angular change already extracted for all 1,916 |
| D8 | Sentinel-2 L2A | EE `COPERNICUS/S2_SR_HARMONIZED`, SCL ∉ {3,8,9,10,11} | per-date clear indicator already extracted for all 1,916 centroids |
| D9 | RADD | EE `projects/radar-wur/raddalert/v1`, `sa_*` snapshots 2021-04…2022-06 | `Date` (YYDDD) masked to 2021–22; **min over the polygon** |

Regions, and the thresholds, are **unchanged**: A = `-56.8409, -5.7426, -55.0379, -3.9339`;
B = Roraima state polygon; **τ_A = 11.39°**, **τ_B = 19.13°** (P1 stable-forest p90).

## 2. Method and pre-registered criteria, fixed in advance

**Step 1 — event date.** `radd_any` = min `Date` over the polygon with `Alert ≥ 2` (unconfirmed or
confirmed); `radd_high` = the same with `Alert = 3` (confirmed only). `date_upper` =
`min(radd_any, DETER view_date)`. Coverage per region; the undated remainder is described by area
distribution and DESMATAMENTO_CR vs DESMATAMENTO_VEG split.

**Step 2 — validation gate (pre-registered).** On the 283 P1 bracketed events, with the tightened
interval `I = [image_before, min(image_after, view_date)]`:
- `diff` = **signed distance from the RADD date to I**: `0` if inside, negative if earlier than
  `image_before`, positive if later than the upper end. This is the statistic the gate is on.
- **ADOPT** RADD dating iff **median |diff| ≤ 20 days**.
- `share inside I` is reported **descriptively only** — RADD fires early by design, so being
  outside I on the early side is expected and is not a failure.
- The midpoint-referenced statistic (RADD date − interval midpoint) is also reported, for
  comparability with P1 §5 and P1c §2.

**Step 3 — explanatory variables (optical only).** `clear_post` = clear S2 observations at the
event centroid after the event date within calendar 2021, from exact per-scene acquisition dates;
`clear_total_2021` = the 2021 total. Same SCL rule as P1.

**Step 4 — registration and model.** `registered = ang_mean > τ_region` on the 10 m-inward
polygon interior. Model `registered ~ clear_post + region + month(event date)`, logistic, L2.
All CIs are 0.5° block-bootstrap, 1,000 draws.
- **H1′** registration at `clear_post ∈ {0,1,2}` is at least **5 pp lower** than at
  `clear_post ≥ 5`, with the bootstrap CI of the difference **excluding 0**.
- **H3** registration at `clear_post ≥ 5` is **≥ 95 %**.
- n in the 0–2 bin is reported per region; **if the pooled total is < 30, H1′ is reported
  UNDERPOWERED, not FAIL.**
- **Sensitivity:** the whole of step 4 repeated with (a) `date_upper` and (b) `radd_high`.

**Step 5 — circularity check.** RADD is a radar product and the AEF embedding ingests S1, so
RADD-dated events could be the ones AEF was always going to register. Registration rate for
RADD-dated vs RADD-undated events, with block-bootstrap CIs, plus one paragraph of discussion.

**Step 6 — retraction note.** `P1_RADD_correction.md` recording that P1 §5 (centroid-sampled RADD
latency) is superseded by P1c §3.

## 3. Budget and compliance

Only one new Earth Engine extraction is required — `radd_high` by `reduceRegions` over ≤ 40
polygons per call. Angular change, `radd_any` and the S2 per-date matrices were extracted in P1c
and are reused. **No `Export.*`**, polygon `reduceRegions` and centroid `sampleRegions` only;
≪ 15 EECU-hours. Nothing under `data/`, no shapefiles, no credentials committed.

## 4. Outputs

`PLAN.md`, `P1d_events.csv`, `P1d_results.md` (≤ 60 lines), `P1_RADD_correction.md`, a
`RESEARCH_LOG.md` line after each numbered step, and the repo-root `PROGRESS.md` board — each
committed and pushed.
