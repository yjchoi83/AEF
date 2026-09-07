"""P5b item 4, step 2 -- re-date the Congo patches against the 2021-vintage RADD raster.

Source: GFW Data API dataset `wur_radd_alerts`, version `v20220109` (the first version whose
coverage spans all of calendar 2021), pixel_meaning `date_conf`, tiles 10N_020E (CG1) and
00N_020E (CG2), fetched with header `x-api-key`. Encoding: value = conf * 10000 + days since
2014-12-31, conf 2 = unconfirmed, 3 = confirmed.

Dating rule is P4's, unchanged: first alert (conf >= 2) inside the patch with a date in
2021-01-01 .. 2022-01-09 (the vintage's own end). `first_any` is also recorded, to show how
many patches carry a pre-2021 alert.
"""
import json, sys, datetime as dt
import numpy as np, pandas as pd, rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds

EPOCH = dt.date(2014, 12, 31)
LO = (dt.date(2021, 1, 1) - EPOCH).days           # 2192
HI = (dt.date(2022, 1, 9) - EPOCH).days           # vintage cutoff
TILES = {"CG1": "radd_10N_020E.tif", "CG2": "radd_00N_020E.tif"}


def bounds(geom):
    xs, ys = [], []
    for ring in geom["coordinates"]:
        for x, y in ring:
            xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def main(patch_json, tiledir, out_csv):
    feats = json.load(open(patch_json))
    rows = []
    for roi, tif in TILES.items():
        src = rasterio.open(f"{tiledir}/{tif}")
        sub = [f for f in feats if f["properties"]["roi"] == roi]
        print(roi, len(sub), "patches", flush=True)
        for k, f in enumerate(sub):
            g = f["geometry"]
            x0, y0, x1, y1 = bounds(g)
            win = from_bounds(x0, y0, x1, y1, src.transform).round_offsets().round_lengths()
            win = win.crop(src.height, src.width)
            if win.width < 1 or win.height < 1:
                continue
            arr = src.read(1, window=win)
            tr = src.window_transform(win)
            mask = geometry_mask([g], out_shape=arr.shape, transform=tr, invert=True,
                                 all_touched=True)
            v = arr[mask & (arr > 0)]
            p = dict(f["properties"])
            day_all = (v % 10000).astype(int) if v.size else np.array([], int)
            conf = (v // 10000).astype(int) if v.size else np.array([], int)
            ok = conf >= 2
            p["npx_alert"] = int(ok.sum())
            p["first_any"] = int(day_all[ok].min()) if ok.any() else -1
            sel = ok & (day_all >= LO) & (day_all <= HI)
            p["first_2021"] = int(day_all[sel].min()) if sel.any() else -1
            p["nhigh_2021"] = int((sel & (conf == 3)).sum())
            rows.append(p)
            if (k + 1) % 500 == 0:
                print(roi, k + 1, flush=True)
    d = pd.DataFrame(rows)
    for c in ("first_any", "first_2021"):
        d[c + "_date"] = [(EPOCH + dt.timedelta(days=int(x))).isoformat() if x > 0 else ""
                          for x in d[c]]
    d.to_csv(out_csv, index=False)
    print("rows", len(d), "dated 2021 vintage",
          (d["first_2021"] > 0).mean().round(4))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
