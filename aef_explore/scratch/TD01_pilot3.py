import ee, math, numpy as np, pandas as pd
ee.Initialize(project='alpha-earth-app')
Y=2022; roi=ee.Geometry.Rectangle([23.5,0.0,24.5,1.0])   # DRC Tshopo/Kisangani, ~110x110 km
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
aef=lambda y: AEF.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(roi).mosaic()
ac=ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').mosaic()
degy=ee.ImageCollection('projects/JRC/TMF/v1_2024/DegradationYear').mosaic().unmask(0)
defy=ee.ImageCollection('projects/JRC/TMF/v1_2024/DeforestationYear').mosaic().unmask(0)
acY,acP=ac.select(f'Dec{Y}'),ac.select(f'Dec{Y-1}')
hl=ee.Image('UMD/hansen/global_forest_change_2025_v1_13').select('lossyear').unmask(0)
cls=(ee.Image(0).where(acY.eq(1).And(degy.eq(0)).And(defy.eq(0)).And(hl.eq(0)),1)
     .where(acY.eq(6).And(acP.eq(6)).And(degy.eq(0)).And(defy.eq(0)),2)
     .where(degy.eq(Y).And(defy.neq(Y)),3)
     .where(defy.eq(Y).Or(hl.eq(Y-2000)).And(degy.neq(Y)),4)).selfMask().rename('cls').toByte()
pts=cls.stratifiedSample(numPoints=500,classBand='cls',region=roi,scale=30,seed=11,
     classValues=[1,2,3,4],classPoints=[500]*4,geometries=True,dropNulls=True,tileScale=8)
raw=pts.getInfo()['features']; print('n_points',len(raw),flush=True)
feats=[ee.Feature(ee.Geometry.Point(f['geometry']['coordinates']),{'cls':f['properties']['cls']}) for f in raw]
def s2(y):
    b=['B2','B3','B4','B8','B11','B12']
    m=(ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate(f'{y}-01-01',f'{y+1}-01-01')
       .filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',60))
       .map(lambda i:i.updateMask(i.select('QA60').bitwiseAnd(1<<10|1<<11).eq(0)).divide(1e4))
       .select(b).median())
    return m.addBands(m.normalizedDifference(['B8','B4']).rename('NDVI')).addBands(
             m.normalizedDifference(['B8','B12']).rename('NBR'))
def ang(a,b):
    n=lambda x:x.divide(x.pow(2).reduce(ee.Reducer.sum()).sqrt())
    return n(a).multiply(n(b)).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/math.pi)
stack=(aef(Y).addBands(ang(aef(Y-1),aef(Y)).rename('ang_aef'))
       .addBands(s2(Y).rename([f'S{i}' for i in range(8)])).addBands(ang(s2(Y-1),s2(Y)).rename('ang_s2')))
recs=[]
for i in range(0,len(feats),700):
    r=stack.sampleRegions(collection=ee.FeatureCollection(feats[i:i+700]),scale=10,tileScale=8).getInfo()['features']
    recs+= [dict(f['properties']) for f in r]; print('chunk',i,len(r),flush=True)
dc=pd.DataFrame(recs).dropna(); dc.to_csv('TD01_congo.csv',index=False)
NAME={1:'intact',2:'nonforest',3:'degrad',4:'clearing'}
print('CONGO n',len(dc),{NAME[k]:int(v) for k,v in dc.cls.value_counts().items()})
from scipy.stats import spearmanr,kendalltau,mannwhitneyu
auc=lambda a,b: mannwhitneyu(a,b).statistic/(len(a)*len(b))
for col in ['ang_aef','ang_s2']:
    print(col,' | '.join(f"{NAME[k]}: n={len(dc[dc.cls==k])} mean={dc.loc[dc.cls==k,col].mean():.2f} sd={dc.loc[dc.cls==k,col].std():.2f}" for k in sorted(dc.cls.unique())))
    s=dc[dc.cls.isin([1,3,4])]; r=s.cls.map({1:0,3:1,4:2})
    o=f"  rho={spearmanr(r,s[col]).statistic:.3f} tau={kendalltau(r,s[col]).statistic:.3f}"
    if 3 in dc.cls.values and 1 in dc.cls.values: o+=f" AUC(deg>intact)={auc(dc.loc[dc.cls==3,col],dc.loc[dc.cls==1,col]):.3f}"
    if 4 in dc.cls.values and 3 in dc.cls.values: o+=f" AUC(clr>deg)={auc(dc.loc[dc.cls==4,col],dc.loc[dc.cls==3,col]):.3f}"
    print(o)
# transfer: train Amazon -> test Congo
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, balanced_accuracy_score
from sklearn.model_selection import GroupKFold, cross_val_score
da=pd.read_csv('TD01_samples.csv')
A=[f'A{i:02d}' for i in range(64)]; S=[f'S{i}' for i in range(8)]
for nm,c in [('AEF64',A),('S2_8b',S)]:
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=4000,class_weight='balanced')).fit(da[c],da.cls)
    p=m.predict(dc[c])
    print(f'{nm:>7s} AMZ->COD  macroF1={f1_score(dc.cls,p,average="macro"):.3f} balAcc={balanced_accuracy_score(dc.cls,p):.3f}')
    dc['blk']=np.floor(dc.get("longitude",pd.Series(np.zeros(len(dc)))) ).astype(int) if False else 0
print('note: in-region Congo CV omitted (no coords retained); transfer drop vs Amazon in-region reported in card')
