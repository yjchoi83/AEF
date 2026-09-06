import sys; sys.path.insert(0,'scratch')
from aefkit import *
ROIS={'ET_somali':[42.6,6.6,43.1,7.1],'BR_caat':[-40.5,-9.5,-40.0,-9.0],
 'SN_ferlo':[-15.2,15.0,-14.7,15.5],'US_az':[-110.3,32.2,-109.8,32.7],
 'KE_marsa':[37.4,1.9,37.9,2.4],'ZW_mata':[27.5,-20.3,28.0,-19.8]}
YS=list(range(2019,2026)); ALL=list(range(2017,2026))
E5=ee.ImageCollection("ECMWF/ERA5_LAND/MONTHLY_AGGR")
S1=ee.ImageCollection("COPERNICUS/S1_GRD").filter(ee.Filter.eq('instrumentMode','IW')).filter(
    ee.Filter.listContains('transmitterReceiverPolarisation','VV'))
H=ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
WC=ee.Image("ESA/WorldCover/v200/2021").select('Map')
DW=ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").select('label')
def dwmode(y,r): return DW.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(r).mode()
def cnt(col,band,y,r):
    c=col.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(r)
    return ee.Image(ee.Algorithms.If(c.size().gt(0),c.select(band).count(),ee.Image(0))).rename('c').toFloat()
def s2col(y,r):
    def m(i):
        s=i.select('QA60'); return i.updateMask(s.bitwiseAnd(1<<10|1<<11).eq(0))
    return ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterDate(
        f"{y}-01-01",f"{y+1}-01-01").filterBounds(r).map(m)
def clim(r):
    pr=[E5.filterDate(f"{y}-01-01",f"{y+1}-01-01").select('total_precipitation_sum').sum() for y in ALL]
    tm=[E5.filterDate(f"{y}-01-01",f"{y+1}-01-01").select('temperature_2m').mean() for y in ALL]
    P=ee.ImageCollection(pr); T=ee.ImageCollection(tm)
    pm,ps=P.mean(),P.reduce(ee.Reducer.stdDev()); tmn,ts=T.mean(),T.reduce(ee.Reducer.stdDev())
    out=[]
    for i,y in enumerate(ALL):
        if y not in YS: continue
        out.append(pr[i].subtract(pm).divide(ps).rename(f'pz{y}'))
        out.append(tm[i].subtract(tmn).divide(ts).rename(f'tz{y}'))
    return ee.Image.cat(out)
rows=[]
for k,b in ROIS.items():
    r=ee.Geometry.Rectangle(b)
    stab=(H.select('lossyear').unmask(0).eq(0)
      .And(H.select('gain').unmask(0).eq(0)).And(H.select('datamask').unmask(0).eq(1))
      .And(WC.remap([10,20,30],[1,1,1],0).eq(1))
      .And(dwmode(2018,r).eq(dwmode(2024,r))).And(dwmode(2018,r).remap([1,2,5],[1,1,1],0).eq(1)))
    bands=[angle(y-1,y,r).rename(f'a{y}') for y in YS]
    bands+=[cnt(S1,'VV',y,r).rename(f's1_{y}') for y in YS]
    bands+=[cnt(s2col(y,r),'B4',y,r).rename(f's2_{y}') for y in YS]
    img=ee.Image.cat(bands).addBands(clim(r)).addBands(dwmode(2018,r).rename('dw')).updateMask(stab)
    df=samp(img,r,n=2000); df['roi']=k; rows.append(df)
    df.to_csv(f'scratch/te02_p_{k}.csv',index=False)
    print(k,len(df),flush=True)
d=pd.concat(rows,ignore_index=True); d.to_csv('scratch/te02_panel.csv',index=False)
print(d.shape); print(d.groupby('roi')[[f'a{y}' for y in YS]].median().round(2))
