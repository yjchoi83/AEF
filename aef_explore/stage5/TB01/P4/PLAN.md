# TB01-P4 — PLAN (written before any computation)

Runs **only if P2's decisive gate H7 passes**. External replication of the P2 finding outside
Brazil, in a bimodal-rainfall basin with a different observation calendar.

## Step 9 — Congo replication
- **ROIs.** Two ~100 × 100 km boxes in the DRC, chosen as the two highest-scoring candidates by
  **JRC TMF 2021 deforestation patch count** from a screen of candidate boxes over the DRC forest
  belt, required to be non-overlapping and ≥ 200 km apart.
- **Events.** TMF 2021 deforestation patches ≥ 1 ha (`projects/JRC/TMF/v1_2024/AnnualChanges`,
  `Dec2020 = 1 ∧ Dec2021 ∈ {2,3}` — i.e. undisturbed forest in 2020 that became degraded or
  deforested in 2021), vectorised and filtered to ≥ 1 ha. DETER does not exist here, which is the
  point: the label is not optical-alert-derived.
- **Dating.** First RADD alert inside the patch (`Alert ≥ 2`, africa tiles), same as P2.
- **Layers.** The same 12 monthly S2 clear-count and 12 monthly S1 scene-count images, built for
  2021 over the two ROIs; `clear_post` / `s1_post` by the same prorated rule.
- **Threshold.** One **regional** τ_CG = p90 of the 2020→2021 angular change on ≥ 2,000
  stable-forest pixels (TMF undisturbed 2020 and 2021, no Hansen loss 2019–22) pooled over the two
  ROIs — Congo is a single region here, not per-ROI, because the ROIs are small.
- **Model.** Identical specification to P2 step 5, with ROI in place of state.

**Pre-registered replication criterion.** The Congo `clear_post ≤ 2` vs `≥ 5` registration gap
**lies inside the Brazil (P2) block-bootstrap CI for that gap**. Reported with its own CI, plus
n(0–2) for Congo; if n(0–2) < 100 the replication is reported as **power-limited** alongside the
verdict rather than as a clean pass or fail.

Outputs `P4_results.md` (≤ 60 lines) and `P4_table.csv`.
