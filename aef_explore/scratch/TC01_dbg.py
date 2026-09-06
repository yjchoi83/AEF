import sys; sys.path.insert(0,'scratch')
from aefkit import *
roi=ee.Geometry.Rectangle([-55.5,-9.0,-54.5,-8.0])
wc=ee.Image("ESA/WorldCover/v200/2021").select('Map').rename('y')
def t(tag, img, **kw):
    try:
        f=img.addBands(wc).stratifiedSample(region=roi, classBand='y', scale=10,
            seed=1, geometries=True, dropNulls=True, **kw)
        print(tag, len(f.getInfo()['features']))
    except Exception as e: print(tag,'FAIL',str(e)[:90])
t('lblonly', wc.rename('x'), numPoints=0, classValues=[10,20,30], classPoints=[500,500,500])
t('lbl_ts16', wc.rename('x'), numPoints=0, classValues=[10,20,30], classPoints=[500,500,500], tileScale=16)
t('aef', aef(2021,roi), numPoints=0, classValues=[10,20,30], classPoints=[500,500,500], tileScale=16)
