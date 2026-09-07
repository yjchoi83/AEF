# Literature map — every reference, its cluster and the job it does

**62 references**, all resolved by DOI content negotiation from doi.org (Crossref / DataCite); `references.bib` holds the registered metadata verbatim. Candidates were found with the Semantic Scholar Graph API (cached under `cache/`, one request per second); the curation — which candidate answers which part of the argument — is in the `ENTRIES` table of `code/bib_build.py`.

## Venue distribution

| venue | n | target |
|---|---|---|
| Remote Sensing of Environment | 12 | ≥ 8 ✔ |
| IEEE Transactions on Geoscience and Remote Sensing | 8 | ≥ 6 ✔ |
| ISPRS Journal of Photogrammetry and Remote Sensing | 6 | ≥ 5 ✔ |
| IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing | 5 | ≥ 4 ✔ |
| arXiv | 4 | — |
| Environmental Research Letters | 3 | — |
| Science | 2 | — |
| Remote Sensing | 2 | — |
| International Journal of Applied Earth Observation and Geoinformation | 2 | — |
| Science Advances | 2 | — |
| Nature Communications | 2 | — |
| IEEE Transactions on Pattern Analysis and Machine Intelligence | 1 | — |
| 2021 IEEE/CVF International Conference on Computer Vision (ICCV) | 1 | — |
| Scientific Data | 1 | — |
| ISPRS International Journal of Geo-Information | 1 | — |
| International Journal of Digital Earth | 1 | — |
| Remote Sensing Applications: Society and Environment | 1 | — |
| Annual Review of Environment and Resources | 1 | — |
| Ecography | 1 | — |
| Methods in Ecology and Evolution | 1 | — |
| 2018 25th IEEE International Conference on Image Processing (ICIP) | 1 | — |
| Scientific Reports | 1 | — |
| 2026 11th International Conference on Electronic Technology and Information Science (ICETIS) | 1 | — |
| Frontiers in Remote Sensing | 1 | — |
| Chapman and Hall/CRC | 1 | — |

MDPI titles: **3** (ceiling 5) ✔

## Clusters

### 1. Geospatial foundation models and embedding products

*What the object under test is, and what the field currently asks of it.*

| reference | venue, year | what it supplies |
|---|---|---|
| `manas2021seco` — Manas et al. | 2021 IEEE/CVF International Conference on Computer Vision (ICCV), 2021 | seasonal contrast pretraining |
| `cong2022satmae` — Cong et al. | arXiv, 2022 | temporal masked autoencoding for EO |
| `jakubik2023prithvi` — Jakubik et al. | arXiv, 2023 | geospatial foundation model |
| `sun2023ringmo` — Sun et al. | IEEE Transactions on Geoscience and Remote Sensing, 2023 | masked-image-modelling FM in TGRS |
| `marsocci2024pangaea` — Marsocci et al. | arXiv, 2024 | benchmark for geospatial FMs |
| `hong2024spectralgpt` — Hong et al. | IEEE Transactions on Pattern Analysis and Machine Intelligence, 2024 | spectral foundation model |
| `brown2025alphaearth` — Brown et al. | arXiv, 2025 | the embedding product under test |
| `szwarcman2026prithvi2` — Szwarcman et al. | IEEE Transactions on Geoscience and Remote Sensing, 2026 | multitemporal FM successor |
| `ma2026harvesting` — Ma et al. | International Journal of Applied Earth Observation and Geoinformation, 2026 | how AlphaEarth is currently evaluated: downstream label accuracy |
| `belyakov2026cloudprior` — Belyakov et al. | 2026 11th International Conference on Electronic Technology and Information Science (ICETIS), 2026 | the assumption that AEF embeddings are robust to observational gaps |

### 2. Temporal semantics of annual composites and products

*The prior art on when a change enters an annual product -- the question this paper asks of embeddings.*

