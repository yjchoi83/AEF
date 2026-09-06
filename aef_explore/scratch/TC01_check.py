import sys; sys.path.insert(0,'scratch')
from aefkit import *
BR = ee.Geometry.Rectangle([-55.6,-6.0,-54.6,-5.0])
CG = ee.Geometry.Rectangle([21.0,-5.0,22.0,-4.0])
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map')
for nm, roi in [('BR',BR),('CG',CG)]:
    h = wc.reduceRegion(ee.Reducer.frequencyHistogram(), roi, scale=100, maxPixels=1e9).getInfo()['Map']
    tot = sum(h.values())
    print(nm, {k: round(100*v/tot,1) for k,v in sorted(h.items(), key=lambda x:-x[1])})
    print(nm, 'AEF2021 bands', len(aef(2021,roi).bandNames().getInfo()))
dem = ee.ImageCollection("COPERNICUS/DEM/GLO30").mosaic().select('DEM').setDefaultProjection('EPSG:4326',None,30)
era = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate('2021-01-01','2022-01-01')
t = era.select('temperature_2m').mean(); p = era.select('total_precipitation_sum').sum()
for nm, roi in [('BR',BR),('CG',CG)]:
    print(nm, 'dem/t/p', dem.addBands(t).addBands(p).reduceRegion(ee.Reducer.mean(), roi, 300, maxPixels=1e9).getInfo())
