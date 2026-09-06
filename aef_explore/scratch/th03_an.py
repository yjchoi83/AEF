import pandas as pd,numpy as np,pyproj
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
import os
if os.path.exists('scratch/th03_cells_gee.csv') and os.path.getsize('scratch/th03_cells_gee.csv')>1000:
    g=pd.read_csv('scratch/th03_cells_gee.csv')
else:
    a=pd.read_csv('scratch/th03_AEF_part.csv').drop_duplicates(subset=['lon','lat'])
    s_=pd.read_csv('scratch/th03_S2_part.csv').drop_duplicates(subset=['lon','lat'])
    g=a.merge(s_,on=['lon','lat'],how='inner'); print('PARTIAL merge: AEF',len(a),'S2',len(s_),'joint',len(g))
tr=pyproj.Transformer.from_crs(4326,32636,always_xy=True)
x,y=tr.transform(g.lon.values,g.lat.values)
g['ix']=np.floor(x/300).astype(int); g['iy']=np.floor(y/300).astype(int)
d=pd.read_csv('/tmp/claude-1002/-d-yj-projects-workspace-yj-Alphaearth/f90c5da1-e8fc-4e10-b6a0-7d8144493182/scratchpad/gaza_cells300.csv')
m=g.merge(d[['ix','iy','d_all','d23','d24','s24']],on=['ix','iy'],how='left')
m[['d_all','d23','d24','s24']]=m[['d_all','d23','d24','s24']].fillna(0)
m=m.dropna(subset=['aef_2224','s2_2224','aef_2425','bs'])
print('cells',len(m),'| UNOSAT sites matched',int(m.d_all.sum()),'of 170422')
b=m[m.bs>=500].copy()                       # >=5% built-up 300m cells
b['bs_ha']=b.bs*9/1e4                       # built surface, ha per cell
b['inten']=b.d24/b.bs_ha                    # damaged sites per built-ha
print('built cells',len(b),'| zero-damage',int((b.d24==0).sum()),'| median d24',b.d24.median(),'| median inten',round(b.inten.median(),1))
print(b[['aef_2223','aef_2324','aef_2224','aef_2425','s2_2224','bs','d23','d24','inten']].describe().round(2).to_string())
for t in ['d24','inten','s24','d23']:
    print(f'Spearman {t}: AEF a2224 {spearmanr(b.aef_2224,b[t]).statistic:+.3f} | S2 a2224 {spearmanr(b.s2_2224,b[t]).statistic:+.3f}')
# partial Spearman controlling for built surface (reviewer-2 preemption)
def prho(a,c,ctrl):
    import numpy as np
    from scipy.stats import rankdata
    A,C,Z=[rankdata(v) for v in (a,c,ctrl)]
    ra=A-np.polyval(np.polyfit(Z,A,1),Z); rc=C-np.polyval(np.polyfit(Z,C,1),Z)
    return np.corrcoef(ra,rc)[0,1]
print('partial-Spearman | bs: AEF a2224 vs inten %+.3f | S2 %+.3f | AEF vs d24 %+.3f | S2 %+.3f'%(
  prho(b.aef_2224,b.inten,b.bs),prho(b.s2_2224,b.inten,b.bs),
  prho(b.aef_2224,b.d24,b.bs),prho(b.s2_2224,b.d24,b.bs)))
print('within-year: AEF a2223 vs d23 %+.3f | S2? n/a | AEF a2324 vs (d24-d23) %+.3f'%(
  spearmanr(b.aef_2223,b.d23).statistic, spearmanr(b.aef_2324,b.d24-b.d23).statistic))
hi=b.inten[b.inten>0].quantile(2/3.)
sub=b[(b.d24==0)|(b.inten>=hi)].copy(); sub['yy']=(sub.inten>=hi).astype(int)
sub['blk']=(np.floor(sub.lat/0.09).astype(int).astype(str)+'_'+np.floor(sub.lon/0.09).astype(int).astype(str))
print('AUC set n',len(sub),'pos',int(sub.yy.sum()),'neg',int(len(sub)-sub.yy.sum()),
      '| thr inten',round(hi,1),'| blocks(~10km)',sub.blk.nunique())
gk=GroupKFold(n_splits=5)
for nm,fs in [('AEF a2224',['aef_2224']),('S2 a2224 [baseline]',['s2_2224']),
              ('AEF 2ang',['aef_2223','aef_2324']),('AEF traj4',['aef_2223','aef_2324','aef_2224','aef_2425']),
              ('S2+bs',['s2_2224','bs']),('AEF a2224+bs',['aef_2224','bs'])]:
    sc=[]
    for tri,tei in gk.split(sub,sub.yy,sub.blk):
        a,e=sub.iloc[tri],sub.iloc[tei]
        if e.yy.nunique()<2: continue
        mo=LogisticRegression(max_iter=3000).fit(a[fs],a.yy)
        sc.append(roc_auc_score(e.yy,mo.predict_proba(e[fs])[:,1]))
    print(f'  {nm}: AUC {np.mean(sc):.3f} sd {np.std(sc):.3f} folds {[round(s,3) for s in sc]} nf={len(sc)}')
q=b.inten
for nm,mask in [('undamaged(d24=0)',b.d24==0),('low',(q>0)&(q<q[q>0].quantile(1/3.))),
                ('heavy',q>=hi)]:
    s=b[mask]
    print(f'{nm} n={len(s)}: a2223 {s.aef_2223.mean():.2f} a2324 {s.aef_2324.mean():.2f} a2425 {s.aef_2425.mean():.2f}±{s.aef_2425.std():.2f} s2_2224 {s.s2_2224.mean():.2f}')
