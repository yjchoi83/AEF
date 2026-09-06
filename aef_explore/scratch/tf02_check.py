import sys; sys.path.insert(0,'scratch')
from aefkit import *
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map')
rois = {'MT_largefield': [-54.0,-13.5,-52.8,-12.3], 'KE_smallholder': [34.2,0.0,35.4,1.2]}
for k,b in rois.items():
    r = ee.Geometry.Rectangle(b)
    h = wc.reduceRegion(ee.Reducer.frequencyHistogram(), r, scale=100, maxPixels=1e9).getInfo()['Map']
    tot = sum(h.values())
    print(k, 'px100m=%d'%tot, {c: round(100*v/tot,1) for c,v in sorted(h.items(), key=lambda x:-x[1])[:7]})
    print('  AEF2021 imgs:', aef(2021,r).bandNames().size().getInfo(),
          'S2 imgs:', ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate('2021-01-01','2022-01-01').filterBounds(r).size().getInfo())
