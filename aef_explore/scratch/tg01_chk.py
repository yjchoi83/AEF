import sys; sys.path.insert(0,'scratch')
from aefkit import *
TMF = ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').mosaic()
print('TMF bands sample:', TMF.bandNames().getInfo()[:3], '...n=', TMF.bandNames().size().getInfo())
rois = {'PA_novo':[-55.6,-6.4,-54.6,-5.4], 'MT_arc':[-55.4,-11.9,-54.4,-10.9], 'GH_lib':[-3.2,5.4,-2.2,6.4]}
for k,b in rois.items():
    roi = ee.Geometry.Rectangle(b)
    lb = TMF.select('Dec2021').unmask(0)
    h = lb.reduceRegion(ee.Reducer.frequencyHistogram(), roi, 200, maxPixels=1e9).getInfo()['Dec2021']
    tot = sum(h.values())
    sh = {c: round(v/tot,4) for c,v in sorted(h.items(), key=lambda x:-x[1])[:8]}
    na = aef(2021, roi).bandNames().size().getInfo()
    ns2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate('2021-01-01','2022-01-01').filterBounds(roi).size().getInfo()
    print(k, 'AEFbands', na, 'S2scenes', ns2, 'TMFdec2021 share', sh)
