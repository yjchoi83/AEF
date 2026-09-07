"""P5b item 2, step 3 -- product files for `data/products/` (git-ignored).

* `<region>_deferral_risk_x1000_200m.tif` -- 12-band Int16 deferral risk (x1000), one band
  per event month, derived locally from the 200 m supply stack so no Earth Engine work is
  repeated.
* the retired P5 layer (d) is renamed, not deleted, to
  `<region>_RETIRED_midyear_prior_pconf_60m.tif`, so nothing silently keeps citing it as an
  attribution-confidence layer.
"""
import json, os
import numpy as np, rasterio

P = "data/products"
REG = ["ParaBR163", "Roraima_S"]


def main():
    st = json.load(open("aef_explore/stage5/TB01/P5b/obs_supply_stats.json"))["_link"]
    b0, b1 = st["b0"], st["b1"]
    for name in REG:
        src = rasterio.open(f"{P}/{name}_obs_supply_x10_200m.tif")
        sup = src.read().astype(float) / 10.0            # (12, h, w)
        e = np.stack([0.5 * sup[m] + sup[m + 1:].sum(axis=0) for m in range(12)])
        risk = 1.0 - 1.0 / (1.0 + np.exp(-(b0 + b1 * np.log1p(e))))
        prof = src.profile.copy()
        prof.update(dtype="int16", count=12, nodata=-1)
        out = f"{P}/{name}_deferral_risk_x1000_200m.tif"
        with rasterio.open(out, "w", **prof) as dst:
            dst.write(np.round(risk * 1000).astype("int16"))
            dst.descriptions = tuple(f"event_month_{m:02d}" for m in range(1, 13))
        print(out, os.path.getsize(out) // 1024, "kB")
        old = f"{P}/{name}_pconf.tif"
        new = f"{P}/{name}_RETIRED_midyear_prior_pconf_60m.tif"
        if os.path.exists(old):
            os.rename(old, new)
            print("renamed", old, "->", new)


if __name__ == "__main__":
    main()
