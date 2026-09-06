import sys; sys.path.insert(0,'scratch')
from aefkit import *
Y = 2021
wc = ee.Image("ESA/WorldCover/v200/2021").select('Map').unmask(0).rename('y')
CTX = [b+'_ctx' for b in S2_BANDS]
SETS = [('AEF64',AEF_BANDS), ('S2',S2_BANDS), ('S2ctx',S2_BANDS+CTX)]
LAD = [('rand',None),('50m',0.0005),('100m',0.001),('200m',0.002),('500m',0.005),('1km',0.01),('2km',0.02)]
ROIS = {'KE_a':([34.70,0.55,34.74,0.59],[10,20,30,40]), 'MT_b':([-55.30,-11.80,-55.26,-11.76],[10,30,40])}
for name,(box,keep) in ROIS.items():
    roi = ee.Geometry.Rectangle(box)
    s = s2(Y, roi)
    ctx = s.reduceNeighborhood(ee.Reducer.mean(), ee.Kernel.circle(15,'pixels')).rename(CTX)
    df = samp(aef(Y,roi).addBands(s).addBands(ctx).addBands(wc), roi, n=3200, seed=11)
    df = df[df.y.isin(keep)].reset_index(drop=True)
    print(f"[{name}] n={len(df)} bal={df.y.value_counts(normalize=True).round(3).to_dict()} box_deg={round(box[2]-box[0],3)}")
    rng = np.random.default_rng(0)
    for fn,fe in SETS:
        r=[]
        for rung,sz in LAD:
            g = pd.Series(rng.integers(0,5,len(df)).astype(str), index=df.index) if sz is None else blocks(df,size=sz)
            m,sd,per,n = probe(df,fe,'y',g,folds=5)
            r.append((rung,m,sd,g.nunique(),len(per)))
        print(f"  {fn:6s} " + " ".join(f"{a}={b:.3f}(sd{c:.3f},b{d},k{e})" for a,b,c,d,e in r))
    df[['lon','lat']].to_csv(f'scratch/tf02_near_{name}.csv', index=False)
