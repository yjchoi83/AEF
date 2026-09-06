import sys; sys.path.insert(0,'scratch')
from aefkit import *
WC = ee.Image("ESA/WorldCover/v200/2021").select('Map')
ROIS = {'BRamz':[-55.5,-9.0,-55.0,-8.5],'CGkasai':[21.0,-5.0,21.5,-4.5],'INpunjab':[75.5,30.5,76.0,31.0],
 'USiowa':[-93.5,42.0,-93.0,42.5],'ESduero':[-4.5,41.5,-4.0,42.0],'SNsahel':[-15.5,14.5,-15.0,15.0],
 'AUnsw':[147.0,-33.0,147.5,-32.5],'ZAhveld':[26.5,-26.5,27.0,-26.0]}
PER=300
out=[]
for k,b in ROIS.items():
    roi=ee.Geometry.Rectangle(b)
    y=WC.remap([10,20,30,40],[1,1,0,0]).rename('y')
    stack=aef(2021,roi).addBands(s2(2021,roi)).addBands(y)
    pts=y.stratifiedSample(numPoints=PER,classBand='y',region=roi,scale=10,seed=7,
        classValues=[0,1],classPoints=[PER,PER],geometries=True,dropNulls=True,tileScale=4)
    pl=pts.toList(2*PER)
    for c0 in range(0,2*PER,200):
        fc=ee.FeatureCollection(pl.slice(c0,min(c0+200,2*PER)))
        try:
            rows=stack.sampleRegions(collection=fc,scale=10,geometries=True,tileScale=4).getInfo()['features']
        except Exception as e:
            print(k,c0,'ERR',str(e)[:70],flush=True); continue
        for r in rows:
            d=dict(r['properties']); c=r['geometry']['coordinates']
            d['lon'],d['lat'],d['roi']=c[0],c[1],k; out.append(d)
    print(k,'cum',len(out),flush=True)
df=pd.DataFrame(out); df.to_csv('scratch/tc03_samples.csv',index=False)
print(df.shape); print(df.groupby('roi').y.agg(['size','mean']).round(3).to_string())
