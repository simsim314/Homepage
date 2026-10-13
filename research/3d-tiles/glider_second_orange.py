#!/usr/bin/env python3
"""Python schematic: complete first orange layer, then complete second layer."""
from itertools import product
import json
from blue_circle_plus_schematic import Svg, output_face
from orange_connector_design import bar, ring, ORANGE
from cgol_computational_tiles import orange_rows, orange_columns
from glider_blue_orange import calculate, OUT
from layer_assembly import require_complete_layer, require_inputs


def vertical_bar(s,x,y,values,pitch):
    s.parts.append(f'<rect x="{x}" y="{y}" width="{pitch}" height="{4*pitch}" '
                   f'fill="#f6e4cd" stroke="{ORANGE}" stroke-width="2"/>')
    for i,v in enumerate(values):
        if i:s.line(x,y+i*pitch,x+pitch,y+i*pitch,True,color='#c9b194')
        ring(s,x+pitch/2,y+(i+.5)*pitch,str(v),pitch/12)


def checked_layers(tiles,targets):
    blue_ids={(t['row'],t['column']) for t in tiles}
    first_ids={(t['row'],t['column'],i) for t in targets for i in range(4)}
    require_complete_layer(blue_ids,blue_ids)
    first_connections=[(v,v) for t in targets for row in t['blue'] for v in row]
    require_inputs(first_connections)
    require_complete_layer(first_ids,first_ids)
    second_connections=[]
    for t in targets:
        rows=orange_rows(t['blue'])
        t['second']=[col.face() for col in orange_columns(rows)]
        for c in range(3):
            second_connections.extend((row.compacted[c],row.compacted[c]) for row in rows)
        assert sum(sum(col[:3]) for col in t['second']) == sum(map(sum,t['neighbourhood']))
    require_inputs(second_connections)
    # A missing first-layer piece is rejected even before trying an upper tile.
    for missing in first_ids:
        try: require_complete_layer(first_ids,first_ids-{missing})
        except ValueError: pass
        else: raise AssertionError('Missing orange tile accepted')
    for index in range(len(second_connections)):
        broken=second_connections.copy()
        broken[index]=(None,broken[index][1])
        try: require_inputs(broken)
        except ValueError: pass
        else: raise AssertionError('Unsupported input accepted')
    for v in (0,1): require_inputs([(v,'*')])
    try: require_inputs([(None,'*')])
    except ValueError: pass
    else: raise AssertionError('Wildcard accepted absent connector')
    return {'blue_tiles':16,'first_orange_tiles':36,'second_orange_tiles':27,
            'missing_tile_cases_rejected':36,'missing_input_cases_rejected':108,
            'wildcard_requires_present_connector':True}


def draw(path,tiles,targets):
    s=Svg(1400,1250)
    s.parts[1]='<title>Glider: first and second orange layers, with no bridging</title>'
    s.text(36,43,'Glider: the two orange layers',29,True)
    s.text(36,80,'Assembly rule: finish the whole previous layer; every input must connect. No bridging.',18,True)
    s.text(36,114,'Same padded glider and same scale. Second-pass pieces are the same orange type, rotated 90°.',17)
    for i,(kind,label) in enumerate((('0','0'),('1','1'),('C0','C0'),('C1','C1'))):
        x=48+i*112
        ring(s,x,149,kind,2.4);s.text(x+17,155,label,15)
    s.text(520,155,'Square/diamond: proposed C profiles. X: blue separator blocker.',15)
    L,top=150,214
    for stage,left in enumerate((36,746)):
        s.text(left,193,('1. Complete horizontal layer · 36 strips',
                        '2. Complete vertical layer · 27 strips')[stage],20,True)
        for tile in tiles:
            output_face(s,left+tile['column']*L,top+tile['row']*L,tile['input'],L)
        for t in targets:
            x,y=left+(t['column']-.4)*L,top+(t['row']-.4)*L
            for i,row in enumerate(t['orange']):bar(s,x,y+i*.2*L,row,.2*L)
            if stage:
                # The old C column remains exposed one layer below the new tops.
                s.parts.append(f'<rect x="{x+.6*L}" y="{y}" width="{.2*L}" height="{.8*L}" fill="#fffefa" stroke="#999" stroke-width="1"/>')
                for i,row in enumerate(t['orange']):
                    ring(s,x+.7*L,y+(i+.5)*.2*L,row[-1],L/60)
                for c,col in enumerate(t['second']):vertical_bar(s,x+c*.2*L,y,col,.2*L)
        s.parts.append(f'<rect x="{left+1.6*L-4}" y="{top+1.6*L-4}" width="{.8*L+8}" height="{.8*L+8}" fill="none" stroke="#237a65" stroke-width="3"/>')
    s.text(36,849,'Each four-slot row packs three bits and preserves its middle value.',16)
    s.text(746,849,'Only the three data columns receive second-pass orange pieces.',16)
    s.text(36,890,'Highlighted target cell after the second pass',21,True,color='#237a65')
    t=next(t for t in targets if (t['row'],t['column'])==(2,2))
    x,y,p=40,914,55
    for c,col in enumerate(t['second']):vertical_bar(s,x+c*p,y,col,p)
    for r,row in enumerate(t['orange']):
        s.parts.append(f'<rect x="{x+3*p}" y="{y+r*p}" width="{p}" height="{p}" fill="#fffefa" stroke="#aaa"/>')
        ring(s,x+3.5*p,y+(r+.5)*p,row[-1],p/12)
    s.parts.append(f'<rect x="{x+3*p-3}" y="{y+p-3}" width="{p+6}" height="{2*p+6}" fill="none" stroke="#237a65" stroke-width="3"/>')
    s.text(325,945,'Upper 3 × 3: five ones, the total of this original neighbourhood.',18,True)
    s.text(325,985,'Bottom three C ports: auxiliary values created by the second pass.',17)
    s.text(325,1025,'White right column: first-pass C ports, exposed ONE LAYER LOWER.',17,True)
    s.text(325,1065,'Its middle two C0 ports preserve the original centre (dead).',17)
    s.text(325,1105,'The connection from these lower C ports to the final layer still needs a 3D design.',16)
    s.text(36,1190,'Both orange passes are complete. Purple classification and the black/white output layer come next.',18,True)
    s.save(path)


if __name__=='__main__':
    tiles,targets=calculate()
    report=checked_layers(tiles,targets)
    draw(OUT/'09_glider_two_orange_layers.svg',tiles,targets)
    (OUT/'09_glider_two_orange_layers.json').write_text(json.dumps({'checks':report,'targets':targets},indent=2)+'\n')
    print(json.dumps(report,indent=2))
