import sys; sys.path.insert(0,'scratch')
from aefkit import *
import pandas as pd, numpy as np
gaza = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1') \
        .filter(ee.Filter.stringContains('ADM1_NAME','Gaza')).geometry()
print('gaza area km2', round(gaza.area(1).getInfo()/1e6,1))
roi = gaza.bounds()
CRS='EPSG:32636'
def unit(img, bands):
    n = img.select(bands).pow(2).reduce(ee.Reducer.sum()).sqrt()
    return img.select(bands).divide(n)
def ang(a,b):
    d = a.multiply(b).reduce(ee.Reducer.sum())
    return d.clamp(-1,1).acos().multiply(180/np.pi)
E={y: aef(y,roi).reproject(crs=CRS,scale=10) for y in (2022,2023,2024,2025)}
S={y: unit(s2(y,roi),S2_BANDS).reproject(crs=CRS,scale=10) for y in (2022,2024)}
bands=[]
for (a,b,nm) in [(2022,2023,'a2223'),(2023,2024,'a2324'),(2022,2024,'a2224'),(2024,2025,'a2425')]:
    bands.append(ang(E[a],E[b]).rename('aef_'+nm))
bands.append(ang(S[2022],S[2024]).rename('s2_a2224'))
OBT=ee.ImageCollection('GOOGLE/Research/open-buildings-temporal/v1')
def obt(y):
    return OBT.filterBounds(roi).filterDate(f'{y}-01-01',f'{y+1}-01-01').mosaic() \
              .select('building_fractional_count').reproject(crs=CRS,scale=4)
bands += [obt(2022).rename('fc22'), obt(2023).rename('fc23')]
stack = ee.Image.cat(bands).reduceResolution(ee.Reducer.mean(), maxPixels=6000) \
          .reproject(crs=CRS, crsTransform=[300,0,0,0,-300,0])
fc = stack.sample(region=gaza, projection=ee.Projection(CRS).atScale(300),
                  factor=1, dropNulls=True, geometries=True)
print('n cells', fc.size().getInfo())
rows=[]
info=fc.getInfo()['features']
for f in info:
    p=dict(f['properties']); c=f['geometry']['coordinates']
    p['lon'],p['lat']=c[0],c[1]; rows.append(p)
df=pd.DataFrame(rows); df.to_csv('scratch/th03_cells_gee.csv',index=False)
print(df.shape); print(df.describe().round(3).to_string())
