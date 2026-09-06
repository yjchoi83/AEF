import sys, numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
A=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NBR']; ST=['elev','slope','tmean','prec']
br=pd.read_csv('scratch/TC01_BR.csv'); cg=pd.read_csv('scratch/TC01_CG.csv')
for d in (br,cg): d['blk']=(np.floor(d.lon/0.1).astype(int).astype(str)+'_'+np.floor(d.lat/0.1).astype(int).astype(str))
al=pd.concat([br,cg],ignore_index=True)
# ranking 1: pooled (cross-region) static decodability -> statics span both climates/terrains
pool={}
for a in A:
    m=make_pipeline(StandardScaler(),Ridge(1.0)).fit(al[ST].values,al[a].values)
    pool[a]=r2_score(al[a].values,m.predict(al[ST].values))
pool=pd.Series(pool).sort_values(ascending=False)
# ranking 2: cross-region standardized mean shift (domain-shift oracle)
sh=pd.Series({a: abs(br[a].mean()-cg[a].mean())/np.sqrt(0.5*(br[a].var()+cg[a].var())) for a in A}).sort_values(ascending=False)
print('pool-R2 top8:',[f'{k}:{v:.2f}' for k,v in pool.head(8).items()],'n>0.9:',int((pool>0.9).sum()),'n>0.7:',int((pool>0.7).sum()))
print('shift top8:',[f'{k}:{v:.2f}' for k,v in sh.head(8).items()],'median',round(sh.median(),2))
print('rank overlap top16 pool vs shift:',len(set(pool.index[:16])&set(sh.index[:16])))
def run(tag,fb,dfb=None,dfc=None):
    B=br if dfb is None else dfb; C=cg if dfc is None else dfc; ind=[];tr=[]
    for tri,tei in GroupKFold(n_splits=5).split(B,groups=B.blk):
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')).fit(B[fb].values[tri],B.y.values[tri])
        ind.append(balanced_accuracy_score(B.y.values[tei],m.predict(B[fb].values[tei])))
        tr.append(balanced_accuracy_score(C.y.values,m.predict(C[fb].values)))
    print(f'{tag:26s} in {np.mean(ind):.3f}(sd{np.std(ind):.3f}) tr {np.mean(tr):.3f}(sd{np.std(tr):.3f}) drop {np.mean(ind)-np.mean(tr):+.3f}')
for k in (8,16,24):
    run(f'drop-top{k}-poolR2',[a for a in A if a not in set(pool.index[:k])])
for k in (8,16,24):
    run(f'drop-top{k}-shift',[a for a in A if a not in set(sh.index[:k])])
# per-region z-scoring of features (tests pure mean/scale domain shift)
zb,zc=br.copy(),cg.copy()
for a in A+S2:
    zb[a]=(br[a]-br[a].mean())/br[a].std(); zc[a]=(cg[a]-cg[a].mean())/cg[a].std()
run('AEF64 per-region z',A,zb,zc); run('S2 per-region z',S2,zb,zc)
