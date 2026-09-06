import ee
ee.Initialize(project='alpha-earth-app')
ROIS = {
 'AMZ': [-63.6,-10.6,-62.4,-9.6],  # Rondonia deforestation arc
 'CGO': [24.0,-0.2,25.2,0.8],      # Kisangani, Congo Basin
 'SAH': [-16.4,14.1,-15.2,15.1],   # Senegal groundnut basin
 'ROK': [126.7,36.1,127.9,37.1],   # central South Korea
 'SEA': [101.3,-0.2,102.5,0.8],    # Riau, Sumatra oil-palm frontier
 'IBE': [-5.2,39.3,-4.0,40.3],     # Castilla-La Mancha, Spain
}
WC = ee.Image("ESA/WorldCover/v200/2021")
REMAP = ([10,20,30,40,50,60,70,80,90,95,100],[1,2,2,3,4,5,0,6,0,0,2])  # 1 tree 2 shrub/grass 3 crop 4 built 5 bare 6 water
lc = WC.remap(*REMAP).rename('lc').selfMask()
for k,b in ROIS.items():
    roi = ee.Geometry.Rectangle(b)
    h = lc.reduceRegion(ee.Reducer.frequencyHistogram(), roi, 300).get('lc').getInfo()
    tot = sum(h.values())
    print(k, sorted((int(c), round(100*v/tot,2)) for c,v in h.items()))
