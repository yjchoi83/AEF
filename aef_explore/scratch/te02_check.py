import sys; sys.path.insert(0,'scratch')
from aefkit import *
ROIS={
 'KE_marsa':[37.4,1.9,37.9,2.4],      # Horn of Africa dryland shrub
 'ET_somali':[42.6,6.6,43.1,7.1],     # HoA 2020-22 drought
 'SN_ferlo':[-15.2,15.0,-14.7,15.5],  # Sahel
 'ZW_mata':[27.5,-20.3,28.0,-19.8],   # S Africa 2023-24 El Nino
 'AU_mulga':[145.0,-25.5,145.5,-25.0],# Australia dryland
 'US_az':[-110.3,32.2,-109.8,32.7],   # SW US drought
 'ES_dehe':[-6.3,38.7,-5.8,39.2],     # Iberia 2022
 'BR_caat':[-40.5,-9.5,-40.0,-9.0],   # Caatinga
}
S1=ee.ImageCollection("COPERNICUS/S1_GRD").filter(ee.Filter.eq('instrumentMode','IW')).filter(
    ee.Filter.listContains('transmitterReceiverPolarisation','VV'))
S2C=ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
E5=ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR")
ys=list(range(2017,2026))
print("roi | s1 per-year 2017..2025 | ret(22-25/18-21) | s2 2019 | era5")
for k,b in ROIS.items():
    r=ee.Geometry.Rectangle(b)
    s1=[S1.filterBounds(r).filterDate(f"{y}-01-01",f"{y+1}-01-01").size() for y in ys]
    s1=ee.List(s1).getInfo()
    s2n=S2C.filterBounds(r).filterDate("2019-01-01","2020-01-01").size().getInfo()
    a=sum(s1[5:9]); bq=sum(s1[1:5]); ret=round(a/bq,2) if bq else -1
    e5=E5.filterBounds(r).filterDate("2017-01-01","2026-01-01").size().getInfo()
    # annual precip totals to identify drought years
    pr=[E5.filterDate(f"{y}-01-01",f"{y+1}-01-01").select('total_precipitation_sum').sum()
        .reduceRegion(ee.Reducer.mean(),r,11000).get('total_precipitation_sum') for y in ys]
    pr=[round(v*1000,0) if v else None for v in ee.List(pr).getInfo()]
    print(k, s1, "ret", ret, "| s2_2019", s2n, "| era5 n", e5)
    print("   precip_mm", pr)
