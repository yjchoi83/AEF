import sys; sys.path.insert(0,'scratch')
from aefkit import *
AGE='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1'
INT='projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1'
ib=ee.Image(INT).bandNames().getInfo(); print('INT bands', ib[:2], '...', ib[-3:], len(ib))
age=ee.Image(AGE).select('secondary_vegetation_age_2023').unmask(0)
mature=ee.Image(INT).select('classification_2023').eq(3).And(age.eq(0))
cands={'BRAGANTINA_PA':[-48.6,-2.4,-47.4,-1.2],'RONDONIA':[-63.2,-10.6,-62.0,-9.4],
       'ATL_SP_big':[-47.6,-24.2,-46.4,-23.0]}
for k,b in cands.items():
    roi=ee.Geometry.Rectangle(b)
    bins=(age.gte(1).And(age.lte(3)).multiply(1)
      .add(age.gte(4).And(age.lte(6)).multiply(2)).add(age.gte(7).And(age.lte(10)).multiply(3))
      .add(age.gte(11).And(age.lte(15)).multiply(4)).add(age.gte(16).And(age.lte(25)).multiply(5))
      .add(age.gte(26).multiply(6)).add(mature.multiply(7)).rename('bin'))
    h=bins.reduceRegion(ee.Reducer.frequencyHistogram(),roi,scale=100,maxPixels=1e9).getInfo()['bin']
    print(k,{int(float(a)):int(v) for a,v in sorted(h.items(),key=lambda x:float(x[0]))})
