import ee
ee.Initialize(project='alpha-earth-app')
# 1) DETER reachability probes (known community/asset ids)
cands = [
 ('projects/earthengine-legacy/assets/projects/mapbiomas-workspace/AUXILIAR/deter', 'IC'),
 ('projects/sat-io/open-datasets/DETER/deter-amz','IC'),
 ('users/deter/deter_amazonia','FC'),
 ('projects/earthengine-legacy/assets/users/inpe/deter','FC'),
]
for cid,kind in cands:
    for ctor in (ee.ImageCollection, ee.FeatureCollection, ee.Image):
        try:
            o = ctor(cid); print('OK', ctor.__name__, cid, o.limit(1).size().getInfo() if ctor is not ee.Image else 'img')
            break
        except Exception as e:
            msg=str(e).split('\n')[0][:70]
    else:
        print('MISS', cid, msg)
# 2) TMF DegradationYear / AnnualChanges over Para ROI
roi = ee.Geometry.Rectangle([-52.6,-4.4,-52.0,-3.8])
deg = ee.ImageCollection('projects/JRC/TMF/v1_2024/DegradationYear').mosaic()
dfr = ee.ImageCollection('projects/JRC/TMF/v1_2024/DeforestationYear').mosaic()
ac  = ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').mosaic()
print('TMF AnnualChanges bands n=', ac.bandNames().size().getInfo())
print('TMF AC band sample', ac.bandNames().getInfo()[-4:])
h = deg.rename('d').addBands(dfr.rename('f')).reduceRegion(
    ee.Reducer.frequencyHistogram(), roi, scale=100, maxPixels=1e9).getInfo()
for k,v in h.items():
    items=sorted(((int(float(a)),b) for a,b in v.items()))
    print(k, [i for i in items if i[0]>=2018][:12], 'total_nonzero_px100m=', int(sum(b for a,b in items if a>0)))
