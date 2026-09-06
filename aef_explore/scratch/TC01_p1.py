import sys; sys.path.insert(0,'scratch')
from aefkit import *
Y=2021
R={'BR':[-55.5,-9.0,-54.5,-8.0],'CG':[21.0,-5.0,22.0,-4.0]}
wc=ee.Image("ESA/WorldCover/v200/2021").select('Map').rename('y')
dem=ee.ImageCollection("COPERNICUS/DEM/GLO30").mosaic().select('DEM').rename('elev')\
      .setDefaultProjection('EPSG:4326',None,30)
slp=ee.Terrain.slope(dem).rename('slope')
era=ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate(f'{Y}-01-01',f'{Y+1}-01-01')
tmp=era.select('temperature_2m').mean().rename('tmean')
prc=era.select('total_precipitation_sum').sum().rename('prec')
def rows(f):
    out=[]
    for r in f.getInfo()['features']:
        d=dict(r['properties']); c=r['geometry']['coordinates']
        d['lon'],d['lat']=c[0],c[1]; out.append(d)
    return pd.DataFrame(out)
for nm,b in R.items():
    roi=ee.Geometry.Rectangle(b)
    pts=wc.stratifiedSample(region=roi,classBand='y',scale=10,seed=1,numPoints=0,
        classValues=[10,20,30],classPoints=[600,600,600],geometries=True,dropNulls=True)
    stack=(aef(Y,roi).addBands(s2(Y,roi)).addBands(dem).addBands(slp)
           .addBands(tmp).addBands(prc).addBands(wc))
    parts=[]
    for i in range(6):
        sub=ee.FeatureCollection(pts.toList(300,i*300))
        parts.append(rows(stack.sampleRegions(collection=sub,scale=10,geometries=True,tileScale=8)))
    df=pd.concat(parts,ignore_index=True); df['reg']=nm
    df.to_csv(f'scratch/TC01_{nm}.csv',index=False)
    F=AEF_BANDS+S2_BANDS+['elev','slope','tmean','prec']
    print(nm,df.shape,df.y.value_counts().to_dict(),'na',int(df[F].isna().any(axis=1).sum()))
