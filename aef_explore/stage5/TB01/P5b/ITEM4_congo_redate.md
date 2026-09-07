# P5b item 4 — Congo re-dated on 2021-vintage RADD

> **The GFW API key unblocks P4b. The re-dating was performed — and it dissolves the test.**
> Under `wur_radd_alerts/v20220109`, the Congo low-observation bin collapses from
> **n(0–2) = 202 to n(0–2) = 8**, because P4's low bin was built almost entirely out of
> 2024-vintage dates that fall in **2022** — after the observation year — which forced
> `clear_post` to zero mechanically. The pre-registered n ≥ 100 floor is not met, so the
> three-way scale **cannot be applied**: the verdict is **not testable under 2021-vintage
> dating**, not "not replicated". **H7(a) still replicates** (coef 0.737 [0.190, 1.349]).

Scripts: `p4b_patches.py` (patch regeneration + monthly S2/S1 counts),
`p4b_redate.py` (local re-dating against the downloaded tiles), `p4b_analyze.py`.
Numbers in `p4b_stats.json`; event table `P4b_events_redated.csv`.

## Access — the route P4b identified, now working

`GET https://data-api.globalforestwatch.org/dataset/wur_radd_alerts/v20220109/download/geotiff`
`?grid=10/100000&tile_id={10N_020E|00N_020E}&pixel_meaning=date_conf`, header `x-api-key`.
Both tiles returned **HTTP 200**, ~72 MB each, `uint16` at 0.0001° (~10 m),
`value = confidence·10000 + days since 2014-12-31`. The dataset metadata confirms
`content_date 2022-01-09`, so the vintage covers all of 2021 and nine days of 2022.

## Patch set

The P4 recipe was re-run (TMF v1_2024, `Dec2020 = 1 ∧ Dec2021 ∈ {2,3}`, ≥ 11 connected 30 m
px, 16 tiles per ROI): **5,252** patches against P4's 5,243 — the nine extra are tile-edge
duplicates. **4,951** match a P4 event within 200 m and are used, so old and new dates are
compared on identical footprints.

## Dating coverage and date movement

| | 2024 vintage (P4) | **2021 vintage (P5b)** |
|---|---|---|
| patches dated | 4,959 / 5,243 = **94.4 %** | 4,749 / 5,252 = **90.4 %** |
| dates falling in 2022 | 3.45 % of dated patches | 0.04 % (2 patches, both ≤ Jan 9) |

Among the 4,951 matched patches, **260 (5.3 %) lose their date** under the 2021 vintage —
and **58.5 % of those had `clear_post ≤ 2` under P4**. The censoring lands squarely on the
low-observation bin, for the obvious reason: a clearing late in 2021 has not yet accumulated a
confirmed alert by 2022-01-09.

For the 4,691 patches dated by both vintages:

| date shift (new − old), days | p5 | p25 | **p50** | p75 | p95 |
|---|---|---|---|---|---|
| | −70 | −2 | **0** | 0 | 0 |

**89.0 % move by ≤ 30 days; 10.96 % move by more than 30 days** and 3.84 % by more than 90.
25.8 % move earlier, none later — as expected, since the later vintage can only add re-alerts.
So the two vintages agree on *most* patches; they disagree on precisely the ones that carried
P4's result.

## The re-dated model

| `clear_post` | 0 | 0–2 | 2–4 | 4–6 | 6–9 | 9–14 | 14+ |
|---|---|---|---|---|---|---|---|
| n | 0 | 8 | 30 | 73 | 102 | 294 | 4,184 |
| registered | — | 1.000 | 1.000 | .945 | .990 | .990 | 1.000 |

| statistic | P4 (2024 vintage, n = 4,959) | same 4,691 patches, old dates | **P5b (2021 vintage)** |
|---|---|---|---|
| n(0–2) | 202 | 50 | **8** |
| p(≤ 2) | .945 | .940 | 1.000 |
| p(≥ 5) | .999 | .999 | .999 |
| gap pp [CI] | **5.34** [2.91, 8.20] | 5.91 [−0.07, 10.85] | **−0.13** [−0.25, −0.05] |
| H7(a) coef [CI] | 2.19 [1.44, 2.84] | — | **0.737** [0.190, 1.349] |

The middle column is the diagnostic: **restricting P4's own dates to the patches the 2021
vintage can also date already destroys the result** — n(0–2) falls to 50 and the CI touches
zero. P4's 5.34 pp was carried by the 260 patches whose 2024-vintage date is least
trustworthy, 152 of which sat in the low bin.

## Applying the pre-registered replication scale

The scale as recorded in `P4b/P4b_results.md` — *replicated* (CI overlaps Brazil 2021
[28.4, 40.2]) / *attenuated but consistent* (CI excludes 0, same sign, below that band) /
*not replicated* — presumes an estimable low-observation bin, which the pre-registered
criterion fixes at **n(0–2) ≥ 100**. Under 2021-vintage dating **n(0–2) = 8**.

**Verdict: NOT TESTABLE under 2021-vintage dating.** Not "attenuated but consistent" (the
sign is nominally negative but rests on 8 events), and not "not replicated" (the test the
criterion describes cannot be run). The honest statement for the paper is that **the Congo
gap has never been measured on trustworthy dates in either direction** — the 2024 vintage
supplies a bin that is a dating artifact, the 2021 vintage supplies almost no bin at all.

**H7(a) does replicate**: with `s1_post` in the model the `clear_post` coefficient is
**0.737 [0.190, 1.349]**, CI excluding zero, on re-dated Congo data. (P4's 2.19 came from
P4's own, unretained, fitting code; 0.737 is on P5b's reconstructed spec, the same one used
for the Brazil sensitivity table, where Brazil 2021 gives 0.217.)

**What would settle it.** A Congo event set dated by a vintage that both post-dates the
clearing year and pre-dates re-disturbance — practically, `v20220403` or `v20220704` for 2021
events — plus registration measured against the 2021→2022 embedding pair as well, so late-2021
events are not censored. That is a P6 task, not a re-analysis of these tables.
