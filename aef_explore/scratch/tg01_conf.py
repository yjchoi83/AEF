import sys, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
sys.path.insert(0,'scratch')
AEF=[f"A{i:02d}" for i in range(64)]; S2=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
df=pd.read_csv('scratch/tg01_samples.csv').dropna(subset=AEF+S2+['tmf'])
df=df[df.tmf>0].copy()
df['y']=df.tmf.map(lambda c:{1:0,2:1,3:2}.get(int(c),3))   # 0 undist,1 degraded,2 deforested,3 other
LON=df.lon.values
TR=df[LON<-55.10]; POOL=df[LON>=-55.00].copy()             # >=11 km gap train|pool
def conf(sc_cal,ycal,sc_te,yte,K,alpha,mondrian):
    n=len(ycal)
    if mondrian:
        q=np.array([np.quantile(sc_cal[ycal==k,k] if (ycal==k).sum()>0 else np.array([1.0]),
            min(1.0,np.ceil((max((ycal==k).sum(),1)+1)*(1-alpha))/max((ycal==k).sum(),1)),
            method='higher') for k in range(K)])
        inset=sc_te<=q[None,:]
    else:
        s=sc_cal[np.arange(n),ycal]
        qq=np.quantile(s,min(1.0,np.ceil((n+1)*(1-alpha))/n),method='higher')
        inset=sc_te<=qq
    cov=inset[np.arange(len(yte)),yte].mean(); size=inset.sum(1).mean()
    cc=[round(float(inset[yte==k,k].mean()),3) if (yte==k).sum()>5 else None for k in range(K)]
    return float(cov),float(size),cc
def run(feats,tag):
    K=4
    m=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,C=1.0)).fit(TR[feats].values,TR.y.values)
    P=m.predict_proba(POOL[feats].values); S=1.0-P; Y=POOL.y.values; lon=POOL.lon.values; lat=POOL.lat.values
    # regime B: 4 spatially separated calib/test splits (>=11 km gap band dropped)
    splits=[]
    for cut,ax in [(-54.70,'lon'),(-54.60,'lon'),(-11.60,'lat'),(-11.40,'lat')]:
        v = lon if ax=='lon' else lat
        c=v< cut-0.05; t=v> cut+0.05
        if c.sum()>200 and t.sum()>200: splits.append((c,t))
    for mond in [False,True]:
        for a in [0.10,0.20]:
            rb=[conf(S[c],Y[c],S[t],Y[t],K,a,mond) for c,t in splits]
            # regime A: random split matched to each spatial split's calib/test sizes
            ra=[]
            for i,(c,t) in enumerate(splits):
                rng=np.random.default_rng(100+i); idx=rng.permutation(len(Y))
                ci=idx[:c.sum()]; ti=idx[c.sum():c.sum()+t.sum()]
                ra.append(conf(S[ci],Y[ci],S[ti],Y[ti],K,a,mond))
            for nm,r in [('rand',ra),('spat',rb)]:
                cv=np.array([x[0] for x in r]); sz=np.array([x[1] for x in r])
                print(f"{tag} mond={int(mond)} a={a:.2f} {nm} cov={cv.mean():.3f}(sd{cv.std():.3f}) "
                      f"size={sz.mean():.2f} ccov={r[0][2]} nfold={len(r)}",flush=True)
    print(f"{tag} nTR={len(TR)} nPOOL={len(POOL)} calib~{splits[0][0].sum()} test~{splits[0][1].sum()}")
print('classbal(pool)',POOL.y.value_counts(normalize=True).round(3).to_dict())
run(AEF,'AEF64'); run(S2,'S2comp')
