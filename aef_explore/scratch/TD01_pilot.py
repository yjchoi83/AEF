import ee, math, numpy as np, pandas as pd, sys, json
ee.Initialize(project='alpha-earth-app')
Y=2022; roi=ee.Geometry.Rectangle([-56.0,-7.0,-54.2,-5.2])   # Para/N-Mato Grosso arc, ~200x200 km
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
aef=lambda y: AEF.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(roi).mosaic()
e0,e1=aef(Y-1),aef(Y)
ang=e0.multiply(e1).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/math.pi).rename('ang_aef')
ac=ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').mosaic()
degy=ee.ImageCollection('projects/JRC/TMF/v1_2024/DegradationYear').mosaic().unmask(0)
defy=ee.ImageCollection('projects/JRC/TMF/v1_2024/DeforestationYear').mosaic().unmask(0)
acY,acP=ac.select(f'Dec{Y}'),ac.select(f'Dec{Y-1}')
hans=ee.Image('UMD/hansen/global_forest_change_2025_v1_13')
intact=acY.eq(1).And(degy.eq(0)).And(defy.eq(0)).And(hans.select('lossyear').eq(0))
deg=degy.eq(Y).And(defy.neq(Y))
clr=defy.eq(Y).Or(hans.select('lossyear').eq(Y-2000)).And(degy.neq(Y))
nonf=acY.eq(6).And(acP.eq(6)).And(degy.eq(0)).And(defy.eq(0))
cls=ee.Image(0).where(intact,1).where(nonf,2).where(deg,3).where(clr,4).selfMask().rename('cls').toByte()
def s2(y):
    b=['B2','B3','B4','B8','B11','B12']
    c=(ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate(f'{y}-01-01',f'{y+1}-01-01')
       .filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',60))
       .map(lambda i: i.updateMask(i.select('SCL').remap([3,8,9,10,11],[0,0,0,0,0],1)))
       .select(b).median().divide(1e4))
    ndvi=c.normalizedDifference(['B8','B4']).rename('NDVI'); nbr=c.normalizedDifference(['B8','B12']).rename('NBR')
    return c.addBands(ndvi).addBands(nbr)
s0,s1=s2(Y-1),s2(Y)
n0=s0.divide(s0.pow(2).reduce(ee.Reducer.sum()).sqrt()); n1=s1.divide(s1.pow(2).reduce(ee.Reducer.sum()).sqrt())
angs2=n0.multiply(n1).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/math.pi).rename('ang_s2')
stack=e1.addBands(ang).addBands(s1.rename([f'S{i}' for i in range(8)])).addBands(angs2).addBands(cls)
samp=stack.stratifiedSample(numPoints=1200,classBand='cls',region=roi,scale=10,seed=7,
                            geometries=True,tileScale=8,dropNulls=True)
rows=samp.getInfo()['features']; print('n_features',len(rows))
recs=[]
for f in rows:
    p=dict(f['properties']); lon,lat=f['geometry']['coordinates']
    p['blk']=f"{int(math.floor(lon/0.1))}_{int(math.floor(lat/0.1))}"; recs.append(p)
df=pd.DataFrame(recs).dropna()
df.to_csv('TD01_samples.csv',index=False)
NAME={1:'intact',2:'nonforest',3:'degradation',4:'clearing'}
print('class balance', {NAME[k]:int(v) for k,v in df.cls.value_counts().items()})
print('n_blocks',df.blk.nunique())
# --- angular gradient ---
for col in ['ang_aef','ang_s2']:
    out=[]
    for k in [1,3,4]:
        s=df.loc[df.cls==k,col]; out.append(f"{NAME[k]}: n={len(s)} mean={s.mean():.2f} sd={s.std():.2f} med={s.median():.2f}")
    print(col,' | '.join(out))
    nf=df.loc[df.cls==2,col]; print(f'  {col} nonforest: n={len(nf)} mean={nf.mean():.2f} sd={nf.std():.2f}')
    sub=df[df.cls.isin([1,3,4])].copy(); rank=sub.cls.map({1:0,3:1,4:2})
    from scipy.stats import spearmanr,kendalltau,mannwhitneyu
    print(f'  spearman_rho={spearmanr(rank,sub[col]).statistic:.3f} kendall_tau={kendalltau(rank,sub[col]).statistic:.3f}',
          f'AUC_intact_vs_deg={mannwhitneyu(df.loc[df.cls==3,col],df.loc[df.cls==1,col]).statistic/(len(df[df.cls==3])*len(df[df.cls==1])):.3f}',
          f'AUC_deg_vs_clr={mannwhitneyu(df.loc[df.cls==4,col],df.loc[df.cls==3,col]).statistic/(len(df[df.cls==4])*len(df[df.cls==3])):.3f}')
# --- separability, spatial block CV ---
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold, cross_val_score
FE={'AEF64':[f'A{i:02d}' for i in range(64)],'S2_8b':[f'S{i}' for i in range(8)],
    'AEF64+ang':[f'A{i:02d}' for i in range(64)]+['ang_aef'],'S2_8b+ang':[f'S{i}' for i in range(8)]+['ang_s2']}
y=df.cls.values; g=df.blk.values; gkf=GroupKFold(n_splits=5)
for nm,cols in FE.items():
    X=df[cols].values
    for mdl,tag in [(LogisticRegression(max_iter=3000,C=1.0),'linprobe'),(KNeighborsClassifier(15),'kNN15')]:
        sc=cross_val_score(make_pipeline(StandardScaler(),mdl),X,y,groups=g,cv=gkf,scoring='f1_macro')
        print(f'{nm:>10s} {tag:>9s} macroF1={sc.mean():.3f}+/-{sc.std():.3f} folds={np.round(sc,3).tolist()}')