| reference | venue, year | what it supplies |
|---|---|---|
| `verbesselt2010bfast` — Verbesselt et al. | Remote Sensing of Environment, 2010 | break detection in time series |
| `kennedy2010landtrendr` — Kennedy et al. | Remote Sensing of Environment, 2010 | temporal segmentation |
| `hansen2013forest` — Hansen et al. | Science, 2013 | the annual forest-loss product family |
| `zhu2014ccdc` — Zhu et al. | Remote Sensing of Environment, 2014 | continuous change detection |
| `zhu2020cold` — Zhu et al. | Remote Sensing of Environment, 2020 | continuous land-disturbance monitoring |
| `zhang2020thirtym` — Zhang et al. | ISPRS Journal of Photogrammetry and Remote Sensing, 2020 | annual land-surface change detection |
| `rodman2021disturbance` — Rodman et al. | Remote Sensing of Environment, 2021 | what governs detectability in a time series: agent and severity, not history |
| `brown2022dynamicworld` — Brown et al. | Scientific Data, 2022 | near-real-time land cover |
| `bogaert2022hmm` — Bogaert et al. | IEEE Transactions on Geoscience and Remote Sensing, 2022 | temporal consistency of annual maps |

### 3. Deforestation alert systems and their latency

*Where the event dates come from, and how their own latency propagates into this study.*

| reference | venue, year | what it supplies |
|---|---|---|
| `diniz2015deterb` — Diniz et al. | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2015 | the reference map used here |
| `hansen2016glad` — Hansen et al. | Environmental Research Letters, 2016 | Landsat-based alerts |
| `tang2019nrt` — Tang et al. | Remote Sensing of Environment, 2019 | near-real-time algorithms and assessment |
| `assis2019terrabrasilis` — F. G. Assis et al. | ISPRS International Journal of Geo-Information, 2019 | the DETER/PRODES data infrastructure |
| `yuan2020lstm` — Yuan et al. | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2020 | sequence models for near-real-time disturbance |
| `reiche2021radd` — Reiche et al. | Environmental Research Letters, 2021 | the alert product used for dating |
| `doblas2022deterr` — Doblas et al. | Remote Sensing, 2022 | radar-based operational alerts |
| `bullock2022timeliness` — Bullock et al. | Remote Sensing of Environment, 2022 | timeliness assessment framework |
| `reiche2024integrating` — Reiche et al. | Environmental Research Letters, 2024 | alert integration and timeliness |
| `potapov2026operational` — Potapov et al. | Frontiers in Remote Sensing, 2026 | intercomparison of operational disturbance products in Brazil |

### 4. Cloud cover and optical observation supply in the tropics

*The mechanism the paper identifies as binding.*

| reference | venue, year | what it supplies |
|---|---|---|
| `whitcraft2015cloud` — Whitcraft et al. | Remote Sensing of Environment, 2015 | cloud cover and optical observability |
| `sudmanns2019coverage` — Sudmanns et al. | International Journal of Digital Earth, 2019 | Sentinel-2 coverage dynamics |
| `prudente2020limitations` — Prudente et al. | Remote Sensing Applications: Society and Environment, 2020 | cloud limits in South America |
| `huang2026optical` — Huang et al. | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2026 | working around optical observation gaps |

### 5. SAR-optical fusion for deforestation

*The obvious remedy, and the evidence on whether it compensates.*

| reference | venue, year | what it supplies |
|---|---|---|
| `reiche2018improving` — Reiche et al. | Remote Sensing of Environment, 2018 | SAR-optical fusion for alerts |
| `hoekman2020widearea` — Hoekman et al. | Remote Sensing, 2020 | wide-area SAR monitoring |
| `ballere2021sar` — Ballère et al. | Remote Sensing of Environment, 2021 | SAR benefit over optical in the tropics |
| `ygorra2021cusum` — Ygorra et al. | International Journal of Applied Earth Observation and Geoinformation, 2021 | Sentinel-1 CuSum forest-cover loss |

### 6. Loss-year attribution, carbon accounting and regulatory cut-offs

