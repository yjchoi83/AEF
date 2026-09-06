import pandas as pd, numpy as np
d = pd.read_csv('scratch/tb02_p1.csv')
YR = list(range(2018,2026))
# long format: one row per pixel-year
L=[]
for y in YR:
    t = d[['roi','grp','lon','lat','dwc',f'ang_{y}',f's1_{y}',f's2_{y}',f'pr_{y}',f'tas_{y}',
           f's1_{y-1}',f's2_{y-1}',f'pr_{y-1}',f'tas_{y-1}']].copy()
    t.columns=['roi','grp','lon','lat','dwc','ang','s1','s2','pr','tas','s1p','s2p','prp','tasp']
    t['year']=y; L.append(t)
L=pd.concat(L,ignore_index=True).dropna(subset=['ang'])
# anomalies vs 2017-2025 per-pixel mean
for c in ['pr','tas']:
    m=L.groupby(['lon','lat'])[c].transform('mean'); L[c+'_an']=L[c]-m
L['s1_min']=L[['s1','s1p']].min(axis=1); L['s2_min']=L[['s2','s2p']].min(axis=1)
L['blk']=(np.floor(L.lon/0.1).astype(int).astype(str)+'_'+np.floor(L.lat/0.1).astype(int).astype(str))
print('n pixel-years',len(L),'n pixels',L.groupby(["lon","lat"]).ngroups)
print('\n== S1 VV scene count per pixel, median by roi x year ==')
print(d.groupby('roi')[[f's1_{y}' for y in range(2017,2026)]].median().astype(int).to_string())
print('\n== S2 usable obs count, median by roi x year ==')
print(d.groupby('roi')[[f's2_{y}' for y in range(2017,2026)]].median().astype(int).to_string())
print('\n== drift angle_deg median (IQR) by roi x year ==')
piv=L.pivot_table(index='roi',columns='year',values='ang',aggfunc='median').round(2)
print(piv.to_string())
print('\n IQR:'); print(L.pivot_table(index='roi',columns='year',values='ang',
      aggfunc=lambda x: np.subtract(*np.percentile(x,[75,25]))).round(2).to_string())
print('\n== group medians ==')
print(L.pivot_table(index='grp',columns='year',values='ang',aggfunc='median').round(2).to_string())
# year effect: per-pixel deviation from that pixel's own 2018-2021+2025 baseline median
base=L[L.year.isin([2019,2020,2021])].groupby(['lon','lat'])['ang'].median().rename('b')
L=L.merge(base,on=['lon','lat'],how='left'); L['dev']=L['ang']-L['b']
print('\n== year effect (median deg above own 2019-21 baseline) ==')
print(L.pivot_table(index='grp',columns='year',values='dev',aggfunc='median').round(2).to_string())
# variance decomposition: nested partial R2, GroupKFold by 0.1deg block
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
def r2(F,dat,tgt='ang'):
    X=dat[F].values; y=dat[tgt].values; g=dat['blk'].values; s=[]
    for tr,te in GroupKFold(n_splits=5).split(X,y,g):
        m=make_pipeline(StandardScaler(),Ridge(alpha=1.0)).fit(X[tr],y[tr])
        s.append(r2_score(y[te],m.predict(X[te])))
    return round(float(np.mean(s)),3), round(float(np.std(s)),3)
D=L.dropna(subset=['ang','s1','s2','pr_an','tas_an']).copy()
D['yr_c']=D.year-2021
SETS={'null_regionyear':['yr_c'],
 'obs_S1':['s1','s1p','s1_min'], 'obs_S2':['s2','s2p','s2_min'],
 'obs_all':['s1','s1p','s1_min','s2','s2p','s2_min'],
 'clim':['pr_an','tas_an'], 'obs+clim':['s1','s1p','s1_min','s2','s2p','s2_min','pr_an','tas_an'],
 'obs+clim+dwc':['s1','s1p','s1_min','s2','s2p','s2_min','pr_an','tas_an','dwc']}
print('\n== partial R2 on drift (5 spatial-block folds), n=%d =='%len(D))
for k,v in SETS.items(): print(f'  {k:18s}', r2(v,D))
for g in ['AF','SA','EU','US']:
    sub=D[D.grp==g]
    print(f'  [{g} only, n={len(sub)}] obs_all', r2(SETS['obs_all'],sub), ' clim', r2(SETS['clim'],sub))
# FPR inflation: threshold calibrated to 5% FPR on stable land in a normal year (2019-2021)
print('\n== FPR at threshold calibrated to 5%/1% FPR on 2019-2021 stable land, per group ==')
for g in ['AF','SA','EU','US']:
    s=D[D.grp==g]
    for a in [0.05,0.01]:
        thr=np.percentile(s[s.year.isin([2019,2020,2021])]['ang'],100*(1-a))
        row=[f'{y}:{(s[s.year==y]["ang"]>thr).mean()*100:.1f}%' for y in YR]
        print(f'  {g} a={a:.2f} thr={thr:.1f}deg', ' '.join(row))
D.to_csv('scratch/tb02_long.csv',index=False)
