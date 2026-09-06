import ee; ee.Initialize(project='alpha-earth-app')
ids=["projects/sat-io/open-datasets/ICESAT2/ATL08","NASA/ICESat-2/ATL08",
     "projects/sat-io/open-datasets/ICESAT2/ATL08_1KM","users/sat-io/ICESAT2/ATL08"]
for aid in ids:
    hit=None
    for ctor in (ee.ImageCollection, ee.FeatureCollection, ee.Image):
        try:
            o=ctor(aid); o.getInfo() if ctor is ee.Image else o.limit(1).size().getInfo()
            hit=ctor.__name__; break
        except Exception as e: last=str(e)[:60]
    print(("OK  "+hit if hit else "NOT FOUND"), aid)
