# Literature clusters — what each body of work settles, and what it leaves open

Twelve clusters, 58 verified references (`references.bib`, `LITERATURE_MAP.md`). This file is
the reading: what the cluster establishes, what it does not, and which claim of ours it
constrains. Candidate discovery used the Semantic Scholar Graph API; every entry was then
resolved by DOI, and the bibliography carries the registered metadata rather than anything
transcribed.

## 1. Geospatial foundation models and embedding products
Establishes that a general-purpose per-pixel representation is now a product, not a research
artefact: `brown2025alphaearth` supplies an annual 64-dimensional embedding field for the whole
land surface, with `jakubik2023prithvi`, `szwarcman2026prithvi2`, `cong2022satmae`,
`sun2023ringmo`, `hong2024spectralgpt` and `manas2021seco` marking the modelling lineage and
`marsocci2024pangaea` the benchmarking practice. **Left open:** every benchmark in this cluster
scores *label accuracy* on downstream tasks. None asks what an *annual* embedding does with an
event whose evidence arrives unevenly within the year. Temporal fidelity is not a benchmark
axis, which is precisely the gap this paper occupies.

## 2. Temporal semantics of annual composites and products
Establishes that "the year a change is recorded" is a product-design decision with known
failure modes: `hansen2013forest` fixes an annual `lossyear`, `zhu2014ccdc`, `verbesselt2010bfast`,
`kennedy2010landtrendr` and `zhu2020cold` show that sub-annual timing is recoverable from dense
time series, `bogaert2022hmm` and `zhang2020thirtym` treat annual-label consistency directly, and
`brown2022dynamicworld` shows the near-real-time alternative. **Left open:** these are all
*algorithms whose temporal behaviour is designed*. An embedding's temporal behaviour is
inherited from whatever imagery the year happened to supply, and is nowhere characterised.

## 3. Deforestation alert systems and their latency
Supplies the event dates and the vocabulary of latency: `reiche2021radd` (the RADD alerts used
here), `hansen2016glad`, `diniz2015deterb` (the DETER polygons used here), `doblas2022deterr`,
`tang2019nrt`, `bullock2022timeliness`, `reiche2024integrating`, `assis2019terrabrasilis`.
**Constrains us directly:** this cluster is unanimous that alert dates carry their own latency,
and `bullock2022timeliness` gives the framework for measuring it. Our dating rule
(`date_upper`) and our treatment of the Congo alert vintage are applications of that lesson to a
problem the cluster has not addressed — using alerts to *audit a third product* rather than to
detect change.

## 4. Cloud cover and optical observation supply in the tropics
Establishes the magnitude of the constraint: `whitcraft2015cloud` and `prudente2020limitations`
quantify how little clear optical observation a tropical growing season affords,
`sudmanns2019coverage` maps Sentinel-2 coverage dynamics globally, `huang2026optical` is a
representative attempt to work around the gaps. **Left open:** the supply is treated as a
nuisance to be mitigated, never as a *predictor of what a downstream annual product will
contain*. Our expected-supply and deferral-risk layers make it exactly that.

## 5. SAR-optical fusion for deforestation
Establishes the standard remedy and its limits: `reiche2018improving`, `ballere2021sar`,
`hoekman2020widearea` and `ygorra2021cusum` show that Sentinel-1 detects tropical clearings
through cloud, often earlier than optical. **Constrains us sharply.** If radar compensates for
optical scarcity in general, our central result should not exist. The reconciliation we offer is
that these papers demonstrate what a *SAR-specific detector* can do, whereas an annual optical-
led embedding does not inherit that capability — a distinction this cluster has had no reason to
draw.

## 6. Loss-year attribution, carbon accounting and regulatory cut-offs
Establishes the stakes: `curtis2018drivers` attributes loss by driver and year,
`tyukavina2018congo` does so for the Congo Basin, and `lambin2023supplychains` sets out how
commodity regulation turns a cut-off *date* into a compliance boundary. **Constrains us:** it is
why a one-year attribution error is not a rounding error, and why our two-tier attribution
guidance is addressed to users rather than to model builders.

## 7. Spatial cross-validation and block bootstrap
Establishes that spatially autocorrelated samples make naive intervals too narrow:
`roberts2017crossvalidation`, `ploton2020spatial`, `meyer2022machine`, `valavi2018blockcv`.
**Constrains us:** every interval in this paper is a 0.5° block bootstrap for this reason, and
it is why we report the block structure rather than an event count alone.

## 8. Reference-data quality, polygon geometry and positional error
Establishes that reference maps are instruments with error: `olofsson2014good`,
`stehman2019key`, `mcroberts2018imperfect`, `ye2018obia`. **Constrains us:** our offset check
(interior versus 50–150 m ring) is a positional-error diagnostic in this tradition, and the
`radd_only` population is a selection-bias diagnostic. Neither is novel methodology; what is new
is applying them to decide whether an embedding *or* its reference map is at fault.

## 9. Change detection with learned representations
Establishes the methodological neighbourhood: `saha2019dcva`, `daudt2018siamese`, `chen2022bit`,
`chen2021dasnet`, `chen2024changemamba`, `li2023sartscc`, `li2022contrastive`,
`tian2022largescale`, `lin2024transformermad`. **Left open:** all of these *train* a change
detector, usually on bitemporal pairs chosen for the task. We do the opposite — take an
off-the-shelf annual representation, apply the simplest possible distance (angular change against
a stable-forest threshold), and ask what it registers. Our contribution is not a better detector
and should not be read as competing with this cluster.

## 10. Amazon deforestation dynamics and seasonality
Establishes that clearing is seasonal and increasingly fine-grained:
`kalamandeen2018pervasive`, `picoli2018bigearth`, `santos2021quality`. **Constrains us:** the
calendar month of an event is not random, so the month of clearing and the supply of clear
observations are correlated in the real world — which is why every model here carries month
fixed effects and why the deferral-risk layer is presented per event month.

## 11. Congo Basin forest monitoring
Supplies the second region: `vancutsem2021tmf` (the TMF product our Congo events come from),
with `tyukavina2018congo` on the loss regime and `reiche2021radd` on the alert product. **Thin
by necessity**, and that thinness is part of our finding: the Congo has no alert archive
contemporaneous with 2021 in Earth Engine, and the reference map is a model-derived annual class
transition rather than an analyst-drawn polygon. This is why we present the Congo as a second
case of reference selection rather than as a replication.

## 12. Measurement error, attenuation and lower-bound reasoning
`carroll2006measurement` supplies the standard result we lean on: error in a covariate
attenuates its coefficient toward zero. **Constrains us:** since event dates carry error, and
`clear_post` is computed from them, every gap we report is a lower bound on the true effect —
the single most important qualifier on our numbers, and the reason the Congo re-dating changes
the verdict rather than the sign.

## Where the gap sits
Clusters 1 and 2 between them contain no measurement of the temporal fidelity of an annual
embedding; cluster 4 has the mechanism but not the consequence; cluster 5 has the remedy but not
the test of whether it transfers to a representation that was not built to use it; cluster 3 has
the dating instruments but has never turned them on a third product. This paper joins those four.
