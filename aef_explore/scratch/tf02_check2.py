import sys; sys.path.insert(0,'scratch')
from aefkit import *
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map')
rois = {'MT_cerrado_frontier': [-53.5,-15.5,-52.3,-14.3], 'MT_sinop': [-55.6,-12.6,-54.4,-11.4]}
for k,b in rois.items():
    r = ee.Geometry.Rectangle(b)
    h = wc.reduceRegion(ee.Reducer.frequencyHistogram(), r, scale=100, maxPixels=1e9).getInfo()['Map']
    tot = sum(h.values())
    print(k, {c: round(100*v/tot,1) for c,v in sorted(h.items(), key=lambda x:-x[1])[:6]})
