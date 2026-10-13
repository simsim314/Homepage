#!/usr/bin/env python3
"""Draw actual blue output coordinates and the first horizontal orange pass.

Python standard library only. C profiles follow the current square/diamond
proposal. This shows routing and one compaction layer, not a Life update.
"""
from itertools import product
from pathlib import Path
import json

from blue_circle_plus_schematic import Svg, output_face, output, INK
from orange_connector_design import bar, ring
from cgol_computational_tiles import blue_gather, orange_rows

OUT = Path(__file__).parent / 'computational-schematics'
FIELD = ((0,0,0,0,0), (0,0,1,0,0), (0,0,0,1,0),
         (0,1,1,1,0), (0,0,0,0,0))


def calculate():
    # Integer coordinates: one complete Life cell has width 10.
    ports, tiles, targets = {}, [], []
    for r,c in product(range(4), repeat=2):
        face = tuple(tuple(FIELD[r+i][c+j] for j in range(2)) for i in range(2))
        copied = output(face)
        for i,j in product(range(4), repeat=2):
            key = (r*10+5+(1,3,7,9)[i], c*10+5+(1,3,7,9)[j])
            assert key not in ports
            ports[key] = copied[i][j]
        tiles.append({'row':r, 'column':c, 'input':face, 'output':copied})
    for r,c in product(range(1,4), repeat=2):
        gathered = tuple(tuple(ports[(r*10+i,c*10+j)] for j in (2,4,6,8))
                         for i in (2,4,6,8))
        neighbourhood = tuple(tuple(FIELD[r+i][c+j] for j in (-1,0,1))
                              for i in (-1,0,1))
        assert gathered == blue_gather(neighbourhood)
        rows = orange_rows(gathered)
        assert tuple(row.centre for row in rows) == (FIELD[r-1][c], FIELD[r][c],
                                                     FIELD[r][c], FIELD[r+1][c])
        for incoming, outgoing in zip(gathered, rows):
            assert sum(outgoing.compacted) == incoming[0]+incoming[1]+incoming[3]
        targets.append({'row':r, 'column':c, 'neighbourhood':neighbourhood,
                        'blue':gathered, 'orange':[row.face() for row in rows]})
    assert len(ports) == 256 and len(targets)*16 == 144
    return tiles, targets


def draw(path, tiles, targets):
    s = Svg(1400,1220)
    s.parts[1] = '<title>Glider: blue routing and the first horizontal orange layer</title>'
    s.text(36,43,'Glider: blue, then the first orange layer',28,True)
    s.text(36,80,'Same positions and scale in both views. All visible data connectors are raised outputs.',17)
    s.text(36,112,'The glider has one ring of zero cells around it; the central 3 × 3 cells receive orange strips.',16)
    for j,(kind,label) in enumerate((('0','0'),('1','1'),('C0','C0'),('C1','C1'))):
        x=48+j*112
        ring(s,x,148,kind,2.4)
        s.text(x+17,154,label,15)
    s.text(510,154,'X = fixed separator blocker',15,color='#786f8b')
    # Small seed, retaining the same orientation as the two large views.
    for r,c in product(range(5),repeat=2):
        x,y=1238+c*19,27+r*19
        s.parts.append(f'<rect x="{x}" y="{y}" width="18" height="18" fill="{INK if FIELD[r][c] else "#e5eff5"}"/>')
    s.text(1230,143,'Input glider',13)
    L, top = 150, 212
    for panel,left in enumerate((36,746)):
        s.text(left,192,'1. BLUE · 16 routing pieces' if not panel else '2. ORANGE · first pass, horizontal',21,True)
        for tile in tiles:
            output_face(s,left+tile['column']*L,top+tile['row']*L,tile['input'],L)
        if panel:
            for target in targets:
                x=left+(target['column']-.4)*L
                y=top+(target['row']-.4)*L
                for i,row in enumerate(target['orange']):
                    bar(s,x,y+i*.2*L,row,.2*L)
        # One target is highlighted identically, independent of blue boundaries.
        x,y=left+1.6*L,top+1.6*L
        s.parts.append(f'<rect x="{x-4}" y="{y-4}" width="{.8*L+8}" height="{.8*L+8}" fill="none" stroke="#237a65" stroke-width="3"/>')
    s.text(36,846,'Each blue piece repeats its 2 × 2 input in four corner groups.',16)
    s.text(746,846,'36 orange strips: four per target cell. Blue padding stays exposed.',16)
    s.text(36,879,'Green outline: one target cell’s gathered neighbourhood, enlarged below.',17,True,color='#237a65')
    target = next(t for t in targets if (t['row'],t['column']) == (2,2))
    s.text(36,921,'Blue top / orange underside',18,True)
    s.text(448,921,'Orange top',18,True)
    for i,(incoming,outgoing) in enumerate(zip(target['blue'],target['orange'])):
        y=942+i*49
        bar(s,36,y,incoming,43)
        s.arrow(234,y+21,406)
        bar(s,448,y,outgoing,43)
        n=incoming[0]+incoming[1]+incoming[3]
        s.text(652,y+27,f'{incoming[0]} + {incoming[1]} + {incoming[3]} = {n}; keep C{incoming[1]}',17)
    s.text(983,951,'For each input (x, y, y, z):',17,True)
    s.text(983,983,'count x + y + z once,',17)
    s.text(983,1015,'pack the ones to the left,',17)
    s.text(983,1047,'carry y separately as C.',17)
    s.text(983,1095,'C0: square · C1: diamond',16)
    s.text(36,1178,'This is not the next Life generation: the second orange pass, purple and black/white layers still follow.',17,True)
    s.save(path)


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    tiles,targets = calculate()
    draw(OUT/'08_glider_blue_orange.svg', tiles,targets)
    report={'input':FIELD, 'blue_tiles':tiles, 'orange_targets':targets,
            'verified_blue_ports':144, 'orange_strips':36,
            'stage':'Blue routing followed by first horizontal orange pass only'}
    (OUT/'08_glider_blue_orange.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Verified 144 blue-to-orange inputs and 36 orange strips across 9 target cells.')
