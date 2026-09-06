import sys; sys.path.insert(0,'scratch')
import numpy as np, pandas as pd
from aefkit import blocks, probe, AEF_BANDS
df=pd.read_csv('scratch/tb01_samples.csv')
df['blk']=blocks(df,0.1)
A3=[f"{k}{b}" for k in 'pyq' for b in AEF_BANDS]; A1=[f"y{b}" for b in AEF_BANDS]
SB=['B4','B8','B11','NDVI','NBR']; S3=[f"s{k}_{b}" for k in 'pyq' for b in SB]
S3=[c for c in S3 if c in df.columns]
df=df.dropna(subset=A3+S3).copy()
ev=df[df.m>0].copy(); st=df[df.m==0].copy()
print('n_ev=%d n_stable=%d blocks=%d'%(len(ev),len(st),df.blk.nunique()))
print('month balance:',ev.m.value_counts().sort_index().to_dict())
# --- (b) month recovery, 12-class + regression ---
for nm,F in [('AEF-192(Y-1,Y,Y+1)',A3),('AEF-64(Y only)',A1),('S2-15(3yr)',S3),('n_s2 only',['n_s2'])]:
    if not set(F)<=set(ev.columns): continue
    c=probe(ev,F,'m',ev.blk,task='clf',folds=5); r=probe(ev,F,'m',ev.blk,task='reg',folds=5)
    d=ev.dropna(subset=F+['m'])
    print('%-22s bal-acc %.3f sd %.3f folds %s | ridge R2 %.3f sd %.3f n=%d'%(nm,c[0],c[1],c[2],r[0],r[1],c[3]))
# MAE for best
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
for nm,F in [('AEF-192',A3),('S2-15',S3)]:
    d=ev.dropna(subset=F+['m']); X,y,g=d[F].values,d.m.values,d.blk.values; mae=[]
    for tr,te in GroupKFold(n_splits=5).split(X,y,g):
        m=make_pipeline(StandardScaler(),Ridge(alpha=10.)).fit(X[tr],y[tr])
        mae.append(float(np.abs(m.predict(X[te])-y[te]).mean()))
    print('%s month MAE %.2f mo (sd %.2f) folds %s'%(nm,np.mean(mae),np.std(mae),[round(v,2) for v in mae]))
# --- (c) detection lag: AUC per event month, year-Y vs year-Y+1 angular change ---
from sklearn.metrics import roc_auc_score
ev['dNBR_pY']=ev['sp_NBR']-ev['sy_NBR']; st['dNBR_pY']=st['sp_NBR']-st['sy_NBR']
ev['dNBR_pQ']=ev['sp_NBR']-ev['sq_NBR']; st['dNBR_pQ']=st['sp_NBR']-st['sq_NBR']
print('month  n  AUC_aY  AUC_aY1  AUC_dNBRpY  AUC_dNBRpQ  n_s2med')
for mm in range(1,13):
    e=ev[ev.m==mm]
    if len(e)<20: continue
    row=[]
    for col in ['aY','aY1','dNBR_pY','dNBR_pQ']:
        a=pd.concat([e[col],st[col]]).values; lab=np.r_[np.ones(len(e)),np.zeros(len(st))]
        ok=~np.isnan(a); row.append(roc_auc_score(lab[ok],a[ok]))
    print('%5d %4d  %.3f   %.3f    %.3f       %.3f      %.0f'%(mm,len(e),*row,e.n_s2.median()))
print('spearman(m,n_s2)=%.3f'%ev[['m','n_s2']].corr(method='spearman').iloc[0,1])
print('FPR of aY at thr=P95(stable): %.3f ; mean aY stable=%.2f, aRef stable=%.2f'%(
  (ev.aY>np.nanpercentile(st.aY,95)).mean(), st.aY.mean(), st.aRef.mean()))
