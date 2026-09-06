import sys; sys.path.insert(0,'scratch')
from aefkit import *
import numpy as np
roi = ee.Geometry.Rectangle([-55.6,-6.2,-54.9,-5.5])
AC = ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').filterBounds(roi).mosaic()
pre, post = AC.select('Dec2019'), AC.select('Dec2022')
lab = (pre.eq(1).And(post.eq(1)).multiply(0)
       .where(pre.eq(1).And(post.eq(2)), 1)
       .where(pre.eq(1).And(post.eq(3)), 2)
       .where(pre.neq(1), 9)).rename('y').unmask(9)
def qm(i):
    return i.updateMask(i.select('quality_flag').eq(1)).updateMask(i.select('degrade_flag').eq(0))
G = (ee.ImageCollection('LARSE/GEDI/GEDI02_A_002_MONTHLY')
     .filterBounds(roi).filterDate('2022-01-01','2024-01-01').map(qm)
     .select(['rh98','rh50']).mosaic())
stack = G.addBands(angle(2019,2022,roi)).addBands(lab)
# sample only where GEDI exists: stratify on label but require rh98 -> dropNulls in samp
df = samp(stack, roi, scale=25, strata=lab, classes=[0,1,2], per_class=3000, seed=11)
df = df[df.y.isin([0,1,2])].dropna(subset=['rh98','angle_deg'])
print('GEDI n=', len(df), df.y.value_counts().to_dict())
if len(df) > 50:
    df['blk'] = blocks(df, 0.1)
    ref = df.loc[df.y==0,'rh98'].median()
    df['hloss'] = ref - df.rh98
    for c in [0,1,2]:
        s = df[df.y==c]
        if len(s) > 5:
            print('cls',c,'n',len(s),'rh98 med %.1f  hloss med %.1f  angle med %.2f' %
                  (s.rh98.median(), s.hloss.median(), s.angle_deg.median()))
    ch = df[df.y>0]
    if len(ch) > 20:
        print('spearman(angle,hloss) all=%.3f  changed-only=%.3f (n=%d)' % (
            df[['angle_deg','hloss']].corr(method='spearman').iloc[0,1],
            ch[['angle_deg','hloss']].corr(method='spearman').iloc[0,1], len(ch)))
        print('ridge rh98 from AEF? skipped (n small)')
