# Correction — P1 §5 (RADD latency) is superseded

**Status: P1 `P1_results.md` §5 is withdrawn. Use P1c `P1c_results.md` §3 instead.**

## What P1 §5 said
| region | coverage | median latency | share ≥ 2 months |
|---|---|---|---|
| A | 122 / 252 (48 %) | +35.5 d [17.0, 46.0] | 0.287 [0.125, 0.368] |
| B | 17 / 31 (55 %) | +70.0 d [24.0, 122.0] | 0.588 [0.167, 1.000] |

It concluded that "RADD reaches barely half of these events" and that Roraima's median latency is
twice Pará's.

## What was wrong
The RADD alert date was sampled at the **event centroid pixel only**. A DETER polygon has a median
area of ~13 ha and RADD alerts fire on a subset of its pixels, so a single centroid pixel misses
the alert whenever the detected patch does not happen to cover the centre. The error is one of
sampling geometry, not of the RADD product or of the date decoding.

## The corrected result (P1c §3, `reduceRegions` min over the whole polygon)
| region | coverage | median latency vs P1 bracket midpoint | share ≥ 2 months |
|---|---|---|---|
| A | 1,217 / 1,247 (**97.6 %**) | **−11 d** [−18, −8] | **0.000** [0.000, 0.000] |
| B | 571 / 669 (**85.4 %**) | **−7 d** [−19, −6] | **0.000** [0.000, 0.000] |

Both conclusions reverse. RADD covers ~90 % of DETER 2021 events, not half; and it fires *before*
the optical bracket midpoint rather than one to two months after it. No event in either region is
≥ 2 months late.

## Consequences
- Any statement in P1 §5, and the sentence in the P1 RESEARCH_LOG entry giving "median latency
  35.5 d (A) vs 70.0 d (B), share ≥ 2 months 0.29 vs 0.59", is superseded by the table above.
- P1's other sections are unaffected: the event set, thresholds, registration curve and H1–H3
  verdicts never used the RADD field.
- The correction is what made P1d possible — RADD read over the polygon is accurate enough to date
  events (P1d §2 gate: median |distance to the tightened interval| = 0 d), which is the design P1c's
  SAR route failed to deliver.

*Raised and verified 2026-09-06 during TB01-P1c step 6; formalised in TB01-P1d.*
