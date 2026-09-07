# P5b item 1 — what the `clear_post = 0` bin is

> **Answer: predominantly a dating error, with a genuinely unobserved minority inside it.**
> The zero bin is not a low-observation population — it is a population whose *assigned RADD
> date* sits far later than the DETER detection, which drives `clear_post` to zero
> mechanically. Recomputed from the DETER `view_date`, only **31 %** (2021) and **8.9 %**
> (2020) of these events are actually observation-poor. Pre-event disturbance is **not**
> supported; December truncation explains almost none of it.

Scripts: `fetch_zero_polygons.py` (DETER WFS polygon refetch, 1,176 of 1,184 matched),
`zero_bin_gee.py` (per-event angular change and monthly clear counts), `zero_bin_analysis.py`.
Numbers in `zero_bin_stats.json`; figure `figures/F9_zero_bin.png`.

**Extraction validated.** The re-extracted event-year angular change exceeds τ for 69.8 %
(2021) and 90.0 % (2020) of these events — identical to the stored registration rates 0.699
and 0.899. The prior-year numbers below therefore come from a pipeline that reproduces P2/P2b
registration exactly.

## 1. DETER `view_date` − RADD date

| | 2021 (n = 173) | 2020 (n = 1,011) |
|---|---|---|
| percentiles p5 / p25 / **p50** / p75 / p95 (days) | −293 / −229 / **−142** / −39 / +88 | −545 / −412 / **−339** / −243 / −20 |
| same, all dated events | −9 / +15 / **+44** / +112 / +376 | −60 / +8 / **+29** / +76 / +289 |
| RADD date **after** the DETER view | **83.8 %** | **96.8 %** |
| … same, all dated events | 8.4 % | 15.0 % |
| RADD date more than 90 days after | 65.3 % | 91.4 % |

The zero bin is dated late relative to detection by an order of magnitude more often than the
population it is drawn from. For 2020 the mechanism is already on record: the earliest RADD
snapshot covering 2020 is `sa_20211013`, so 2020 events are dated by 2021-vintage re-alerts.

## 2. Registration under `date_upper`

Switching to the `date_upper` dating variant dissolves most of the bin: **only 22.0 % (2021)
and 4.9 % (2020) of these events still have `clear_post = 0`**, and their median `clear_post`
becomes **4.74** and **15.65**. The `date_upper` zero bin is a much smaller, much worse-off
set — n = 38 registering at **0.289** (2021) and n = 50 at **0.500** (2020), i.e. *below* the
1–2 bin rather than above it. Under a dating rule that pushes dates earlier, the non-monotone
lift at zero disappears.

## 3. Prior-year angular change against τ

Prior year = 2019→2020 for the 2021 cohort, 2018→2019 for the 2020 cohort; τ is the same
per-state p90 of stable forest, which by construction 10 % of undisturbed pixels exceed.

| share with prior-year change > τ | 2021 | 2020 |
|---|---|---|
| all zero-bin events | 30.8 % | 79.0 % |
| … those that **registered** | 42.5 % | 85.6 % |
| … those that did **not** register | **3.8 %** | **19.8 %** |
| event-year change > τ (= registration) | 69.8 % | 90.0 % |

**This is the opposite of the pre-event-disturbance signature.** That explanation predicts
prior-year change *high* and event-year change *suppressed* among the events that fail to
register. Observed: the non-registering events are quiet in **both** years (3.8 % / 19.8 %
above τ, at or below the 10 % rate expected of undisturbed forest in 2021), while the
already-disturbed events are exactly the ones that do register. In 2020 the prior year is
genuinely busy (79 %) — these are re-disturbance-dated locations — and it does not stop them
registering.

## 4. Registration curve with December events excluded

| `clear_post` | 0 | 0–2 | 2–4 | 4–6 | 6–9 | 9–14 | 14+ |
|---|---|---|---|---|---|---|---|
| 2021, all | .699 | .597 | .763 | .872 | .922 | .970 | .980 |
| 2021, **December excluded** | **.723** | .601 | .770 | .872 | .922 | .970 | .980 |
| 2020, all | .899 | .724 | .824 | .907 | .956 | .977 | .986 |
| 2020, **December excluded** | **.908** | .767 | .833 | .909 | .957 | .977 | .986 |

December supplies only **18.5 %** (2021) and **4.7 %** (2020) of the zero bin, and dropping it
*raises* the zero-bin rate. Excluding December by DETER `view_date` instead of by RADD month
gives the same picture (.733 / .922). **The non-monotonicity is not a year-end truncation
artifact.**

## 5. `clear_post` recomputed from the DETER `view_date`

For the 155 (2021) and 985 (2020) events whose DETER detection falls inside the event year,
the same monthly clear-count layers and the same proration rule, applied to `view_date`:

| | 2021 | 2020 |
|---|---|---|
| percentiles p5 / p25 / **p50** / p75 / p95 | 0.0 / 1.3 / **5.8** / 16.8 / 39.4 | 0.7 / 8.1 / **15.7** / 25.2 / 48.2 |
| share still ≤ 2 | **31.0 %** | **8.9 %** |
| median, events that registered | 6.84 | 15.99 |
| median, events that did **not** register | **0.96** | **12.33** |
| share ≤ 2, events that did not register | 53.8 % | 31.4 % |

## Which explanation the data support

**Dating error, for the bin as a whole.** Two thirds (2021) to nine tenths (2020) of the zero
bin had ample post-detection optical coverage; the zero is a property of the RADD date
assigned to the event, not of the observation record. That also explains the non-monotone
lift directly: these events *were* well observed, so the embedding registers them at .699/.899
— above the genuinely observation-starved 1–2 bin (.597/.724).

**Genuine low observation, for the minority inside it.** The events that fail to register are
the ones that remain observation-poor when measured from the correct date — median `clear_post`
0.96 vs 6.84 in 2021, and 53.8 % of them at ≤ 2. The bin is a mixture, and both components
behave exactly as the paper's core claim predicts.

**Not pre-event disturbance** (§3) and **not December truncation** (§4).

**Consequence for the write-up.** The exactly-zero bin must be reported as a
*dating-artifact stratum*, not as the extreme of the observation axis; the registration curve
should be drawn from the 1–2 bin upward, with the zero bin shown separately and annotated.
The honest headline is that P2's H1″ gap is if anything *understated*: the low-observation
bin as defined contains a majority of well-observed, correctly-registering events.
