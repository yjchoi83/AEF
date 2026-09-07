# When does an annual embedding register a clearing? Observation supply and temporal fidelity of AlphaEarth embeddings in the Brazilian Amazon, 2020–2021

**Authors.** [AUTHORS TBD]

**Target journal.** Remote Sensing of Environment. Fallback: ISPRS Journal of Photogrammetry
and Remote Sensing.

## Abstract

Annual global embedding fields compress a year of satellite observation into one vector per
pixel and are increasingly used for land-change analysis. Their accuracy on downstream labels
is benchmarked; their temporal fidelity is not. We ask which forest-clearing events an annual
embedding registers, and what governs the exceptions. Using
77,967 expert-mapped clearings across the Brazilian Legal Amazon in 2020 and 2021, dated by
combining Sentinel-1 RADD alerts read over the whole polygon with the analyst's own detection
date, we define registration as a year-on-year embedding angular change exceeding a per-state
stable-forest threshold. Registration saturates at 97.5 % (2021) and 98.1 % (2020) for events
followed by five or more clear Sentinel-2 observations, and falls to 51.0 % and 60.6 % for
events followed by two or fewer, a gap of 46.5 percentage points [39.0, 53.6] and 37.5
[31.3, 43.9]. The deficit is specifically optical: among low-observation events, registration
is lowest where Sentinel-1 coverage is densest, so radar acquisition does not compensate.
Unregistered events are deferred rather than missed, 94.1 % and 96.5 % registering the
following year. For nearly half of unregistered events the change signal exceeds the
threshold in a 50–150 m ring around the polygon but not inside it. A Congo Basin comparison cannot presently answer the
same question: the low-observation stratum available for testing is an artefact of the alert
vintage used for dating. We provide expected-supply and
deferral-risk maps, and two-tier guidance for users who do and do not have an event date.

**Keywords.** annual embedding; AlphaEarth; temporal fidelity; deforestation alerts;
observation supply; year attribution

## 1. Introduction

### 1.1 The problem

A new class of Earth-observation product ships a learned representation rather than a
classification. AlphaEarth Foundations (Brown et al., 2025) publishes an annual, global,
10 m embedding field in which each pixel carries a 64-dimensional unit vector summarising that
pixel's year of observation, and comparable representations are being released or benchmarked
at pace (Cong et al., 2022; Jakubik et al., 2023; Sun et al., 2023; Hong et al., 2024; Marsocci et al., 2024; Szwarcman et al., 2026). The appeal for land-change work is direct: the
difference between two consecutive annual vectors is a ready-made change signal that requires
no training data, no radiometric normalisation and no sensor-specific engineering. Users are
already treating it as such.

The word doing the most work in that sentence is *annual*. A user who takes the difference
between the 2020 and 2021 embeddings, thresholds it, and calls the result "2021 clearing" has
made an assumption about temporal semantics that the product does not state and that no
benchmark measures: that a clearing occurring at any point in 2021 is fully expressed in the
2021 vector. That assumption is not obviously true. The embedding draws on optical,
radar and ancillary inputs, and in the humid tropics the supply of cloud-free optical
observation is both scarce and strongly seasonal (Whitcraft et al., 2015; Sudmanns et al., 2019; Prudente et al., 2020). A clearing in late November may be followed by one usable Sentinel-2
observation before the year ends; a clearing in July may be followed by thirty. If the annual
vector is a summary of what was seen, then when in the year an event happens should determine
whether it appears in that year's vector at all.

There is a specific reason to expect an embedding to behave differently from a classified
annual product here. A change-detection algorithm applied to a time series decides, explicitly,
what to do when observations are missing: it interpolates, it widens its confidence band, or it
declines to report. An embedding has no such decision point. It compresses whatever the year
supplied into a fixed-length vector, and a pixel observed twice in December produces a vector
in the same format, with the same apparent authority, as a pixel observed forty times. Nothing
in the product distinguishes them, and nothing in the difference between two years' vectors
records how much evidence each was built from. The question is therefore not whether an
embedding handles sparse observation badly — it has no mechanism for handling it at all — but
how much of the year's change survives compression when the evidence arrives late.

The consequence is not academic. The year to which a forest loss is assigned determines
whether it falls inside a national inventory period, whether it crosses a regulatory cut-off
date for commodity supply chains (Lambin and Furumo, 2023), and how it is attributed to a
driver in global accounting (Curtis et al., 2018; Tyukavina et al., 2018). A product that
systematically defers a subset of clearings by one year, and does so in a way correlated with
season and with location, introduces a bias into every one of those uses.

### 1.2 What is already known

Three literatures bear on this and none answers it. The first is the design of annual change
products, where temporal semantics are explicit engineering choices. The Global Forest Change
`lossyear` band assigns a year by construction (Hansen et al., 2013), and a line of algorithms
recovers sub-annual timing from dense time series by fitting and breaking temporal models
(Kennedy et al., 2010; Verbesselt et al., 2010; Zhu and Woodcock, 2014; Zhu et al., 2020), with recent work
aimed squarely at the temporal consistency of annual labels (Zhang et al., 2020; Bogaert et al., 2022) and near-real-time products that abandon the annual step altogether
(Brown et al., 2022). These products know what they do with timing because timing is designed
in. An embedding's temporal behaviour is instead inherited from whatever imagery the year
supplied, and has not been characterised.

The second is alert systems, which exist precisely because annual products are too slow.
RADD (Reiche et al., 2021), GLAD (Hansen et al., 2016), DETER (Diniz et al., 2015) and DETER-R
(Doblas et al., 2022) deliver detections within days to weeks, and a mature sub-literature
measures their own latency and how to combine them (Tang et al., 2019; Yuan et al., 2020; Bullock et al., 2022; Reiche et al., 2024). This literature supplies the instrument we use for dating, and it is
unanimous that alert dates carry error of their own — a point that turns out to be central
here. What it has not done is turn that instrument on a third product to audit *its* temporal
behaviour.

The third is SAR-optical fusion, the obvious remedy for cloud. Sentinel-1 sees through cloud
and detects tropical clearings, often earlier than optical sensors (Reiche et al., 2018; Hoekman et al., 2020; Ballère et al., 2021; Ygorra et al., 2021). If radar compensates for optical
scarcity in a general-purpose representation, the concern raised above largely evaporates.
Whether it does is an empirical question that has not been asked of an embedding field, even as
methods for working around optical gaps continue to accumulate (Huang et al., 2026).

### 1.3 The gap

No published work measures the temporal fidelity of an annual embedding field: which events
enter the right year's vector, which are deferred, and what predicts the difference. The
benchmarks that accompany foundation models score label accuracy on downstream tasks and treat
the temporal dimension as a modelling input rather than as a property to be validated
(Marsocci et al., 2024; Ma et al., 2026). Where the temporal behaviour of an embedding is
invoked at all, it tends to be as an assumption in its favour: embeddings built from a full
year of fused observation are described as robust to temporary gaps such as cloud, and are used
as priors for exactly that reason (Belyakov et al., 2026). Our results qualify that
assumption rather than contradict it — a year-long embedding is indeed a stable descriptor of a
place, which is why it survives cloud; what does not survive is the timing of a change that
arrives near the end of the year.

The change-detection literature that works with learned
representations trains detectors on bitemporal pairs or on curated time series (Caye Daudt et al., 2018; Saha et al., 2019; Chen et al., 2021; Chen et al., 2022; Tian et al., 2022; Li et al., 2023; Chen et al., 2024; Lin et al., 2024), and the self-supervised branch pretrains on
seasonal or contrastive objectives before doing so (Manas et al., 2021; Li et al., 2022). Both
are a different question from what an untrained, off-the-shelf annual representation already
contains.

### 1.4 Contributions

We report five things. First, a registration curve for an annual embedding at continental
scale and in two independent years: the probability that a mapped clearing produces a
year-on-year embedding change above a stable-forest threshold, as a function of the number of
clear optical observations after the event. Second, evidence that the deficit is specifically
optical and is not repaired by radar, from a stratified test pre-registered on one year and
confirmed on another. Third, a separation of deferral from omission: events not registered in
their own year almost always register in the next, so the practical failure is a one-year
delay rather than a missing event. Fourth, a demonstration that both the reference map and the
alert vintage used to date events are themselves selective, and that in the Congo Basin this
selectivity currently prevents the question from being answered at all. Fifth, expected-supply
and deferral-risk map layers, and two-tier guidance for users who do and do not possess an
event date.

Each contribution is stated as a claim about a specific, published product rather than about
embeddings in general, and each is accompanied by the sensitivity that would overturn it. We
regard that pairing as part of the contribution: the literature on learned representations for
Earth observation has more results than it has statements about the conditions under which
those results fail, and a user deciding whether to trust an annual vector needs the second kind
more than the first.

We also report a negative result that we believe is more useful than a positive one would have
been: the observation-supply signal that predicts non-registration is unavailable to a rule
that must infer the event year, because computing it requires the date being inferred.

## 2. Data

### 2.1 The annual embedding

Two features of the Brazilian setting make it the right place to ask this question: the
clearing regime has shifted markedly toward small patches that stress any detector
(Kalamandeen et al., 2018), and the national monitoring infrastructure supplies dated,
analyst-drawn reference polygons at continental scale (Picoli et al., 2018).

We use the AlphaEarth Foundations annual embedding field, distributed as
`GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`, for 2018 through 2022 (Brown et al., 2025). Each
image year provides 64 bands at 10 m, and the per-pixel vector has unit norm, so the angle
between two years' vectors is a natural dimensionless change measure. We treat the product
exactly as a user would: no retraining, no fine-tuning, and no access to its internals.

### 2.2 Reference events

