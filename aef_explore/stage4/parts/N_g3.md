## TA02 — Stand-age ceiling

Queries run:
- [S2] "secondary forest stand age mapping saturation"
- [S2] "AlphaEarth Foundations embedding field model"
- [S2] "regrowth age embedding regression remote sensing" (429, no data returned)
- [S2] "AlphaEarth Foundations mapping" (429, no data returned)
- [S2] "stand age saturation remote sensing forest growth curve" (429, no data returned)
- [arXiv] all:"secondary forest" AND all:"stand age"
- [arXiv] all:regrowth OR all:age AND all:embedding OR all:regression
- [arXiv] all:"AlphaEarth"
- [arXiv] all:geospatial OR all:foundation OR all:model AND all:regression AND all:age
- [arXiv] all:"forest age" AND all:"deep learning" (0 hits)
- [arXiv] all:"canopy height" AND all:"forest age" (0 hits)
- [arXiv] all:"stand age" AND all:saturation (0 hits)
- [arXiv] all:"forest regrowth" AND all:embedding (0 hits)
- [arXiv] all:"forest age" AND all:embedding (0 hits)
- [arXiv] all:"secondary forest" AND all:"time series" AND all:age (0 hits)
- [arXiv] all:"foundation model" AND all:"forest age" (0 hits)
- [arXiv] all:"canopy height" AND all:"secondary forest" (0 hits)

Semantic Scholar was intermittently rate-limited (429) despite backoff; the queries above that returned 429 are recorded but contributed no data (not fabricated). Two S2 queries and four arXiv queries returned usable data.

| Title | Year | Venue | ID | V/U | Relation |
|---|---|---|---|---|---|
| AlphaEarth Foundations: An embedding field model for accurate and efficient global mapping from sparse label data | 2025 | arXiv | arXiv:2507.22291 / DOI:10.48550/arXiv.2507.22291 | V | MANDATORY-CITE (base embedding paper) |
| Pixel-Based Mapping of Rubber Plantation Age at Annual Resolution Using Supervised Learning for Forest Inventory and Monitoring | 2025 | Forests | DOI:10.3390/f16040672 | V | ADJACENT (plantation age via ML, not embedding-based, no saturation/ceiling analysis, no nonlinear/ordinal-head framing) |
| Changes in stand structure and tree species diversity by forest age on ridges and in valleys of a subtropical secondary forest, Amami Ohshima Island | 2025 | Journal of Forest Research | DOI:10.1080/13416979.2025.2548096 | V | IRRELEVANT (field ecology, not RS regression) |
| Assessing the Utility of Satellite Embedding Features for Biomass Prediction in Subtropical Forests with Machine Learning | 2026 | Remote Sensing | DOI:10.3390/rs18030436 | V | ADJACENT (embedding→biomass regression, not age) |
| A new AI paradigm for groundwater level prediction: integrating the AlphaEarth foundations model in the Leizhou Peninsula | 2026 | Frontiers in Earth Science | DOI:10.3389/feart.2026.1790934 | V | IRRELEVANT |
| Machine Learning for Urban Air Quality Prediction Using Google AlphaEarth Foundations Satellite Embeddings: Quito, Ecuador | 2025 | Remote Sensing | DOI:10.3390/rs17203472 | V | IRRELEVANT |
| Advancing Mangrove Classification and Biomass Estimation in the Colombian Pacific Through Google AlphaEarth Foundations and ML | 2026 | Computers | DOI:10.3390/computers15070414 | V | ADJACENT (biomass/classification, not age) |
| Tree species mapping in Denmark: A comparison of spectral-temporal features with geospatial foundation model embeddings | 2026 | arXiv | arXiv:2609.03480 | V | ADJACENT (species mapping, not age) |
| BEACON: Behavioral and Semantic Enrichment of AlphaEarth Embeddings through Tri-Modal Contrastive Learning | 2026 | arXiv | arXiv:2608.29553 | V | IRRELEVANT |
| Above-ground Biomass Estimation with Geospatial Foundation Models | 2026 | arXiv | arXiv:2608.04792 | V | ADJACENT (embedding regression to structural target, methodologically related but target is biomass not age/saturation) |
| Biomazon: A Multimodal Dataset for 3D Forest Structure and Biomass Modeling in the Amazon Basin | 2026 | arXiv | arXiv:2606.05368 | V | ADJACENT (potential independent structural reference dataset — worth checking as validation source, not a competing age-ceiling study) |
| Evaluating AlphaEarth Foundations Embeddings for Wildfire Susceptibility Mapping | 2026 | arXiv | arXiv:2608.12663 | V | IRRELEVANT |

