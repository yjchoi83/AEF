# AEF research — package board

Stages 1–5 (landscape → screen → feasibility → proposals → ranking → ROI) are recorded in
`aef_explore/`. This board tracks the TB01 execution packages.

## TB01 — Annual embedding: within-year event timing and detection lag

- [x] **P1 — expert-dated event set and registration curve** (`aef_explore/stage5/TB01/`)
      *Done, verdict FAIL.* 283 optical-bracketed events (A 252, B 31; both short of the 300
      target). τ_A = 11.39°, τ_B = 19.13°. H1 FAIL, H2 rejected but ≤ 0.4 pp, H3 PASS.
      Failed **by design**: the ≤ 62-day Alerta bracket admits only well-observed events, so
      P(registered) sat on a ~0.996 ceiling and H1 was untestable.
      ⚠️ §5 (RADD latency) is **superseded** — see `P1d/P1_RADD_correction.md`.
- [x] **P1c — SAR-dated event population** (`aef_explore/stage5/TB01/P1c/`)
      *Done, pre-registered gate FAILED → stopped at step 2.* S1 single-breakpoint dating on all
      1,916 events gave median |SAR − midpoint| 27.0 d (needed ≤ 20) and 27.9 % inside the
      tightened interval (needed ≥ 70 %); no diagnostic variant came close. Steps 3–5 not run.
      Delivered anyway: the un-selected 1,916-event population, the corrected in-polygon RADD
      result, and full-population registration A 0.9928 / B 0.9492.
- [ ] **P1d — RADD-dated event population and the low-observation test** — *in progress*
- [ ] **P2** — pending
- [ ] **P3** — pending
- [ ] **P4** — pending
- [ ] **P5** — pending
- [ ] **P6** — pending
