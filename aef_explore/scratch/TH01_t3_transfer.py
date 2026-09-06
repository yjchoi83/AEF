import ee, math, numpy as np, json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
ee.Initialize(project='alpha-earth-app')
AEF = ee.ImageCollection("GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL")
DW  = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1"); S2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
WC  = ee.ImageCollection("ESA/WorldCover/v200").first().select('Map')
Y = 2021   # WorldCover v200 epoch -> AEF year 2021 (label/embedding year aligned, PROMPT 3.5)
ROK = [127.10, 37.35, 128.40, 38.15]; DPRK = [126.20, 38.75, 127.50, 39.55]
# 6 classes: 0 water 1 forest 2 grass/bare/shrub 3 wetland 4 cropland 5 built
WCMAP = ([10,20,30,40,50,60,70,80,90,95,100], [1,2,2,4,5,2,2,0,3,3,2])
DWMAP = ([0,1,2,3,4,5,6,7,8], [0,1,2,3,4,2,5,2,2])
LAB = WC.remap(*WCMAP).rename('lab')
def aef(y, roi): return AEF.filterDate(f"{y}-01-01", f"{y+1}-01-01").filterBounds(roi).mosaic()
def s2n(y, roi):
    c = (S2.filterDate(f"{y}-01-01", f"{y+1}-01-01").filterBounds(roi)
           .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
           .map(lambda i: i.updateMask(i.select('SCL').remap([3,8,9,10,11],[0]*5,1)))
           .select(['B2','B3','B4','B8','B11','B12']).median().divide(10000))
    return c.addBands(c.normalizedDifference(['B8','B4']).rename('nd'))
def grab(bb, n_per, tag):
    x0,y0,x1,y1 = bb; pts = None
    for i in range(3):
        for j in range(3):
            t = ee.Geometry.Rectangle([x0+(x1-x0)*i/3, y0+(y1-y0)*j/3, x0+(x1-x0)*(i+1)/3, y0+(y1-y0)*(j+1)/3])
            s = LAB.stratifiedSample(numPoints=n_per, classBand='lab', region=t, scale=30,
                                     seed=7, geometries=True, dropNulls=True, tileScale=4)
            pts = s if pts is None else pts.merge(s)
    roi = ee.Geometry.Rectangle(bb)
    dwl = DW.filterDate(f"{Y}-01-01", f"{Y+1}-01-01").filterBounds(roi).select('label').mode().remap(*DWMAP).rename('dw')
    stk = aef(Y, roi).rename([f"e{k}" for k in range(64)]).addBands(s2n(Y, roi)).addBands(dwl)
    fs = stk.sampleRegions(collection=pts, properties=['lab'], scale=10, tileScale=8, geometries=True).getInfo()['features']
    rows = []
    for f in fs:
        p = f['properties']; lon, lat = f['geometry']['coordinates']
        r = [p.get(f"e{k}") for k in range(64)] + [p.get(b) for b in ('B2','B3','B4','B8','B11','B12','nd')] \
            + [p.get('lab'), p.get('dw'), math.floor(lon/0.12), math.floor(lat/0.12)]
        if None not in r: rows.append(r)
    a = np.array(rows, dtype=float)
    print(f"{tag}: n={len(a)} (raw {len(fs)})")
    return a[:,:64], a[:,64:71], a[:,71].astype(int), a[:,72].astype(int), np.array([f"{int(u)}_{int(v)}" for u,v in a[:,73:75]])
Xa, Xs, y, dw, g = grab(ROK, 90, 'ROK')
Xa2, Xs2, y2, dw2, g2 = grab(DPRK, 70, 'DPRK')
print(f"blocks ROK={len(set(g))} DPRK={len(set(g2))}")
print("ROK bal(WC) ", {int(k): int(v) for k,v in zip(*np.unique(y, return_counts=True))})
print("DPRK bal(WC)", {int(k): int(v) for k,v in zip(*np.unique(y2, return_counts=True))})
res = {}
for lbl,(X,X2) in (('AEF',(Xa,Xa2)),('S2',(Xs,Xs2))):
    sc = StandardScaler().fit(X); Z, Z2 = sc.transform(X), sc.transform(X2)
    accs = []
    for tr,te in GroupKFold(n_splits=5).split(Z,y,g):
        m = LogisticRegression(max_iter=4000).fit(Z[tr], y[tr]); accs.append((m.predict(Z[te])==y[te]).mean())
    m = LogisticRegression(max_iter=4000).fit(Z, y); p2 = m.predict(Z2); p1 = m.predict(Z)
    a_wc = (p2==y2).mean(); a_dw = (p2==dw2).mean(); ceil = (y2==dw2).mean()
    cls = sorted(set(y)|set(y2))
    tv = 0.5*sum(abs((p2==c).mean()-(y2==c).mean()) for c in cls)
    res[lbl] = dict(rok_cv=float(np.mean(accs)), sd=float(np.std(accs)), folds=[round(a,3) for a in accs],
                    agr_wc=float(a_wc), agr_dw=float(a_dw), dw_wc_ceiling=float(ceil), tv=float(tv))
    print(f"{lbl}: ROK 5-fold spatial OA={np.mean(accs):.3f}+-{np.std(accs):.3f} folds={[round(a,3) for a in accs]}")
    print(f"{lbl}: DPRK agr(WC)={a_wc:.3f} agr(DW)={a_dw:.3f} | WC-vs-DW ceiling on DPRK={ceil:.3f} | TV(pred,WC)={tv:.3f}")
    print(f"{lbl}: ROK-vs-DPRK agreement gap (in-region OA - DPRK agr(WC)) = {np.mean(accs)-a_wc:+.3f}")
U = Xa/np.linalg.norm(Xa,axis=1,keepdims=True); U2 = Xa2/np.linalg.norm(Xa2,axis=1,keepdims=True)
C = np.stack([(lambda v: v/np.linalg.norm(v))(U[y==c].mean(0)) for c in sorted(set(y))])
m1, m2 = (U@C.T).max(1).mean(), (U2@C.T).max(1).mean()
kap = lambda A: (lambda rb,d: rb*(d-rb**2)/(1-rb**2))(np.linalg.norm(A.mean(0)), A.shape[1])
print(f"AEF sphere: mean max-cos to ROK centroids ROK={m1:.3f} DPRK={m2:.3f} drop={m1-m2:+.3f}")
print("AEF vMF kappa ROK/DPRK: " + " ".join(f"c{c}:{kap(U[y==c]):.0f}/{kap(U2[y2==c]):.0f}"
      for c in sorted(set(y)) if (y2==c).sum()>25 and (y==c).sum()>25))
res['shift'] = dict(maxcos_rok=float(m1), maxcos_dprk=float(m2), n_rok=len(y), n_dprk=len(y2))
json.dump(res, open('/d/yj_projects/workspace_yj/Alphaearth/aef_explore/scratch/TH01_t3_out.json','w'))
