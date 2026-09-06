import ee, sys, numpy as np, pandas as pd
ee.Initialize()
TAG=sys.argv[1]; box=[float(v) for v in sys.argv[2:6]]; Y=2021
roi=ee.Geometry.Rectangle(box)
AEF=ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
aef=lambda y: AEF.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).mosaic()
gfc=ee.Image('UMD/hansen/global_forest_change_2025_v1_13')
tc,ly=gfc.select('treecover2000'),gfc.select('lossyear')
radd=ee.ImageCollection('projects/radar-wur/raddalert/v1').filterMetadata('layer','contains','alert')\
  .filter(ee.Filter.stringContains('system:index','sa_' if TAG=='BR' else 'africa_')).sort('system:time_end',False).first()
A=radd.select('Alert').unmask(0)
stable=tc.gt(80).And(ly.unmask(0).eq(0)).And(A.eq(0)).unmask(0)
# 300 stable points
stpts=stable.rename('cls').stratifiedSample(numPoints=300,classBand='cls',region=roi,scale=10,seed=11,
      classValues=[0,1],classPoints=[0,300],tileScale=16,geometries=True)
stpts=stpts.map(lambda f: f.set('lon',f.geometry().coordinates().get(0),'lat',f.geometry().coordinates().get(1),'cls',0))
def dot(a,b,n): return a.multiply(b).reduce(ee.Reducer.sum()).rename(n)
e0,e1=aef(Y-1),aef(Y)
ang=dot(e0,e1,'x').clamp(-1,1).acos().rename('sep_stable')
st=ang.sampleRegions(stpts,['lon','lat','cls'],scale=10,tileScale=16).getInfo()['features']
dS=pd.DataFrame([f['properties'] for f in st])
dS.to_csv(f'G1_{TAG}_stable.csv',index=False)
print(TAG,'stable n',len(dS))

# clearing subsample points (already picked, 480/region) -> build FeatureCollection
cl=pd.read_csv(f'G1_{TAG}_clear_sub.csv')
feats=[ee.Feature(ee.Geometry.Point([r.lon,r.lat]),{'lon':r.lon,'lat':r.lat,'cls':int(r.cls)}) for _,r in cl.iterrows()]
clpts=ee.FeatureCollection(feats)
allpts=clpts.merge(stpts.select(['lon','lat','cls']))

def scl_mask(i):
    s=i.select('SCL')
    k=s.neq(3).And(s.neq(8)).And(s.neq(9)).And(s.neq(10)).And(s.neq(1))
    return i.updateMask(k)

months=[]
d=pd.Timestamp('2020-12-01')
while d<=pd.Timestamp('2022-01-01'):
    months.append((d.year,d.month)); d=d+pd.DateOffset(months=1)

bands=[]
for (yy,mm) in months:
    start=f'{yy}-{mm:02d}-01'
    nxt=pd.Timestamp(start)+pd.DateOffset(months=1)
    end=nxt.strftime('%Y-%m-%d')
    col=(ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate(start,end).filterBounds(roi)
         .map(scl_mask))
    cnt=col.select('B8').count().unmask(0).rename(f'cnt_{yy}{mm:02d}')
    m=col.select(['B4','B8','B11','B12']).median()
    ndvi=m.normalizedDifference(['B8','B4']).unmask(-9).rename(f'ndvi_{yy}{mm:02d}')
    nbr=m.normalizedDifference(['B8','B12']).unmask(-9).rename(f'nbr_{yy}{mm:02d}')
    bands+=[ndvi,nbr,cnt]
stack=ee.Image.cat(bands)
out=stack.sampleRegions(allpts,['lon','lat','cls'],scale=20,tileScale=16).getInfo()['features']
df=pd.DataFrame([f['properties'] for f in out])
df.to_csv(f'G1_{TAG}_monthly.csv',index=False)
print(TAG,'monthly stack n',len(df),'cols',len(df.columns))