Verdict: SURVIVES. No verified 2025-2026 paper addresses the core RQ — bounding the age ceiling of embedding-based secondary-forest regrowth-age regression using nonlinear/ordinal heads plus an independent non-Landsat structural reference. All narrow queries directly targeting "stand age saturation," "forest age + embedding," "forest regrowth + embedding," and "canopy height + forest age" combinations returned zero 2025-2026 hits on arXiv, and Semantic Scholar's closest hits are either plantation-age ML (no saturation/ceiling framing, no embeddings) or AlphaEarth-embedding regression papers targeting biomass/species/other variables, not age. The AlphaEarth Foundations paper itself (arXiv:2507.22291) [V] is a mandatory citation as the base embedding source. Above-ground Biomass Estimation with Geospatial Foundation Models (arXiv:2608.04792) [V] and the Biomazon dataset (arXiv:2606.05368) [V] are worth citing as methodological/data precedent (embedding→structural-target regression; independent 3D structure reference) but neither addresses age saturation. No kill threat identified; topic remains open, pending confirmation that no non-indexed 2025-2026 preprint (rate-limiting prevented full S2 coverage) addresses this exact mechanism.
## TA04 — Label efficiency for ASGM

Queries run:
- Semantic Scholar: "artisanal small-scale gold mining detection few labels"; "label efficiency foundation model embedding remote sensing"; "galamsey mining Sentinel-2 detection"; "negative transfer cross-region mining detection"; "artisanal mining deep learning satellite Amazon"; "AlphaEarth Foundations mining"; "geospatial foundation model label efficiency transfer learning"; "small-scale mining detection Sentinel-2 machine learning Africa"
- arXiv: "artisanal gold mining detection satellite"; "label efficiency foundation model remote sensing"; "galamsey mining detection Sentinel" (all returned 0 results; further arXiv queries were abandoned after persistent 429 rate-limiting from export.arxiv.org — the 3 that did complete returned zero hits, consistent with a genuinely thin literature niche rather than a query-syntax failure, since the same terms returned real hits on Semantic Scholar)

| Title | Year | Venue | ID | V/U | Relation |
|---|---|---|---|---|---|
| A Sentinel-2 Image Dataset for Mining Detection Across Mining Proportion Ranges in the Brazilian Legal Amazon | 2026 | WCAMA 2026 | DOI:10.5753/wcama.2026.22440 | V | ADJACENT (dataset paper, no label-efficiency/embedding comparison) |
| Using High-Resolution Satellite Imagery and Deep Learning to Map Artisanal Mining Spatial Extent in the DRC | 2025 | Remote Sensing | DOI:10.3390/rs17244057 | V | ADJACENT (ASGM detection via DL, no embedding-vs-baseline label-efficiency ratio, no cross-region transfer test) |
| Multi-modal deep learning approaches to semantic segmentation of mining footprints with multispectral satellite imagery | 2025 | Remote Sensing of Environment | DOI:10.1016/j.rse.2024.114584 | V | ADJACENT (mining segmentation, not ASGM-specific label efficiency/transfer) |
| Deep Learning-Based Violence Detection for Surveillance of Artisanal Gold Mining Sites in Senegal | 2025 | ICNGN 2025 | DOI:10.1109/ICNGN67480.2025.11413701 | V | IRRELEVANT (violence detection, not mining footprint detection) |
| Monitoring mining-induced subsidence from satellite imagery using transformer-based deep learning | 2025 | J. Environmental Management | DOI:10.1016/j.jenvman.2025.127536 | V | IRRELEVANT (subsidence, not ASGM footprint) |
| Landscape controls on water availability limit revegetation after artisanal gold mining in the Peruvian Amazon | 2025 | Communications Earth & Environment | DOI:10.1038/s43247-025-02332-y | V | IRRELEVANT (ecology, not detection method) |
| Scalable Geospatial Data Generation Using AlphaEarth Foundations Model | 2025 | arXiv | arXiv:2508.11739 | V | MANDATORY-CITE (uses AEF embeddings for data generation; establishes AEF-adjacent tooling but not mining/label-efficiency) |
| Slum Detection and Density Mapping with AlphaEarth Foundations: A Representation Learning Evaluation Across 12 Global Cities | 2026 | arXiv | arXiv:2605.10029 | V | MANDATORY-CITE (closest structural analog found: AEF representation-learning evaluation across many sites/cities for a socioeconomic land-cover task — worth citing as a precedent for "AEF representation learning for a detection task across many regions," but is slums not mining, and does not measure label-efficiency parity ratios vs S2 baseline nor transfer asymmetry) |
| Combining specialized Sentinel-2 time series features with AlphaEarth Foundations for forest type mapping | 2026 | ISPRS Annals | DOI:10.5194/isprs-annals-xi-3-2026-117-2026 | V | ADJACENT (AEF vs S2-features comparison for forest type, not mining, no explicit label-efficiency-ratio or transfer-asymmetry framing) |
| Evaluating AlphaEarth Foundations Embeddings for Wildfire Susceptibility Mapping | 2026 | arXiv | arXiv:2608.12663 | V | ADJACENT (AEF embedding evaluation for a hazard-mapping task, not label efficiency vs baseline, not mining) |
| Utilizing a Geospatial Foundation Model for Coastline Delineation in Small Sandy Islands | 2025 | arXiv | arXiv:2511.10177 | V | ADJACENT (GFM fine-tuning for a detection task, no label-efficiency-ratio/transfer-asymmetry framing, not mining) |
| Transductive Transfer-Learning for LULC Classification Using Geospatial Foundation Models | 2025 | IGARSS 2025 | DOI:10.1109/IGARSS55030.2025.11243977 | V | ADJACENT (transfer learning with GFMs for LULC, not mining, not an explicit parity-ratio/asymmetry study) |
| How Foundational Is the Retina Foundation Model? Estimating RETFound's Label Efficiency on Binary Classification | 2025 | Ophthalmology Science | DOI:10.1016/j.xops.2025.100707 | V | IRRELEVANT (medical imaging domain; only relevant as a methodological analog for "label efficiency of a foundation model," no RS/mining content) |
| Performance and label efficiency of traditional deep-learning models and a retina-specific foundation model | 2026 | Lancet Digital Health | DOI:10.1016/j.landig.2026.101031 | V | IRRELEVANT (medical domain analog only) |

