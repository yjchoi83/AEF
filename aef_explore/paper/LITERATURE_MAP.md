# Literature map — every reference, its cluster and the job it does

**58 references**, all resolved by DOI content negotiation from doi.org (Crossref / DataCite); `references.bib` holds the registered metadata verbatim. Candidates were found with the Semantic Scholar Graph API (cached under `cache/`, one request per second); the curation — which candidate answers which part of the argument — is in the `ENTRIES` table of `code/bib_build.py`.

## Venue distribution

| venue | n | target |
|---|---|---|
| Remote Sensing of Environment | 11 | ≥ 8 ✔ |
| IEEE Transactions on Geoscience and Remote Sensing | 8 | ≥ 6 ✔ |
| ISPRS Journal of Photogrammetry and Remote Sensing | 6 | ≥ 5 ✔ |
| IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing | 5 | ≥ 4 ✔ |
| arXiv | 4 | — |
| Environmental Research Letters | 3 | — |
| Science | 2 | — |
| Remote Sensing | 2 | — |
| Science Advances | 2 | — |
| Nature Communications | 2 | — |
| IEEE Transactions on Pattern Analysis and Machine Intelligence | 1 | — |
| 2021 IEEE/CVF International Conference on Computer Vision (ICCV) | 1 | — |
| Scientific Data | 1 | — |
| ISPRS International Journal of Geo-Information | 1 | — |
| International Journal of Digital Earth | 1 | — |
| Remote Sensing Applications: Society and Environment | 1 | — |
| International Journal of Applied Earth Observation and Geoinformation | 1 | — |
| Annual Review of Environment and Resources | 1 | — |
| Ecography | 1 | — |
| Methods in Ecology and Evolution | 1 | — |
| 2018 25th IEEE International Conference on Image Processing (ICIP) | 1 | — |
| Scientific Reports | 1 | — |
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

