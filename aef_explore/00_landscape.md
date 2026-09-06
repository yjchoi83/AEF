# 00 Landscape — AEF novelty baseline (verified 2026-09-03)

MODE: LIVE (GEE_PROJECT config was empty, but `~/.config/earthengine/credentials` carries
project `alpha-earth-app`; `ee.Initialize` + AEF 1-pixel sample succeeded -> pilots enabled).
ASSUMPTIONS: GEE project = alpha-earth-app; `data/rok/` is EMPTY -> D1 runs with LABELS=FALLBACK
(Dynamic World / WorldCover on the ROK side as noisy labels).

## Verified dataset facts (this session)
- GEE STAC `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`: 64 bands A00-A63, 10 m, unit-norm, images
  ~163,840 m tiles in local UTM. Catalog wording [V]: embeddings "encodes temporal trajectories of
  surface conditions ... over a single **calendar year**"; `system:time_start` = Y-01-01,
  `system:time_end` = (Y+1)-01-01. -> reference labels must be aligned to calendar years;
  PRODES (Aug-Jul) needs re-binning. STAC temporal extent still advertises 2017-01-01..2025-01-01,
  but `filterDate(2025)` returns 11,078 images -> the 2025 layer IS live (2017: 10,562).
- Coverage: terrestrial + shallow water, incl. intertidal/reef; poles limited.

## Verified works beyond PROMPT.md §4.3 (all [V]: DOI or arXiv id retrieved in-session)
| Work | id | gist | bucket |
|---|---|---|---|
| On the foundations of Earth foundation models | 10.1038/s43247-025-03127-x | Comms Earth Env perspective/critique of EO FM evaluation practice | E,F |
| Beyond Accuracy: Calibration of Geospatial FMs and their Sensitivity | arXiv:2608.16614 | calibration/UQ of GFMs incl. AEF | E,F,G |
| How to Embed Matters: Evaluation of EO Embedding Design Choices | OpenAlex arXiv (2026) | design-choice ablation across EO embeddings | E,F |
| From Pixels to Patches: Pooling Strategies for Earth Embeddings | arXiv:2603.02080 | pixel vs patch aggregation of AEF | E |
| Temporal Sensitivity Analysis of Tessera Embeddings | arXiv:2608.27175 | temporal sensitivity, TESSERA (not AEF) | B |
| BEACON: tri-modal contrastive enrichment of AEF embeddings | arXiv:2608.29553 | adds behavioral/semantic modalities to AEF | C |
| AEF-Econ: plug-and-play socioeconomic embeddings from AEF | arXiv:2606.20697 | urban socioeconomic probing | A,C |
| Earth Embeddings Reveal Diverse Urban Signals from Space | arXiv:2604.03456 | urban signal decodability | E |
| Cross-View Urban Sensing: streetscape perception via AEF | arXiv:2608.16310 | AEF + street imagery | C |
| Evaluating AEF Embeddings for Wildfire Susceptibility Mapping | arXiv:2608.12663 | AEF as susceptibility covariates | A,D |
| Above-ground Biomass Estimation with Geospatial FMs | arXiv:2608.04792 | AGB with GFMs | D |
| Foundation-Model Earth Representations for Regional AGB Monitoring | arXiv:2607.27217 | regional AGB monitoring | D,G |
| Is sub-metre resolution necessary for cocoa mapping? | arXiv:2607.08945 | landscape-stratified VHR vs 10 m for cocoa | A,F |
| When Context Compensates for Sparse Event History (AEF point processes) | arXiv:2607.01082 | AEF as context for ST point-process forecasting | C |
| Characterizing Brazilian Atlantic Forest Restoration with AEF | arXiv:2605.05547 | restoration outcome characterization | A,G |
| Subsurface Property Mapping using AEF / subsurface temperature ICL | arXiv:2604.14756, arXiv:2605.16665 | AEF for subsurface targets | D,E |
| Physically Interpretable AEF Embeddings + LLM land-surface intelligence | arXiv:2602.10354 | interpretable dims -> LLM | E |
| Cropland Mapping using Geospatial Embeddings / Senegal groundnut crop type | arXiv:2511.02923, arXiv:2601.16900 | AEF crop mapping, incl. Sahel smallholders | D |
| Embedding-based crop type: comparative examination | 10.1016/j.jag.2026.105531 | IJAEOG crop-type comparison | F |
| Satellite embeddings for boreal standing dead-tree volume | 10.1016/j.ecoinf.2026.104013 | AEF as complementary predictor | D |
| Winter wheat / crop rotation Henan with embeddings | 10.5194/isprs-annals-xi-2-2026-865-2026 | multi-year embeddings, cropping | D |
| Deep Learning Burned Area Mapping with Bi-Temporal Siamese + AEF | arXiv:2509.07852 | bi-temporal AEF change (fire) | B,A |
| Beyond Backscatter: AEF priors for SAR flood segmentation | arXiv:2606.29134 | AEF priors + SAR | D,H |
| Poverty mapping with compact satellite embeddings + GNN | arXiv:2511.01408 | socioeconomic | A |
| Estimating River Water Quality in South Korea using AEF | 10.7780/kjrs.2025.41.5.10 | only ROK AEF paper found; no DPRK AEF work | H,D |
| Coral-reef habitat decodability with satellite embedding fields | 10.31223/x50v35 | decodability study (preprint) | E |
| Atoll island ecosystem mapping with AEF (MDPI, excluded venue) | 10.3390/rs18172964 | GFM vs baselines, atolls | A |
| Aitchison-loss compositional land-cover with geo-embeddings | 10.5194/isprs-archives-l-4-w1-2026-95-2026 | compositional (soft) land cover | E |
| Hokkaido foliage height diversity, GEDI + FM | 10.5194/isprs-archives-l-4-w1-2026-267-2026 | AEF+GEDI structure | D |
| Spatiotemporal cropland reconstruction, Korean Peninsula (MDPI Land) | 10.3390/land15010117 | Korea-wide cropland history, NO AEF, coarse | H |
| Spatial database of planted forests in East Asia | 10.1038/s41597-023-02383-w | includes DPRK planted forest, coarse | H |
| Site index model for six tree species, North Korea | 10.1007/s11676-022-01506-0 | DPRK forest productivity, no EO embeddings | H |

