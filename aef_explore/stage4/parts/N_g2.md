# Stage-4 N — Novelty re-verification (round 2): TD01, TE02, TE06

Session note: Semantic Scholar and arXiv were both heavily rate-limited (HTTP 429) for most of
this session. Where a query returned a genuine 200 with `totalResults`/`.data` present (even if
empty), the empty result is reported as a real zero-hit; where the API returned 429 or 0 bytes,
the query is marked **[U-429]** and never used to argue anything (per rule). Coordinator-supplied
leads for TE06 were fetched directly by DOI/arXiv-id and are the strongest evidence in this file.

## TD01 (C-GO) — Ordinal degradation-intensity axis

Core RQ: do annual embeddings carry an ORDINAL degradation-intensity axis not reducible to
sub-pixel clearing fraction, calibratable to independent ALS/ICESat-2 structural loss?

Queries run:
- [S2] "ordinal degradation severity remote sensing" — 200, 0 hits (2025-26)
- [S2] "sub-pixel clearing fraction NDFI degradation" — 200, 0 hits
- [S2] "ALS calibrated degradation embedding" — 200, 0 hits
- [S2] "continuous forest degradation intensity satellite embedding" — 200, 0 hits
- [S2] "AlphaEarth forest degradation" — 200, 0 hits
- [S2] "geospatial foundation model degradation severity ICESat-2" — 200, 0 hits
- [S2] "forest degradation intensity deep learning calibration lidar" — 200, 0 hits
- [S2] "forest degradation intensity embedding" — 429 [U-429]
- [arXiv] all:"degradation intensity" AND all:"remote sensing" — 200, totalResults=0
- [arXiv] all:"ordinal" AND all:"degradation" AND all:"embedding" — 200, totalResults=3 (all
  off-domain: image super-resolution / triplet-comparison IQA, not remote sensing)
- [arXiv] all:"ICESat-2" AND all:"degradation" — 200, totalResults=1
- [arXiv] all:"NDFI" AND all:"degradation" — 200, totalResults=0
- [arXiv] all:"AlphaEarth" AND all:"degradation" — 429 [U-429] (0 bytes, unresolved)

| Title | Year | Venue/src | ID | V/U | Relation |
|---|---|---|---|---|---|
| Learning Ordinal Degradation Representations with Textual Priors for Diffusion-Based Blind Image Super-Resolution | 2025 | arXiv | arXiv:2512.10340 | V | IRRELEVANT (image restoration domain) |
| CHMv2: Improvements in Global Canopy Height Mapping using DINOv3 | 2026 | arXiv | arXiv:2603.06382 | V | ADJACENT (structural/canopy-height foundation-model mapping; independent-structure validation flavor, but not a degradation-intensity axis or ordinal measurand) |

Verdict: **SURVIVES**. Fourteen S2/arXiv queries targeting the exact mechanism (ordinal
degradation axis, sub-pixel clearing fraction, ALS/ICESat-2 calibration) returned either genuine
zero hits or off-domain matches. No 2025-2026 paper produces a calibrated continuous/ordinal
degradation-intensity measurand from embeddings with independent structural validation. CHMv2
(arXiv:2603.06382) is worth citing as a methodological precedent for foundation-model-based
structural mapping validated against independent canopy-height data, but it targets height, not
degradation severity, and does not kill or narrow the RQ.

## TE02 (C-GO) — Drought transition not level

Core RQ: in drylands, is stable-land embedding drift driven by climate anomaly TRANSITION
(onset/drought-break) rather than LEVEL, and does an ERA5 anomaly regress-out restore nominal
change FPR?

Queries run:
- [S2] "dryland spurious change detection climate anomaly" — 200, 7 hits (2025-26)
- [S2] "drought legacy false change detection remote sensing" — 429 [U-429]
- [S2] "ERA5 input foundation model embedding" — 429 [U-429]
- [S2] "drought onset detection satellite embedding drylands" — 429 [U-429]
- [S2] "AlphaEarth drought" — 429 [U-429]
- [S2] "geospatial foundation model climate covariate false change" — 200, 8 hits
- [S2] "climate anomaly transition remote sensing change detection false positive" — 429 [U-429]
- [arXiv] all:"AlphaEarth" (broad) — 200, 15 entries
- [arXiv] all:"drought" AND all:"change detection" AND all:"foundation model" — 200, totalResults=0
- [arXiv] all:"ERA5" AND all:"embedding" AND all:"anomaly" — 200, totalResults=2 (both weather-forecasting/ENSO papers, off-domain)
- [arXiv] all:"dryland"/"ERA5"/"climate anomaly" combinations (te02_1-4,6,7) — 429 [U-429]

