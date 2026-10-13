#!/usr/bin/env python3
"""Six boundary blue types and a constant-footprint, zero-outside Life board.

Edge and corner pieces have full-width overhanging bodies, with only two/one
recessed inputs respectively. The absent outside inputs are constants built
into these source pieces, not missing connectors. Every board cell evolves.
"""
from itertools import product
from pathlib import Path
import json,gzip,zipfile,base64
import numpy as np
import trimesh
from all_tiles_3d import transform
from blue_tiles_3d import blue_tile, life_cell, box, moved, canonical, verify_mesh, intersection_volume, symbol, fixed_blocker
from cgol_computational_tiles import compute, rotate, BW_CASES, reference_life
from glider_blue_orange import FIELD

ROOT=Path(__file__).parent
OUT=ROOT/'bounded-solids'
OLD=ROOT/'all-solids'
L=60


def boundary_kind(r,c,n,face):
    if r in (0,n) and c in (0,n):
        turns={(0,0):0,(0,n):1,(n,n):2,(n,0):3}[r,c]
        base=face
        for _ in range((-turns)%4):base=rotate(base)
        assert base[0]==(0,0) and base[1][0]==0
        return f'corner-{base[1][1]}',turns
    turns=0 if r==0 else 1 if c==n else 2 if r==n else 3
    base=face
    for _ in range((-turns)%4):base=rotate(base)
    assert base[0]==(0,0)
    return f'edge-{base[1][0]}{base[1][1]}',turns


def boundary_tile(face, corner=False):
    """Full blue body; only supported input sockets are cut into its underside.

    Top/bottom coordinates remain the same as an interior blue piece. The
    missing neighbours are zero constants encoded in its output keys, with
    solid underside where an ordinary blue tile would demand outside inputs.
    """
    body=box(L,L,6)
    ports=[(1,1)] if corner else [(1,0),(1,1)]
    cuts=[moved(symbol(face[r][c],2.01),((20,40)[c],(20,40)[r],-.01)) for r,c in ports]
    body=trimesh.boolean.difference([body,*cuts],engine='manifold')
    keys=[moved(symbol(face[r%2][c%2]),((6,18,42,54)[c],(6,18,42,54)[r],6))
          for r,c in product(range(4),repeat=2)]
    keys += [moved(fixed_blocker(),((c+.5)*12,(r+.5)*12,6))
             for r,c in product(range(5),repeat=2) if r==2 or c==2]
    return trimesh.boolean.union([body,*keys],engine='manifold')


