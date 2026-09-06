import sys; sys.path.insert(0,'scratch')
from aefkit import *
roi = ee.Geometry.Rectangle([-55.5,-6.0,-55.0,-5.5])   # Para, Amazon frontier
hansen = ee.Image("UMD/hansen/global_forest_change_2025_v1_13")
loss = hansen.select('lossyear')
lbl = loss.unmask(0).eq(20).rename('loss20')  # loss in 2020
img = aef(2021, roi).addBands(angle(2019,2021,roi)).addBands(lbl)
df = samp(img, roi, n=3000)
df['blk'] = blocks(df)
print("n=",len(df),"pos=",int(df.loss20.sum()),"blocks=",df.blk.nunique())
print("AEF probe AUC:", probe(df, AEF_BANDS, 'loss20', df['blk']))
print("angle-only AUC:", probe(df, ['angle_deg'], 'loss20', df['blk']))
