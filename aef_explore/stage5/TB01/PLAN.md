# TB01-P1 — PLAN (written before any computation)

Package: expert-dated event set + registration-probability curve for the **annual**
AlphaEarth embedding. Two regions, 2021 events, one row per event.

## 0. Gate check — MapBiomas Alerta before/after image dates

**REQUIRED BY THE BRIEF: STOP if Alerta does not expose before/after image dates.**
Gate **PASSED**. Verified by `DescribeFeatureType` + a live `GetFeature` on the public
MapBiomas Alerta GeoServer (no token needed):

- Layer `mapbiomas-alertas:dashboard-alerts` exposes typed `xsd:date` fields
  **`image_acquired_before_at`** and **`image_acquired_after_at`** (plus `detected_at`,
  `published_at`, `area_ha`, `alert_code`, `geom`).
- Read-back of 2 arbitrary features returned populated real values, e.g.
  `alert_code 594044: before 2022-01-20, after 2022-07-07`.
- `numberMatched` for `detected_at` in calendar 2021 = **91,015** nationally.
- Sibling layer `mapbiomas-alertas:dashboard-alert-shapefile` carries the same pair as
  strings (`image_before_at` / `image_after_at`) and reports 91,602 alerts with
  `year_detected_at = 2021`; it is the cross-check, not the primary source.

No substitution is made or needed.

## 1. Datasets and verified access paths

