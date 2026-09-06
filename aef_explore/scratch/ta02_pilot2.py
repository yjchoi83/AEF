import sys; sys.path.insert(0,'scratch')
from aefkit import *
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error
from scipy.stats import spearmanr
Y=2023; PC=400; CL=[1,2,3,4,5,6,7]
AGE='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1'
INT='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1'
age=ee.Image(AGE).select(f'secondary_vegetation_age_{Y}').unmask(0).rename('age')
mature=ee.Image(INT).select(f'classification_{Y}').eq(3).And(age.eq(0))
b=(age.gte(1).And(age.lte(3)).multiply(1).add(age.gte(4).And(age.lte(6)).multiply(2))
   .add(age.gte(7).And(age.lte(10)).multiply(3)).add(age.gte(11).And(age.lte(15)).multiply(4))
   .add(age.gte(16).And(age.lte(25)).multiply(5)).add(age.gte(26).multiply(6))
   .add(mature.multiply(7)).rename('bin'))
TR=[(y,y+1) for y in range(2017,Y)]; TB=[f'g{y}' for y,_ in TR]
def grab(box,seed):
    roi=ee.Geometry.Rectangle(box)
    pts=b.stratifiedSample(numPoints=PC,classBand='bin',region=roi,scale=30,classValues=CL,
        classPoints=[PC]*7,geometries=True,dropNulls=True,seed=seed,tileScale=4)
    st=aef(Y,roi).addBands(s2(Y,roi)).addBands(age).addBands(b)
    for y1,y2 in TR: st=st.addBands(angle(y1,y2,roi).rename(f'g{y1}'))
    f=st.sampleRegions(collection=pts,scale=10,geometries=True,tileScale=4).getInfo()['features']
    rr=[]
    for r in f:
        d=dict(r['properties']); c=r['geometry']['coordinates']; d['lon'],d['lat']=c[0],c[1]; rr.append(d)
    d=pd.DataFrame(rr).dropna(subset=AEF_BANDS+S2_BANDS+TB+['age','bin']); d['blk']=blocks(d,0.1); return d
AM=grab([-48.6,-2.4,-47.4,-1.2],11); SP=grab([-47.6,-24.2,-46.4,-23.0],12)
AM.to_csv('scratch/ta02_am.csv',index=False); SP.to_csv('scratch/ta02_sp.csv',index=False)
def fit(tr,feats):
    return make_pipeline(StandardScaler(),Ridge(alpha=10.0)).fit(tr[feats],tr.age)
def inreg(df,feats,tag):
    s=df[df.bin<=6]; m=df[df.bin==7]; R=[];M=[];pb={};mp=[];rho=[]
    for a,t in GroupKFold(n_splits=5).split(s,groups=s.blk):
        S,T=s.iloc[a],s.iloc[t]; mo=fit(S,feats); p=mo.predict(T[feats])
        R.append(r2_score(T.age,p)); M.append(mean_absolute_error(T.age,p))
        rho.append(spearmanr(T.age,p).statistic); mp.append(mo.predict(m[feats]).mean())
        for k in range(1,7):
            q=T.bin==k
            if q.sum()>4: pb.setdefault(k,[]).append((mean_absolute_error(T.age[q],p[q]),p[q].mean()))
    print(f'  {tag:20s} R2 {np.mean(R):.3f}+/-{np.std(R):.3f} {[round(x,2) for x in R]} MAE {np.mean(M):.2f}y rho {np.mean(rho):.3f} mature_pred {np.mean(mp):.1f}y')
    print('    perbin MAE/pred:',{k:(round(np.mean([x for x,_ in v]),2),round(np.mean([y for _,y in v]),1)) for k,v in sorted(pb.items())})
for nm,df in [('AMAZON_Bragantina',AM),('ATL_SP',SP)]:
    print(nm,'n=',len(df),df.bin.value_counts().sort_index().to_dict(),'blk',df.blk.nunique())
    for f,t in [(AEF_BANDS,'AEF-64'),(S2_BANDS,'S2-8'),(TB,'traj only'),(AEF_BANDS+TB,'AEF+traj')]: inreg(df,f,t)
    for lo,hi,t in [(1,15,'young<=15y'),(16,60,'old>=16y')]:
        s=df[(df.bin<=6)&(df.age>=lo)&(df.age<=hi)]; R=[]
        for a,tt in GroupKFold(n_splits=5).split(s,groups=s.blk):
            S,T=s.iloc[a],s.iloc[tt]; R.append(r2_score(T.age,fit(S,AEF_BANDS).predict(T[AEF_BANDS])))
        print(f'    AEF-64 restricted {t}: R2 {np.mean(R):.3f} (n={len(s)})')
for a,bb,na,nb in [(AM,SP,'AMZ','SP'),(SP,AM,'SP','AMZ')]:
    m=fit(a[a.bin<=6],AEF_BANDS); t=bb[bb.bin<=6]; p=m.predict(t[AEF_BANDS])
    print(f'  TRANSFER {na}->{nb}: R2 {r2_score(t.age,p):.3f} MAE {mean_absolute_error(t.age,p):.2f}y rho {spearmanr(t.age,p).statistic:.3f}')
