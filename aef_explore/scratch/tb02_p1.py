import sys, time; sys.path.insert(0,'scratch')
from aefkit import *
import ee, pandas as pd, numpy as np

ROIS = {  # name: (lon0,lat0,lon1,lat1, group)
 'CD_congo': (23.0,0.0,23.5,0.5,'AF'), 'ZM_miombo': (27.0,-13.7,27.5,-13.2,'AF'),
 'BR_para':  (-55.5,-6.0,-55.0,-5.5,'SA'), 'BO_chiq': (-62.0,-16.5,-61.5,-16.0,'SA'),
 'DE_bav':   (11.0,48.5,11.5,49.0,'EU'), 'US_mo':   (-92.5,37.5,-92.0,38.0,'US'),
}
YRS = list(range(2017,2026))
H = ee.Image('UMD/hansen/global_forest_change_2025_v1_13')
DW = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')

def dwmode(y, roi):
    return DW.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).select('label').reduce(ee.Reducer.mode())

def s1c(y, roi):
    c = (ee.ImageCollection('COPERNICUS/S1_GRD').filterDate(f'{y}-01-01',f'{y+1}-01-01')
         .filterBounds(roi).filter(ee.Filter.eq('instrumentMode','IW'))
         .filter(ee.Filter.listContains('transmitterReceiverPolarisation','VV')))
    return c.select('VV').count().unmask(0).rename(f's1_{y}')

def s2c(y, roi):
    c = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate(f'{y}-01-01',f'{y+1}-01-01')
         .filterBounds(roi).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',60))
         .map(lambda i: i.updateMask(i.select('QA60').bitwiseAnd((1<<10)|(1<<11)).eq(0))))
    return c.select('B4').count().unmask(0).rename(f's2_{y}')

def era(y):
    c = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR').filterDate(f'{y}-01-01',f'{y+1}-01-01')
    return (c.select('total_precipitation_sum').sum().rename(f'pr_{y}')
             .addBands(c.select('temperature_2m').mean().rename(f'tas_{y}')))

allrows=[]
for nm,(a,b,c,d,grp) in ROIS.items():
    t0=time.time(); roi = ee.Geometry.Rectangle([a,b,c,d])
    dw18, dw24 = dwmode(2018,roi), dwmode(2024,roi)
    stab = (H.select('lossyear').unmask(0).eq(0)
            .And(H.select('gain').unmask(0).eq(0)).And(H.select('datamask').eq(1))
            .And(dw18.eq(dw24))
            .And(dw24.neq(0)).And(dw24.neq(6)).And(dw24.neq(8)))
    img = ee.Image(0).rename('dummy')
    for y1,y2 in zip(YRS[:-1],YRS[1:]):
        img = img.addBands(angle(y1,y2,roi).rename(f'ang_{y2}'))
    for y in YRS: img = img.addBands(s1c(y,roi)).addBands(s2c(y,roi)).addBands(era(y))
    img = img.addBands(dw24.rename('dwc')).updateMask(stab)
    df = samp(img, roi, n=900, scale=10)
    df['roi']=nm; df['grp']=grp; allrows.append(df)
    print(nm, len(df), round(time.time()-t0,1), 's', flush=True)
out = pd.concat(allrows, ignore_index=True)
out.to_csv('scratch/tb02_p1.csv', index=False)
print('total', out.shape)
# GEE check: GRACE mascon coverage
g = ee.ImageCollection('NASA/GRACE/MASS_GRIDS_V04/MASCON')
print('GRACE n=', g.size().getInfo(), g.aggregate_min('system:time_start').getInfo(),
      g.aggregate_max('system:time_start').getInfo())
