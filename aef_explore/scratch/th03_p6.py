import sys; sys.path.insert(0,'scratch')
from aefkit import *
import pandas as pd, numpy as np
CRS='EPSG:32636'; P10=ee.Projection(CRS).atScale(10); P300=ee.Projection(CRS).atScale(300)
CT=[300,0,0,0,-300,0]
gaza=ee.FeatureCollection('FAO/GAUL_SIMPLIFIED_500m/2015/level1')\
      .filter(ee.Filter.eq('ADM0_NAME','Gaza Strip')).geometry(); roi=gaza.bounds()
def unit(i,b): return i.select(b).divide(i.select(b).pow(2).reduce(ee.Reducer.sum()).sqrt())
def ang(a,b): return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/np.pi)
def agg(img,mp=1024): return img.reduceResolution(ee.Reducer.mean(),maxPixels=mp).reproject(crs=CRS,crsTransform=CT)
E={y:aef(y,roi).setDefaultProjection(P10) for y in (2022,2023,2024,2025)}
ghs=ee.ImageCollection('JRC/GHSL/P2023A/GHS_BUILT_S').filterDate('2020-01-01','2021-01-01').first()\
      .select(0).setDefaultProjection(ee.Projection(CRS).atScale(100))
A=agg(ee.Image.cat([ang(E[2022],E[2023]).rename('aef_2223'),ang(E[2023],E[2024]).rename('aef_2324'),
     ang(E[2022],E[2024]).rename('aef_2224'),ang(E[2024],E[2025]).rename('aef_2425')]))\
   .addBands(agg(ghs,64).rename('bs'))
S={y:unit(s2(y,roi),S2_BANDS).setDefaultProjection(P10) for y in (2022,2024)}
B=agg(ang(S[2022],S[2024]).rename('s2_2224'))
def grab(st,box):
    fc=st.sample(region=box,projection=P300,factor=1,dropNulls=False,geometries=True); o=[]
    for f in fc.getInfo()['features']:
        p=dict(f['properties']); c=f['geometry']['coordinates']
        p['lon'],p['lat']=round(c[0],6),round(c[1],6); o.append(p)
    return o
def sweep(st,tag,nlat,nlon):
    rows=[]; dy=0.40/nlat; dx=0.40/nlon
    for i in range(nlat):
        for j in range(nlon):
            y0=31.20+i*dy; x0=34.20+j*dx
            try: rows+=grab(st,ee.Geometry.Rectangle([x0,y0,x0+dx,y0+dy]).intersection(gaza,10))
            except Exception as ex:
                for k in range(4):
                    bb=ee.Geometry.Rectangle([x0+(k%2)*dx/2,y0+(k//2)*dy/2,x0+(k%2+1)*dx/2,y0+(k//2+1)*dy/2]).intersection(gaza,10)
                    try: rows+=grab(st,bb)
                    except Exception as e2: print(tag,i,j,k,'FAIL',str(e2)[:50],flush=True)
        print(tag,'lat',i,'cum',len(rows),flush=True); pd.DataFrame(rows).to_csv('scratch/th03_%s_part.csv'%tag,index=False)
    return pd.DataFrame(rows).drop_duplicates(subset=['lon','lat'])
da=sweep(A,'AEF',10,4); da.to_csv('scratch/th03_aef.csv',index=False); print('AEF',da.shape,flush=True)
db=sweep(B,'S2',10,4);  db.to_csv('scratch/th03_s2.csv',index=False);  print('S2',db.shape,flush=True)
df=da.merge(db,on=['lon','lat'],how='inner'); df.to_csv('scratch/th03_cells_gee.csv',index=False)
print('MERGED',df.shape,flush=True); print(df.describe().round(3).to_string(),flush=True)
