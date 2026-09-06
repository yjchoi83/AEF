import ee, json, numpy as np
ee.Initialize(project='alpha-earth-app')
roi = ee.Geometry.Rectangle([-56.0,-7.5,-54.5,-6.0])   # Novo Progresso / BR-163, Para
YRS = list(range(2017,2026)); N=9
H = ee.Image('UMD/hansen/global_forest_change_2025_v1_13'); ly = H.select('lossyear').unmask(0)
DEG = ee.ImageCollection('projects/JRC/TMF/v1_2024/DegradationYear').mosaic().select('constant')
MB = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1')
SV = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1')
FOR=[3]; NF=[15,18,19,20,21,39,41,46,47,48,35,9]
mbF = ee.Image(1); mbN = ee.Image(1)
for y in range(2017,2024):
    c = MB.select('classification_%d'%y)
    mbF = mbF.And(c.remap(FOR,[1],0)); mbN = mbN.And(c.remap(NF,[1]*len(NF),0))
loss = ly.gte(18).And(ly.lte(24)); ryL = ly.add(2000)
deg  = DEG.gte(2018).And(DEG.lte(2023)).And(ly.eq(0)); ryD = DEG
reg = ee.Image(0); ryR = ee.Image(0)
for y in range(2018,2024):
    m = SV.select('secondary_vegetation_age_%d'%y).eq(1).And(reg.Not()).And(ly.eq(0))
    reg = reg.Or(m); ryR = ryR.where(m, y)
sf = H.select('treecover2000').gt(80).And(ly.eq(0)).And(mbF)
snf = mbN.And(ly.eq(0))
strata = ee.Image(0).where(snf,5).where(sf,4).where(reg,3).where(deg,2).where(loss,1).rename('str').selfMask()
refy = ee.Image(0).where(reg,ryR).where(deg,ryD).where(loss,ryL).rename('refy')
def gram(imgs, tag):
    out=[]
    for i in range(N):
        for j in range(i,N):
            out.append(imgs[i].multiply(imgs[j]).reduce(ee.Reducer.sum()).rename('%s%d_%d'%(tag,i,j)))
    return ee.Image.cat(out)
AEF = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
aef = [AEF.filterDate('%d-01-01'%y,'%d-01-01'%(y+1)).filterBounds(roi).mosaic() for y in YRS]
def s2y(y):
    c = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate('%d-01-01'%y,'%d-01-01'%(y+1)).filterBounds(roi)
    def msk(im):
        s=im.select('SCL'); ok=s.neq(3).And(s.neq(8)).And(s.neq(9)).And(s.neq(10)).And(s.neq(1))
        return im.updateMask(ok).divide(10000)
    m = c.map(msk).median()
    ndvi=m.normalizedDifference(['B8','B4']); nbr=m.normalizedDifference(['B8','B12'])
    return ee.Image.cat([ndvi,nbr,m.select('B8'),m.select('B11'),m.select('B12')]).rename(['ndvi','nbr','b8','b11','b12'])
s2 = [s2y(y) for y in YRS]
s2b = ee.Image.cat(s2).rename(['%s_%d'%(b,y) for y in YRS for b in ['ndvi','nbr','b8','b11','b12']])
stack = gram(aef,'a').addBands(s2b).addBands(refy).addBands(strata)
pts = strata.addBands(refy).stratifiedSample(numPoints=1000, classBand='str', region=roi, scale=30, seed=7, geometries=True, tileScale=4)
rows=[]
for k in range(1,6):
    sub = pts.filter(ee.Filter.eq('str',k))
    fc = stack.sampleRegions(collection=sub, scale=10, tileScale=4, geometries=True)
    f = fc.getInfo()['features']
    for ft in f:
        p=ft['properties']; c=ft['geometry']['coordinates']; p['lon']=c[0]; p['lat']=c[1]; rows.append(p)
    print('stratum',k,'n=',len(f), flush=True)
json.dump(rows, open('TB04_rows.json','w'))
print('total', len(rows))
