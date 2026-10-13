#!/usr/bin/env python3
"""Four final B/W tile schematics, generated in Python.

Plan views share assembly coordinates, not a mirrored underside photograph.
Purple sockets are typed placeholders. The section explains the two input
heights; it is not a finished CAD profile or clearance certification.
"""
from pathlib import Path
from itertools import product
import json
from blue_circle_plus_schematic import Svg, INK
from orange_connector_design import ring
from cgol_computational_tiles import BW_CASES, black_white, verify

OUT=Path(__file__).parent/'computational-schematics'
PURPLE='#7d529b'


def centre_socket(s,x,y,centre,scale):
    # Union of the two proposed profiles: one recessed socket accepts either.
    for kind in ('C0','C1') if centre=='X' else (f'C{centre}',):
        ring(s,x,y,kind,scale)


def underside(s,x,y,L,category,centre):
    s.parts.append(f'<rect x="{x}" y="{y}" width="{L}" height="{L}" fill="#faf9f4" stroke="{INK}" stroke-width="2"/>')
    # Projected lower-layer regions, not extra parts of the B/W tile.
    s.parts.append(f'<rect x="{x+.1*L}" y="{y+.1*L}" width="{.6*L}" height="{.6*L}" fill="#eadff0" stroke="#c7b6d1" stroke-dasharray="4 4"/>')
    s.parts.append(f'<rect x="{x+.7*L}" y="{y+.1*L}" width="{.2*L}" height="{.8*L}" fill="#f5eee3" stroke="#c9b194" stroke-dasharray="4 4"/>')
    # Placeholder for the higher category socket: no new shape is implied.
    px,py=x+.4*L,y+.4*L
    s.parts.append(f'<rect x="{px-31}" y="{py-23}" width="62" height="46" rx="5" fill="#fffefa" stroke="{PURPLE}" stroke-width="2" stroke-dasharray="3 3"/>')
    s.text(px-(24 if category=='other' else 6),py+6,category,16,True,PURPLE)
    cx,cy=x+.8*L,y+.4*L
    s.parts.append(f'<rect x="{cx-21}" y="{cy-24}" width="42" height="48" fill="#fffefa" stroke="#ad6b23" stroke-width="2"/>')
    centre_socket(s,cx,cy,centre,L/60)
    s.text(x+.8*L-15,y+.72*L,'C*' if centre=='X' else f'C{centre}',16,True,'#ad6b23')
    s.text(x+12,y+L-14,'Both inputs recessed',13)


def top_face(s,x,y,L,bit):
    fill='#263d45' if bit else '#fffefa'
    line='#6e858c' if bit else '#c7d0c9'
    colour='#fcf8e9' if bit else '#5188b4'
    s.parts.append(f'<rect x="{x}" y="{y}" width="{L}" height="{L}" fill="{fill}" stroke="{INK}" stroke-width="2"/>')
    for f in (1/3,2/3):
        s.line(x+f*L,y,x+f*L,y+L,True,color=line)
        s.line(x,y+f*L,x+L,y+f*L,True,color=line)
    for r,c in product((1/6,5/6),repeat=2):
        xx,yy=x+c*L,y+r*L
        if bit:
            d=2.6*L/60
            s.line(xx-d,yy,xx+d,yy,sw=.9*L/60,color=colour)
            s.line(xx,yy-d,xx,yy+d,sw=.9*L/60,color=colour)
        else:ring(s,xx,yy,'0',L/60)
    s.text(x+L/2-20,y+L/2+6,'LIVE' if bit else 'DEAD',17,True,colour)


