import ee, numpy as np, pandas as pd, json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score, cohen_kappa_score
ee.Initialize(project='alpha-earth-app')
A=[f"A{i:02d}" for i in range(64)]; S=['B2','B3','B4','B8','B11','B12','NDVI','NDWI']
N=['elev','slope','asp_s','asp_c','t2m','prec']
SETS={'i_AEF64':A,'ii_S2':S,'iii_S2+anc':S+N,'iv_AEF+anc':A+N}
def msk(im):
    q=im.select('SCL'); m=q.neq(3).And(q.neq(8)).And(q.neq(9)).And(q.neq(10)).And(q.neq(11))
    return im.updateMask(m).divide(10000)
def feats(roi,Y,lab):
    aef=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi).mosaic()
    s2=(ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',40)).map(msk).select(['B2','B3','B4','B8','B11','B12']).median())
    s2=s2.addBands(s2.normalizedDifference(['B8','B4']).rename('NDVI')).addBands(s2.normalizedDifference(['B3','B8']).rename('NDWI'))
    d=ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").select('DEM').filterBounds(roi).mosaic().setDefaultProjection('EPSG:4326',None,30)
    t=ee.Terrain.products(d.rename('elev')); ap=t.select('aspect').multiply(np.pi/180)
    anc=t.select(['elev','slope']).addBands(ap.sin().rename('asp_s')).addBands(ap.cos().rename('asp_c'))
    e=ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate(f"{Y}-01-01",f"{Y+1}-01-01")
    anc=anc.addBands(e.select('temperature_2m').mean().rename('t2m')).addBands(e.select('total_precipitation_sum').sum().rename('prec'))
    return aef.addBands(s2).addBands(anc).addBands(lab)
def grab(roi,Y,lab,n,seed):
    pts=ee.FeatureCollection.randomPoints(roi,n,seed)
    fc=feats(roi,Y,lab).sampleRegions(collection=pts,scale=10,tileScale=16,geometries=True)
    rows=[]
    for x in fc.getInfo()['features']:
        p=dict(x['properties']); c=x['geometry']['coordinates']; p['lon'],p['lat']=c[0],c[1]; rows.append(p)
    df=pd.DataFrame(rows); df=df.dropna(subset=A+S+N+['lab'])
    df['blk']=(np.floor(df.lon/0.1)*1000+np.floor(df.lat/0.1)).astype(int); return df
def cv(df,fs,k=5):
    X=df[fs].values; y=df['lab'].values; g=df['blk'].values; a=[];kp=[]
    for tr,te in GroupKFold(n_splits=k).split(X,y,g):
        m=RandomForestClassifier(n_estimators=300,min_samples_leaf=2,n_jobs=-1,random_state=0).fit(X[tr],y[tr])
        p=m.predict(X[te]); a.append(accuracy_score(y[te],p)); kp.append(cohen_kappa_score(y[te],p))
    return np.mean(a),np.std(a),np.mean(kp)
res={}
BR=ee.Geometry.Rectangle([-55.4,-12.6,-54.6,-11.8])
mb=ee.Image("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1").select('classification_2023').rename('lab')
d1=None
for n in (4000,2000):
    try:
        d1=grab(BR,2023,mb,n,7); break
    except Exception as ex: print("retry",n,type(ex).__name__,str(ex)[:60])
if d1 is not None:
    vc=d1.lab.value_counts(); d1=d1[d1.lab.isin(vc[vc>=100].index)]
    print("ARM1 MapBiomas2023 n=",len(d1),"classes=",dict(d1.lab.value_counts()),"blocks=",d1.blk.nunique())
    for k_,fs in SETS.items():
        r=cv(d1,fs); res['arm1_'+k_]=list(r); print(f"ARM1 {k_:11s} OA {r[0]:.4f}+-{r[1]:.4f} kappa {r[2]:.4f}")
    d1.to_csv('TE06_arm1.csv',index=False); json.dump(res,open('TE06_res.json','w'))
try:
    wcB=ee.Image(ee.ImageCollection("ESA/WorldCover/v200").filterBounds(BR).first()).select('Map').rename('lab')
    CG=ee.Geometry.Rectangle([23.2,0.2,24.0,1.0])
    wcC=ee.Image(ee.ImageCollection("ESA/WorldCover/v200").filterBounds(CG).first()).select('Map').rename('lab')
    a1=grab(BR,2021,wcB,2500,7); a2=grab(CG,2021,wcC,2500,11)
    com=sorted(set(a1.lab.value_counts()[lambda s:s>=80].index)&set(a2.lab.value_counts()[lambda s:s>=80].index))
    a1=a1[a1.lab.isin(com)]; a2=a2[a2.lab.isin(com)]
    print("ARM2 WorldCover2021 shared",com,"nBR",len(a1),"nCG",len(a2),"balBR",dict(a1.lab.value_counts()),"balCG",dict(a2.lab.value_counts()))
    for k_,fs in SETS.items():
        ino=cv(a1,fs)
        M=RandomForestClassifier(n_estimators=300,min_samples_leaf=2,n_jobs=-1,random_state=0).fit(a1[fs].values,a1.lab.values)
        p=M.predict(a2[fs].values); oa=accuracy_score(a2.lab.values,p)
        res['arm2_'+k_]=[ino[0],ino[1],oa]; print(f"ARM2 {k_:11s} inBR {ino[0]:.4f}+-{ino[1]:.4f} -> CG {oa:.4f} drop {ino[0]-oa:.4f}")
except Exception as ex: print("ARM2 FAILED",type(ex).__name__,str(ex)[:90])
json.dump(res,open('TE06_res.json','w')); print("saved")