Events are DETER polygons of class `DESMATAMENTO_CR` (clear-cut) or `DESMATAMENTO_VEG`
(clearing with residual vegetation) with geodesic area of at least one hectare, in the
Brazilian Legal Amazon, for calendar years 2020 and 2021, obtained from the TerraBrasilis WFS
(Diniz et al., 2015; F. G. Assis et al., 2019). DETER is a near-real-time system in which an
analyst delineates a polygon on an image acquired on a recorded date (`view_date`), which we
use both as an upper bound on the event date and as evidence about the event's own visibility.
The 2021 population contains 37,689 polygons across nine states, the 2020 population 43,316.
Fig. 1 maps their density and locates the two demonstration regions used later for map products.
The distribution is heavily uneven — Pará contributes 14,565 events in 2021, Amazonas 7,801 and
Rondônia 6,108, while Amapá contributes 33 — and this matters because the states differ in
cloud regime as well as in clearing regime. Roraima, the state with the sparsest optical
supply, is also the state with by far the lowest registration rate (0.796 against 0.955 to
1.000 elsewhere), which is the first hint that observation supply rather than clearing type is
the operative variable.

Because DETER is itself optically driven, it will map a clearing late if the clearing is not
visible. To measure that selection rather than inherit it, we add a second population:
polygons that DETER mapped only in the following year but that contain at least one hectare of
high-confidence RADD alerts within the target year. These *optically late* events number
3,082 for 2021 and 2,601 for 2020. The combined populations are 40,771 and 45,917 events,
of which 38,303 and 39,772 carry a usable event date (Section 3.1).

### 2.3 Alerts used for dating

Event dates come from RADD, the Sentinel-1 radar-based disturbance alert product
(Reiche et al., 2021), read over the whole polygon rather than at its centroid. The distinction is
not cosmetic: centroid sampling yields 48–55 % date coverage and a spurious latency of +35 to
+70 days, whereas polygon-wide sampling yields 85–98 % coverage and a latency of −7 to −11 days
(Supplementary Table S3). This correction was made during the study and is reported because it
determines whether the study is possible at all.

### 2.4 Explanatory variables

For each event we count clear Sentinel-2 observations and Sentinel-1 IW acquisitions by
calendar month at the event location, from `COPERNICUS/S2_SR_HARMONIZED` and
`COPERNICUS/S1_GRD`. An observation is clear when the scene classification band is not in
{3, 8, 9, 10, 11}, that is, not shadow, cloud, cirrus or snow. Monthly counts, rather than
totals, are stored so that any dating rule can be applied afterwards without re-extraction.

### 2.5 Thresholds and stable forest

Registration requires a threshold, which we derive per state from undisturbed forest: pixels
classed as undisturbed tropical moist forest in both years of the pair by the JRC Tropical
Moist Forest product (Vancutsem et al., 2021) and not flagged as loss in the surrounding years by
Global Forest Change (Hansen et al., 2013). The threshold τ is the 90th percentile of angular
change over that sample, so that by construction one undisturbed pixel in ten exceeds it.
Values range from 10.20° (Amazonas) to 19.54° (Roraima) for the 2020–2021 pair
(Supplementary Table S1).

### 2.6 The Congo Basin comparison

For a second region we use two 100 × 100 km boxes in the Democratic Republic of the Congo,
selected as the highest-ranking candidates by TMF-mapped 2021 change subject to a 200 km
separation constraint. Events there are TMF 2021 disturbance patches of at least one hectare,
5,243 in total with a median area of 1.61 ha, dated from RADD Africa. The construction differs
from the Brazilian case at every step: a patch is a connected component of pixels whose TMF
class changes from undisturbed moist forest in 2020 to deforested or degraded in 2021, so it is
the output of a model rather than the judgement of an analyst, and its boundary is a
class-transition boundary rather than a delineation of a clearing. The regional threshold,
derived from the same stable-forest procedure, is 16.31°. As Section 4.6 shows,
the reference map and the alert archive available for that region are different enough from
the Brazilian case that we present it as a second instance of reference selection rather than
as a replication.

## 3. Methods

### 3.1 Dating, and a post-hoc redefinition

Every quantity in this paper depends on when the event happened, so the dating rule deserves
more space than it usually receives. Our primary rule is

    date_upper = min(first RADD alert inside the polygon, DETER view_date),

that is, the earlier of the radar alert and the analyst's own detection. The secondary rule,
used throughout as a sensitivity, is the RADD alert alone.

We adopted `date_upper` as primary **after** examining the data, and say so plainly. The
original analysis used the RADD alert alone and produced a registration curve that was
non-monotone at its left end: events with exactly zero post-event clear observations
registered *more* often (69.9 % in 2021, 89.9 % in 2020) than events with one or two
(59.7 % and 72.4 %). A diagnosis of that stratum showed it to be an artefact of the dating
rule rather than a property of the embedding. Among events with no post-event clear
observation, the RADD alert falls *after* the analyst's own detection in 83.8 % of 2021 cases
and 96.8 % of 2020 cases, by a median of 142 and 339 days, against 8.4 % and 15.0 % in the
population at large. Recomputing the observation count from the DETER detection date leaves
only 31.0 % and 8.9 % of them observation-poor. Two rival explanations were tested and
rejected: pre-event disturbance, which predicts elevated prior-year change among the events
that fail to register and is contradicted (3.8 % and 19.8 % of them exceed τ in the prior
year, at or below the ten per cent that τ implies for undisturbed forest); and year-end
truncation, since December supplies only 18.5 % and 4.7 % of the stratum and excluding it
*raises* the stratum's registration rate.

We can offer a plausible mechanism for the lateness but have not tested it. RADD confirms an
alert on subsequent acquisitions, and no RADD archive contemporaneous with 2020 exists, so a
2020 event's first recorded alert may be a re-detection carried by a later snapshot rather than
the original detection. That is a hypothesis consistent with the pattern, not a demonstrated
cause: we observe that the alert date is systematically later than the analyst's, and we do not
observe why. The correction does not depend on the mechanism being right. Taking the minimum
with the analyst's detection date removes most of the error under any explanation of it, and
never moves a date later than the evidence allows. Under `date_upper` the registration curve is monotone from zero upward in
both years and the zero stratum shrinks from 173 to 38 events (2021) and from 1,011 to 50
(2020). We report every headline quantity under both rules and treat the difference between
them as a measurement of dating sensitivity rather than as a nuisance.

### 3.2 Registration

For an event in year *Y*, angular change is

    θ = arccos(⟨e_{Y−1}, e_Y⟩) in degrees,

averaged over the polygon interior, defined as the polygon buffered inward by 10 m so that
edge pixels mixing cleared and intact forest do not dominate small polygons. The event is
*registered* when θ exceeds the state threshold τ. Registration is thus a property of the
embedding and the threshold alone: it does not depend on the event date, a fact we use
repeatedly, since it means the deferral analysis and the offset diagnostic are invariant to
the dating rule.

Two aspects of this definition are choices rather than necessities and were fixed in advance.
The inward buffer of 10 m removes exactly one pixel ring, which is the minimum that guarantees
no interior pixel straddles the polygon boundary at the embedding's own resolution; a larger
buffer would sharpen the contrast but would empty the smallest polygons. The threshold at the
90th percentile of undisturbed forest fixes a nominal false-positive rate of ten per cent per
pixel, before averaging over a polygon, which is deliberately permissive: a stricter threshold
would raise the measured gap, as the p95 rows of Table 1 confirm, so the permissive choice is
the conservative one for our central claim.

### 3.3 Explanatory variables

`clear_post` is the number of clear Sentinel-2 observations between the event date and the end
of the event year, computed from the monthly counts with the event month prorated by the
fraction of days remaining. `s1_post` is the analogous count of Sentinel-1 IW acquisitions.
Both are therefore mechanically bounded by how much of the year remains, which is a
correlation the analysis must handle rather than ignore (Section 3.5).

Because monthly rather than cumulative counts are stored, both `clear_post` and `s1_post` can
be recomputed under any dating rule without returning to the image archive. That is what makes
the dating sensitivity in this paper cheap enough to run on every headline quantity rather than
on one of them, and we recommend the practice: the storage cost is twenty-four numbers per
event, and it converts a dating decision from an irreversible one into a reported one.

### 3.4 Models and inference

The event-level model is a logistic regression of registration on the square root of
`clear_post`, `s1_post`, state fixed effects, event-month fixed effects and an indicator for
optically late events, with an L2 penalty. All confidence intervals in this paper come from a
block bootstrap that resamples 0.5° blocks with replacement and refits, 1,000 draws, following
standard practice for spatially autocorrelated samples (Roberts et al., 2017; Valavi et al., 2018; Ploton et al., 2020; Meyer and Pebesma, 2022). Blocks rather than events are the
resampling unit because clearings cluster along frontiers, so event-level resampling would
give intervals that are too narrow.

Two choices in that specification deserve justification. The square-root transform of
`clear_post` was selected because the untransformed count enters the logit almost linearly over
a range where the response is manifestly saturating, and because it reproduces the reported
coefficients of the earlier stage; the log transform, which fits the marginal curve better
still, is used for the map link in Section 3.7 where calibration rather than partial
inference is the goal. The L2 penalty is present because state and month fixed effects create
near-empty cells in the smaller size classes, where an unpenalised fit separates; at the
penalty used it moves the main-variant coefficient by less than 0.02.

The fitting code used in the earlier stages of this work was not retained. We therefore
rebuilt it from the written specification and validated the reconstruction against the two
coefficients the earlier stage reported, reproducing 0.211 as 0.213 and 0.219 as 0.217. All
point estimates reproduce; two bootstrap intervals do not, and in both cases the earlier
interval was wider. The manuscript prints the re-derived values, and the full
published-versus-re-derived comparison is given in the numbers trace that accompanies this
paper.

### 3.5 Pre-registration record, including two criteria that failed as written

