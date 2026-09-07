# TB01-P5 — Products, figures and paper skeleton

## 1. Map products (`figures/M_*.png` committed; GeoTIFFs in `data/products/`, **not** committed)
Two regions — **ParaBR163** `-56.8409, -5.7426, -55.0379, -3.9339` (τ = 12.73°) and **Roraima_S**
`-61.30, 1.20, -60.30, 2.10` (τ = 19.54°) — each with five layers:
(a) 2020→2021 angular change, (b) registration `change > τ_state`, (c) 2021 clear S2 observation count, (d) **attribution confidence** `p = σ(β₀ + β₁·clear_count)` with **β₀ = 2.1413, β₁ = 0.0552** fitted on the 38,303 dated 2021 events (`clear_post` only; stored in `p5_mapmodel.json`), (e) 2021→2022 deferral for pixels unregistered in 2021.

**Deviation from the brief, and why.** The PNG plates render the native 10 m sources, but the distributable GeoTIFFs are **30 m** (angular change, registration, deferral) and **60 m** (clear count, confidence), tiled 4 × 4 (Pará) / 2 × 2 (Roraima). `getDownloadURL` caps a request at 50 MB and the 10 m Pará angular-change grid is 404 MB; `Export.image.toDrive` is not reachable here.

**Worth reading off plates (c)/(d):** Sentinel-2 orbit-overlap striping is directly visible — the observation supply is banded, and so is confidence in the annual label. The paper's argument, rendered as a map.

## 2. Figures (all committed under `figures/`)
| file | content |
|---|---|
| `F1_registration_curve.png` | P(registered) vs post-event clear count, 2021 and 2020, bootstrap bands, H3 line |
| `F2_s1_stratification.png` | H7(b)′: low- vs high-SAR strata among `clear_post ≤ 2`, both years, 0.80 bar |
| `F3_deferral.png` | H4: share of Y-unregistered events registering in Y+1, both directions |
| `F4_radd_only.png` | optically-late events: registration and observability vs DETER-mapped |
| `F5_congo_panel.png` | gap by region-year, Congo marked **dating-limited** |
| `F6_offset_examples.png` | interior (green) vs 50–150 m ring (magenta) on 2 offset-suspect and 2 clean events |
| `M_ParaBR163.png`, `M_Roraima_S.png` | the five map layers per region |

**Note on F1:** monotone from the 1–2 bin upward, but the *exactly-zero* bin sits **higher** (0.699 in 2021, 0.899 in 2020). Zero-post-observation events are a distinct population — clearings dated to the last days of the year, whose change is carried almost entirely by the next year's imagery — and should be described separately, not smoothed over.

## 3. Attribution test on the mixed 2020 + 2021 population — **FAIL, and informatively so**
Replaces the degenerate H5. Pool both years (**77,962** events registering in Y or Y+1; 2,326 deferred). The year of **first registration** `Z` is observable; truth is `Z` for direct events, `Z−1` for deferred. The rule may use only variables computable without the event date — so `clear_post` is **disallowed**, and the feature is the *annual* clear-observation count of year `Z−1` at that pixel (newly extracted for both sets). `k` fitted on 2020, evaluated on the 38,256-event 2021 half; 0.5° block bootstrap.

| | value |
|---|---|
| deferred share (eval half) | 3.36 % |
| median annual clear obs in `Z−1`: deferred vs direct | **34.0 vs 35.0** |
| AUC, prior-year observation count predicting deferral | **0.599** |
| naive rule (assume `Z` is the truth) misattribution | **3.36 %** [2.94, 3.78] |
| fitted rule misattribution | **3.36 %** [2.94, 3.78] |
| reduction | **0.0 %** [0.0, 0.0] → **FAIL** |

`k*` is 0 — the rule never fires, because the feature does not separate the classes.

**Why this matters more than a pass would have.** `clear_post` predicts non-registration well (AUC 0.729/0.712, P3) but is **not available at attribution time** — computing it needs the event date the rule is inferring. Replacing it with the year-level count that *is* available destroys the signal. **Observation supply cannot repair year attribution.** The recommendation is the trivial thing that does work: a two-year acceptance window, cutting naive misattribution from 3.48 % to 0.12 %.

## 4. `PAPER_OUTLINE.md`
115 lines: title, 256-word abstract, sections 1–8 with figure/table pointers, the six claims (97.5–98.2 % ceiling; optical dominance not SAR-compensated; 94.0–96.5 % deferral; 45.7 % offset share; AUC 0.71–0.73 predictability; effect size as a lower bound set by dating accuracy), six limitations, the §7 negative result, and RSE as target.

## 5. Compute / compliance
GEE within the 40 EECU-h ceiling. **Exports used, as permitted**: GeoTIFFs in `data/products/` (git-ignored; `.gitignore` already excludes `data/` and `*.tif`). The whole-region 60 m clear-count and confidence rasters for both regions completed; the tiled 30 m angular-change / registration / deferral set was still downloading tile-by-tile when this was written — the PNG plates are the authoritative deliverable and are complete. PNG figures committed; no shapefiles or credentials committed.
