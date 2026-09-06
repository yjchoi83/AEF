import ee; ee.Initialize(project='alpha-earth-app')
mb=ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_integration_v1')
b=mb.bandNames().getInfo(); print('MB',len(b),b[:2],b[-2:])
sv=ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection9/mapbiomas_collection90_secondary_vegetation_age_v1')
s=sv.bandNames().getInfo(); print('SV',len(s),s[:2],s[-2:])
for n in ['DeforestationYear','DegradationYear']:
    ic=ee.ImageCollection('projects/JRC/TMF/v1_2024/'+n)
    print(n, ic.size().getInfo(), ic.first().bandNames().getInfo())
h=ee.Image('UMD/hansen/global_forest_change_2025_v1_13'); print('H', h.bandNames().getInfo())
