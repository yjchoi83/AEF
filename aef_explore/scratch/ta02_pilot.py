import sys; sys.path.insert(0,'scratch')
from aefkit import *
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error
NAME=sys.argv[1]; BOX=[float(x) for x in sys.argv[2].split(',')]; Y=2023
AGE='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1'
INT='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1'
roi=ee.Geometry.Rectangle(BOX)
age=ee.Image(AGE).select(f'secondary_vegetation_age_{Y}').unmask(0).rename('age')
mature=ee.Image(INT).select(f'classification_{Y}').eq(3).And(age.eq(0))
b=(age.gte(1).And(age.lte(3)).multiply(1).add(age.gte(4).And(age.lte(6)).multiply(2))
   .add(age.gte(7).And(age.lte(10)).multiply(3)).add(age.gte(11).And(age.lte(15)).multiply(4))
   .add(age.gte(16).And(age.lte(25)).multiply(5)).add(age.gte(26).multiply(6))
   .add(mature.multiply(7)).rename('bin'))
CL=[1,2,3,4,5,6,7]; PC=500
pts=b.stratifiedSample(numPoints=PC,classBand='bin',region=roi,scale=30,classValues=CL,
      classPoints=[PC]*7,geometries=True,dropNulls=True,seed=7,tileScale=4)
TR=[(y,y+1) for y in range(2017,Y)]
stack=aef(Y,roi).addBands(s2(Y,roi)).addBands(age).addBands(b)
for y1,y2 in TR: stack=stack.addBands(angle(y1,y2,roi).rename(f'g{y1}'))
f=stack.sampleRegions(collection=pts,scale=10,geometries=True,tileScale=4).getInfo()['features']
rows=[]
for r in f:
    d=dict(r['properties']); c=r['geometry']['coordinates']; d['lon'],d['lat']=c[0],c[1]; rows.append(d)
df=pd.DataFrame(rows); TB=[f'g{y}' for y,_ in TR]
df=df.dropna(subset=AEF_BANDS+S2_BANDS+TB+['age','bin'])
df['blk']=blocks(df,0.1)
print(NAME,'n=',len(df),'bins=',df.bin.value_counts().sort_index().to_dict(),'blocks=',df.blk.nunique())
sec=df[df.bin<=6].copy(); mat=df[df.bin==7].copy()
def run(feats,tag):
    gk=GroupKFold(n_splits=5); R2=[];MA=[]; pb={}; mp=[]
    for tr,te in gk.split(sec,groups=sec.blk):
        S,T=sec.iloc[tr],sec.iloc[te]
        m=make_pipeline(StandardScaler(),Ridge(alpha=10.0)).fit(S[feats],S.age)
        p=m.predict(T[feats]); R2.append(r2_score(T.age,p)); MA.append(mean_absolute_error(T.age,p))
        for bb in range(1,7):
            k=T.bin==bb
            if k.sum()>4: pb.setdefault(bb,[]).append((mean_absolute_error(T.age[k],p[k]),p[k].mean(),T.age[k].mean()))
        mp.append(m.predict(mat[feats]).mean())
    print(f'{tag:22s} R2 {np.mean(R2):.3f}+/-{np.std(R2):.3f} {[round(x,2) for x in R2]}  MAE {np.mean(MA):.2f}+/-{np.std(MA):.2f}y')
    print('   perbin MAE/meanpred/meantrue:',{bb:(round(np.mean([a for a,_,_ in v]),2),round(np.mean([b_ for _,b_,_ in v]),1),round(np.mean([c for _,_,c in v]),1)) for bb,v in sorted(pb.items())})
    print(f'   mature-stratum mean predicted age {np.mean(mp):.1f}y (n={len(mat)})')
run(AEF_BANDS,'AEF-64 (single yr)')
run(S2_BANDS,'S2-8 baseline')
run(TB,'traj angles only')
run(AEF_BANDS+TB,'AEF-64 + traj')
