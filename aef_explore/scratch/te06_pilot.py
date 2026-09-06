import sys, json; sys.path.insert(0,'scratch')
from aefkit import *
REG = {'A_andes':([-72.6,-13.9,-71.8,-13.1],[10,20,30,40,50,60]),
       'B_matogrosso':([-55.9,-13.0,-55.1,-12.2],[10,20,30,40,50,80])}
name = sys.argv[1]; BOX, CV = REG[name]; roi = ee.Geometry.Rectangle(BOX)
DEM = ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").select('DEM').mosaic() \
        .setDefaultProjection('EPSG:3857', None, 30)
def static(y):
    asp = ee.Terrain.aspect(DEM).multiply(np.pi/180)
    e = ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR").filterDate(f"{y}-01-01", f"{y+1}-01-01")
    return (DEM.rename('elev')
        .addBands(ee.Terrain.slope(DEM).rename('slope'))
        .addBands(asp.sin().rename('asp_s')).addBands(asp.cos().rename('asp_c'))
        .addBands(e.select('temperature_2m').mean().rename('t2m'))
        .addBands(e.select('total_precipitation_sum').sum().rename('prcp')))
STAT = ['elev','slope','asp_s','asp_c','t2m','prcp']
res = {}
def run(y, lbl, tgt, task, pts):
    img = aef(y, roi).addBands(s2(y, roi)).addBands(static(y)).addBands(lbl.rename(tgt))
    f = img.sampleRegions(collection=pts, scale=10, geometries=True, tileScale=4)
    df = pd.DataFrame([dict(list(r['properties'].items()) +
         [('lon', r['geometry']['coordinates'][0]), ('lat', r['geometry']['coordinates'][1])])
         for r in f.getInfo()['features']])
    df = df.dropna(subset=[tgt] + AEF_BANDS[:1] + S2_BANDS + STAT)
    if task == 'clf':
        vc = df[tgt].value_counts(); keep = vc[vc >= 150].index
        df = df[df[tgt].isin(keep)]
        bal = {int(k): int(v) for k, v in df[tgt].value_counts().items()}
    else:
        bal = {'mean': round(df[tgt].mean(), 2), 'sd': round(df[tgt].std(), 2)}
    blk = blocks(df, 0.1)
    out = {'n': len(df), 'balance': bal, 'nblk': int(blk.nunique()), 'year': y}
    for tag, fe in [('AEF64', AEF_BANDS), ('S2', S2_BANDS),
                    ('S2+static', S2_BANDS + STAT), ('static', STAT)]:
        m, sd, folds, n = probe(df, fe, tgt, blk, task=task, folds=5)
        out[tag] = {'mean': round(m, 3), 'sd': round(sd, 3), 'folds': folds}
    out['delta_AEF_minus_S2static'] = round(out['AEF64']['mean'] - out['S2+static']['mean'], 3)
    out['delta_AEF_minus_S2'] = round(out['AEF64']['mean'] - out['S2']['mean'], 3)
    return out
# T1 land cover (WorldCover v200 = 2021 epoch, calendar-year aligned with AEF 2021)
wc = ee.Image("ESA/WorldCover/v200/2021").rename('lc')
pts_lc = wc.stratifiedSample(numPoints=450, classBand='lc', region=roi, scale=30, seed=7,
         classValues=CV, classPoints=[450]*len(CV), geometries=True, dropNulls=True, tileScale=4)
res['landcover'] = run(2021, wc, 'lc', 'clf', pts_lc)
# T4 canopy height (ETH 2020 -> AEF/S2/ERA5 2020)
eth = ee.Image("users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1").select(0).rename('hgt')
pts_h = ee.FeatureCollection.randomPoints(region=roi, points=2500, seed=11)
res['canopyheight'] = run(2020, eth, 'hgt', 'reg', pts_h)
print(json.dumps(res, indent=1))
json.dump(res, open(f'scratch/te06_{name}.json', 'w'), indent=1)
