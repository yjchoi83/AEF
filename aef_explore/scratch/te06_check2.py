import sys; sys.path.insert(0,'scratch')
from aefkit import *
cands = {'MT_sorriso':[-55.9,-13.0,-55.1,-12.2], 'CONUS_iowa':[-94.2,41.6,-93.4,42.4],
         'PA_arc':[-49.9,-3.6,-49.1,-2.8]}
dem = ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").select('DEM').mosaic().setDefaultProjection('EPSG:3857',None,30)
wc = ee.Image("ESA/WorldCover/v200/2021"); eth = ee.Image("users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1")
for nm,c in cands.items():
    r = ee.Geometry.Rectangle(c)
    s = dem.addBands(ee.Terrain.slope(dem).rename('slope')).reduceRegion(ee.Reducer.percentile([2,50,98]), r, 300).getInfo()
    h = eth.select(0).reduceRegion(ee.Reducer.percentile([2,50,98]), r, 100).getInfo()
    hist = wc.reduceRegion(ee.Reducer.frequencyHistogram(), r, 100).getInfo()['Map']; tot=sum(hist.values())
    print(nm, {k:round(v,1) for k,v in s.items()}, "h", {k:round(v,1) for k,v in h.items()})
    print("   WC%", {k:round(100*v/tot,1) for k,v in sorted(hist.items(), key=lambda x:-x[1])[:6]})
