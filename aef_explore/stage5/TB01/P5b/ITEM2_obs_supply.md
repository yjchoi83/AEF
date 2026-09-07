# P5b item 2 — map layer (d) replaced by observation supply and deferral risk

> **Layer (d) is retired.** P5's `σ(2.1413 + 0.0552 · count)` "attribution confidence" plate is
> stamped RETIRED on both `M_*.png` and its GeoTIFFs renamed
> `*_RETIRED_midyear_prior_pconf_60m.tif`. In its place: **F7 expected observation supply by
> calendar month** and **F8 deferral risk by event month**, both region-wide, both derived from
> the same monthly Sentinel-2 record the paper's covariate comes from.

Scripts: `obs_supply.py` (Earth Engine), `make_plates.py` (figures + link refit),
`make_products.py` (GeoTIFFs, rename), `relabel_layer_d.py` (plate stamp).
Numbers in `obs_supply_stats.json`.

## Why (d) had to go — two defects, both measured

1. **Wrong input.** The link was fitted on `clear_post`, a *post-event* count, and the map fed
   it the *annual* count. P5 §3 measured what the annual count is worth for the question the
   layer claims to answer: **AUC 0.599** for predicting deferral.
2. **Mis-calibrated where it matters.** Logit-linear in the raw count predicts **0.907**
   registration at one post-event clear observation; the data give **0.585** (n = 130). The
   layer's near-uniform blue was not confidence, it was a saturated link function.

Refitting the same one-covariate model as logit-linear in `ln(1 + clear_post)`, on the 38,158
dated 2021 events with `clear_post > 0` (the exactly-zero bin is excluded — item 1 shows it is
a dating artifact, not an observation state), gives **β₀ = −0.1800, β₁ = 1.2396** and tracks
the empirical curve:

| `clear_post` | (0,1] | (1,2] | (2,3] | (3,4] | (4,6] | (6,9] | (9,14] | (14,25] | (25,50] | > 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| n | 130 | 215 | 303 | 415 | 1,002 | 1,665 | 4,036 | 13,317 | 13,119 | 3,928 |
| empirical | .585 | .605 | .723 | .793 | .872 | .922 | .970 | .980 | .982 | .977 |
| **fitted (log link)** | .604 | .733 | .799 | .845 | .886 | .923 | .951 | .972 | .985 | .994 |
| old raw-count link | .907 | .911 | .915 | .919 | .924 | .933 | .945 | .963 | .981 | .997 |

## F7 — expected observation supply (`figures/F7_obs_supply.png`)

Mean clear Sentinel-2 observations per pixel per calendar month, averaged over 2019–2021
(clear = SCL ∉ {3, 8, 9, 10, 11}), 24 panels on one sequential ramp plus the region-mean curves.

| region-mean clear obs | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | annual |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Pará / BR-163 | 2.03 | **1.04** | 1.78 | 1.48 | 2.95 | 5.93 | **6.48** | 6.24 | 4.21 | 3.22 | 1.87 | 1.97 | 39.2 |
| Roraima (south) | 2.63 | 2.98 | **4.41** | 1.77 | **1.33** | 1.32 | 2.56 | 2.65 | 3.63 | 3.18 | 2.93 | 2.70 | 32.1 |

**The two regions are out of phase.** Pará's supply is a single dry-season peak (6.5× its
February floor); Roraima's peaks in March and bottoms in May–June. A single "wet season"
correction would be wrong for one of them. Within a region the supply is also *banded* —
Sentinel-2 orbit overlaps are directly visible as stripes carrying roughly double the
single-swath count (p90/p10 ≈ 3× in every month), so two clearings a few kilometres apart can
face very different observation odds in the same month.

## F8 — deferral risk by event month (`figures/F8_deferral_risk.png`)

For an event in month *m*, `E_m = 0.5·s_m + Σ_{k>m} s_k` (P2's proration rule applied to the
supply climatology), then risk `= 1 − σ(β₀ + β₁·ln(1 + E_m))`.

| mean deferral risk | Jan | Mar | Jun | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|
| Pará / BR-163 | .015 | .017 | .022 | .080 | .120 | .203 | **.354** |
| Roraima (south) | .018 | .025 | .034 | .073 | .091 | .148 | **.306** |

Risk is flat and small from January to August and then rises by an order of magnitude in the
last quarter — the map form of the paper's claim that a clearing's chance of appearing in the
right annual embedding is set by how much of the observing year is left. Pará's Jan–Aug floor
is lower than Roraima's despite a *later* peak, because what matters is the integral of what
remains, not the month's own supply. Within December, the striping is fully expressed: the
orbit-overlap bands sit near .25 while single-swath ground sits near .40.

**Read F8 as a prior, not a per-pixel probability.** It conditions on nothing but pixel and
month — not on patch size, not on the state τ, not on SAR — and it is calibrated on Brazilian
DETER polygons in 2021 only.

## Products (git-ignored `data/products/`)

| file | content |
|---|---|
| `<region>_obs_supply_x10_200m.tif` | 12-band Int16, mean clear obs × 10 per calendar month |
| `<region>_deferral_risk_x1000_200m.tif` | 12-band Int16, deferral risk × 1000 per event month |
| `<region>_RETIRED_midyear_prior_pconf_60m.tif` | the retired layer (d), renamed, kept for provenance |

## Compute
One Earth Engine pass per region (12 monthly means × 3 years, reduceRegion statistics, one NPY
and one GeoTIFF download); every panel, the risk stack and the link refit are computed locally
from those arrays, so no per-panel EE work was repeated.