| # | Dataset | Access path | Verification |
|---|---|---|---|
| D1 | DETER Amazonia clearing polygons 2021 | WFS `https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/deter_amz/ows`, `typeNames=deter-amz:deter_amz`, CQL `view_date` in 2021 AND `classname IN ('DESMATAMENTO_CR','DESMATAMENTO_VEG')` | `resultType=hits` → **37,938**, identical to the stage5/roi ROI_REPORT count, so this is the same download being reused (the stage5 copy lived under the git-ignored `data/` tree and is re-fetched here) |
| D2 | MapBiomas Alerta 2021 | WFS `https://geoserver.alerta.mapbiomas.org/geoserver/ows`, `typeNames=mapbiomas-alertas:dashboard-alerts`, GeoJSON out, `CQL_FILTER=BBOX(geom,minlon,minlat,maxlon,maxlat,'CRS:84') AND detected_at ...` | see §0; BBOX axis order confirmed by reading back feature coordinates (WFS 2.0 defaults to lat/lon, so `'CRS:84'` is passed explicitly) |
| D3 | Brazilian Legal Amazon limit | WFS `https://terrabrasilis.dpi.inpe.br/geoserver/ows`, `prodes-legal-amz:brazilian_legal_amazon` | hits = 1 |
| D4 | Roraima state polygon (region B) | same WFS, `prodes-legal-amz:states_legal_amazon`, `sigla='RR'` (official IBGE/INPE limit) | hits = 13 states |
| D5 | AlphaEarth annual embedding | EE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` | 2020: 10,576 images; 2021: 10,614; 64 bands |
| D6 | JRC TMF Annual Changes | EE `projects/JRC/TMF/v1_2024/AnnualChanges` | 3 images, bands `Dec1990`…`Dec2024`; uses `Dec2020`, `Dec2021`, class 1 = undisturbed tropical moist forest |
| D7 | Hansen GFC | EE `UMD/hansen/global_forest_change_2025_v1_13` | band list read back; `lossyear` 19–22 excluded from stable forest |
| D8 | Sentinel-2 L2A | EE `COPERNICUS/S2_SR_HARMONIZED`, `SCL` band, clear = `SCL ∉ {3,8,9,10,11}` | collection reachable; `SCL` present |
| D9 | RADD alerts | EE `projects/radar-wur/raddalert/v1`, South America tiles (`system:index` contains `sa_`), latest = `sa_20260826`, bands `Alert`,`Date` (YYDDD) | read back |
| D10 | Custom-embedding boxes (flag only) | EE `projects/alpha-earth-app/assets/TB01_custom_embedding_roi` | 2 features (BoxA_BR163_Para, BoxB_Roraima) |

## 2. Regions

- **A — Pará / BR-163 corridor.** Stage-5 box A1 is `-56.3, -5.2, -55.5788, -4.4765`
  (centre `-55.9394, -4.8383`). Expanded to ~200 × 200 km about that centre:
  **`-56.8409, -5.7426, -55.0379, -3.9339`**.
- **B — Roraima.** The state polygon (D4), used as-is.
- Every event is flagged `in_custom_box` when its centroid falls inside either 80 × 80 km
  box of D10, for later sub-annual work.

## 3. Glossary — terms fixed before computing

- **DETER event**: a 2021 `DESMATAMENTO_CR`/`DESMATAMENTO_VEG` polygon with geodesic area ≥ 1 ha.
- **Bracket**: `[image_acquired_before_at, image_acquired_after_at]` of the matched Alerta alert.
- **Bracket length**: after − before, in days; kept only if ≤ 62 days.
- **Match**: DETER∩Alerta area ≥ 50 % of the DETER polygon area. When several alerts qualify,
  the one with the largest overlap fraction is kept.
- **Event month**: calendar month of the bracket midpoint `before + (after−before)/2`.
- **Angular change**: `acos(clamp(⟨e2020, e2021⟩, −1, 1))` in degrees on the unit-norm 64-d
  AEF vectors; per event, the mean over the polygon **interior** (10 m inward buffer).
- **Stable forest** (per region): TMF `Dec2020 = 1` AND `Dec2021 = 1`, AND Hansen
  `lossyear` ∉ {19, 20, 21, 22}. ≥ 2,000 pixels sampled per region.
- **Threshold `τ_region`**: the **p90 of the angular change over that region's stable-forest
  sample** — one number per region, defined here and not re-tuned afterwards.
- **Registered**: event mean angular change > `τ_region`.
- **Post-event clear count**: number of `COPERNICUS/S2_SR_HARMONIZED` scenes at the event
  centroid, within calendar 2021, with acquisition date **after the bracket midpoint** and
  clear SCL at that pixel. **Total 2021 clear count**: same, whole of 2021.
- **RADD latency**: RADD first-alert date at the event centroid minus the bracket midpoint, days.

## 4. Pre-registered criteria (fixed before any model is fitted)

- **H1** P(registered) increases monotonically with post-event clear count —
  Spearman ρ over count bins ≥ 0.5 **in both regions**.
- **H2** the region term is not significant once clear count is controlled (informative either way).
- **H3** events with ≥ 5 post-event clear observations are registered ≥ 95 % of the time.
- **Pass = H1 AND H3.**
- Model: logistic `registered ~ post_clear + region + month`, plus a likelihood-ratio test of
  the `region × post_clear` interaction. Reported P(registered) at post-event counts
  0, 1, 2, 3, 5, 10 per region. **All** reported numbers carry 0.5° block-bootstrap CIs,
  1,000 draws, blocks resampled with replacement.

## 5. Observability-bias check (§6 of the brief)

200 random 80 × 80 km boxes inside the Legal Amazon (D3); per box, DETER 2021 clearing
count (centroids inside) vs mean 2021 clear-observation count (`reduceRegion`, mean, 500 m).
Pearson and Spearman, each with a bootstrap CI over boxes.

## 6. Budget and compliance

Earth Engine: interactive `reduceRegion`/`getRegion` only, chunked ≤ 10,000 samples per call,
**no `Export.*`**. Stable-forest sampling is 2 × ~4,000 points at 10 m; per-event reductions are
batched over ≤ 500 polygons per call at 10 m; the 200-box bias scan reduces at 500 m.
Estimated well under the 25 EECU-hour ceiling. Nothing under `data/`, no shapefiles and no
credentials are committed.

## 7. Outputs

`PLAN.md` (this file), `P1_event_set.csv` (one row per event, written not printed),
`P1_results.md` (≤ 60 lines), and a 10-line entry appended to `/RESEARCH_LOG.md`.
