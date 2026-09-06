# Stage 1 — Bucket H (defense, security, humanitarian). Screened 2026-09-03

MODE=LIVE (GEE project `alpha-earth-app`). ASSUMPTIONS: `data/rok/` is EMPTY -> TH01 is scored with
`LABELS=FALLBACK` (Dynamic World + ESA WorldCover on the ROK side as noisy labels; ROK MoE
land-cover / KFS 임상도 / MAFRA 팜맵 would raise F and V if downloaded later).
All cards are strategic-scale, public-data, civilian-protection/transparency framed. No targeting,
no force/vehicle/individual tracking, no real-time tactical use, no weapon-system or military-facility
identification, no evasion support — per §5-H out-of-scope list.
Lookups used: 4/4 (OpenAlex conflict-cropland-abandonment 2023+; OpenAlex refugee/IDP-camp EO 2024+;
arXiv UAV cross-view geo-localization; OpenAlex DPRK land-use + foundation model 2024+, 193 hits, zero relevant).
Novelty baseline: `00_landscape.md` gaps G1-G8. Confirmed again this session: **no AEF/embedding work on
DPRK or any data-denied territory** (G4 intact).

| ID | Title (<=12 words) | Region | RQ (1 sentence) | Why AEF (1 sentence) | Reference data (named) | Closest prior work (title, year, [V]/[U]) | N R F A V J Total | PASS/KILL + reason (<=15 words) |
|---|---|---|---|---|---|---|---|---|
| TH01 | D1: DPRK annual land-use monitoring under zero ground truth | DPRK + ROK border provinces (Korean Peninsula) | Can annual AEF embeddings measure DPRK forest recovery vs hillside-farming expansion 2017-2025, and transfer across the DMZ, when no in-situ label exists? | AEF gives a label-free 10 m annual trajectory whose ROK->DPRK transfer gap isolates static/climate-input dependence, and whose similarity structure supports design-based stratification where no map exists. | Dynamic World + ESA WorldCover (ROK-side noisy labels, LABELS=FALLBACK); later ROK MoE land-cover, KFS 임상도, MAFRA 팜맵; Hansen GFC, GHSL, JRC Surface Water; 38 North / Beyond Parallel dated project completions; stratified VHR interpretation (Google Earth historical) | Spatiotemporal cropland reconstruction of the Korean Peninsula, 2026 [V] (10.3390/land15010117; coarse, no embeddings); Site index model for six tree species, North Korea, 2022 [V] (10.1007/s11676-022-01506-0) | 3 3 2 2 2 3 = 15 | PASS (MUST_EVALUATE) — bypasses kills; G4 open, validation design is the novelty |
| TH02 | D2: Conflict cropland abandonment vs ACLED event density | Ukraine front line, Sudan, Tigray, central Sahel | Does annual AEF cropland status show a dose-response to ACLED event density and front-line distance, transferably across four unrelated conflicts? | A single annual embedding encodes full-season cropping phenology, so a cropland-status probe trained on one pre-war baseline can be applied where no in-country labels exist. | WorldCereal, ACLED event points, national/FAO-GIEWS crop statistics, Dynamic World crops, S2 composite baseline | Monitoring cropland cultivation, abandonment, fallowing and recultivation dynamics, 2025 [V] (10.1016/j.srs.2025.100326); Revealing abandoned cropland in Ukraine from dual-period change, 2025 [V] (10.1038/s41598-025-89556-2) | 2 3 2 2 3 2 = 14 | PASS — abandonment mapped per-conflict, no embedding-based multi-conflict dose-response |
| TH03 | D3: Neighbourhood-scale conflict damage density and reconstruction trajectories | Mariupol, Gaza, Khartoum | Do annual embedding trajectories recover grid-level damage fraction and, more importantly, multi-year reconstruction that building-level bi-temporal methods cannot express? | AEF's annual cadence is a poor fit for damage timing but a natural fit for multi-year recovery, and 100-500 m aggregation should beat the weak per-building AEF signal (AUC ~0.59). | UNOSAT/UNITAR damage assessments and Copernicus EMS activations aggregated to grid; Google Open Buildings 2.5D Temporal; GHSL built-up; OSM/HOT reconstruction edits | Building-level damage mapping fusing AEF embedding EMD with Sentinel-1 PWTT, 7 Ukrainian cities, 2026 [V] (§4.3 pre-verified; AEF alone AUC ~0.59, fusion ~0.68) | 2 3 3 2 3 2 = 15 | PASS — grid-annual reconstruction measurand differs from published building-level damage |
| TH04 | D4: Displacement-site emergence and growth from embedding similarity | Sudan-Chad border, eastern DRC, Cox's Bazar | Can similarity search seeded from ~50 known camp pixels find newly emerged displacement sites and reconstruct their annual growth curves? | Documented AEF similarity retrieval from tens of labels offers a label-efficient discovery mode for a class with almost no training data anywhere. | UNHCR Operational Data Portal / HDX camp footprints and establishment dates, HOT/OSM building footprints, GHSL built-up, WorldPop | From Meta SAM to ArcGIS: segmentation methods for monitoring refugee settlements, 2025 [V] (10.3390/geomatics5020022; single-site, VHR, no embeddings) | 2 3 2 2 2 2 = 13 | PASS — camp discovery + growth open; tent-scale 10 m detectability is the risk |
| TH05 | D5: Military land use and DMZ/CCZ wildfire recovery, Korea | ROK border region: DMZ, CCZ, training ranges | Does post-fire and post-disturbance recovery differ between the unmanaged DMZ/CCZ and managed ROK forest, and does AEF add anything over dNBR/NDVI recovery curves? | The DMZ is an access-denied, unmanaged reference ecosystem where AEF's SAR+structure inputs may separate natural regeneration from KFS replanting better than optical indices alone. | KFS wildfire records, MODIS/VIIRS burned area, KFS 임상도, ROK MoE land-cover, GEDI/ETH canopy height, VHR visual check | Evaluating AEF Embeddings for Wildfire Susceptibility Mapping, 2026 [V] (arXiv:2608.12663); Bi-Temporal Siamese burned-area mapping with AEF, 2025 [V] (arXiv:2509.07852) | 2 2 3 1 3 2 = 13 | PASS (borderline) — strong validation, weak AEF advantage vs spectral recovery indices |
| TH06 | D6: Dual-use GNSS-denied coarse localisation from AEF reference map | Public cross-view datasets (global) | Can compact AEF embeddings serve as a global reference map for coarse UAV localisation when GNSS is denied? | AEF is compact and global, which is a storage convenience rather than a representational advantage for cross-view matching. | University-1652 / SUES-200 / public cross-view benchmarks; AEF annual mosaics | ReLATE: Reliability-Guided Evidence Fusion for UAV-Satellite Cross-View Geo-Localization, 2026 [V] (arXiv:2607.25524); OffNadirLoc benchmark, 2026 [V] (arXiv:2607.19951) | 1 2 2 1 2 1 = 9 | KILL — no gap confirmed; crowded 2026 field; A<=1 and N<=1 hard kill |

