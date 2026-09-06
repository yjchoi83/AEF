import ee, sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
ee.Initialize(project='alpha-earth-app')
TAG=sys.argv[1]; box=[float(v) for v in sys.argv[2:6]]; Y=int(sys.argv[6]); NP=int(sys.argv[7])
roi=ee.Geometry.Rectangle(box); geo='sa_' if TAG=='BR' else 'africa_'
AEF=ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
aef=lambda y: AEF.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).mosaic()
radd=ee.ImageCollection('projects/radar-wur/raddalert/v1').filterMetadata('layer','contains','alert')\
      .filter(ee.Filter.stringContains('system:index',geo)).sort('system:time_end',False).first()
A,D=radd.select('Alert'),radd.select('Date')
gfc=ee.Image('UMD/hansen/global_forest_change_2025_v1_13'); tc,ly=gfc.select('treecover2000'),gfc.select('lossyear')
doy=D.subtract((Y-2000)*1000)
mon=doy.subtract(1).divide(30.5).floor().add(1).clamp(1,12).toInt()
clr=A.eq(3).And(doy.gte(1)).And(doy.lte(366)).And(tc.gt(50)).And(ly.eq(Y-2000))
stable=tc.gt(80).And(ly.unmask(0).eq(0)).And(A.unmask(0).eq(0))
clr=clr.unmask(0); stable=stable.unmask(0)
cls=mon.updateMask(clr).unmask(0).updateMask(clr.Or(stable)).rename('cls')
pts=cls.stratifiedSample(numPoints=NP,classBand='cls',region=roi,scale=10,seed=7,
      classValues=list(range(13)),classPoints=[NP*2]+[NP]*12,tileScale=16,geometries=True)
pts=pts.map(lambda f: f.set('lon',f.geometry().coordinates().get(0),'lat',f.geometry().coordinates().get(1)))
def dots(a,b,n): return a.multiply(b).reduce(ee.Reducer.sum()).rename(n)
e0,e1,e2=aef(Y-1),aef(Y),aef(Y+1)
E=dots(e0,e2,'uv').addBands(dots(e0,e1,'x')).addBands(dots(e1,e2,'yy'))
a1=E.sampleRegions(pts,['cls','lon','lat'],scale=10,tileScale=16).getInfo()['features']
dA=pd.DataFrame([f['properties'] for f in a1]); print('AEF n',len(dA))
def s2(y):
    c=ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate(f'{y}-01-01',f'{y+1}-01-01')\
      .filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',40))
    def m(i):
        s=i.select('SCL'); k=s.neq(3).And(s.neq(8)).And(s.neq(9)).And(s.neq(10)).And(s.neq(1))
        return i.updateMask(k).select(['B2','B3','B4','B8','B11','B12']).divide(10000)
    md=c.map(m).median()
    return md.addBands(md.normalizedDifference(['B8','B4']).rename('NDVI'))\
             .rename([f'{b}_{y}' for b in ['B2','B3','B4','B8','B11','B12','NDVI']])
dS=None
for y in (Y-1,Y,Y+1):
    r=s2(y).sampleRegions(pts,['lon','lat'],scale=10,tileScale=16).getInfo()['features']
    t=pd.DataFrame([f['properties'] for f in r]); print('S2',y,'n',len(t))
    dS=t if dS is None else dS.merge(t,on=['lon','lat'],how='inner')
df=dA.merge(dS,on=['lon','lat'],how='inner').dropna(); print('merged n',len(df))
def wres(uv,x,y):
    c=np.clip(uv,-1,1); tot=np.arccos(c); w=np.arccos(np.clip(x,-1,1))/np.maximum(tot,1e-9)
    inpl=(x**2-2*x*y*c+y**2)/np.maximum(1-c**2,1e-9)
    return w,tot,np.sqrt(np.maximum(0,1-inpl))
df['w'],df['sep'],df['res']=wres(df.uv.values,df.x.values,df.yy.values)
B=['B2','B3','B4','B8','B11','B12','NDVI']; V={y:df[[f'{b}_{y}' for b in B]].values for y in (Y-1,Y,Y+1)}
al=np.vstack(list(V.values())); mu,sd=al.mean(0),al.std(0)+1e-9
for y in V: Z=(V[y]-mu)/sd; V[y]=Z/np.linalg.norm(Z,axis=1,keepdims=True)
df['s_uv']=(V[Y-1]*V[Y+1]).sum(1); df['s_x']=(V[Y-1]*V[Y]).sum(1); df['s_y']=(V[Y]*V[Y+1]).sum(1)
df['w_s2'],df['sep_s2'],df['res_s2']=wres(df.s_uv.values,df.s_x.values,df.s_y.values)
df['blk']=np.floor(df.lon/0.1).astype(int).astype(str)+'_'+np.floor(df.lat/0.1).astype(int).astype(str)
df.to_csv(f'TB01_{TAG}{Y}.csv',index=False)
d=df[df.cls>0]; s=df[df.cls==0]
print(f'== {TAG}{Y} n_clear={len(d)} n_stable={len(s)} blocks={df.blk.nunique()}')
print('sep_deg AEF clear %.1f stable %.1f | S2 clear %.1f stable %.1f'%(np.degrees(d.sep.mean()),
  np.degrees(s.sep.mean()),np.degrees(d.sep_s2.mean()),np.degrees(s.sep_s2.mean())))
for nm,wc in (('AEF','w'),('S2 ','w_s2')):
    r,p=spearmanr(d.cls,d[wc]); ex=(12-d.cls)/12.0
    print(f'{nm} rho(month,w)={r:.3f} p={p:.1e} pearson(w,(12-m)/12)={np.corrcoef(d[wc],ex)[0,1]:.3f} MAE={np.abs(d[wc]-ex).mean():.3f}')
    print(d.groupby('cls')[wc].agg(['count','mean','std']).round(3).T.to_string())
print('resid AEF mean %.3f p90 %.3f | stable %.3f | S2 clear %.3f'%(d.res.mean(),d.res.quantile(.9),s.res.mean(),d.res_s2.mean()))
bl=[spearmanr(sb.cls,sb.w)[0] for _,sb in d.groupby('blk') if len(sb)>=25 and sb.cls.nunique()>=5]
if bl: bl=np.array(bl); print('block rho n=%d mean=%.3f sd=%.3f min=%.3f max=%.3f'%(len(bl),bl.mean(),bl.std(),bl.min(),bl.max()))
