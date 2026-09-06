import pandas as pd, numpy as np
from sklearn.linear_model import Ridge; from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler; from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
L=pd.read_csv('scratch/tb02_long.csv'); YR=list(range(2018,2026))
d=pd.read_csv('scratch/tb02_p1.csv')
pre=d.groupby('roi')[[f's1_{y}' for y in range(2017,2022)]].median().mean(axis=1)
gap=d.groupby('roi')[[f's1_{y}' for y in range(2022,2025)]].median().mean(axis=1)
ret=(gap/pre).round(2); print('S1 retention 2022-24 / 2017-21 by roi:\n',ret.to_string())
L['s1ret']=L.roi.map(ret); L['gapROI']=np.where(L.s1ret<0.6,'S1GAP','S1OK')
for lab,sub in [('ALL',L),('TREES(dwc=1)',L[L.dwc==1])]:
    print(f'\n===== {lab}  n_pixyr={len(sub)} =====')
    print('median drift by roi x year'); print(sub.pivot_table(index='roi',columns='year',values='ang',aggfunc='median').round(2).to_string())
    print('year effect (dev vs own 2019-21 median)')
    print(sub.pivot_table(index=['gapROI','roi'],columns='year',values='dev',aggfunc='median').round(2).to_string())
    print('year effect by S1-gap stratum'); print(sub.pivot_table(index='gapROI',columns='year',values='dev',aggfunc='median').round(2).to_string())
def r2(F,dat,tgt):
    D=dat.dropna(subset=F+[tgt]); X=D[F].values;y=D[tgt].values;g=D['blk'].values;s=[]
    if len(np.unique(g))<5 or len(D)<200: return ('ns',len(D))
    for tr,te in GroupKFold(n_splits=5).split(X,y,g):
        m=make_pipeline(StandardScaler(),Ridge(1.0)).fit(X[tr],y[tr]); s.append(r2_score(y[te],m.predict(X[te])))
    return (round(float(np.mean(s)),3), round(float(np.std(s)),3), len(D))
S1=['s1','s1p','s1_min']; S2=['s2','s2p','s2_min']; CL=['pr_an','tas_an']
print('\n== partial R2 on WITHIN-PIXEL drift deviation (dev), 5 spatial-block folds ==')
for nm,dat in [('pooled',L)]+[(g,L[L.roi==g]) for g in sorted(L.roi.unique())]:
    print(f'  {nm:12s} S1={r2(S1,dat,"dev")} S2={r2(S2,dat,"dev")} S1+S2={r2(S1+S2,dat,"dev")} clim={r2(CL,dat,"dev")} all={r2(S1+S2+CL,dat,"dev")}')
print('\n== FPR by roi, threshold = 95th pct of 2019-2021 stable-land drift ==')
for g in sorted(L.roi.unique()):
    s=L[L.roi==g]; thr=np.percentile(s[s.year.isin([2019,2020,2021])]['ang'],95)
    print(f'  {g:10s} thr={thr:5.1f} '+' '.join(f'{y}:{(s[s.year==y]["ang"]>thr).mean()*100:4.1f}%' for y in YR))
