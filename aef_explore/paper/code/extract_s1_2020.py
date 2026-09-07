"""P6 item 1 -- monthly Sentinel-1 IW scene counts at the 2020 event centroids.

P2b stored `s1_post` only under the RADD dating rule, so switching the primary event date to
`date_upper = min(RADD first alert, DETER view_date)` leaves the 2020 SAR control undefined.
This re-extracts the twelve monthly counts (the quantity `s1_post` is prorated from), so any
dating rule can be applied locally -- and so the stored `s1_post_radd_any` can be reproduced
as a check.

Extraction geometry follows P2: centroid `sampleRegions`, not polygon `reduceRegions`.
"""
import ee, sys, time
import pandas as pd

ee.Initialize()
CHUNK = 1500


def monthly_s1(year, roi):
    out = []
    for m in range(1, 13):
        s = ee.Date.fromYMD(year, m, 1)
        col = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(roi)
               .filterDate(s, s.advance(1, "month"))
               .filter(ee.Filter.eq("instrumentMode", "IW")))
        out.append(col.map(lambda i: i.select(0).multiply(0).add(1).rename("n").unmask(0))
                   .sum().rename(f"s1_{m:02d}"))
    return ee.Image.cat(out).toFloat()


def main(events_csv, out_csv, year):
    d = pd.read_csv(events_csv)
    d = d[d["radd_any"].notna()].copy()
    d = d.sort_values(["block", "lon"]).reset_index(drop=True)
    print("points", len(d), flush=True)
    rows = []
    for i in range(0, len(d), CHUNK):
        part = d.iloc[i:i + CHUNK]
        fc = ee.FeatureCollection([
            ee.Feature(ee.Geometry.Point([r.lon, r.lat]), {"event_id": r.event_id})
            for r in part.itertuples()])
        img = monthly_s1(year, fc.geometry().bounds())
        for attempt in range(5):
            try:
                got = img.sampleRegions(collection=fc, scale=10, geometries=False).getInfo()
                break
            except Exception as e:
                print("retry", i, repr(e)[:100], flush=True)
                time.sleep(15 * (attempt + 1))
        else:
            raise RuntimeError(f"chunk {i} failed")
        rows.extend(f["properties"] for f in got["features"])
        print(i + len(part), "of", len(d), "->", len(rows), flush=True)
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print("rows", len(rows))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