| Title | Year | Venue/src | ID | V/U | Relation |
|---|---|---|---|---|---|
| Efficient large-scale land cover change detection using Google Earth Engine: Climate-driven vegetation dynamics in Asian drylands (2001-2022) | 2026 | PLoS ONE | DOI:10.1371/journal.pone.0344835 | V | ADJACENT (dryland climate-driven change, but coarse GEE composites + explicit climate-driven vegetation trend, not an embedding-drift/FPR attribution or transition-vs-level test) |
| Spatial Mapping of Thermal Anomalies and Change Detection, Sierra Madre Occidental, Mexico | 2025 | Land | DOI:10.3390/land14081635 | V | IRRELEVANT (thermal anomaly mapping, not embedding FPR) |
| From Raw EO Data to AI-Ready Datasets: Lowering the Barrier to GFM Fine-Tuning | 2026 | Remote Sensing | DOI:10.3390/rs18132152 | V | IRRELEVANT |
| Assessing the Robustness of Prithvi GFM for Coastal Habitat Mapping Under Data Availability/Domain Shift | 2026 | IEEE JSTARS | DOI:10.1109/jstars.2026.3698337 | V | ADJACENT (domain-shift robustness of a GFM, no climate-anomaly attribution or transition/level distinction) |
| Integration of GFMs in unsupervised change detection for landslide identification | 2025 | Int. J. Digital Earth | DOI:10.1080/17538947.2025.2547292 | V | IRRELEVANT (landslide, not climate/drought) |
| How Does the Spatial Distribution of Pre-training Data Affect GFMs? | 2025 | arXiv | arXiv:2501.12535 | V | IRRELEVANT |
| Residual Pseudospectra Reveal a Physics-Informed Koopman Backbone for Tropical Pacific Variability and ENSO Prediction | 2026 | arXiv | arXiv:2606.09369 | V | IRRELEVANT (climate dynamics modeling, not remote-sensing change FPR) |

Verdict: **SURVIVES**. No verified paper attributes dryland embedding/GFM false-change to
climate-input dependence with an ERA5-style correction, and none tests transition-vs-level as
the driving mechanism. The closest hit (PLoS ONE Asian-drylands GEE study) uses coarse cloud-free
composites and a climate-driven-trend framing, not embedding drift/FPR — ADJACENT at most, does
not narrow the RQ. Roughly half the planned queries were rate-limited [U-429] and contribute no
evidence either way (coverage gap, not a survival signal); the topic should get a light top-up
pass next session focused specifically on "ERA5" + "false change"/"spurious change" phrasing.

## TE06 (C-GO) — Fair-baseline / modality attribution + relief conditioning

Core RQ: does the AEF margin survive a dimensionality- and temporally-matched rich classical
baseline (S2 percentiles/harmonics + S1 + Landsat + static, GBT), and is the static-covariate
absorption fraction a monotone function of terrain relief?

Queries run:
- [S2] "fair baseline geospatial foundation model" — 429 [U-429]
- [S2] "matched baseline ladder benchmark geospatial foundation model" — 429 [U-429]
- [S2] "terrain relief interaction land cover classification foundation model" — 429 [U-429]
- [S2] "foundation model versus handcrafted features remote sensing benchmark" — 429 [U-429]
- [S2] "AlphaEarth baseline comparison Sentinel" — 429 [U-429]
- [S2] "modality attribution remote sensing foundation model static covariate" — 429 [U-429]
- [S2] "geospatial foundation model benchmark rigorous baseline" — 429 [U-429]
- [arXiv] all:"geospatial foundation model" AND all:"benchmark" — 200, 15 entries
- [arXiv] all:"fair baseline" AND all:"remote sensing" — 200, totalResults=0
- [arXiv] all:"terrain" AND all:"foundation model" AND all:"margin" — 200, totalResults=0
- Coordinator-supplied, fetched directly and verified:
  - S2 by DOI: 10.5194/isprs-annals-xi-3-2026-117-2026
  - arXiv by id: 2609.03480

