# AEF research — package board

Stages 1–5 (landscape → screen → feasibility → proposals → ranking → ROI) are recorded in
`aef_explore/`. This board tracks the TB01 execution packages.

## TB01 — Annual embedding: within-year event timing and detection lag

**Batch verdict (P2–P4): CONDITIONAL GO, pending QC** — see `aef_explore/stage5/TB01/BATCH_SUMMARY.md`.

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
- [ ] **P2b — 2020 out-of-sample replication + re-pre-registered H7(b)′** — *in progress*
      Step 1 ✔ offset check: 608/1,332 (45.7 %) of unregistered 2021 events are OFFSET_SUSPECT;
      H1″ and H7(a) both still pass with them excluded (gap +28.0 pp [22.0, 34.4]).
- [ ] **P3 — deferral and attribution** — **not run** (P2 STOP rule fired); PLAN written and ready
- [ ] **P4 — Congo replication** — **not run** (P2 STOP rule fired); PLAN written and ready
- [ ] **P5 — products** — pending (explicitly not started in this batch)
- [ ] **P6** — pending
