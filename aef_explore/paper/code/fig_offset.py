"""Figure F6 -- worked examples of the polygon-offset diagnostic.

Two events flagged OFFSET_SUSPECT (change in the 50-150 m ring, not in the interior) and two
unregistered events that are not flagged, each shown as a pre-event Sentinel-2 composite, a
post-event composite and the 2019->2020 angular-change field, with the DETER polygon and its
ring drawn on top.
"""
import io, json, sys, time, urllib.parse, urllib.request
import numpy as np
import pandas as pd
import ee
import matplotlib.pyplot as plt
from PIL import Image
from figstyle import W2, C, INK, INK2, SEQ_BLUE, save, panel_tag
from matplotlib.colors import LinearSegmentedColormap

WFS = ("https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/deter_amz/ows"
       "?service=WFS&version=2.0.0&request=GetFeature&typeNames=deter-amz:deter_amz"
       "&outputFormat=application/json&count=50&CQL_FILTER=")
OFFSETS = "aef_explore/paper/code/offset_2020.csv"
EVENTS = "aef_explore/stage5/TB01/P2b/P2b_events_2020.csv"
ANG = LinearSegmentedColormap.from_list("ang", SEQ_BLUE)
PAD = 0.006


def polygon(row):
    cql = (f"view_date = {row.view_date} AND classname = '{row.classname}' AND "
           f"BBOX(geom,{row.lon-0.05},{row.lat-0.05},{row.lon+0.05},{row.lat+0.05},'CRS:84')")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(WFS + urllib.parse.quote(cql), timeout=120) as r:
                feats = json.load(r)["features"]
            break
        except Exception:
            if attempt == 4:
                raise
            time.sleep(5 * (attempt + 1))
    best, bd = None, 1e9
    for f in feats:
        g = f["geometry"]
        rings = g["coordinates"] if g["type"] == "Polygon" else [c for p in g["coordinates"] for c in p]
        pts = [pt for ring in rings for pt in ring]
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
        d = (cx - row.lon) ** 2 + (cy - row.lat) ** 2
        if d < bd:
            best, bd = f, d
    return best["geometry"]


def rings(geom):
    if geom["type"] == "Polygon":
        return [np.asarray(r) for r in geom["coordinates"]]
    return [np.asarray(r) for p in geom["coordinates"] for r in p]


def thumb(img, region, vis, dims=340):
    url = img.getThumbURL(dict(region=region, dimensions=dims, format="png", **vis))
    for a in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return np.asarray(Image.open(io.BytesIO(r.read())).convert("RGB")) / 255.0
        except Exception:
            time.sleep(4 * (a + 1))
    raise RuntimeError("thumb failed")


def s2_median(year, m0, m1, roi):
    col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(roi)
           .filterDate(f"{year}-{m0:02d}-01", f"{year}-{m1:02d}-28")
           .map(lambda i: i.updateMask(i.select("SCL").neq(3).And(i.select("SCL").lt(8)))))
    return col.median().select(["B4", "B3", "B2"])


def ang_img(y0, y1, roi):
    A = "GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL"
    a = ee.ImageCollection(A).filterDate(f"{y0}-01-01", f"{y0}-12-31").filterBounds(roi).mosaic()
    b = ee.ImageCollection(A).filterDate(f"{y1}-01-01", f"{y1}-12-31").filterBounds(roi).mosaic()
    return a.multiply(b).reduce(ee.Reducer.sum()).clamp(-1, 1).acos().multiply(180 / np.pi)


def main():
    ee.Initialize()
    off = pd.read_csv(OFFSETS)
    ev = pd.read_csv(EVENTS).set_index("event_id")
    off = off.join(ev[["lon", "lat", "view_date", "classname"]], on="event_id")
    off = off[off.area_ha.between(5, 60)]
    sus = off[off.offset_suspect == 1].sort_values("ring_50_150m_ang_deg", ascending=False).head(2)
    cln = off[(off.offset_suspect == 0)].sort_values("interior_ang_deg").head(2)
    sel = pd.concat([sus, cln])
    fig, axes = plt.subplots(3, 4, figsize=(W2, W2 * 0.80))
    fig.subplots_adjust(wspace=0.06, hspace=0.10, left=0.055, right=0.985, top=0.90, bottom=0.03)
    for j, row in enumerate(sel.itertuples()):
        geom = polygon(row)
        rr = rings(geom)
        xs = np.concatenate([r[:, 0] for r in rr]); ys = np.concatenate([r[:, 1] for r in rr])
        ext = (xs.min() - PAD, xs.max() + PAD, ys.min() - PAD, ys.max() + PAD)
        region = ee.Geometry.Rectangle([ext[0], ext[2], ext[1], ext[3]])
        pre = thumb(s2_median(2019, 6, 9, region), region,
                    dict(min=200, max=2200, bands=["B4", "B3", "B2"]))
        post = thumb(s2_median(2020, 6, 9, region), region,
                     dict(min=200, max=2200, bands=["B4", "B3", "B2"]))
        a = thumb(ang_img(2019, 2020, region), region,
                  dict(min=0, max=40, palette=[c.lstrip("#") for c in SEQ_BLUE]))
        for i, (arr, lab) in enumerate(((pre, "2019 dry-season S2"),
                                        (post, "2020 dry-season S2"),
                                        (a, "2019→2020 angular change"))):
            ax = axes[i][j]
            ax.imshow(arr, extent=ext, interpolation="nearest")
            for r in rr:
                ax.plot(r[:, 0], r[:, 1], color="#ffd166", lw=0.9, zorder=3)
            from shapely.geometry import Polygon as SPoly
            from shapely.ops import unary_union
            poly = unary_union([SPoly(r) for r in rr if len(r) > 3])
            for buf in (50, 150):
                b = poly.buffer(buf / (111320.0 * np.cos(np.radians(row.lat))))
                for part in (b.geoms if b.geom_type == "MultiPolygon" else [b]):
                    ax.plot(*np.asarray(part.exterior.coords).T, color="#f77f00",
                            lw=0.6, ls=":", zorder=3)
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_color("#cdd3d9"); s.set_linewidth(0.4)
            if j == 0:
                ax.set_ylabel(lab, fontsize=6.6, color=INK2)
            if i == 0:
                flag = "OFFSET-SUSPECT" if row.offset_suspect else "not flagged"
                ax.set_title(f"{row.event_id} · {row.state} · {row.area_ha:.0f} ha\n"
                             f"interior {row.interior_ang_deg:.1f}° · ring "
                             f"{row.ring_50_150m_ang_deg:.1f}° · τ {row.tau_p90:.1f}°\n{flag}",
                             fontsize=6.2,
                             color=C["flag"] if row.offset_suspect else INK2, pad=3)
    fig.text(0.055, 0.965, "Polygon interior (solid) and 50–150 m ring (dotted)", fontsize=7.5,
             color=INK)
    save(fig, "F7_offset_examples.png")


if __name__ == "__main__":
    main()
