import sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
AEF=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
df=pd.read_csv('scratch/tg01_samples.csv').dropna(subset=AEF+S2+['tmf'])
df=df[df.tmf>0].copy(); df['y']=df.tmf.map(lambda c:{1:0,2:1,3:2}.get(int(c),3))
TR=df[df.lon<-55.10]; PO=df[df.lon>=-55.00].copy()
def nnd(Xte,Xca,ang):
    if ang:
        A=Xte/np.linalg.norm(Xte,axis=1,keepdims=True); B=Xca/np.linalg.norm(Xca,axis=1,keepdims=True)
        return np.degrees(np.arccos(np.clip((A@B.T).max(1),-1,1)))
    d=((Xte[:,None,:]-Xca[None,:,:])**2).sum(2) if len(Xca)<1500 else None
    if d is None:
        o=np.empty(len(Xte))
        for i in range(0,len(Xte),400):
            o[i:i+400]=np.sqrt(((Xte[i:i+400,None,:]-Xca[None,:,:])**2).sum(2).min(1))
        return o
    return np.sqrt(d.min(1))
for feats,tag,ang in [(AEF,'AEF64-angular',True),(S2,'S2comp-euclid',False)]:
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000)).fit(TR[feats].values,TR.y.values)
    P=m.predict_proba(PO[feats].values); S=1-P; Y=PO.y.values
    cal=PO.lon.values<-54.70; te=PO.lon.values>-54.60
    s=S[cal][np.arange(cal.sum()),Y[cal]]
    q=np.quantile(s,np.ceil((cal.sum()+1)*0.9)/cal.sum(),method='higher')
    inset=S<=q; cov=inset[np.arange(len(Y)),Y]; sz=inset.sum(1)
    Xc=PO[feats].values[cal]; Xt=PO[feats].values[te]
    if not ang:
        sc=StandardScaler().fit(TR[feats].values); Xc=sc.transform(Xc); Xt=sc.transform(Xt)
    d=nnd(Xt,Xc,ang); cvt=cov[te]; szt=sz[te]
    b=np.digitize(d,np.quantile(d,[.2,.4,.6,.8]))
    print(tag,'nominal=0.900 overall_cov=%.3f'%cvt.mean(),'ntest',te.sum(),'ncal',cal.sum(),flush=True)
    for k in range(5):
        mk=b==k
        print('  Q%d dist[%.3f,%.3f] n=%d cov=%.3f size=%.2f'%(k+1,d[mk].min(),d[mk].max(),mk.sum(),cvt[mk].mean(),szt[mk].mean()))
    r=np.corrcoef(d,cvt)[0,1]
    print('  corr(dist, covered)=%.3f  cov(Q1)-cov(Q5)=%+.3f'%(r,cvt[b==0].mean()-cvt[b==4].mean()),flush=True)
