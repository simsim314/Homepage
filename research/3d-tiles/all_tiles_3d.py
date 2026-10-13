#!/usr/bin/env python3
"""Build the 26 Life-computation tile types and a complete finite glider stack.

PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/all_tiles_3d.py
Nominal zero-clearance solids, not calibrated print fits. Purple category rings
are a new proposed C4-symmetric encoding. Complete layers/no bridging is an
assembly convention, not a property enforced by collision alone.
"""
from pathlib import Path
from itertools import product
from functools import lru_cache
import json, gzip, zipfile
import numpy as np
import trimesh
from blue_tiles_3d import (box,moved,symbol,blue_tile,life_cell,verify_mesh,
                           intersection_volume,canonical,orient_tile)
from cgol_computational_tiles import PURPLE_TILES, BW_CASES, compute, verify, rotate
from glider_blue_orange import FIELD

OUT=Path(__file__).parent/'all-solids'
H=6.; STUD=2.; L=60.
RINGS={'3':4.2,'4':6.4,'other':8.6}


def union(parts): return trimesh.boolean.union(parts,engine='manifold')
def cut(body,parts): return trimesh.boolean.difference([body,*parts],engine='manifold')


@lru_cache(None)
def key(kind,height=STUD):
    if kind in ('0','1'): return symbol(int(kind),height)
    if kind in ('C0','C1'):
        shape=cut(moved(box(6.8,6.8,height),(-3.4,-3.4,0)),
                  [moved(box(5,5,height+.02),(-2.5,-2.5,-.01))])
        if kind=='C1': shape.apply_transform(trimesh.transformations.rotation_matrix(np.pi/4,(0,0,1)))
        return shape
    if kind=='X': return union([key('0',height),key('1',height)])
    if kind=='C*': return union([key('C0',height),key('C1',height)])
    r=RINGS[kind]
    shape=trimesh.creation.annulus(r_min=r-.55,r_max=r+.55,height=height,sections=48)
    return moved(shape,(0,0,height/2))


def orange_mesh(x,y,z):
    from cgol_computational_tiles import orange
    incoming=(x,y,y,z); outgoing=orange(*incoming).face()
    shape=cut(box(48,12,H),[moved(key(str(v),STUD+.01),(6+i*12,6,-.01)) for i,v in enumerate(incoming)])
    return union([shape,*[moved(key(str(v)),(6+i*12,6,H)) for i,v in enumerate(outgoing)]])


def purple_mesh(tile):
    shape=cut(box(36,36,H),[moved(key(tile.mask[r][c],STUD+.01),(6+c*12,6+r*12,-.01))
                          for r,c in product(range(3),repeat=2)])
    category=tile.category if tile.category in ('3','4') else 'other'
    return union([shape,moved(key(category),(18,18,H))])


def bw_mesh(category,centre,bit):
    # Local z=0 is the first orange output plane. Purple's top is z=12.
    cap=moved(box(60,60,H),(0,0,12))
    leg=moved(box(10,10,12),(43,19,0))
    shape=union([cap,leg])
    shape=cut(shape,[moved(key(category,STUD+.01),(24,24,12-.01)),
                     moved(key('C*' if centre=='X' else f'C{centre}',STUD+.01),(48,24,-.01))])
    return union([shape,*[moved(key(str(bit)),(x,y,18)) for x,y in product((10,50),repeat=2)]])


def transform(mesh,x,y,z,turns=0,centre=None):
    result=mesh.copy()
    if turns:
        result.apply_transform(trimesh.transformations.rotation_matrix(turns*np.pi/2,(0,0,1),point=centre))
    result.apply_translation((x,y,z))
    return result


