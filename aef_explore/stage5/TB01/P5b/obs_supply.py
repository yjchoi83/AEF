"""P5b item 2 — expected Sentinel-2 clear-observation supply by calendar month, and the
deferral risk it implies for an event occurring in each month.

Layer (a): mean number of clear S2 observations per pixel in calendar month m, averaged
over 2019, 2020 and 2021 (the three years bracketing the study years).
Layer (b): for an event in month m, the expected post-event clear count for the rest of
the year, E_m = 0.5 * s_m + sum_{k>m} s_k -- the same proration rule P2 used for
`clear_post` -- pushed through the registration model P(reg) = sigmoid(b0 + b1 * clear_post)
fitted on the 38,303 dated 2021 events (b0 = 2.1413, b1 = 0.0552). Deferral risk = 1 - P.

Unlike the retired P5 map layer (d), which fed this model an *annual* clear count it was
never fitted on, E_m is an expected post-event count -- the model's own input variable.
"""
import ee, json, os, sys, urllib.request
import numpy as np

ee.Initialize()

REGIONS = {
    "ParaBR163": [-56.8409, -5.7426, -55.0379, -3.9339],
    "Roraima_S": [-61.30, 1.20, -60.30, 2.10],
}
YEARS = [2019, 2020, 2021]
B0, B1 = 2.1413, 0.0552
OUTDIR = "aef_explore/stage5/TB01/P5b"
CLOUDY = [3, 8, 9, 10, 11]  # SCL: shadow, cloud med/high, cirrus, snow


def clear_count(roi, year, month):
    start = ee.Date.fromYMD(year, month, 1)
    end = start.advance(1, "month")
    col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
           .filterBounds(roi).filterDate(start, end))
    def is_clear(img):
        scl = img.select("SCL")
        clear = ee.Image(1)
        for c in CLOUDY:
            clear = clear.And(scl.neq(c))
        return clear.And(scl.gt(0)).rename("clear").unmask(0)
    return ee.ImageCollection(col.map(is_clear)).sum().rename(f"m{month:02d}")


def monthly_supply(roi):
    """12-band image: mean clear-observation count per calendar month over YEARS."""
    bands = []
    for m in range(1, 13):
        per_year = [clear_count(roi, y, m) for y in YEARS]
        bands.append(ee.ImageCollection(per_year).mean().rename(f"m{m:02d}"))
    return ee.Image.cat(bands).toFloat()


def expected_post(supply):
    """E_m for m = 1..12, as a 12-band image."""
    out = []
    for m in range(1, 13):
        e = supply.select(f"m{m:02d}").multiply(0.5)
        for k in range(m + 1, 13):
            e = e.add(supply.select(f"m{k:02d}"))
        out.append(e.rename(f"e{m:02d}"))
    return ee.Image.cat(out).toFloat()


def risk(expected):
    """1 - sigmoid(B0 + B1 * E_m)."""
    out = []
    for m in range(1, 13):
        p = expected.select(f"e{m:02d}").multiply(B1).add(B0).multiply(-1).exp().add(1).pow(-1)
        out.append(ee.Image(1).subtract(p).rename(f"r{m:02d}"))
    return ee.Image.cat(out).toFloat()


def thumb(img, roi, vis, path, dims=520):
    url = img.getThumbURL(dict(region=roi, dimensions=dims, format="png", **vis))
    urllib.request.urlretrieve(url, path)
    return path


def main():
    stats = {}
    tmp = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
    for name, box in REGIONS.items():
        roi = ee.Geometry.Rectangle(box)
        supply = monthly_supply(roi)
        exp = expected_post(supply)
        rsk = risk(exp)
        # region-mean series, for the tables
        sc = 100
        s_mean = supply.reduceRegion(ee.Reducer.mean(), roi, sc, maxPixels=1e10, bestEffort=True).getInfo()
        e_mean = exp.reduceRegion(ee.Reducer.mean(), roi, sc, maxPixels=1e10, bestEffort=True).getInfo()
        r_mean = rsk.reduceRegion(ee.Reducer.mean(), roi, sc, maxPixels=1e10, bestEffort=True).getInfo()
        s_p10 = supply.reduceRegion(ee.Reducer.percentile([10, 90]), roi, sc, maxPixels=1e10, bestEffort=True).getInfo()
        stats[name] = dict(supply=s_mean, expected=e_mean, risk=r_mean, supply_pct=s_p10, box=box)
        print(name, "supply means", {k: round(v, 2) for k, v in sorted(s_mean.items())}, flush=True)
        # panels
        for m in range(1, 13):
            thumb(supply.select(f"m{m:02d}"), roi, dict(min=0, max=8, palette=
                  ["440154", "3b528b", "21918c", "5ec962", "fde725"]),
                  f"{tmp}/supply_{name}_{m:02d}.png")
        for m in (3, 6, 9, 12):
            thumb(rsk.select(f"r{m:02d}"), roi, dict(min=0, max=0.5, palette=
                  ["1a9850", "fee08b", "f46d43", "a50026"]),
                  f"{tmp}/risk_{name}_{m:02d}.png")
        print(name, "panels done", flush=True)
    json.dump(stats, open(f"{OUTDIR}/obs_supply_stats.json", "w"), indent=1)


if __name__ == "__main__":
    main()


def download_arrays(tmp="/tmp", dims=600, tif_scale=200, want_tif=True):
    """Pull the 12-band supply stack as NPY (for the plates) and as a 200 m GeoTIFF
    (for `data/products/`), so all colouring and the derived risk layer are computed
    locally rather than re-billed to Earth Engine per panel."""
    import urllib.request, zipfile, io
    for name, box in REGIONS.items():
        roi = ee.Geometry.Rectangle(box)
        supply = monthly_supply(roi)
        url = supply.getDownloadURL(dict(region=roi, dimensions=dims, format="NPY"))
        urllib.request.urlretrieve(url, f"{tmp}/supply_{name}.npy")
        print("npy", name, flush=True)
        if want_tif:
            img = supply.multiply(10).round().toInt16()
            url = img.getDownloadURL(dict(region=roi, scale=tif_scale, format="GEO_TIFF"))
            urllib.request.urlretrieve(url, f"data/products/{name}_obs_supply_x10_{tif_scale}m.tif")
            print("tif", name, flush=True)
