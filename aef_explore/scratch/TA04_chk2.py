import ee,time,random
for a in range(40):
    try: ee.Initialize(); break
    except Exception as e: time.sleep(20+random.random()*20)
def rt(f,tag):
    for a in range(30):
        try: return f()
        except Exception as e:
            if '429' in str(e) or 'Too Many' in str(e): time.sleep(20+random.random()*25); continue
            print(tag,"ERR",str(e)[:150]); return None
    print(tag,"GIVEUP"); return None
fc=ee.FeatureCollection("projects/sat-io/open-datasets/global-mining/global_mining_polygons")
for k,b in {"AMZ":[-58.0,-8.0,-54.0,-4.0],"GHA":[-3.2,4.9,-0.9,7.2]}.items():
    r=ee.Geometry.Rectangle(b); s=fc.filterBounds(r)
    n=rt(lambda: s.size().getInfo(),k)
    print(k,"n_polys",n,flush=True)
    if n:
        f=rt(lambda: s.first().getInfo(),k)
        if f: print(k,"props",list(f['properties'].keys()),flush=True)
        ar=rt(lambda: s.geometry().area(1000).getInfo(),k)
        if ar: print(k,"area_km2",round(ar/1e6,1),flush=True)
