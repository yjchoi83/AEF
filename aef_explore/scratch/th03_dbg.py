import sys; sys.path.insert(0,'scratch')
from aefkit import *
import numpy as np
CRS='EPSG:32636'; P10=ee.Projection(CRS).atScale(10)
roi=ee.Geometry.Rectangle([34.44,31.50,34.48,31.53])   # Gaza City
def unit(i,b): return i.select(b).divide(i.select(b).pow(2).reduce(ee.Reducer.sum()).sqrt())
def ang(a,b): return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1,1).acos().multiply(180/np.pi)
E={y:aef(y,roi).setDefaultProjection(P10) for y in (2022,2024,2025)}
S={y:unit(s2(y,roi),S2_BANDS).setDefaultProjection(P10) for y in (2022,2024)}
OBT=ee.ImageCollection('GOOGLE/Research/open-buildings-temporal/v1')
o22=OBT.filterBounds(roi).filterDate('2022-01-01','2023-01-01').mosaic().select('building_fractional_count')
tests={'aef_2224':ang(E[2022],E[2024]),'aef_2425':ang(E[2024],E[2025]),
       's2_2224':ang(S[2022],S[2024]),'fc22':o22.setDefaultProjection(P10)}
for k,v in tests.items():
    try: print(k,'mean@300',v.rename('v').reduceRegion(ee.Reducer.mean(),roi,300).getInfo())
    except Exception as e: print(k,'ERR',str(e)[:80])
st=ee.Image.cat([v.rename(k) for k,v in tests.items()]).reduceResolution(ee.Reducer.mean(),maxPixels=1024)\
     .reproject(crs=CRS,crsTransform=[300,0,0,0,-300,0])
pts=ee.FeatureCollection([ee.Feature(ee.Geometry.Point([34.45+0.004*i,31.51]),{'i':i}) for i in range(5)])
print('sampleRegions:',st.sampleRegions(pts,scale=300,projection=ee.Projection(CRS).atScale(300)).getInfo()['features'][:2])
print('sample factor:',st.sample(region=roi,projection=ee.Projection(CRS).atScale(300),factor=1,dropNulls=False,geometries=True).size().getInfo())
