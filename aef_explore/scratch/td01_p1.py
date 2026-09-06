import sys; sys.path.insert(0,'scratch')
from aefkit import *
import numpy as np, pandas as pd
roi = ee.Geometry.Rectangle([-55.6,-6.2,-54.9,-5.5])
AC = ee.ImageCollection('projects/JRC/TMF/v1_2024/AnnualChanges').filterBounds(roi).mosaic()
pre, post = AC.select('Dec2019'), AC.select('Dec2022')
# graded label: 0 intact, 1 degraded, 2 deforested (all from undisturbed 2019 baseline)
lab = (pre.eq(1).And(post.eq(1)).multiply(0)
       .where(pre.eq(1).And(post.eq(2)), 1)
       .where(pre.eq(1).And(post.eq(3)), 2)
       .where(pre.neq(1), 9)).rename('y').unmask(9)
stack = (aef(2022, roi).addBands(s2(2022, roi))
         .addBands(angle(2019, 2022, roi)).addBands(lab))
df = samp(stack, roi, scale=10, strata=lab, classes=[0,1,2], per_class=1000, seed=7)
df = df[df.y.isin([0,1,2])].copy()
df['blk'] = blocks(df, size=0.1)
print('n=', len(df), 'balance=', df.y.value_counts().to_dict(), 'blocks=', df.blk.nunique())
for name, F in [('AEF64', AEF_BANDS), ('S2comp', S2_BANDS), ('angle', ['angle_deg']),
                ('AEF+angle', AEF_BANDS+['angle_deg'])]:
    print(name, probe(df, F, 'y', df['blk'], folds=5))
# per-class angle medians / overlap
for c in [0,1,2]:
    a = df.loc[df.y==c,'angle_deg'].dropna()
    print('cls', c, 'n', len(a), 'angle med %.2f q25 %.2f q75 %.2f' % (a.median(), a.quantile(.25), a.quantile(.75)))
a0 = df.loc[df.y==0,'angle_deg'].dropna(); a1 = df.loc[df.y==1,'angle_deg'].dropna(); a2 = df.loc[df.y==2,'angle_deg'].dropna()
print('P(deg>intact)=%.3f P(defor>deg)=%.3f' % (
    np.mean(np.random.choice(a1,20000,1) > np.random.choice(a0,20000,1)),
    np.mean(np.random.choice(a2,20000,1) > np.random.choice(a1,20000,1))))
# confusion (pooled out-of-fold, AEF)
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
d = df.dropna(subset=AEF_BANDS+['y']); X,y,g = d[AEF_BANDS].values, d.y.values, d.blk.values
pr = np.zeros_like(y)
for tr,te in GroupKFold(n_splits=5).split(X,y,g):
    pr[te] = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000,class_weight='balanced')).fit(X[tr],y[tr]).predict(X[te])
print('confusion rows=true 0/1/2\n', confusion_matrix(y,pr))
df.to_csv('scratch/td01_p1.csv', index=False)