Criteria were fixed before fitting at each stage. Three were substantive. H1″ requires
registration at `clear_post ≤ 2` to be at least five percentage points below registration at
`clear_post ≥ 5`, with the interval of the difference excluding zero and at least 100 events
in the low bin. H3 requires registration at `clear_post ≥ 5` to be at least 95 %. H7 was the
decisive criterion and had two parts: (a) the `clear_post` coefficient must survive
conditioning on `s1_post`, and (b) among events with `s1_post` above its median, registration
at `clear_post ≤ 2` must still be below 80 %.

Criterion H7(b) as written was inestimable, and the reason is instructive. `clear_post` and
`s1_post` are both driven by how much of the year remains after the event, so events with few
optical observations also have few radar acquisitions: exactly one event in 38,303 satisfied
both conditions. The criterion selected an empty stratum. We re-specified it before looking at
the result, as H7(b)′, by measuring radar density *relative to the event's own calendar month*,
which removes the shared dependence on time of year, and confirmed it out of sample on the
2020 population, which had not been examined when the re-specification was fixed.

A fourth criterion, on year attribution, was degenerate for a different reason: every event in
a single-year population has the same true year, so a rule that assigns that year is perfect by
construction. We report the attribution question in the form that can be answered
(Section 4.7) and record the failure rather than a spurious pass.

### 3.6 The polygon-offset diagnostic

A reference polygon can be right about the clearing and wrong about where it is
(Olofsson et al., 2014; McRoberts et al., 2018; Ye et al., 2018; Stehman and Foody, 2019), and the reference
class itself can carry noise that propagates into any validation built on it
(Santos et al., 2021). For every unregistered event we
compare mean angular change in the polygon interior with that in a 50–150 m outer ring. An
event is *offset-suspect* when the ring exceeds τ and the interior does not, that is, when the
change signal sits beside the mapped polygon rather than inside it. This does not require the
event date and so applies identically under both dating rules.

### 3.7 Observation-supply layers

For two demonstration regions we compute, for each calendar month, the mean number of clear
Sentinel-2 observations per pixel over 2019–2021. From that climatology we derive, for an
event occurring in month *m*, the expected remaining clear count under the same proration rule
used for `clear_post`, and convert it to a deferral risk through a one-covariate logistic link
fitted on the dated 2021 events. We fit that link in log space, because the raw-count link used
in an earlier iteration is badly calibrated at the low end, predicting 91 % registration where
one post-event clear observation actually yields 59 %.

## 4. Results

### 4.1 The registration curve

Registration rises monotonically with the number of clear optical observations following the
event, in both years and under both dating rules (Fig. 2). Under the primary rule, in 2021 an
event followed by at least five clear observations registers with probability 0.975
[0.972, 0.978], and one followed by two or fewer registers with probability 0.510
[0.438, 0.584]; the gap is **46.5 percentage points [39.0, 53.6]** on 361 low-observation
events out of 38,303. In 2020 the corresponding values are 0.981 [0.979, 0.984], 0.606
[0.541, 0.669] and a gap of **37.5 points [31.3, 43.9]** on 439 of 39,664. H1″ and H3 are met
in both years.

The bins plotted in Fig. 2 exclude the exactly-zero stratum, which is reported separately for
the reason given in Section 3.1, so the leftmost plotted bin is the half-open interval (0, 2]
rather than the closed interval [0, 2] used for the H1″ statistic. Bin by bin the 2021 curve
runs 0.536, 0.743, 0.861, 0.920, 0.968 and 0.981 over (0, 2], (2, 4], (4, 6], (6, 9], (9, 14]
and 14+, and the 2020 curve 0.620, 0.793, 0.893, 0.954, 0.975 and 0.985. Pooling the zero
stratum back in reconciles the two: 0.536 on 323 events and 0.289 on 38 give 0.510 on 361 in
2021, and 0.620 on 389 with 0.500 on 50 give 0.606 on 439 in 2020, which are the H1″ values
quoted above.

Two features of these numbers matter more than their magnitude. The first is that the ceiling
is high and the floor is low: an annual embedding registers essentially every clearing it is
given a reasonable chance to see, and misses between a third and a half of those it is not.
The second is that the two years agree. Under the RADD-only rule they did not — the same gap
was 34.4 points [27.8, 40.3] in 2021 but only 14.1 [11.4, 16.7] in 2020, and the discrepancy
was previously attributed to a real difference between years. It was not: it was a dating
artefact, produced by the absence of a RADD archive contemporaneous with 2020 events, and it
largely disappears once the analyst's own detection date is allowed to bound the event date.
This is the clearest demonstration we can offer that the effect size of this kind of study is
set by dating accuracy.

Under the primary rule the low-observation bin is also what the mechanism predicts it should
be: 97.8 % of it falls in October to December. It is a population of late-year clearings, not
a scattering of unlucky ones.

The effect is not confined to a size class or a state. Splitting 2021 by polygon area, the gap
is 40.6 points [33.8, 47.3] for events between 5 and 25 ha and 65.7 points [52.7, 75.2] for
events of 25 ha or more; the smallest class holds only two low-observation events and is
uninformative. That the largest clearings show the largest gap is worth pausing on, because it
rules out the most obvious alternative explanation. If the deficit were a detection-threshold
problem — small changes failing to move a vector far enough — it would shrink with size. It
grows. Large late-year clearings are exactly the events an annual product is least entitled to
miss, and they are the ones most often deferred.

### 4.2 The deficit is optical, and radar does not compensate

If the deficit merely reflected an absence of *any* observation, Sentinel-1 — which is
unaffected by cloud and acquires on a fixed orbit schedule — would fill the gap. It does not.

The pre-registered stratified test, re-specified as H7(b)′ after the original form selected an
empty stratum (Section 3.5) and confirmed out of sample on 2020, compares low-observation
events whose radar density is at or above their own month's median with those below it
(Fig. 3a). In 2021 the radar-dense stratum registers 0.447 [0.348, 0.554] on 152 events,
against 0.555 on the radar-sparse stratum; in 2020, 0.538 [0.436, 0.646] on 169 events against
0.648. Both satisfy the criterion in all three of its parts: below the 0.80 bar, an upper
interval bound below 0.85, and below the radar-sparse stratum. Radar-rich low-optical events
register *less* often, not more.

The monotone version of the same statement is Fig. 3b. Sorting low-observation events into
quartiles of within-month radar density, registration in 2021 runs 0.593, 0.556, 0.467, 0.422
from sparsest to densest, and in 2020 0.627, 0.718, 0.541, 0.537. The 2021 series declines
monotonically; the 2020 series peaks in the second quartile at 0.718 before falling, so the
relationship is not monotone in both years. What is common to both is the end point that
matters for the argument: the densest radar quartile registers lowest of the four, at 0.422 in
2021 and 0.537 in 2020, and in neither year does it approach the rate of the well-observed
population. The explanation is not that radar destroys information. Sentinel-1 acquisition follows a
fixed observation plan, so within-month radar density is set almost entirely by where a pixel
sits relative to the overlap of adjacent orbit swaths, and is close to independent of the
weather that governs optical supply. Conditioning on it therefore does not select
better-observed events in the sense that matters; it selects a different part of the
acquisition geometry, and within the low-optical population those parts are not the easier
cases. What the pattern establishes is the negative claim we need: whatever Sentinel-1
contributes to the annual vector is not enough, on its own, to carry a clearing across a
threshold calibrated on undisturbed forest.

It is worth being explicit about what this test does and does not establish. It does not show
that Sentinel-1 is uninformative about clearing; the alert product we use for dating is built
from Sentinel-1 and detects these same events. It shows that whatever radar information reaches
the annual embedding is insufficient, on its own, to carry a clearing past a threshold
calibrated on optical-dominated variation in undisturbed forest. Those are different claims,
and the second is the one relevant to a user differencing annual vectors. The negative slope
across radar-density quartiles is best read not as radar harming registration but as radar
density being a poor substitute variable: it varies with orbit geometry and latitude, and where
it is highest the optical deficit tends to be most severe, so conditioning on it selects harder
cases rather than better-observed ones.

The parametric form of the test, H7(a), asks whether the `clear_post` coefficient survives
conditioning on `s1_post`. Under the primary dating rule it survives, but only just, and this
is a real weakening that we do not paper over (Table 1). In 2021 the joint coefficient is
0.083 with a bootstrap interval of [0.000, 0.172]; in 2020 it is 0.112 [0.010, 0.252]. Under
RADD-only dating the same coefficients are 0.217 [0.111, 0.327] and 0.318 [0.221, 0.419]. The
reason for the attenuation is understood: `date_upper` moves event dates earlier, which raises
both `clear_post` and `s1_post` together and increases their collinearity, so the partial
coefficient of one given the other shrinks even as the marginal relationship strengthens.

**Table 1. H7(a) sensitivity: the `clear_post` coefficient conditional on `s1_post`, under the
primary dating rule, with 0.5° block-bootstrap intervals.** Variants marked ✘ have an interval
that includes zero.

| variant | 2021 coefficient [CI] | 2020 coefficient [CI] |
|---|---|---|
| main (τ = state p90) | 0.083 [0.000, 0.172] | 0.112 [0.010, 0.252] |
| τ = state p85 | ✘ 0.069 [−0.024, 0.160] | 0.138 [0.012, 0.296] |
| τ = state p95 | ✘ 0.059 [−0.009, 0.135] | 0.120 [0.022, 0.232] |
| high-confidence alerts only | 0.113 [0.034, 0.199] | not available † |
| RADD-only dating | 0.217 [0.111, 0.327] | 0.318 [0.221, 0.419] |
| excluding optically late events | 0.252 [0.107, 0.428] | 0.289 [0.150, 0.455] |
| area < 5 ha (n low bin = 2 / 5) | ✘ 0.003 [−0.788, 0.961] | ✘ 0.476 [−0.331, 1.126] |
| area 5–25 ha | 0.165 [0.058, 0.273] | 0.197 [0.085, 0.345] |
| area ≥ 25 ha | 0.146 [0.035, 0.279] | 0.181 [0.059, 0.402] |

