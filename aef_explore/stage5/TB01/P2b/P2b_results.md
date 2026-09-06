# TB01-P2b — Results: 2020 out-of-sample replication and the re-pre-registered H7(b)′

> **H7(b)′ PASSES on 2020, the confirmatory year. H1″, H3, H7(a) all replicate. → P3 and P4 run.**
> The 2021 timing-controlled value (0.523) was seen before the criterion was fixed and is
> exploratory (PLAN.md §1); 2020 carries the confirmatory weight.

## 1. Offset check on the 2021 unregistered events
Interior (10 m inward) vs **50–150 m outer ring** 2020→2021 angular change on all **1,332** unregistered 2021 events. `OFFSET_SUSPECT` = ring > τ ∧ interior < τ; interior < τ holds by construction here, so the rule reduces to ring > τ. **608 flagged = 45.7 %** — per state AC .674, AM .571, RO .534, PA .450, MT .310, MA .267, RR .199; higher for `radd_only` (.499) than DETER-mapped (.399); median ring 12.27° vs interior 10.43°. Excluding all 608 (row 3 below): **H1″ and H7(a) both still pass**, H7(a) *more strongly* (coef 0.508 [0.205, 0.958] vs 0.219). Geometric mismatch explains part of the deficit — p_lo rises 0.631 → 0.708 — but not most of it.

## 2. 2020 population
DETER 2020 CR+VEG ≥ 1 ha: **43,316** (PA 17,846, RO 6,763, AM 6,345, MT 5,833, AC 4,411, RR 1,248, MA 768, TO 67, AP 35) plus **2,601 `radd_only_2020`** (DETER-2021 polygons with no 2020 overlap holding ≥ 1 ha of high-confidence RADD 2020) = **45,917**; **39,772 RADD-dated**. Per-state τ on 2019→2020 stable forest: AM 9.15°, AP 9.38°, PA 10.30°, RO 10.84°, AC 11.22°, MT 12.20°, TO 12.37°, MA 14.22°, RR 16.49°.
⚠ **Threshold sample floor missed again in MA (1,270 px) and TO (183 px)** — provisional, 835 events.
⚠ **Dating asymmetry between years.** RADD's earliest South-America snapshot is **2021-10-13**; none is contemporaneous with 2020. 2020 dates come from the 2021-10 / 2021-12 / 2022-03 snapshots, so any pixel re-alerted during 2021 has had its 2020 date overwritten. Coverage is therefore lower than 2021's (PA .857, AM .939, AC .929, RO .884, RR .780, MT .752, MA .570, AP .514, TO .373) and the 2020 dated set is mildly biased toward events *not* re-disturbed in 2021. This weakens but does not invalidate the replication.

## 3–4. H7(b)′ and the 2020 vs 2021 replication

| | n | n(0–2) | p(≤2) | p(≥5) | gap pp [CI] | joint coef [CI] | H1″ | H3 | H7(a) |
|---|---|---|---|---|---|---|---|---|---|
| **2020 (confirmatory)** | 39,772 | 1,508 | .842 | .982 | **14.1** [11.6, 16.6] | 0.387 [0.129, 0.732] | PASS | PASS | PASS |
| 2021 | 38,303 | 518 | .631 | .975 | **34.4** [28.4, 40.2] | 0.219 [0.062, 0.424] | PASS | PASS | PASS |
| 2021 excl. offset | 37,695 | 462 | .708 | .988 | **28.0** [21.6, 34.0] | 0.508 [0.205, 0.958] | PASS | PASS | PASS |

**H7(b)′ — PASS on 2020, all three conditions met.** Among `clear_post ≤ 2` events split by
`s1_post` relative to the **same-month median**:

| | high-S1 n | p(high-S1) [CI] | low-S1 n | p(low-S1) | c1 < .80 | c2 CI-upper < .85 | c3 not higher |
|---|---|---|---|---|---|---|---|
| **2020** | 243 | **0.626** [0.548, 0.712] | 1,265 | 0.883 | ✔ | ✔ (0.712) | ✔ |
| 2021 | 172 | 0.523 [0.434, 0.618] | 346 | 0.685 | ✔ | ✔ (0.618) | ✔ |
| 2021 excl. offset | 160 | 0.619 [0.543, 0.719] | 302 | 0.755 | ✔ | ✔ (0.719) | ✔ |

Registration curves, rate (n) across bins 0 / ≤2 / ≤4 / ≤6 / ≤9 / ≤14 / >14 — monotone from bin 2 up in both years:
- **2020**: .899 (1,011) · .724 (497) · .824 (814) · .907 (1,146) · .956 (2,084) · .977 (4,759) · .986 (29,461)
- **2021**: .699 (173) · .597 (345) · .763 (718) · .872 (1,002) · .922 (1,665) · .970 (4,036) · .980 (30,364)

Within-month S1 quartiles among `clear_post ≤ 2` — the decline sits in the S1-*dense* tail, the opposite of "no observations, no change": 2020 .890 → .929 → .851 → **.684**; 2021 .777 → .631 → .638 → **.477**.

**Reading the year difference.** 2020's gap (14.1 pp) is under half 2021's (34.4 pp) and p(≤2) is much higher (.842 vs .631). Part is real, part is the dating asymmetry: 2020's low-observation events are enriched for those RADD could still date from a late snapshot, i.e. the cleaner un-re-disturbed ones. Direction, monotonicity, the S1-quartile pattern and every pre-registered verdict replicate; the effect **size** does not, and should be quoted as a range across years, not as 2021's number.

## 5. Continuation
H7(b)′ and H1″ both pass on 2020 → **P3 and P4 run**, per PLAN.md §6.

## 6. Compute / compliance
Polygon `reduceRegions` and centroid `sampleRegions` only; no image exports; within the 40 EECU-h ceiling. No `data/`, shapefiles or credentials committed.
