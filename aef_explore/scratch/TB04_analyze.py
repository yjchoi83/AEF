import json, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import balanced_accuracy_score
rows=json.load(open('TB04_rows.json')); YRS=list(range(2017,2026)); N=9
BL=['ndvi','nbr','b8','b11','b12']
ok=[r for r in rows if all('a%d_%d'%(i,j) in r and r['a%d_%d'%(i,j)] is not None for i in range(N) for j in range(i,N))
    and all(r.get('%s_%d'%(b,y)) is not None for y in YRS for b in BL)]
print('rows',len(rows),'complete',len(ok))
def gA(r):
    G=np.zeros((N,N))
    for i in range(N):
        for j in range(i,N): G[i,j]=G[j,i]=r['a%d_%d'%(i,j)]
    return G
X=np.array([[[r['%s_%d'%(b,y)] for b in BL] for y in YRS] for r in ok])  # n,9,5
mu=X.reshape(-1,5).mean(0); sd=X.reshape(-1,5).std(0); Xz=(X-mu)/sd
GA=np.array([gA(r) for r in ok]); GS=np.einsum('nyf,nzf->nyz',Xz,Xz)
def jumps(G): return np.array([G[:,i,i]+G[:,i+1,i+1]-2*G[:,i,i+1] for i in range(N-1)]).T  # n,8
def costbrk(G):
    sc=[]
    for k in range(1,N):
        s1=G[:,:k,:k].sum((1,2))/k; s2=G[:,k:,k:].sum((1,2))/(N-k); sc.append(s1+s2)
    return np.argmax(np.array(sc).T,1)+1   # index of first year of segment 2
def offplane1(g,m):
    p=max(m-1,0); q=min(m+1,N-1)
    A=np.array([[g[p,p],g[p,q]],[g[p,q],g[q,q]]]); b=np.array([g[p,m],g[q,m]])
    try: c=np.linalg.solve(A+1e-9*np.eye(2),b)
    except Exception: c=np.zeros(2)
    return np.sqrt(max(g[m,m]-c@b,0)/max(g[m,m],1e-9))
st=np.array([r['str'] for r in ok]); ry=np.array([r['refy'] for r in ok],float)
lon=np.array([r['lon'] for r in ok]); lat=np.array([r['lat'] for r in ok])
res={}
for tag,G in [('AEF',GA),('S2',GS)]:
    J=jumps(G); mj=np.argmax(J,1)+1; cb=costbrk(G)
    res[tag]=dict(J=J,mj=mj,cb=cb,mag=np.sqrt(J.max(1)))
NAME={1:'loss',2:'degrad',3:'regrow',4:'stableF',5:'stableNF'}
print('\n=== dating accuracy (detected break year = 2017+idx) ===')
for k in [1,2,3]:
    m=st==k; print('%s n=%d refyr med=%d'%(NAME[k],m.sum(),int(np.median(ry[m]))))
    for tag in ['AEF','S2']:
        for det in ['mj','cb']:
            dy=2017+res[tag][det][m]-ry[m]
            print('   %s-%s exact=%.3f pm1=%.3f bias=%+.2f'%(tag,det,(dy==0).mean(),(np.abs(dy)<=1).mean(),dy.mean()))
print('\n=== false alarm: max-jump magnitude, thr = stableF p90 ===')
for tag in ['AEF','S2']:
    thr=np.percentile(res[tag]['mag'][st==4],90)
    line=' '.join('%s=%.3f'%(NAME[k],(res[tag]['mag'][st==k]>thr).mean()) for k in [1,2,3,4,5])
    print(' %s thr=%.3f  detrate: %s'%(tag,thr,line))
print('\n=== 3-class type probe, GroupKFold 5 (0.1deg ~11km blocks) ===')
sel=np.isin(st,[1,2,3]); grp=(np.floor(lon[sel]*10)*1000+np.floor(lat[sel]*10)).astype(int)
y=st[sel]; print(' n=%d balance=%s blocks=%d'%(sel.sum(),np.bincount(y)[1:4].tolist(),len(set(grp))))
for tag in ['AEF','S2']:
    G=(GA if tag=='AEF' else GS)[sel]; J=res[tag]['J'][sel]; m=res[tag]['cb'][sel]
    F=[]
    for t in range(G.shape[0]):
        mm=m[t]; pre=J[t,:max(mm-1,1)].mean(); post=J[t,mm:].mean() if mm<N-1 else 0.0
        d08=G[t,0,0]+G[t,8,8]-2*G[t,0,8]; dpl=G[t,mm-1,mm-1]+G[t,8,8]-2*G[t,mm-1,8]
        F.append([pre,np.sqrt(max(J[t,mm-1],0)),post,d08,dpl,dpl-J[t,mm-1],mm,offplane1(G[t],mm)])
    F=np.array(F)
    sc=[]
    for tr,te in GroupKFold(5).split(F,y,grp):
        c=RandomForestClassifier(300,min_samples_leaf=5,random_state=0,n_jobs=4).fit(F[tr],y[tr])
        sc.append(balanced_accuracy_score(y[te],c.predict(F[te])))
    print(' %s bal-acc=%.3f +-%.3f  folds=%s'%(tag,np.mean(sc),np.std(sc),[round(s,3) for s in sc]))
