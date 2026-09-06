# Stage-2 pilot kit (verified in-session 2026-09-03, LIVE mode)

## Environment
- `ee.Initialize()` works with NO project argument (default credentials). Do not pass a project.
- earthengine-api 1.7.42, sklearn/pandas available. Laptop-scale only.
- arXiv API: use **https**://export.arxiv.org/api/query (http returns 0 bytes in this environment).
- Semantic Scholar graph API returned empty bodies this session -> prefer OpenAlex + arXiv(https).

## AEF facts [V]
- `GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL`, 64 bands A00-A63, 10 m.
- Per-year image counts: 2017:10562 2018:10635 2019:10690 2020:10576 2021:10614 2022:10853
  2023:11074 2024:11073 2025:11078. So **2017-2025 = 9 layers** (STAC temporal extent field
  wrongly stops at 2025-01-01; the images exist).
- Catalog wording [V]: each pixel "encodes temporal trajectories of surface conditions at and
  around that pixel ... over a single **calendar year**"; `system:time_start`/`time_end` reflect
  that calendar year. => align reference labels to calendar years (PRODES Aug-Jul needs remap).
- Tiles are per-UTM-zone (`UTM_ZONE` property); `filterDate(year)+mosaic()` has **no fixed
  projection** -> always pass an explicit `scale=` and prefer point sampling (below).

## Verified GEE asset IDs [V] (checked with ee.data.getAsset)
OK: UMD/hansen/global_forest_change_2025_v1_13 (latest; 2024_v1_12 superseded but exists) |
projects/JRC/TMF/v1_2024/AnnualChanges | projects/JRC/TMF/v1_2023/AnnualChanges |
projects/JRC/TMF/v1_2022/DegradationYear | projects/radar-wur/raddalert/v1 |
projects/glad/alert/UpdResult |
projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1 |
.../collection9/mapbiomas_collection90_secondary_vegetation_age_v1 | GOOGLE/DYNAMICWORLD/V1 |
ESA/WorldCover/v200 | JRC/GHSL/P2023A/GHS_BUILT_S | JRC/GHSL/P2023A/GHS_POP |
GOOGLE/Research/open-buildings-temporal/v1 | GOOGLE/Research/open-buildings/v3/polygons |
LARSE/GEDI/GEDI02_A_002_MONTHLY | LARSE/GEDI/GEDI04_A_002_MONTHLY | LARSE/GEDI/GEDI04_B_002 |
users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1 |
projects/meta-forest-monitoring-okw37/assets/CanopyHeight | MODIS/061/MCD64A1 |
JRC/GSW1_4/GlobalSurfaceWater | ESA/WorldCereal/2021/MODELS/v100 | COPERNICUS/S1_GRD |
COPERNICUS/S2_SR_HARMONIZED | LANDSAT/LC08/C02/T1_L2 | LANDSAT/LC09/C02/T1_L2 |
WorldPop/GP/100m/pop | DLR/WSF/WSF2015/v1 | COPERNICUS/DEM/GLO30 |
ECMWF/ERA5_LAND/MONTHLY_AGGR | NASA/GRACE/MASS_GRIDS_V04/MASCON |
projects/forestdatapartnership/assets/{cocoa,coffee,rubber,palm}/model_2025b
NOT FOUND: mapbiomas collection10 (use collection9); the sat-io paths I guessed. CORRECTION [V, TA04]:
sat-io mirrors ARE readable - `projects/sat-io/open-datasets/global-mining/global_mining_polygons`
(Maus et al. 10.1038/s41597-022-01547-4) works; only my guessed IDs were wrong. Verify exact paths
against the awesome-gee-community-catalog rather than assuming the namespace is closed.
TESSERA is NOT in GEE -> treat TESSERA comparisons as desk-only unless you find a public mirror.

## Use the shared helper: `scratch/aefkit.py` (verified working)
```python
import sys; sys.path.insert(0,'scratch')
from aefkit import *          # ee already initialized; numpy/pandas as np/pd
roi = ee.Geometry.Rectangle([-55.5,-6.0,-55.0,-5.5])
img = aef(2021, roi).addBands(angle(2019,2021,roi)).addBands(lbl.unmask(0))
df  = samp(img, roi, n=3000)              # randomPoints + sampleRegions; keep n<=5000
df['blk'] = blocks(df, size=0.1)          # ~10 km spatial blocks for GroupKFold
probe(df, AEF_BANDS, 'y', df['blk'])      # -> (mean, sd, per-fold, n); AUC if binary, else bal-acc
probe(df, S2_BANDS,  'y', df['blk'])      # mandatory baseline: s2(y, roi) annual median composite
probe(df, ['angle_deg'], 'y', df['blk'], task='clf')
probe(df, AEF_BANDS, 'height', df['blk'], task='reg')   # ridge R2
samp(img, roi, strata=lblimg, classes=[0,1], per_class=1500)   # stratified for rare classes
```
Two gotchas that already cost time:
1. **Label rasters are masked outside their positive class** (Hansen `lossyear`, TMF, alerts).
   `sampleRegions` then silently drops those points (3000 -> 51). ALWAYS `.unmask(0)` labels.
2. `img.sample(numPixels=...)` under-returns badly on unprojected mosaics -> use `samp()`.

## Smoke reference numbers (Para, 55.5-55.0W / 6.0-5.5S, n=3000, only 11 positives -> indicative only)
Hansen loss-2020 detection, 3 spatial folds: AEF-64 probe AUC 0.67 (sd 0.17);
angle(2019,2021) alone AUC 0.91 (sd 0.13). Do not cite; re-run with stratified sampling.
