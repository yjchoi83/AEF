# Stage 1 — Bucket E: representation analysis and critique (2026-09-03)

MODE: LIVE. Lookups used: 4/4 (OpenAlex only; arXiv API returned empty bodies -> not used).
Framing rule respected: GLO-30 DEM, ERA5-Land and GRACE are DIRECT AEF inputs, so every card below is
phrased as **static/climate-input dependence**, never as leakage.

Verified this session (abstracts retrieved via OpenAlex):
- Rahman 2026, `10.1016/j.rsase.2026.102045` [V]: CONUS 2017-2023, 12.1M samples, 64-D vs 26 env vars;
  full space reconstructs 12/26 vars at R2>0.90, **elevation and temperature ~R2=0.97**; dim-variable maps
  survive spatial block CV (mean dR2=0.017) and are temporally stable (inter-year r=0.963).
  Scope limits: one region, static targets, no change detection, no transfer, no drought-year test.
- "What on Earth is AlphaEarth?" 2026, `10.48550/arxiv.2603.16911` [V]: functional/hierarchical roles of dims
  (specialist / low- / mid- / high-generalist); **2-12 of 64 dims reach 98% of baseline land-cover accuracy**
  -> heavy redundancy, and a ready-made handle for targeted dimension ablation. Static classification only.
- "From Pixels to Patches" 2026, `10.48550/arxiv.2603.02080` [V]: EuroSAT-Embed, 11 training-free poolings,
  AEF/OlmoEarth/Tessera; stats/covariance pooling cuts the geographic generalization gap >50% vs mean pooling.
  This is post-hoc *aggregation*, not the encoder's own spatial context -> TE03 stays distinct.
- OpenAlex search for embedding int8/precision effects: 25 hits, none about EO embedding quantization
  (all onboard-inference / YOLO reviews) -> genuine void, but see TE04 kill.
=> Conclusion on the assigned check: dimension-level **decodability is done** (and stronger than expected:
   terrain/temperature near-saturated). What is untouched is the *consequence* side — change detection,
   cross-region transfer, and fair baselines that are given AEF's own ancillary inputs.

