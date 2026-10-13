#!/usr/bin/env python3
"""2D row section illustrating an actual solid-model registration counterexample."""
from pathlib import Path
from blue_circle_plus_schematic import Svg, INK

out=Path(__file__).parent/'blue-schematics'/'08_separator_registration.svg'
s=Svg(1220,850)
s.parts[1]='<title>Empty separator versus a raised registration blocker</title>'
s.text(30,43,'What the blue separator enforces',28,True)
s.text(30,78,'Top view of one row across TWO neighbouring blue tiles. All data values are 0.',17)
p=70
for row,(start,title,note,blocker) in enumerate((
    (3,'Correct placement','Four recesses engage four outputs across the blue-tile boundary.',False),
    (0,'Wrong placement, empty separator','Three recesses engage; one faces empty space. The solid can still seat.',False),
    (0,'Same wrong placement, raised X','The raised X collides with the circular recess and blocks seating.',True),
)):
    y=142+row*216
    s.text(30,y,title,21,True)
    x=450
    for i in range(10):
        gap=i%5==2
        s.parts.append(f'<rect x="{x+i*p}" y="{y-25}" width="{p}" height="{p}" fill="{"#f6f5ef" if gap else "#e5eff5"}" stroke="#b7c7cd"/>')
        cx,cy=x+(i+.5)*p,y+10
        if not gap:s.symbol(cx,cy,0,12)
        elif blocker:
            s.line(cx-12,cy-12,cx+12,cy+12,sw=4,color='#6c648f')
            s.line(cx-12,cy+12,cx+12,cy-12,sw=4,color='#6c648f')
    s.line(x+5*p,y-25,x+5*p,y+45,sw=3,color=INK)
    # Orange footprint and its four inward ports, projected onto the blue top.
    s.parts.append(f'<rect x="{x+start*p}" y="{y-25}" width="{4*p}" height="{p}" fill="none" stroke="#b87930" stroke-width="4"/>')
    for j in range(4):
        s.parts.append(f'<circle cx="{x+(start+j+.5)*p}" cy="{y+10}" r="20" fill="none" stroke="#b87930" stroke-width="2" stroke-dasharray="4 3"/>')
    s.text(30,y+90,note,17)
    if row==0:
        s.text(30,y+124,'Orange outline = one 4-input piece. Dashed rings = its recesses.',15)
s.text(30,789,'This demonstrates one wrong placement and a blocker for it. It is not yet a proof covering every translation and rotation.',15)
s.save(out)
print(out)
