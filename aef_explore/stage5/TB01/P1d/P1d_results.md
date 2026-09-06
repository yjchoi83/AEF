# TB01-P1d — Results: RADD-dated event population and the low-observation test

> **Gate PASSED → RADD dating ADOPTED.** All 6 steps ran. The low-observation regime P1 could not
> reach is now visible, and H1′ is met — on 23 events, below the pre-registered power floor.

## 1. Event date = first RADD alert inside the polygon (all 1,916 DETER 2021 CR+VEG ≥ 1 ha)
| | A | B |
|---|---|---|
| events | 1,247 | 669 |
| `radd_any` (Alert ≥ 2) coverage | **1,217 (97.6 %)** | **571 (85.4 %)** |
| `radd_high` (Alert = 3) coverage | 1,211 (97.1 %) | 567 (84.8 %) |

Confirmation costs almost nothing (−0.5/−0.6 pp), so any-vs-high is not the binding choice. `date_upper = min(radd_any, view_date)` clips 93 events. **Undated remainder n = 128** (A 30, B 98): 124/128 are DESMATAMENTO_CR; in A they are *smaller* than the dated (median 8.6 vs 13.5 ha), in B they are not (11.9 vs 11.5 ha) — Roraima's 15 % gap is not a polygon-size effect.

## 2. Validation gate on the 281 bracketed events with a RADD date — **PASS**
Statistic = signed distance to `I = [before, min(after, view_date)]`, 0 when inside (PLAN.md).

| variant | median \|diff\| (≤ 20 required) | share inside I (descriptive) | vs interval midpoint |
|---|---|---|---|
| `radd_any` | **0 d** [0, 0] ✔ | 0.626 [0.567, 0.679] | −10 d [−16, −8] |
| `radd_high` | **0 d** [0, 0] ✔ | 0.625 [0.571, 0.674] | −9 d [−16, −7.5] |
| `date_upper` | **0 d** [0, 0] ✔ | 0.690 [0.610, 0.763] | −10 d [−16, −8] |

80.1 % are within 20 d of I; mean |diff| is 21.2 d, carried by an early tail (p90 = 93 d). Errors are asymmetric as RADD's design implies: 31 % early (median 57 d before I), 6 % late (median 3 d after). Per region: A 0 d / 61.8 % inside, B 0 d / 70.0 %.

## 3–4. Registration vs post-event clear S2 count (n = 1,788 dated; τ_A = 11.39°, τ_B = 19.13°)
Empirical registration by post-event clear count (`radd_any`), n in brackets:

| clear_post | 0 | 1–2 | 3–4 | 5–6 | 7–9 | 10–14 | 15+ |
|---|---|---|---|---|---|---|---|
| **A** | 0.667 (3) | 0.778 (9) | 0.963 (27) | 0.972 (36) | 0.981 (107) | 1.000 (283) | 0.999 (752) |
| **B** | 1.000 (1) | 0.500 (10) | 0.364 (11) | 0.643 (28) | 0.892 (37) | 1.000 (38) | 0.984 (446) |

Model `registered ~ clear_post + region + month`, logistic L2, 0.5° block-bootstrap CIs:

| post-event clear obs | 0 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| **A** | .925 [.696,.984] | .938 [.756,.986] | .949 [.809,.988] | .958 [.846,.990] | .972 [.903,.993] | .990 [.972,.996] |
| **B** | .586 [.103,.970] | .634 [.135,.975] | .680 [.174,.979] | .723 [.220,.982] | .798 [.343,.987] | .917 [.714,.994] |

- **H1′ — criterion MET, power-limited.** Registration at `clear_post ≤ 2` is **0.652** [0.294, 0.903] vs **0.986** [0.968, 0.994] at `≥ 5`: a gap of **+33.3 pp** [8.4, 68.1] — ≥ 5 pp with the CI excluding 0. But the 0–2 bin holds only **23 events (A 12, B 11)**, under the pre-registered 30-event floor. PLAN.md's sub-30 clause was written to stop a small bin being called a FAIL; it does not license calling this a clean PASS either, so the verdict is **PASS (provisional, power-limited)**.
- **H3 — PASS.** Registration at `clear_post ≥ 5` = **0.9855** [0.968, 0.994] ≥ 0.95. Per region A 0.9966, B 0.9617.
- **Sensitivity** (same direction and verdicts, all n₀₋₂ < 30): `radd_high` +36.0 pp [12.5, 64.8] (p_lo 0.625, p_hi 0.985, n₀₋₂ = 24); `date_upper` +40.7 pp [12.0, 76.5] (p_lo 0.579, p_hi 0.986, n₀₋₂ = 19).

**This is the result P1 was built to get and could not.** P1's optical bracket left no event below 3 post-event observations and pinned P(registered) at ~0.996; RADD dating exposes a 0–2 regime where registration falls to 0.65, and Roraima — the low-observation region — carries the effect.

## 5. Circularity check
| region | RADD-dated | RADD-undated | gap |
|---|---|---|---|
| A | 0.9934 [0.985, 0.998] (n = 1,217) | 0.9667 [0.800, 1.000] (n = 30) | +2.7 pp [−0.9, +18.5] |
| B | 0.9422 [0.910, 0.974] (n = 571) | 0.9899 [0.957, 1.000] (n = 98) | **−4.8 pp [−8.5, −0.4]** |

RADD is a radar product and AEF ingests Sentinel-1, so the worry is that RADD-dated events are just the ones AEF was always going to register, inflating H1′ by construction. The data do not support it: in A the gap is +2.7 pp with a CI spanning zero, and in B it is **negative** — RADD-dated events register *less* often than undated ones, the opposite of the circularity direction. The undated events are also not a low-registration residue (B: 0.990), so RADD non-detection does not track AEF non-registration. A weaker concern survives: both products ingest S1, so a scene-level S1 outage would hide an event from both. Testing that needs an S1-observation-density covariate, which P1d does not carry.

## 6. Retraction
`P1_RADD_correction.md` records that P1 §5 (centroid-sampled RADD latency) is superseded by P1c §3.

## 7. Compute / compliance
One new EE extraction (`radd_high`, polygon `reduceRegions`, ≤ 40 features per call); angular change, `radd_any` and the S2 per-date matrices reused from P1c. **No exports**; ≪ 15 EECU-h. No `data/`, shapefiles or credentials committed.
