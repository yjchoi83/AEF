import numpy as np, pandas as pd, itertools, glob
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr
AB=[f'A{i:02d}' for i in range(64)]; SB=['B2','B3','B4','B8','B11','B12','NDVI']
TAX=[1,2,4,6]  # tree, shrub/grass, built, water: only classes present in ALL 6 regions
D={}
for f in sorted(glob.glob('TC03_???.csv')):
    d=pd.read_csv(f); d=d[d.lc.isin(TAX)].reset_index(drop=True); D[f.split('_')[1][:3]]=d
allS2=np.vstack([d[SB].values for d in D.values()]); mu,sd=allS2.mean(0),allS2.std(0)
R={}
for k,d in D.items():
    g=(np.floor(d.lon/0.1).astype(int).astype(str)+'_'+np.floor(d.lat/0.1).astype(int).astype(str)).values
    A=d[AB].values; A=A/np.linalg.norm(A,axis=1,keepdims=True)
    S=(d[SB].values-mu)/sd
    R[k]=dict(y=d.lc.values,g=g,AEF=A,S2=S,n=len(d))
def probe(): return LogisticRegression(max_iter=3000,C=1.0)
def kappa(X):
    U=X/np.linalg.norm(X,axis=1,keepdims=True); r=np.linalg.norm(U.mean(0)); d=X.shape[1]
    return r*(d-r*r)/max(1-r*r,1e-9)
def energy(X,Y,m=400,s=0):
    rs=np.random.RandomState(s); a=X[rs.choice(len(X),min(m,len(X)),False)]; b=Y[rs.choice(len(Y),min(m,len(Y)),False)]
    f=lambda P,Q: np.sqrt(((P[:,None,:]-Q[None,:,:])**2).sum(-1)).mean()
    return 2*f(a,b)-f(a,a)-f(b,b)
def stats(X,Y):
    Ux=X/np.linalg.norm(X,axis=1,keepdims=True); Uy=Y/np.linalg.norm(Y,axis=1,keepdims=True)
    cx,cy=Ux.mean(0),Uy.mean(0)
    cos=float(cx@cy/(np.linalg.norm(cx)*np.linalg.norm(cy)))
    kr=abs(np.log(kappa(X)/kappa(Y)))
    mmd=float(np.linalg.norm(X.mean(0)-Y.mean(0)))
    ed=energy(X,Y)
    Z=np.vstack([X,Y]); t=np.r_[np.zeros(len(X)),np.ones(len(Y))]
    rs=np.random.RandomState(0); idx=rs.permutation(len(Z)); h=len(Z)//2
    m=probe().fit(Z[idx[:h]],t[idx[:h]]); auc=roc_auc_score(t[idx[h:]],m.predict_proba(Z[idx[h:]])[:,1])
    return dict(cos_dist=1-cos,kappa_ratio=kr,mmd_lin=mmd,energy=ed,dom_auc=auc)
INR={}
print('== per-region (n, class counts, in-region 5-block-fold CV acc mean+-sd) ==')
for k,v in R.items():
    cc=dict(sorted(pd.Series(v['y']).value_counts().items()))
    line=[k,f"n={v['n']}",str(cc)]
    for sp in ['AEF','S2']:
        cv=cross_val_score(probe(),v[sp],v['y'],groups=v['g'],cv=GroupKFold(5))
        INR[(k,sp)]=cv.mean(); line.append(f"{sp}={cv.mean():.3f}+-{cv.std():.3f}")
    print(' | '.join(line))
rows=[]
for a,b in itertools.permutations(R.keys(),2):
    r={'src':a,'tgt':b}
    for sp in ['AEF','S2']:
        m=probe().fit(R[a][sp],R[a]['y'])
        tr=(m.predict(R[b][sp])==R[b]['y']).mean()
        r[sp+'_tacc']=tr; r[sp+'_drop']=INR[(a,sp)]-tr
        for kk,vv in stats(R[a][sp],R[b][sp]).items(): r[f'{sp}_{kk}']=vv
    rows.append(r)
P=pd.DataFrame(rows); P.to_csv('TC03_pairs.csv',index=False)
print(f'\n== n_pairs={len(P)}  mean drop AEF={P.AEF_drop.mean():.3f} S2={P.S2_drop.mean():.3f} '
      f'| median AEF={P.AEF_drop.median():.3f} S2={P.S2_drop.median():.3f} ==')
print('stat            rho(AEF stat,AEF drop) p     rho(S2 stat,S2 drop) p     rho(S2 stat,AEF drop)')
for s in ['cos_dist','kappa_ratio','mmd_lin','energy','dom_auc']:
    r1,p1=spearmanr(P['AEF_'+s],P.AEF_drop); r2,p2=spearmanr(P['S2_'+s],P.S2_drop); r3,_=spearmanr(P['S2_'+s],P.AEF_drop)
    print(f'{s:14s}  {r1:+.3f} (p={p1:.4f})   {r2:+.3f} (p={p2:.4f})   {r3:+.3f}')
print('\ncorr(AEF_drop,S2_drop) spearman=%.3f'%spearmanr(P.AEF_drop,P.S2_drop)[0])
