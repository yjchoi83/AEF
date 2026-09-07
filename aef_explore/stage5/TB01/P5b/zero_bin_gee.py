"""P5b item 1 -- per-event extraction for the clear_post == 0 events of both cohorts.

For each event (polygon interior, 10 m inward buffer, exactly as P1/P2 defined it):
  ang_event   angular change across the event year   (2020->2021 for the 2021 cohort,
              2019->2020 for the 2020 cohort) -- a reproduction check against the stored value
  ang_prior   the prior-year angular change          (2019->2020 / 2018->2019), the quantity
              that tests the "pre-event disturbance" explanation against tau
  m01..m12    clear Sentinel-2 observation counts by month of the event year, so `clear_post`
              can be recomputed from the DETER view_date instead of the RADD date
"""
import ee, json, sys, time
import numpy as np

ee.Initialize()
AEF = "GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL"
CLOUDY = [3, 8, 9, 10, 11]
CHUNK = 1  # one event per request: a bounds box spanning scattered polygons
           # blows the interactive memory budget once the 64-band embedding is
           # mosaicked over it


def ang(y0, y1, roi):
    a = ee.ImageCollection(AEF).filterDate(f"{y0}-01-01", f"{y0}-12-31").filterBounds(roi).mosaic()
    b = ee.ImageCollection(AEF).filterDate(f"{y1}-01-01", f"{y1}-12-31").filterBounds(roi).mosaic()
    dot = a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1, 1)
    return dot.acos().multiply(180 / np.pi).rename("ang")


def monthly_clear(year, roi):
    out = []
    for m in range(1, 13):
        s = ee.Date.fromYMD(year, m, 1)
        col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(roi)
               .filterDate(s, s.advance(1, "month")))

        def is_clear(img):
            scl = img.select("SCL")
            c = ee.Image(1)
            for k in CLOUDY:
                c = c.And(scl.neq(k))
            return c.And(scl.gt(0)).rename("clear").unmask(0)
        out.append(ee.ImageCollection(col.map(is_clear)).sum().rename(f"m{m:02d}"))
    return ee.Image.cat(out).toFloat()


def one(f):
    yr = 2021 if f["cohort"] == "2021" else 2020
    g = ee.Geometry(f["geometry"])
    roi = g.buffer(-10)
    img = ee.Image.cat([
        ang(yr - 1, yr, g).rename("ang_event"),
        ang(yr - 2, yr - 1, g).rename("ang_prior"),
        monthly_clear(yr, g)])
    for attempt in range(5):
        try:
            v = img.reduceRegion(ee.Reducer.mean(), roi, 10, maxPixels=1e8,
                                 bestEffort=True).getInfo()
            break
        except Exception as e:
            if attempt == 4:
                print("give up", f["event_id"], repr(e)[:80], flush=True)
                return None
            time.sleep(8 * (attempt + 1))
    v["event_id"] = f["event_id"]
    v["cohort"] = f["cohort"]
    return v


def main(poly_json, out_csv):
    from concurrent.futures import ThreadPoolExecutor
    import pandas as pd
    feats = json.load(open(poly_json))
    rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for k, r in enumerate(ex.map(one, feats)):
            if r is not None:
                rows.append(r)
            if (k + 1) % 100 == 0:
                print(k + 1, "of", len(feats), flush=True)
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print("rows", len(rows))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
