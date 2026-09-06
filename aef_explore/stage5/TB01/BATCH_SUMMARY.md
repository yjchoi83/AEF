# TB01 batch P2–P4 — summary and revised GO statement

> **QC COMPLETE.** All 53 chips adjudicated — `P2/qc_decisions.md`, `P2/qc_table.csv`.
> **⚠ BATCH STOPPED AFTER P2.** The decisive gate H7 failed *as pre-registered*, so under the STOP
> rule **P3 (deferral/attribution) and P4 (Congo replication) were not run.** Their PLANs are
> written and unchanged, ready to execute once the gate question is resolved.

## QC result
The 53 contact-sheet chips have been adjudicated by a human reviewer. Of the eight unregistered
low-observation events, **3 are verified real clearings** (B_131, B_140, B_141), **1 is real but
only partly inside the polygon** (A_336, change at the polygon edge), **1 is offset-suspect**
(B_139, change signal adjacent to the polygon), and **4 are unverifiable** (A_320 no clear
post-event view, A_328 haze, B_134 cloud) — unverifiable for precisely the reason they are in the
low-observation bin at all. **None was adjudicated a false DETER polygon, so there is no evidence
that the unregistered low-observation events are label noise**, and the H1″ result stands on its
own terms. All 45 registered controls are confirmed real; five (B_125, B_527, A_288, A_309, A_161)
sit near τ and would flip under a modestly higher threshold, which is what the p85/p95 robustness
rows already probe. The single offset-suspect case is the reason P2b adds a polygon-interior vs
50–150 m outer-ring geometric check on every unregistered event.

## What P2 established
- **Population.** 37,689 DETER 2021 CR+VEG events ≥ 1 ha across 9 states, plus **3,082 `radd_only`** events (2021 clearings DETER first mapped in 2022) = **40,771**; 38,303 RADD-dated. RADD in-polygon coverage 0.50–0.98 by state.
- **H1″ PASS.** Registration **0.631** at `clear_post ≤ 2` (n = 518) vs **0.975** at `≥ 5` (n = 36,638) — **+34.4 pp**, CI **[28.3, 40.3]**; monotone across seven bins (0.60 → 0.98). P1d's 23-event provisional finding is confirmed at 22× the sample.
- **H3 PASS.** 0.975 at `clear_post ≥ 5`.
- **Robust.** H1″ holds in 8 of 9 variants (τ p85/p90/p95, high-confidence RADD, `date_upper`, with/without `radd_only`, size classes); the ninth (< 5 ha, n(0–2) = 5) is underpowered, not failed.
- **`radd_only` events register at 0.753 vs 0.984** for DETER-mapped ones; RR — the low-observation state — sits at 0.796 against 0.955–1.000 elsewhere.

## Why the batch stopped
H7 required (a) the `clear_post` effect to survive conditioning on `s1_post`, **and** (b)
registration at `clear_post ≤ 2` to stay below 80 % among events with `s1_post ≥ median`.
**(a) passes** (joint coefficient CI [0.046, 0.429]). **(b) is inestimable**: exactly **1** event in
38,303 satisfies both conditions, because `clear_post` and `s1_post` are both driven by how much of
2021 remains after the event date — 79 % of low-optical events are Oct–Dec, when S1 counts are also
small. The criterion selected an empty stratum.

A timing-controlled diagnostic (**not pre-registered, not a substitute**) answers the underlying question in the opposite direction: among `clear_post ≤ 2` events whose `s1_post` is at or above their **own month's** median, registration is **0.523** [0.431, 0.626] on n = 172, and within the low-optical group registration *falls* as within-month S1 density rises (0.777 → 0.477). Neither disjunct of the brief's own definition of "H7 fails" holds.

**Letter and stated intent disagree.** Rather than resolve that myself I took the conservative branch of the STOP rule. The fix is to re-pre-register H7(b) with a timing-controlled S1 stratum (density relative to the event month) — which must be fixed *before* re-running, not after seeing this number.

## Revised GO statement
**CONDITIONAL GO — one decision remaining.** The core claim is stronger than at any earlier stage: the annual AlphaEarth embedding registers essentially every clearing that is optically re-observed (0.975 at ≥ 5 clear observations) and misses roughly a third of those that are not (0.631 at ≤ 2), on 38,303 events, with tight CIs and robustness across nine variants. This is **not** "no observations, no change" — S1 density does not explain it. The paper is not downgraded on the evidence, and condition (1) — QC confirmation that the low-observation non-registrations are not label noise — is now **met** (see QC result above). GO remains withheld only on (2): H7(b) must be re-pre-registered in timing-controlled form. P3 and P4 then run unchanged.

## Known limitations recorded now
- MA (1,268 px) and TO (251 px) missed the ≥ 2,000-px stable-forest floor; their τ is provisional (356 events, 0.9 %).
- H7(a) is not uniformly robust — the joint coefficient CI crosses 0 under τ p85, `date_upper`, size ≥ 25 ha.
- `clear_post` moved from P1d's exact per-scene dates to monthly counts prorated in the event month, forced by running Amazon-wide.
- P5 (products) not started, as instructed.
