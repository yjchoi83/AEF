# TB01-P2 — Results: QC, Amazon-wide scale-up, decisive covariate

> **⚠ ALL VERDICTS BELOW ARE PENDING QC** — `qc_table.csv` `decision` column is unfilled.
> **⚠ DECISIVE GATE H7 = FAIL AS PRE-REGISTERED → BATCH STOPPED. P3 and P4 were not run.**
> The failure is *inestimability*, not the substantive failure H7 was written to catch — see §5.

## 0. QC chips
53 three-panel chips in `results/qc_chips/` (S2 2020 dry median | S2 post-event clear | AEF 2020→2021 angular change; DETER polygon painted, RADD date in title): all 23 events from P1d's `clear_post ≤ 2` bin plus 30 registered controls. `qc_table.csv` awaits a human `decision`.

## 1–2. Population
**37,689** DETER 2021 CR+VEG polygons ≥ 1 ha in the Legal Amazon — PA 14,565, AM 7,801, RO 6,108, AC 4,057, MT 3,982, RR 669, MA 432, TO 42, AP 33 — plus **3,082 `radd_only`** events (DETER-2022 polygons with no 2021 counterpart containing ≥ 1 ha of high-confidence RADD 2021 alerts): PA 966, AC 583, RO 482, AM 478, MT 376, RR 168, MA 28, AP 1. **Total 40,771; 38,303 RADD-dated.** RADD coverage: AM .979, AC .966, RO .939, PA .931, MT .864, RR .854, AP .727, MA .711, TO .500.

