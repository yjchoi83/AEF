# TB01-P3 — Results: deferral and attribution

> **H4 PASSES in both directions.** **H5 is NOT TESTABLE as specified** — the ground truth is
> degenerate on this population, so the literal rule scores perfectly by construction. The
> substantive quantities it was meant to deliver are reported instead.

## 7. Deferral (H4: ≥ 80 % of Y-unregistered events register in Y+1)
Next-year angular change on the polygon interior, thresholded at a **separately estimated** next-year τ (TMF stable forest for that year pair, Hansen `lossyear` excluded for the surrounding four years, ≥ 2,000 px per state — met in every state used).

| direction | unregistered in Y | with Y+1 value | **register in Y+1** | median next-year angular change | H4 |
|---|---|---|---|---|---|
| 2020 → 2021 | 1,107 | 1,107 | **0.940** [0.922, 0.957] | 41.3° | **PASS** |
| 2021 → 2022 | 1,332 | 1,332 | **0.965** [0.953, 0.975] | 43.8° | **PASS** |

By state, 2021→2022: RR .987, AM .977, PA .974, RO .969, AC .964, MT .916, MA .733 (n = 15);
2020→2021: RO .969, AC .965, RR .965, PA .961, AM .895, MT .875.

**Interpretation, fixed in the PLAN before running:** the annual embedding **defers** these events by one year rather than missing them. Only **47 of 38,303** 2021 events (0.12 %) and **66 of 39,772** 2020 events (0.17 %) register in neither year — the genuine miss population is ~1 in 800.

## 8. Attribution
**H5 verdict: NOT TESTABLE (degenerate ground truth).** The rule is "assign to Y if `clear_post ≥ k`, else Y+1", `k` fitted on 2020 and evaluated on 2021. But **every event in each population has the same true year** — the 2021 set is by construction a set of 2021 clearings. The loss is minimised by any rule that always answers Y, the grid duly picks **k = 0**, and the held-out reduction comes out at **100 % [100, 100]**. That is an artifact of the label, not evidence, and is not reported as a pass. (An earlier run using the RADD date's *year* as truth gave k = 1 and 88.3 % — also circular, since `clear_post` is computed from that same date and is 0 by construction when the date falls in Y+1.)

**What a valid test needs:** a population spanning more than one true year, with the rule given only year-agnostic inputs — concretely `clear_post` computed in the year of *first registration* rather than in the known event year, which for deferred events requires the Y+1 monthly S2 stack P3 did not extract. Recommended follow-up.

**The substantive quantities, which are testable and are the practical content of step 8:**

| | 2020 | 2021 |
|---|---|---|
| n | 39,772 | 38,303 |
| naive rule misattribution (date to first registration) | **2.78 %** [2.50, 3.10] | **3.48 %** [3.08, 3.92] |
| two-year rule misattribution | **0.17 %** [0.12, 0.22] | **0.12 %** [0.09, 0.17] |
| reduction, two-year vs naive | **94.0 %** [92.0, 95.6] | **96.5 %** [95.2, 97.5] |
| AUC of `clear_post` predicting non-registration in Y | **0.729** [0.700, 0.756] | **0.712** [0.680, 0.737] |
| median `clear_post`, registered vs not | 21.7 vs 8.0 | 23.7 vs 10.7 |

So: dating a clearing to the year the annual embedding first registers it is wrong for ~3 % of events; a two-year window removes ~95 % of that error; and post-event optical observation count is a genuine but moderate predictor of which events get deferred (AUC ≈ 0.72 in both years, tight CIs) — the H1″ signal seen from the attribution side.

## Compute / compliance
Polygon `reduceRegions` only; no image exports. No `data/`, shapefiles or credentials committed.
