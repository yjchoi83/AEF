import sys; sys.path.insert(0,'scratch')
from aefkit import *
ROIS={'ET_somali':[42.6,6.6,43.1,7.1],'BR_caat':[-40.5,-9.5,-40.0,-9.0],
 'SN_ferlo':[-15.2,15.0,-14.7,15.5],'US_az':[-110.3,32.2,-109.8,32.7],
 'KE_marsa':[37.4,1.9,37.9,2.4],'ZW_mata':[27.5,-20.3,28.0,-19.8]}
DW=ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").select('label')
FE=['B2','B3','B4','B8','B11','B12','NDVI','NBR']
def dwm(y,r): return DW.filterDate(f"{y}-01-01",f"{y+1}-01-01").filterBounds(r).mode()
out=[]
for k,b in ROIS.items():
    r=ee.Geometry.Rectangle(b)
    a,c=dwm(2019,r),dwm(2020,r)
    veg=a.remap([1,2,4,5,6,7],[1,1,1,1,1,1],0).eq(1).And(c.remap([1,2,4,5,6,7],[1,1,1,1,1,1],0).eq(1))
    strat=a.neq(c).And(veg).rename('strat').unmask(0)
    img=(angle(2019,2020,r).addBands(ee.Image.cat(
        [s2(y,r).select(FE,[f'{x}_{y}' for x in FE]) for y in (2019,2020)])))
    try:
        df=samp(img,r,strata=strat,classes=[0,1],per_class=300,scale=10)
    except Exception as e:
        print(k,'FAIL',str(e)[:80],flush=True); continue
    df['roi']=k; out.append(df); print(k,len(df),df.groupby('strat').angle_deg.median().round(2).to_dict(),flush=True)
d=pd.concat(out,ignore_index=True)
V={}
for y in (2019,2020):
    v=d[[f'{x}_{y}' for x in FE]].values; n=np.linalg.norm(v,axis=1,keepdims=True); V[y]=v/np.where(n==0,np.nan,n)
d['s2_angle']=np.degrees(np.arccos(np.clip((V[2019]*V[2020]).sum(1),-1,1)))
d.to_csv('scratch/te02_chg.csv',index=False)
print("AEF angle by strat:"); print(d.groupby('strat').angle_deg.describe()[['count','25%','50%','75%']].round(2))
print("S2  angle by strat:"); print(d.groupby('strat').s2_angle.describe()[['count','25%','50%','75%']].round(2))
