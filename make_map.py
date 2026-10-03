import json
from pathlib import Path
from urllib.request import urlopen

root=Path(__file__).parent
source=root/'world.geojson'
if not source.exists():
    source.write_bytes(urlopen('https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson').read())
geo=json.loads(source.read_text())

def point(p):
    x=(p[0]+180)*1000/360
    y=(90-p[1])*500/180
    return f'{round(x)},{round(y)}'

def ring(coords):
    return 'M'+'L'.join(point(p) for p in coords)+'Z' if coords else ''

def geometry_path(geometry):
    coords=geometry['coordinates']
    if geometry['type']=='Polygon':
        return ''.join(ring(r) for r in coords)
    if geometry['type']=='MultiPolygon':
        return ''.join(ring(r) for poly in coords for r in poly)
    return ''

paths={}
centers={}
for feature in geo['features']:
    props=feature['properties']
    if props.get('ADMIN')=='Antarctica':continue
    code=props.get('ADM0_A3')
    path=geometry_path(feature['geometry'])
    if code and path:
        paths[code]=path
        centers[code]=[(props['LABEL_X']+180)*1000/360,(90-props['LABEL_Y'])*500/180]

(root/'map-data.js').write_text(
    'window.MAP_PATHS = '+json.dumps(paths,separators=(',',':'))+';\n'+
    'window.MAP_CENTERS = '+json.dumps(centers,separators=(',',':'))+';\n')
