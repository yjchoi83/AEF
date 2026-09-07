"""P5b item 4, step 1 -- regenerate the P4 Congo TMF-2021 patches and pull, per patch,
the 12 monthly Sentinel-2 clear-observation counts and Sentinel-1 scene counts of 2021.

Recipe is P4's, unchanged: JRC TMF v1_2024 AnnualChanges, Dec2020 == 1 (undisturbed moist
forest) and Dec2021 in {2, 3} (deforested / degraded), connected components >= 11 px at
30 m (>= 1 ha), vectorised in 16 tiles per ROI. Geometry is written out so the re-dating
against the 2021-vintage RADD raster runs on exactly the footprints P4 used.
"""
import ee, json, sys, time

ee.Initialize()

ROIS = {"CG1": [28.679, 0.426, 29.578, 1.331], "CG2": [23.301, -4.096, 24.201, -3.191]}
SCALE = 30
CLOUDY = [3, 8, 9, 10, 11]
OUT = sys.argv[1]


def patches(roi):
    tmf = ee.ImageCollection("projects/JRC/TMF/v1_2024/AnnualChanges").mosaic()
    chg = tmf.select("Dec2020").eq(1).And(
        tmf.select("Dec2021").eq(2).Or(tmf.select("Dec2021").eq(3)))
    size = chg.selfMask().connectedPixelCount(200, False)
    return chg.selfMask().updateMask(size.gte(11))


def monthly_layers(roi):
    s2, s1 = [], []
    for m in range(1, 13):
        start = ee.Date.fromYMD(2021, m, 1)
        end = start.advance(1, "month")
        col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
               .filterBounds(roi).filterDate(start, end))

        def is_clear(img):
            scl = img.select("SCL")
            clear = ee.Image(1)
            for c in CLOUDY:
                clear = clear.And(scl.neq(c))
            return clear.And(scl.gt(0)).rename("clear").unmask(0)

        s2.append(ee.ImageCollection(col.map(is_clear)).sum().rename(f"s2_{m:02d}"))
        sar = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(roi)
               .filterDate(start, end).filter(ee.Filter.eq("instrumentMode", "IW")))
        s1.append(sar.map(lambda i: i.select(0).multiply(0).add(1).rename("n").unmask(0))
                  .sum().rename(f"s1_{m:02d}"))
    return ee.Image.cat(s2 + s1).toFloat()


def main():
    feats = []
    for name, box in ROIS.items():
        roi = ee.Geometry.Rectangle(box)
        pat = patches(roi)
        layers = monthly_layers(roi)
        x0, y0, x1, y1 = box
        nx = ny = 4
        for i in range(nx):
            for j in range(ny):
                tile = ee.Geometry.Rectangle([x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny,
                                              x0 + (x1 - x0) * (i + 1) / nx, y0 + (y1 - y0) * (j + 1) / ny])
                vec = pat.reduceToVectors(geometry=tile, scale=SCALE, geometryType="polygon",
                                          eightConnected=False, maxPixels=1e10,
                                          bestEffort=False, labelProperty="lab")
                vec = vec.map(lambda f: f.set("area_ha", f.area(10).divide(1e4))
                              .set("lon", f.geometry().centroid(10).coordinates().get(0))
                              .set("lat", f.geometry().centroid(10).coordinates().get(1)))
                vec = vec.filter(ee.Filter.gte("area_ha", 1.0))
                vec = layers.reduceRegions(collection=vec, reducer=ee.Reducer.mean(),
                                           scale=SCALE, tileScale=4)
                for attempt in range(4):
                    try:
                        got = vec.getInfo()["features"]
                        break
                    except Exception as e:
                        print("retry", name, i, j, repr(e)[:120], flush=True)
                        time.sleep(20)
                else:
                    raise RuntimeError(f"tile {name} {i}{j} failed")
                for f in got:
                    p = f["properties"]
                    p["roi"] = name
                    feats.append({"properties": p, "geometry": f["geometry"]})
                print(name, i, j, len(got), "total", len(feats), flush=True)
    json.dump(feats, open(OUT, "w"))
    print("patches", len(feats))


if __name__ == "__main__":
    main()
