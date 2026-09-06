import sys; sys.path.insert(0,'scratch')
from aefkit import *
rA = ee.Geometry.Rectangle([-72.6,-13.9,-71.8,-13.1])   # Andes (Cusco)
rB = ee.Geometry.Rectangle([-55.6,-6.5,-54.8,-5.7])     # Para lowland
wc = ee.Image("ESA/WorldCover/v200/2021")
print("WC bands", wc.bandNames().getInfo(), "start", wc.get('system:time_start').getInfo())
eth = ee.Image("users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1")
print("ETH bands", eth.bandNames().getInfo())
dem = ee.ImageCollection("COPERNICUS/DEM/GLO30").select('DEM').mosaic().setDefaultProjection('EPSG:3857',None,30)
era = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate('2021-01-01','2022-01-01')
print("ERA5 n", era.size().getInfo(), [b for b in era.first().bandNames().getInfo() if 'temperature_2m'==b or 'total_precipitation_sum'==b])
for nm,r in [('A',rA),('B',rB)]:
    st = ee.Terrain.slope(dem)
    s = dem.addBands(st.rename('slope')).reduceRegion(ee.Reducer.percentile([2,50,98]), r, 300).getInfo()
    h = eth.select(0).reduceRegion(ee.Reducer.percentile([2,50,98]), r, 100).getInfo()
    hist = wc.reduceRegion(ee.Reducer.frequencyHistogram(), r, 100).getInfo()['Map']
    tot=sum(hist.values())
    print(nm, "elev/slope", {k:round(v,1) for k,v in s.items()}, "hgt", {k:round(v,1) for k,v in h.items()})
    print(nm, "WC%", {k:round(100*v/tot,1) for k,v in sorted(hist.items(), key=lambda x:-x[1])[:8]}, "aef", aef(2021,r).bandNames().size().getInfo())
