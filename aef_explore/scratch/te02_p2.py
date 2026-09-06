import sys, os; sys.path.insert(0,'scratch')
from aefkit import *
YS=list(range(2020,2026)); AY=list(range(2019,2026))
FE=['B2','B4','B8','B11','NDVI','NBR']
d=pd.read_csv('scratch/te02_panel.csv')
def uv(y,r):
    i=s2(y,r).select(FE)
    n=i.pow(2).reduce(ee.Reducer.sum()).sqrt()
    return i.divide(n)
for k,g in d.groupby('roi'):
    f=f'scratch/te02_s2_{k}.csv'
    if os.path.exists(f): print('skip',k,flush=True); continue
    g=g.sample(n=min(900,len(g)),random_state=1)
    r=ee.Geometry.Rectangle([g.lon.min()-.01,g.lat.min()-.01,g.lon.max()+.01,g.lat.max()+.01])
    U={y:uv(y,r) for y in AY}
    bands=[]
    for y in YS:
        dot=U[y-1].multiply(U[y]).reduce(ee.Reducer.sum()).clamp(-1,1)
        bands.append(dot.acos().multiply(180/np.pi).rename(f'sa{y}'))
    pts=ee.FeatureCollection([ee.Feature(ee.Geometry.Point([float(a),float(b)]),{'i':int(i)})
         for i,(a,b) in zip(g.index,zip(g.lon,g.lat))])
    import time
    for att in range(4):
        try:
            rr=ee.Image.cat(bands).sampleRegions(collection=pts,scale=10,tileScale=4).getInfo()['features']; break
        except Exception as e:
            print(k,'retry',att,str(e)[:60],flush=True); time.sleep(90); rr=None
    if not rr: continue
    p=pd.DataFrame([x['properties'] for x in rr]).set_index('i'); p['roi']=k
    p.to_csv(f); print(k,len(p),p[[f'sa{y}' for y in YS]].median().round(2).to_dict(),flush=True)
import glob
fs=glob.glob('scratch/te02_s2_*.csv')
if len(fs)>=5:
    pd.concat([pd.read_csv(x,index_col=0) for x in fs]).to_csv('scratch/te02_s2.csv'); print('merged',len(fs))
