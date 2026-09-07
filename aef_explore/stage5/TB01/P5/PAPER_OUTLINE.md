# TB01 — Paper outline

**Title.** *Annual is not blind, but it is optical: what a global annual embedding registers when
clouds hide the clearing*

**Target.** Remote Sensing of Environment (RSE). Fallback: ISPRS J. Photogramm. Remote Sens.

## Abstract (250 words)
Annual global embedding products such as AlphaEarth Foundations compress a year of satellite
observation into one per-pixel vector and are increasingly used as a general-purpose substrate for
land-change analysis. We ask a prior question: which forest-clearing events does an annual embedding
actually register, and what governs the exceptions? Using 78,000 expert-mapped clearings across the
Brazilian Legal Amazon for 2020 and 2021, dated by Sentinel-1 RADD alerts read over the whole
polygon, we define registration as a year-on-year embedding angular change exceeding a per-state
stable-forest p90 threshold. Registration is saturated — 97.5 % (2021) and 98.2 % (2020) — for
events followed by five or more clear Sentinel-2 observations, but falls to 63.1 % and 84.2 % for
events followed by two or fewer. The deficit is specifically optical, not a general observation
deficit: among low-optical events, registration is *lowest* where Sentinel-1 coverage is densest
(0.48–0.68 in the top within-month SAR quartile), so radar acquisition does not compensate. Events
unregistered in year Y are deferred rather than missed — 94.0 % and 96.5 % register in Y+1, leaving
a true miss rate near 1 in 800. We show that 45.7 % of unregistered events carry a stronger change
signal in a 50–150 m ring than in the polygon interior, a geometric mismatch explaining part but not
most of the deficit. Post-event observation count predicts non-registration with AUC 0.71–0.73, yet
this signal is unavailable to a year-attribution rule, because computing it requires the event date
being inferred. A Congo Basin replication reproduces the direction but not the magnitude.

## 1. Introduction
- Annual embeddings as a substrate; the implicit assumption that "annual" means "complete for the year".
- Prior work treats misses as a detector-threshold problem; we treat them as an *observation-supply* problem.
- Contributions: (i) registration curve vs post-event optical supply at continental scale and in two
  years; (ii) the SAR-does-not-compensate result; (iii) deferral vs miss; (iv) a negative result on
  year attribution; (v) an explicit statement that the effect size is a lower bound set by dating accuracy.

## 2. Data
- AlphaEarth annual embedding (`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`) 2019–2022.
- Events: DETER 2020 and 2021 CR+VEG ≥ 1 ha, Legal Amazon (43,316 + 37,689) → **Table 1**.
- `radd_only` events: RADD-confirmed clearings DETER mapped only the following year (2,601 + 3,082).
- Dating: RADD first alert **inside the polygon** (§3.1) — the correction that made the study possible.
- Covariates: monthly Sentinel-2 clear-observation counts (SCL rule) and Sentinel-1 IW scene counts.
- Thresholds: per-state p90 of angular change on ≥ 2,000 TMF/Hansen stable-forest pixels → **Table 2**.
- Congo: two 100 × 100 km DRC ROIs, 5,243 TMF-2021 patches ≥ 1 ha.

## 3. Methods
### 3.1 Dating and the centroid trap
Centroid sampling gives 48–55 % RADD coverage and a spurious +35 to +70 d latency; polygon-wide
sampling gives 85–98 % and −7 to −11 d. **Table 3**; retraction note `P1d/P1_RADD_correction.md`.
### 3.2 Registration
Interior mean (10 m inward buffer) of `acos(⟨e_{Y−1}, e_Y⟩)`; `registered = change > τ_state`.
### 3.3 Explanatory variables
`clear_post` / `s1_post`, prorated in the event month; annual totals.
### 3.4 Inference
Logistic models; 0.5° block bootstrap, 1,000 draws, throughout.
### 3.5 Pre-registration and its failures
Criteria fixed before fitting in every package; two were unusable as written (H7(b) selected an empty stratum; H5 had a degenerate label) and are reported as such — see §7.

