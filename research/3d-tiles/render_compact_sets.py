#!/usr/bin/env python3
"""Render whole tile families on one shared 3D plane; crop existing SVG diagrams."""
from pathlib import Path
import json, math, re, shutil
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont
from export_homepage_tiles import SOURCE, IMAGES, ROOT, COLOURS

FAMILIES={'Blue':'blue','Orange':'orange','Purple':'purple','Black / white':'final','Boundary blue':'boundary'}

def render_set(tiles,path):
    width,height=1600,650
    pixels=np.full((height,width,3),(243,243,236),dtype=np.uint8)
    depth=np.full((height,width),-np.inf)
    view=np.array((.14,-.59,.8));view/=np.linalg.norm(view)
    right=np.cross((0,0,1),view);right/=np.linalg.norm(right)
    basis=np.stack((right,np.cross(view,right),view),axis=1)
    light=np.array((-.35,-.5,.8));light/=np.linalg.norm(light)
    cols=4 if len(tiles)==8 else 3 if len(tiles)==6 else 4
    rows=math.ceil(len(tiles)/cols)
    surfaces=[];labels=[]
    for i,t in enumerate(tiles):
        mesh=trimesh.load_mesh(SOURCE/f"{t['name']}.stl")
        verts=mesh.vertices-mesh.bounds.mean(axis=0);normals=mesh.face_normals.copy()
        if t['family']=='Purple':
            verts*=np.array((1,-1,-1));normals*=np.array((1,-1,-1))
        verts[:,2]-=verts[:,2].min()
        shift=np.array(((i%cols-(cols-1)/2)*79,((rows-1)/2-i//cols)*80,0))
        verts+=shift
        colour=COLOURS.get(t['family'],(77,88,88) if t['name'] in ('final-0','final-2') else (231,229,213))
        surfaces.append((verts@basis,mesh.faces,normals,colour))
        label=t['label'].split(' · ')[0]
        labels.append(((shift+np.array((0,-37,0)))@basis,label))
    coords=np.concatenate([s[0] for s in surfaces]+[np.array([p for p,_ in labels])])
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
    img=Image.fromarray(pixels);draw=ImageDraw.Draw(img)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
    for p,label in labels:
        x,y,_=screen(p);draw.text((x,y),label,font=font,fill='#34494d',anchor='mt')
    img.resize((1200,488),Image.Resampling.LANCZOS).save(path,optimize=True)


def crop_svg(source,dest,box):
    text=source.read_text();x,y,w,h=box
    text=re.sub(r'<svg[^>]+>',f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{x} {y} {w} {h}" role="img">',text,count=1)
    # Cover the full viewBox even when it starts below the original background.
    text=text.replace('<rect width="100%" height="100%" fill="#f6f5ef"/>',f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f6f5ef"/>')
    dest.write_text(text)


def main():
    data=json.loads((SOURCE/'viewer-data.json').read_text())['types']
    for family,slug in FAMILIES.items():
        render_set([t for t in data if t['family']==family],IMAGES/f'set-{slug}.png');print(family,flush=True)
    base=Path(__file__).parent
    for src,dest,box in [
        ('blue-schematics/03_circle_plus_faces.svg','blue-example.svg',(20,90,1360,460)),
        ('computational-schematics/05_orange_eight_faces.svg','orange-example.svg',(20,320,600,170)),
        ('computational-schematics/10_glider_purple.svg','purple-example.svg',(20,905,770,225)),
        ('computational-schematics/11_four_final_bw_tiles.svg','final-example.svg',(20,130,610,330)),
    ]:crop_svg(base/src,IMAGES/dest,box)
    shutil.copyfile(IMAGES/'set-blue.png',ROOT/'src/assets/images/life-tiles-blue.png')

if __name__=='__main__':main()
