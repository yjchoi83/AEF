import numpy as np, pandas as pd, sys
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import r2_score
YS=list(range(2019,2026))
d=pd.read_csv('scratch/te02_panel.csv')
try: s2=pd.read_csv('scratch/te02_s2.csv',index_col=0); HAVE_S2=True
except Exception: HAVE_S2=False
d['pid']=np.arange(len(d)); d['blk']=(np.floor(d.lon/0.1).astype(int).astype(str)+'_'+np.floor(d.lat/0.1).astype(int).astype(str))
L=[]
for y in YS:
    t=d[['pid','roi','blk','lon','lat']].copy(); t['yr']=y
    t['drift']=d[f'a{y}']; t['s1']=d[f's1_{y}']; t['s2c']=d[f's2_{y}']
    t['pz']=d[f'pz{y}']; t['tz']=d[f'tz{y}']
    if HAVE_S2: t['sdrift']=s2.reindex(d.index)[f'sa{y}'].values
    L.append(t)
p=pd.concat(L,ignore_index=True).dropna(subset=['drift','pz','s1','s2c'])
print("n pixel-years",len(p),"n pixels",p.pid.nunique(),"rois",p.roi.nunique())
p['dcls']=pd.cut(p.pz,[-9,-1.0,-0.5,0.5,9],labels=['severe','moderate','normal','wet'])
def q(g,c): return pd.Series({'n':len(g),'med':g[c].median(),'iqr':g[c].quantile(.75)-g[c].quantile(.25)})
for c in (['drift','sdrift'] if HAVE_S2 else ['drift']):
    print("\n==",c,"by drought class =="); print(p.groupby('dcls',observed=True).apply(q,c).round(2))
    print("-- by roi x class (median) --"); print(p.pivot_table(index='roi',columns='dcls',values=c,aggfunc='median',observed=True).round(2))
# within-pixel demeaning (pixel fixed effect)
for c in (['drift','sdrift'] if HAVE_S2 else ['drift']):
    p[c+'_w']=p[c]-p.groupby('pid')[c].transform('mean')
p['ls1']=np.log1p(p.s1); p['ls2']=np.log1p(p.s2c)
def pr2(tgt,base,add,grp):
    x=p.dropna(subset=[tgt]+base+add); g=x[grp].values
    def sc(f):
        s=[]
        for tr,te in GroupKFold(n_splits=5).split(x,groups=g):
            m=Ridge(1.0).fit(x[f].values[tr],x[tgt].values[tr]); s.append(r2_score(x[tgt].values[te],m.predict(x[f].values[te])))
        return np.mean(s),np.std(s)
    r0,_=sc(base); r1,s1_=sc(base+add)
    return round(r0,3),round(r1,3),round(max(0,(r1-r0)/(1-r0)),3),round(s1_,3)
for c in (['drift_w','sdrift_w'] if HAVE_S2 else ['drift_w']):
    print("\n==",c,"variance decomposition (5 spatial-block folds) ==")
    print(" obs-only R2, +clim R2, partial R2(clim|obs), sd:",pr2(c,['ls1','ls2'],['pz','tz'],'blk'))
    print(" clim-only R2, +obs R2, partial R2(obs|clim), sd:",pr2(c,['pz','tz'],['ls1','ls2'],'blk'))
    for roi,g in p.groupby('roi'):
        if len(g)<300: continue
        gg=g.dropna(subset=[c])
        def r2r(f):
            s=[]
            for tr,te in GroupKFold(n_splits=3).split(gg,groups=gg.blk.values):
                m=Ridge(1.0).fit(gg[f].values[tr],gg[c].values[tr]); s.append(r2_score(gg[c].values[te],m.predict(gg[f].values[te])))
            return np.mean(s)
        print("  ",roi,"obs",round(r2r(['ls1','ls2']),3),"clim",round(r2r(['pz','tz']),3),"all",round(r2r(['ls1','ls2','pz','tz']),3))
# FPR calibration on non-drought pixel-years, evaluated on drought pixel-years
print("\n== FPR (threshold = 95th pct of non-drought (pz>-0.5) drift, per ROI) ==")
for c in (['drift','sdrift'] if HAVE_S2 else ['drift']):
    print("--",c)
    for roi,g in p.groupby('roi'):
        g=g.dropna(subset=[c]); nd=g[g.pz>-0.5][c]; dr=g[g.pz<=-1.0][c]
        if len(nd)<100 or len(dr)<50: print("  ",roi,"n_nd",len(nd),"n_dr",len(dr),"skip"); continue
        th=nd.quantile(.95); fpr=(dr>th).mean()
        # correction: regress out climate on non-drought fit, apply to all
        X=g[['pz','tz']].values; m=LinearRegression().fit(g[g.pz>-0.5][['pz','tz']],nd)
        res=g[c]-m.predict(X)+nd.mean()
        th2=res[g.pz>-0.5].quantile(.95); fpr2=(res[g.pz<=-1.0]>th2).mean()
        print(f"   {roi} th={th:.2f} FPR_drought={fpr:.3f} -> after climate-regress-out {fpr2:.3f} (n_dr={len(dr)})")
