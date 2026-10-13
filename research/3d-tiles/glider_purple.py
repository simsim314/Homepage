#!/usr/bin/env python3
"""Purple classification of the glider; Python SVG, with explicit port checks.

Purple output badges are logical labels, not finalized connector profiles.
The wildcard drawing combines ordinary zero/one input cavities. Fixed blue
X blockers are unrelated. All inputs must be supplied by a completed layer.
"""
from itertools import product
import json
from blue_circle_plus_schematic import Svg, output_face
from orange_connector_design import bar, ring
from glider_blue_orange import calculate, OUT
from glider_second_orange import checked_layers, vertical_bar
from cgol_computational_tiles import compute, rotate, verify
from layer_assembly import require_complete_layer, require_inputs

PURPLE='#7d529b'


def classify(t):
    trace=compute(t['neighbourhood'])
    tile,turns,mask=trace.matches[0]
    # Published masks pack bottom/right; our displayed orange face packs top/left.
    actual=tuple(tuple(t['second'][c][r] for c in range(3)) for r in range(3))
    mask=rotate(rotate(mask))
    assert actual==rotate(rotate(trace.interior))
    require_inputs([(actual[r][c], '*' if mask[r][c]=='X' else int(mask[r][c]))
                    for r,c in product(range(3),repeat=2)])
    category=trace.category if trace.category in ('3','4') else 'other'
    return {'tile':tile.name,'turns_from_published':(turns+2)%4,
            'mask':mask,'actual':actual,'total':sum(map(sum,actual)),
            'output':category}


def input_grid(s,x,y,mask,p):
    """Assembly-coordinate view of purple underside (not a flipped bottom view)."""
    for r,c in product(range(3),repeat=2):
        xx,yy=x+c*p,y+r*p
        s.parts.append(f'<rect x="{xx}" y="{yy}" width="{p}" height="{p}" fill="#f0e6f5" stroke="{PURPLE}"/>')
        value=mask[r][c]
        for kind in ('0','1') if value=='X' else (value,):
            ring(s,xx+p/2,yy+p/2,kind,p/12)
    s.parts.append(f'<rect x="{x}" y="{y}" width="{3*p}" height="{3*p}" fill="none" stroke="{PURPLE}" stroke-width="3"/>')


def draw(path,tiles,targets):
    s=Svg(1400,1320)
    s.parts[1]='<title>Glider: purple classification after both orange layers</title>'
    s.text(36,43,'Next: purple tiles classify the packed total',28,True)
    s.text(36,80,'Nine supplied bits in; one of three logical output classes: 3, 4, or other. The count includes the centre.',17)
    s.text(36,115,'Complete the second orange layer first. Circle = 0; plus = 1; circle + plus socket = either bit.',16)
    s.text(36,149,'Purple output badges below are signal labels; their physical connector profiles are not yet specified.',16,color=PURPLE)
    L,top=150,212
    for stage,left in enumerate((36,746)):
        s.text(left,192,('1. Second orange layer complete','2. Purple layer complete · 9 pieces')[stage],21,True)
        for tile in tiles:
            output_face(s,left+tile['column']*L,top+tile['row']*L,tile['input'],L)
        for t in targets:
            x,y=left+(t['column']-.4)*L,top+(t['row']-.4)*L
            # Retained first-pass C side column, one layer below orange pass 2.
            for i,row in enumerate(t['orange']):
                s.parts.append(f'<rect x="{x+.6*L}" y="{y+i*.2*L}" width="{.2*L}" height="{.2*L}" fill="#fffefa" stroke="#aaa"/>')
                ring(s,x+.7*L,y+(i+.5)*.2*L,row[-1],L/60)
            for c,col in enumerate(t['second']):vertical_bar(s,x+c*.2*L,y,col,.2*L)
            if stage:
                out=t['purple']['output']
                s.parts.append(f'<rect x="{x}" y="{y}" width="{.6*L}" height="{.6*L}" fill="#e8d8f0" stroke="{PURPLE}" stroke-width="3"/>')
                s.text(x+.3*L-(23 if out=='other' else 9),y+.3*L+8,out,18 if out=='other' else 26,True,PURPLE)
                s.text(x+7,y+.6*L-7,t['purple']['tile'],11,color=PURPLE)
        s.parts.append(f'<rect x="{left+1.6*L-4}" y="{top+1.6*L-4}" width="{.8*L+8}" height="{.8*L+8}" fill="none" stroke="#237a65" stroke-width="3"/>')
    s.text(36,848,'Top-left 3 × 3 in each target cell: nine ordinary bit outputs.',16)
    s.text(746,848,'C ports remain outside the purple footprint, at their existing heights.',16)
    s.text(36,893,'Highlighted cell: five ones are enough to select “other”',22,True,color='#237a65')
    t=next(t for t in targets if (t['row'],t['column'])==(2,2))
    p=57;y=946
    s.text(36,928,'Orange outputs',17,True)
    input_grid(s,36,y,tuple(tuple(str(v) for v in row) for row in t['purple']['actual']),p)
    s.arrow(232,y+85,292)
    s.text(318,928,'Purple underside · P5a',17,True)
    input_grid(s,318,y,t['purple']['mask'],p)
    s.arrow(514,y+85,574)
    s.text(600,928,'Purple top',17,True)
    s.parts.append(f'<rect x="600" y="{y}" width="171" height="171" fill="#e8d8f0" stroke="{PURPLE}" stroke-width="3"/>')
    s.text(645,y+94,'other',27,True,PURPLE)
    s.text(825,967,'Five plus-only sockets require five 1s.',17,True)
    s.text(825,1000,'The other four sockets accept 0 or 1.',17)
    s.text(825,1033,'All nine sockets still need a connector.',17,True)
    s.text(825,1066,'This tile therefore recognizes a total of 5 or more.',16)
    s.text(36,1158,'Three output classes feed the black/white layer:',19,True)
    s.text(36,1194,'3: live for either centre state.     4: live only for C1.     Other: dead for either centre state.',17)
    s.text(36,1240,'The original centre travels separately on the right-hand C column; it is not replaced by the count.',17)
    s.text(36,1283,'Colours identify layers. Connector shape, not colour, will distinguish the three purple output signals.',16,color=PURPLE)
    s.save(path)


if __name__=='__main__':
    tiles,targets=calculate()
    report=checked_layers(tiles,targets)
    ids={(t['row'],t['column'],c) for t in targets for c in range(3)}
    require_complete_layer(ids,ids)
    for t in targets:t['purple']=classify(t)
    # Validate the actual displayed orientation for every possible neighbourhood.
    for bits in product((0,1),repeat=9):
        grid=tuple(tuple(bits[r*3:r*3+3]) for r in range(3))
        tr=compute(grid)
        classify({'neighbourhood':grid,'second':[c.face() for c in tr.columns]})
    report['purple_orientations_checked']=512
    report['full_logic']=verify()
    draw(OUT/'10_glider_purple.svg',tiles,targets)
    (OUT/'10_glider_purple.json').write_text(json.dumps({'checks':report,'targets':targets},indent=2)+'\n')
    print('Validated 512 purple input matches in the displayed orientation; 9 glider purple pieces drawn.')
