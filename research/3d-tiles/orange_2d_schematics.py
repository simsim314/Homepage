#!/usr/bin/env python3
"""Dimensioned orange port layouts derived from the current blue spacing.

Pure Python SVG generator. Connector positions are explicit; C0/C1 are typed
port labels, not a proposed physical profile. The proposed orange rectangular
footprint is 4L/5 by L/5. Both faces use assembly coordinates as seen from above;
the bottom is not mirrored as it would be when physically turning a tile over.
"""
from itertools import product
from pathlib import Path
import json
from blue_circle_plus_schematic import Svg, dimension, INK
from cgol_computational_tiles import orange, blue_gather, compute, verify

OUT=Path(__file__).parent/'computational-schematics'
EDGE='#ad6b23'
FILL='#f6e4cd'


def rect(svg,x,y,w,h,fill=FILL,stroke=EDGE,sw=2):
    svg.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def port(svg,x,y,value,pitch):
    if isinstance(value,int):
        svg.symbol(x,y,value,pitch*.15)
    else:
        # Deliberately textual: no invented C connector geometry.
        svg.text(x-pitch*.22,y+6,value,17,True,EDGE)


def bar(svg,x,y,values,pitch,vertical=False):
    w,h=(pitch,4*pitch) if vertical else (4*pitch,pitch)
    rect(svg,x,y,w,h)
    for i,v in enumerate(values):
        if i:
            if vertical:svg.line(x,y+i*pitch,x+w,y+i*pitch,True,color='#c9b194')
            else:svg.line(x+i*pitch,y,x+i*pitch,y+h,True,color='#c9b194')
        px=x+pitch/2 if vertical else x+(i+.5)*pitch
        py=y+(i+.5)*pitch if vertical else y+pitch/2
        port(svg,px,py,v,pitch)