† The high-confidence variant cannot be computed for 2020. The 2020 event table records the
high-confidence alert date but `clear_post` was never extracted under it, and recomputing it
would require re-running the monthly observation extraction for that year.

The coefficient is positive in every variant of both years and its interval excludes zero in
thirteen of sixteen estimable cases; the exceptions are the two threshold variants in 2021 and
the smallest size class, which has two and five low-observation events respectively and is
simply underpowered. Our reading is that H7(a) is directionally robust but marginal under the
primary dating rule, and that the weight of the SAR argument rests on the stratified test and
on the quartile pattern, not on the partial coefficient.

### 4.3 Deferral, not omission

Events that fail to register in their own year almost always register in the next. Of the 2021
events unregistered in 2021, 96.5 % [95.3, 97.4] register in 2022 against a separately
estimated 2021–2022 threshold; of the 1,107 events unregistered in 2020, 94.1 %
[92.3, 95.7] register in 2021 (Fig. 4). Both directions are re-derived here, the 2020
direction by refetching the reference polygons and recomputing the 2020–2021 angular change
against the next year's own state threshold. Roughly one event in 800 registers in neither year. Because
registration does not depend on the event date, this result is invariant to the dating rule.

The residual matters for how the result should be described. An event that registers in
neither year is a genuine omission, and there are 47 of them in 2021 and 66 in 2020. Inspection
of the offset diagnostic suggests that a substantial share of even these are reference-map
problems rather than embedding failures: they are concentrated among events whose ring signal
also fails to exceed the threshold, which is the signature of a polygon drawn where little
detectable change occurred, rather than of a clearing the embedding could not see. We do not
claim to have adjudicated them individually, and the honest summary is that the true omission
rate is at most one event in 800 and plausibly lower.

The practical failure mode of an annual embedding is therefore a one-year delay rather than a
missing event, and that is a materially different problem for users. A change map built by
differencing consecutive annual embeddings will find nearly all clearings; it will place a
minority of them in the wrong year, with the minority concentrated in the last quarter.

### 4.4 The reference map is selective, and what it selects are weaker changes

Clearings that DETER mapped only in the following year, but that RADD confirms within the
target year, register at 0.753 in 2021 and 0.776 in 2020, against 0.984 and 0.986 for events
DETER mapped contemporaneously (Fig. 5a). This is a population invisible to any study anchored
solely on an annual reference map, and it is large: 3,082 and 2,591 events.

The obvious explanation is that these are events the satellites did not see, but that is not
what the data show. The primary dating rule cannot correct them — an optically late event's
DETER date lies in the following year, so the minimum with the alert date never binds, and
their `clear_post` is identical under both dating rules — which means their observation counts
come entirely from the alert date, the least corrected dating available. Even so they are only
mildly observation-poor: median post-event clear count 23.0 against 23.7 in 2021, though with a
heavier low tail (3.8 % against 0.7 % of events in the low-observation bin). In 2020 the tail
is heavier still, 17.0 against 22.7 at the median. Adjusting the registration deficit for
observation supply, radar density, state, event month and polygon area removes about two fifths
of it and no more: 23.0 points [19.9, 26.2] falls to **14.2 points [12.3, 16.4]** in 2021, and
20.8 [18.1, 23.7] to **13.3 [11.1, 15.6]** in 2020 (Fig. 5c).

What separates them is the intensity of the change itself. Expressed as a multiple of the
event's own state threshold, the interior angular change of an optically late clearing has a
median of 1.37 τ in 2021 against 2.92 τ for contemporaneously mapped clearings, and 1.44 τ
against 2.99 τ in 2020; the whole distribution is displaced, not just its tail, with quartiles
of 1.01–1.88 τ against 2.13–3.72 τ (Fig. 5b). Within the same adjustment as above, an optically
late event's change is **0.56 [0.54, 0.58]** of a comparable contemporaneously mapped event's
in 2021 and **0.60 [0.57, 0.62]** in 2020. Polygon area is not the difference — medians of
14.2 against 13.0 ha in 2021 — and neither is alert confidence, since every optically late
event carries a high-confidence alert by construction against 99.4 % of the rest.

So the deficit is an intensity effect rather than an observation effect, and the two are
distinguishable here because the adjustment controls one while measuring the other. Part of the
statement is definitional, since registration is by construction the event of intensity
exceeding τ; the content that is not definitional is that the intensity shift survives
conditioning on observation supply and composition, and that supply accounts for under two
fifths of the registration gap. The reading we take from this is that a clearing which is
incomplete, partially vegetated or spread across a year is both harder for an analyst to
delineate in the year it begins and genuinely produces less annual embedding change — the
reference map's lateness and the embedding's silence share a cause rather than one explaining
the other. This also cuts in a conservative direction for the paper's central estimate:
excluding these events *lowers* the gap in 2021 from 46.5 to 40.6 points but raises the
conditional coefficient from 0.083 to 0.252.

### 4.5 Polygon geometry accounts for part of the residual

Among unregistered events, the change signal frequently sits beside the mapped polygon rather
than inside it: 45.6 % of the 1,332 unregistered 2021 events and 48.0 % of the 1,102
unregistered 2020 events are offset-suspect, with a ring exceeding τ and an interior that does
not (Fig. 7). Removing them from the 2021 population lowers the gap from 46.5 to 39.3 points
[31.2, 47.0] and raises the conditional coefficient from 0.083 to 0.211 [0.090, 0.340]. The
diagnostic is a positional-error check in the tradition of reference-data quality assessment
(Olofsson et al., 2014; McRoberts et al., 2018), and the conclusion is that geometric mismatch
between a hand-drawn polygon and a 10 m embedding explains part but not most of the deficit.
The worked examples in Fig. 7 also show the other kind of residual: unregistered events where
neither the interior nor the ring exceeds τ, that is, where nothing the embedding can see
happened at all.

### 4.6 The Congo Basin: a second case of reference selection

We set out to replicate the Brazilian result in the Congo Basin and cannot, for reasons that
are themselves the finding.

Using the RADD Africa archive available in Earth Engine — whose earliest snapshot post-dates
the events by more than two years — the Congo gap is 5.34 points [2.91, 8.20] on 202
low-observation patches, far below the Brazilian estimates. Re-dating the same patches against
a 2021-contemporaneous alert vintage obtained from the Global Forest Watch Data API dissolves
that stratum: 3.4 % of the later-vintage dates fall in 2022, after the observation year, which
forces the post-event count to zero mechanically and manufactures most of the low-observation
bin the estimate rested on. Under the contemporaneous vintage the low-observation bin holds
eight patches, below the pre-registered floor of 100, and no gap is estimable (Fig. 6).

The vintage also censors in the opposite direction. Coverage falls from 94.4 % to 90.4 %, and
of the 260 patches that lose their date entirely, 58.5 % had been in the low-observation bin —
because a clearing late in 2021 has not yet accumulated a confirmed alert by the vintage's
January 2022 cutoff. Between the two vintages, 11.0 % of dates move by more than 30 days.
What survives is the qualitative result: the conditional `clear_post` coefficient on the
re-dated Congo data is 0.737 [0.190, 1.349], excluding zero.

The Congo reference map differs from the Brazilian one in kind as well as in dating. TMF
patches are model-derived annual class transitions with a median area of 1.61 ha, eight times
smaller than DETER polygons and produced by an entirely different process. We therefore
present the Congo not as a failed replication but as a second demonstration that what a study
like this can measure is bounded by the reference map and the alert archive it can obtain.

### 4.7 Products, and a negative result on year attribution

For two demonstration regions we publish the expected clear-observation supply by calendar
month (Fig. 8) and the deferral risk it implies for each event month (Fig. 9), together with
angular change, registration and deferral layers at 100 m (Figs. M1, M2). The supply
climatology is strongly seasonal and, importantly, the two regions are out of phase: the
Pará region peaks in July at 6.5 clear observations and floors in February at 1.0, while the
Roraima region peaks in March at 4.4 and floors in June at 1.3. A single seasonal correction
would be wrong for one of them. Within a region the supply is banded by Sentinel-2 orbit
overlap, with the 90th percentile of monthly supply roughly three times the 10th in every
month, so two clearings a few kilometres apart can face very different odds in the same month.
Converted to risk, an event in January to August carries a deferral probability near 0.02,
rising to 0.354 in Pará and 0.306 in Roraima for a December event, with the orbit-overlap
bands near 0.25 against 0.40 on single-swath ground.

The map layers are published at 100 m for the embedding-derived quantities and 200 m for the
supply climatology, resolutions set by the practical limits of extracting a 64-band product
over a 200 km region rather than by the science. That is a real constraint on this kind of work
and worth recording: computing an angular change field from an annual embedding is inexpensive
per pixel and expensive per region, because the sixty-four bands must be mosaicked before they
can be reduced. Users wanting native 10 m output should expect to tile aggressively.

The obvious next step — using observation supply to *correct* a year label after the fact —
does not work, and the reason is worth stating. `clear_post` predicts non-registration well
(area under the curve 0.729 and 0.712 for 2020 and 2021), but it is unavailable to an
attribution rule, because computing it requires the event date the rule is trying to infer.
Substituting the quantity that *is* available without a date — the annual clear-observation
count of the candidate prior year — collapses the signal: the area under the curve for
predicting deferral falls to 0.599, the fitted rule never fires, and it reduces misattribution
by 0.0 % [0.0, 0.0] against the naive rule on a held-out year of 38,256 events. Observation
supply cannot repair year attribution from the outside. What does work is trivial and worth
saying anyway: accepting a two-year window rather than a one-year label cuts misattribution
from 3.48 % to 0.12 %.

