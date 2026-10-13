#!/usr/bin/env python3
"""Blue routing: contiguous 2x2 corner inputs, full-width 4x4 output.

L denotes both Life-cell width and blue-tile width. Life connectors are at
L/6 and 5L/6. A blue tile is centred on a junction of four Life cells;
its four inputs lie at L/3 and 2L/3 in its local coordinates. The input
region consists of four contiguous L/3 squares, surrounded by L/6 margins.
Its top repeats the input in four 0.4L square groups separated by a 0.2L cross carrying nine fixed X blockers.
Standalone standard-library Python; nominal integer-offset fit checks only.
"""

from collections import Counter
from html import escape
from itertools import product
import json
from pathlib import Path

INK, BLUE, PAPER = '#233c43', '#5188b4', '#f6f5ef'


def rotate(face):
    return tuple(tuple(row) for row in zip(*face[::-1]))


def representative(face):
    versions = []
    for _ in range(4):
        versions.append(face)
        face = rotate(face)
    return min(versions)


def output(face):
    return tuple(tuple(face[r % 2][c % 2] for c in range(4)) for r in range(4))


def profile(bit):
    # C4-symmetric equal-depth plugs and matching cavities. Neither value
    # profile is contained in the other, so wrong bits physically collide.
    if bit == 0:
        return frozenset((x, y) for x, y in product(range(-3, 4), repeat=2)
                         if 4 <= x*x + y*y <= 9)
    return frozenset({(i, 0) for i in range(-3, 4)} | {(0, i) for i in range(-3, 4)})


def verify_geometry():
    size, blue_size = 60, 60  # Life centres 10,50; blue-local centres 20,40.
    assert not (profile(0) <= profile(1))
    assert not (profile(1) <= profile(0))
    # Lower plugs of both possible values at every anchor: this allows MORE
    # data assignments than valid Life cells, making rejection independent of bits.
    available = set()
    for cx, cy, px, py, bit in product(range(2), range(2), (10, 50), (10, 50), range(2)):
        available.add(frozenset((x + cx * size + px, y + cy * size + py)
                               for x, y in profile(bit)))
    checked, offsets = 0, set()
    for bits, turns in product(product((0, 1), repeat=4), range(4)):
        local = []
        for bit, (cx, cy) in zip(bits, ((20, 20), (40, 20), (20, 40), (40, 40))):
            shape = frozenset((x + cx, y + cy) for x, y in profile(bit))
            for _ in range(turns):
                shape = frozenset((blue_size - y, x) for x, y in shape)
            local.append(shape)
        for dx, dy in product(range(size), repeat=2):
            fits = all(frozenset((x + dx, y + dy) for x, y in shape) in available
                       for shape in local)
            assert fits == ((dx, dy) == (30, 30)), (bits, turns, dx, dy)
            if fits:
                offsets.add((dx, dy))
            checked += 1
    return {'placement_checks': checked, 'life_cell_pitch': size,
            'blue_piece_width': blue_size,
            'life_connector_coordinates': [10, 50], 'blue_input_coordinates': [20, 40],
            'only_valid_offset_modulo_cell': sorted(offsets),
            'scope': 'Exact nominal ring/plus profiles, integer offsets and quarter-turns; no print tolerance proof.'}


