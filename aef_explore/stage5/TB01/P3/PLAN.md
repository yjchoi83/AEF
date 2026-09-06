# TB01-P3 — PLAN (written before any computation)

Runs **only if P2's decisive gate H7 passes**. Uses the P2 Amazon-wide RADD-dated event population
and the P2 per-state thresholds τ_state unchanged.

## Step 7 — deferral
For every event **not registered in 2021**, compute the 2021→2022 polygon-interior mean angular
change `acos(⟨e2021, e2022⟩)` (10 m inward buffer) and apply the **same per-state threshold**
τ_state, re-estimated on 2021→2022 stable forest (TMF `Dec2021 = 1 ∧ Dec2022 = 1`, Hansen
`lossyear ∉ {20,21,22,23}`, ≥ 2,000 px per state) so the 2022 test is not borrowing the 2021
threshold's calibration.
- **H4** — **≥ 80 %** of 2021-unregistered events register in 2022, CI reported.
- Interpretation fixed in advance: H4 passing means the annual embedding **defers** these events by
  one year rather than missing them; H4 failing means a genuine miss population exists.

## Step 8 — attribution rule
Rule: assign an event to year **Y** if `clear_post ≥ k`, else to **Y+1**. `k` is chosen on a **50 %
split by 0.5° block** (blocks assigned to the fit half at random, seed fixed) by minimising
misattribution on that half; it is then **evaluated on the held-out half only**. Ground truth is the
RADD-dated event year. Baselines, evaluated on the same held-out half:
- **naive** — assign every event to the year in which the embedding first registers it;
- **two-year** — assign to Y if registered in either Y or Y+1, i.e. always Y for deferred events.
- **H5** — misattribution rate is reduced by **≥ 30 %** relative to the naive rule, with the
  block-bootstrap CI of the reduction **excluding 0**.

All CIs 0.5° block-bootstrap, 1,000 draws. Outputs `P3_results.md` (≤ 60 lines) and `P3_table.csv`.