def build():
    OUT.mkdir(exist_ok=True)
    meshes={};meta=[]
    def add(name,mesh,family,label,description):
        report=verify_mesh(mesh)
        mesh.export(OUT/f'{name}.stl')
        meshes[name]=mesh
        meta.append({'name':name,'family':family,'label':label,'description':description,**report})
        print(f'{name}: {report["triangles"]} triangles',flush=True)
    faces=sorted({canonical((bits[:2],bits[2:])) for bits in product((0,1),repeat=4)})
    blue_names={}
    for i,face in enumerate(faces):
        name=f'blue-{i}';blue_names[face]=name
        add(name,blue_tile(face),'Blue',f'B{i} · '+''.join(map(str,sum(face,()))),'4 recessed bits; 16 raised copies and 9 fixed X blockers')
    for x,y,z in product((0,1),repeat=3):
        name=f'orange-{x}{y}{z}'
        add(name,orange_mesh(x,y,z),'Orange',f'O{x}{y}{z} · {x}{y}{y}{z}', '4 recessed bits; 3 packed bits and C on top')
    for tile in PURPLE_TILES:
        add(f'purple-{tile.name}',purple_mesh(tile),'Purple',f'{tile.name} · total {tile.category}',
            f'9 recessed inputs; raised category ring {tile.category if tile.category in ("3","4") else "other"}')
    for i,(category,centre,bit) in enumerate(BW_CASES):
        add(f'final-{i}',bw_mesh(category,centre,bit),'Black / white',
            f'{category} + {"C*" if centre=="X" else "C"+centre} → {"live" if bit else "dead"}',
            'Stepped underside: purple + original C; 4 identical raised corner bits')
    assert len(meshes)==26
    # Two initial-state solids are supporting pieces, not extra transition types.
    for bit in (0,1):meshes[f'start-{bit}']=life_cell(bit)
    records=[]; solids=[]
    def place(name,xyz,layer,turns=0,centre=None):
        records.append({'name':name,'xyz':xyz,'layer':layer,'turns':turns,'centre':centre})
        m=transform(meshes[name],*xyz,turns,centre)
        solids.append((layer,m,name))
        return m
    for r,c in product(range(5),repeat=2):place(f'start-{FIELD[r][c]}',(c*L,r*L,0),0)
    # Starting Life tiles have height 5. All computation layers have height 6.
    for r,c in product(range(4),repeat=2):
        face=tuple(tuple(FIELD[r+i][c+j] for j in range(2)) for i in range(2))
        base=canonical(face);candidate=base;turns=0
        while candidate!=face:candidate=rotate(candidate);turns+=1
        place(blue_names[base],((c+.5)*L,(r+.5)*L,5),1,turns,(30,30,0))
    for r,c in product(range(1,4),repeat=2):
        grid=tuple(tuple(FIELD[r+i][c+j] for j in (-1,0,1)) for i in (-1,0,1))
        tr=compute(grid);ox,oy=c*L+6,r*L+6
        for i,row in enumerate(tr.blue):
            place(f'orange-{row[0]}{row[1]}{row[3]}',(ox,oy+i*12,11),2)
        for i in range(3):
            incoming=[row.compacted[i] for row in tr.rows]
            # R90 sends local y=0..12 to x=-12..0, so offset by one pitch.
            place(f'orange-{incoming[0]}{incoming[1]}{incoming[3]}',(ox+(i+1)*12,oy,17),3,1,(0,0,0))
        tile,turns,mask=tr.matches[0]
        place(f'purple-{tile.name}',(ox,oy,23),4,(turns+2)%4,(18,18,0))
        category=tr.category if tr.category in ('3','4') else 'other'
        index=next(i for i,(k,cc,bit) in enumerate(BW_CASES) if k==category and (cc=='X' or int(cc)==tr.centre))
        place(f'final-{index}',(c*L,r*L,17),5)
    # AABB broad phase then exact boolean intersection for all assembly pairs.
    checks=0;max_overlap=0.
    for i,(_,a,an) in enumerate(solids):
        for _,b,bn in solids[i+1:]:
            overlap=np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0])
            if np.any(overlap<.001):continue
            v=intersection_volume(a,b);checks+=1;max_overlap=max(max_overlap,v)
            assert v<.003,(an,bn,v)
    # Check each new port's nominal accepted/rejected key combinations.
    matches={};profiles=('0','1','C0','C1','3','4','other')
    for socket in (*profiles,'X','C*'):
        matches[socket]={}
        cavity=key(socket)
        for incoming in profiles:
            peg=key(incoming)
            remaining=cut(peg,[cavity])
            triangles=remaining.triangles
            v=abs(float(np.einsum('ij,ij->i',triangles[:,0],np.cross(triangles[:,1],triangles[:,2])).sum()/6)) if len(triangles) else 0.
            accepted=bool(v<.001)
            expected=incoming==socket or (socket=='X' and incoming in ('0','1')) or (socket=='C*' and incoming in ('C0','C1'))
            assert accepted==expected,(incoming,socket,v)
            matches[socket][incoming]=accepted
    scene=trimesh.Scene()
    for name,mesh in meshes.items():
        mesh.visual=trimesh.visual.ColorVisuals(mesh)
        scene.add_geometry(mesh,geom_name=name,node_name=name)
    data=scene.export(file_type='glb')
    (OUT/'all-26-tiles.glb').write_bytes(data)
    (OUT/'all-26-tiles.glb.gz').write_bytes(gzip.compress(data))
    report={'types':meta,'logical':verify(),'assembly_pieces':len(solids),
            'assembly_boolean_checks':checks,'max_overlap':max_overlap,'port_fit_matrix':matches,
            'scope':'Nominal meshes, canonical assembly, fixed socket orientation. No print tolerances or arbitrary-placement proof.'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'viewer-data.json').write_text(json.dumps({'types':meta,'assembly':records},separators=(',',':')))
    (OUT/'DESIGN-NOTES.txt').write_text('26 transition types: 6 blue + 8 orange + 8 purple + 4 black/white.\n'
        'Units: nominal millimetres; Life pitch 60; computation body height 6; keys 2 high.\n'
        'C0 square ring; C1 diamond ring; C* union cavity. Purple classes 3/4/other use annular keys\n'
        'with centreline radii 4.2/6.4/8.6 and wall width 1.1, proposed for this prototype.\n'
        'All inputs inward; outputs outward. Assembly requires completed previous layers, no bridging.\n'
        'STLs have zero mating clearance. Calibrate before fabrication. No print-fit certification.\n'
        'The finite demonstration computes the inner 3x3 of a padded 5x5 glider; border extension is not included.\n')
    with zipfile.ZipFile(OUT/'life-26-tile-models.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(OUT.glob('*.stl')):archive.write(p,p.name)
        for name in ('DESIGN-NOTES.txt','validation.json','all-26-tiles.glb'):archive.write(OUT/name,name)
    print(json.dumps({k:report[k] for k in ('assembly_pieces','assembly_boolean_checks','max_overlap')},indent=2),flush=True)
    print('GLB',len(data),'gzipped',len(gzip.compress(data)),flush=True)


if __name__=='__main__':build()
