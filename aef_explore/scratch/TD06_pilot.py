import ee, json, numpy as np, sys
ee.Initialize(project='alpha-earth-app')
Y=2020
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
ETH=ee.Image("users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1").select([0],['eth'])
META=ee.ImageCollection("projects/meta-forest-monitoring-okw37/assets/CanopyHeight").mosaic().select([0],['meta'])
WC=ee.ImageCollection("ESA/WorldCover/v200").first().select('Map').rename('wc')
S2B=['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12']
def s2(roi):
    def msk(i):
        s=i.select('SCL'); ok=s.neq(3).And(s.neq(8)).And(s.neq(9)).And(s.neq(10)).And(s.neq(11)).And(s.neq(1))
        return i.updateMask(ok).divide(10000)
    c=ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi).map(msk)
    m=c.select(S2B).median()
    return m.addBands(m.normalizedDifference(['B8','B4']).rename('ndvi')), c.size()
def s1(roi):
    c=ee.ImageCollection("COPERNICUS/S1_GRD").filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi).filter(ee.Filter.eq('instrumentMode','IW'))
    return c.select(['VV','VH']).mean().rename(['vv','vh']), c.size()
BOX={'below':[9.0,48.5,12.0,50.8],'above':[13.0,56.0,16.0,58.3]}
out={}
for side,b in BOX.items():
    roi=ee.Geometry.Rectangle(b)
    aef=AEF.filterDate(f"{Y}-01-01",f"{Y+1}-01-01").filterBounds(roi).mosaic()
    S2,n2=s2(roi); S1,n1=s1(roi)
    stack=aef.addBands(ETH).addBands(META).addBands(WC).addBands(S2).addBands(S1)
    pts=ee.FeatureCollection.randomPoints(roi,5000,17)
    fc=stack.sampleRegions(collection=pts,scale=10,tileScale=16,geometries=True)
    rows=fc.getInfo()['features']
    out[side]={'rows':rows,'n_s2':n2.getInfo(),'n_s1':n1.getInfo()}
    print(side,'sampled',len(rows),'s2scenes',out[side]['n_s2'],'s1scenes',out[side]['n_s1'],flush=True)
json.dump({k:{'n_s2':v['n_s2'],'n_s1':v['n_s1'],'rows':[f['properties']|{'lon':f['geometry']['coordinates'][0],'lat':f['geometry']['coordinates'][1]} for f in v['rows']]} for k,v in out.items()},open('TD06_samples.json','w'))
print('saved')
