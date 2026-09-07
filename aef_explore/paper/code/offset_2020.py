"""P6 item 1 -- the polygon-offset check on the 2020 unregistered events.

P2b ran this only for 2021.  Same definition: an event is OFFSET_SUSPECT when the mean angular
change in a 50-150 m outer ring exceeds tau while the polygon interior (10 m inward buffer)
does not -- i.e. the change signal sits beside the mapped polygon rather than inside it.
The unregistered set is dating-independent, so the flags serve both dating rules.

Stage 1 refetches the DETER polygons from the WFS; stage 2 reduces the 2019->2020 angular
change over interior and ring.
"""
import ee, json, sys, time
import numpy as np, pandas as pd
from concurrent.futures import ThreadPoolExecutor
import urllib.parse, urllib.request

WFS = ("https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/deter_amz/ows"
       "?service=WFS&version=2.0.0&request=GetFeature&typeNames=deter-amz:deter_amz"
       "&outputFormat=application/json&count=50&CQL_FILTER=")
HALF = 0.06
AEF = "GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL"


def fetch(row):
    cql = (f"view_date = {row.view_date} AND classname = '{row.classname}' AND "
           f"BBOX(geom,{row.lon-HALF},{row.lat-HALF},{row.lon+HALF},{row.lat+HALF},'CRS:84')")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(WFS + urllib.parse.quote(cql), timeout=120) as r:
                feats = json.load(r).get("features", [])
            break
        except Exception:
            if attempt == 3:
                return None
            time.sleep(3 * (attempt + 1))
    best, bestd = None, 1e9
    for f in feats:
        g = f["geometry"]
        rings = g["coordinates"] if g["type"] == "Polygon" else [c for p in g["coordinates"] for c in p]
        pts = [pt for ring in rings for pt in ring]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        dd = (cx - row.lon) ** 2 + (cy - row.lat) ** 2
        if dd < bestd:
            best, bestd = f, dd
    if best is None:
        return None
    return {"event_id": row.event_id, "geometry": best["geometry"],
            "tau_p90": row.tau_p90, "area_ha": row.area_ha, "state": row.state}


def ang(y0, y1, roi):
    a = ee.ImageCollection(AEF).filterDate(f"{y0}-01-01", f"{y0}-12-31").filterBounds(roi).mosaic()
    b = ee.ImageCollection(AEF).filterDate(f"{y1}-01-01", f"{y1}-12-31").filterBounds(roi).mosaic()
    return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1, 1).acos().multiply(180 / np.pi)


def one(f):
    g = ee.Geometry(f["geometry"])
    img = ang(2019, 2020, g)
    interior = g.buffer(-10)
    ring = g.buffer(150).difference(g.buffer(50), 1)
    for attempt in range(5):
        try:
            vi = img.reduceRegion(ee.Reducer.mean(), interior, 10, maxPixels=1e8,
                                  bestEffort=True).getInfo()
            vr = img.reduceRegion(ee.Reducer.mean(), ring, 10, maxPixels=1e8,
                                  bestEffort=True).getInfo()
            break
        except Exception as e:
            if attempt == 4:
                return None
            time.sleep(8 * (attempt + 1))
    return dict(event_id=f["event_id"], state=f["state"], area_ha=f["area_ha"],
                tau_p90=f["tau_p90"],
                interior_ang_deg=list(vi.values())[0] if vi else None,
                ring_50_150m_ang_deg=list(vr.values())[0] if vr else None)


def main(events_csv, out_csv):
    ee.Initialize()
    ev = pd.read_csv(events_csv)
    print("unregistered 2020 events:", len(ev), flush=True)
    polys = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, r in enumerate(ex.map(fetch, ev.itertuples())):
            if r is not None:
                polys.append(r)
            if (i + 1) % 200 == 0:
                print("wfs", i + 1, "->", len(polys), flush=True)
    print("polygons", len(polys), flush=True)
    rows = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        for i, r in enumerate(ex.map(one, polys)):
            if r is not None:
                rows.append(r)
            if (i + 1) % 200 == 0:
                print("gee", i + 1, "->", len(rows), flush=True)
    d = pd.DataFrame(rows)
    d["offset_suspect"] = ((d.ring_50_150m_ang_deg > d.tau_p90) &
                           (d.interior_ang_deg <= d.tau_p90)).astype(int)
    d.to_csv(out_csv, index=False)
    print("rows", len(d), "offset_suspect share", round(d.offset_suspect.mean(), 4))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
