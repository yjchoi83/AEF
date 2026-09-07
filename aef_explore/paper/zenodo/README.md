# When does an annual embedding register a clearing? — data and code

Deposit accompanying the manuscript *"When does an annual embedding register a clearing?
Observation supply and temporal fidelity of AlphaEarth annual embeddings in the Brazilian
Amazon, 2020–2021"*.

Everything needed to reproduce every number and every figure in the paper is here, except the
source satellite products, which are public and are named in Section 2 of the manuscript.

## What the study did

We asked which forest-clearing events an annual global embedding field records in the right
year. 77,967 expert-mapped clearings across the Brazilian Legal Amazon in 2020 and 2021 were
dated by combining Sentinel-1 RADD alerts with the mapping analyst's own detection date, and an
event counted as *registered* when the year-on-year angular change of the embedding exceeded a
per-state stable-forest threshold. Registration saturates where clear optical observation
follows the event and falls by 37–47 percentage points where it does not; radar coverage does
not compensate; and unregistered events are deferred to the following year rather than lost.

## Layout

    event_tables/     one row per clearing event — the analysis inputs
    model_code/       the model, the block bootstrap, and the scripts that re-derive the numbers
    extraction_code/  the Earth Engine and WFS steps that built the tables
    figure_code/      reproduces every figure at submission specification
    map_layers_100m/  GeoTIFF products for the two demonstration regions
    manuscript/       manuscript, supplementary tables, bibliography, numbers trace

`MANIFEST.md` lists every file with its size and a truncated SHA-256.

## Reproducing the numbers

    OMP_NUM_THREADS=1 python model_code/run_numbers.py event_tables/s1_post_2020_derived.csv
    python model_code/intensity.py
    python model_code/numbers_trace.py
    python model_code/supplementary.py

`OMP_NUM_THREADS=1` matters: the block bootstrap runs one process per core, and multithreaded
BLAS inside each of them slows the run by roughly an order of magnitude. Expect about twenty
minutes on 32 cores, almost all of it in the 1,000-draw bootstraps of the logistic coefficient.

Scripts under `extraction_code/` need an authenticated Earth Engine session and network access
to the TerraBrasilis WFS; they are included for completeness, not because reproduction requires
re-running them — their outputs are the tables in `event_tables/`.

## The event tables

Each row is one clearing event. The columns that matter for the argument are the event date
under each dating rule (`radd_any`, `date_upper`), the post-event clear Sentinel-2 observation
count and Sentinel-1 scene count prorated from that date (`clear_post_*`, `s1_post_*`), the mean
interior angular change of the embedding across the event year, the state stable-forest
threshold τ at three percentiles, the resulting registration flag, and a 0.5° block identifier
used as the bootstrap resampling unit.

Two conventions are worth stating because they are easy to get wrong. `date_upper` is
`min(first RADD alert inside the polygon, DETER view_date)` and is the manuscript's primary
dating rule; `radd_any` alone is the pre-registered sensitivity. And registration depends only
on the angular change and the threshold, never on the event date, which is why the deferral and
offset analyses are invariant to the dating rule.

## The map layers

`map_layers_100m/` holds, for the Pará / BR-163 and southern Roraima demonstration regions:
2020→2021 angular change (×100, Int16, 100 m, tiled), the registration mask, the layer of
pixels unregistered in 2021 that register in 2022, and at 200 m the monthly clear-observation
supply climatology (×10) and the deferral risk it implies (×1000). Resolution and scaling are in
every filename. Coarser-than-native resolution is a constraint of extracting a 64-band product
over a 200 km region, not a scientific choice; the manuscript says so in Section 4.7.

An earlier "attribution confidence" layer is deliberately **not** included. It applied a link
fitted on post-event observation counts to an annual count, and was retired; the reasoning is in
Section 5.2 of the manuscript.

## Licence and citation

Code: MIT. Data tables and derived layers: CC BY 4.0. The underlying products keep their own
terms — DETER and PRODES from INPE, RADD from Wageningen University and Global Forest Watch,
JRC Tropical Moist Forest, Sentinel-1 and Sentinel-2 from Copernicus, and the AlphaEarth
Foundations annual embedding from Google DeepMind.

Cite the manuscript. If you use only the tables or the layers, cite this deposit as well.
