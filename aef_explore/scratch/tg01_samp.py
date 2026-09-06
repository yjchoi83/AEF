import sys; sys.path.insert(0,'scratch')
from aefkit import *
roi = ee.Geometry.Rectangle([-55.4,-11.9,-54.4,-10.9])
TMF = ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').mosaic()
lb = TMF.select('Dec2021').unmask(0).rename('tmf')
img = aef(2021, roi).addBands(s2(2021, roi)).addBands(lb)
out = []
for sd in [1,2,3]:
    d = samp(img, roi, n=3000, seed=sd)
    print('seed', sd, d.shape, flush=True)
    out.append(d)
df = pd.concat(out, ignore_index=True).drop_duplicates(subset=['lon','lat'])
df.to_csv('scratch/tg01_samples.csv', index=False)
print('TOTAL', df.shape)
print(df.tmf.value_counts(normalize=True).round(4).to_dict())