## 5. Discussion

### 5.1 Two-tier guidance for users

The results support a simple decision rule that depends on one thing: whether the user has an
independent event date.

A user who has one — from an alert product, a field record, a permit database or an analyst's
delineation — can compute the post-event clear-observation count directly and use it as a
confidence flag. Below about five clear observations the annual embedding registers the event
with probability between one half and nine tenths depending on the year and the threshold, and
above about fourteen it registers with probability above 0.98. The count is the single most
informative covariate we found, and it is cheap: it needs only the scene classification band
of the same imagery the embedding already consumes. We recommend reporting it alongside any
embedding-derived change label, in the same way a per-pixel uncertainty is reported alongside
a biomass estimate.

A worked example makes the flag concrete. A user mapping 2021 clearing in the Pará
demonstration region by differencing annual embeddings, who also holds RADD alerts, would
compute for each detected patch the number of clear Sentinel-2 observations between the alert
date and the year's end. Patches with fourteen or more — the large majority, since the region's
annual supply averages 39 clear observations — carry a registration probability above 0.98 and
need no qualification. Patches with two or fewer, which in this region means almost exclusively
November and December alerts, carry a probability near one half, and the appropriate action is
not to discard them but to re-check them against the following year's embedding, where
Section 4.3 says they will almost certainly appear. The flag converts an invisible,
seasonally structured bias into an explicit, per-event caveat.

A user who has no event date should not attempt to recover the year from observation supply,
because Section 4.7 shows it cannot be done. The alternative is to widen the label: treat an
embedding-derived change as evidence of clearing in a two-year window ending in the year of
first registration. That costs temporal precision and buys almost all of the accuracy back,
reducing misattribution from 3.48 % to 0.12 %. For applications with a hard annual boundary —
a regulatory cut-off, an inventory period — the honest statement is that a differenced annual
embedding is not on its own an adequate instrument, and should be paired with an alert product
whose latency is measured (Bullock et al., 2022; Reiche et al., 2024). Intercomparisons of
the operational products available in Brazil provide a starting point for that pairing
(Potapov et al., 2026).

### 5.2 Expected-supply maps as a planning instrument

The deferral-risk layer is a *prior*, computed before any event is observed, that says how
likely a clearing in a given pixel and month is to be recorded in the right annual vector. It
conditions on nothing but location and month, and it is calibrated on Brazilian DETER polygons
in 2021, so it should not be read as a per-pixel probability for another region or another
reference standard. Within those limits it has two uses. It tells a monitoring programme where
and when an annual product will be least reliable, which is actionable in a way that a global
accuracy figure is not; and it makes visible a structure that is otherwise invisible, namely
that observation supply is banded by orbit overlap, so reliability has a spatial pattern
inherited from acquisition geometry rather than from ecology.

An earlier iteration of this layer illustrates the failure mode to avoid. It applied the same
logistic link to the *annual* clear-observation count rather than the post-event count, which
is the quantity the link was fitted on. The result looked reasonable and was nearly
uninformative: the annual count predicts deferral with an area under the curve of 0.599, and
the raw-count link predicted 91 % registration where the data give 59 %. We retired that layer
rather than reinterpret it, and record it here because the mistake is easy to make and hard to
see in a map.

### 5.3 What this implies for benchmarking foundation models

Benchmarks for geospatial foundation models score downstream label accuracy on curated tasks
(Marsocci et al., 2024), which is the right first question and an incomplete one. A model can
score well on every such task and still place a third of late-year clearings in the wrong year,
because the benchmark's labels are usually drawn from the same annual products whose temporal
semantics are in question, and because the evaluation is rarely stratified by anything to do
with acquisition. The evaluation we describe here is cheap to add and does not require any
model internals: take an independently dated event set, compute a registration rate as a
function of post-event observation count, and report the curve rather than a single number.
Any representation that ingests optical imagery can be scored this way, and the score is
directly interpretable by users as a confidence flag.

We would go further and argue that temporal fidelity deserves the status that spatial
validation now has in the ecological-mapping literature, where it took a sequence of papers
showing inflated accuracy under naive validation before blocked designs became standard
practice (Roberts et al., 2017; Ploton et al., 2020; Meyer and Pebesma, 2022). The analogous
naive assumption here is that a year label means the year; the analogous correction is to
validate against events whose dates come from outside the product being tested.

### 5.4 Every effect size here is a lower bound

Event dates carry error, and `clear_post` is computed from them. Classical measurement-error
theory says that error in a covariate attenuates its estimated effect toward the null
(Carroll et al., 2006), so every gap and every coefficient we report understates the true
relationship by an unknown amount. Three pieces of evidence in this paper show the attenuation
operating rather than merely postulating it. Moving from RADD-only dating to `date_upper`
raised the 2021 gap from 34.4 to 46.5 points and the 2020 gap from 14.1 to 37.5. Excluding
events whose reference polygon is geometrically offset raised the conditional coefficient from
0.083 to 0.211. Re-dating the Congo patches on a contemporaneous alert vintage removed a
low-observation stratum that turned out to be composed largely of dates falling outside the
observation year altogether.

The corollary for readers is that the numbers in Section 4 should be read as a floor. The
corollary for practitioners is sharper: a study of this kind is only as good as its worst
dating, and reporting the alert vintage is not optional. In the Congo case the choice of
vintage moved the answer from "a small but significant effect" to "not estimable".

### 5.5 Relation to the alert-latency literature

The alert community has developed a precise vocabulary for this class of problem: detection
delay, confirmation lag, and the trade-off between the two (Tang et al., 2019; Bullock et al., 2022; Reiche et al., 2024). What we describe is the same phenomenon displaced onto a product that
does not present itself as an alert and therefore is not usually held to that standard. An
annual embedding has, in effect, a detection delay that is zero for a January clearing and one
year for some fraction of December clearings, and the fraction is set by cloud climatology and
orbit geometry rather than by an algorithmic confirmation rule.

Framed that way, our expected-supply layer is the embedding analogue of the alert-latency maps
that accompany operational alert systems, and our two-year window is the analogue of a
confirmation threshold. The difference is who bears the cost of the choice. An alert system
picks its confirmation rule and publishes the resulting latency; an annual embedding leaves the
equivalent choice implicit, and the user discovers it, if at all, as an unexplained
discrepancy against a reference product.

### 5.6 What an annual embedding field is, and is not, for

One further reading of the results deserves stating, because it is the one a sceptical reader
should test first: that the low-observation events are simply harder events — smaller, more
partial, more ambiguous — and that observation count is a proxy for difficulty rather than a
cause of non-registration. It is the same class of question as asking whether a time-series
detector's accuracy depends on the disturbance agent and its severity rather than on the site's
history (Rodman et al., 2021).

Section 4.4 shows that this mechanism is real, and shows exactly where it operates. Clearings
the reference map records a year late produce 0.56–0.60 of the annual embedding change of
otherwise comparable clearings it records on time, an intensity difference that survives
conditioning on observation supply, state, month and area. Those events are, in the relevant
sense, harder — and the embedding's silence and the analyst's lateness share that cause rather
than one explaining the other.

What that finding does not do is explain the main result, and three things separate the two.
The gap along the observation axis grows rather than shrinks with polygon size (Section 4.1),
where a difficulty account predicts the opposite. It survives excluding the optically late
events entirely — the conditional coefficient triples when they are removed (Section 4.4) —
so the population in which intensity demonstrably differs is not the population carrying the
gap. And the deferral result shows the same events, with the same polygons and the same
intensity, registering at 94–97 % one year later, when the observations have arrived
(Section 4.3). Difficulty does not resolve itself after twelve months; observation supply does.
The honest summary is that both mechanisms exist in this data, that they act on different
subpopulations, and that the design separates them rather than having to choose between them.

The picture that emerges is coherent and, we think, reassuring about the product while
cautionary about one specific use. An annual embedding field is an excellent detector of
clearing that has been optically observed after the fact: at five or more clear observations
it registers 97.5–98.1 % of expert-mapped clearings with no training data at all. That is a
strong result for a general-purpose representation, and it supports the use of differenced
annual embeddings for mapping *where* clearing has occurred over a multi-year window.

It is a weak instrument for *when*, and weak in a structured rather than a random way. The
events it defers are late-year events in cloudy places, which are not a random subset of
clearings in either space or time: they concentrate in the last quarter, in specific states,
and between orbit-overlap bands. Any downstream statistic that is computed per year — an
annual rate, a year-on-year change, a compliance test against a cut-off date — inherits that
structure. The remedy is not to distrust the embedding but to stop asking it a question it was
never constructed to answer, and to pair it with an instrument that was.

This also suggests what a future version of such a product could publish alongside the
embedding: a per-pixel count of the clear observations that entered each annual vector. That
single band would let any user compute the confidence flag of Section 5.1 without an event
date and without reprocessing the source archive, and it would cost the producer almost
nothing, since the count is a by-product of building the composite.

## 6. Limitations

The reference map is optically selected. DETER analysts work from optical imagery, so
clearings that are hard to see are mapped late or not at all. We measure that selection
directly by adding optically late events (Section 4.4), and it does not disappear: those
events register 23 points lower than contemporaneously mapped ones for reasons that
observation scarcity explains only partially.

The primary dating rule was chosen after seeing the data. Section 3.1 states the reasoning and
the diagnosis that motivated it, and every headline quantity is reported under the
pre-registered RADD-only rule as well, but a reader who prefers the pre-registered rule should
take the smaller gaps of 34.4 and 14.1 points as the headline and read the rest accordingly.
We think that would be the wrong choice, because the diagnosis showing RADD-only dates to be
systematically late is itself evidence, but the choice is visible rather than hidden.

