#!/usr/bin/env python3
"""Proposed orange C connector profiles, with sampled profile-fit checks.

Python standard library only. Square-ring C0 and diamond-ring C1 are new design
proposals, not recovered historical geometry. Blue and ordinary 0/+ connectors
are unchanged. Profile tests sample at 0.05 model units (L=60); no tolerances.
"""
from pathlib import Path
from itertools import product
from math import sqrt
import json
from blue_circle_plus_schematic import Svg, INK
from cgol_computational_tiles import orange, verify

OUT=Path(__file__).parent/'computational-schematics'
ORANGE='#ad6b23'


def profile(name):
    points=set()
    for i,j in product(range(-110,111),repeat=2):
        x,y=(i+.5)/20,(j+.5)/20
        if name=='0':inside=1.7**2<=x*x+y*y<=2.6**2
        elif name=='1':inside=(abs(x)<=2.6 and abs(y)<=.45) or (abs(y)<=2.6 and abs(x)<=.45)
        elif name=='C0':inside=2.5<=max(abs(x),abs(y))<=3.4
        elif name=='C1':inside=2.5*sqrt(2)<=abs(x)+abs(y)<=3.4*sqrt(2)
        else:raise ValueError(name)
        if inside:points.add((i,j))
    return frozenset(points)


def ring(svg,x,y,kind,scale):
    # Model units at L=60. Output is drawn from above; it is a raised ring.
    if kind=='C0':
        outer,inner=3.4*scale,2.5*scale
        pts=lambda a:f'{x-a},{y-a} {x+a},{y-a} {x+a},{y+a} {x-a},{y+a}'
        svg.parts.append(f'<path d="M{x-outer},{y-outer} h{2*outer} v{2*outer} h{-2*outer} Z M{x-inner},{y-inner} v{2*inner} h{2*inner} v{-2*inner} Z" fill="{ORANGE}" fill-rule="evenodd"/>')
    elif kind=='C1':
        outer,inner=3.4*sqrt(2)*scale,2.5*sqrt(2)*scale
        svg.parts.append(f'<path d="M{x},{y-outer} L{x+outer},{y} L{x},{y+outer} L{x-outer},{y} Z M{x},{y-inner} L{x-inner},{y} L{x},{y+inner} L{x+inner},{y} Z" fill="{ORANGE}" fill-rule="evenodd"/>')
    elif kind=='0':
        r=(2.6+1.7)*scale/2
        svg.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#5188b4" stroke-width="{.9*scale}"/>')
    elif kind=='1':
        svg.parts.append(f'<path d="M{x-2.6*scale},{y} H{x+2.6*scale} M{x},{y-2.6*scale} V{y+2.6*scale}" stroke="#5188b4" stroke-width="{.9*scale}" fill="none"/>')
    else:raise ValueError(kind)


def bar(svg,x,y,values,pitch):
    svg.parts.append(f'<rect x="{x}" y="{y}" width="{4*pitch}" height="{pitch}" fill="#f6e4cd" stroke="{ORANGE}" stroke-width="2"/>')
    for i,value in enumerate(values):
        if i:svg.line(x+i*pitch,y,x+i*pitch,y+pitch,True,color='#c9b194')
        ring(svg,x+(i+.5)*pitch,y+pitch/2,str(value),pitch/12)


def draw(path):
    s=Svg(1400,1200)
    s.parts[1]='<title>Proposed physical C0 and C1 connectors for the eight orange tiles</title>'
    s.text(32,42,'Orange tiles — proposed C0 / C1 connector shapes',28,True)
    s.text(32,78,'Ordinary circle/plus signals stay the same. The last output uses a distinct centre-state connector.',17)
    for i,(kind,label) in enumerate((('0','0 · circle'),('1','1 · plus'),('C0','C0 · square ring'),('C1','C1 · diamond ring'))):
        x=100+i*330
        ring(s,x+48,153,kind,8)
        s.text(x-10,218,label,19,True)
    s.text(32,259,'Eight directed tile types · input (x, y, y, z) → three packed bits + C_y',22,True)
    p=60
    for index,(x,y,z) in enumerate(product((0,1),repeat=3)):
        left,top=35+(index%2)*700,307+(index//2)*183
        incoming=(x,y,y,z);outgoing=orange(*incoming).face()
        s.text(left,top,f'O{index}: {x}{y}{y}{z}',19,True)
        s.text(left,top+30,'BOTTOM · all four recessed',14,True)
        s.text(left+325,top+30,'TOP · all four raised',14,True)
        bar(s,left,top+45,incoming,p)
        s.arrow(left+258,top+75,left+300)
        bar(s,left+325,top+45,outgoing,p)
        s.text(left,top+133,f'Count {x+y+z}; preserve C{y}.',15)
    s.text(32,1056,'The same rectangular piece is used horizontally, then rotated 90° for the second pass.',18,True)
    s.text(32,1090,'C0 and C1 fit neither ordinary input profile, so the next orange layer cannot cover the C column.',17)
    s.text(32,1124,'Proposed dimensions: body 4L/5 × L/5; connector pitch L/5. C profiles are symmetric under 90° turns.',16)
    s.text(32,1165,'Profile proposal only. The C-channel height and final-layer reach-down connection remain to be designed.',15)
    s.save(path)


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    profiles={name:profile(name) for name in ('0','1','C0','C1')}
    matches={a:{b:profiles[a]<=profiles[b] for b in profiles} for a in profiles}
    for a,b in product(profiles,repeat=2):assert matches[a][b]==(a==b),(a,b)
    for name,points in profiles.items():
        # Cell-centre raster quarter-turn: (i+.5,j+.5) -> (-j-.5,i+.5).
        assert points==frozenset((-j-1,i) for i,j in points),name
    logical=verify()
    report={'profile_sample_step':.05,'life_width':60,'fits_matrix':matches,
            'all_profiles_C4_symmetric':True,'logical_neighbourhoods_checked':logical['neighbourhoods_checked'],
            'status':'Proposed C profiles. Sampled nominal checks, not print-fit certification.'}
    (OUT/'orange-connector-profile-check.json').write_text(json.dumps(report,indent=2)+'\n')
    draw(OUT/'07_orange_C_profile_proposal.svg')
    print(json.dumps(report,indent=2))
