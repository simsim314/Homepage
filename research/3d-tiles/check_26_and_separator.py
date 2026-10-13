#!/usr/bin/env python3
"""Check the forum's logical 26-tile construction and draw a NEW spacer proposal.

No third-party Python dependencies. Xs on the proposed blue face are positional
spacer markers, not an implementation of the purple layer's wildcard predicate.
Source: https://conwaylife.com/forums/viewtopic.php?p=73033#p73033
"""
from pathlib import Path
from itertools import product
from collections import defaultdict
import json
import cgol_computational_tiles as logic
from blue_circle_plus_schematic import Svg, input_face, output_face, dimension, INK

OUT=Path(__file__).parent/'blue-schematics'


def spacer_centres():
    # Nine L/5 squares in the middle row/column, each containing 2x2 Xs.
    return tuple(((c+(dc+.5)/2)/5,(r+(dr+.5)/2)/5)
                 for r,c in product(range(5),repeat=2) if r==2 or c==2
                 for dr,dc in product(range(2),repeat=2))


def draw_spacer_proposal():
    svg=Svg(1160,660)
    svg.parts[1]='<title>Proposed blue separator keys, distinct from logical wildcard masks</title>'
    svg.text(32,43,'Blue tile — proposed X-filled separator',27,True)
    svg.text(32,78,'The 16 data outputs stay in their four corner groups. Only the middle cross receives X markers.',16)
    face=((0,1),(0,0))
    svg.text(65,128,'BOTTOM: four inward inputs',21,True)
    input_face(svg,65,155,face,330)
    svg.arrow(455,320,558)
    svg.text(615,128,'TOP: data + outward spacer keys',21,True)
    output_face(svg,615,155,face,330,blockers=False)
    for xx,yy in spacer_centres():
        x,y=615+330*xx,155+330*yy
        radius=330*.018
        svg.line(x-radius,y-radius,x+radius,y+radius,sw=2,color='#927b60')
        svg.line(x-radius,y+radius,x+radius,y-radius,sw=2,color='#927b60')
    # Boundaries of the nine L/5 spacer squares, only within the cross.
    for i in (1,2,3,4):
        svg.line(615+330*.4,155+330*i/5,615+330*.6,155+330*i/5,color='#b5ada0')
        svg.line(615+330*i/5,155+330*.4,615+330*i/5,155+330*.6,color='#b5ada0')
    dimension(svg,615+330*.4,615+330*.6,510,'L/5')
    svg.text(65,559,'Input region: 2L/3; border: L/6.',17)
    svg.text(615,559,'9 spacer squares × 4 Xs = 36 X markers.',17)
    svg.text(32,610,'Proposed spacer layout only. A fixed X-shaped key is different from a cavity that accepts either 0 or 1.',16)
    path=OUT/'07_blue_separator_proposal.svg'
    svg.save(path)
    return path


def audit():
    report=logic.verify()
    by_total=defaultdict(set)
    by_mask=defaultdict(set)
    for bits in product((0,1),repeat=9):
        grid=tuple(bits[k:k+3] for k in (0,3,6))
        tr=logic.compute(grid)
        total=sum(bits)
        by_total[total].add(tr.interior)
        for tile,turns,mask in tr.matches:
            by_mask[tile.name].add(total)
        # Four-case B/W decision, independently of the mask names.
        assert tr.output==int(total==3 or (total==4 and grid[1][1]==1))
    xs=spacer_centres()
    assert len(xs)==len(set(xs))==36
    # Rotation invariance of the fixed filler scheme preserves the six blue types.
    points={(round(x,6),round(y,6)) for x,y in xs}
    assert points=={(round(1-y,6),round(x,6)) for x,y in xs}
    data={(x,y) for x,y in product((.1,.3,.7,.9),repeat=2)}
    assert not data & points
    report['packed_shapes_per_total']={str(t):len(v) for t,v in sorted(by_total.items())}
    report['purple_mask_accepted_totals']={k:sorted(v) for k,v in by_mask.items()}
    report['orange_catalogue']=[{'input':[x,y,y,z], 'output':logic.orange(x,y,y,z).face()}
                                for x,y,z in product((0,1),repeat=3)]
    report['separator_proposal']={'spacer_squares':9,'x_markers_per_square':4,
        'x_markers':36,'data_outputs':16,'fractional_x_centres':xs,
        'status':'New positional spacer proposal. No physical wildcard/full-fit proof.'}
    report['historical_note']='The 2019 posts explicitly allow wildcard cavity gaps; they do not specify this new 20% separator or its filler geometry.'
    return report


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    report=audit()
    (OUT/'26-tile-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:report[k] for k in ('result','neighbourhoods_checked','packed_interiors_checked','packed_shapes_per_total','purple_mask_accepted_totals')},indent=2))
    print(draw_spacer_proposal())
