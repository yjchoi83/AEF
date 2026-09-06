import sys; sys.path.insert(0,'scratch')
from aefkit import *
R = {'BR_arc':[-55.5,-9.0,-54.5,-8.0], 'BR_sinop':[-55.6,-12.2,-54.6,-11.2],
     'CG_kasai':[21.0,-5.0,22.0,-4.0], 'CG_tshopo':[24.0,0.3,25.0,1.3]}
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map')
dw = (ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterDate('2021-01-01','2022-01-01')
      .select('label').reduce(ee.Reducer.mode()).rename('dw'))
for nm, b in R.items():
    roi = ee.Geometry.Rectangle(b)
    h1 = wc.reduceRegion(ee.Reducer.frequencyHistogram(), roi, 100, maxPixels=1e9).getInfo()['Map']
    h2 = dw.reduceRegion(ee.Reducer.frequencyHistogram(), roi, 100, maxPixels=1e9).getInfo()['dw']
    t1, t2 = sum(h1.values()), sum(h2.values())
    print(nm, 'WC', {k: round(100*v/t1,1) for k,v in h1.items() if v/t1 > 0.005})
    print(nm, 'DW', {k: round(100*v/t2,1) for k,v in h2.items() if v/t2 > 0.005})
