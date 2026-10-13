#!/usr/bin/env python3
"""Draw and verify the 26-tile logical connection map, without adding filler Xs.

Shows real centre channels separately from auxiliary C channels. Geometry of
height bridges and wildcard sockets remains a separate construction problem.
"""
from pathlib import Path
from itertools import product
import json
import cgol_computational_tiles as t


def connect(grid):
    tr=t.compute(grid)
    # Same orientation as first orange output: ones pack left, then up.
    raw=tuple(tuple(tr.columns[c].compacted[r] for c in range(3)) for r in range(3))
    second=tuple((*raw[r],f'C{tr.rows[r].centre}') for r in range(3))+(tuple(f'A{p.centre}' for p in tr.columns)+(f'C{tr.rows[3].centre}',),)
    assert second[1][3]==second[2][3]==f'C{grid[1][1]}'
    assert sum(map(sum,raw))==sum(map(sum,grid))
    # A ports are derived from the packed middle ROW, not copies of the true centre.
    assert tuple(p.centre for p in tr.columns)==t.unary(sum(grid[1]))
    return tr,second


def audit():
    differing=0
    for bits in product((0,1),repeat=9):
        grid=tuple(bits[i:i+3] for i in (0,3,6))
        tr,second=connect(grid)
        differing+=any(p.centre!=grid[1][1] for p in tr.columns)
    return {'neighbourhoods_checked':512,'cases_with_auxiliary_flags_different_from_true_centre':differing,
            'required_channels':{'blue':'0/1','orange':'0/1 and typed C0/C1',
                                 'purple':'3,4,other','final':'new 0/1 repeated four times'},
            'scope':'Logical channels and canonical two-pass layout. Not a mechanical fit or mixed-orientation exclusion proof.'}


def draw(path):
    # A living glider cell with three live neighbours: inclusive count 4.
    grid=((0,0,1),(1,1,1),(0,0,0))
    tr,second=connect(grid)
    svg=t.Svg(1500,910)
    svg.text(32,43,'26 tiles: the connections after blue',28,weight='bold')
    svg.text(32,78,'Example: a live glider cell with three live neighbours. The total INCLUDING the centre is 4.',17)
    panels=[('Blue: gather around ONE Life cell',tr.blue,t.BLUE),
            ('Orange 1: four horizontal pieces',tuple(p.face() for p in tr.rows),t.ORANGE),
            ('Orange 2: three vertical pieces',second,t.ORANGE)]
    for i,(name,values,color) in enumerate(panels):
        x=35+i*490
        svg.text(x,128,name,20,weight='bold')
        svg.grid(x,158,values,color,cell=62)
        if i<2:svg.arrow(x+292,278,x+431)
    svg.text(35,457,'Each row is (x, y, y, z).',18)
    svg.text(35,488,'The middle two rows also agree.',17)
    svg.text(525,457,'Each piece: unary(x+y+z), C_y.',18)
    svg.text(525,488,'Right edge: C_N, C_centre, C_centre, C_S.',16)
    svg.text(1015,457,'Top-left 3×3: packed total = 4.',18)
    svg.text(1015,488,'Right edge: preserved from orange 1.',16)
    svg.text(1015,519,'Bottom A ports: auxiliary C-shaped outputs.',16)
    svg.text(1015,546,'A is a label here, NOT a new connector type.',14)
    svg.text(32,594,'Connections to the last two layers',23,weight='bold')
    svg.text(35,638,'Packed 3×3',19,weight='bold')
    svg.arrow(205,631,290)
    svg.text(314,638,'Purple: output category 4',19,weight='bold')
    svg.arrow(642,631,745)
    svg.text(767,638,'B/W: (4, C1) → live',19,weight='bold')
    svg.text(35,689,'Original centre C1',19,weight='bold')
    svg.line(257,682,699,682,t.ORANGE)
    svg.line(699,682,699,656,t.ORANGE)
    svg.arrow(699,656,745,t.ORANGE)
    svg.text(35,731,'The original centre bypasses counting. Other C ports must be ignored safely by the final piece.',17)
    svg.text(35,773,'The purple masks are oriented bottom/right in the post; this drawing packs top/left (a 180° rotation).',16)
    svg.text(35,822,'20% blue separator: nine fixed raised X blockers per blue tile. They carry no logical signal.',17)
    svg.text(35,863,'Remaining physical work: centre-channel height bridges, orientation enforcement, and wildcard socket geometry.',16)
    svg.save(path)


if __name__=='__main__':
    out=Path(__file__).parent/'computational-schematics'
    out.mkdir(exist_ok=True)
    report=audit()
    (out/'orange-connections-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    draw(out/'04_orange_connections.svg')
    print(json.dumps(report,indent=2))
