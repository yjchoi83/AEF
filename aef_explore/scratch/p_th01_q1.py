# Q1: DPRK hillslope forest vs cropland, 2018 vs 2024, ROK-trained AEF probe + DW cross-check
import sys, numpy as np, pandas as pd
sys.path.insert(0,'/d/yj_projects/workspace_yj/Alphaearth/aef_explore/scratch')
from aefkit import *
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
ROK=ee.Geometry.Rectangle([127.0,37.35,128.4,38.05]); DPR=ee.Geometry.Rectangle([126.2,38.45,127.6,39.35])
dem=ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM").mosaic().rename("elev")
slp=ee.Terrain.slope(dem.setDefaultProjection('EPSG:4326',None,30)).rename('slope')
def dwl(y,roi):
    d=(ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterDate(f"{y}-01-01",f"{y+1}-01-01")
       .filterBounds(roi).select('label').reduce(ee.Reducer.mode()).rename('dw'))
    return d.remap([0,1,2,3,4,5,6,7,8],[0,1,4,5,2,4,3,4,0])
tr=samp(aef(2024,ROK).addBands(dwl(2024,ROK).unmask(99).rename('y')),ROK,n=3000,seed=11)
tr=tr[tr.y!=99]
m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')).fit(tr[AEF_BANDS].values,tr.y.values)
print("train ROK n=%d prior=%s"%(len(tr),dict(tr.y.value_counts(normalize=True).round(3))))
img=(aef(2018,DPR).rename([b+'_18' for b in AEF_BANDS]).addBands(aef(2024,DPR))
     .addBands(dwl(2018,DPR).unmask(99).rename('dw18')).addBands(dwl(2024,DPR).unmask(99).rename('dw24'))
     .addBands(dem).addBands(slp))
d=samp(img,DPR,n=5000,seed=12); d=d[(d.dw18!=99)&(d.dw24!=99)]
p18=m.predict(d[[b+'_18' for b in AEF_BANDS]].values); p24=m.predict(d[AEF_BANDS].values)
d['p18'],d['p24']=p18,p24
NM={0:'water',1:'forest',2:'crop',3:'built',4:'grass/bare',5:'wetland'}
for lo,hi in [(0,5),(5,10),(10,20),(20,90)]:
    s=d[(d.slope>=lo)&(d.slope<hi)]
    if len(s)<80: continue
    f=lambda c,y: (s[c]==y).mean()*100
    print(f"slope {lo}-{hi} n={len(s)} | AEFprobe forest {f('p18',1):.1f}->{f('p24',1):.1f} crop {f('p18',2):.1f}->{f('p24',2):.1f}"
          f" | DW forest {f('dw18',1):.1f}->{f('dw24',1):.1f} crop {f('dw18',2):.1f}->{f('dw24',2):.1f}")
print("agreement probe-vs-DW 2024 overall: %.3f"%(d.p24==d.dw24).mean())
