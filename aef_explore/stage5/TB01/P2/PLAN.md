# TB01-P2 — PLAN (written before any computation)

**Where this stands.** P1 (optical-bracket events) hit a registration ceiling and failed H1 *by
design*. P1c (SAR dating) failed its pre-registered gate but exposed a centroid-sampling bug in the
RADD field. P1d (RADD dating, polygon-wide) passed its gate and **met H1′** — registration 0.652 at
`clear_post ≤ 2` vs 0.986 at `≥ 5`, a +33.3 pp gap [8.4, 68.1] — but on only **23 events** in the
0–2 bin, below the 30-event floor. P2 scales the design to the whole Brazilian Legal Amazon to put
n(0–2) over 100, and adds the covariate that decides whether the finding is about *optical*
observation density or about observation density in general.

## 1. Datasets and access paths (verified in P1/P1c/P1d unless marked NEW)

| # | Dataset | Path |
|---|---|---|
| D1 | DETER 2021 CR+VEG | TerraBrasilis WFS `deter-amz:deter_amz`, `view_date` in 2021 — 37,938 polygons (all sizes) |
| **D1b (NEW)** | DETER **2022** CR+VEG | same WFS, `view_date` in 2022 — for the RADD-only set |
| D3 | Legal Amazon limit | `prodes-legal-amz:brazilian_legal_amazon` |
| D4 | States | `prodes-legal-amz:states_legal_amazon` (13 features) |
| D5 | AlphaEarth annual | EE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` 2020, 2021 |
| D6 | JRC TMF | EE `projects/JRC/TMF/v1_2024/AnnualChanges`, `Dec2020`, `Dec2021`, class 1 |
| D7 | Hansen GFC | EE `UMD/hansen/global_forest_change_2025_v1_13`, `lossyear` ∉ {19,20,21,22} |
| D8 | Sentinel-2 L2A | EE `COPERNICUS/S2_SR_HARMONIZED`, clear = SCL ∉ {3,8,9,10,11} |
| **D11** | Sentinel-1 GRD | EE `COPERNICUS/S1_GRD`, IW, both passes — scene counts only |
| D9 | RADD | EE `projects/radar-wur/raddalert/v1`, `sa_*` snapshots 2021-04…2022-06, `Date` masked to 2021–22 |

## 2. Steps and definitions, fixed in advance

**Step 0 — QC chips.** The 23 unregistered-or-low-observation events from P1d's 0–2 bin plus 30
registered events stratified by region. Three panels per event — S2 2020 dry-season median, S2 2021
post-event clear composite (else the latest clear scene), 2020→2021 AEF angular change — each with
the DETER polygon painted and the RADD date in the title. `qc_table.csv` carries
`id, region, clear_post, registered, decision (blank), auto_note`. **Work continues without the
human decision; every verdict in this batch is stamped "pending QC" until `decision` is filled.**

**Step 1 — population.** All DETER 2021 CR+VEG polygons ≥ 1 ha in the Legal Amazon. Event date =
first RADD alert inside the polygon (any confidence, `Alert ≥ 2`, min `Date`);
`date_upper = min(radd_any, view_date)`. Per-state counts and RADD coverage reported.

**Step 2 — RADD-only set.** DETER **2022** CR+VEG polygons ≥ 1 ha that do **not** overlap any DETER
2021 polygon, and inside which RADD **high-confidence 2021** alerts cover ≥ 1 ha. These are
clearings that happened in 2021 but were optically invisible until 2022. Dated by their first RADD
2021 alert, flagged `radd_only = 1`, counted per state.

**Step 3 — covariate layers, built once.** Twelve monthly 2021 S2 clear-observation-count images
(same SCL rule) and twelve monthly 2021 S1 GRD scene-count images (both passes). Per event, sampled
at the centroid: `clear_post` = S2 clear observations in the months **after** the RADD date, with
the event month **prorated** by the fraction of the month remaining; `s1_post` likewise; plus the
2021 totals. Monthly proration replaces P1d's exact per-scene dates — the change is forced by
running Amazon-wide and is recorded here.

**Step 4 — registration.** Stable forest = TMF `Dec2020 = 1 ∧ Dec2021 = 1`, Hansen
`lossyear ∉ {19,20,21,22}`; **per-state** threshold τ_state = p90 of the 2020→2021 angular change on
**≥ 2,000 stable-forest pixels per state**. `registered = ang_mean > τ_state`, where `ang_mean` is
the polygon-interior mean (10 m inward buffer) of `acos(⟨e2020, e2021⟩)` in degrees.

**Step 5 — model and pre-registered criteria.**
`registered ~ f(clear_post) + f(s1_post) + state + month + radd_only`, logistic, L2; all CIs are
0.5° block-bootstrap, 1,000 draws.
- **H1″** registration at `clear_post ≤ 2` is **≥ 5 pp below** that at `clear_post ≥ 5`, with the
  CI of the difference **excluding 0**, **and n(0–2) ≥ 100**.
- **H3** registration at `clear_post ≥ 5` is **≥ 95 %**.
- **H7 (DECISIVE)** both must hold: (a) the `clear_post` effect survives conditioning on `s1_post`
  — its coefficient CI still excludes 0 in the joint model; **and** (b) among events with
  `s1_post ≥ median(s1_post)`, registration at `clear_post ≤ 2` is **still below 80 %**.
- **If H7 fails** — the optical effect vanishes once S1 density is controlled, or low registration
  occurs only where S1 is *also* sparse — the finding is **"no observations, no change"**, the
  paper is downgraded, and **the batch STOPS** (P3 and P4 are not run).

**Step 6 — robustness.** τ at p85 / p90 / p95; polygon size classes; `radd_high` only; `date_upper`;
with and without `radd_only` events. H1″ and H7 are reported for **every** variant.

## 3. Budget and compliance
Polygon `reduceRegions` (AEF, RADD), centroid `sampleRegions` (covariates) and `getThumbURL`
(QC chips) only. **No image exports.** Batch ceiling 60 EECU-hours across P2–P4. Nothing under
`data/`, no shapefiles, no credentials committed.

## 4. Outputs
`PLAN.md`, `P2_events.csv`, `qc_table.csv`, `results/qc_chips/*.png`, `P2_results.md` (≤ 60 lines);
a `RESEARCH_LOG.md` line and a `PROGRESS.md` update after each numbered step.
