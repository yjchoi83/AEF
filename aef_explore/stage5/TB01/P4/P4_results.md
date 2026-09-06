# TB01-P4 — Results: Congo replication

> **Replication criterion FAILS.** The Congo `clear_post ≤ 2` vs `≥ 5` gap is **5.34 pp**
> [2.91, 8.20], **outside** the Brazil 2021 CI [28.4, 40.2] **and** outside the Brazil 2020 CI
> [11.6, 16.6]. Not power-limited (n(0–2) = 202 ≥ 100). Direction and H7(a) do replicate.

## ROIs (step 9)
Grid of 100 × 100 km boxes over the DRC forest belt (17–29 °E, −5–3 °N), kept only if fully inside the country, ranked by **JRC TMF 2021 deforestation/degradation area** (`Dec2020 = 1 ∧ Dec2021 ∈ {2,3}`), picked greedily with a ≥ 200 km separation constraint:
- **CG1** `28.679, 0.426, 29.578, 1.331` — 16,692 ha TMF-2021 change (eastern DRC, Ituri/N. Kivu)
- **CG2** `23.301, −4.096, 24.201, −3.191` — 12,804 ha (central DRC, Sankuru)

## Event set and layers
TMF 2021 patches ≥ 1 ha (connected component ≥ 11 px at 30 m, vectorised in 16 tiles per ROI): **5,243** patches (CG1 2,872, CG2 2,371), median **1.61 ha** — 8× smaller than the Brazilian DETER polygons. Dated by first RADD alert inside the patch (`Alert ≥ 2`, africa tiles, `Date` masked to 2021–22): **4,959 dated (94.6 %)**. Same monthly 2021 S2 clear-count and S1 scene-count layers and the same prorated `clear_post`/`s1_post`. Regional **τ_CG = 16.31°** (p90 on n = 3,019 stable-forest px pooled over both ROIs).
⚠ **Dating caveat, worse than Brazil's.** No 2021 archive exists for the africa RADD tiles — the earliest rolling snapshot is **2024-01-03**, so Congo dates come from snapshots 2+ years after the event, against 2021-10 for Brazil. Masking `Date` to 2021–22 recovers 94.6 % coverage, but a patch first alerted in 2019–20 and re-alerted in 2021 contributes its 2021 re-alert.

## Model (identical specification to P2 step 5, ROI in place of state)
n = 4,959; 17 blocks of 0.5°; overall registration **0.996**.

| clear_post | 0 | ≤2 | ≤4 | ≤6 | ≤9 | ≤14 | >14 |
|---|---|---|---|---|---|---|---|
| n | 171 | 31 | 46 | 106 | 165 | 339 | 4,101 |
| registered | .942 | .968 | 1.000 | .953 | 1.000 | .994 | 1.000 |

| statistic | Congo | Brazil 2021 | Brazil 2020 |
|---|---|---|---|
| n | 4,959 | 38,303 | 39,772 |
| n(0–2) | 202 | 518 | 1,508 |
| p(≤2) | **.945** | .631 | .842 |
| p(≥5) | **.999** | .975 | .982 |
| gap pp [CI] | **5.34** [2.91, 8.20] | 34.4 [28.4, 40.2] | 14.1 [11.6, 16.6] |
| joint `clear_post` coef [CI] | **2.19** [1.44, 2.84] | 0.219 [0.062, 0.424] | 0.387 [0.129, 0.732] |

**Verdict — NOT REPLICATED on the pre-registered criterion.** The gap is real and positive (CI excludes 0) and **H7(a) replicates emphatically** — the `clear_post` coefficient is the strongest of any region tested — but the *magnitude* is far below Brazil's, because Congo registration barely falls in the low-observation bin (.945 vs Brazil 2021's .631).

## Why the magnitudes differ (interpretation, not pre-registered)
Three candidates, none tested here: (i) **the label differs** — TMF patches are model-confirmed forest-class transitions, not optically-spotted alerts, and are 8× smaller, so the Congo set is not the same kind of object as a DETER polygon; (ii) **change is large relative to τ** — Congo clearings show very large angular change against τ_CG = 16.31°, leaving little room for a deficit; (iii) **dating is weaker** — 2024-snapshot dates blur `clear_post` and attenuate the gap toward zero. Only (iii) biases against replication, so the true Congo gap is probably somewhat above 5.34 pp — but not plausibly into the Brazilian range.

**What this means for the claim.** The qualitative finding — registration falls when post-event optical observation is scarce, and it is not S1 density doing the work — transfers to the Congo Basin. The quantitative Brazilian effect size does **not**, and must not be presented as global. TB01 should report the gap as a region-specific quantity, with Brazil 2020, Brazil 2021 and Congo as three separate estimates.

## Compute / compliance
`reduceToVectors` for the event set, polygon `reduceRegions` thereafter; no image exports. No `data/`, shapefiles or credentials committed.
