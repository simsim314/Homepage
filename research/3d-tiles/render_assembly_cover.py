#!/usr/bin/env python3
"""Render the complete exploded glider from the existing 286-piece model."""
import json
import numpy as np
import trimesh
from PIL import Image
from export_homepage_tiles import SOURCE, ROOT
from all_tiles_3d import transform

def main():
    width,height=1600,1050
    pixels=np.full((height,width,3),(25,25,24),dtype=np.uint8)
    depth=np.full((height,width),-np.inf)
    view=np.array((.65,-.85,.85));view/=np.linalg.norm(view)
    right=np.cross((0,0,1),view);right/=np.linalg.norm(right)
    basis=np.stack((right,np.cross(view,right),view),axis=1)
    light=np.array((-.35,-.5,.8));light/=np.linalg.norm(light)
    data=json.loads((SOURCE/'viewer-data.json').read_text())
    scene=trimesh.load(SOURCE/'all-32-tiles.glb',force='scene')
    meshes={}
    for node in scene.graph.nodes_geometry:
        matrix,name=scene.graph[node]
        mesh=scene.geometry[name].copy();mesh.apply_transform(matrix);meshes[node]=mesh
    surfaces=[]
    for item in data['assembly']:
        name=item['name'];x,y,z=item['xyz']
        mesh=transform(meshes[name],x,y,z+item['layer']*20,item['turns'],item['centre'])
        if name.startswith(('blue','edge','corner')):colour=(86,148,250)
        elif name.startswith('orange'):colour=(248,121,35)
        elif name.startswith('purple'):colour=(168,115,230)
        else:colour=(213,213,207) if name in ('start-1','final-0','final-2') else (67,67,64)
        surfaces.append((mesh.vertices@basis,mesh.faces,mesh.face_normals,colour))
    coords=np.concatenate([s[0] for s in surfaces])
    lo=coords[:,:2].min(axis=0);hi=coords[:,:2].max(axis=0)
    scale=min((width-150)/(hi[0]-lo[0]),(height-110)/(hi[1]-lo[1]))
    mid=(lo+hi)/2
    def screen(p):
        q=p.copy();q[...,0]=(q[...,0]-mid[0])*scale+width/2;q[...,1]=height/2-(q[...,1]-mid[1])*scale
        return q
    for verts,faces,normals,colour in surfaces:
        projected=screen(verts)
        for tri,n in zip(projected[faces],normals):
            if n@view<1e-7:continue
            xmin=max(0,int(np.floor(tri[:,0].min())));xmax=min(width-1,int(np.ceil(tri[:,0].max())))
            ymin=max(0,int(np.floor(tri[:,1].min())));ymax=min(height-1,int(np.ceil(tri[:,1].max())))
            if xmax<xmin or ymax<ymin:continue
            x,y=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
            a,b,c=tri;den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(den)<1e-10:continue
            w0=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
            w1=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den;w2=1-w0-w1
            z=w0*a[2]+w1*b[2]+w2*c[2];old=depth[ymin:ymax+1,xmin:xmax+1]
            hit=(w0>=-1e-7)&(w1>=-1e-7)&(w2>=-1e-7)&(z>old);old[hit]=z[hit]
            pixels[ymin:ymax+1,xmin:xmax+1][hit]=np.clip(np.array(colour)*(.5+.5*max(0,float(n@light))),0,255).astype(np.uint8)
    dest=ROOT/'src/assets/images/life-tiles-assembly.png'
    Image.fromarray(pixels).resize((1200,788),Image.Resampling.LANCZOS).save(dest,optimize=True)
    print(dest,flush=True)

if __name__=='__main__':main()