## 4. Results
### 4.1 The registration curve — **Figure 1**
Monotone from bin 2 upward in both years; 0.60 → 0.98 (2021), 0.72 → 0.99 (2020). Ceiling **97.5 % / 98.2 %** at ≥ 5 observations. Gap **+34.4 pp** [28.4, 40.2] (2021) and **+14.1 pp** [11.6, 16.6] (2020); n(0–2) = 518 / 1,508. **Table 4** carries nine robustness variants (τ p85/p90/p95, high-confidence RADD, `date_upper`, ± `radd_only`, three size classes).
### 4.2 Optical dominance is not SAR-compensated — **Figure 2**
Pre-registered out-of-sample test on 2020: low-optical events with at-or-above-own-month-median S1
register **0.626** [0.548, 0.712], below the low-S1 stratum's 0.883. Within-month S1 quartiles run
0.890 → 0.684 (2020) and 0.777 → 0.477 (2021) — registration *falls* as SAR density rises.
The joint `clear_post` coefficient survives conditioning on `s1_post` (0.387 [0.129, 0.732]).
### 4.3 Deferral, not miss — **Figure 3**
94.0 % [92.2, 95.7] and 96.5 % [95.3, 97.5] of Y-unregistered events register in Y+1 against an
independently estimated next-year threshold. True miss rate 0.12–0.17 % (~1 in 800).
### 4.4 Optically late events — **Figure 4**
3,082 clearings RADD confirmed in 2021 and DETER mapped only in 2022 register at 0.753 vs 0.984 —
a population invisible to any DETER-anchored study, and enriched in the low-observation tail.
### 4.5 Polygon geometry — **Figure 6**, **Table 5**
45.7 % of unregistered events show ring > τ with interior < τ. Excluding them, the gap falls
34.4 → 28.0 pp [21.6, 34.0] and the joint coefficient *strengthens* (0.508 [0.205, 0.958]).
### 4.6 Congo — **Figure 5**
Gap **5.34 pp** [2.91, 8.20]: direction replicates, magnitude does not; `clear_post` coefficient
2.19 [1.44, 2.84] is the strongest of any region. **Dating-limited** — see §6.2.

## 5. Products — **Figure 7** (map plates), `data/products/`
Angular change, registration, 2021 clear-count, attribution confidence
`p = σ(β₀ + β₁·clear_count)`, and the 2021→2022 deferral layer, for the Pará BR-163 200 km region
and a Roraima region. The clear-count and confidence plates show Sentinel-2 orbit-overlap striping
directly — the observation supply is visibly banded, and so is the confidence in the annual label.

## 6. Limitations
1. **DETER is optically selected.** The event set inherits an optical bias; `radd_only` events (§4.4) partly correct it but do not remove it.
2. **RADD dating vintage.** Brazil 2021 uses snapshots from 2021-10; Brazil 2020 has no
   contemporaneous snapshot (earliest 2021-10-13); Congo has none before 2024-01. Dating error
   attenuates `clear_post`, so **every reported gap is a lower bound**, and the 2020 < 2021 ordering
   is partly a dating artifact. A 2021-vintage RADD Africa raster exists (`wur_radd_alerts v20220109`)
   but needs a GFW API key.
3. **Polygon geometry.** 45.7 % offset-suspect share (§4.5); DETER polygons are drawn to a coarser standard than 10 m embeddings.
4. **Threshold sample floor** missed in MA and TO (1,270 and 183 px); 835–356 events affected.
5. **Congo is not a like-for-like replication**: TMF patches are 8× smaller and model-derived.
6. **H7(a) is not uniformly robust** — the coefficient CI crosses 0 under τ p85, `date_upper` and the ≥ 25 ha size class.

## 7. A negative result worth reporting
`clear_post` predicts non-registration well (AUC **0.729** / **0.712**), but a year-attribution rule
cannot use it: computing `clear_post` requires the event date the rule is inferring. Substituting
the *annual* clear-observation count of the candidate prior year — which **is** available — the
signal collapses (AUC **0.599**, deferred median 34.0 vs direct 35.0 observations) and the fitted
rule reduces misattribution by **0.0 %** [0.0, 0.0] over the naive first-registration rule on a
38,256-event held-out year. **Attribution therefore cannot be repaired from observation supply
alone.** What does work is trivial and worth stating: a two-year acceptance window removes
94–96 % of naive misattribution (3.48 % → 0.12 %).

## 8. Conclusion
Annual embeddings register essentially every clearing they are given a chance to see, defer almost
all of the rest by one year, and truly miss about one in 800. The binding constraint is optical
observation supply, which radar does not substitute for. Users should treat the annual label as a
two-year window and should not expect the embedding to resolve *when* within the year.

## Figures and tables
F1 registration curve · F2 SAR stratification · F3 deferral · F4 optically-late events ·
F5 Congo panel (dating-limited) · F6 offset examples · F7 map plates (2 regions × 5 layers).
T1 event population by state/year · T2 per-state thresholds · T3 centroid-vs-polygon RADD ·
T4 nine robustness variants · T5 offset check and its sensitivity.
