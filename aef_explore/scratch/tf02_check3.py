import sys; sys.path.insert(0,'scratch')
from aefkit import *
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map')
cands = {'KE_a':[34.70,0.55,34.74,0.59],'KE_b':[34.90,0.30,34.94,0.34],
         'MT_a':[-55.10,-12.10,-55.06,-12.06],'MT_b':[-55.30,-11.80,-55.26,-11.76],
         'MT_c':[-54.90,-11.95,-54.86,-11.91]}
for k,b in cands.items():
    r = ee.Geometry.Rectangle(b)
    h = wc.reduceRegion(ee.Reducer.frequencyHistogram(), r, scale=20, maxPixels=1e9).getInfo()['Map']
    t = sum(h.values())
    print(k, {c: round(100*v/t,1) for c,v in sorted(h.items(), key=lambda x:-x[1])[:5]})
