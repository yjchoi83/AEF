import sys; sys.path.insert(0,'scratch')
from aefkit import *
import pandas as pd, numpy as np
CRS='EPSG:32636'; P10=ee.Projection(CRS).atScale(10); P300=ee.Projection(CRS).atScale(300)
gaza=ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1')\
      .filter(ee.Filter.eq('ADM0_NAME','Gaza Strip')).geometry()
roi=gaza.bounds()
def unit(i,b): return i.select(b).divide(i.select(b).pow(2).reduce(ee.Reducer.sum()).sqrt())
def ang(a,b): return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/np.pi)
E={y:aef(y,roi).setDefaultProjection(P10) for y in (2022,2023,2024,2025)}
S={y:unit(s2(y,roi),S2_BANDS).setDefaultProjection(P10) for y in (2022,2024)}
ghs=ee.ImageCollection('JRC/GHSL/P2023A/GHS_BUILT_S').filterDate('2020-01-01','2021-01-01')\
      .first().select(0).setDefaultProjection(ee.Projection(CRS).atScale(100))
b=[ang(E[2022],E[2023]).rename('aef_2223'),ang(E[2023],E[2024]).rename('aef_2324'),
   ang(E[2022],E[2024]).rename('aef_2224'),ang(E[2024],E[2025]).rename('aef_2425'),
   ang(S[2022],S[2024]).rename('s2_2224')]
st=ee.Image.cat(b).reduceResolution(ee.Reducer.mean(),maxPixels=1024)\
     .reproject(crs=CRS,crsTransform=[300,0,0,0,-300,0])
st=st.addBands(ghs.reduceResolution(ee.Reducer.mean(),maxPixels=64)
     .reproject(crs=CRS,crsTransform=[300,0,0,0,-300,0]).rename('bs'))
rows=[]
for i in range(9):
    y0=31.20+i*0.05; box=ee.Geometry.Rectangle([34.20,y0,34.60,y0+0.05])
    try:
        fc=st.sample(region=box,projection=P300,factor=1,dropNulls=False,geometries=True)
        for f in fc.getInfo()['features']:
            p=dict(f['properties']); c=f['geometry']['coordinates']
            p['lon'],p['lat']=c[0],c[1]; rows.append(p)
        print('strip',i,'cum',len(rows),flush=True)
    except Exception as ex: print('strip',i,'FAIL',str(ex)[:70],flush=True)
df=pd.DataFrame(rows).drop_duplicates(subset=['lon','lat'])
df.to_csv('scratch/th03_cells_gee.csv',index=False)
print(df.shape,flush=True); print(df.describe().round(3).to_string(),flush=True)
