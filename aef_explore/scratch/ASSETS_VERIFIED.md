# GEE asset IDs verified in-session 2026-09-03 (project alpha-earth-app)
OK: GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL (64 bands, calendar-year, 2017-2025 live)
OK: UMD/hansen/global_forest_change_2025_v1_13 (CURRENT; 2024_v1_12 and 2023_v1_11 exist but deprecated)
OK: projects/JRC/TMF/v1_2024/{AnnualChanges,DeforestationYear,DegradationYear}  (also v1_2023)
OK: GOOGLE/DYNAMICWORLD/V1 | ESA/WorldCover/{v100,v200}
OK: JRC/GHSL/P2023A/{GHS_BUILT_S,GHS_POP} | WorldPop/GP/100m/pop
OK: GOOGLE/Research/open-buildings-temporal/v1 | GOOGLE/Research/open-buildings/v3/polygons
OK: LARSE/GEDI/{GEDI02_A_002_MONTHLY,GEDI04_A_002_MONTHLY,GEDI04_B_002}
OK: projects/radar-wur/raddalert/v1 | projects/glad/alert/UpdResult
OK: projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1 (39 bands)
OK: projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1 (38 bands)
OK: COPERNICUS/S2_SR_HARMONIZED | COPERNICUS/S1_GRD | LANDSAT/LC08/C02/T1_L2
OK: MODIS/061/MCD64A1 | ESA/WorldCereal/2021/MODELS/v100 | JRC/GSW1_4/GlobalSurfaceWater
OK: users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1 | projects/meta-forest-monitoring-okw37/assets/CanopyHeight (IC)
OK: ECMWF/ERA5_LAND/MONTHLY_AGGR | NASA/GRACE/MASS_GRIDS_V04/LAND
OK: COPERNICUS/DEM/GLO30_2024_1 (CURRENT; GLO30 deprecated)
NOT FOUND as given: JRC/GFC2020/V2 (is an ImageCollection, V3 not an IC either -> check exact type),
  MapBiomas collection10 id, projects/sat-io/open-datasets/GMW/annual-extent (GMW: use sat-io alt id or external).
Boilerplate: ee.Initialize(project='alpha-earth-app'); AEF year Y = filterDate(Y-01-01,(Y+1)-01-01).filterBounds(roi).mosaic()
Note: whole-collection getInfo() on AEF raises "User memory limit exceeded" -> never call it.

## Structure details verified
- projects/radar-wur/raddalert/v1: IC, system:index like 'africa_20240103'/'sa_*'; bands ['Alert','Date'];
  select images with .filterMetadata('layer','contains','alert'); Date band = YYDDD-style julian -> gives
  MONTH-level event dates for TB01 timing tests.
- MapBiomas secondary-vegetation age v1: single Image, bands secondary_vegetation_age_1986..2023 (age in years).
- projects/JRC/TMF/v1_2024/{DeforestationYear,DegradationYear}: IC of 1 image, band name 'constant'.
- AEF coverage over DPRK verified for ALL years 2017-2025 at Pyongyang, Sinuiju, Ryonpho, Jungpyong, DMZ Cheorwon,
  plus ROK side (Seoul). Dynamic World has 56 images over Pyongyang for 2023; ESA WorldCover v200 covers DPRK.
  -> D1 (TH01) is data-feasible even with LABELS=FALLBACK.
