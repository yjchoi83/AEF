import ee, csv, sys, os
ee.Initialize(project='alpha-earth-app')
ROIS = {'AMZ':[-63.6,-10.6,-62.4,-9.6],'CGO':[24.0,-0.2,25.2,0.8],'SAH':[-16.4,14.1,-15.2,15.1],
        'ROK':[126.7,36.1,127.9,37.1],'SEA':[101.3,-0.2,102.5,0.8],'IBE':[-5.2,39.3,-4.0,40.3]}
CLS=[1,2,4,6]; NPTS=400; YEAR=2021
WC=ee.Image("ESA/WorldCover/v200/2021").remap([10,20,30,40,50,60,70,80,90,95,100],
                                               [1,2,2,3,4,5,0,6,0,0,2]).rename('lc').selfMask()
AEF=ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
SB=['B2','B3','B4','B8','B11','B12']
def s2(roi):
    def msk(i):
        s=i.select('SCL')
        return i.updateMask(s.neq(3).And(s.neq(8)).And(s.neq(9)).And(s.neq(10)).And(s.neq(11)))
    c=(ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(f'{YEAR}-01-01',f'{YEAR+1}-01-01')
        .filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',70)).map(msk))
    m=c.select(SB).median().divide(10000)
    return m.addBands(m.normalizedDifference(['B8','B4']).rename('NDVI'))
for k,b in ROIS.items():
    out=f'TC03_{k}.csv'
    if os.path.exists(out): print('skip',k); continue
    roi=ee.Geometry.Rectangle(b)
    pts=WC.stratifiedSample(numPoints=NPTS,classBand='lc',classValues=CLS,
        classPoints=[NPTS]*len(CLS),region=roi,scale=30,seed=7,geometries=True,tileScale=4)
    aef=AEF.filterDate(f'{YEAR}-01-01',f'{YEAR+1}-01-01').filterBounds(roi).mosaic()
    stack=aef.addBands(s2(roi))
    samp=stack.sampleRegions(collection=pts,properties=['lc'],scale=10,tileScale=8,geometries=True)
    feats=samp.getInfo()['features']
    ab=[f'A{i:02d}' for i in range(64)]; cols=['lc','lon','lat']+ab+SB+['NDVI']
    rows=[]
    for f in feats:
        p=f['properties']; g=f['geometry']['coordinates']
        if any(p.get(c) is None for c in ab+SB+['NDVI']): continue
        rows.append([p['lc'],round(g[0],5),round(g[1],5)]+[p[c] for c in ab+SB+['NDVI']])
    with open(out,'w',newline='') as fh:
        w=csv.writer(fh); w.writerow(cols); w.writerows(rows)
    from collections import Counter
    print(k,'n=',len(rows),dict(sorted(Counter(r[0] for r in rows).items())))
