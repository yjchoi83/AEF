import sys; sys.path.insert(0,'scratch')
from aefkit import *
import numpy as np, pandas as pd
Y=2021
C=ee.ImageCollection('projects/radar-wur/raddalert/v1')
wk=[i for i in C.aggregate_array('system:index').getInfo() if i.startswith('sa_') and len(i)==11]
last=sorted(wk)[-1]; print('RADD image:',last)
al=ee.Image('projects/radar-wur/raddalert/v1/'+last)
H=ee.Image('UMD/hansen/global_forest_change_2025_v1_13')
tc=H.select('treecover2000'); ly=H.select('lossyear').unmask(0)
d=al.select('Date').unmask(0); conf=al.select('Alert').unmask(0)
yy=d.divide(1000).floor(); doy=d.mod(1000)
mon=ee.Image(1)
for t in [31,59,90,120,151,181,212,243,273,304,334]: mon=mon.add(doy.gt(t))
ev=mon.updateMask(yy.eq(Y-2000).And(conf.eq(3)).And(ly.eq(0).Or(ly.eq(Y-2000))))
stab=ee.Image(0).updateMask(d.eq(0).And(ly.eq(0)))
lab=ev.unmask(stab,False).rename('m').toInt().updateMask(tc.gt(50))
def pull(img,fc):
    r=img.sampleRegions(collection=fc,scale=10,geometries=True,tileScale=8).getInfo()['features']
    o=[]
    for f in r:
        p=dict(f['properties']); c=f['geometry']['coordinates']; p['lon'],p['lat']=c[0],c[1]; o.append(p)
    return pd.DataFrame(o)
df=None
for box,npc in [([-55.4,-6.4,-54.6,-5.6],180),([-55.3,-6.3,-54.9,-5.9],120)]:
    roi=ee.Geometry.Rectangle(box)
    try:
        fc=lab.stratifiedSample(numPoints=npc,classBand='m',region=roi,scale=10,seed=7,
            classValues=list(range(13)),classPoints=[npc]*13,geometries=True,dropNulls=True,tileScale=8)
        A=[aef(y,roi).rename([f"{k}{b}" for b in AEF_BANDS]) for k,y in zip('pyq',[Y-1,Y,Y+1])]
        A+= [angle(Y-1,Y,roi).rename('aY'),angle(Y,Y+1,roi).rename('aY1'),
             angle(Y-1,Y+1,roi).rename('aPP'),angle(Y-2,Y-1,roi).rename('aRef')]
        df=pull(ee.Image.cat(A),fc); print('ROI',box,'n',len(df))
        S=[s2(y,roi).select(['B4','B8','B11','NDVI','NBR']).rename([f"s{k}_{b}" for b in ['B4','B8','B11','NDVI','NBR']]) for k,y in zip('pyq',[Y-1,Y,Y+1])]
        s2c=(ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f"{Y}-01-01",f"{Y+1}-01-01")
             .filterBounds(roi).map(lambda i:i.updateMask(i.select('QA60').bitwiseAnd(1<<10|1<<11).eq(0))))
        S+=[s2c.select('B8').count().rename('n_s2')]
        ds=pull(ee.Image.cat(S),fc)
        df=df.merge(ds[[c for c in ds.columns if c.startswith('s') or c in ('n_s2','lon','lat')]],on=['lon','lat'],how='left')
        break
    except Exception as e: print('FAIL',box,str(e)[:120])
df.to_csv('scratch/tb01_samples.csv',index=False)
print('n=',len(df),'cols=',df.shape[1]); print('class:',df.m.value_counts().sort_index().to_dict())
P=df[[f"p{b}" for b in AEF_BANDS]].values; Yv=df[[f"y{b}" for b in AEF_BANDS]].values; Q=df[[f"q{b}" for b in AEF_BANDS]].values
print('||e_Y|| mean %.4f'%float(np.nanmean(np.linalg.norm(Yv,axis=1))))
ok=~(np.isnan(P).any(1)|np.isnan(Yv).any(1)|np.isnan(Q).any(1))
df=df[ok].reset_index(drop=True); P,Yv,Q=P[ok],Yv[ok],Q[ok]
cpy=(P*Yv).sum(1); cpq=(P*Q).sum(1); cyq=(Yv*Q).sum(1); a_=np.full(len(P),np.nan)
for i in range(len(P)):
    G=np.array([[1.,cpq[i]],[cpq[i],1.]]); b=np.array([cpy[i],cyq[i]])
    try:
        s=np.linalg.solve(G,b)
        if s.sum()!=0: a_[i]=s[1]/s.sum()
    except Exception: pass
df['cos_pY'],df['cos_pq'],df['cos_Yq'],df['alpha']=cpy,cpq,cyq,a_
df.to_csv('scratch/tb01_samples.csv',index=False)
e=df[df.m>0]; st=df[df.m==0]
print(e.groupby('m').agg(n=('m','size'),cos_pY=('cos_pY','mean'),cos_Yq=('cos_Yq','mean'),
      alpha=('alpha','mean'),aY=('aY','mean'),aY1=('aY1','mean'),ns2=('n_s2','median')).round(3).to_string())
print('STABLE n=%d cos_pY=%.3f alpha=%.3f aY=%.2f aRef=%.2f cos_pq=%.3f'%(len(st),st.cos_pY.mean(),
      np.nanmean(st.alpha),st.aY.mean(),st.aRef.mean(),st.cos_pq.mean()))
from scipy.stats import spearmanr,pearsonr
w=(12-e.m)/12.0; g=e.dropna(subset=['alpha'])
print('spearman(m,cos_pY)=%.3f spearman(m,alpha)=%.3f'%(spearmanr(e.m,e.cos_pY).statistic,spearmanr(g.m,g.alpha).statistic))
print('pearson(alpha,(12-m)/12)=%.3f slope=%.3f intercept=%.3f'%(pearsonr(g.alpha,(12-g.m)/12).statistic,
      *np.polyfit((12-g.m)/12,g.alpha,1)))
