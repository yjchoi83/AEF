import ee; ee.Initialize(project='alpha-earth-app')
roi = ee.Geometry.Rectangle([-55.4,-5.8,-54.6,-5.0])   # Para, BR
radd = ee.ImageCollection('projects/radar-wur/raddalert/v1').filterMetadata('layer','contains','alert')
print('RADD imgs:', radd.size().getInfo())
sa = radd.filterMetadata('geography','equals','sa')
print('sa n:', sa.size().getInfo(), sa.aggregate_array('system:index').getInfo()[-2:])
im = ee.Image(sa.sort('system:time_end',False).first())
print('bands:', im.bandNames().getInfo(), 'idx:', im.get('system:index').getInfo())
d = im.select('Date'); a = im.select('Alert')
print('Date stats:', d.updateMask(d.gt(0)).reduceRegion(ee.Reducer.minMax(),roi,30,maxPixels=1e9).getInfo())
print('Alert hist:', a.reduceRegion(ee.Reducer.frequencyHistogram(),roi,60,maxPixels=1e9).getInfo())
# decode YYDDD assumption on confirmed 2021 alerts
m21 = a.eq(3).And(d.gte(21001)).And(d.lte(21366))
print('conf2021 px(60m):', m21.selfMask().reduceRegion(ee.Reducer.count(),roi,60,maxPixels=1e9).getInfo())
samp = d.updateMask(m21).sample(roi,60,numPixels=8,seed=3).aggregate_array('Date').getInfo()
import datetime
for v in samp:
    yy,ddd = divmod(int(v),1000)
    print(v,'->',(datetime.date(2000+yy,1,1)+datetime.timedelta(days=ddd-1)).isoformat())
AEF = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
for y in (2020,2021,2022):
    print(y,'AEF imgs over roi:', AEF.filterDate(f'{y}-01-01',f'{y+1}-01-01').filterBounds(roi).size().getInfo())
