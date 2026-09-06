import ee, numpy as np, pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
ee.Initialize(project='alpha-earth-app')
Y=2022; roi=ee.Geometry.Rectangle([-55.5,-7.0,-53.0,-4.5])
AGE=ee.Image("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1").select(f"secondary_vegetation_age_{Y}")
age=AGE.updateMask(AGE.gte(1).And(AGE.lte(35)))          # >=36 right-censored (1986 record start) -> excluded
BINS=[(1,3),(4,6),(7,10),(11,15),(16,25),(26,35)]
strat=ee.Image(0)
for i,(lo,hi) in enumerate(BINS): strat=strat.where(age.gte(lo).And(age.lte(hi)), i+1)
strat=strat.updateMask(strat.gt(0)).rename('strat').toInt()
pts=strat.addBands(age.rename('age')).stratifiedSample(numPoints=800,classBand='strat',region=roi,scale=30,seed=7,geometries=True,dropNulls=True)
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
def aef(y): return AEF.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(roi).mosaic()
def s2(y):
    def m(im):
        s=im.select('SCL'); k=s.neq(3).And(s.neq(8)).And(s.neq(9)).And(s.neq(10)).And(s.neq(11))
        return im.updateMask(k).divide(10000)
    c=ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',60)).map(m)
    med=c.select(['B2','B3','B4','B8','B11','B12']).median()
    return med.addBands(med.normalizedDifference(['B8','B4']).rename('NDVI')).addBands(med.normalizedDifference(['B8','B12']).rename('NBR'))
A=[f"A{i:02d}" for i in range(64)]; S2B=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
LL=ee.Image.pixelLonLat().rename(['lon','lat'])
stackA=aef(Y).rename(A).addBands(s2(Y).select(S2B)).addBands(LL)
stackB=aef(2017).rename([a+'_17' for a in A]).addBands(LL.select('lon').rename('lon2'))
def fetch(stack, tag):
    out=[]
    for i in range(1,len(BINS)+1):
        sub=pts.filter(ee.Filter.eq('strat',i))
        fc=stack.sampleRegions(collection=sub, scale=10, tileScale=8, geometries=False)
        out += [f['properties'] for f in fc.getInfo()['features']]
        print(tag,"bin",i,"n",len(out),flush=True)
    return pd.DataFrame(out)
dfA=fetch(stackA,'A'); dfB=fetch(stackB,'B')
key=['age','strat']
df=pd.concat([dfA.reset_index(drop=True), dfB.reset_index(drop=True)[[a+'_17' for a in A]]],axis=1).dropna()
assert (dfA.age.reset_index(drop=True)==dfB.age.reset_index(drop=True)).all(), "row misalign"
df['blk']=np.floor(df.lon/0.1).astype(int).astype(str)+"_"+np.floor(df.lat/0.1).astype(int).astype(str)
df['bin']=df.age.apply(lambda a: next(f"{lo}-{hi}" for lo,hi in BINS if lo<=a<=hi))
print("N",len(df),"blocks",df.blk.nunique(),"bins",df['bin'].value_counts().to_dict(),flush=True)
y=df.age.values.astype(float); g=df.blk.values
def run(cols,name,model='ridge'):
    X=StandardScaler().fit_transform(df[cols].values.astype(float)); oof=np.full(len(y),np.nan); fm=[]
    for tr,te in GroupKFold(n_splits=5).split(X,y,g):
        m=RidgeCV(alphas=np.logspace(-2,4,13)) if model=='ridge' else HistGradientBoostingRegressor(max_iter=300,random_state=0)
        m.fit(X[tr],y[tr]); p=m.predict(X[te]); oof[te]=p
        fm.append((1-((y[te]-p)**2).sum()/((y[te]-y[te].mean())**2).sum(), np.sqrt(((y[te]-p)**2).mean())))
    r2=1-((y-oof)**2).sum()/((y-y.mean())**2).sum()
    print(f"{name:10s} {model:6s} R2={r2:.3f} RMSE={np.sqrt(((y-oof)**2).mean()):.2f} MAE={np.abs(y-oof).mean():.2f} foldR2=[{','.join(f'{f[0]:.2f}' for f in fm)}] foldRMSE=[{','.join(f'{f[1]:.1f}' for f in fm)}]",flush=True)
    return oof
res={}
res['AEF22']=run(A,'AEF22'); res['S2_22']=run(S2B,'S2_22'); res['AEF22+17']=run(A+[a+'_17' for a in A],'AEF22+17')
res['AEF22g']=run(A,'AEF22','gbt'); res['S2g']=run(S2B,'S2_22','gbt')
for nm in ['AEF22','S2_22','AEF22g']:
    o=res[nm]; print(nm+" per-bin | "+" | ".join(f"{lo}-{hi}: pred={o[df['bin'].values==f'{lo}-{hi}'].mean():.1f} res={(o-y)[df['bin'].values==f'{lo}-{hi}'].mean():+.1f} n={(df['bin']==f'{lo}-{hi}').sum()}" for lo,hi in BINS),flush=True)
