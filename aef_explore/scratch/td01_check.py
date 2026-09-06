import sys; sys.path.insert(0,'scratch')
from aefkit import *
roi = ee.Geometry.Rectangle([-55.6,-6.2,-54.9,-5.5])   # Para, ~77x77 km
ac = ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').filterBounds(roi).mosaic()
print('AC bands tail:', ac.bandNames().getInfo()[-6:])
dy = ee.ImageCollection('projects/JRC/TMF/v1_2022/DegradationYear').filterBounds(roi).mosaic().select(0)
print('DEGYEAR band:', dy.bandNames().getInfo())
for y in [2019,2021,2022]:
    h = ac.select(f'Dec{y}').reduceRegion(ee.Reducer.frequencyHistogram(), roi, 90,
        maxPixels=1e9, bestEffort=True).getInfo()
    print(y, {k:int(v) for k,v in list(h.values())[0].items()})
h2 = dy.updateMask(dy.gt(0)).reduceRegion(ee.Reducer.frequencyHistogram(), roi, 90,
     maxPixels=1e9, bestEffort=True).getInfo()
print('degyear hist:', {k:int(v) for k,v in sorted(list(h2.values())[0].items()) if int(v)>50})
g = ee.ImageCollection('LARSE/GEDI/GEDI02_A_002_MONTHLY').filterBounds(roi).filterDate('2019-01-01','2023-01-01')
print('GEDI imgs:', g.size().getInfo(), 'bands has rh98:', 'rh98' in g.first().bandNames().getInfo())
