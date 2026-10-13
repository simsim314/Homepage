#!/usr/bin/env python3
"""Standalone schematics and ideal geometry checks for corner-only blue tiles.

SUPERSEDED PROPOSAL: Michael clarified that the connectors must be circles
and pluses, not directional keys. These diagrams remain only an abandoned
proposal. See blue_circle_plus_schematic.py for the requested face symbols.

Run: python -S blue_geometry.py

Source logic: https://conwaylife.com/forums/viewtopic.php?p=73018#p73018
The original text describes six 4x4 blue types, four cell values as inputs,
and copied outputs. Physical notch profiles/locations were not fully defined.

NEW PROPOSAL, following Michael's directional-droplet suggestion:
One 32-unit Life square outputs its single bit on FOUR identical-value keys
at (8,8), (24,8), (8,24), (24,24). Their asymmetric tails point INWARDS.
A 32-unit blue tile reads four keys at these same local coordinates, but
expects OUTWARD tails. It can therefore seat at offset (16,16), crossing
four Life squares, rather than offset (16,0) on an edge or (0,0) at a centre.
Both 0 and 1 have the same directional tail and distinct equal-area tabs.
No wildcard sockets, extra clearance regions, or unmatched cavity volume.

Voxel cross-sections are extruded into upward plugs and exact bottom
recesses. All eight value/orientation profiles have equal area: a wrong
profile cannot hide inside a larger socket. Shapes are a coarse directional
key prototype, not literal smooth droplets and not recovered historical CAD.
Checks use exact nominal geometry: all 32x32 INTEGER offsets within one
Life-square period, all 16 input combinations, and all four quarter-turns.
No claim is made about printing tolerances, tilted insertion, intermediate
angles, mechanical attachment, or the rest of the five-layer construction.
"""

from collections import Counter
from html import escape
from itertools import product
import json
from pathlib import Path

SIZE = 32
ANCHORS = ((8, 8), (24, 8), (8, 24), (24, 24))
OUTWARD = (0, 1, 3, 2)  # NW, NE, SW, SE
INK, BLUE, PAPER = '#233c43', '#5188b4', '#f6f5ef'


def turn(points):
    return frozenset((-y, x) for x, y in points)


def key(value, orientation):
    """Connected equal-area directional profile, in integer square voxels."""
    if value not in (0, 1):
        raise ValueError('Only definite 0/1 keys are used.')
    head = {(x, y) for x, y in product(range(-1, 2), repeat=2)}
    tail = {(x, y) for x, y in product(range(-3, 0), repeat=2)}
    tab = {(2, 0), (2, 1)} if value == 0 else {(0, 2), (1, 2)}
    profile = frozenset(head | tail | tab)
    for _ in range(orientation % 4):
        profile = turn(profile)
    return profile


def place(profile, x, y):
    return frozenset((px + x, py + y) for px, py in profile)


def blue_inputs(bits, turns=0, origin=(0, 0)):
    result = []
    for value, (x, y), orientation in zip(bits, ANCHORS, OUTWARD):
        profile = place(key(value, orientation), x, y)
        for _ in range(turns % 4):
            profile = frozenset((SIZE - py, px) for px, py in profile)
        result.append(place(profile, *origin))
    return tuple(result)


def life_outputs(value, origin=(0, 0)):
    return tuple(place(key(value, direction + 2), origin[0] + x, origin[1] + y)
                 for (x, y), direction in zip(ANCHORS, OUTWARD))


def rotate_face(face):
    return tuple(tuple(row) for row in zip(*face[::-1]))


def representative(face):
    faces = []
    for _ in range(4):
        faces.append(face)
        face = rotate_face(face)
    return min(faces)


def copied(face):
    return tuple(tuple(face[r % 2][c % 2] for c in range(4)) for r in range(4))


def verify():
    profiles = {key(bit, angle) for bit, angle in product(range(2), range(4))}
    assert len(profiles) == 8
    assert {len(profile) for profile in profiles} == {19}
    for a, b in product(profiles, repeat=2):
        assert (a <= b) == (a == b), 'A wrong plug hides in a recess'
    # Give every lower anchor BOTH possible values. A wrong location is thus
    # rejected by geometry irrespective of which Life bits happen to be below.
    available = set()
    for cx, cy, bit in product(range(2), range(2), range(2)):
        available.update(life_outputs(bit, (cx * SIZE, cy * SIZE)))
    placements, valid = 0, Counter()
    for bits, angle in product(product((0, 1), repeat=4), range(4)):
        for dx, dy in product(range(SIZE), repeat=2):
            sockets = blue_inputs(bits, angle, (dx, dy))
            fits = all(socket in available for socket in sockets)
            assert fits == ((dx, dy) == (16, 16)), (bits, angle, dx, dy)
            if fits:
                valid[(dx, dy)] += 1
            placements += 1
    classes = Counter(representative((bits[:2], bits[2:]))
                      for bits in product((0, 1), repeat=4))
    assert len(classes) == 6
    for bits, angle in product(product((0, 1), repeat=4), range(4)):
        face = (bits[:2], bits[2:])
        spun = face
        for _ in range(angle):
            spun = rotate_face(spun)
        assert set(blue_inputs(bits, angle)) == set(blue_inputs(sum(spun, ())))
        output = copied(face)
        for _ in range(angle):
            output = rotate_face(output)
        assert output == copied(spun)
    return {'status': 'All ideal geometry checks passed.',
            'placement_checks': placements,
            'valid_offsets_modulo_32': [list(point) for point in valid],
            'profiles': 8, 'voxels_per_profile': 19,
            'blue_types_up_to_rotation': len(classes),
            'scope': 'New directional-key proposal; exact profiles, integer offsets, quarter-turns. Not print-ready CAD.'}