Verdict: SURVIVES.

No 2025-2026 paper measures a label-efficiency parity ratio (AEF vs. an S2 baseline) for ASGM/mining detection, nor tests cross-region transfer asymmetry or the effect of pooling foreign labels for mining. The closest hits are (a) generic ASGM detection-via-DL papers (DRC, Brazilian Amazon dataset) with no embedding-vs-baseline or label-efficiency framing [V, DOI:10.3390/rs17244057; DOI:10.5753/wcama.2026.22440], and (b) AEF representation-learning-evaluation papers in other domains — slums [V, arXiv:2605.10029], forest type [V, DOI:10.5194/isprs-annals-xi-3-2026-117-2026], wildfire [V, arXiv:2608.12663] — that establish AEF-vs-classical-feature comparison as an active pattern but never touch mining or transfer asymmetry. arXiv turned up nothing on the ASGM+label-efficiency intersection at all (0 hits across 3 completed queries; remaining queries blocked by persistent rate-limiting). TA04's specific mechanism (label-efficiency parity ratio + directional transfer asymmetry + negative-transfer-from-pooling for ASGM) remains unaddressed. Mandatory cites to carry forward: the AlphaEarth Foundations paper itself (not re-verified this session but foundational), arXiv:2508.11739 (AEF tooling), and arXiv:2605.10029 (closest AEF-representation-evaluation structural analog) as related-work anchors.
## TH01 — DMZ discontinuity / DPRK design-based estimation

Queries run:
- Semantic Scholar: "North Korea land cover change remote sensing"; "DPRK deforestation Sentinel"; "DMZ land cover satellite"; "cross-border domain shift land cover embedding"; "design-based area estimation foundation model"; "North Korea forest cover satellite change detection"; "design-based accuracy assessment land cover change area estimator"; "Korean Journal of Remote Sensing AlphaEarth"; "Korean Journal of Remote Sensing land cover 2025" (last query returned no data — API rate-limited after retries)
- arXiv: all:"North Korea" AND all:"land cover"; all:DPRK AND all:deforestation; all:DMZ AND all:satellite; all:"domain shift" AND all:"land cover"; all:"design-based" AND all:"area estimation"; all:"AlphaEarth" AND all:Korea