The conditional-coefficient test is marginal under the primary rule. In 2021 the interval's
lower bound is 0.000 to three decimal places, and it includes zero under two of the three
threshold settings. We rest the SAR conclusion on the stratified test and the quartile
pattern, which are robust in both years, and report the coefficient as directionally robust
but not decisive.

The reconstructed model does not reproduce two published intervals. Point estimates reproduce
throughout; two bootstrap intervals from the earlier stage are wider than the reconstruction's
and the discrepancy cannot be attributed, because the original code was not retained. Both
concern intervals rather than signs, and in both cases the published interval was the more
conservative.

Thresholds in two states rest on small stable-forest samples. Maranhão and Tocantins did not
reach the intended 2,000-pixel floor, and together hold under one per cent of events; their
thresholds should be regarded as provisional.

The Congo comparison is not a replication and is currently not answerable. The reference map
is model-derived and eight times finer-grained, and the alert archives available either
post-date the events by two years or censor the late-year events that the test needs. We
report what the vintage does rather than an effect size.

Covariates are sampled at polygon centroids while registration is measured over polygon
interiors. For events of the sizes studied here the difference is small, but for a clearing
that straddles an orbit-overlap boundary the centroid count may misrepresent the polygon, and
the effect would be to add noise to `clear_post` — attenuating the reported relationship rather
than creating it. The 2020 Sentinel-1 re-extraction returned values for 39,664 of 39,772 dated
events; the 108 missing events are dropped from the 2020 primary analysis.

Finally, the analysis covers two years in one biome, with a Congo Basin case that could not be
completed. Whether the same curve holds in drier forests, in plantations, or under a different
national reference standard is untested, and the deferral-risk layer in particular is
calibrated on a single region-year.

## 7. Conclusions

We measured the temporal fidelity of a global annual embedding field against 77,967
expert-mapped clearings in the Brazilian Legal Amazon over two years, and found that it is
governed by the supply of clear optical observation after the event. Registration saturates at
97.5–98.1 % where five or more clear Sentinel-2 observations follow the clearing and falls to
51.0–60.6 % where two or fewer do, a gap of 46.5 and 37.5 percentage points in the two years.
Radar acquisition does not compensate: among low-observation events, registration falls as
Sentinel-1 density rises, in both years and in a test pre-registered on one of them.

The failure is a deferral rather than an omission. Between 94.1 % and 96.5 % of events not
registered in their own year register in the next, and roughly one in 800 registers in
neither. Users therefore lose a year, not an event — but they lose it selectively, in the last
quarter of the year and in the cloudiest places, which is precisely the structure that
corrupts an annual statistic.

Two methodological findings travel beyond this product. Dating accuracy sets the effect size:
correcting a systematically late alert date changed the 2020 estimate from 14.1 to 37.5 points
and reconciled two years that had appeared to differ. And observation supply, which predicts
deferral well when the event date is known, cannot repair year attribution when it is not,
because computing it presupposes the answer. The remedy for the user without a date is a
two-year acceptance window; the remedy for the producer is to publish the per-pixel clear
observation count that went into each annual vector.

## Figure captions

**Fig. 1.** Study area. Density of 2021 DETER clearing events across the Brazilian Legal
Amazon, counted on a 0.25° grid and divided by each cell's true ground area, with the Legal
Amazon limit in black and state boundaries in grey; the nine states contributing events are
labelled. Red boxes mark the two demonstration regions whose map products appear in Figs. 8, 9,
M1 and M2. The upper inset locates the Legal Amazon in South America; the lower inset shows the
two Congo Basin boxes of Section 4.6 within the Democratic Republic of the Congo. EPSG:4326.
Double column.

**Fig. 2.** Registration probability against the number of clear Sentinel-2 observations
following the event, for (a) 2021 and (b) 2020. Solid lines and shaded bands are the primary
`date_upper` dating rule with 0.5° block-bootstrap intervals; dashed lines with open markers
are the RADD-only sensitivity. The exactly-zero stratum is drawn separately, on the shaded
band at the left, because under RADD-only dating it is a dating artefact rather than the left
end of the curve (Section 3.1). Sample sizes are printed beside the zero stratum; the dotted
line is the pre-registered 0.95 floor for H3. Double column.

**Fig. 3.** Radar does not compensate for optical scarcity. (a) Registration among events with
two or fewer post-event clear observations, split at the median Sentinel-1 density *of the
event's own calendar month*, with the pre-registered 0.80 bar. (b) The same population sorted
into within-month radar-density quartiles. Both panels use the primary dating rule; error bars
and intervals are 0.5° block bootstraps. Double column.

**Fig. 4.** Deferral rather than omission: the share of events unregistered in year *Y* that
register in *Y*+1, against an independently estimated next-year threshold. Both directions are
re-derived, with 0.5° block-bootstrap intervals. Single column.

**Fig. 5.** Clearings that the reference map records late. (a) Registration for events DETER
mapped in the target year against events it mapped only the following year but that RADD
confirms within the target year. (b) Distribution of interior angular change in units of the
event's own state threshold τ, for both groups and both years: the late group's distribution is
displaced toward τ rather than merely tailed, so these are weaker changes. (c) The registration
deficit before and after adjusting for post-event clear observations, radar density, state,
event month and polygon area; adjustment removes about two fifths of it. Error bars are 0.5°
block bootstraps. Double column.

**Fig. 6.** Reference selection decides what is measurable. (a) The share of events falling in
the low-observation bin, for the two Brazilian years and for the Congo patches under two alert
vintages. (b) What the alert vintage does to the Congo event set: dating coverage under each
vintage, the share of dates that move by more than 30 days, and the share that lose their date
entirely. (c) The registration gap where it is estimable; the Congo panel is empty because the
low-observation bin holds eight patches under contemporaneous dating, below the pre-registered
floor of 100. Double column.

**Fig. 7.** The polygon-offset diagnostic, four worked examples. Columns are individual events;
rows are a pre-event Sentinel-2 composite, a post-event composite and the annual angular-change
field. The DETER polygon is solid, the 50–150 m ring dotted. The two left-hand events are
flagged offset-suspect — the change signal lies beside the polygon — while the two right-hand
events show no change above threshold anywhere, the other kind of residual. Double column.

**Fig. 8.** Expected clear Sentinel-2 observation supply by calendar month, 2019–2021 mean, for
the two demonstration regions. Sentinel-2 orbit overlaps are directly visible as bands of
roughly doubled supply. The lower panel gives the region means; the two regions are out of
phase. Double column.

**Fig. 9.** Deferral risk implied by the supply climatology for an event occurring in each of
four months, and the full monthly profile below. Risk is one minus the fitted registration
probability at the expected remaining clear count. Double column.

**Fig. M1, M2.** Map plates for the Pará / BR-163 and southern Roraima regions at 100 m:
(a) 2020→2021 angular change, (b) registration against the state threshold, (c) pixels
unregistered in 2021 that register in 2022. Graticule, scale bar, north arrow and locator
inset on each plate. Double column.

## Data and code availability

The event tables, the model and its block bootstrap, the extraction scripts, the figure code and
the 100 m map layers for both demonstration regions are archived at
Zenodo, https://doi.org/10.5281/zenodo.[DOI TBD], under CC BY 4.0 for the data and MIT for the
code. The working repository, including the full analysis history that precedes this manuscript,
is at https://github.com/yjchoi83/AEF; the manuscript, its numbers trace and everything needed to
regenerate the figures are under `aef_explore/paper/`.

Because the fitting code from an earlier stage of this work was not retained, the model used
here is a reconstruction validated against the coefficients that stage reported; the
published-versus-re-derived comparison is Table S10, and the reconstruction itself is in the
archive as `model_code/p2_model.py`.

The source products are public and are named in Section 2: the AlphaEarth Foundations annual
embedding, Sentinel-1 and Sentinel-2, DETER, RADD, JRC Tropical Moist Forest and Global Forest
Change. The Congo re-dating additionally uses `wur_radd_alerts` version `v20220109` from the
Global Forest Watch Data API, which requires a free API key.

## Acknowledgements

[TBD]

## References

Elsevier Harvard (author–date). Generated from `references.bib` by `code/render_rse.py`; every entry is the metadata registered at the DOI.

Ballère, M., Bouvet, A., Mermoz, S., Le Toan, T., Koleck, T., Bedeau, C., André, M., Forestier, E., Frison, P.L., Lardeux, C., 2021. SAR data for tropical forest disturbance alerts in French Guiana: Benefit over optical imagery. Remote Sensing of Environment 252, 112159. https://doi.org/10.1016/j.rse.2020.112159

Belyakov, N., Illarionova, S., Rubin, I., Shadrin, D., Burnaev, E., 2026. Geospatial Priors from Alphaearth Foundations for Cloud-Robust Satellite Image Restoration. 2026 11th International Conference on Electronic Technology and Information Science (ICETIS), 481–486. https://doi.org/10.1109/icetis70504.2026.11633492

Bogaert, P., Lamarche, C., Defourny, P., 2022. Hidden Markov Models for Annual Land Cover Mapping—Increasing Temporal Consistency and Completeness. IEEE Transactions on Geoscience and Remote Sensing 60, 1–14. https://doi.org/10.1109/tgrs.2021.3123738

Brown, C.F., Brumby, S.P., Guzder-Williams, B., Birch, T., Hyde, S.B., Mazzariello, J., Czerwinski, W., Pasquarella, V.J., Haertel, R., Ilyushchenko, S., Schwehr, K., Weisse, M., et al., 2022. Dynamic World, Near real-time global 10 m land use land cover mapping. Scientific Data 9 (1). https://doi.org/10.1038/s41597-022-01307-4