class Svg:
    def __init__(self, width, height, title):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
                      f'viewBox="0 0 {width} {height}" role="img"><title>{escape(title)}</title>',
                      '<style>text{font-family:DejaVu Sans,Arial,sans-serif}</style>',
                      f'<rect width="100%" height="100%" fill="{PAPER}"/>']

    def text(self, x, y, value, size=16, bold=False, color=INK):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" '
                          f'font-weight="{"bold" if bold else "normal"}" fill="{color}">{escape(str(value))}</text>')

    def rect(self, x, y, w, h, fill='none', stroke='#c9d3cf', dashed=False, sw=1):
        dash = ' stroke-dasharray="8 5"' if dashed else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                          f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')

    def line(self, x1, y1, x2, y2, color=INK, sw=2):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="{color}" stroke-width="{sw}"/>')

    def arrow(self, x1, y, x2):
        self.line(x1, y, x2, y)
        self.line(x2 - 9, y - 5, x2, y)
        self.line(x2 - 9, y + 5, x2, y)

    def grid(self, x, y, values, cell=36):
        for r, row in enumerate(values):
            for c, value in enumerate(row):
                self.rect(x + c * cell, y + r * cell, cell, cell, '#fffefa')
                self.text(x + c * cell + cell * .37, y + r * cell + cell * .67,
                          value, int(cell * .49), True)

    def profile(self, x, y, cells, scale, color):
        for px, py in cells:
            self.rect(x + (px - .5) * scale, y + (py - .5) * scale, scale, scale, color, color)

    def save(self, path):
        path.write_text('\n'.join(self.parts + ['</svg>']), encoding='utf8')