| Title | Year | Venue | ID | V/U | Relation |
|---|---|---|---|---|---|
| Estimating River Water Quality Indicators in South Korea Using AlphaEarth Embeddings | 2025 | Korean Journal of Remote Sensing | DOI 10.7780/kjrs.2025.41.5.10 | [V] | MANDATORY-CITE (known KJRS AEF paper; water quality, not land cover — the KJRS+AlphaEarth query surfaced no other KJRS 2025/2026 AlphaEarth paper; the companion 'KJRS land cover 2025' query was exhausted by API rate limits, so 'no other KJRS AEF land-cover paper' is unconfirmed rather than a verified negative) |
| TerraDA: A Domain-Adaptive Framework With Dynamic Multimodal Remote Sensing Data Fusion and Consistency Learning for Cross-City Land Cover Classification | 2025 | IEEE JSTARS | DOI 10.1109/JSTARS.2025.3608777 | [V] | ADJACENT (cross-city domain adaptation for land-cover classification, but supervised deep-learning domain adaptation, not embedding-space cosine/vMF discontinuity diagnostics on a foundation model; no DPRK/border framing) |
| HyperKD: Distilling Cross-Spectral Knowledge in Masked Autoencoders via Inverse Domain Shift with Spatial-Aware Masking and Specialized Loss | 2025 | ICDSAA / arXiv 2508.09453 | arXiv:2508.09453 | [V] | ADJACENT (domain-shift term refers to sensor/spectral shift in MAE distillation, unrelated to political-border management discontinuity) |
| MVT: Mask-Grounded Vision-Language Models for Taxonomy-Aligned Land-Cover Tagging | 2025 | arXiv | arXiv:2509.18693 | [V] | IRRELEVANT (VLM tagging taxonomy, no border/change-area-estimation angle) |
| Integrating Google Earth Engine and random forest for land use and land cover change detection and analysis in the upper Tekeze Basin | 2025 | Earth Science Informatics | DOI 10.1007/s12145-025-01750-y | [V] | IRRELEVANT (Ethiopia basin, standard RF classification, no design-based CI estimator, no foundation model, no DPRK) |
| Accuracy Assessment of Four Land Cover Datasets at Urban, Rural and Metropolitan Area Level | 2025 | Remote Sensing | DOI 10.3390/rs17050756 | [V] | ADJACENT (accuracy-assessment framing but comparing existing LC products, not a design-based area-change estimator from a foundation model) |
| An Integrated Earth Observation Assessment of Land-Cover Change, Settlement Expansion, and Tropospheric NO2 in East Kazakhstan | 2026 | Land | DOI 10.3390/land15081513 | [V] | IRRELEVANT (Kazakhstan, no design-based estimator, no foundation-model embeddings, no cross-border discontinuity) |
| Design-Based Cross-Validation for Comparing Small Area Estimators | 2026 | arXiv | arXiv:2604.23464 | [V] | ADJACENT (design-based small-area-estimation methodology, general statistics — no remote sensing / foundation-model / DPRK application; background-literature relevance only, not mandatory) |
| Hierarchical models for small area estimation using zero-inflated forest inventory variables | 2025 | arXiv | arXiv:2503.22103 | [V] | ADJACENT (forest-inventory small-area estimation, model-based not embedding-based, no DPRK/closed-border case) |
| Leveraging national forest inventory data to estimate forest carbon density status and trends for small areas | 2025 | arXiv | arXiv:2503.08653 | [V] | ADJACENT (same small-area-estimation family, US forest inventory; not a foundation-model / data-denied-region application) |

No hit from either API involves: (a) cross-border embedding-space (cosine/vMF) shift diagnostics across a managed/unmanaged political border, or (b) design-based DPRK (or comparable data-denied region) land-change area estimation with confidence intervals built on a geospatial foundation model (AlphaEarth or otherwise). No paper mentions DMZ, DPRK, or North Korea in combination with AlphaEarth, embedding discontinuity, or design-based estimation. The only confirmed AEF+Korea hit is the KJRS water-quality embeddings paper (mandatory cite/context, not competing). arXiv searches for "North Korea"+"land cover" and DMZ+satellite returned zero results (some 429-exhausted before falling back to "no results", so treat as weak/inconclusive rather than a strong negative — but combined with the Semantic Scholar coverage, no positive hit for either sub-RQ emerged).

Verdict: SURVIVES. Neither sub-RQ (a: label-free cross-border cosine/vMF discontinuity diagnostics; b: design-based DPRK land-change area estimation with CIs from annual embeddings) is addressed by any 2025-2026 paper found. Closest adjacent work is generic domain-adaptation for cross-city land-cover classification (TerraDA, [V] JSTARS 2025) and generic design-based small-area-estimation statistics (arXiv:2604.23464, [V]) — neither combines a geospatial foundation model with a political border or a closed/data-denied country case. KJRS AlphaEarth paper (DOI 10.7780/kjrs.2025.41.5.10, [V]) remains a mandatory citation for AEF-in-Korea context but does not touch land cover or borders. No kill reference found for either sub-RQ.
