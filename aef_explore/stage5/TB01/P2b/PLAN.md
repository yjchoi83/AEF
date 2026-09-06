# TB01-P2b — PLAN (written before any 2020 computation)

**Why.** P2 established H1″ at Amazon scale (registration 0.631 at `clear_post ≤ 2` vs 0.975 at
`≥ 5`, +34.4 pp [28.3, 40.3], n = 38,303) and passed H7(a), but **H7(b) was inestimable**: only 1
event had `clear_post ≤ 2` *and* `s1_post ≥ overall median`, because both counts are driven by how
much of 2021 remains after the event date. Human QC has since cleared the label-noise worry (3/8
unregistered low-observation events verified real, 0/8 false polygons; `P2/qc_decisions.md`).
P2b does two things: it re-pre-registers H7(b) in a timing-controlled form, and — because the
timing-controlled statistic was **already seen on 2021** — it moves the confirmatory test to an
**out-of-sample year, 2020**.

## 1. Disclosure of prior exposure (required reading for the criterion below)

**The 2021 timing-controlled diagnostic was computed and inspected before this criterion was
fixed.** It returned registration **0.523** [0.431, 0.626] on n = 172 among `clear_post ≤ 2`
events with at-or-above-own-month-median S1, and a monotone decline across within-month S1
quartiles (0.777 → 0.631 → 0.638 → 0.477). That number is therefore **not confirmatory evidence**
and is reported in P2b only as the exploratory result it is. **2020 is the confirmatory year**:
no 2020 registration statistic has been computed at the time of writing.

## 2. Step 1 — finish the 2021 offset check (already running when this PLAN was written)

For every 2021 event unregistered at τ_state(p90): mean 2020→2021 angular change over the polygon
interior (10 m inward buffer) vs over a **50–150 m outer ring** (`buffer(150) \ buffer(50)`).
**`OFFSET_SUSPECT` iff ring > τ and interior < τ.** Note that for unregistered events
`interior < τ` holds by construction, so the flag reduces to `ring > τ`. Report the share per
region/state, then **rerun 2021 H1″ and H7(a) excluding flagged events** as a sensitivity.

## 3. Step 2 — 2020 population

- DETER **2020** CR+VEG polygons ≥ 1 ha, Brazilian Legal Amazon (WFS `deter-amz:deter_amz`).
- Event date = first RADD alert inside the polygon (`Alert ≥ 2`, `Date` masked to 2020–21),
  `date_upper = min(radd_any, view_date)`; `radd_high` = `Alert = 3`.
- **`radd_only_2020`**: DETER **2021** polygons ≥ 1 ha with no DETER 2020 overlap containing ≥ 1 ha
  of high-confidence RADD **2020** alerts.
- Layers: twelve monthly **2020** S2 clear-observation counts (SCL ∉ {3,8,9,10,11}) and twelve
  monthly 2020 S1 GRD IW scene counts (both passes, VV present); `clear_post` / `s1_post` prorated
  in the event month, as in P2.
- Registration: **2019→2020** angular change, polygon interior; per-state τ = p90 of that change on
  ≥ 2,000 stable-forest pixels (TMF `Dec2019 = 1 ∧ Dec2020 = 1`, Hansen `lossyear ∉ {18,19,20,21}`).

## 4. Step 3 — pre-registered **H7(b)′** (the new criterion, fixed here)

Among events with `clear_post ≤ 2`, split by `s1_post` relative to the **median of events sharing
the same event month**. **H7(b)′ passes iff all three hold:**
1. registration in the **high-S1 stratum** (`s1_post ≥ own-month median`) is **< 0.80**;
2. the **upper bound of its block-bootstrap CI is < 0.85**;
3. it is **not higher** than registration in the low-S1 stratum.

Failing H7(b)′ means low registration is explained by sparse observation in general rather than by
sparse *optical* observation — the "no observations, no change" reading — and the batch **stops**.

## 5. Step 4 — replication

H1″ (registration at `clear_post ≤ 2` ≥ 5 pp below `≥ 5`, CI excluding 0, n(0–2) ≥ 100), **H3**
(≥ 95 % at `clear_post ≥ 5`) and **H7(a)** (the `clear_post` coefficient's CI excludes 0 with
`s1_post` in the model) are re-run on 2020 and reported **side by side with 2021**, all CIs by
0.5° block bootstrap, 1,000 draws.

## 6. Step 5 — conditional continuation

**If H7(b)′ and H1″ both pass on 2020**, run **P3** (deferral 2020→2021 and 2021→2022; attribution
rule with `k` chosen on **2020** and evaluated on **2021**) and **P4** (Congo, TMF 2021 patches
dated by RADD) exactly as their existing PLANs. **If H7(b)′ fails, stop and report.**

## 7. Budget and compliance

Polygon `reduceRegions` and centroid `sampleRegions` only; **no image exports**; ≤ 40 EECU-hours.
Nothing under `data/`, no shapefiles, no credentials committed.

## 8. Outputs

`PLAN.md`, `P2b_events_2020.csv`, `P2b_offset_2021.csv`, `P2b_results.md` (≤ 60 lines); a
`RESEARCH_LOG.md` line and `PROGRESS.md` update per step; `BATCH_SUMMARY.md` refreshed at the end.
