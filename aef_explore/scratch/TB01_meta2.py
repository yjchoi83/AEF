import ee, numpy as np; ee.Initialize(project='alpha-earth-app')
Y=2021
for TAG,box in (('BR',[-55.5,-7.5,-54.5,-6.5]),('CG',[23.0,0.0,24.0,1.0])):
    roi=ee.Geometry.Rectangle(box); geo='sa_' if TAG=='BR' else 'africa_'
    radd=ee.ImageCollection('projects/radar-wur/raddalert/v1').filterMetadata('layer','contains','alert')\
         .filter(ee.Filter.stringContains('system:index',geo)).sort('system:time_end',False).first()
    A,D=radd.select('Alert'),radd.select('Date')
    gfc=ee.Image('UMD/hansen/global_forest_change_2025_v1_13')
    tc,ly=gfc.select('treecover2000'),gfc.select('lossyear')
    stable=tc.gt(80).And(ly.unmask(0).eq(0)).And(A.unmask(0).eq(0)).selfMask()
    print(TAG,'stable px@60m',stable.reduceRegion(ee.Reducer.count(),roi,60,maxPixels=1e9).getInfo())
    doy=D.subtract((Y-2000)*1000)
    clr=A.eq(3).And(doy.gte(1)).And(doy.lte(366)).And(tc.gt(50)).And(ly.eq(Y-2000)).selfMask()
    print(TAG,'clear px@60m',clr.reduceRegion(ee.Reducer.count(),roi,60,maxPixels=1e9).getInfo())
    AEF=ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
    aef=lambda y: AEF.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).mosaic()
    e0,e1,e2=aef(Y-1),aef(Y),aef(Y+1)
    dd=lambda a,b,n: a.multiply(b).reduce(ee.Reducer.sum()).rename(n)
    uv,x,yy=dd(e0,e2,'uv'),dd(e0,e1,'x'),dd(e1,e2,'yy')
    sep=uv.clamp(-1,1).acos().multiply(180/np.pi).rename('sep')
    inpl=x.pow(2).subtract(x.multiply(yy).multiply(uv).multiply(2)).add(yy.pow(2))\
         .divide(ee.Image(1).subtract(uv.pow(2)).max(1e-9))
    res=ee.Image(1).subtract(inpl).max(0).sqrt().rename('res')
    st=sep.addBands(res).updateMask(stable)
    r=st.reduceRegion(ee.Reducer.percentile([10,50,90]).combine(ee.Reducer.mean(),None,True),roi,60,maxPixels=1e9,tileScale=8).getInfo()
    print(TAG,'STABLE-forest AEF:',{k:round(v,3) for k,v in r.items() if v is not None})
