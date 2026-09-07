"""Fetch simplified country outlines once, for the locator insets on the map plates.

`USDOS/LSIB_SIMPLE/2017` from Earth Engine, simplified to 5 km and cached as a small GeoJSON
so the figure scripts need no network access.
"""
import ee, json

ee.Initialize()
COUNTRIES = ["Brazil", "Peru", "Colombia", "Venezuela", "Bolivia", "Guyana", "Suriname",
             "French Guiana", "Ecuador", "Paraguay", "Argentina", "Chile", "Uruguay",
             "Congo (Kinshasa)", "Congo (Brazzaville)", "Gabon", "Cameroon",
             "Central African Republic", "Uganda", "Rwanda", "Burundi", "Tanzania",
             "Angola", "Zambia", "South Sudan", "Equatorial Guinea"]

fc = (ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017")
      .filter(ee.Filter.inList("country_na", COUNTRIES))
      .map(lambda f: ee.Feature(f.geometry().simplify(20000), {"name": f.get("country_na")})))
gj = fc.getInfo()
json.dump(gj, open("aef_explore/paper/code/outlines.geojson", "w"))
print("features", len(gj["features"]),
      "bytes", len(json.dumps(gj)))
