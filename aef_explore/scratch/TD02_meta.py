import ee; ee.Initialize(project='alpha-earth-app')
AGE = ee.Image("projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1")
print("bands_n", len(AGE.bandNames().getInfo()))
print("has2022", "secondary_vegetation_age_2022" in AGE.bandNames().getInfo())
a = AGE.select("secondary_vegetation_age_2022")
# Amazon ROI: Para/Rondonia arc-of-deforestation, ~1.5x1.5 deg
roi = ee.Geometry.Rectangle([-55.0, -6.5, -53.5, -5.0])
hist = a.updateMask(a.gt(0)).reduceRegion(
    reducer=ee.Reducer.histogram(maxBuckets=40).combine(ee.Reducer.minMax(), sharedInputs=True),
    geometry=roi, scale=90, maxPixels=1e9, bestEffort=True).getInfo()
h = hist["secondary_vegetation_age_2022_histogram"]
import math
buckets = list(zip([h["bucketMin"]+i*h["bucketWidth"] for i in range(len(h["histogram"]))], h["histogram"]))
tot = sum(h["histogram"])
print("min/max", hist["secondary_vegetation_age_2022_min"], hist["secondary_vegetation_age_2022_max"], "total_px90m", int(tot))
bins = {"1-3":0,"4-6":0,"7-10":0,"11-15":0,"16-25":0,"26+":0}
for lo,c in buckets:
    v=lo
    k = "1-3" if v<=3 else "4-6" if v<=6 else "7-10" if v<=10 else "11-15" if v<=15 else "16-25" if v<=25 else "26+"
    bins[k]+=c
for k,v in bins.items(): print("bin",k,int(v),round(100*v/tot,1),"%")
