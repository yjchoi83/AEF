import ee, math, numpy as np, pandas as pd
ee.Initialize(project='alpha-earth-app')
Y=2022; roi=ee.Geometry.Rectangle([-55.4,-6.2,-54.6,-5.4])   # Para arc-of-deforestation, ~88x88 km
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
aef=lambda y: AEF.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(roi).mosaic()
ac=ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').mosaic()
degy=ee.ImageCollection('projects/JRC/TMF/v1_2024/DegradationYear').mosaic().unmask(0)
defy=ee.ImageCollection('projects/JRC/TMF/v1_2024/DeforestationYear').mosaic().unmask(0)
acY,acP=ac.select(f'Dec{Y}'),ac.select(f'Dec{Y-1}')
hl=ee.Image('UMD/hansen/global_forest_change_2025_v1_13').select('lossyear').unmask(0)
intact=acY.eq(1).And(degy.eq(0)).And(defy.eq(0)).And(hl.eq(0))
nonf  =acY.eq(6).And(acP.eq(6)).And(degy.eq(0)).And(defy.eq(0))
deg   =degy.eq(Y).And(defy.neq(Y))
clr   =defy.eq(Y).Or(hl.eq(Y-2000)).And(degy.neq(Y))
cls=ee.Image(0).where(intact,1).where(nonf,2).where(deg,3).where(clr,4).selfMask().rename('cls').toByte()
pts=cls.stratifiedSample(numPoints=900,classBand='cls',region=roi,scale=30,seed=7,
     classValues=[1,2,3,4],classPoints=[900,900,900,900],geometries=True,dropNulls=True,tileScale=8)
raw=pts.getInfo()['features']; print('n_points',len(raw))
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
e0,e1=aef(Y-1),aef(Y); s0,s1=s2(Y-1),s2(Y)
stack=(e1.addBands(ang(e0,e1).rename('ang_aef'))
        .addBands(s1.rename([f'S{i}' for i in range(8)]))
        .addBands(ang(s0,s1).rename('ang_s2')))
recs=[]
for i in range(0,len(feats),900):
    fc=ee.FeatureCollection(feats[i:i+900])
    r=stack.sampleRegions(collection=fc,scale=10,geometries=True,tileScale=8).getInfo()['features']
    for f in r:
        p=dict(f['properties']); lon,lat=f['geometry']['coordinates']
        p['blk']=f"{math.floor(lon/0.1)}_{math.floor(lat/0.1)}"; recs.append(p)
    print('chunk',i,len(r),flush=True)
df=pd.DataFrame(recs).dropna(); df.to_csv('TD01_samples.csv',index=False)
NAME={1:'intact',2:'nonforest',3:'degrad',4:'clearing'}
print('n_final',len(df),'balance',{NAME[k]:int(v) for k,v in df.cls.value_counts().items()},'blocks',df.blk.nunique())
from scipy.stats import spearmanr,kendalltau,mannwhitneyu
auc=lambda a,b: mannwhitneyu(a,b).statistic/(len(a)*len(b))
for col in ['ang_aef','ang_s2']:
    print(col, ' | '.join(f"{NAME[k]}: n={len(df[df.cls==k])} mean={df.loc[df.cls==k,col].mean():.2f} sd={df.loc[df.cls==k,col].std():.2f} med={df.loc[df.cls==k,col].median():.2f}" for k in [1,3,4,2]))
    s=df[df.cls.isin([1,3,4])]; r=s.cls.map({1:0,3:1,4:2})
    print(f"  rho={spearmanr(r,s[col]).statistic:.3f} tau={kendalltau(r,s[col]).statistic:.3f}"
          f" AUC(deg>intact)={auc(df.loc[df.cls==3,col],df.loc[df.cls==1,col]):.3f}"
          f" AUC(clr>deg)={auc(df.loc[df.cls==4,col],df.loc[df.cls==3,col]):.3f}")
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold, cross_val_score
A=[f'A{i:02d}' for i in range(64)]; S=[f'S{i}' for i in range(8)]
FE={'AEF64':A,'AEF64+ang':A+['ang_aef'],'S2_8b':S,'S2_8b+ang':S+['ang_s2']}
for nm,c in FE.items():
    for m,t in [(LogisticRegression(max_iter=4000,class_weight='balanced'),'linprobe'),(KNeighborsClassifier(15),'kNN15')]:
        for sc_n in ['f1_macro','balanced_accuracy']:
            sv=cross_val_score(make_pipeline(StandardScaler(),m),df[c].values,df.cls.values,
                 groups=df.blk.values,cv=GroupKFold(n_splits=5),scoring=sc_n)
            print(f'{nm:>10s} {t:>8s} {sc_n:>18s}={sv.mean():.3f}+/-{sv.std():.3f} {np.round(sv,3).tolist()}')
