import sys; sys.path.insert(0,'scratch')
from aefkit import *
import pandas as pd, numpy as np
CRS='EPSG:32636'
gaza = ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1') \
        .filter(ee.Filter.stringContains('ADM1_NAME','Gaza')).geometry()
roi = gaza.bounds()
P10 = ee.Projection(CRS).atScale(10)
def unit(img,b):
    return img.select(b).divide(img.select(b).pow(2).reduce(ee.Reducer.sum()).sqrt())
def ang(a,b):
    return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/np.pi)
E={y: aef(y,roi).setDefaultProjection(P10) for y in (2022,2023,2024,2025)}
S={y: unit(s2(y,roi),S2_BANDS).setDefaultProjection(P10) for y in (2022,2024)}
OBT=ee.ImageCollection('GOOGLE/Research/open-buildings-temporal/v1')
def obt(y): return OBT.filterBounds(roi).filterDate(f'{y}-01-01',f'{y+1}-01-01').mosaic() \
    .select('building_fractional_count').setDefaultProjection(P10)
b=[ang(E[2022],E[2023]).rename('aef_2223'), ang(E[2023],E[2024]).rename('aef_2324'),
   ang(E[2022],E[2024]).rename('aef_2224'), ang(E[2024],E[2025]).rename('aef_2425'),
   ang(S[2022],S[2024]).rename('s2_2224'), obt(2022).rename('fc22'), obt(2023).rename('fc23')]
stack = ee.Image.cat(b).reduceResolution(ee.Reducer.mean(), maxPixels=1024) \
          .reproject(crs=CRS, crsTransform=[300,0,0,0,-300,0])
P300 = ee.Projection(CRS).atScale(300)
rows=[]
for i in range(8):
    y0=31.20+i*0.05; strip=ee.Geometry.Rectangle([34.15,y0,34.62,y0+0.05]).intersection(gaza,1)
    try:
        fc=stack.sample(region=strip, projection=P300, factor=1, dropNulls=True, geometries=True)
        for f in fc.getInfo()['features']:
            p=dict(f['properties']); c=f['geometry']['coordinates']
            p['lon'],p['lat']=c[0],c[1]; rows.append(p)
        print('strip',i,'cum',len(rows),flush=True)
    except Exception as ex: print('strip',i,'FAIL',str(ex)[:90],flush=True)
df=pd.DataFrame(rows); df.to_csv('scratch/th03_cells_gee.csv',index=False)
print(df.shape); print(df.describe().round(3).to_string())
