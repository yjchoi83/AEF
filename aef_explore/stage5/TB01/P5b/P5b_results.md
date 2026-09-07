# TB01-P5b — fixes before drafting

Four items, each with its own results file, script set and commit. Everything below is
reproducible from the scripts in this directory; the only external credential used is
`GFW_API_KEY` (item 4), read from the environment and never written to disk.

| item | file | outcome |
|---|---|---|
| 1 | `ITEM1_zero_bin.md` | the `clear_post = 0` bin is a **dating artifact**, not a low-observation stratum |
| 2 | `ITEM2_obs_supply.md` | map layer (d) **retired**; replaced by observation-supply (F7) and deferral-risk (F8) plates |
| 3 | `../P2/P2_results.md` §6b | H7(a) coefficient + CI in all nine variants, three marked as crossing zero |
| 4 | `ITEM4_congo_redate.md` | Congo re-dated on RADD `v20220109`: the test is **not testable**, not failed |

## 1. Zero-bin diagnosis — dating error

83.8 % (2021) and 96.8 % (2020) of zero-bin events carry a RADD date *after* the DETER
`view_date` — median 142 and 339 days — against 8.4 % / 15.0 % in the population. Recomputed
from the DETER detection, only 31.0 % / 8.9 % are still observation-poor. Under `date_upper`
the bin nearly dissolves (22.0 % / 4.9 % remain at zero) and its non-monotone lift disappears.
Prior-year angular change exceeds τ for only 3.8 % / 19.8 % of the *non-registering* zero-bin
events, so pre-event disturbance is excluded; December supplies 18.5 % / 4.7 % of the bin and
excluding it raises the zero-bin rate, so year-end truncation is excluded. The bin is a mixture
of a mis-dated well-observed majority and a genuinely unobserved minority — and H1″'s gap is
therefore, if anything, understated. Figure `figures/F9_zero_bin.png`.

## 2. Observation supply replaces layer (d)

Layer (d) fed a model fitted on post-event counts the *annual* count (AUC 0.599 for deferral)
through a raw-count link that predicts .91 registration where one clear observation gives .59.
It is stamped RETIRED on both map plates and its GeoTIFFs renamed. The replacement layers,
from the 2019–2021 monthly Sentinel-2 record: **F7** mean clear observations per pixel per
calendar month (Pará peaks 6.5 in July, floors 1.0 in February; Roraima peaks 4.4 in March,
floors 1.3 in June — the regions are out of phase), and **F8** the deferral risk each event
month implies under a refitted log link (β₀ = −0.180, β₁ = 1.240), rising from ≈ .02 for
January–August events to **.354 / .306** for December ones, banded by Sentinel-2 orbit overlap.

## 3. H7(a) sensitivity

Added as `P2_results.md` §6b: coefficient and CI for all nine variants, with τ p85,
`date_upper` and size ≥ 25 ha marked as crossing zero under the pre-registered CIs. The P2
fitting script was not retained, so the model was rebuilt from `P2/PLAN.md` step 5 and
calibrated to P2's reported coefficients (0.211 → 0.213 solo, 0.219 → 0.217 joint); the refit
CIs come out narrower and the table is marked on the pre-registered ones, the conservative
reading.

## 4. Congo re-dating

`GFW_API_KEY` works; both tiles downloaded from the GFW Data API and the P4 patch set
regenerated so both vintages are compared on identical footprints. 2021-vintage coverage
**90.4 %** against 94.4 %; **11.0 %** of dates move by more than 30 days; **260 patches (5.3 %)
lose their date entirely and 58.5 % of those sat in P4's low-observation bin**. P4's bin turns
out to be an artifact — 3.4 % of 2024-vintage dates fall in 2022, after the observation year —
and re-dating drops n(0–2) from **202 to 8**, below the pre-registered floor of 100. The
three-way replication scale therefore cannot be applied: **not testable under 2021-vintage
dating**. H7(a) replicates (0.737 [0.190, 1.349]).

## Effect on the paper

- The Congo can no longer be quoted as "5.3 pp, not replicated". F5 was rebuilt to say so.
- The registration curve must show the zero bin as a separate stratum.
- The map product set loses a layer and gains two climatology layers.
- H7(a) is reported as directionally robust and marginally significant in three variants.

None of this touches the core claim. H1″, H3, H4 and H7(b)′ are unchanged, and item 1 makes
the Brazilian gap a conservative estimate rather than an inflated one.

## Compute / compliance

Earth Engine: two region passes for the monthly supply climatology, 1,176 single-event
extractions for item 1, and one patch-regeneration pass with per-patch monthly counts for
item 4 — comfortably inside the 15 EECU-hour ceiling; no batch exports, all downloads via
`getDownloadURL`/`getThumbURL`. The two 72 MB RADD tiles and the intermediate CSV/JSON stay in
the session scratchpad; only scripts, result documents, figures, `h7a_sensitivity.csv`,
`P4b_events_redated.csv` and the stats JSONs are committed. No credentials, no `data/`, no
shapefiles.