*Why the year a clearing is assigned to has consequences outside remote sensing.*

| reference | venue, year | what it supplies |
|---|---|---|
| `curtis2018drivers` — Curtis et al. | Science, 2018 | why loss year and driver matter |
| `tyukavina2018congo` — Tyukavina et al. | Science Advances, 2018 | Congo Basin loss attribution |
| `lambin2023supplychains` — Lambin et al. | Annual Review of Environment and Resources, 2023 | supply-chain cut-off dates |

### 7. Spatial cross-validation and block bootstrap

*The inference machinery: why every CI here is blocked.*

| reference | venue, year | what it supplies |
|---|---|---|
| `roberts2017crossvalidation` — Roberts et al. | Ecography, 2017 | blocked validation with autocorrelation |
| `valavi2018blockcv` — Valavi et al. | Methods in Ecology and Evolution, 2018 | spatial block cross-validation tooling |
| `ploton2020spatial` — Ploton et al. | Nature Communications, 2020 | spatial validation of large-scale models |
| `meyer2022machine` — Meyer et al. | Nature Communications, 2022 | assessing global ML maps |

### 8. Reference-data quality, polygon geometry and positional error

*Why the reference map is a measurement instrument, not ground truth.*

| reference | venue, year | what it supplies |
|---|---|---|
| `olofsson2014good` — Olofsson et al. | Remote Sensing of Environment, 2014 | area estimation and accuracy practice |
| `mcroberts2018imperfect` — McRoberts et al. | ISPRS Journal of Photogrammetry and Remote Sensing, 2018 | imperfect reference data |
| `ye2018obia` — Ye et al. | ISPRS Journal of Photogrammetry and Remote Sensing, 2018 | object-based accuracy assessment |
| `stehman2019key` — Stehman et al. | Remote Sensing of Environment, 2019 | rigorous accuracy assessment |

### 9. Change detection with learned representations

*The methodological neighbourhood of angular change in an embedding space.*

| reference | venue, year | what it supplies |
|---|---|---|
| `daudt2018siamese` — Caye Daudt et al. | 2018 25th IEEE International Conference on Image Processing (ICIP), 2018 | siamese change detection |
| `saha2019dcva` — Saha et al. | IEEE Transactions on Geoscience and Remote Sensing, 2019 | unsupervised deep change vector analysis |
| `chen2021dasnet` — Chen et al. | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2021 | attention-based change detection |
| `chen2022bit` — Chen et al. | IEEE Transactions on Geoscience and Remote Sensing, 2022 | transformer change detection |
| `li2022contrastive` — Li et al. | IEEE Transactions on Geoscience and Remote Sensing, 2022 | contrastive representations for RS |
| `tian2022largescale` — Tian et al. | ISPRS Journal of Photogrammetry and Remote Sensing, 2022 | large-scale deep change detection |
| `li2023sartscc` — Li et al. | IEEE Transactions on Geoscience and Remote Sensing, 2023 | SAR time-series change detection |
| `chen2024changemamba` — Chen et al. | IEEE Transactions on Geoscience and Remote Sensing, 2024 | state-space change detection |
| `lin2024transformermad` — Lin et al. | IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 2024 | unsupervised multivariate alteration detection |

### 10. Amazon deforestation dynamics and seasonality

*Why the calendar month of a clearing is not random.*

| reference | venue, year | what it supplies |
|---|---|---|
| `kalamandeen2018pervasive` — Kalamandeen et al. | Scientific Reports, 2018 | small-clearing dynamics in Amazonia |
| `picoli2018bigearth` — Picoli et al. | ISPRS Journal of Photogrammetry and Remote Sensing, 2018 | Brazilian time-series monitoring |
| `santos2021quality` — Santos et al. | ISPRS Journal of Photogrammetry and Remote Sensing, 2021 | class noise in image time series |

### 11. Congo Basin forest monitoring

*The second region, and why its reference data are a different kind of object.*

