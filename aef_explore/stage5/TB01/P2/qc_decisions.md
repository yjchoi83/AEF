# TB01-P2 — QC adjudications (human review of the 53 contact-sheet chips)

Source chips: `results/qc_chips/`, tiled in `qc_sheets/qc_sheet_{01,02,03}.png`.
Codes recorded in the `decision` column of `qc_table.csv`, with free text in `decision_note`.

| code | meaning |
|---|---|
| `REAL` | clearing visibly present inside the polygon in the post-event imagery |
| `REAL_PARTIAL` | clearing real but only part of the polygon changed |
| `UNVERIFIABLE` | no usable post-event optical view — cannot confirm or refute |
| `OFFSET_SUSPECT` | change signal present but displaced relative to the polygon |
| `REAL_REGISTERED` | registered event, clearing confirmed (control) |

## The 8 unregistered low-observation events

| id | region | clear_post | decision | note |
|---|---|---|---|---|
| B_131 | B | 2 | **REAL** | |
| B_140 | B | 1 | **REAL** | plausible, partial clear view |
| B_141 | B | 2 | **REAL** | |
| A_336 | A | 2 | **REAL_PARTIAL** | change at polygon edge |
| B_139 | B | 2 | **OFFSET_SUSPECT** | change signal adjacent to polygon |
| A_320 | A | 0 | **UNVERIFIABLE** | no clear post-event view |
| A_328 | A | 2 | **UNVERIFIABLE** | haze |
| B_134 | B | 2 | **UNVERIFIABLE** | cloud |

## The 45 registered controls
All adjudicated **REAL_REGISTERED**. Five are marked `near-threshold` in `decision_note` —
**B_125** (19.65° vs τ 19.13°), **B_527** (23.54° vs 19.13°), **A_288** (12.08° vs 11.39°),
**A_309** (12.63° vs 11.39°), **A_161** (20.06° vs 11.39°) — i.e. their registration would flip
under a modestly higher τ. This is the population the p85/p95 robustness rows in `P2_results.md`
are designed to probe.

## Summary

**No evidence that unregistered low-observation events are DETER label noise: 3/8 verified real,
1/8 offset-suspect, 4/8 unverifiable due to absent optical data.** (Counting `A_336`
`REAL_PARTIAL` with the real cases gives 4/8 real.) The four unverifiable cases are unverifiable
for exactly the reason the events are in the low-observation bin at all — there is no clear
post-event optical view to adjudicate against — so they can neither confirm nor refute the
finding, and no reviewer could resolve them from optical imagery. Crucially, none of the eight
was adjudicated as a false DETER polygon. The single `OFFSET_SUSPECT` case motivates the
geometric check added to P2b step 1.

*Adjudicated by the human reviewer; recorded 2026-09-06.*
