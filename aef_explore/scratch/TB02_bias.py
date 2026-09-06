import sys, time; sys.path.insert(0,'scratch')
from aefkit import *
import ee, pandas as pd, numpy as np
ROIS = {'CD_congo':(23.0,0.0,23.5,0.5),'ZM_miombo':(27.0,-13.7,27.5,-13.2),
        'BR_para':(-55.5,-6.0,-55.0,-5.5),'BO_chiq':(-62.0,-16.5,-61.5,-16.0),
        'DE_bav':(11.0,48.5,11.5,49.0),'US_mo':(-92.5,37.5,-92.0,38.0)}
H = ee.Image('UMD/hansen/global_forest_change_2025_v1_13')
DW = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
TMF = ee.ImageCollection('projects/JRC/TMF/v1_2024/DeforestationYear').first()
def dwmode(y,roi): return DW.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).select('label').reduce(ee.Reducer.mode())
res={}
for nm,(a,b,c,d) in ROIS.items():
    t0=time.time(); roi=ee.Geometry.Rectangle([a,b,c,d])
    dw18,dw24=dwmode(2018,roi),dwmode(2024,roi)
    stab=(H.select('lossyear').unmask(0).eq(0).And(H.select('gain').unmask(0).eq(0))
          .And(H.select('datamask').eq(1)).And(dw18.eq(dw24))
          .And(dw24.neq(0)).And(dw24.neq(6)).And(dw24.neq(8)))
    ly=H.select('lossyear').unmask(0)
    bands=[stab.rename('stab'), H.select('treecover2000').gt(30).rename('fc30')]
    for y in range(2018,2026): bands.append(ly.eq(y-2000).rename(f'hl_{y}'))
    tm=TMF.select([0],['tmf']).unmask(0)
    for y in range(2018,2025): bands.append(tm.eq(y).rename(f'tf_{y}'))
    img=ee.Image.cat(bands)
    r=img.reduceRegion(ee.Reducer.mean(), roi, scale=30, maxPixels=1e9, bestEffort=True).getInfo()
    res[nm]={k:(None if v is None else round(v*100,4)) for k,v in r.items()}
    print(nm, round(time.time()-t0,1),'s', flush=True)
df=pd.DataFrame(res).T
df.to_csv('scratch/TB02_bias.csv')
print(df.to_string())
