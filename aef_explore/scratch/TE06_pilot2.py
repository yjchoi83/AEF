import ee, numpy as np, pandas as pd, json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score, cohen_kappa_score
ee.Initialize(project='alpha-earth-app'); Y=2021
def s2mask(im):
    scl=im.select('SCL'); m=scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return im.updateMask(m).divide(10000)
def build(roi):
    aef=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi).mosaic()
    s2=(ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',60)).map(s2mask).select(['B2','B3','B4','B8','B11','B12']).median())
    s2=s2.addBands(s2.normalizedDifference(['B8','B4']).rename('NDVI')).addBands(s2.normalizedDifference(['B3','B8']).rename('NDWI'))
    dem=ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").select('DEM').mosaic().rename('elev')
    ter=ee.Terrain.products(dem.setDefaultProjection('EPSG:4326',None,30)); asp=ter.select('aspect').multiply(np.pi/180)
    anc=dem.addBands(ter.select('slope')).addBands(asp.sin().rename('asp_s')).addBands(asp.cos().rename('asp_c'))
    era=ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate(f"{Y}-01-01",f"{Y+1}-01-01")
    anc=anc.addBands(era.select('temperature_2m').mean().rename('t2m')).addBands(era.select('total_precipitation_sum').sum().rename('prec'))
    wc=ee.Image(ee.ImageCollection("ESA/WorldCover/v200").filterBounds(roi).first()).select('Map').rename('lab')
    return aef.addBands(s2).addBands(anc).addBands(wc)
def grab(roi,n,seed):
    s=build(roi).sample(region=roi,scale=10,numPixels=n,seed=seed,geometries=True,dropNulls=True,tileScale=16).randomColumn('r',3)
    rows=[]
    for lo,hi in [(0,.5),(.5,1.01)]:
        for x in s.filter(ee.Filter.And(ee.Filter.gte('r',lo),ee.Filter.lt('r',hi))).getInfo()['features']:
            d=dict(x['properties']); c=x['geometry']['coordinates']; d['lon'],d['lat']=c[0],c[1]; rows.append(d)
    return pd.DataFrame(rows).dropna()
BR=ee.Geometry.Rectangle([-55.6,-12.8,-54.1,-11.3]); CG=ee.Geometry.Rectangle([23.0,0.0,24.5,1.5])
a=grab(BR,4000,7); b=grab(CG,4000,11); print("nBR",len(a),"nCG",len(b))
com=sorted(set(a.lab.value_counts()[lambda s:s>=100].index)&set(b.lab.value_counts()[lambda s:s>=100].index))
a=a[a.lab.isin(com)]; b=b[b.lab.isin(com)]
for d in (a,b): d['blk']=(np.floor(d.lon/0.1)*1000+np.floor(d.lat/0.1)).astype(int)
print("shared classes",com,"nBR",len(a),"nCG",len(b),"balBR",dict(a.lab.value_counts()),"balCG",dict(b.lab.value_counts()))
AEF=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NDWI']; AN=['elev','slope','asp_s','asp_c','t2m','prec']
res={}
for nm,fs in {'i_AEF64':AEF,'ii_S2':S2,'iii_S2+anc':S2+AN,'iv_AEF+anc':AEF+AN}.items():
    ac=[]
    for tr,te in GroupKFold(n_splits=5).split(a[fs].values,a.lab.values,a.blk.values):
        m=RandomForestClassifier(n_estimators=300,min_samples_leaf=2,n_jobs=-1,random_state=0).fit(a[fs].values[tr],a.lab.values[tr])
        ac.append(accuracy_score(a.lab.values[te],m.predict(a[fs].values[te])))
    M=RandomForestClassifier(n_estimators=300,min_samples_leaf=2,n_jobs=-1,random_state=0).fit(a[fs].values,a.lab.values)
    p=M.predict(b[fs].values); tr_oa=accuracy_score(b.lab.values,p); tr_k=cohen_kappa_score(b.lab.values,p)
    res[nm]=[np.mean(ac),np.std(ac),tr_oa,tr_k]
    print(f"{nm:12s} inBR {np.mean(ac):.4f}+-{np.std(ac):.4f} -> CG {tr_oa:.4f} (kappa {tr_k:.4f}) drop {np.mean(ac)-tr_oa:.4f}")
json.dump(res,open('TE06_p2.json','w'))