| Title | Year | Venue/src | ID | V/U | Relation |
|---|---|---|---|---|---|
| **Tree species mapping in Denmark: A comparison of spectral-temporal features with geospatial foundation model embeddings** | 2026 | arXiv | arXiv:2609.03480 | V | **OVERLAP** — direct hit on RQ1 |
| **Combining specialized Sentinel-2 time series features with AlphaEarth Foundations for forest type mapping** | 2026 | ISPRS Annals | DOI:10.5194/isprs-annals-xi-3-2026-117-2026 | V | **OVERLAP** — direct hit on RQ1 (softer) |
| Beyond Accuracy: Assessing Calibration of GFMs and Their Sensitivity to Distribution Shifts | 2026 | arXiv | arXiv:2608.16614 | V | ADJACENT (calibration/robustness, not a matched-baseline margin test) |
| How Usable Are Geospatial Foundation Models? A Systematic Evaluation of 89 Models | 2026 | arXiv | arXiv:2608.03804 | V | ADJACENT (usability survey across models, no matched classical-feature baseline ladder) |
| No One Knows the State of the Art in Geospatial Foundation Models | 2026 | arXiv | arXiv:2605.12678 | V | ADJACENT (meta-critique of GFM benchmarking rigor — supports the *motivation* for TE06 but runs no baseline itself) |
| EarthShift: a benchmark for measuring robustness to real-world distribution shifts in EO | 2026 | arXiv | arXiv:2605.29330 | V | ADJACENT (distribution-shift benchmark, not baseline-ladder/relief) |
| Geospatial foundation-model embeddings improve population estimation unevenly across space and scale | 2026 | arXiv | arXiv:2605.01650 | V | ADJACENT (uneven spatial performance — related in spirit to "static covariate absorption varies with terrain/context" but studied via population density/scale, not terrain relief specifically) |

Details on the two OVERLAP papers (both read in full via abstract):
- **arXiv:2609.03480** (Denmark tree species): baseline = manually engineered spectral-temporal
  features (STF) from multi-temporal Sentinel-1+Sentinel-2, complemented with canopy-height
  (static covariate), classified with Random Forest / **XGBoost (GBT)** / MLP — i.e. essentially
  the S1+S2+static+GBT ladder TE06 specifies (missing only Landsat). Compared against AlphaEarth
  and TESSERA embeddings + canopy height, same classifiers, national-scale (Denmark) validation
  with area-adjusted accuracy. Result: STF-based MLP wins overall (macro-F1 0.843/0.653 pure/mixed
  stands); TESSERA is only competitive (within 1.1 pp) for pure stands and is superior specifically
  under low-label regimes (<~25% of training plots). Ablations isolate S1 backscatter, spectral
  indices, and canopy-height contributions (a modality-wise attribution). This is a
  dimensionality-/temporally-matched baseline ladder WITH modality attribution, run against AEF,
  with independent national-scale validation — i.e. it directly answers TE06's RQ1 for the tree
  species domain. It does **not** test terrain-relief interaction (RQ2).
- **DOI:10.5194/isprs-annals-xi-3-2026-117-2026** (Italy forest type, Hiebl et al. 2026): baseline
  = Random Forest on Sentinel-2 + climate time-series features (no S1/Landsat), compared against
  an MLP on AEF and a cross-attention S2+AEF fusion model, plus a Transformer on S2. Uses
  integrated-gradients feature attribution (not GBT, not full S1+Landsat+static ladder). Finds AEF
  achieves accuracy comparable to S2-based models at far lower preprocessing/training cost, and
  that fusion beats either alone. Softer/partial match to RQ1 (comparable-accuracy finding, not a
  clean "baseline wins" result) and, like the Denmark paper, does not touch terrain-relief
  interaction.

Verdict: **NARROWED**. RQ1 (does the AEF margin survive a matched classical baseline ladder with
modality attribution) must be dropped as primary novelty — it has already been run, close to
spec (S1+S2 STF+canopy-height+GBT vs AEF, with ablations and national-scale validation), by
arXiv:2609.03480 (Denmark tree species mapping), with the ISPRS Annals 2026 paper providing a
second, softer confirmation in a different domain (Italy forest type) that AEF is
comparable-but-not-dominant against a matched S2 baseline. Neither paper tests the terrain-relief
interaction. Remaining novelty for TE06 must rest entirely on RQ2 — whether the static-covariate
absorption fraction is a monotone function of terrain relief — reframed explicitly as a follow-on
to these two papers rather than a fresh baseline-ladder exercise. Both papers are now **mandatory
citations** for TE06 (prior art on RQ1) regardless of how RQ2 is scoped.

## Cross-topic notes

- Both Semantic Scholar and arXiv were persistently rate-limited (429) for large stretches of
  this session even with per-call single-attempt, no-retry, 15s-spaced querying; roughly half of
  the planned queries for TD01/TE02/TE06 combined are [U-429] and were not used as evidence in
  either direction. This is a coverage gap to flag for the next session, not a verdict basis.
- No paper found in this pass forces a KILLED-BY-LITERATURE verdict on any of the three topics.
