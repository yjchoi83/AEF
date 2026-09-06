import sys; sys.path.insert(0,'scratch')
import numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import balanced_accuracy_score, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
A=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
ST=['elev','slope','tmean','prec']
br=pd.read_csv('scratch/TC01_BR.csv'); cg=pd.read_csv('scratch/TC01_CG.csv')
for d in (br,cg): d['blk']=(np.floor(d.lon/0.1).astype(int).astype(str)+'_'+np.floor(d.lat/0.1).astype(int).astype(str))
# (a) per-dim ridge R2 from statics, spatial-block CV, in BR
def dimR2(d,dim):
    sc=[]
    for tr,te in GroupKFold(n_splits=5).split(d,groups=d.blk):
        m=make_pipeline(StandardScaler(),Ridge(1.0)).fit(d[ST].values[tr],d[dim].values[tr])
        sc.append(r2_score(d[dim].values[te],m.predict(d[ST].values[te])))
    return float(np.mean(sc))
r2=pd.Series({a:dimR2(br,a) for a in A}).sort_values(ascending=False)
print('R2 top10:',[f'{k}:{v:.2f}' for k,v in r2.head(10).items()])
print('R2 quantiles:',[round(r2.quantile(q),3) for q in (0.9,0.75,0.5,0.25,0.0)],'n>0.5:',int((r2>0.5).sum()))
def run(tag,fb,fc=None):
    fc=fc or fb; ind=[];tr_=[]
    for tri,tei in GroupKFold(n_splits=5).split(br,groups=br.blk):
        m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')).fit(br[fb].values[tri],br.y.values[tri])
        ind.append(balanced_accuracy_score(br.y.values[tei],m.predict(br[fb].values[tei])))
        tr_.append(balanced_accuracy_score(cg.y.values,m.predict(cg[fc].values)))
    print(f'{tag:22s} in {np.mean(ind):.3f}(sd{np.std(ind):.3f}) tr {np.mean(tr_):.3f}(sd{np.std(tr_):.3f}) drop {np.mean(ind)-np.mean(tr_):+.3f} folds_in {[round(x,3) for x in ind]}')
    return np.mean(ind),np.mean(tr_)
for k in (8,16):
    top=list(r2.index[:k])
    run(f'AEF64',A) if k==8 else None
    run(f'AEF drop-top{k}',[a for a in A if a not in top])
    run(f'AEF only-top{k}',top)
run('S2-8band',S2); run('statics-only',ST)
# residualise all 64 dims on statics (fit on BR, apply to both)
rb,rc=br.copy(),cg.copy()
for a in A:
    m=make_pipeline(StandardScaler(),Ridge(1.0)).fit(br[ST].values,br[a].values)
    rb[a]=br[a].values-m.predict(br[ST].values); rc[a]=cg[a].values-m.predict(cg[ST].values)
br_o,cg_o=br,cg; br,cg=rb,rc; run('AEF64 residualised',A); br,cg=br_o,cg_o
