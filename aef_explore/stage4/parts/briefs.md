# Stage-4 N topic briefs (core RQ = what a 2025-2026 paper would have to answer to kill the topic)

## TB01 (GO) — Within-year timing in annual embeddings
Core RQ: does an ANNUAL Earth-observation embedding (AlphaEarth/AEF year Y) encode WITHIN-year event
timing (month of tropical forest clearing), and what is the pre->post replacement law w(m) and the
detection lag of an annual-embedding change rule? KILL only if a paper measures event-month
recoverability / within-year mixing of an annual embedding product with comparable data+validation.

## TB02 (C-GO) — Observation-availability artefacts
Core RQ: does missing SAR (Sentinel-1B outage 2021-12) observation availability causally inflate
angular drift of stable-land annual embeddings and thus change false-positive rates, and can an
availability-aware threshold restore nominal FPR? KILL if a paper quantifies sensor-outage-induced
spurious change in an embedding/GFM product.

## TC01 (C-GO) — Dimension-level attribution of static/climate-input dependence
Core RQ: are the AEF dimensions decodable from terrain/climate the same ones carrying cross-region
identity, and does removing them recover transfer loss without in-domain cost? Scale dependence of
static decodability (25->1000 km). KILL if a paper does dimension-level attribution + ablation of
static-input dependence in a geospatial FM.

## TD01 (C-GO) — Ordinal degradation-intensity axis
Core RQ: do annual embeddings carry an ORDINAL degradation-intensity axis that is not reducible to
sub-pixel clearing fraction and is calibratable to independent ALS/ICESat-2 structural loss?
KILL if a paper produces a calibrated continuous/ordinal degradation-intensity measurand from
embeddings with independent structural validation.

## TE02 (C-GO) — Drought transition not level
Core RQ: in drylands, is stable-land embedding drift driven by climate anomaly TRANSITION (onset /
drought-break) rather than LEVEL, and does ERA5 anomaly regress-out restore nominal change FPR?
KILL if a paper attributes dryland embedding/GFM false change to climate-input dependence with a
correction.

## TE06 (C-GO) — Fair-baseline / modality attribution + relief conditioning
Core RQ: does the AEF margin survive a dimensionality- and temporally-matched rich classical
baseline (S2 percentiles/harmonics + S1 + Landsat + static, GBT), and is the static-covariate
absorption fraction a monotone function of terrain relief? KILL if a paper runs a matched baseline
ladder with modality-wise attribution AND relief interaction.

## TA02 (C-GO) — Stand-age ceiling
Core RQ: what is the upper age bound recoverable from single-year annual embeddings for secondary
forest (saturation ~12-15 y, attenuation slope), and is it representational rather than a linear
probe artefact? KILL if a paper bounds the age ceiling of embedding-based regrowth age with
nonlinear/ordinal heads and independent (non-Landsat) reference.

## TA04 (C-GO) — Label efficiency for ASGM
Core RQ: how few labels does AEF need to match a 1000-label S2 baseline for artisanal gold mining,
is cross-region transfer directionally asymmetric, and does pooling foreign labels hurt?
KILL if a paper measures label-efficiency parity ratios for mining detection with embeddings +
transfer asymmetry.

## TH01 (C-GO) — DMZ as management discontinuity / DPRK design-based estimation
Core RQ: is the ROK-DPRK border a representation discontinuity or a management discontinuity
(label-free cross-border cosine/vMF diagnostics), and can design-based DPRK land-change areas with
CIs be produced from annual embeddings? KILL if a paper does cross-border embedding shift
diagnostics or design-based DPRK land-cover change from a GFM.
