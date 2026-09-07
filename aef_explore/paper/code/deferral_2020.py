"""P7 item 4 -- re-derive the 2020 -> 2021 deferral rate.

P3 reported this direction but its per-event table was not retained, so the manuscript had to
cite it rather than print a re-derived value. This recomputes it from scratch: refetch the
DETER polygons of every event unregistered in 2020, take the mean 2020->2021 angular change
over the polygon interior (10 m inward buffer, as everywhere else), and compare it with the
2020->2021 stable-forest threshold of the event's own state -- the same tau the 2021 cohort
uses, since it is estimated on the same year pair.
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
P2B = "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv"
P2 = "aef_explore/stage5/TB01/P2/P2_events.csv"


def fetch(row):
    cql = (f"view_date = {row.view_date} AND classname = '{row.classname}' AND "
           f"BBOX(geom,{row.lon-HALF},{row.lat-HALF},{row.lon+HALF},{row.lat+HALF},'CRS:84')")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(WFS + urllib.parse.quote(cql), timeout=120) as r:
                feats = json.load(r).get("features", [])
            break
        except Exception:
            if attempt == 4:
                return None
            time.sleep(4 * (attempt + 1))
    best, bd = None, 1e9
    for f in feats:
        g = f["geometry"]
        rings = (g["coordinates"] if g["type"] == "Polygon"
                 else [c for p in g["coordinates"] for c in p])
        pts = [pt for ring in rings for pt in ring]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        d = (cx - row.lon) ** 2 + (cy - row.lat) ** 2
        if d < bd:
            best, bd = f, d
    if best is None:
        return None
    return dict(event_id=row.event_id, state=row.state, block=row.block,
                area_ha=row.area_ha, tau_next=row.tau_next, geometry=best["geometry"])


def ang(y0, y1, roi):
    a = ee.ImageCollection(AEF).filterDate(f"{y0}-01-01", f"{y0}-12-31").filterBounds(roi).mosaic()
    b = ee.ImageCollection(AEF).filterDate(f"{y1}-01-01", f"{y1}-12-31").filterBounds(roi).mosaic()
    return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1, 1).acos().multiply(180 / np.pi)


def one(f):
    g = ee.Geometry(f["geometry"])
    for attempt in range(5):
        try:
            v = ang(2020, 2021, g).reduceRegion(ee.Reducer.mean(), g.buffer(-10), 10,
                                                maxPixels=1e8, bestEffort=True).getInfo()
            break
        except Exception:
            if attempt == 4:
                return None
            time.sleep(8 * (attempt + 1))
    out = {k: f[k] for k in ("event_id", "state", "block", "area_ha", "tau_next")}
    out["ang_2020_2021_deg"] = list(v.values())[0] if v else None
    return out


def main(out_csv):
    ee.Initialize()
    d = pd.read_csv(P2B)
    d = d[d["radd_any"].notna() & (d["registered"] == 0)].copy()
    tau_next = (pd.read_csv(P2).groupby("state")["tau_p90"].first())   # 2020->2021 thresholds
    d["tau_next"] = d["state"].map(tau_next)
    d = d[d["tau_next"].notna()]
    print("unregistered 2020 events:", len(d), flush=True)
    polys = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, r in enumerate(ex.map(fetch, d.itertuples())):
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
    out = pd.DataFrame(rows)
    out["registered"] = (out["ang_2020_2021_deg"] > out["tau_next"]).astype(float)
    out.to_csv(out_csv, index=False)
    print("rows", len(out), "deferral rate %.4f" % out["registered"].mean())


if __name__ == "__main__":
    main(sys.argv[1])