## Ethics / data-provenance notes (one per card)

- TH01: Land-use classes only (forest, cropland, built-up, water); no facility identification, no
  named-installation analysis; all inputs public (AEF CC-BY, GEE products, 38 North / Beyond Parallel
  open reports, Google Earth historical imagery); rationale = food security, flood risk and inter-Korean
  forestry cooperation. Dual-use flag: YES — DPRK monitoring is inherently sensitive; mitigate by
  publishing aggregated area estimates with CIs, never per-site interpretation of non-civilian sites,
  and by reporting VHR interpretation protocol and inter-interpreter agreement instead of raw chips.
- TH02: ACLED is licensed for academic use and reported only as aggregated event density; results are
  district-level food-security indicators, never farm-level or party-attributed. Dual-use flag: LOW —
  abandonment maps could in principle inform land seizure; publish at admin-2 aggregation.
- TH03: Uses only already-published UNOSAT/Copernicus EMS damage assessments; outputs are neighbourhood
  damage-and-recovery fractions for reconstruction planning, never building-level status of identifiable
  homes, and never near-real-time. Dual-use flag: YES — damage maps have battle-damage-assessment value;
  the annual cadence and grid aggregation make tactical use infeasible, and that constraint is stated.
- TH04: Camp footprints come from UNHCR/HDX/HOT public releases; outputs are site-level extent and
  growth, never population enumeration, ethnicity, or movement tracking of individuals. Dual-use flag:
  YES — displacement-site locations can expose vulnerable populations; report only sites already public
  in UNHCR/HDX, and withhold coordinates of any newly detected candidate site pending OCHA/UNHCR contact.
- TH05: Fire scars and vegetation recovery only; training-range footprints are treated as land-cover
  disturbance polygons with no unit, activity or facility attribution; KFS wildfire records are public.
  Dual-use flag: LOW.
- TH06: Killed. Even in the civil disaster-response framing, GNSS-denied localisation is navigation
  support with direct military transfer; killing it on novelty grounds also removes the ethical exposure.

## Which G-gaps the PASS candidates attack

G4 (data-denied territory) is attacked head-on by TH01, which additionally probes G3 (ROK->DPRK as a
management discontinuity without a climate/DEM discontinuity), G5 (design-based area estimation with CIs
under zero ground truth) and G1 (detection lag at dated state projects).
G7 (conflict/humanitarian at neighbourhood-annual scale) is attacked by TH03 (grid damage density plus a
new reconstruction measurand), TH02 (annual cropland status vs ACLED dose-response) and TH04 (camp
emergence and growth via similarity retrieval) — all three sit above the published building-level work.
G8 (AEF failure modes vs simple spectral baselines) is attacked by TH05 (AEF vs dNBR/NDVI recovery) and
secondarily by TH02's S2-composite label-efficiency comparison; TH05 also touches G2 (drift on stable,
unmanaged land inside the DMZ, where no management confound exists).
