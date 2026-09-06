import sys, json, numpy as np, pandas as pd
MONTHS=[(2020,12),(2021,1),(2021,2),(2021,3),(2021,4),(2021,5),(2021,6),(2021,7),
        (2021,8),(2021,9),(2021,10),(2021,11),(2021,12),(2022,1)]
NDVI_MIN,NBR_MIN=0.10,0.05

def breakpoint(row, var):
    vals=np.array([row[f'{var}_{y}{m:02d}'] for y,m in MONTHS])
    cnt=np.array([row[f'cnt_{y}{m:02d}'] for y,m in MONTHS])
    best_b,best_drop=None,-9
    for b in range(1,13):  # idx b = calendar month b of 2021 (idx1=Jan..idx12=Dec)
        pre=vals[:b][cnt[:b]>0]; post=vals[b:][cnt[b:]>0]
        if len(pre)<2 or len(post)<2: continue
        drop=pre.mean()-post.mean()
        if drop>best_drop: best_drop,best_b=drop,b
    minmag=NDVI_MIN if var=='ndvi' else NBR_MIN
    if best_b is None or best_drop<minmag: return np.nan, best_drop if best_drop>-9 else np.nan
    return best_b, best_drop

def load(tag):
    cl=pd.read_csv(f'G1_{tag}_clear_sub.csv')
    mo=pd.read_csv(f'G1_{tag}_monthly.csv')
    st=pd.read_csv(f'G1_{tag}_stable.csv')
    d=cl.merge(mo, on=['lon','lat'], suffixes=('','_m'))
    d=d[d['cls']==d['cls_m']] if 'cls_m' in d else d
    d['b_ndvi'],d['drop_ndvi']=zip(*d.apply(lambda r: breakpoint(r,'ndvi'), axis=1))
    d['b_nbr'],d['drop_nbr']=zip(*d.apply(lambda r: breakpoint(r,'nbr'), axis=1))
    d['unresolved']=d['b_ndvi'].isna()
    d['n_clear_2021']=sum((d[f'cnt_2021{m:02d}']>0).astype(int) for m in range(1,13))
    d['m_indep']=d['b_ndvi']
    thr=np.degrees(st['sep_stable']).quantile(0.90)
    return d, thr

def wres_fit(d, mcol):
    dd=d.dropna(subset=[mcol,'w']).copy()
    ex=(12-dd[mcol])/12.0
    X=np.column_stack([np.ones(len(dd)),ex]); Y=dd['w'].values
    coef,_,_,_=np.linalg.lstsq(X,Y,rcond=None)
    return coef[0],coef[1],dd

def boot_ci(d, mcol, blk, n=500):
    blocks=blk.unique(); out=[]
    for _ in range(n):
        bs=np.random.choice(blocks,len(blocks),replace=True)
        idx=np.concatenate([np.where(blk==b)[0] for b in bs])
        sub=d.iloc[idx]
        if sub[mcol].notna().sum()<10: continue
        a,b,_=wres_fit(sub,mcol)
        out.append((a,b))
    out=np.array(out)
    return np.percentile(out[:,0],[2.5,97.5]), np.percentile(out[:,1],[2.5,97.5])

def report(tag,d,thr):
    print(f'\n=== {tag} thr(p90 stable, deg)={thr:.2f} n_clear={len(d)} unresolved={d.unresolved.sum()} ({100*d.unresolved.mean():.1f}%)')
    agree=(d.dropna(subset=['b_ndvi','b_nbr']))
    if len(agree): print('NDVI/NBR exact agree %.1f%%  within1 %.1f%%  n=%d'%(
        (agree.b_ndvi==agree.b_nbr).mean()*100,(agree.b_ndvi-agree.b_nbr).abs().le(1).mean()*100,len(agree)))
    for label,mcol in [('OLD(RADD cls)','cls'),('NEW(indep m_indep)','m_indep')]:
        a,b,dd=wres_fit(d,mcol)
        (a_lo,a_hi),(b_lo,b_hi)=boot_ci(dd,mcol,dd['blk'],n=300)
        print(f'{label}: a={a:.3f} [{a_lo:.3f},{a_hi:.3f}] b={b:.3f} [{b_lo:.3f},{b_hi:.3f}] resid_mean={dd.res.mean():.3f} resid_p90={dd.res.quantile(.9):.3f} n={len(dd)}')
        dec=d[d[mcol]==12]
        print(f'  Dec-shift n={len(dec)} mean ang(e{{Y-1}},eY) deg = %.1f'%(np.degrees(np.arccos(dec.x.clip(-1,1))).mean() if len(dec) else np.nan))
        d2=d.dropna(subset=[mcol]).copy(); d2['ang_deg']=np.degrees(np.arccos(d2.x.clip(-1,1)))
        d2['flag']=d2.ang_deg>=thr; d2['q']=((d2[mcol]-1)//3+1).astype(int)
        print('  detection rate by quarter:', d2.groupby('q')['flag'].mean().round(3).to_dict(),
              'overall %.1f%%'%(100*d2.flag.mean()))
    diff=d.dropna(subset=['m_indep'])['cls']-d.dropna(subset=['m_indep'])['m_indep']
    print('RADD-indep month diff: median=%.1f IQR=[%.1f,%.1f] frac>=2mo late=%.1f%% n=%d'%(
        diff.median(),diff.quantile(.25),diff.quantile(.75),100*(diff>=2).mean(),len(diff)))
    d['obs_tercile']=pd.qcut(d['n_clear_2021'],3,labels=['low','mid','high'],duplicates='drop')
    for t,sub in d.groupby('obs_tercile'):
        if len(sub)<20: continue
        a,b,dd=wres_fit(sub,'m_indep')
        print(f'  tercile={t} n={len(sub)} unresolved%%={100*sub.unresolved.mean():.1f} a={a:.3f} b={b:.3f}')
    return d

if __name__=='__main__':
    for tag in ['BR','CG']:
        d,thr=load(tag)
        d=report(tag,d,thr)
        d.to_csv(f'G1_{tag}_final.csv',index=False)
