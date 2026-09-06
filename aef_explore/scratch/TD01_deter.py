import ee
ee.Initialize(project='alpha-earth-app')
cands=['projects/mapbiomas-workspace/AUXILIAR/deter',
 'projects/sat-io/open-datasets/DETER/deter-amz',
 'users/deter/deter_amazonia',
 'projects/earthengine-legacy/assets/users/inpe/deter',
 'projects/sat-io/open-datasets/DETER',
 'users/tainacunha/DETER']
for cid in cands:
    got=False
    for ctor in (ee.FeatureCollection, ee.ImageCollection, ee.Image):
        try:
            o=ctor(cid)
            info=o.size().getInfo() if ctor is not ee.Image else o.bandNames().getInfo()
            print('REACHABLE',ctor.__name__,cid,info); got=True; break
        except Exception as e:
            last=str(e).split('\n')[0][:60]
    if not got: print('MISS',cid,'|',last)