| reference | venue, year | what it supplies |
|---|---|---|
| `vancutsem2021tmf` — Vancutsem et al. | Science Advances, 2021 | the Congo event set |

### 12. Measurement error, attenuation and lower-bound reasoning

*Why a dating error makes the reported effect a lower bound.*

| reference | venue, year | what it supplies |
|---|---|---|
| `carroll2006measurement` — Carroll et al. | Chapman and Hall/CRC, 2006 | attenuation from covariate error |


## Novelty pass

Eight targeted searches were run against the Semantic Scholar Graph API on the four questions
the brief specifies — annual-embedding temporal fidelity, AlphaEarth change detection, the
optical-versus-SAR contribution inside a learned representation, and deforestation year
attribution — plus four adjacent formulations (cloud effects on annual composites, `lossyear`
timing accuracy, observation density as a predictor of omission, and operational product
intercomparison). Queries are in `code/queries/novelty.json`; every response is cached under
`cache/`.

**Nothing found measures the temporal fidelity of an annual embedding field.** The closest work
falls into four groups, and each is adjacent rather than overlapping.

*AlphaEarth applications and benchmarks.* A rapidly growing set of papers applies the published
embeddings to a downstream task — agricultural monitoring (`ma2026harvesting`, now cited),
biomass, air quality, slum mapping, mangrove classification, tea plantations, wildfire
susceptibility. Every one of them scores label accuracy on a task; none asks which events enter
which year's vector. `ma2026harvesting` is the most systematic and is explicit that the
existing evaluation record is "mostly about land cover and land use classification", which is
precisely the gap we occupy. **No overlap; cited as evidence for the gap.**

*Embeddings used as cloud-robust priors.* One conference paper conditions an image-restoration
model on AlphaEarth embeddings on the stated grounds that they are "robust to temporary
observational gaps such as cloud cover" (`belyakov2026cloudprior`, now cited). This is the only
result found that makes a claim in the neighbourhood of ours, and it points the other way. The
tension is resolvable and we resolve it in Section 1.3: a year-long embedding is a stable
descriptor of a *place*, which is why it helps restore a cloudy image, and that is compatible
with it being a poor descriptor of *when* a change happened. **Partial overlap in subject,
opposite in direction; engaged explicitly in the manuscript.**

*Operational product intercomparison.* An evaluation of MapBiomas Alerta, Tree Cover Loss and
TMF in Brazilian primary forests for 2023–2024 (`potapov2026operational`, now cited) compares
disturbance products against one another. It shares our concern with what operational products
record, but compares alert and annual products among themselves rather than auditing a
general-purpose representation, and it does not model observation supply. **No overlap; cited
in the discussion as the natural companion to our two-tier guidance.**

*What governs detectability in a time series.* Work on Landsat time series shows detection
accuracy depends on mortality agent and disturbance severity rather than on prior disturbance
history (`rodman2021disturbance`, now cited). Methodologically this is the same shape of
question as ours — what property of the event, rather than of the algorithm, governs whether it
is detected — applied to a different product and a different candidate explanation. **No
overlap; cited where we test the rival "harder events" explanation.**

*Year attribution.* Searches on loss-year misattribution returned nothing measuring the
timing accuracy of an annual product against independently dated events. The nearest is older
work on how the choice of imagery affects attribution of change to disturbance type, which
concerns *what* a change is attributed to rather than *when*. **No overlap.**

*Optical versus SAR inside a representation.* This search returned essentially nothing: the
literature compares optical and SAR *detectors* (cluster 5) but does not ask what each
contributes to a fused learned representation's ability to record an event. **No overlap, and
we regard this as the least contested of our contributions.**

**Assessment.** The four searches the brief names return no prior measurement of what we
measure. The one paper that touches the same product and the same mechanism assumes the
property we test and finds it useful for a different purpose; we now cite it and address the
apparent conflict directly rather than leaving a reviewer to raise it. Four references were
added to the bibliography as a result of this pass, bringing it to 62.
