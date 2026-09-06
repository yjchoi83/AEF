# TB01-P1 — Results (annual embeddings, 2021; A = Pará BR-163 200×200 km, B = Roraima state)

**Gate:** Alerta exposes before/after image dates (`image_acquired_before_at`/`image_acquired_after_at`, WFS `mapbiomas-alertas:dashboard-alerts`) — verified, no substitution (PLAN.md).

## 1. Event set — n after every filter
| filter | A | B |
|---|---|---|
| DETER 2021 CR+VEG in region | 1263 | 674 |
| … area ≥ 1 ha | 1247 | 669 |
| Alerta 2021 alerts in region (all carry both image dates) | 1409 | 2307 |
| DETER × Alerta intersecting pairs | 1340 | 640 |
| overlap ≥ 50 % of DETER polygon (best alert per event) | 917 | 395 |
| DETER `view_date` inside Alerta bracket | 759 | 276 |
| **bracket ≤ 62 days → FINAL** | **252** | **31** |
| of which inside the 80×80 km custom-embedding boxes | 129 | 10 |

Both regions **miss the 300 target**, Roraima badly. The binding filter is the ≤ 62-day bracket (759→252, 276→31): Alerta brackets are long where cloud is persistent, so it keeps only well-observed events. 0.5° bootstrap blocks: A 10, B 11.

## 2. Registration threshold (defined once, in the PLAN glossary)
Stable forest = TMF `Dec2020=1 ∧ Dec2021=1`, Hansen `lossyear ∉ {19,20,21,22}`; τ = p90 of its angular change. **τ_A = 11.39°** (n = 6,256 px) · **τ_B = 19.13°** (n = 5,655 px). Event mean 2020→2021 angular change (10 m inward buffer): median 37.7° (A) / 39.5° (B) — 2–3× τ. Registered: **A 251/252 = 0.996** [0.990, 1.000] · **B 31/31 = 1.000** [1.000, 1.000].

## 3. P(registered) vs post-event clear S2 count (logistic + region + month, L2; block-bootstrap CI)
| post-event clear obs | 0 | 1 | 2 | 3 | 5 | 10 |
|---|---|---|---|---|---|---|
| **A** | .994 [.990,1.000] | .995 [.991,1.000] | .995 [.991,1.000] | .995 [.991,1.000] | .996 [.992,1.000] | .997 [.993,1.000] |
| **B** | .996 [.994,1.000] | .996 [.994,1.000] | .996 [.994,1.000] | .997 [.994,1.000] | .997 [.995,1.000] | .998 [.996,1.000] |

Counts 0–3 are **extrapolation**: observed counts run 3–37 (A, median 13) and 0–21 (B, median 13), and no event has 1 or 2. The set cannot populate the low-observability end — the ≤ 62-day bracket removes precisely those events.

## 4. Pre-registered verdicts (fixed in PLAN.md before fitting)
- **H1 — FAIL.** Spearman over count bins: A **0.00** [0.00, 0.00]; B **undefined** (every populated bin = 1.000). A ceiling, not a contradiction — registration is already ~100 % at the lowest count present.
- **H2 — rejected in sign, negligible in size.** Region coefficient 0.247 [0.108, 0.458] (standardised, L2); implied A→B probability gap ≤ 0.4 pp. Region × clear-count interaction: LR ≈ 0.00, p = 1.00.
- **H3 — PASS.** ≥ 5 post-event clear obs: A 0.996 [0.989, 1.000], B 1.000 [1.000, 1.000], pooled 0.996 [0.990, 1.000].
- **Pass = H1 ∧ H3 → FAIL** (H3 passes; H1 fails on the ceiling above).

## 5. RADD latency (first RADD alert ≥ 2, 2021–22, minus bracket midpoint)
| region | RADD alert at centroid | median latency (d) | share ≥ 2 months |
|---|---|---|---|
| A | 122 / 252 (48 %) | **35.5** [17.0, 46.0] | **0.287** [0.125, 0.368] |
| B | 17 / 31 (55 %) | **70.0** [24.0, 122.0] | **0.588** [0.167, 1.000] |

RADD reaches barely half of these events; where it fires, Roraima's median latency is 2× Pará's (B's CI is wide at n = 17).

## 6. Observability bias of alert references (200 random 80×80 km boxes, Legal Amazon)
DETER 2021 count (mean 48.3, median 5, max 1015) vs mean 2021 clear-obs count at 500 m (mean 43.2, range 21.4–85.0): **Pearson −0.088** [−0.158, −0.006], p = 0.218 · **Spearman −0.008** [−0.150, 0.141], p = 0.907. Unrestricted, alert count is **not** positively driven by optical visibility; the r = 0.25 of the stage-5 candidate set was a range-restriction artefact. Selection acts one level down: at the *event* level the paired bracket admits only well-observed events.

## 7. Compute / compliance
Interactive EE only, ≤ 10,000 samples per call, **no exports**, well under 25 EECU-h. No `data/`, shapefiles or credentials committed.