def catalogue(path):
    svg=Svg(1340,1010)
    svg.parts[1]='<title>Eight orange tile input and output port layouts</title>'
    svg.text(32,43,'Orange tiles — all eight bottom/top port layouts',27,True)
    svg.text(32,79,'Circle = 0. Plus = 1. C0/C1 preserves the repeated middle input using a separate connector type.',16)
    svg.text(32,110,'Both faces shown in assembly coordinates from above: port positions align vertically; the underside is not mirrored.',15)
    p=58
    for index,(x,y,z) in enumerate(product((0,1),repeat=3)):
        left,top=35+(index%2)*665,161+(index//2)*179
        incoming=(x,y,y,z)
        outgoing=orange(*incoming).face()
        svg.text(left,top,f'O{index}: ({x}, {y}, {y}, {z})',19,True)
        svg.text(left,top+29,'BOTTOM · recessed',14,True)
        svg.text(left+324,top+29,'TOP · raised',14,True)
        bar(svg,left,top+44,incoming,p)
        svg.arrow(left+249,top+73,left+300)
        bar(svg,left+324,top+44,outgoing,p)
        svg.text(left,top+129,f'Count x+y+z = {x+y+z}; carry C{y}.',15)
    svg.text(32,895,'Position geometry derived from the blue face',21,True)
    svg.text(32,930,'Proposed body: 4L/5 × L/5. Port pitch: L/5. End margins: L/10. Four ports centred across the width.',16)
    svg.text(32,961,'Local port centres along length: L/10, 3L/10, 5L/10, 7L/10. All lie on the midline L/10.',16)
    svg.text(32,991,'C0/C1 are labels here: their actual raised/recessed profiles and channel heights still need to be drawn.',14)
    svg.save(path)


def placement(path):
    svg=Svg(1560,1035)
    svg.parts[1]='<title>Orange tile footprints aligned to blue outputs</title>'
    svg.text(32,43,'Orange placement — one Life cell, two perpendicular passes',27,True)
    svg.text(32,77,'Same scale throughout. L is the Life-cell width. Data ports sit at 0.2L, 0.4L, 0.6L, 0.8L on each axis.',16)
    svg.text(32,109,'Outer dotted square: Life-cell boundary. Inner work area: 0.8L × 0.8L. Orange outlines: proposed piece boundaries.',15)
    field=((0,0,1),(1,1,1),(0,0,0))
    tr=compute(field)
    pitch=76
    L=pitch*5
    for stage,left in enumerate((40,575,1110)):
        top=193
        svg.text(left,154,('1. Blue outputs around the cell','2. Four horizontal orange tiles','3. Three vertical orange tiles')[stage],19,True)
        # Dotted cell boundary, no deceptive extra input/output grid divisions.
        for a,b,c,d in ((left,top,left+L,top),(left+L,top,left+L,top+L),(left+L,top+L,left,top+L),(left,top+L,left,top)):
            svg.line(a,b,c,d,True,color='#7f9599')
        ox,oy=left+pitch/2,top+pitch/2
        if stage==0:
            for r,c in product(range(4),repeat=2):
                rect(svg,ox+c*pitch,oy+r*pitch,pitch,pitch,fill='#e5eff5',stroke='#aabfc9',sw=1)
                port(svg,ox+(c+.5)*pitch,oy+(r+.5)*pitch,tr.blue[r][c],pitch)
            # Boundaries of the four blue groups arriving from neighbouring tiles.
            for r,c in product(range(2),repeat=2):
                rect(svg,ox+c*2*pitch,oy+r*2*pitch,2*pitch,2*pitch,fill='none',stroke='#5188b4',sw=3)
            # X blockers on the surrounding blue separator; boundary studs
            # are shared with adjacent Life-cell work regions.
            for rr,cc in product(range(6),repeat=2):
                if rr not in (0,5) and cc not in (0,5):continue
                cx,cy=left+cc*pitch,top+rr*pitch
                d=L*.075/(2**.5)
                svg.line(cx-d,cy-d,cx+d,cy+d,sw=L/60,color='#786f8b')
                svg.line(cx-d,cy+d,cx+d,cy-d,sw=L/60,color='#786f8b')
        elif stage==1:
            for r,row in enumerate(tr.rows):bar(svg,ox,oy+r*pitch,row.face(),pitch)
        else:
            for c,col in enumerate(tr.columns):bar(svg,ox+c*pitch,oy,col.face(),pitch,vertical=True)
            # First pass C column remains outside the second pass footprint.
            for r,row in enumerate(tr.rows):
                rect(svg,ox+3*pitch,oy+r*pitch,pitch,pitch,fill='#fffefa',stroke='#b4b5ac',sw=1)
                port(svg,ox+3.5*pitch,oy+(r+.5)*pitch,f'C{row.centre}',pitch)
            # Ring the TWO genuine copies of the original centre.
            rect(svg,ox+3*pitch,oy+pitch,pitch,2*pitch,fill='none',stroke='#38705d',sw=3)
        dimension(svg,left,left+L,top+L+21,'L')
        if stage<2:svg.arrow(left+L+25,top+L/2,left+L+109)
    svg.text(40,666,'Each row has form (x, y, y, z).',17)
    svg.text(40,697,'Port pitch = L/5.',17)
    svg.text(575,666,'Three unary bits + one C port per row.',17)
    svg.text(575,697,'Each body is 4L/5 long and L/5 wide.',17)
    svg.text(1110,666,'Rotate the SAME orange types 90°.',17)
    svg.text(1110,697,'The existing C column is bypassed.',17)
    svg.text(32,758,'The green outline marks the original centre channel.',20,True)
    svg.text(32,793,'The three new C ports along the bottom are auxiliary. They must not replace the original centre at the final rule tile.',16)
    svg.text(32,837,'Height still to resolve: the preserved C column is one layer below the newest outputs.',18,True)
    svg.text(32,872,'The post proposes raising the C end of the first orange pieces, or reaching down to it with a stepped final piece.',16)
    svg.text(32,918,'Fixed X blockers in the blue separator surround the work area. They carry no data and obstruct misplaced orange pieces.',16)
    svg.text(32,973,'These are dimensioned 2D port/footprint schematics. They do not yet specify C profiles or prove that wrong placements are impossible.',14)
    svg.save(path)


if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    report=verify()
    catalogue(OUT/'05_orange_eight_faces.svg')
    placement(OUT/'06_orange_placement.svg')
    report['orange_geometry_draft']={'length_over_L':.8,'width_over_L':.2,'pitch_over_L':.2,
        'local_x_over_L':[.1,.3,.5,.7],'local_y_over_L':.1,
        'global_work_region_over_L':[.1,.9], 'status':'Port map and proposed footprint; C profile and height bridges unspecified.'}
    (OUT/'orange-2d-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 512 neighbourhoods; eight orange cases; dimensioned faces and placement written.')