Brown, C.F., Kazmierski, M.R., Pasquarella, V.J., Rucklidge, W.J., Samsikova, M., Zhang, C., Shelhamer, E., Lahera, E., Wiles, O., Ilyushchenko, S., Gorelick, N., Zhang, L.L., et al., 2025. AlphaEarth Foundations: An embedding field model for accurate and efficient global mapping from sparse label data. arXiv. https://doi.org/10.48550/ARXIV.2507.22291

Bullock, E.L., Healey, S.P., Yang, Z., Houborg, R., Gorelick, N., Tang, X., Andrianirina, C., 2022. Timeliness in forest change monitoring: A new assessment framework demonstrated using Sentinel-1 and a continuous change detection algorithm. Remote Sensing of Environment 276, 113043. https://doi.org/10.1016/j.rse.2022.113043

Carroll, R.J., Ruppert, D., Stefanski, L.A., Crainiceanu, C.M., 2006. Measurement Error in Nonlinear Models. Chapman and Hall/CRC. https://doi.org/10.1201/9781420010138

Caye Daudt, R., Le Saux, B., Boulch, A., 2018. Fully Convolutional Siamese Networks for Change Detection. 2018 25th IEEE International Conference on Image Processing (ICIP), 4063–4067. https://doi.org/10.1109/icip.2018.8451652

Chen, J., Yuan, Z., Peng, J., Chen, L., Huang, H., Zhu, J., Liu, Y., Li, H., 2021. DASNet: Dual Attentive Fully Convolutional Siamese Networks for Change Detection in High-Resolution Satellite Images. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 14, 1194–1206. https://doi.org/10.1109/jstars.2020.3037893

Chen, H., Qi, Z., Shi, Z., 2022. Remote Sensing Image Change Detection With Transformers. IEEE Transactions on Geoscience and Remote Sensing 60, 1–14. https://doi.org/10.1109/tgrs.2021.3095166

Chen, H., Song, J., Han, C., Xia, J., Yokoya, N., 2024. ChangeMamba: Remote Sensing Change Detection With Spatiotemporal State Space Model. IEEE Transactions on Geoscience and Remote Sensing 62, 1–20. https://doi.org/10.1109/tgrs.2024.3417253

Cong, Y., Khanna, S., Meng, C., Liu, P., Rozi, E., He, Y., Burke, M., Lobell, D.B., Ermon, S., 2022. SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery. arXiv. https://doi.org/10.48550/ARXIV.2207.08051

Curtis, P.G., Slay, C.M., Harris, N.L., Tyukavina, A., Hansen, M.C., 2018. Classifying drivers of global forest loss. Science 361 (6407), 1108–1111. https://doi.org/10.1126/science.aau3445

Diniz, C.G., Souza, A.A.d.A., Santos, D.C., Dias, M.C., Luz, N.C.d., Moraes, D.R.V.d., Maia, J.S.A., Gomes, A.R., Narvaes, I.d.S., Valeriano, D.M., Maurano, L.E.P., Adami, M., 2015. DETER-B: The New Amazon Near Real-Time Deforestation Detection System. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 8 (7), 3619–3628. https://doi.org/10.1109/jstars.2015.2437075

Doblas, J., Reis, M.S., Belluzzo, A.P., Quadros, C.B., Moraes, D.R.V., Almeida, C.A., Maurano, L.E.P., Carvalho, A.F.A., Sant’Anna, S.J.S., Shimabukuro, Y.E., 2022. DETER-R: An Operational Near-Real Time Tropical Forest Disturbance Warning System Based on Sentinel-1 Time Series Analysis. Remote Sensing 14 (15), 3658. https://doi.org/10.3390/rs14153658

F. G. Assis, L.F., Ferreira, K.R., Vinhas, L., Maurano, L., Almeida, C., Carvalho, A., Rodrigues, J., Maciel, A., Camargo, C., 2019. TerraBrasilis: A Spatial Data Analytics Infrastructure for Large-Scale Thematic Mapping. ISPRS International Journal of Geo-Information 8 (11), 513. https://doi.org/10.3390/ijgi8110513

Hansen, M.C., Potapov, P.V., Moore, R., Hancher, M., Turubanova, S.A., Tyukavina, A., Thau, D., Stehman, S.V., Goetz, S.J., Loveland, T.R., Kommareddy, A., Egorov, A., et al., 2013. High-Resolution Global Maps of 21st-Century Forest Cover Change. Science 342 (6160), 850–853. https://doi.org/10.1126/science.1244693

Hansen, M.C., Krylov, A., Tyukavina, A., Potapov, P.V., Turubanova, S., Zutta, B., Ifo, S., Margono, B., Stolle, F., Moore, R., 2016. Humid tropical forest disturbance alerts using Landsat data. Environmental Research Letters 11 (3), 034008. https://doi.org/10.1088/1748-9326/11/3/034008

Hoekman, D., Kooij, B., Quiñones, M., Vellekoop, S., Carolita, I., Budhiman, S., Arief, R., Roswintiarti, O., 2020. Wide-Area Near-Real-Time Monitoring of Tropical Forest Degradation and Deforestation Using Sentinel-1. Remote Sensing 12 (19), 3263. https://doi.org/10.3390/rs12193263

Hong, D., Zhang, B., Li, X., Li, Y., Li, C., Yao, J., Yokoya, N., Li, H., Ghamisi, P., Jia, X., Plaza, A., Gamba, P., et al., 2024. SpectralGPT: Spectral Remote Sensing Foundation Model. IEEE Transactions on Pattern Analysis and Machine Intelligence 46 (8), 5227–5244. https://doi.org/10.1109/tpami.2024.3362475

Huang, M., Li, H., Chen, N., Lin, H., Zhu, D., Gong, D., Chen, Y., Altan, O., Gong, J., 2026. Overcoming Optical Observation Limitations: Automatic Dense Time-Series Mapping of Impervious Surfaces in Cloudy and Snow-Covered Regions. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 19, 21312–21333. https://doi.org/10.1109/jstars.2026.3701406

Jakubik, J., Roy, S., Phillips, C.E., Fraccaro, P., Godwin, D., Zadrozny, B., Szwarcman, D., Gomes, C., Nyirjesy, G., Edwards, B., Kimura, D., Simumba, N., et al., 2023. Foundation Models for Generalist Geospatial Artificial Intelligence. arXiv. https://doi.org/10.48550/ARXIV.2310.18660

Kalamandeen, M., Gloor, E., Mitchard, E., Quincey, D., Ziv, G., Spracklen, D., Spracklen, B., Adami, M., Aragão, L.E.O.C., Galbraith, D., 2018. Pervasive Rise of Small-scale Deforestation in Amazonia. Scientific Reports 8 (1). https://doi.org/10.1038/s41598-018-19358-2

Kennedy, R.E., Yang, Z., Cohen, W.B., 2010. Detecting trends in forest disturbance and recovery using yearly Landsat time series: 1. LandTrendr — Temporal segmentation algorithms. Remote Sensing of Environment 114 (12), 2897–2910. https://doi.org/10.1016/j.rse.2010.07.008

Lambin, E.F., Furumo, P.R., 2023. Deforestation-Free Commodity Supply Chains: Myth or Reality?. Annual Review of Environment and Resources 48 (1), 237–261. https://doi.org/10.1146/annurev-environ-112321-121436

Li, H., Li, Y., Zhang, G., Liu, R., Huang, H., Zhu, Q., Tao, C., 2022. Global and Local Contrastive Self-Supervised Learning for Semantic Segmentation of HR Remote Sensing Images. IEEE Transactions on Geoscience and Remote Sensing 60, 1–14. https://doi.org/10.1109/tgrs.2022.3147513

Li, W., Ma, P., Wang, H., Fang, C., 2023. SAR-TSCC: A Novel Approach for Long Time Series SAR Image Change Detection and Pattern Analysis. IEEE Transactions on Geoscience and Remote Sensing 61, 1–16. https://doi.org/10.1109/tgrs.2023.3243900

Lin, Y., Liu, S., Zheng, Y., Tong, X., Xie, H., Zhu, H., Du, K., Zhao, H., Zhang, J., 2024. An Unsupervised Transformer-Based Multivariate Alteration Detection Approach for Change Detection in VHR Remote Sensing Images. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 17, 3251–3261. https://doi.org/10.1109/jstars.2024.3349775

Ma, Y., Shen, Y., Swatantran, A., Lobell, D.B., 2026. Harvesting AlphaEarth: Benchmarking the geospatial foundation model for agricultural downstream tasks. International Journal of Applied Earth Observation and Geoinformation 149, 105258. https://doi.org/10.1016/j.jag.2026.105258

Manas, O., Lacoste, A., Giro-i-Nieto, X., Vazquez, D., Rodriguez, P., 2021. Seasonal Contrast: Unsupervised Pre-Training from Uncurated Remote Sensing Data. 2021 IEEE/CVF International Conference on Computer Vision (ICCV), 9394–9403. https://doi.org/10.1109/iccv48922.2021.00928

Marsocci, V., Jia, Y., Bellier, G.L., Kerekes, D., Zeng, L., Hafner, S., Gerard, S., Brune, E., Yadav, R., Shibli, A., Fang, H., Ban, Y., et al., 2024. PANGAEA: A Global and Inclusive Benchmark for Geospatial Foundation Models. arXiv. https://doi.org/10.48550/ARXIV.2412.04204

McRoberts, R.E., Stehman, S.V., Liknes, G.C., Næsset, E., Sannier, C., Walters, B.F., 2018. The effects of imperfect reference data on remote sensing-assisted estimators of land cover class proportions. ISPRS Journal of Photogrammetry and Remote Sensing 142, 292–300. https://doi.org/10.1016/j.isprsjprs.2018.06.002

