import ee; ee.Initialize(project='alpha-earth-app')
cands=[("projects/sat-io/open-datasets/ATL08","IC"),("projects/sat-io/open-datasets/icesat2/atl08","IC"),
("NASA/ICESat_2/ATL08","IC"),("projects/sat-io/open-datasets/ICESat2/ATL08_canopy","IC"),
("projects/sat-io/open-datasets/GEDI/ICESAT2","IC"),
("projects/sat-io/open-datasets/CANOPY_HEIGHT","I"),
("projects/sat-io/open-datasets/ETH/GlobalCanopyHeight_10m_2020_version1","I"),
("users/potapovpeter/GEDI_V27","I"),
("projects/sat-io/open-datasets/facebook/canopy_height","I")]
for aid,t in cands:
    for ctor in (ee.ImageCollection, ee.Image):
        try:
            o=ctor(aid); nm=o.limit(1).size().getInfo() if ctor is ee.ImageCollection else len(o.bandNames().getInfo())
            print("OK",ctor.__name__,aid,nm); break
        except Exception as e:
            msg=str(e).split("\n")[0][:70]
    else: print("MISS",aid,msg)
