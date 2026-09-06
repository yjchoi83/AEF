import ee; ee.Initialize(project='alpha-earth-app')
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
ETH=ee.Image("users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1")
META=ee.ImageCollection("projects/meta-forest-monitoring-okw37/assets/CanopyHeight").mosaic()
GEDI=ee.ImageCollection("LARSE/GEDI/GEDI02_A_002_MONTHLY").filterDate("2020-01-01","2022-01-01")
pts={"DE_49N":[10.0,49.3],"DE_50.8N":[10.0,50.8],"SE_57N":[14.5,57.2],"SE_62N":[15.0,62.0],
     "FI_64N":[26.0,64.0],"CA_60N":[-105.0,60.0],"NO_69N":[24.0,69.0]}
for k,(lo,la) in pts.items():
    p=ee.Geometry.Point([lo,la]); r=ee.Geometry.Rectangle([lo-.2,la-.2,lo+.2,la+.2])
    naef=AEF.filterDate("2020-01-01","2021-01-01").filterBounds(p).size()
    eth=ETH.select(0).reduceRegion(ee.Reducer.mean(),r,100,maxPixels=1e8)
    mt=META.select(0).reduceRegion(ee.Reducer.mean(),r,100,maxPixels=1e8)
    ng=GEDI.filterBounds(r).size()
    print(k, ee.Dictionary({"aef":naef,"eth":eth.values().get(0),"meta":mt.values().get(0),"gedi_imgs":ng}).getInfo())
