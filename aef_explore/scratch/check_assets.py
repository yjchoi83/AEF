import ee, sys
ee.Initialize(project='alpha-earth-app')
ids = [
 ("UMD/hansen/global_forest_change_2024_v1_12","I"),
 ("UMD/hansen/global_forest_change_2023_v1_11","I"),
 ("projects/JRC/TMF/v1_2023/AnnualChanges","C"),
 ("projects/JRC/TMF/v1_2024/AnnualChanges","C"),
 ("projects/JRC/TMF/v1_2023/DeforestationYear","C"),
 ("projects/JRC/TMF/v1_2023/DegradationYear","C"),
 ("JRC/GFC2020/V2","I"),
 ("GOOGLE/DYNAMICWORLD/V1","C"),
 ("ESA/WorldCover/v200","C"),
 ("ESA/WorldCover/v100","C"),
 ("JRC/GHSL/P2023A/GHS_BUILT_S","C"),
 ("JRC/GHSL/P2023A/GHS_POP","C"),
 ("GOOGLE/Research/open-buildings-temporal/v1","C"),
 ("GOOGLE/Research/open-buildings/v3/polygons","F"),
 ("LARSE/GEDI/GEDI02_A_002_MONTHLY","C"),
 ("LARSE/GEDI/GEDI04_A_002_MONTHLY","C"),
 ("LARSE/GEDI/GEDI04_B_002","I"),
 ("projects/radar-wur/raddalert/v1","X"),
 ("projects/glad/alert/UpdResult","X"),
 ("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1","I"),
 ("projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_collection100_integration_v1","I"),
 ("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1","I"),
 ("COPERNICUS/S2_SR_HARMONIZED","C"),
 ("COPERNICUS/S1_GRD","C"),
 ("LANDSAT/LC08/C02/T1_L2","C"),
 ("MODIS/061/MCD64A1","C"),
 ("ESA/WorldCereal/2021/MODELS/v100","X"),
 ("JRC/GSW1_4/GlobalSurfaceWater","I"),
 ("users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1","I"),
 ("projects/meta-forest-monitoring-okw37/assets/CanopyHeight","I"),
 ("ECMWF/ERA5_LAND/MONTHLY_AGGR","C"),
 ("NASA/GRACE/MASS_GRIDS_V04/LAND","C"),
 ("COPERNICUS/DEM/GLO30","C"),
 ("WorldPop/GP/100m/pop","C"),
 ("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL","C"),
]
for aid, kind in ids:
    try:
        if kind=="I": o=ee.Image(aid); n=len(o.bandNames().getInfo())
        elif kind=="C": o=ee.ImageCollection(aid); n=o.limit(1).size().getInfo()
        elif kind=="F": o=ee.FeatureCollection(aid); n=o.limit(1).size().getInfo()
        else:
            try: o=ee.ImageCollection(aid); n=o.limit(1).size().getInfo()
            except Exception: o=ee.Image(aid); n=len(o.bandNames().getInfo())
        print(f"OK   {aid} ({n})")
    except Exception as e:
        print(f"FAIL {aid} :: {str(e)[:70]}")
