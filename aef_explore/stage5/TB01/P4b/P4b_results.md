# TB01-P4b — Congo re-dating

> **SUPERSEDED BY P5b ITEM 4 (2026-09-07).** `GFW_API_KEY` was supplied, route 1 below returned
> HTTP 200 for both tiles, and the re-dating **was performed** — see `../P5b/ITEM4_congo_redate.md`.
> Outcome: 2021-vintage coverage **90.4 %** (against 94.4 %), **11.0 %** of patches move by more
> than 30 days, and the low-observation bin collapses from **n(0–2) = 202 to 8** because P4's bin
> was built out of 2024-vintage dates falling in **2022**. The pre-registered n ≥ 100 floor is not
> met, so the three-way scale cannot be applied: **not testable under 2021-vintage dating**.
> H7(a) still replicates (0.737 [0.190, 1.349]). The record below is kept as written, for the
> access-route findings; its "P4's verdict stands" conclusion is no longer current.

## Original record (2026-09-07, before the key was supplied)


> **Pre-registered fallback fired: "If GFW/WUR RADD 2021 for Africa is not obtainable, stop and
> mark Congo dating-limited."** A 2021-vintage RADD Africa raster is **not obtainable from this
> environment**. No re-dating was performed; P4's verdict stands, now labelled dating-limited.

## What was sought
A RADD Africa product contemporaneous with 2021, to replace the GEE asset's earliest africa
snapshot (`africa_20240103`, ~2 years post-event) used in P4. **The right version exists and was
identified**: GFW Data API dataset **`wur_radd_alerts`**, version **`v20220109`** — the first
version whose coverage spans all of calendar 2021 (the version list runs `v20210704`, `v20211017`,
**`v20220109`**, `v20220403`, …). `v20211017` was rejected because it would truncate Nov–Dec 2021.

## Access routes attempted, with outcomes

| # | Route | Result |
|---|---|---|
| 1 | GFW Data API tile download — `GET /dataset/wur_radd_alerts/v20220109/download/geotiff?grid=10/100000&tile_id=10N_020E&pixel_meaning=date_conf` | **HTTP 403** — `"Request is missing valid API key"` |
| 2 | Underlying data lake — `s3://gfw-data-lake/wur_radd_alerts/v20220109/raster/epsg-4326/10/100000/date_conf/geotiff/{tile}.tif` via `gfw-data-lake.s3.amazonaws.com` | **HTTP 403 Forbidden** (bucket private) |
| 3 | Same path via `storage.googleapis.com` | **HTTP 404** (asset is on S3, not GCS) |
| 4 | GFW anonymous raster query — `POST /dataset/wur_radd_alerts/v20220109/query` with an ROI polygon | empty response; endpoint also key-gated |
| 5 | WUR direct — `radd-alert.wur.nl` (resolves to 137.224.9.30) | **TCP 443 and 80 both filtered** from this host; `curl` returns code 000 on http, https and `--insecure` |
| 6 | GFW public raster tile cache — `tiles.globalforestwatch.org/wur_radd_alerts/v20220109/default/{z}/{x}/{y}.png` | Bucket **is** public (returns `NoSuchKey`, not `AccessDenied`), but only **z = 8** tiles exist for both ROIs (z = 10/12/14 → 404). z = 8 is ~611 m/px against a median patch of **1.61 ha** (~127 m across), and the `default` symbology is styled RGB, not a decodable date band. **Unusable.** |
| 7 | Earth Engine `projects/radar-wur/raddalert/v1` re-checked across all `layer` values (646 alert images) | Only `radd_africa_alert_2019_*` and `radd_africa_alert_2020_*` archives exist; **no 2021 africa archive**; earliest rolling africa snapshot remains `africa_20240103` |
| 8 | Zenodo search for a mirrored RADD Africa 2021 release | No matching dataset |

Route 1 is the only viable one and needs a **GFW API key**, which requires creating an account
against an email address. I did not do that on the user's behalf — see *Unblocking* below.

## Consequence for the Congo result
P4 stands **unchanged and dating-limited**: gap **5.34 pp** [2.91, 8.20] on 4,959 RADD-dated
TMF-2021 patches, dated from 2024-vintage snapshots. Under the P4b three-way scale that verdict
would read **"attenuated but consistent"** (CI excludes 0 but lies below the Brazil-2021 CI
[28.4, 40.2]) rather than "not replicated" — but **that relabelling is not claimed here**, because
the P4b scale was written to be applied to *re-dated* estimates and no re-dating happened. The
dating vintage biases `clear_post` toward noise and therefore attenuates the gap, so 5.34 pp should
be read as a **lower bound** on the Congo effect.

The neither-reported-nor-testable quantities from the P4b brief — dating coverage under the 2021
vintage, and the share of patches whose date moves by > 30 days — remain **unmeasured**.

## Unblocking
One action by the user resolves this: register for a free GFW Data API key
(`https://data-api.globalforestwatch.org/#tag/Authentication`) and supply it as an environment
variable. The tiles needed are `10N_020E` (CG1) and `00N_020E` (CG2) at
`wur_radd_alerts/v20220109`, `pixel_meaning=date_conf`; the rest of P4b is scripted and would run
in well under an hour. Failing that, a WUR mirror reachable from this network would also work.
