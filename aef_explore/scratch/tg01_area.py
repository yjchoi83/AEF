import sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
AEF=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
df=pd.read_csv('scratch/tg01_samples.csv').dropna(subset=AEF+S2+['tmf'])
df=df[df.tmf>0].copy(); df['y']=df.tmf.map(lambda c:{1:0,2:1,3:2}.get(int(c),3))
TR=df[df.lon<-55.10]; PO=df[df.lon>=-55.00].copy()
def strat_se(strata,truth,n):
    """proportional-allocation stratified SE of P(truth) using pool as pseudo-population"""
    out=0.0
    for h in np.unique(strata):
        m=strata==h; W=m.mean(); p=truth[m].mean(); nh=max(n*W,2.0)
        out+=W*W*p*(1-p)/nh
    return float(np.sqrt(out))
for feats,tag in [(AEF,'AEF64'),(S2,'S2comp')]:
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000)).fit(TR[feats].values,TR.y.values)
    P=m.predict_proba(PO[feats].values); S=1-P; yh=P.argmax(1); Y=PO.y.values
    tgt=(Y==2).astype(float)   # deforested-area indicator
    cal=PO.lon.values<-54.70; te=~cal          # calibration from spatially separated blocks
    s=S[cal][np.arange(cal.sum()),Y[cal]]
    q=np.quantile(s,np.ceil((cal.sum()+1)*0.9)/cal.sum(),method='higher')
    setsz=(S<=q).sum(1)
    Ai,Bi,Ci=yh,np.clip(setsz,1,3),yh*10+np.clip(setsz,1,3)
    mx=P.max(1); Di=np.digitize(mx,np.quantile(mx,[.25,.5,.75]))
    for n in [500,1000,2000]:
        r={'srs':np.sqrt(tgt.mean()*(1-tgt.mean())/n),
           'mapclass':strat_se(Ai,tgt,n),'setsize':strat_se(Bi,tgt,n),
           'map x setsize':strat_se(Ci,tgt,n),'maxprob-q4':strat_se(Di,tgt,n)}
        print(tag,'n=',n,{k:round(v,5) for k,v in r.items()},
              'relSE_vs_mapclass',{k:round(v/r['mapclass'],3) for k,v in r.items()},flush=True)
    print(tag,'P_true_deforested=%.4f'%tgt.mean(),'setsize dist',
          dict(zip(*np.unique(np.clip(setsz,1,3),return_counts=True))),'nPOOL',len(PO))
