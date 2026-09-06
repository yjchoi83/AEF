import sys, numpy as np, pandas as pd; sys.path.insert(0,'scratch')
from scipy.linalg import sqrtm; from scipy.stats import spearmanr
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
AEF=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
df=pd.read_csv('scratch/tc03_samples.csv').dropna(subset=AEF+S2+['y'])
df['blk']=(np.floor(df.lon/0.1).astype(int).astype(str)+'_'+np.floor(df.lat/0.1).astype(int).astype(str))
rois=sorted(df.roi.unique())
print('n per ROI / pos-frac / blocks'); print(df.groupby('roi').agg(n=('y','size'),pos=('y','mean'),nblk=('blk','nunique')).round(3).to_string())
def mk(): return make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced'))
res={}
for F,nm in [(AEF,'AEF'),(S2,'S2')]:
    # global standardize for shift stats
    Z=StandardScaler().fit_transform(df[F].values); X={r:Z[(df.roi==r).values] for r in rois}
    inr={}
    for r in rois:
        d=df[df.roi==r]; sc=[]
        for tr,te in GroupKFold(n_splits=5).split(d[F],d.y,d.blk):
            m=mk().fit(d[F].values[tr],d.y.values[tr]); sc.append(roc_auc_score(d.y.values[te],m.predict_proba(d[F].values[te])[:,1]))
        inr[r]=(np.mean(sc),np.std(sc))
    print(nm,'in-region AUC:',{r:(round(v[0],3),round(v[1],3)) for r,v in inr.items()})
    # median-heuristic bandwidth on pooled subsample
    sub=Z[np.random.RandomState(0).choice(len(Z),1200,replace=False)]
    D=((sub[:,None,:]-sub[None,:,:])**2).sum(-1); g=1.0/np.median(D[D>0])
    rows=[]
    for a in rois:
        d=df[df.roi==a]; M=mk().fit(d[F].values,d.y.values)
        for b in rois:
            if a==b: continue
            e=df[df.roi==b]; auc=roc_auc_score(e.y.values,M.predict_proba(e[F].values)[:,1])
            drop=inr[a][0]-auc
            A,B=X[a],X[b]; ma,mb=A.mean(0),B.mean(0)
            cs=float(ma@mb/(np.linalg.norm(ma)*np.linalg.norm(mb)+1e-12))
            Sa,Sb=np.cov(A,rowvar=False),np.cov(B,rowvar=False)
            fr=float(((ma-mb)**2).sum()+np.trace(Sa+Sb-2*np.real(sqrtm(Sa@Sb))))
            lin=float(((ma-mb)**2).sum())
            K=lambda P,Q: np.exp(-g*((P[:,None,:]-Q[None,:,:])**2).sum(-1)).mean()
            mmd=float(K(A,A)+K(B,B)-2*K(A,B))
            An=A/np.linalg.norm(A,axis=1,keepdims=True); Bn=B/np.linalg.norm(B,axis=1,keepdims=True)
            nn=float((1-(Bn@An.T).max(1)).mean())
            rows.append(dict(a=a,b=b,auc=auc,dr=drop,cos=cs,frechet=fr,mmd_lin=lin,mmd_rbf=mmd,nn_cos=nn))
    R=pd.DataFrame(rows); res[nm]=R
    print(nm,'pairs',len(R),'drop mean/med/max',round(R['dr'].mean(),3),round(R['dr'].median(),3),round(R['dr'].max(),3))
    for s in ['cos','frechet','mmd_lin','mmd_rbf','nn_cos']:
        rho,p=spearmanr(R[s],R['dr']); print(f'  {nm} {s:9s} rho={rho:+.3f} p={p:.1e}')
# cross: S2-space statistic vs AEF drop; and AEF stat vs S2 drop
A_,S_=res['AEF'],res['S2']; k=['a','b']
M=A_.merge(S_,on=k,suffixes=('_ae','_s2'))
for s in ['cos','frechet','mmd_lin','mmd_rbf','nn_cos']:
    r1=spearmanr(M[s+"_s2"],M["dr_ae"])[0]; r2=spearmanr(M[s+"_ae"],M["dr_s2"])[0]
    print("cross S2stat->AEFdrop %-9s rho=%+.3f   AEFstat->S2drop rho=%+.3f"%(s,r1,r2))
print('AEF vs S2 drop corr', round(spearmanr(M['dr_ae'],M['dr_s2'])[0],3))
# threshold utility on best AEF stat
for s in ['nn_cos','mmd_rbf','frechet']:
    for th in np.quantile(A_[s],[0.25,0.5,0.75]):
        lo,hi=A_[A_[s]<=th]['dr'],A_[A_[s]>th]['dr']
        print(f'thr {s} q={th:.3f}: below n={len(lo)} meandrop={lo.mean():.3f} maxdrop={lo.max():.3f} | above n={len(hi)} meandrop={hi.mean():.3f}')
A_.to_csv('scratch/tc03_pairs_aef.csv',index=False); S_.to_csv('scratch/tc03_pairs_s2.csv',index=False)
