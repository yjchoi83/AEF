import sys; sys.path.insert(0,'scratch')
from aefkit import *
import json
NAME, BOX = sys.argv[1], [float(x) for x in sys.argv[2].split(',')]
KEEP = [int(x) for x in sys.argv[3].split(',')]
Y = 2021
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map').unmask(0).rename('y')

def stack(roi):
    a = aef(Y, roi)
    s = s2(Y, roi)
    ctx = s.reduceNeighborhood(ee.Reducer.mean(), ee.Kernel.circle(15, 'pixels')) \
           .rename([b + '_ctx' for b in S2_BANDS])
    return a.addBands(s).addBands(ctx).addBands(wc)

CTX_BANDS = [b + '_ctx' for b in S2_BANDS]
SETS = [('AEF64', AEF_BANDS), ('S2', S2_BANDS), ('S2ctx', S2_BANDS + CTX_BANDS)]
cx, cy = (BOX[0]+BOX[2])/2, (BOX[1]+BOX[3])/2
DENSE = [cx-0.1, cy-0.1, cx+0.1, cy+0.1]
LADDER = {'dense': [('rand',None),('0.2km',0.002),('1km',0.01),('5km',0.045),('10km',0.09)],
          'wide':  [('rand',None),('1km',0.01),('5km',0.045),('10km',0.09),('25km',0.225),('50km',0.45)]}
out = {}
for tag, box in [('dense', DENSE), ('wide', BOX)]:
    roi = ee.Geometry.Rectangle(box)
    df = samp(stack(roi), roi, n=3500, seed=7)
    df = df[df.y.isin(KEEP)].reset_index(drop=True)
    bal = df.y.value_counts(normalize=True).round(3).to_dict()
    print(f"[{NAME}/{tag}] n={len(df)} bal={bal} extent_deg={round(box[2]-box[0],2)}")
    rng = np.random.default_rng(0)
    for fname, feats in SETS:
        row = []
        for rung, sz in LADDER[tag]:
            g = pd.Series(rng.integers(0, 5, len(df)).astype(str), index=df.index) if sz is None \
                else blocks(df, size=sz)
            m, sd, per, n = probe(df, feats, 'y', g, folds=5)
            row.append((rung, round(m,3), round(sd,3), g.nunique(), len(per)))
        print(f"  {fname:6s} " + "  ".join(f"{r}={m:.3f}(sd{s:.3f},b{b},k{k})" for r,m,s,b,k in row))
        out[f"{tag}|{fname}"] = row
json.dump(out, open(f"scratch/tf02_{NAME}.json", "w"))
