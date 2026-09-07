"""P7 item 4 -- block-bootstrap CI for the re-derived 2020 -> 2021 deferral rate.

Merges the result into numbers.json as `h4_2020`, beside the 2021 -> 2022 value that
run_numbers.py already produces, so both directions of Fig. 3 are re-derived rather than cited.
"""
import json
import pandas as pd
import p2_model as M

OUT = "aef_explore/paper/numbers.json"

d = pd.read_csv("aef_explore/paper/code/deferral_2020.csv")
d = d[d["ang_2020_2021_deg"].notna()].copy()
res = dict(n=int(len(d)),
           share=M.boot_ci(32, d, "share", "area_ha", "area_ha", "registered"))
n = json.load(open(OUT))
n["h4_2020"] = res
json.dump(n, open(OUT, "w"), indent=1)
print("2020 -> 2021 deferral: %.4f [%.4f, %.4f] on n = %d"
      % (res["share"]["point"], res["share"]["lo"], res["share"]["hi"], res["n"]))