class Svg:
    def __init__(self, width=1440, height=1170):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                      f'viewBox="0 0 {width} {height}" role="img">',
                      '<title>Six blue tile faces using circle and plus connectors</title>',
                      '<style>text{font-family:DejaVu Sans,Arial,sans-serif}</style>',
                      f'<rect width="100%" height="100%" fill="{PAPER}"/>']

    def text(self, x, y, value, size=16, bold=False, color=INK):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" '
                          f'font-weight="{"bold" if bold else "normal"}" fill="{color}">{escape(str(value))}</text>')

    def line(self, x1, y1, x2, y2, dashed=False, sw=1, color='#b9c8c2'):
        dash = ' stroke-dasharray="3 4"' if dashed else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="{color}" stroke-width="{sw}"{dash}/>')

    def arrow(self, x1, y, x2):
        self.line(x1, y, x2, y, sw=2, color=INK)
        self.line(x2 - 8, y - 5, x2, y, sw=2, color=INK)
        self.line(x2 - 8, y + 5, x2, y, sw=2, color=INK)

    def symbol(self, x, y, bit, radius):
        if bit == 0:
            self.parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="none" '
                              f'stroke="{BLUE}" stroke-width="{radius * .35}"/>')
        else:
            self.line(x - radius, y, x + radius, y, sw=radius * .35, color=BLUE)
            self.line(x, y - radius, x, y + radius, sw=radius * .35, color=BLUE)

    def face(self, x, y, values, side, construction=False, positions=None, radius_factor=.088, fill='#fffefa'):
        n = len(values)
        cell = side / n
        self.parts.append(f'<rect x="{x}" y="{y}" width="{side}" height="{side}" '
                          f'fill="{fill}" stroke="{INK}" stroke-width="1.5"/>')
        if n == 4:
            for i in range(1, n):
                self.line(x + i * cell, y, x + i * cell, y + side, True)
                self.line(x, y + i * cell, x + side, y + i * cell, True)
        if construction:
            # Whole Life cell has ONE 3x3 guide grid, not a separate guide
            # grid in each half-cell piece.
            for third in (1, 2):
                self.line(x + third * side / 3, y, x + third * side / 3, y + side, True, color='#d6dfd7')
                self.line(x, y + third * side / 3, x + side, y + third * side / 3, True, color='#d6dfd7')
        for r, row in enumerate(values):
            for c, bit in enumerate(row):
                xx = x + (positions[c] * side if positions else (c + .5) * cell)
                yy = y + (positions[r] * side if positions else (r + .5) * cell)
                self.symbol(xx, yy, bit, side * radius_factor)

    def save(self, path):
        path.write_text('\n'.join(self.parts + ['</svg>']), encoding='utf8')


def input_face(svg, x, y, face, side):
    # The INPUT REGION is 2L/3 wide. Its four squares are contiguous.
    # The symbols are at L/3,2L/3, NOT at the Life-cell corner coordinates.
    svg.parts.append(f'<rect x="{x}" y="{y}" width="{side}" height="{side}" fill="#fffefa" stroke="{INK}" stroke-width="2"/>')
    margin, region = side/6, side*2/3
    svg.parts.append(f'<rect x="{x+margin}" y="{y+margin}" width="{region}" height="{region}" fill="#e5eff5" stroke="{BLUE}" stroke-width="2"/>')
    svg.line(x+side/2, y+margin, x+side/2, y+side-margin, color=BLUE)
    svg.line(x+margin, y+side/2, x+side-margin, y+side/2, color=BLUE)
    for r,c in product(range(2), repeat=2):
        svg.symbol(x+(c+1)*side/3, y+(r+1)*side/3, face[r][c], side*.055)



