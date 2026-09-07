"""P5b item 1 — refetch the DETER polygons for the clear_post == 0 events of both cohorts.

The P2/P2b event tables carry only centroids, so the polygon geometry needed for the
prior-year angular-change extraction is pulled back from the DETER WFS one event at a
time (bbox around the stored centroid + the event's own view_date + classname), keeping
the candidate whose centroid is nearest the stored one.
"""
import json, sys, time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import urllib.parse, urllib.request

WFS = ("https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/deter_amz/ows"
       "?service=WFS&version=2.0.0&request=GetFeature&typeNames=deter-amz:deter_amz"
       "&outputFormat=application/json&count=50&CQL_FILTER=")
OUT = sys.argv[1]
HALF = 0.06  # deg box half-width; DETER polygons are < 5 km across


def fetch(row):
    cql = (f"view_date = {row.view_date} AND classname = '{row.classname}' AND "
           f"BBOX(geom,{row.lon-HALF},{row.lat-HALF},{row.lon+HALF},{row.lat+HALF},'CRS:84')")
    url = WFS + urllib.parse.quote(cql)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
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
        d = (cx - row.lon) ** 2 + (cy - row.lat) ** 2
        if d < bestd:
            best, bestd = f, d
    if best is None:
        return None
    return {"event_id": row.event_id, "dist_deg": bestd ** 0.5, "geometry": best["geometry"],
            "gid": best["properties"]["gid"], "uf": best["properties"]["uf"]}


def main():
    frames = []
    for cohort, path in (("2021", "aef_explore/stage5/TB01/P2/P2_events.csv"),
                         ("2020", "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv")):
        d = pd.read_csv(path).dropna(subset=["clear_post_radd_any"])
        z = d[d["clear_post_radd_any"] == 0].copy()
        z["cohort"] = cohort
        frames.append(z)
    z = pd.concat(frames)
    print("events to fetch:", len(z), flush=True)
    out = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for i, r in enumerate(ex.map(fetch, z.itertuples())):
            if r is not None:
                r["cohort"] = z.iloc[i]["cohort"]
                out.append(r)
            if (i + 1) % 100 == 0:
                print(i + 1, "done,", len(out), "matched", flush=True)
    json.dump(out, open(OUT, "w"))
    print("matched", len(out), "of", len(z))


if __name__ == "__main__":
    main()
