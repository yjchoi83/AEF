import sys, time; sys.path.insert(0,'scratch')
from aefkit import *
import ee, pandas as pd, numpy as np
ROIS = {'CD_congo':(23.0,0.0,23.5,0.5,'AF'),'ZM_miombo':(27.0,-13.7,27.5,-13.2,'AF'),
 'BR_para':(-55.5,-6.0,-55.0,-5.5,'SA'),'BO_chiq':(-62.0,-16.5,-61.5,-16.0,'SA'),
 'DE_bav':(11.0,48.5,11.5,49.0,'EU'),'US_mo':(-92.5,37.5,-92.0,38.0,'US')}
YRS=list(range(2019,2026))   # S2 L2A global only from 2018-12
H=ee.Image('UMD/hansen/global_forest_change_2025_v1_13'); DW=ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
def dwmode(y,roi): return DW.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).select('label').reduce(ee.Reducer.mode())
def s2v(y,roi):
    m=s2(y,roi).select(S2_BANDS)
    n=m.multiply(m).reduce(ee.Reducer.sum()).sqrt()
    return m.divide(n)                       # unit-norm S2 feature vector
def s2ang(y1,y2,roi):
    d=s2v(y1,roi).multiply(s2v(y2,roi)).reduce(ee.Reducer.sum())
    return d.clamp(-1,1).acos().multiply(180/np.pi).rename(f's2ang_{y2}')
rows=[]
for nm,(a,b,c,d,grp) in ROIS.items():
    t0=time.time(); roi=ee.Geometry.Rectangle([a,b,c,d])
    dw18,dw24=dwmode(2018,roi),dwmode(2024,roi)
    stab=(H.select('lossyear').unmask(0).eq(0).And(H.select('gain').unmask(0).eq(0))
          .And(H.select('datamask').eq(1)).And(dw18.eq(dw24))
          .And(dw24.neq(0)).And(dw24.neq(6)).And(dw24.neq(8)))
    img=ee.Image(0).rename('dummy')
    for y1,y2 in zip(YRS[:-1],YRS[1:]):
        img=img.addBands(s2ang(y1,y2,roi)).addBands(angle(y1,y2,roi).rename(f'ang_{y2}'))
    img=img.updateMask(stab)
    df=samp(img,roi,n=700,scale=10); df['roi']=nm; df['grp']=grp; rows.append(df)
    print(nm,len(df),round(time.time()-t0,1),flush=True)
pd.concat(rows,ignore_index=True).to_csv('scratch/tb02_p2.csv',index=False); print('done')