def draw(path):
    s=Svg(1440,1390)
    s.parts[1]='<title>Four black/white tile types: purple and centre inputs, uniform Life outputs</title>'
    s.text(32,43,'The four final black/white tiles',29,True)
    s.text(32,79,'Two recessed inputs: the purple category and the original centre C. Four raised outputs: the next cell state.',17)
    s.text(32,111,'Bottom and top use the same assembly coordinates. C* is the combined square/diamond recess: C0 OR C1.',16)
    L=205
    for i,(category,centre,bit) in enumerate(BW_CASES):
        x=36+(i%2)*712;y=159+(i//2)*355
        name=('B3','W4','B4','Wother')[i]
        s.text(x,y,f'{name}: {category} + {"C0 or C1" if centre=="X" else "C"+centre} → {"LIVE" if bit else "DEAD"}',21,True)
        s.text(x,y+34,'BOTTOM · input locations',15,True)
        s.text(x+350,y+34,'TOP · four identical outputs',15,True)
        underside(s,x,y+52,L,category,centre)
        s.arrow(x+230,y+150,x+318)
        top_face(s,x+350,y+52,L,bit)
        s.text(x,y+286,'Purple count includes the centre.' if category in ('3','4') else 'Other means total 0–2 or 5–9.',15)
        s.text(x+350,y+286,'Corner centres: L/6 and 5L/6.',15)
    s.text(32,880,'Shared stepped underside · section through the two input locations',23,True)
    s.text(32,914,'The C input reaches down to the first orange layer. The purple input meets the higher purple output.',17)
    # Explanatory section. Relative heights only; port widths exaggerated for clarity.
    x=60;ytop=961;zC=1166;zPurple=1066
    s.parts.append(f'<rect x="{x+35}" y="{zPurple}" width="315" height="50" fill="#e8d8f0" stroke="{PURPLE}" stroke-width="2"/>')
    # Purple body sits on the second orange pass.
    s.parts.append(f'<rect x="{x+35}" y="1116" width="315" height="50" fill="#f6e4cd" stroke="#ad6b23" stroke-width="2"/>')
    s.parts.append(f'<rect x="{x+35}" y="{zC}" width="475" height="50" fill="#f6e4cd" stroke="#ad6b23" stroke-width="2"/>')
    s.text(x+60,1200,'First orange layer',16)
    s.text(x+60,1148,'Second orange layer',16)
    s.text(x+60,1100,'Purple layer',16)
    # Final cap with a narrow descending foot at the original C position.
    d=f'M{x}, {ytop} H{x+550} V{ytop+38} H{x+491} V{zC} H{x+441} V{ytop+38} H{x+350} V{zPurple} H{x+35} V{ytop+38} H{x} Z'
    s.parts.append(f'<path d="{d}" fill="#d4dddb" stroke="{INK}" stroke-width="2"/>')
    # Recess openings shown as cutouts with a generic mating stud. The actual
    # purple connector profile is deliberately not fabricated here.
    for px,zz,col in ((x+191,zPurple,PURPLE),(x+466,zC,'#ad6b23')):
        s.parts.append(f'<path d="M{px-13},{zz+1} V{zz-18} H{px+13} V{zz+1}" fill="#fffefa" stroke="{INK}" stroke-width="2"/>')
        s.parts.append(f'<rect x="{px-9}" y="{zz-14}" width="18" height="14" fill="{col}"/>')
    s.text(x+145,ytop+25,'Final B/W tile',17,True)
    s.text(690,984,'HIGH INPUT: purple category',18,True,PURPLE)
    s.text(690,1022,'LOW INPUT: original C0 / C1',18,True,'#ad6b23')
    s.text(690,1060,'Two layer heights lower, if layers have equal thickness.',16)
    s.text(690,1108,'Other exposed C ports get clearance, not data sockets.',16)
    s.text(690,1146,'Finish the previous layer; no bridging over missing pieces.',16,True)
    s.text(32,1280,'Purple input boxes are typed placeholders. The section shows the height relationship, not a finished CAD profile.',16)
    s.text(32,1320,'Actual purple key shapes and clearances remain to be designed; the four logical cases are verified for all 512 neighbourhoods.',16)
    s.text(32,1359,'Black/white denotes the new Life cell state. Every corner on one tile carries that same state.',17,True)
    s.save(path)


if __name__=='__main__':
    for category,centre in product(('0–2','3','4','5–9'),(0,1)):
        total={'0–2':2,'3':3,'4':4,'5–9':5}[category]
        assert black_white(category,centre)==int(total==3 or (total==4 and centre==1))
    report=verify()
    draw(OUT/'11_four_final_bw_tiles.svg')
    (OUT/'11_four_final_bw_tiles.json').write_text(json.dumps({'cases':BW_CASES,'verification':report},indent=2)+'\n')
    print('Four B/W cases drawn; full 512-neighbourhood logic verified.')
