import ee, json
ee.Initialize(project='alpha-earth-app')
ROIS = {
 'AMZ': [-55.0,-4.0,-54.4,-3.4],   'CGO': [24.5,0.2,25.1,0.8],
 'SAH': [-15.5,14.5,-14.9,15.1],   'ROK': [127.0,36.3,127.6,36.9],
 'SEA': [111.5,-2.5,112.1,-1.9],   'IBE': [-5.0,39.5,-4.4,40.1],
}
WC = ee.Image("ESA/WorldCover/v200/2021")
AEF = ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
for k,b in ROIS.items():
    roi = ee.Geometry.Rectangle(b)
    h = WC.reduceRegion(ee.Reducer.frequencyHistogram(), roi, 300).get('Map').getInfo()
    n = AEF.filterDate('2021-01-01','2022-01-01').filterBounds(roi).size().getInfo()
    tot = sum(h.values())
    top = sorted(((int(c), round(100*v/tot,1)) for c,v in h.items()), key=lambda x:-x[1])[:6]
    print(k, 'aef_imgs=%d'%n, 'wc%:', top)
print('WC v200 props:', WC.get('system:time_start').getInfo())
