import ee, numpy as np, pandas as pd, sys, json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import accuracy_score, cohen_kappa_score
ee.Initialize(project='alpha-earth-app')
Y=2023; roi=ee.Geometry.Rectangle([-55.6,-12.8,-54.1,-11.3])   # Mato Grosso, Amazon/Cerrado transition ~220km
aef=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi).mosaic()
def s2mask(im):
    scl=im.select('SCL'); m=scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11))
    return im.updateMask(m).divide(10000)
s2=(ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f"{Y}-01-01",f"{Y+1}-01-01")
    .filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',60)).map(s2mask)
    .select(['B2','B3','B4','B8','B11','B12']).median())
s2=s2.addBands(s2.normalizedDifference(['B8','B4']).rename('NDVI')).addBands(s2.normalizedDifference(['B3','B8']).rename('NDWI'))
dem=ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").select('DEM').mosaic().rename('elev')
ter=ee.Terrain.products(dem.setDefaultProjection('EPSG:4326',None,30))
asp=ter.select('aspect').multiply(np.pi/180)
anc=(dem.addBands(ter.select('slope')).addBands(asp.sin().rename('asp_s')).addBands(asp.cos().rename('asp_c')))
era=ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate(f"{Y}-01-01",f"{Y+1}-01-01")
anc=anc.addBands(era.select('temperature_2m').mean().rename('t2m')).addBands(era.select('total_precipitation_sum').sum().rename('prec'))
mb=ee.Image("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1").select(f'classification_{Y}').rename('lab')
stack=aef.addBands(s2).addBands(anc).addBands(mb)
samp=stack.sample(region=roi,scale=10,numPixels=6000,seed=7,geometries=True,dropNulls=True,tileScale=16).randomColumn('r',3)
rows=[]
for lo,hi in [(0,.34),(.34,.67),(.67,1.01)]:
    f=samp.filter(ee.Filter.And(ee.Filter.gte('r',lo),ee.Filter.lt('r',hi))).getInfo()['features']
    for x in f:
        d=dict(x['properties']); c=x['geometry']['coordinates']; d['lon'],d['lat']=c[0],c[1]; rows.append(d)
df=pd.DataFrame(rows).dropna(); print("n_raw",len(df))
vc=df['lab'].value_counts(); keep=vc[vc>=120].index; df=df[df['lab'].isin(keep)]
df['blk']=(np.floor(df.lon/0.1)*1000+np.floor(df.lat/0.1)).astype(int)
AEF=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NDWI']
AN=['elev','slope','asp_s','asp_c','t2m','prec']
sets={'i_AEF64':AEF,'ii_S2':S2,'iii_S2+anc':S2+AN,'iv_AEF+anc':AEF+AN}
print("n",len(df),"classes",dict(df['lab'].value_counts()),"blocks",df.blk.nunique())
out={}
for name,fs in sets.items():
    X=df[fs].values; y=df['lab'].values; g=df['blk'].values; a=[];k=[]
    for tr,te in GroupKFold(n_splits=5).split(X,y,g):
        m=RandomForestClassifier(n_estimators=300,min_samples_leaf=2,n_jobs=-1,random_state=0).fit(X[tr],y[tr])
        p=m.predict(X[te]); a.append(accuracy_score(y[te],p)); k.append(cohen_kappa_score(y[te],p))
    out[name]=(np.mean(a),np.std(a),np.mean(k),np.std(k))
    print(f"{name:12s} OA {np.mean(a):.4f}+-{np.std(a):.4f}  kappa {np.mean(k):.4f}+-{np.std(k):.4f}")
df.to_csv('TE06_indomain.csv',index=False); json.dump({k:list(v) for k,v in out.items()},open('TE06_p1.json','w'))
