"""Check actual boundary STL sockets/keys, including wrong-bit rejection."""
from pathlib import Path
from itertools import product
import json
import trimesh
from blue_tiles_3d import symbol,moved,intersection_volume
P=Path(__file__).parent/'bounded-solids'
checks=[]
for name in ('edge-00','edge-01','edge-10','edge-11','corner-0','corner-1'):
    mesh=trimesh.load_mesh(P/f'{name}.stl')
    corner=name.startswith('corner')
    bits=[int(x) for x in name.split('-')[1]]
    face=((0,0),(0,bits[0])) if corner else ((0,0),tuple(bits))
    inputs=[(40,40,bits[0])] if corner else [(20,40,bits[0]),(40,40,bits[1])]
    for x,y,bit in inputs:
        assert intersection_volume(mesh,moved(symbol(bit),(x,y,0)))<.003
        assert intersection_volume(mesh,moved(symbol(1-bit),(x,y,0)))>1
    # Exterior underside is solid: these are dedicated source variants,
    # not ordinary four-input blue tiles shifted beyond the board.
    for r,c in product(range(2),repeat=2):
        if (r==1 and (not corner or c==1)):continue
        probe=moved(symbol(0),((20,40)[c],(20,40)[r],0))
        assert abs(intersection_volume(mesh,probe)-probe.volume)<.003
    n=0
    for r,c in product(range(4),repeat=2):
        x,y=(6,18,42,54)[c],(6,18,42,54)[r]
        bit=face[r%2][c%2];key=moved(symbol(bit),(x,y,6))
        assert abs(intersection_volume(mesh,key)-key.volume)<.003,(name,x,y,bit)
        n+=1
    checks.append({'type':name,'sockets':len(inputs),'matched_keys_and_rejected_wrong_bits':True,'verified_output_keys':n})
print(json.dumps(checks,indent=2))
(P/'boundary-port-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