def output_face(svg, x, y, face, side, blockers=True):
    # Four 2x2 groups, anchored at the corners. The middle 20% of each
    # axis holds fixed X registration blockers, not logical wildcard ports.
    group = side * .4
    svg.parts.append(f'<rect x="{x}" y="{y}" width="{side}" height="{side}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    for row,col in product(range(2),repeat=2):
        gx,gy=x+col*side*.6,y+row*side*.6
        svg.parts.append(f'<rect x="{gx}" y="{gy}" width="{group}" height="{group}" fill="#e5eff5" stroke="{BLUE}" stroke-width="1.5"/>')
        svg.line(gx+group/2,gy,gx+group/2,gy+group,color=BLUE)
        svg.line(gx,gy+group/2,gx+group,gy+group/2,color=BLUE)
        for r,c in product(range(2),repeat=2):
            svg.symbol(gx+(c+.5)*group/2,gy+(r+.5)*group/2,face[r][c],side*.045)


    if blockers:
        for r,c in product(range(5),repeat=2):
            if r!=2 and c!=2:continue
            cx,cy=x+(c+.5)*side/5,y+(r+.5)*side/5
            d=side*.075/(2**.5)
            svg.line(cx-d,cy-d,cx+d,cy+d,sw=side/60,color='#786f8b')
            svg.line(cx-d,cy+d,cx+d,cy-d,sw=side/60,color='#786f8b')


def dimension(svg, x1, x2, y, label):
    svg.line(x1,y,x2,y,color=INK)
    for x in (x1,x2):
        svg.line(x,y-5,x,y+5,color=INK)
    svg.text((x1+x2)/2-3.9*len(label),y+23,label,15)


def draw(path):
    svg=Svg(1400,1110)
    svg.text(35,42,'Blue input: four ADJACENT corner squares',28,True)
    svg.text(35,76,'L = Life-cell width = blue-tile width. Each lower Life cell still repeats ONE value at its four corners.',16)
    face=((0,0),(0,1))
    svg.text(35,119,'1. Four Life cells meeting at a corner',19,True)
    x,y,cell=45,145,150
    for r,c in product(range(2),repeat=2):
        bit=face[r][c]
        svg.face(x+c*cell,y+r*cell,((bit,bit),(bit,bit)),cell,True,(1/6,5/6),.045)
    # Highlight the four adjacent L/3 squares; no obscuring fill.
    left,top=x+cell*2/3,y+cell*2/3
    svg.parts.append(f'<rect x="{left}" y="{top}" width="{cell*2/3}" height="{cell*2/3}" fill="none" stroke="#bd732c" stroke-width="4"/>')
    svg.text(35,475,'Orange: contiguous 2×2 input region.',16)
    svg.text(35,502,'One corner square from each Life cell.',16)
    svg.arrow(375,285,420)
    svg.text(459,119,'2. Blue bottom — recessed input',19,True)
    input_face(svg,470,145,face,300)
    dimension(svg,470,520,465,'L/6')
    dimension(svg,520,720,465,'2L/3')
    dimension(svg,720,770,465,'L/6')
    svg.text(459,517,'Four touching squares, each L/3 × L/3.',16)
    svg.text(459,543,'Symbol centres: L/3 and 2L/3.',16)
    svg.arrow(795,285,845)
    svg.text(890,119,'3. Blue top — raised output',19,True)
    output_face(svg,900,145,face,300)
    dimension(svg,900,1020,465,'0.4L')
    dimension(svg,1020,1080,465,'0.2L')
    dimension(svg,1080,1200,465,'0.4L')
    svg.text(890,517,'Four data groups + nine fixed raised Xs.',16)
    svg.text(890,543,'Each 2×2 group repeats the input. Total: L × L.',16)
    svg.text(35,590,'Six types up to rotation — bottom input → top output',23,True)
    classes=Counter(representative((bits[:2],bits[2:])) for bits in product((0,1),repeat=4))
    names=('All circles','One plus','Two adjacent pluses','Two diagonal pluses','Three pluses','All pluses')
    for i,((face,count),name) in enumerate(zip(sorted(classes.items()),names)):
        x,y=35+(i%3)*458,627+(i//3)*228
        svg.text(x,y,name,18,True)
        input_face(svg,x,y+22,face,156)
        svg.arrow(x+176,y+100,x+210)
        output_face(svg,x+230,y+22,face,156)
        svg.text(x,y+201,f'{count} orientation(s)',13)
    svg.save(path)


def draw_placement(path):
    svg = Svg(1420, 760)
    svg.text(32, 43, 'Circle and plus geometry: the spacing forces the corner', 27, True)
    svg.text(32, 79, 'A Life cell is divided into an invisible 3x3 grid. Its four keys sit in the CENTRES of the four corner squares.', 16)
    svg.text(32, 108, 'Life corner centres are separated by 2L/3; blue input centres are separated by L/3.', 15)
    for col, (offset, title, fits) in enumerate((((.5, .5), 'CORNER: full match', True),
                                               ((.5, 0), 'EDGE: no match', False),
                                               ((0, 0), 'CELL CENTRE: no match', False))):
        x, y, side = 40 + col * 470, 172, 184
        svg.text(x, y - 22, title, 19, True, '#286959' if fits else '#9e5549')
        for r, c in product(range(2), repeat=2):
            svg.face(x + c * side, y + r * side, ((0, 0), (0, 0)), side,
                     True, (1/6, 5/6), .044)
        bx, by = x + offset[0] * side, y + offset[1] * side
        blue_side = side
        color = '#286959' if fits else '#9e5549'
        for xx, yy in ((bx, by), (bx + blue_side, by)):
            svg.line(xx, yy, xx, yy + blue_side, True, 3, color)
        for yy in (by, by + blue_side):
            svg.line(bx, yy, bx + blue_side, yy, True, 3, color)
        # Small coloured rings mark the cavity centres. Their overlap with
        # the lower circle centres, rather than a wildcard region, is shown.
        for r, c in product((1/3, 2/3), repeat=2):
            svg.parts.append(f'<circle cx="{bx+c*blue_side}" cy="{by+r*blue_side}" r="{side*.044}" '
                             f'fill="none" stroke="{color}" stroke-width="2"/>')
        svg.text(x, 568, 'Blue circles = lower keys; coloured circles = blue recesses.', 11)
    svg.text(32, 614, 'Blue width L. Input region: 2L/3 with L/6 margins. Input centres: L/3 and 2L/3.', 17, True)
    svg.text(32, 645, 'Centred on the junction, inputs coincide with lower keys at 5L/6 and 7L/6.', 16)
    svg.text(32, 688, 'Verified with nominal ring/plus profiles: 230,400 integer-offset/value/quarter-turn checks; only the corner offset fits.', 15)
    svg.text(32, 722, 'The spacing carries the alignment constraint. Both value symbols remain C4-symmetric; the six-type reduction is preserved.', 15)
    svg.save(path)


def draw_previous_layer(path):
    """Every Life cell carries FOUR IDENTICAL values. Mixed inputs span cells."""
    svg = Svg(1420, 1240)
    svg.text(32, 43, 'Previous Life-state layer: one value per cell, four identical corners', 27, True)
    svg.text(32, 79, 'A mixed 2x2 input belongs to a blue piece BETWEEN four Life cells. It is not the state of one Life cell.', 16)

    def cells(x, y, field, size, junction=None):
        for r, row in enumerate(field):
            for c, bit in enumerate(row):
                four_copies = ((bit, bit), (bit, bit))
                assert len({value for line in four_copies for value in line}) == 1
                svg.face(x + c * size, y + r * size, four_copies, size, True,
                         (1/6, 5/6), .044, '#e0edf1' if bit else '#fffefa')
        if junction:
            jr, jc = junction
            bx, by = x + (jc - 1/3) * size, y + (jr - 1/3) * size
            bs = size * 2/3
            svg.parts.append(f'<rect x="{bx}" y="{by}" width="{bs}" height="{bs}" '
                             'fill="none" stroke="#a56b36" '
                             'stroke-width="3" stroke-dasharray="5 3"/>')

    svg.text(40, 127, 'Four adjacent Life cells', 21, True)
    cells(40, 151, ((0, 0), (0, 1)), 148, (1, 1))
    svg.text(40, 475, 'Three dead cells: four circles EACH.', 16)
    svg.text(40, 502, 'One live cell: four pluses.', 16)
    svg.text(40, 537, 'Orange outline = four touching corner squares (input region).', 14)

    svg.text(570, 127, 'Glider padded with zero cells', 21, True)
    glider = ((0, 1, 0), (0, 0, 1), (1, 1, 1))
    field = ((0, 0, 0, 0, 0),) + tuple((0, *row, 0) for row in glider) + ((0, 0, 0, 0, 0),)
    assert sum(map(sum, field)) == 5
    cells(570, 151, field, 76, (2, 2))
    svg.text(1000, 183, 'Each outlined square is', 16)
    svg.text(1000, 211, 'one complete Life cell.', 16)
    svg.text(1000, 255, 'Blue tint: live cell.', 16)
    svg.text(1000, 283, 'White: dead cell.', 16)
    svg.text(1000, 327, 'The dotted 3x3 guides', 16)
    svg.text(1000, 355, 'are inside each cell.', 16)
    svg.text(1000, 399, 'Every blue input takes', 16)
    svg.text(1000, 427, 'one corner from each', 16)
    svg.text(1000, 455, 'of four adjacent cells.', 16)

    svg.text(32, 598, 'Six junction configurations, shown in their actual cell context', 23, True)
    classes = Counter(representative((bits[:2], bits[2:])) for bits in product((0, 1), repeat=4))
    names = ('All four cells dead', 'One live cell', 'Two adjacent live cells',
             'Two diagonal live cells', 'Three live cells', 'All four cells live')
    for i, ((face, count), name) in enumerate(zip(sorted(classes.items()), names)):
        x, y = 40 + (i % 3) * 465, 644 + (i // 3) * 271
        svg.text(x, y, name, 18, True)
        cells(x, y + 21, face, 88, (1, 1))
        svg.text(x + 203, y + 79, f'{count} orientation(s)', 14)
        svg.text(x + 203, y + 106, 'One blue type', 14)
        svg.text(x, y + 223, 'Four complete cells; same symbol in every corner of each.', 12)
    svg.text(32, 1190, 'This figure is ONLY the previous Life-state layer and blue INPUT locations. No blue output assumption is made here.', 14)
    svg.save(path)



def draw_glider_routing(path):
    """Compute every blue tile from the actual four cells at its junction."""
    glider=((0,1,0),(0,0,1),(1,1,1))
    field=((0,0,0,0,0),)+tuple((0,*row,0) for row in glider)+((0,0,0,0,0),)
    tiles=[]
    for r,c in product(range(4),repeat=2):
        incoming=tuple(tuple(field[r+dr][c+dc] for dc in range(2)) for dr in range(2))
        top=output(incoming)
        for qr,qc in product(range(2),repeat=2):
            assert tuple(tuple(top[qr*2+a][qc*2+b] for b in range(2)) for a in range(2))==incoming
        tiles.append({'row':r,'column':c,'input':incoming,'output':top})
    assert sum(map(sum,field))==5
    # Every live cell is internal and touches four junctions; each junction
    # repeats that value four times. This catches missing/extra copies.
    plus_count=sum(sum(map(sum,t['output'])) for t in tiles)
    assert plus_count==5*4*4
    svg=Svg(1530,1060)
    svg.parts[1]='<title>Glider input and computed blue routing output</title>'
    svg.text(35,44,'Glider — input and computed blue-layer output',29,True)
    svg.text(35,79,'Circle = 0. Plus = 1. Both layers are viewed from above, at the same scale and orientation.',17)
    svg.text(35,126,'INPUT · 5×5 Life cells',22,True)
    svg.text(850,126,'OUTPUT · 4×4 blue tiles at the junctions',22,True)
    x,y,cell=35,172,120
    for r,c in product(range(5),repeat=2):
        bit=field[r][c]
        svg.face(x+c*cell,y+r*cell,((bit,bit),(bit,bit)),cell,True,(1/6,5/6),.052,
                 '#cfdfeb' if bit else '#fffefa')
    # Highlight the junction between rows 1/2 and columns 1/2 (zero-based).
    jr,jc=2,2
    hx,hy=x+(jc-1/3)*cell,y+(jr-1/3)*cell
    svg.parts.append(f'<rect x="{hx}" y="{hy}" width="{cell*2/3}" height="{cell*2/3}" fill="none" stroke="#bd732c" stroke-width="4"/>')
    svg.arrow(684,445,804)
    # Offset by half a Life cell: blue bodies centre on Life-cell junctions.
    ox,oy=850+cell/2,y+cell/2
    for tile in tiles:
        tx,ty=ox+tile['column']*cell,oy+tile['row']*cell
        output_face(svg,tx,ty,tile['input'],cell)
        # Strong seams distinguish physical tiles from the 2x2 groups.
        svg.parts.append(f'<rect x="{tx}" y="{ty}" width="{cell}" height="{cell}" fill="none" stroke="{INK}" stroke-width="2"/>')
    svg.parts.append(f'<rect x="{ox+cell}" y="{oy+cell}" width="{cell}" height="{cell}" fill="none" stroke="#bd732c" stroke-width="4"/>')
    svg.text(35,810,'Five live cells, padded with one ring of zero cells.',17)
    svg.text(35,841,'Each Life cell has four identical corner symbols.',17)
    svg.text(850,810,'Each blue tile copies its four inputs into four 2×2 groups.',16)
    svg.text(850,841,'Nine fixed X blockers per tile; separator width: 0.2L.',16)
    svg.text(35,903,'Orange example: the four adjacent corner inputs are copied into the matching orange-outlined output tile.',17,True)
    # A readable selected-junction example, calculated from the field.
    chosen=tiles[5]
    svg.text(35,948,'Selected input:',16)
    svg.text(200,948,'0  +',21,True)
    svg.text(200,982,'0  0',21,True)
    assert chosen['input']==((0,1),(0,0))
    svg.text(350,948,'The output tile contains four copies of this arrangement.',17)
    svg.text(350,982,'This is routing only; the Life update rule has not yet been applied.',17)
    svg.save(path)
    report={'life_input':field,'blue_tiles':tiles,'output_plus_symbols':plus_count,
            'output_circle_symbols':16*16-plus_count,'output_gap_fraction':.2,'fixed_X_blockers_per_tile':9,
            'stage':'Blue copying/routing only, before the Life rule'}
    path.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    destination = Path(__file__).parent / 'blue-schematics' / '03_circle_plus_faces.svg'
    destination.parent.mkdir(parents=True, exist_ok=True)
    report = verify_geometry()
    draw(destination)
    draw_placement(destination.parent / '04_circle_plus_placement.svg')
    draw_previous_layer(destination.parent / '05_uniform_life_cells.svg')
    draw_glider_routing(destination.parent / '06_glider_blue_input_output.svg')
    (destination.parent / 'circle-plus-verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    print(json.dumps(report, indent=2))
    print(destination)
