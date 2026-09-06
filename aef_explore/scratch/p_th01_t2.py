import sys, numpy as np, pandas as pd
sys.path.insert(0,'/d/yj_projects/workspace_yj/Alphaearth/aef_explore/scratch')
from aefkit import *
SITES={  # name:(lon,lat,radius_m,project_year)
 'Jungphyong_gh_2019':(129.632113,41.557469,800,2019),
 'Ryonpho_gh_2022':(127.535775,39.792279,900,2022),
 'Songhwa_hsg_2022':(125.8008,38.9994,700,2022),
 'Hwasong_hsg_2022_26':(125.7774,39.0965,800,2023)}
YRS=list(range(2018,2026))
dem=ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM").mosaic().rename("elev")
def dw(y,roi):
    return (ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterDate(f"{y}-01-01",f"{y+1}-01-01")
            .filterBounds(roi).select('label').reduce(ee.Reducer.mode()).rename('dw'))
def s2ang(y1,y2,roi):  # baseline: normalized spectral distance of S2 annual medians
    a=s2(y1,roi).select(S2_BANDS[:6]); b=s2(y2,roi).select(S2_BANDS[:6])
    return a.subtract(b).pow(2).reduce(ee.Reducer.sum()).sqrt().rename('s2d')
rows=[]
for nm,(lo,la,R,py) in SITES.items():
    p=ee.Geometry.Point([lo,la]); big=p.buffer(22000); roi=p.buffer(1200)
    img=dem.addBands(dw(2018,big).unmask(99))
    for y in YRS: img=img.addBands(angle(y-1,y,big).rename(f"a{y}"))
    for y in (2019,2022,2024): img=img.addBands(s2ang(y-1,y,big).rename(f"s{y}"))
    sp=ee.FeatureCollection.randomPoints(p.buffer(R),120,seed=7)
    ctl=ee.FeatureCollection.randomPoints(big.difference(p.buffer(6000),1),300,seed=8)
    for tag,fc in [('site',sp),('ctl',ctl)]:
        f=img.sampleRegions(collection=fc,scale=10,geometries=True,tileScale=4).getInfo()['features']
        for r in f:
            d=dict(r['properties']); d['tag']=tag; d['site']=nm; d['py']=py; rows.append(d)
df=pd.DataFrame(rows); df.to_csv('/d/yj_projects/workspace_yj/Alphaearth/aef_explore/scratch/t2_raw.csv',index=False)
for nm,(lo,la,R,py) in SITES.items():
    s=df[(df.site==nm)&(df.tag=='site')]; c=df[(df.site==nm)&(df.tag=='ctl')]
    if not len(s) or not len(c): print(nm,"NO DATA"); continue
    md=s.dw.mode().iat[0]; e0,e1=s.elev.quantile(.05)-80,s.elev.quantile(.95)+80
    cm=c[(c.dw==md)&(c.elev.between(e0,e1))]
    if len(cm)<30: cm=c[c.elev.between(e0,e1)]
    print(f"\n== {nm} (declared {py}) n_site={len(s)} n_ctl_matched={len(cm)}/{len(c)} pre2018DW={int(md)} elev={s.elev.mean():.0f}m")
    det=None; out=[]
    for y in YRS:
        k=f"a{y}"; mu_s=s[k].mean(); mu_c=cm[k].mean(); sd_c=cm[k].std()
        z=(mu_s-mu_c)/sd_c if sd_c>0 else np.nan
        out.append(f"{y}:{mu_s:.1f}/{mu_c:.1f}(z{z:.1f})")
        if det is None and z>=3: det=y
    print("  AEF angle deg site/ctl(z):", " ".join(out)); print("  AEF detection year:",det)
    o2=[]
    for y in (2019,2022,2024):
        k=f"s{y}"
        if k not in s: continue
        mu_s=s[k].mean(); mu_c=cm[k].mean(); sd_c=cm[k].std()
        o2.append(f"{y}:z{(mu_s-mu_c)/sd_c:.1f}" if sd_c>0 else f"{y}:na")
    print("  S2-composite dist z:", " ".join(o2))
