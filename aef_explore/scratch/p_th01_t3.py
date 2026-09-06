import sys, numpy as np, pandas as pd
sys.path.insert(0,'/d/yj_projects/workspace_yj/Alphaearth/aef_explore/scratch')
from aefkit import *
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import GroupKFold
Y=2024
ROK=ee.Geometry.Rectangle([127.0,37.35,128.4,38.05])   # Gyeonggi/Gangwon N (south of DMZ)
DPR=ee.Geometry.Rectangle([127.0,38.45,128.4,39.15])   # Kangwon/N.Hwanghae (north of DMZ)
dem=ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM").mosaic().rename("elev")
slope=ee.Terrain.slope(dem.setDefaultProjection('EPSG:4326',None,30)).rename('slope')
# DW annual mode -> harmonised 6 classes
def lab(roi):
    dw=(ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterDate(f"{Y}-01-01",f"{Y+1}-01-01")
        .filterBounds(roi).select('label').reduce(ee.Reducer.mode()).rename('dw'))
    # DW: 0 water 1 trees 2 grass 3 flooded_veg 4 crops 5 shrub 6 built 7 bare 8 snow
    return dw.remap([0,1,2,3,4,5,6,7,8],[0,1,4,5,2,4,3,4,0]).rename('y')  # 0 water 1 forest 2 crop 3 built 4 grass/bare 5 wetland
def grab(roi,seed):
    img=aef(Y,roi).addBands(s2(Y,roi)).addBands(lab(roi).unmask(99)).addBands(dem).addBands(slope)
    d=samp(img,roi,n=4000,seed=seed); d=d[d.y!=99].copy(); return d
r=grab(ROK,1); n=grab(DPR,2)
for d in (r,n): d['blk']=blocks(d,0.1)
print("ROK n=%d prior=%s"%(len(r),dict(r.y.value_counts(normalize=True).round(3))))
print("DPR n=%d prior=%s"%(len(n),dict(n.y.value_counts(normalize=True).round(3))))
def infold(d,f):
    g=d.blk.values; X=d[f].values; y=d.y.values; sc=[]
    for tr,te in GroupKFold(n_splits=5).split(X,y,g):
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')).fit(X[tr],y[tr])
        sc.append(balanced_accuracy_score(y[te],m.predict(X[te])))
    return np.mean(sc),np.std(sc),[round(s,3) for s in sc]
def xfer(f):
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')).fit(r[f].values,r.y.values)
    p=m.predict(n[f].values)
    agree=balanced_accuracy_score(n.y.values,p)
    ov=(p==n.y.values).mean()
    pri_p=pd.Series(p).value_counts(normalize=True); pri_t=n.y.value_counts(normalize=True)
    k=sorted(set(pri_p.index)|set(pri_t.index))
    a=np.array([pri_p.get(i,1e-9) for i in k]); b=np.array([pri_t.get(i,1e-9) for i in k])
    tv=0.5*np.abs(a-b).sum()
    return agree,ov,tv
for nm,f in [("AEF64",AEF_BANDS),("S2comp",S2_BANDS)]:
    mu,sd,fo=infold(r,f); ag,ov,tv=xfer(f)
    print(f"{nm}: ROK in-fold balacc={mu:.3f} sd={sd:.3f} folds={fo} | cross-DMZ balacc-vs-DW={ag:.3f} overall={ov:.3f} priorTV={tv:.3f} | drop={mu-ag:.3f}")
# domain shift: elevation-stratified mean-embedding cos sim + linear MMD
bins=[0,100,300,600,3000]
for lo,hi in zip(bins[:-1],bins[1:]):
    a=r[(r.elev>=lo)&(r.elev<hi)]; b=n[(n.elev>=lo)&(n.elev<hi)]
    if len(a)<40 or len(b)<40: continue
    ma=a[AEF_BANDS].values.mean(0); mb=b[AEF_BANDS].values.mean(0)
    cs=ma@mb/(np.linalg.norm(ma)*np.linalg.norm(mb)); mmd=np.linalg.norm(ma-mb)
    sa=r[S2_BANDS].values.std(0)
    ma2=a[S2_BANDS].values.mean(0)/sa; mb2=b[S2_BANDS].values.mean(0)/sa
    print(f"elev {lo}-{hi}m nROK={len(a)} nDPR={len(b)} AEFcos={cs:.4f} AEF_MMD={mmd:.4f} S2_MMDz={np.linalg.norm(ma2-mb2):.3f}")
