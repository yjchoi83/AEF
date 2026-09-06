import sys; sys.path.insert(0,'scratch')
from aefkit import *
aid='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1'
img=ee.Image(aid)
bn=img.bandNames().getInfo()
print('NBANDS',len(bn)); print('BANDS',bn[:6],'...',bn[-6:])
print('PROPS',[k for k in ee.Image(aid).propertyNames().getInfo()][:20])
# coverage / value range in two ROIs, using the latest age band
last=bn[-1]
for name,roi in [('AMZ_Para',ee.Geometry.Rectangle([-55.5,-6.0,-55.0,-5.5])),
                 ('ATL_SP',ee.Geometry.Rectangle([-46.5,-23.5,-46.0,-23.0]))]:
    st=img.select(last).unmask(0).reduceRegion(ee.Reducer.histogram(maxBuckets=80),roi,scale=100,maxPixels=1e9).getInfo()[last]
    h=dict(zip([round(x) for x in st['bucketMeans']],st['histogram']))
    nz={k:int(v) for k,v in h.items() if k>0 and v>0}
    print(name,'band',last,'zero_px',int(sum(v for k,v in h.items() if k<=0)),'nonzero_total',sum(nz.values()))
    print('  age_hist(100m):',dict(sorted(nz.items())))