## 3–4. Layers and thresholds
Twelve monthly 2021 S2 clear-count and S1 scene-count images; `clear_post`/`s1_post` prorated in the event month. Per-state stable-forest p90 (τ): PA 12.73°, AM 10.20°, RO 11.22°, AC 11.22°, MT 13.17°, AP 13.47°, TO 15.89°, MA 17.27°, **RR 19.54°** (matching P1's independent 19.13°). ⚠ The stable-forest sample missed the pre-registered ≥ 2,000 px floor in **MA (1,268)** and **TO (251)**; those states hold 356 events (0.9 %) and their τ is provisional.

## 5. Model — H1″ PASS, H3 PASS, H7 FAIL (as specified)
n = 38,303 dated events; registration by post-event clear-observation count:

| clear_post | 0 | 0–2 | 2–4 | 4–6 | 6–9 | 9–14 | 14+ |
|---|---|---|---|---|---|---|---|
| n | 173 | 345 | 718 | 1,002 | 1,665 | 4,036 | 30,364 |
| registered | 0.699 | 0.597 | 0.763 | 0.872 | 0.922 | 0.970 | 0.980 |

- **H1″ — PASS.** `clear_post ≤ 2`: **0.631** (n = **518** ≥ 100) vs `≥ 5`: **0.975** (n = 36,638). Gap **+34.4 pp**, CI **[28.3, 40.3]** — excludes 0, ≥ 5 pp, n floor met. P1d's 23-event provisional result is confirmed at 22× the sample.
- **H3 — PASS.** Registration at `clear_post ≥ 5` = 0.975 ≥ 0.95.
- **H7 — FAIL as pre-registered**, because criterion (b) is **inestimable**:
  - **(a) PASSES.** With `s1_post` in the model, the `clear_post` coefficient is 0.219,
    CI **[0.046, 0.429]** — excludes 0. Solo coefficient 0.211, so conditioning on S1 barely moves it.
  - **(b) CANNOT BE EVALUATED.** Only **1** event in 38,303 has `clear_post ≤ 2` *and* `s1_post ≥ median (31.4)`. Both counts are driven by how much of 2021 remains after the event date (79 % of `clear_post ≤ 2` events fall in Oct–Dec, where median `s1_post` is 7.5/5.2/2.7). The stratum is empty by construction, so (b) tests nothing.

**Diagnostic — not pre-registered, not a substitute for the gate.** Taking `s1_post` relative to the event's **own month's** median: among `clear_post ≤ 2` events with at-or-above-median S1 density, n = **172**, registration = **0.523** [0.431, 0.626] — far below the 0.80 bar — and the gap vs `clear_post ≥ 5` in the same stratum is **44.4 pp** [34.6, 53.8]. Within `clear_post ≤ 2`, registration *falls* as within-month S1 density rises (Q1 0.777 → Q2 0.631 → Q3 0.638 → Q4 0.477). **Both disjuncts of the brief's own definition of "H7 fails" are therefore false**: the optical effect does not disappear under S1 control, and low registration is not confined to where S1 is sparse too. Letter and stated intent disagree; the conservative action is taken (STOP) and the resolution left to the human.

Supporting: `radd_only` events register at **0.753** (n = 3,082) vs **0.984** for DETER-mapped ones, and supply 118 of the 518 low-observation events. By state, registration is 0.955–1.000 everywhere except **RR 0.796** — the low-observation state.

## 6. Robustness (H1/H3/H7 in every variant)

| variant | n | n(0–2) | p_lo | p_hi | gap pp [CI] | joint coef CI | H1 | H3 | H7 |
|---|---|---|---|---|---|---|---|---|---|
| main (τ p90) | 38,303 | 518 | .631 | .975 | 34.4 [28.3, 40.3] | [0.046, 0.429] | PASS | PASS | FAIL |
| τ p85 | 38,303 | 518 | .664 | .981 | 31.7 [25.7, 37.4] | [−0.003, 0.420] | PASS | PASS | FAIL |
| τ p95 | 38,303 | 518 | .542 | .965 | 42.2 [35.8, 48.3] | [0.037, 0.348] | PASS | PASS | FAIL |
| radd_high only | 38,101 | 489 | .624 | .976 | 35.2 [29.1, 41.3] | [0.009, 0.377] | PASS | PASS | FAIL |
| date_upper | 38,303 | 361 | .510 | .975 | 46.5 [39.5, 53.2] | [−0.072, 0.212] | PASS | PASS | FAIL |
| no radd_only | 35,221 | 400 | .713 | .991 | 27.8 [21.6, 34.1] | [0.376, 1.604] | PASS | PASS | FAIL |
| size < 5 ha | 221 | 5 | .800 | .985 | 18.5 [−2.9, 65.3] | [−0.975, 1.551] | UNDERPOW. | PASS | FAIL |
| size 5–25 ha | 29,953 | 402 | .679 | .981 | 30.2 [24.8, 35.9] | [0.182, 0.767] | PASS | PASS | FAIL |
| size ≥ 25 ha | 8,129 | 111 | .450 | .954 | 50.4 [37.2, 62.2] | [−0.082, 0.384] | PASS | PASS | FAIL |

**H1″ holds in 8 of 9 variants** (the ninth, < 5 ha, has n(0–2) = 5 — underpowered, not failed); **H3 holds in all 9**; **H7 fails in all 9 for the same structural reason** (n(0–2) ∩ dense-S1 ≤ 1). H7(a) is *not* uniformly robust: the joint coefficient CI crosses 0 under τ p85, `date_upper` and size ≥ 25 ha, even though the empirical gap is large everywhere.

## 6b. H7(a) sensitivity — coefficient and CI under every variant *(added by P5b item 3)*

The joint `clear_post` coefficient of the §5 model, with its 0.5° block-bootstrap CI, in each
of the nine robustness variants. **⚠ marks the three variants where the pre-registered CI
crosses zero** — the caveat §6 states in prose, here with the numbers attached.

| variant | n | **coef** | **pre-registered CI** (§6) | P5b refit coef | P5b refit CI |
|---|---|---|---|---|---|
| main (τ p90) | 38,303 | 0.219 | [0.046, 0.429] | 0.217 | [0.116, 0.335] |
| **⚠ τ p85** | 38,303 | 0.222 | **[−0.003, 0.420]** | 0.222 | [0.097, 0.354] |
| τ p95 | 38,303 | 0.188 | [0.037, 0.348] | 0.188 | [0.090, 0.297] |
| radd_high only | 38,101 | 0.196 | [0.009, 0.377] | 0.196 | [0.098, 0.300] |
| **⚠ date_upper** | 38,303 | 0.218 | **[−0.072, 0.212]** | 0.218 | [0.116, 0.346] |
| no radd_only | 35,221 | 0.463 | [0.376, 1.604] | 0.463 | [0.314, 0.613] |
| (⚠) size < 5 ha — underpowered, n(0–2) = 5 | 221 | −0.091 | [−0.975, 1.551] | −0.091 | [−0.885, 0.703] |
| size 5–25 ha | 29,953 | 0.323 | [0.182, 0.767] | 0.323 | [0.199, 0.449] |
| **⚠ size ≥ 25 ha** | 8,129 | 0.194 | [−0.082, 0.384] | 0.194 | [0.078, 0.354] |

**Provenance.** The original P2 fitting script was not retained, so P5b rebuilt the model from
the spec in `P2/PLAN.md` step 5 — logistic, L2 (λ = 1), `sqrt(clear_post)` + `s1_post` + state
+ month + `radd_only` — and calibrated it against the only two coefficients P2 reports: solo
**0.211** (refit 0.213) and joint **0.219** (refit 0.217). The point estimates therefore
reproduce; the refit **CIs are narrower**, and under them only the underpowered < 5 ha variant
crosses zero. The discrepancy is in the bootstrap, not the model, and cannot be resolved
without the original script — so **the table is marked on the pre-registered CIs**, which is
the conservative reading. Either way the substantive conclusion is unchanged: the coefficient
is positive in eight of nine variants and its sign is never reversed with any confidence, but
its CI is not uniformly clear of zero, so **H7(a) should be reported as directionally robust
and marginally significant in three variants — not as uniformly established**.

Machine-readable: `../P5b/h7a_sensitivity.csv`; script `../P5b/h7a_sensitivity.py`.

## 7. Compute / compliance
Polygon `reduceRegions`, centroid `sampleRegions`, `getThumbURL` only; **no image exports**; within the 60 EECU-h ceiling. No `data/`, shapefiles or credentials committed.