Query log: OpenAlex "AlphaEarth" (608 works), "satellite embedding|AEF" (569), AEF+change/temporal (13),
AEF+transfer/domain-shift (35), DPRK land cover (66); arXiv all:AlphaEarth (42 entries, 2025-07..2026-09),
arXiv "satellite embeddings" (15). Semantic Scholar: HTTP 429 -> skipped [U-source, nothing cited from it].

## Gap list (shared novelty baseline for Stage 1)
G1 Temporal fidelity of the ANNUAL product: no work on within-year event timing, geodesic mixing,
   or detection lag for AEF. TESSERA has arXiv:2608.27175; AEF equivalent is open.
G2 Stable-land inter-annual drift attribution (S1-B gap 2022-24, ERA5/GRACE drought years):
   only blog-level treatment; no journal paper. Calibration paper (2608.16614) is accuracy-side, not drift-side.
G3 Static/climate-input dependence vs cross-region transfer: many single-region evaluations,
   no controlled AEF-vs-TESSERA test of the DEM/ERA5 hypothesis.
G4 Data-denied territory monitoring (DPRK): zero AEF work; existing DPRK EO work is coarse and non-embedding.
G5 Design-based area estimation + UQ on embedding products: calibration studied, area estimation not.
G6 Degradation intensity / secondary-forest age with AEF: AGB and restoration exist, intensity+age open.
G7 Conflict/humanitarian at neighbourhood-annual scale: building-level damage published & weak; grid-level open.
G8 AEF failure modes vs simple spectral baselines: scattered counter-results (Andean AGB, Better Together),
   no systematic multi-target study.