| ID | Title (<=12 words) | Region | RQ (1 sentence) | Why AEF (1 sentence) | Reference data (named) | Closest prior work (title, year, [V]/[U]) | N R F A V J Total | PASS/KILL + reason (<=15 words) |
|---|---|---|---|---|---|---|---|---|
| TE01 | S4: Ablating terrain/climate dimensions — in-domain accuracy versus cross-region transfer | Brazil (Amazon/Cerrado) -> Congo Basin; ROK -> DPRK | Does zeroing or orthogonalizing the DEM/ERA5-aligned AEF dimensions cost in-domain accuracy while improving cross-region transfer of a fixed land-cover classifier? | DEM, ERA5-Land and GRACE are direct AEF inputs and their dimensions are already decodable, while TESSERA (Sentinel-1/2 only) supplies a matched no-static-input control model. | MapBiomas (Brazil), LandCoverNet (Africa/S.America, 2018), ESA WorldCover + Dynamic World (ROK/DPRK fallback labels), GLO-30 DEM and ERA5-Land as the ablation targets | Physically interpretable AlphaEarth embeddings enable LLM-based land surface intelligence, 2026, [V]; What on Earth is AlphaEarth?, 2026, [V] | 3 2 2 3 3 3 = 16 | PASS — decodability known, transfer consequence untested; TESSERA gives clean control |
| TE02 | S6: Do drought-year climate anomalies manufacture embedding change on stable land? | Horn of Africa + Southern Africa (2019, 2023-24 droughts), Iberia 2022; CONUS control | Does angular embedding change on independently-verified stable pixels scale with ERA5-Land/GRACE anomaly magnitude, and does projecting out climate-aligned dimensions reduce change false-positive rate at fixed recall? | Change with AEF is scored as arccos of a dot product over an embedding whose inputs include monthly ERA5-Land and GRACE, so a climate anomaly can enter the change signal without any land-cover change. | Hansen GFC lossyear (no-loss = stable), JRC TMF stable classes, MapBiomas stable classes, ERA5-Land (SPEI-style anomalies), GRACE TWS, per-pixel S1/S2/Landsat observation counts | Practitioner cosine-drift reports vs MapBiomas (blogs, Apr 2026), [U]; Beyond Accuracy: Calibration of Geospatial FMs, 2026, [V] | 2 3 3 3 3 2 = 16 | PASS — drought false alerts hit real alert users; overlaps bucket B S2 |
| TE03 | S6: Encoder spatial context caps sub-1-ha smallholder and boundary accuracy | Senegal/Mali groundnut belt + Ethiopian highlands; Iowa and France as large-field controls | How steeply does AEF pixel-embedding purity decay with distance to a parcel boundary and with shrinking field size, and does that decay explain the smallholder accuracy ceiling relative to a 10 m Sentinel-2 composite? | AEF is delivered as a 10 m pixel product from a spatial encoder whose effective receptive field is undocumented, so boundary mixing is a property of the representation, not of the label set. | MAFRA FarmMap (ROK parcels), France RPG parcels, WorldCereal, LandCoverNet, Google Open Buildings (urban edge control) | From Pixels to Patches: Pooling Strategies for Earth Embeddings, 2026, [V]; Cropland mapping / Senegal groundnut crop type with geospatial embeddings, 2026, [V] | 2 3 2 3 3 2 = 15 | PASS — parcel geometry makes it falsifiable; smallholder ceiling is policy-relevant |
| TE04 | int8 quantization of the public COG product versus float GEE bands | Global sample: Amazon, Congo, ROK tiles | Does int8 quantization/dequantization of `gs://alphaearth_foundations` COGs shift angular-change magnitudes enough to flip near-threshold change decisions relative to the float GEE bands? | The two distribution channels of the same AEF product differ only in precision, so any decision flip is attributable to quantization alone. | GEE `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL` float bands vs public GCS COGs; Hansen GFC and RADD alerts as the decision task | none found (OpenAlex: 25 hits, none on EO embedding quantization), [V-negative] | 2 1 3 1 2 1 = 10 | KILL — engineering note, no stakeholder; fold in as a TE02 control |
| TE05 | Cross-model and cross-year embedding disagreement as per-pixel uncertainty | Amazon + Congo Basin | Does AEF-vs-TESSERA and leave-one-year-out disagreement predict downstream classification error better than classifier confidence, and does it tighten deforestation-area confidence intervals? | Disagreement is computable from two public pixel-embedding products over identical geometry with no retraining. | Hansen GFC, JRC TMF, RADD alerts; TESSERA 2024 global layer; stratified VHR interpretation for area estimation | Beyond Accuracy: Calibration of Geospatial FMs and their Sensitivity, 2026, [V]; Better Together: complementarity of AEF/TESSERA/GeoCLIP/SatCLIP, 2026, [V] | 1 2 2 1 2 2 = 10 | KILL — hard rule A<=1 and N<=1; calibration paper already owns this |
| TE06 | S6: Is AEF's margin just terrain and climate? Static-covariate-controlled baselines | CONUS + Tropical Andes + Congo Basin, 5-6 targets | Across thematic and biophysical targets, how much of AEF's reported margin over a Sentinel-2 composite baseline disappears once that baseline is given AEF's own ancillary inputs (GLO-30 DEM + ERA5-Land)? | Every published AEF-beats-composite claim compares a representation that has seen terrain and climate against a baseline that has not, and Rahman 2026 shows AEF encodes elevation at R2~0.97. | MapBiomas, Hansen GFC, GEDI L4A biomass, ETH/Meta canopy height, ESA WorldCover, LandCoverNet; GLO-30 DEM + ERA5-Land as baseline covariates | Harvesting AlphaEarth: benchmarking the GFM for agricultural downstream tasks, 2026, [V]; On the foundations of Earth foundation models, 2025, [V]; Lucero et al. Andean AGB counter-result, [U] | 3 2 3 3 3 3 = 17 | PASS — cheap, decisive, reframes every published AEF-versus-baseline comparison |

## Notes on the strongest surviving gap
1. TE06 is the strongest: no verified study equips the spectral baseline with DEM+ERA5-Land, so the field's
   headline comparison is confounded by ancillary-data access rather than representation quality.
2. Reviewer 2 for TE06: "you crippled AEF." Preempt by keeping AEF untouched and only *strengthening* the
   baseline, reporting per-target margins with spatial-block fold spread, and adding TE01's dim ablation as
   the mechanistic corroboration (both should be one paper if Stage 2 confirms).
3. Rahman 2026's R2~0.97 for elevation is the load-bearing verified premise for TE01/TE06; it is CONUS-only,
   so Stage 2 must re-check decodability magnitude in Congo/DPRK before claiming generality.
4. TE02 collides with seed S2 (bucket B drift attribution): keep TE02 only if it owns the *dimension-level*
   attribution plus the mitigation rule, and cede pure observation-count drift decomposition to bucket B.
5. Stakeholders named, per §3.6: Congo Basin/DRC national forest monitoring reusing Brazil-trained models
   (TE01), RADD/GLAD alert consumers and FAO GIEWS drought reporting (TE02), and WorldCereal/CGIAR
   smallholder crop-area users (TE03).