Meyer, H., Pebesma, E., 2022. Machine learning-based global maps of ecological variables and the challenge of assessing them. Nature Communications 13 (1). https://doi.org/10.1038/s41467-022-29838-9

Olofsson, P., Foody, G.M., Herold, M., Stehman, S.V., Woodcock, C.E., Wulder, M.A., 2014. Good practices for estimating area and assessing accuracy of land change. Remote Sensing of Environment 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015

Picoli, M.C.A., Camara, G., Sanches, I., Simões, R., Carvalho, A., Maciel, A., Coutinho, A., Esquerdo, J., Antunes, J., Begotti, R.A., Arvor, D., Almeida, C., 2018. Big earth observation time series analysis for monitoring Brazilian agriculture. ISPRS Journal of Photogrammetry and Remote Sensing 145, 328–339. https://doi.org/10.1016/j.isprsjprs.2018.08.007

Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S., et al., 2020. Spatial validation reveals poor predictive performance of large-scale ecological mapping models. Nature Communications 11 (1). https://doi.org/10.1038/s41467-020-18321-y

Potapov, P., Turubanova, S., Rosa, M., Teixeira, L., Shimbo, J., Zalles, V., Sims, M.J., Stanimirova, R., Lima, A., Goldman, E., Harris, N., Stolle, F., 2026. Evaluation of operational satellite-based disturbance detection products in Brazilian primary forests for the years 2023 and 2024. Frontiers in Remote Sensing 7. https://doi.org/10.3389/frsen.2026.1818592

Prudente, V.H.R., Martins, V.S., Vieira, D.C., Silva, N.R.d.F.e., Adami, M., Sanches, I.D., 2020. Limitations of cloud cover for optical remote sensing of agricultural areas across South America. Remote Sensing Applications: Society and Environment 20, 100414. https://doi.org/10.1016/j.rsase.2020.100414

Reiche, J., Hamunyela, E., Verbesselt, J., Hoekman, D., Herold, M., 2018. Improving near-real time deforestation monitoring in tropical dry forests by combining dense Sentinel-1 time series with Landsat and ALOS-2 PALSAR-2. Remote Sensing of Environment 204, 147–161. https://doi.org/10.1016/j.rse.2017.10.034

Reiche, J., Mullissa, A., Slagter, B., Gou, Y., Tsendbazar, N.E., Odongo-Braun, C., Vollrath, A., Weisse, M.J., Stolle, F., Pickens, A., Donchyts, G., Clinton, N., et al., 2021. Forest disturbance alerts for the Congo Basin using Sentinel-1. Environmental Research Letters 16 (2), 024005. https://doi.org/10.1088/1748-9326/abd0a8

Reiche, J., Balling, J., Pickens, A.H., Masolele, R.N., Berger, A., Weisse, M.J., Mannarino, D., Gou, Y., Slagter, B., Donchyts, G., Carter, S., 2024. Integrating satellite-based forest disturbance alerts improves detection timeliness and confidence. Environmental Research Letters 19 (5), 054011. https://doi.org/10.1088/1748-9326/ad2d82

Roberts, D.R., Bahn, V., Ciuti, S., Boyce, M.S., Elith, J., Guillera‐Arroita, G., Hauenstein, S., Lahoz‐Monfort, J.J., Schröder, B., Thuiller, W., Warton, D.I., Wintle, B.A., et al., 2017. Cross‐validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40 (8), 913–929. https://doi.org/10.1111/ecog.02881

Rodman, K.C., Andrus, R.A., Veblen, T.T., Hart, S.J., 2021. Disturbance detection in landsat time series is influenced by tree mortality agent and severity, not by prior disturbance. Remote Sensing of Environment 254, 112244. https://doi.org/10.1016/j.rse.2020.112244

Saha, S., Bovolo, F., Bruzzone, L., 2019. Unsupervised Deep Change Vector Analysis for Multiple-Change Detection in VHR Images. IEEE Transactions on Geoscience and Remote Sensing 57 (6), 3677–3693. https://doi.org/10.1109/tgrs.2018.2886643

Santos, L.A., Ferreira, K.R., Camara, G., Picoli, M.C., Simoes, R.E., 2021. Quality control and class noise reduction of satellite image time series. ISPRS Journal of Photogrammetry and Remote Sensing 177, 75–88. https://doi.org/10.1016/j.isprsjprs.2021.04.014

Stehman, S.V., Foody, G.M., 2019. Key issues in rigorous accuracy assessment of land cover products. Remote Sensing of Environment 231, 111199. https://doi.org/10.1016/j.rse.2019.05.018

Sudmanns, M., Tiede, D., Augustin, H., Lang, S., 2019. Assessing global Sentinel-2 coverage dynamics and data availability for operational Earth observation (EO) applications using the EO-Compass. International Journal of Digital Earth 13 (7), 768–784. https://doi.org/10.1080/17538947.2019.1572799

Sun, X., Wang, P., Lu, W., Zhu, Z., Lu, X., He, Q., Li, J., Rong, X., Yang, Z., Chang, H., He, Q., Yang, G., et al., 2023. RingMo: A Remote Sensing Foundation Model With Masked Image Modeling. IEEE Transactions on Geoscience and Remote Sensing 61, 1–22. https://doi.org/10.1109/tgrs.2022.3194732

Szwarcman, D., Roy, S., Fraccaro, P., Gíslason, Þ.E., Blumenstiel, B., Ghosal, R., de Oliveira, P.H., de Sousa Almeida, J.L., Sedona, R., Kang, Y., Chakraborty, S., Wang, S., et al., 2026. Prithvi-EO-2.0: A Versatile Multitemporal Foundation Model for Earth Observation Applications. IEEE Transactions on Geoscience and Remote Sensing 64, 1–20. https://doi.org/10.1109/tgrs.2025.3642610

Tang, X., Bullock, E.L., Olofsson, P., Estel, S., Woodcock, C.E., 2019. Near real-time monitoring of tropical forest disturbance: New algorithms and assessment framework. Remote Sensing of Environment 224, 202–218. https://doi.org/10.1016/j.rse.2019.02.003

Tian, S., Zhong, Y., Zheng, Z., Ma, A., Tan, X., Zhang, L., 2022. Large-scale deep learning based binary and semantic change detection in ultra high resolution remote sensing imagery: From benchmark datasets to urban application. ISPRS Journal of Photogrammetry and Remote Sensing 193, 164–186. https://doi.org/10.1016/j.isprsjprs.2022.08.012

Tyukavina, A., Hansen, M.C., Potapov, P., Parker, D., Okpa, C., Stehman, S.V., Kommareddy, I., Turubanova, S., 2018. Congo Basin forest loss dominated by increasing smallholder clearing. Science Advances 4 (11). https://doi.org/10.1126/sciadv.aat2993

Valavi, R., Elith, J., Lahoz‐Monfort, J.J., Guillera‐Arroita, G., 2018. block CV : An r package for generating spatially or environmentally separated folds for k ‐fold cross‐validation of species distribution models. Methods in Ecology and Evolution 10 (2), 225–232. https://doi.org/10.1111/2041-210x.13107

Vancutsem, C., Achard, F., Pekel, J.F., Vieilledent, G., Carboni, S., Simonetti, D., Gallego, J., Aragão, L.E.O.C., Nasi, R., 2021. Long-term (1990–2019) monitoring of forest cover changes in the humid tropics. Science Advances 7 (10). https://doi.org/10.1126/sciadv.abe1603

Verbesselt, J., Hyndman, R., Newnham, G., Culvenor, D., 2010. Detecting trend and seasonal changes in satellite image time series. Remote Sensing of Environment 114 (1), 106–115. https://doi.org/10.1016/j.rse.2009.08.014

Whitcraft, A.K., Vermote, E.F., Becker-Reshef, I., Justice, C.O., 2015. Cloud cover throughout the agricultural growing season: Impacts on passive optical earth observations. Remote Sensing of Environment 156, 438–447. https://doi.org/10.1016/j.rse.2014.10.009

Ye, S., Pontius, R.G., Rakshit, R., 2018. A review of accuracy assessment for object-based image analysis: From per-pixel to per-polygon approaches. ISPRS Journal of Photogrammetry and Remote Sensing 141, 137–147. https://doi.org/10.1016/j.isprsjprs.2018.04.002

Ygorra, B., Frappart, F., Wigneron, J., Moisy, C., Catry, T., Baup, F., Hamunyela, E., Riazanoff, S., 2021. Monitoring loss of tropical forest cover from Sentinel-1 time-series: A CuSum-based approach. International Journal of Applied Earth Observation and Geoinformation 103, 102532. https://doi.org/10.1016/j.jag.2021.102532

Yuan, Y., Lin, L., Huo, L.Z., Kong, Y.L., Zhou, Z.G., Wu, B., Jia, Y., 2020. Using An Attention-Based LSTM Encoder–Decoder Network for Near Real-Time Disturbance Detection. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing 13, 1819–1832. https://doi.org/10.1109/jstars.2020.2988324

Zhang, X., Wang, J., Henebry, G.M., Gao, F., 2020. Development and evaluation of a new algorithm for detecting 30 m land surface phenology from VIIRS and HLS time series. ISPRS Journal of Photogrammetry and Remote Sensing 161, 37–51. https://doi.org/10.1016/j.isprsjprs.2020.01.012

Zhu, Z., Woodcock, C.E., 2014. Continuous change detection and classification of land cover using all available Landsat data. Remote Sensing of Environment 144, 152–171. https://doi.org/10.1016/j.rse.2014.01.011

Zhu, Z., Zhang, J., Yang, Z., Aljaddani, A.H., Cohen, W.B., Qiu, S., Zhou, C., 2020. Continuous monitoring of land disturbance based on Landsat time series. Remote Sensing of Environment 238, 111116. https://doi.org/10.1016/j.rse.2019.03.009
