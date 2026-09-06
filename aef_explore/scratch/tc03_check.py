import sys; sys.path.insert(0,'scratch')
from aefkit import *
WC = ee.Image("ESA/WorldCover/v200/2021").select('Map')
ROIS = {
 'BRamz':[-55.5,-9.0,-55.0,-8.5],'CGkasai':[21.0,-5.0,21.5,-4.5],'IDsumatra':[102.0,-1.0,102.5,-0.5],
 'INpunjab':[75.5,30.5,76.0,31.0],'USiowa':[-93.5,42.0,-93.0,42.5],'ESduero':[-4.5,41.5,-4.0,42.0],
 'SNsahel':[-15.5,14.5,-15.0,15.0],'AUnsw':[147.0,-33.0,147.5,-32.5],'CNhenan':[113.5,34.0,114.0,34.5],
 'ZAhveld':[26.5,-26.5,27.0,-26.0]}
for k,b in ROIS.items():
    roi = ee.Geometry.Rectangle(b)
    h = WC.reduceRegion(ee.Reducer.frequencyHistogram(), roi, 100, maxPixels=1e9).getInfo()['Map']
    tot = sum(h.values())
    print(k, {c:round(100*v/tot,1) for c,v in sorted(h.items(), key=lambda x:-x[1]) if 100*v/tot>1.5},
          'AEFimgs', AEF.filterDate('2021-01-01','2022-01-01').filterBounds(roi).size().getInfo())
