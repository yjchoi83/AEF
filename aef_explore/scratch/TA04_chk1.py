import sys; sys.path.insert(0,'scratch')
import ee
ee.Initialize()
cands=["projects/sat-io/open-datasets/global-mining/global_mining_polygons",
 "projects/sat-io/open-datasets/global_mining_polygons",
 "users/maus/mining_polygons",
 "projects/ee-amazonminingwatch/assets/mining",
 "GOOGLE/Research/open-buildings/v3/polygons"]
for c in cands:
    try: ee.data.getAsset(c); print("OK",c)
    except Exception as e: print("NO",c,str(e)[:60])
# ROI coverage: Tapajos (Amazon ASGM) and Ghana Ankobra/Offin
rois={"AMZ_tapajos":[-56.6,-6.6,-55.8,-5.9],"GHA_ankobra":[-2.30,5.30,-1.80,5.90]}
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
for k,b in rois.items():
    r=ee.Geometry.Rectangle(b)
    for y in [2020,2024]:
        print(k,y,"AEF imgs",AEF.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(r).size().getInfo())
    h=ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
    g=ee.Image("JRC/GSW1_4/GlobalSurfaceWater")
    # area stats: loss 2018-2024, water occurrence>25 proximity
    ly=h.select('lossyear').unmask(0)
    loss=ly.gte(18).And(ly.lte(24))
    occ=g.select('occurrence').unmask(0)
    wat=occ.gte(20)
    near=wat.fastDistanceTransform(60).sqrt().multiply(30).lt(1000)  # placeholder
    st=ee.Image.cat(loss.rename('loss'),wat.rename('wat')).reduceRegion(
        ee.Reducer.mean(),r,scale=90,maxPixels=1e9,bestEffort=True).getInfo()
    print(k,"frac loss18-24",round(st['loss'],5),"frac water>=20%",round(st['wat'],5))
