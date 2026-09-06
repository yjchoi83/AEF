import ee, json, math, numpy as np
ee.Initialize(project='alpha-earth-app')
AEF = ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
DW  = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
S2  = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
DEM = ee.ImageCollection("COPERNICUS/DEM/GLO30_2024_1").mosaic().select('DEM')
YRS = list(range(2017, 2026))
SITES = {  # name: (lat, lon, reported change year)
 'Jungpyong_gh_2019': (41.557469, 129.632113, 2019),
 'Ryonpho_gh_2022':   (39.792279, 127.535775, 2022),
 'Hwasong_pyy_2022_24':(39.100, 125.800, 2023),
 'Uiju_flood_2024':   (40.150, 124.560, 2024),
}
R = 900.0  # m -> ~1.8 km box
def box(lat, lon, r=R):
    d = r/111320.0; dx = d/math.cos(math.radians(lat))
    return ee.Geometry.Rectangle([lon-dx, lat-d, lon+dx, lat+d])
def aef(y, roi): return AEF.filterDate(f"{y}-01-01", f"{y+1}-01-01").filterBounds(roi).mosaic()
def s2n(y, roi):
    c = (S2.filterDate(f"{y}-01-01", f"{y+1}-01-01").filterBounds(roi)
           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
           .map(lambda i: i.updateMask(i.select('SCL').remap([3,8,9,10,11],[0]*5,1)))
           .select(['B2','B3','B4','B8','B11','B12']).median().divide(10000))
    ndvi = c.normalizedDifference(['B8','B4']).rename('nd')
    v = c.addBands(ndvi)
    return v.divide(v.pow(2).reduce(ee.Reducer.sum()).sqrt())
def angle_img(roi, fn, a, b):
    d = fn(a, roi).multiply(fn(b, roi)).reduce(ee.Reducer.sum())
    return d.clamp(-1, 1).acos().multiply(180/math.pi).rename('ang')
# ---- control candidates: 8 directions x {20,30} km, matched on DEM band + DW-2017 mode class
cand = []
for nm, (lat, lon, cy) in SITES.items():
    cand.append((nm, 'SITE', lat, lon))
    for k in (20.0, 30.0):
        for th in range(0, 360, 45):
            dy = k/111.32*math.cos(math.radians(th)); dx = k/111.32*math.sin(math.radians(th))/math.cos(math.radians(lat))
            cand.append((nm, f"c{int(k)}_{th}", lat+dy, lon+dx))
fc = ee.FeatureCollection([ee.Feature(box(la, lo), {'site': s, 'tag': t}) for s, t, la, lo in cand])
ctx = DEM.rename('dem').addBands(DW.filterDate('2017-01-01','2018-01-01').select('label').mode().rename('dw'))
rows = ctx.reduceRegions(collection=fc, reducer=ee.Reducer.mode(), scale=30).getInfo()['features']
ctxd = {(f['properties']['site'], f['properties']['tag']): (f['properties'].get('dem'), f['properties'].get('dw')) for f in rows}
chosen = {}
for nm, (lat, lon, cy) in SITES.items():
    sd, sc = ctxd[(nm, 'SITE')]
    ok = [(s, t, la, lo) for s, t, la, lo in cand if s == nm and t != 'SITE'
          and ctxd.get((s, t), (None, None))[0] is not None
          and abs(ctxd[(s, t)][0]-sd) <= 60 and ctxd[(s, t)][1] == sc]
    if len(ok) < 3:
        ok = [(s, t, la, lo) for s, t, la, lo in cand if s == nm and t != 'SITE'
              and ctxd.get((s, t), (None, None))[0] is not None and abs(ctxd[(s, t)][0]-sd) <= 120]
    chosen[nm] = ok[:6]
    print(f"CTX {nm}: dem={sd:.0f} dw2017={sc} controls_matched={len(ok)} used={len(chosen[nm])}")
# ---- angular change series
out = {}
for nm, (lat, lon, cy) in SITES.items():
    regs = [ee.Feature(box(lat, lon), {'tag': 'SITE'})] + [ee.Feature(box(la, lo), {'tag': t}) for _, t, la, lo in chosen[nm]]
    rfc = ee.FeatureCollection(regs); roi = box(lat, lon, 38000)
    res = {}
    for lbl, fn in (('AEF', aef), ('S2', s2n)):
        res[lbl] = {}
        for a, b in zip(YRS[:-1], YRS[1:]):
            try:
                r = angle_img(roi, fn, a, b).reduceRegions(collection=rfc, reducer=ee.Reducer.mean(), scale=10 if lbl == 'AEF' else 20, tileScale=16).getInfo()['features']
            except Exception as e:
                print(f"  FAIL {nm} {lbl} {b}: {str(e)[:60]}"); continue
            for f in r: res[lbl].setdefault(f['properties']['tag'], {})[f"y{b}"] = f['properties'].get('mean')
    out[nm] = {'reported': cy, 'res': res}
    for lbl in ('AEF', 'S2'):
        d = res[lbl]; site = d.get('SITE', {})
        ser = [(y, site.get(f"y{y}")) for y in YRS[1:] if site.get(f"y{y}") is not None]
        if not ser: print(f"{nm} {lbl}: NO DATA"); continue
        pk = max(ser, key=lambda t: t[1])
        cvals = [v for t, dd in d.items() if t != 'SITE' for v in dd.values() if v is not None]
        cm, cs = (np.mean(cvals), np.std(cvals)) if cvals else (float('nan'),)*2
        z = (pk[1]-cm)/cs if cs == cs and cs > 0 else float('nan')
        print(f"{nm} {lbl}: rep={cy} peak={pk[0]} ang={pk[1]:.2f} ctrl={cm:.2f}+-{cs:.2f} z={z:.1f} n_ctrl={len(d)-1} series=" +
              ",".join(f"{y}:{v:.1f}" for y, v in ser))
json.dump(out, open('/d/yj_projects/workspace_yj/Alphaearth/aef_explore/scratch/TH01_t2_out.json','w'))