def build():
    OUT.mkdir(exist_ok=True)
    meta=json.loads((OLD/'viewer-data.json').read_text())['types']
    meshes={t['name']:trimesh.load_mesh(OLD/f'{t["name"]}.stl') for t in meta}
    for bit in (0,1):meshes[f'start-{bit}']=life_cell(bit)
    for a,b in product((0,1),repeat=2):
        face=((0,0),(a,b))
        mesh=boundary_tile(face)
        name=f'edge-{a}{b}';meshes[name]=mesh
        meta.append({'name':name,'family':'Boundary blue','label':f'Edge {a}{b} · 2 inside / 2 outside zeros',
                     'description':'Full-width edge piece · 2 inside sockets · 2 outside zeros · half-cell overhang',**verify_mesh(mesh)})
    for bit in (0,1):
        mesh=boundary_tile(((0,0),(0,bit)),corner=True)
        name=f'corner-{bit}';meshes[name]=mesh
        meta.append({'name':name,'family':'Boundary blue','label':f'Corner {bit} · 1 inside / 3 outside zeros',
                     'description':'Full-width corner piece · 1 inside socket · 3 outside zeros · half-cell overhang on two edges',**verify_mesh(mesh)})
    records=[];solids=[];n=len(FIELD)
    def value(r,c):return FIELD[r][c] if 0<=r<n and 0<=c<n else 0
    def place(name,xyz,layer,turns=0,centre=None):
        records.append({'name':name,'xyz':xyz,'layer':layer,'turns':turns,'centre':centre})
        solids.append((name,transform(meshes[name],*xyz,turns,centre)))
    for r,c in product(range(n),repeat=2):place(f'start-{FIELD[r][c]}',(c*L,r*L,0),0)
    faces=sorted({canonical((bits[:2],bits[2:])) for bits in product((0,1),repeat=4)})
    blue_names={face:f'blue-{i}' for i,face in enumerate(faces)}
    route={};counts={'full':0,'edge':0,'corner':0}
    for r,c in product(range(n+1),repeat=2):
        face=tuple(tuple(value(r-1+i,c-1+j) for j in range(2)) for i in range(2))
        if r in (0,n) or c in (0,n):name,turns=boundary_kind(r,c,n,face)
        else:
            base=canonical(face);name=blue_names[base];turns=0
            while base!=face:base=rotate(base);turns+=1
        counts['edge' if name.startswith('edge') else 'corner' if name.startswith('corner') else 'full']+=1
        place(name,((c-.5)*L,(r-.5)*L,5),1,turns,(30,30,0))
        # Exact displayed port coordinates, in tenths of L, clipping to board.
        for i,j in product(range(4),repeat=2):
            yy,xx=(r-.5)*10+(1,3,7,9)[i],(c-.5)*10+(1,3,7,9)[j]
            if 0<xx<n*10 and 0<yy<n*10:
                assert (yy,xx) not in route
                route[yy,xx]=face[i%2][j%2]
    result=[]
    for r in range(n):
        outrow=[]
        for c in range(n):
            grid=tuple(tuple(value(r+i,c+j) for j in (-1,0,1)) for i in (-1,0,1))
            tr=compute(grid);ox,oy=c*L+6,r*L+6
            assert tuple(tuple(route[r*10+i,c*10+j] for j in (2,4,6,8)) for i in (2,4,6,8))==tr.blue
            outrow.append(tr.output)
            for i,row in enumerate(tr.blue):place(f'orange-{row[0]}{row[1]}{row[3]}',(ox,oy+i*12,11),2)
            for i in range(3):
                v=[row.compacted[i] for row in tr.rows]
                place(f'orange-{v[0]}{v[1]}{v[3]}',(ox+(i+1)*12,oy,17),3,1,(0,0,0))
            tile,turns,_=tr.matches[0]
            place(f'purple-{tile.name}',(ox,oy,23),4,(turns+2)%4,(18,18,0))
            category=tr.category if tr.category in ('3','4') else 'other'
            index=next(i for i,(k,cc,_) in enumerate(BW_CASES) if k==category and (cc=='X' or int(cc)==tr.centre))
            place(f'final-{index}',(c*L,r*L,17),5)
        result.append(outrow)
    assert sum(map(sum,result))==5
    # Independent unbounded one-step reference confirms no birth is lost here.
    alive={(r,c) for r,c in product(range(n),repeat=2) if FIELD[r][c]}
    next_alive=set()
    for r,c in product(range(-1,n+1),repeat=2):
        neighbours=sum((r+dr,c+dc) in alive for dr,dc in product((-1,0,1),repeat=2) if (dr,dc)!=(0,0))
        if neighbours==3 or ((r,c) in alive and neighbours==2):next_alive.add((r,c))
    assert next_alive=={(r,c) for r,c in product(range(n),repeat=2) if result[r][c]}
    # Blue overhangs by half a cell; all later computation returns to the original board.
    layer_bounds={}
    for layer in range(6):
        arr=np.array([m.bounds for record,(_,m) in zip(records,solids) if record['layer']==layer])
        bounds=[arr[:,0,:2].min(axis=0).tolist(),arr[:,1,:2].max(axis=0).tolist()]
        layer_bounds[layer]=bounds
        minimum,maximum=(-L/2,n*L+L/2) if layer==1 else (0,n*L)
        assert np.all(np.array(bounds)>=minimum-.001) and np.all(np.array(bounds)<=maximum+.001)
    assert np.allclose(layer_bounds[0],layer_bounds[5])
    assert np.allclose(layer_bounds[1],[[-L/2,-L/2],[n*L+L/2,n*L+L/2]])
    checks=0;worst=0.
    for i,(an,a) in enumerate(solids):
        for bn,b in solids[i+1:]:
            if np.any(np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])<.001):continue
            v=intersection_volume(a,b);checks+=1;worst=max(worst,v)
            assert v<.003,(an,bn,v)
    for t in meta:meshes[t['name']].export(OUT/f'{t["name"]}.stl')
    scene=trimesh.Scene()
    for name,mesh in meshes.items():
        mesh.visual=trimesh.visual.ColorVisuals(mesh)
        scene.add_geometry(mesh,geom_name=name,node_name=name)
    glb=scene.export(file_type='glb')
    (OUT/'all-32-tiles.glb').write_bytes(glb)
    (OUT/'all-32-tiles.glb.gz').write_bytes(gzip.compress(glb))
    report={'original_types':26,'boundary_types':6,'blue_piece_counts':counts,'all_assembly_pieces':len(records),
            'board_dimensions_cells':[n,n],'board_dimensions_mm':[n*L,n*L],
            'input':FIELD,'output':result,'matches_unbounded_life_for_this_step':True,
            'verified_routed_inputs':len(route),'collision_checks':checks,'max_overlap_mm3':worst,
            'layer_bounds_xy':layer_bounds,'new_type_mesh_checks':meta[-6:],
            'boundary_condition':'Exterior held at zero. All on-board cells evolve normally. Infinite-plane agreement requires sufficient padding for the chosen duration.'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'viewer-data.json').write_text(json.dumps({'types':meta,'assembly':records},separators=(',',':')))
    (OUT/'DESIGN-NOTES.txt').write_text('26 original computation types + 4 full-width blue edge types + 2 full-width blue corner types.\n'
        'Blue overhangs the board by half a cell on every edge; orange/purple/final return to the original grid. Outside cells are fixed zero constants in boundary blue routing.\n'
        'Assembly rule: the six boundary types may be placed only on the declared outer perimeter, facing inward.\n'
        'On-board padding cells evolve normally; an empty cell is not automatically a zero-to-zero wire.\n'
        'The supplied glider advances one full generation on the same 5x5 footprint, preserving all five live cells.\n'
        'For unlimited evolution on the infinite plane, choose more padding or enlarge the board when activity reaches it.\n'
        'Nominal millimetres, zero mating clearance. New annular purple keys are prototype design choices.\n'
        'Complete each layer before starting the next; no bridging. Full-width boundary blue types have only 2 or 1 input sockets, all over real cells. Exterior zero outputs are built into their keys; no outside input sockets are left unfilled.\n')
    with zipfile.ZipFile(OUT/'life-32-tile-models.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.glob('*.stl')):z.write(p,p.name)
        for name in ('validation.json','DESIGN-NOTES.txt','all-32-tiles.glb'):z.write(OUT/name,name)
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':build()