def faces_diagram(out):
    svg = Svg(1320, 1030, 'Blue tiles: four independent inputs and sixteen copied outputs')
    svg.text(32, 43, 'Blue tiles: input, output, and why there are six', 28, True)
    svg.text(32, 78, 'One Life cell = one bit. Four repeated corner keys carry the SAME bit; they are not four independent states.', 16)
    svg.text(40, 122, 'One Life cell: value S', 19, True)
    svg.rect(40, 141, 175, 175, '#fffefa', INK)
    svg.grid(67, 168, (('S', 'S'), ('S', 'S')), 60)
    svg.text(40, 347, 'Four outputs, all S', 15)
    svg.text(294, 122, 'Blue bottom: 2x2 inputs', 19, True)
    svg.rect(294, 141, 175, 175, '#ecf1f4', BLUE)
    svg.grid(321, 168, (('A', 'B'), ('C', 'D')), 60)
    svg.text(294, 347, 'A, B, C, D: four different cells', 14)
    svg.arrow(492, 226, 555)
    svg.text(579, 122, 'Blue top: 4x4 copies', 19, True)
    svg.grid(579, 141, copied((('A', 'B'), ('C', 'D'))), 44)
    svg.line(667, 141, 667, 317, BLUE, 3)
    svg.line(579, 229, 755, 229, BLUE, 3)
    svg.text(579, 347, 'Each quadrant has all four values', 14)
    svg.text(824, 160, 'The same 4x4 physical footprint', 17, True)
    svg.text(824, 192, 'BOTTOM: four quarter-centre inputs.', 15)
    svg.text(824, 222, 'TOP: sixteen finer output positions.', 15)
    svg.text(824, 260, 'Input 2x2 -> output 4x4 means', 15)
    svg.text(824, 286, 'connector layout, not a larger body.', 15)
    svg.text(32, 397, 'Six blue types: both faces rotate together', 22, True)
    classes = Counter(representative((bits[:2], bits[2:])) for bits in product((0, 1), repeat=4))
    names = ('All zero', 'One live', 'Two adjacent', 'Two diagonal', 'Three live', 'All live')
    for i, ((face, count), name) in enumerate(zip(sorted(classes.items()), names)):
        x, y = 40 + (i % 3) * 426, 438 + (i // 3) * 248
        svg.text(x, y, name, 19, True)
        svg.grid(x, y + 26, face, 36)
        svg.arrow(x + 91, y + 62, x + 134)
        svg.grid(x + 156, y + 8, copied(face), 30)
        svg.text(x, y + 158, f'{count} orientation(s) among the 16 inputs', 14)
    svg.text(32, 968, 'Source: six 4x4 blue types and neighbourhood copying. Sparse bottom keys are a proposed geometric realization.', 14)
    svg.text(32, 995, 'Plan views use the SAME global coordinates for both faces; do not mirror the bottom labels as if viewing from below.', 14)
    svg.save(out / '01_blue_input_output.svg')


def geometry_diagram(out):
    svg = Svg(1380, 1190, 'Directional keys enforce blue tile placement at four-cell corners')
    svg.text(32, 43, 'Corner-only seating: directional keys independent of the bit', 27, True)
    svg.text(32, 77, 'NEW PROPOSAL: each Life cell has four inward tails; the blue underside expects four outward tails.', 16)
    svg.text(35, 119, 'One Life cell: its four 0 keys', 18, True)
    svg.rect(35, 139, 256, 256, '#fffefa', INK)
    for cells in life_outputs(0):
        svg.profile(35, 139, cells, 8, BLUE)
    svg.text(343, 119, 'Blue underside: outward tails', 18, True)
    svg.rect(343, 139, 256, 256, '#fffefa', INK)
    for cells in blue_inputs((0, 0, 0, 0)):
        svg.profile(343, 139, cells, 8, '#d7a15c')
    svg.text(649, 139, 'Prototype 0 and 1 profiles, same NW tail', 18, True)
    for x, bit in ((713, 0), (873, 1)):
        svg.profile(x, 223, key(bit, 0), 17, BLUE)
        svg.text(x - 23, 300, f'Bit {bit}', 17, True)
    svg.text(1016, 168, 'The tail encodes orientation.', 15)
    svg.text(1016, 199, 'A separate tab encodes 0/1.', 15)
    svg.text(649, 340, 'Equal area, distinct profiles: wrong value or direction causes a collision.', 15)
    svg.text(649, 370, 'Underside recess = exact matching profile. No wildcard cavity.', 15)
    svg.text(32, 443, 'Test using ALL-ZERO cells: placement must work without help from the data', 20, True)
    for col, (offset, title, accepted) in enumerate((((16, 16), 'CORNER: fits', True),
                                                  ((16, 0), 'EDGE: blocked', False),
                                                  ((0, 0), 'CELL CENTRE: blocked', False))):
        x, y, scale = 40 + col * 452, 491, 5.5
        svg.text(x, y - 14, title, 19, True, '#286959' if accepted else '#9e5549')
        for r, c in product(range(2), repeat=2):
            svg.rect(x + c * SIZE * scale, y + r * SIZE * scale,
                     SIZE * scale, SIZE * scale, '#fffefa', '#8ba09c')
            for cells in life_outputs(0, (c * SIZE, r * SIZE)):
                svg.profile(x, y, cells, scale, '#94b7ca')
        # Expected cavity outlines, offset from lower plugs so mismatch is visible.
        sockets = blue_inputs((0, 0, 0, 0), origin=offset)
        for cells in sockets:
            for px, py in cells:
                svg.rect(x + (px - .5) * scale, y + (py - .5) * scale,
                         scale, scale, 'none', '#b46738', sw=1.5)
        svg.rect(x + offset[0] * scale, y + offset[1] * scale,
                 SIZE * scale, SIZE * scale, 'none', '#286959' if accepted else '#ac5349', True, 3)
        svg.text(x, 868, 'Solid blue = lower plugs; orange outline = expected recesses.', 11)
    svg.text(32, 913, 'WHY THIS PRESERVES THE SIX-TILE REDUCTION', 17, True)
    svg.text(32, 944, 'The outward pattern rotates into itself. Rotating the whole tile moves values and key directions together.', 16)
    svg.text(32, 978, 'Value regions alone cannot enforce the offset: a uniform field would admit the wrong placement.', 16)
    svg.text(32, 1027, 'Verified: 65,536 candidate placements; only (16,16) modulo the 32-unit Life-cell pitch seats correctly.', 17, True)
    svg.text(32, 1060, 'Includes every 0/1 input combination, all four quarter-turns, and every integer horizontal/vertical offset.', 15)
    svg.text(32, 1114, 'Ideal extrusion proposal, not print-ready CAD. Smooth droplets, tolerances, body alignment and attachment remain to be designed.', 14)
    svg.text(32, 1148, 'Profiles shown here are exact voxel shapes. The TOP 4x4 outputs need the appropriate keys for the next layer, designed separately.', 14)
    svg.save(out / '02_corner_only_geometry.svg')


if __name__ == '__main__':
    report = verify()
    output = Path(__file__).parent / 'blue-schematics'
    output.mkdir(parents=True, exist_ok=True)
    faces_diagram(output)
    geometry_diagram(output)
    (output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    print(json.dumps(report, indent=2))
    print(f'Schematics: {output}')
