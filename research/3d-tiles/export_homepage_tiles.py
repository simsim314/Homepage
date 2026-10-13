#!/usr/bin/env python3
"""Publish local prototype assets to the local Astro tree (no network/upload).

Rasterizes the real STL triangle surfaces with a depth buffer. No image model,
browser capture, or painter sorting: recessed inputs remain visible correctly.
PYTHONPATH=/tmp/homepage-mesh-runtime python research/3d-tiles/export_homepage_tiles.py
"""
from pathlib import Path
import json,shutil
import numpy as np
import trimesh
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).parent/'bounded-solids'
ASSETS=ROOT/'public/models/life-tiles'
IMAGES=ROOT/'public/images/life-tiles'
COLOURS={'Blue':(88,139,178),'Orange':(216,151,71),'Purple':(151,114,180),
         'Boundary blue':(88,139,178)}


def render_pair(mesh,colour,path):
    width,height=720,300
    pixels=np.full((height,width,3),(243,243,236),dtype=np.uint8)
    depth=np.full((height,width),-np.inf)
    view=np.array((.28,-.57,.77));view/=np.linalg.norm(view)
    right=np.cross((0,0,1),view);right/=np.linalg.norm(right)
    up=np.cross(view,right)
    light=np.array((-.35,-.5,.8));light/=np.linalg.norm(light)
    basis=np.stack((right,up,view),axis=1)
    for index in range(2):
        vertices=mesh.vertices-mesh.bounds.mean(axis=0)
        normals=mesh.face_normals.copy()
        if index:vertices=vertices*np.array((1,-1,-1));normals=normals*np.array((1,-1,-1))
        projected=vertices@basis
        extent=np.ptp(projected[:,:2],axis=0)
        scale=min(285/max(extent[0],1),220/max(extent[1],1),4.4)
        projected[:,:2]*=scale
        projected[:,0]+=180+index*360
        projected[:,1]=height/2-projected[:,1]
        for tri,n in zip(projected[mesh.faces],normals):
            if n@view<1e-7:continue
            xmin=max(0,int(np.floor(tri[:,0].min())));xmax=min(width-1,int(np.ceil(tri[:,0].max())))
            ymin=max(0,int(np.floor(tri[:,1].min())));ymax=min(height-1,int(np.ceil(tri[:,1].max())))
            if xmax<xmin or ymax<ymin:continue
            x,y=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
            a,b,c=tri
            den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-10:continue
            w0=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
            w1=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
            w2=1-w0-w1
            z=w0*a[2]+w1*b[2]+w2*c[2]
            old=depth[ymin:ymax+1,xmin:xmax+1]
            hit=(w0>=-1e-7)&(w1>=-1e-7)&(w2>=-1e-7)&(z>old)
            old[hit]=z[hit]
            shade=.44+.56*max(0,float(n@light))
            pixels[ymin:ymax+1,xmin:xmax+1][hit]=np.clip(np.array(colour)*shade,0,255).astype(np.uint8)
    Image.fromarray(pixels).save(path,optimize=True)


def main():
    ASSETS.mkdir(parents=True,exist_ok=True);IMAGES.mkdir(parents=True,exist_ok=True)
    data=json.loads((SOURCE/'viewer-data.json').read_text())
    (ASSETS/'assembly.json').write_text(json.dumps(data['assembly'],separators=(',',':'))+'\n')
    for t in data['types']:
        name=t['name']; colour=COLOURS.get(t['family'],(77,88,88) if name in ('final-0','final-2') else (231,229,213))
        render_pair(trimesh.load_mesh(SOURCE/f'{name}.stl'),colour,IMAGES/f'{name}.png')
        shutil.copyfile(SOURCE/f'{name}.stl',ASSETS/f'{name}.stl')
        t['image']=f'images/life-tiles/{name}.png';t['file']=f'models/life-tiles/{name}.stl'
        print(name,flush=True)
    shutil.copyfile(SOURCE/'all-32-tiles.glb',ASSETS/'all-32-tiles.glb')
    shutil.copyfile(IMAGES/'blue-1.png',ROOT/'src/assets/images/life-tiles-blue.png')
    for name in ('life-32-tile-models.zip','DESIGN-NOTES.txt','validation.json','boundary-port-checks.json'):
        shutil.copyfile(SOURCE/name,ASSETS/name)
    images={
        'blue-routing.svg':'blue-schematics/06_glider_blue_input_output.svg',
        'orange-passes.svg':'computational-schematics/09_glider_two_orange_layers.svg',
        'purple-classification.svg':'computational-schematics/10_glider_purple.svg',
        'final-tiles.svg':'computational-schematics/11_four_final_bw_tiles.svg',
    }
    for name,source in images.items():shutil.copyfile(Path(__file__).parent/source,IMAGES/name)
    dest=ROOT/'src/data/life-tile-catalogue.json';dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(data['types'],indent=2)+'\n')
    (ASSETS/'manifest.json').write_text(json.dumps({'types':data['types']},indent=2)+'\n')


if __name__=='__main__':main()
