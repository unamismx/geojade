import json
from pathlib import Path

root=Path(__file__).parent
geo=json.loads(Path('/tmp/admin1.geojson').read_text())

def xy(p):
    return ((p[0]+118)*25,(33-p[1])*(500/19))

def simplify(points,tolerance=1.5):
    if len(points)<=3:return points
    a,b=points[0],points[-1];dx=b[0]-a[0];dy=b[1]-a[1];den=(dx*dx+dy*dy)**.5
    distances=[abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/den if den else 0 for p in points]
    i=max(range(len(points)),key=distances.__getitem__)
    if distances[i]>tolerance:return simplify(points[:i+1],tolerance)[:-1]+simplify(points[i:],tolerance)
    return [a,b]

def ring(coords):
    # GeoJSON rings repeat their first vertex at the end. Remove that duplicate
    # before Douglas-Peucker; otherwise the baseline has zero length and the
    # whole state collapses to a single point.
    raw=[xy(p) for p in coords]
    if len(raw)>1 and raw[0]==raw[-1]:raw=raw[:-1]
    pts=simplify(raw)
    return 'M'+'L'.join(f'{round(x)},{round(y)}' for x,y in pts)+'Z' if pts else ''

def path_for(geometry):
    c=geometry['coordinates']
    if geometry['type']=='Polygon':return ''.join(ring(r) for r in c)
    return ''.join(ring(r) for poly in c for r in poly)

paths={}; centers={}; names={}
for f in geo['features']:
    p=f['properties']
    if p.get('adm0_a3')!='MEX' or not p.get('name'):continue
    code=p['iso_3166_2'].replace('MX-','')
    name='Ciudad de México' if p['name']=='Distrito Federal' else (p.get('name_es') or p['name'])
    paths[code]=path_for(f['geometry'])
    centers[code]=[(p['longitude']+118)*25,(33-p['latitude'])*(500/19)]
    names[code]=name

(root/'mexico-map.js').write_text(
    'window.MEXICO_PATHS='+json.dumps(paths,separators=(',',':'))+';\n'+
    'window.MEXICO_CENTERS='+json.dumps(centers,separators=(',',':'))+';\n'+
    'window.MEXICO_NAMES='+json.dumps(names,ensure_ascii=False,separators=(',',':'))+';\n')
