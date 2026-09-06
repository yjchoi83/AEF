import numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import r2_score
YS=list(range(2020,2026))
d=pd.read_csv('scratch/te02_panel.csv')
try: s2=pd.read_csv('scratch/te02_s2.csv',index_col=0); HAVE=True
except Exception: HAVE=False
print("HAVE_S2",HAVE)
d['pid']=np.arange(len(d)); d['blk']=(np.floor(d.lon/0.1).astype(int).astype(str)+'_'+np.floor(d.lat/0.1).astype(int).astype(str))
L=[]
for y in YS:
    t=d[['pid','roi','blk','lon','lat']].copy(); t['yr']=y
    t['drift']=d[f'a{y}']; t['s1']=d[f's1_{y}']+d[f's1_{y-1}']; t['s2c']=d[f's2_{y}']+d[f's2_{y-1}']
    t['ds1']=(d[f's1_{y}']-d[f's1_{y-1}']).abs(); t['ds2']=(d[f's2_{y}']-d[f's2_{y-1}']).abs()
    t['dpz']=d[f'pz{y}']-d[f'pz{y-1}']; t['dtz']=d[f'tz{y}']-d[f'tz{y-1}']; t['pz']=d[f'pz{y}']
    if HAVE: t['sdrift']=s2.reindex(d.index)[f'sa{y}'].values
    L.append(t)
p=pd.concat(L,ignore_index=True).dropna(subset=['drift','dpz','s1','s2c'])
p['adpz']=p.dpz.abs(); p['adtz']=p.dtz.abs()
COLS=['drift','sdrift'] if HAVE else ['drift']
print("n pixel-years",len(p),"px",p.pid.nunique())
p['cls']=pd.cut(p.dpz,[-9,-1,-0.5,0.5,1,9],labels=['onset','drying','stable','wetting','break'])
for c in COLS:
    x=p.dropna(subset=[c])
    print("\n==",c,"by dpz class ==")
    print(x.groupby('cls',observed=True)[c].agg(n='size',med='median',q25=lambda s:s.quantile(.25),q75=lambda s:s.quantile(.75)).round(2))
    print(x.pivot_table(index='roi',columns='cls',values=c,aggfunc='median',observed=True).round(2))
for c in COLS: p[c+'_w']=p[c]-p.groupby('pid')[c].transform('mean')
p['ls1']=np.log1p(p.s1); p['ls2']=np.log1p(p.s2c); p['lds1']=np.log1p(p.ds1); p['lds2']=np.log1p(p.ds2)
OBS=['ls1','ls2','lds1','lds2']; CLM=['dpz','dtz','adpz','adtz']
def pr2(tgt,base,add,k=5):
    x=p.dropna(subset=[tgt]+base+add); g=x.blk.values
    def sc(f):
        s=[]
        for tr,te in GroupKFold(n_splits=k).split(x,groups=g):
            m=Ridge(1.0).fit(x[f].values[tr],x[tgt].values[tr]); s.append(r2_score(x[tgt].values[te],m.predict(x[f].values[te])))
        return float(np.mean(s)),float(np.std(s))
    r0,_=sc(base); r1,s1=sc(base+add); return round(r0,3),round(r1,3),round(max(0,(r1-r0)/(1-r0)),3),round(s1,3)
for c in [x+'_w' for x in COLS]:
    print("\n==",c,"partial R2 (5 block folds) =="); print("  obs->+clim:",pr2(c,OBS,CLM),"  clim->+obs:",pr2(c,CLM,OBS))
    for roi,g in p.groupby('roi'):
        gg=g.dropna(subset=[c])
        def r(f):
            s=[]
            for tr,te in GroupKFold(n_splits=3).split(gg,groups=gg.blk.values):
                m=Ridge(1.0).fit(gg[f].values[tr],gg[c].values[tr]); s.append(r2_score(gg[c].values[te],m.predict(gg[f].values[te])))
            return round(float(np.mean(s)),3)
        print("   ",roi,"obs",r(OBS),"clim",r(CLM),"all",r(OBS+CLM))
print("\n== FPR: threshold from |dpz|<0.5 pixel-years (5% nominal), tested on |dpz|>=1 ==")
for c in COLS:
    print("--",c)
    for roi,g in p.groupby('roi'):
        g=g.dropna(subset=[c]); nd=g[g.adpz<0.5]; dr=g[g.adpz>=1.0]
        if len(nd)<100 or len(dr)<50: print("   ",roi,"n_nd",len(nd),"n_dr",len(dr),"SKIP"); continue
        th=nd[c].quantile(.95); f0=(dr[c]>th).mean()
        m=LinearRegression().fit(g[CLM],g[c]); res=g[c]-m.predict(g[CLM])
        th2=res[g.adpz<0.5].quantile(.95); f1=(res[g.adpz>=1.0]>th2).mean()
        print(f"    {roi} th={th:.2f} FPR={f0:.3f} -> corrected {f1:.3f} (n_nd={len(nd)},n_dr={len(dr)})")
