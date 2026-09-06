# AEF research — package board

Stages 1–5 (landscape → screen → feasibility → proposals → ranking → ROI) are recorded in
`aef_explore/`. This board tracks the TB01 execution packages.

## TB01 — Annual embedding: within-year event timing and detection lag

**Batch verdict (P2–P4b): GO, effect size scoped per region-year** — see `aef_explore/stage5/TB01/BATCH_SUMMARY.md`.

- [x] **P1 — expert-dated event set and registration curve** (`aef_explore/stage5/TB01/`)
      *Done, verdict FAIL.* 283 optical-bracketed events (A 252, B 31; both short of the 300
      target). τ_A = 11.39°, τ_B = 19.13°. H1 FAIL, H2 rejected but ≤ 0.4 pp, H3 PASS.
      Failed **by design**: the ≤ 62-day Alerta bracket admits only well-observed events, so
      P(registered) sat on a ~0.996 ceiling and H1 was untestable.
      ⚠️ §5 (RADD latency) is **superseded** — see `P1d/P1_RADD_correction.md`.
      ⚠️ H1's ceiling is resolved by P1d, which reaches the low-observation regime P1 could not.
- [x] **P1c — SAR-dated event population** (`aef_explore/stage5/TB01/P1c/`)
      *Done, pre-registered gate FAILED → stopped at step 2.* S1 single-breakpoint dating on all
      1,916 events gave median |SAR − midpoint| 27.0 d (needed ≤ 20) and 27.9 % inside the
      tightened interval (needed ≥ 70 %); no diagnostic variant came close. Steps 3–5 not run.
      Delivered anyway: the un-selected 1,916-event population, the corrected in-polygon RADD
      result, and full-population registration A 0.9928 / B 0.9492.
- [x] **P1d — RADD-dated event population and the low-observation test** (`aef_explore/stage5/TB01/P1d/`)
      *Done, pre-registered gate PASSED, RADD dating adopted.* Event date = first RADD alert inside
      the polygon; coverage A 97.6 % / B 85.4 % of 1,916 events. Gate: median distance to the
      tightened interval **0 d** (≤ 20 required); RADD leads the optical midpoint by 10 d.
      **H1′ criterion MET** — registration 0.652 at ≤ 2 post-event clear observations vs 0.986 at
      ≥ 5, gap **+33.3 pp** [8.4, 68.1] — but on only 23 events in the 0–2 bin, below the 30-event
      floor, so recorded **PASS (provisional, power-limited)**. **H3 PASS** (0.9855).
      Circularity check does not support the RADD/AEF-shared-input worry (B gap is negative).
- [x] **P2 — QC, Amazon-wide scale-up, decisive covariate** (`aef_explore/stage5/TB01/P2/`)
      *All 6 steps done. H1″ PASS, H3 PASS, **H7 FAIL as pre-registered → batch stopped**.*
      40,771 events (37,689 DETER + 3,082 RADD-only), 38,303 RADD-dated, 9 states.
      Registration **0.631** at `clear_post ≤ 2` (n = 518) vs **0.975** at `≥ 5`; gap **+34.4 pp**
      [28.3, 40.3], monotone over seven bins. Robust in 8/9 variants.
      H7(b) is *inestimable* (1 event in the stratum), not substantively failed — a
      timing-controlled diagnostic gives 0.523 [0.431, 0.626] and refutes "no observations, no change".
      ⚠ **Pending QC** — `qc_table.csv` decisions unfilled; all verdicts provisional.
- [x] **P2b — 2020 out-of-sample replication + re-pre-registered H7(b)′** (`.../P2b/`)
      *Done. **H7(b)′ PASSES on 2020**, H1″/H3/H7(a) all replicate → STOP lifted.*
      Offset check: 608/1,332 (45.7 %) of unregistered 2021 events OFFSET_SUSPECT; H1″ and H7(a)
      survive their exclusion. 2020: 45,917 events, 39,772 dated; high-S1 low-optical stratum
      registers **0.626** [0.548, 0.712] (< 0.80, CI-upper < 0.85, below low-S1 0.883).
      H1″ gap +14.1 pp [11.6, 16.6] (2021: +34.4). ⚠ no RADD snapshot contemporaneous with 2020.
- [x] **P3 — deferral and attribution** (`.../P3/`) — *H4 **PASS** both directions; H5 **not testable**.*
      Deferral 0.940 [0.922, 0.957] (2020→2021) and 0.965 [0.953, 0.975] (2021→2022); only ~1 in 800
      events register in neither year. H5's ground truth is degenerate (one true year per population),
      so k = 0 is perfect by construction — reported as an artifact, not a pass. Naive dating
      misattributes 2.78 %/3.48 %; a two-year window removes ~95 %; AUC(`clear_post`) 0.73/0.71.
- [x] **P4 — Congo replication** (`.../P4/`) — ***not replicated** on the pre-registered criterion.*
      5,243 TMF-2021 patches ≥ 1 ha in two DRC ROIs, 94.6 % RADD-dated, τ_CG = 16.31°. Gap
      **5.34 pp** [2.91, 8.20] falls outside both Brazil CIs; not power-limited (n(0–2) = 202).
      Direction replicates and H7(a) is the strongest of any region (2.19 [1.44, 2.84]).
      ⚠ no 2021 africa RADD archive — dates come from 2024 snapshots.
- [ ] **P5 — products** — pending (explicitly not started in this batch)
- [ ] **P6** — pending
