#!/usr/bin/env python3
"""Executable study of Michael Simkin's March 13, 2019 computational Life tiles.

Run with Python 3.10+; no third-party packages are required:
    python cgol_computational_tiles.py
    python cgol_computational_tiles.py --pattern '010/110/001' --out /tmp/life-tiles
    python cgol_computational_tiles.py --check-only

Source: https://conwaylife.com/forums/viewtopic.php?p=73033#p73033
Earlier diagrams: https://conwaylife.com/forums/viewtopic.php?p=73018#p73018

This models the computational tiles, not the later construction-piece CAD.
Orange's three stated examples and all eight purple masks are transcribed into
executable constraints. Blue's routing is reconstructed as a 4x4 neighbourhood
with the central row/column duplicated. Orange keeps the centre on a separate
port and compacts the other three bits in unary. The second pass is perpendicular.
The interior is turned 180 degrees to use the post's bottom/right-packed masks.

Schematics show logical ports, not manufacturing geometry. The four black/white
cases are a logical normal form of B3/S23, not a recovered notch-shape catalogue.
X is a logical mask only. Michael's current full-fit requirement cannot be
implemented by a union cavity: it would leave unused space. The 26 logical
families have not been realized or verified as full-fit physical tile shapes.
The program checks every intermediate constraint for all 512 neighbourhoods.
It also checks all 20 compressed interiors against the masks independently.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from html import escape
from itertools import product
import json
from pathlib import Path

Grid = tuple[tuple[int, ...], ...]
Mask = tuple[str, str, str]
BLUE = '#5188b4'
ORANGE = '#d7a15c'
PURPLE = '#ac88be'
INK = '#233c43'
PAPER = '#f6f5ef'


def rotate(grid):
    """A clockwise quarter-turn, also usable on masks of 0/1/X symbols."""
    size = len(grid)
    return tuple(tuple(grid[size - 1 - c][r] for c in range(size)) for r in range(size))


def all_rotations(grid):
    for _ in range(4):
        yield grid
        grid = rotate(grid)


def canonical_rotation(grid):
    return min(all_rotations(grid))


def blue_catalogue() -> tuple[Grid, ...]:
    """Six rotational classes of the sixteen 2x2 binary input configurations."""
    return tuple(sorted({
        canonical_rotation((bits[:2], bits[2:])) for bits in product((0, 1), repeat=4)
    }))


def blue_tile(face: Grid) -> Grid:
    """Copy the four input states into each of the four 2x2 output quadrants.

    A B -> A B A B     Each adjacent Life square receives all four states in
    C D    C D C D     its local quadrant, rather than just its own state.
           A B A B
           C D C D
    """
    if len(face) != 2 or any(len(row) != 2 for row in face):
        raise ValueError('A blue tile has four inputs arranged as a 2x2 face.')
    if any(bit not in (0, 1) for row in face for bit in row):
        raise ValueError('Blue inputs must be bits.')
    return tuple(tuple(face[r % 2][c % 2] for c in range(4)) for r in range(4))


def blue_gather(neighbourhood: Grid) -> Grid:
    """Logical routing: expand 3x3 to 4x4 by duplicating its middle row/column.

    NW N N NE    This makes each orange input x,y,y,z. Four blue input patterns
    W  C C E     are the overlapping 2x2 quadrants around the target cell.
    W  C C E     Physical coordinates/connector profiles are not specified here.
    SW S S SE
    """
    validate_neighbourhood(neighbourhood)
    result = [[0] * 4 for _ in range(4)]
    for block_row, block_col in product(range(2), repeat=2):
        face = tuple(tuple(neighbourhood[block_row+r][block_col+c]
                           for c in range(2)) for r in range(2))
        copied = blue_tile(face)
        # Select the quadrant adjoining the target centre cell.
        source_row, source_col = (1-block_row)*2, (1-block_col)*2
        for r, c in product(range(2), repeat=2):
            result[block_row*2+r][block_col*2+c] = copied[source_row+r][source_col+c]
    return tuple(tuple(row) for row in result)


def unary(count: int) -> tuple[int, int, int]:
    if count not in range(4):
        raise ValueError('An orange output has three unary slots.')
    return tuple(int(i < count) for i in range(3))


@dataclass(frozen=True)
class OrangePorts:
    compacted: tuple[int, int, int]
    centre: int

    def face(self):
        return (*self.compacted, f'C{self.centre}')


def orange(x: int, y: int, duplicate_y: int, z: int) -> OrangePorts:
    """(x,y,y,z) -> (unary(x+y+z), C_y), matching the post's examples.

    The two y inputs must agree. The separate centre port carries the other copy.
    This is unary packing, not a binary adder. Input-position distinctions still
    give eight tile cases, even when two cases have the same output face.
    """
    if any(bit not in (0, 1) for bit in (x, y, duplicate_y, z)):
        raise ValueError('Orange inputs must be bits.')
    if y != duplicate_y:
        raise ValueError('The repeated centre inputs disagree: this tile cannot fit.')
    return OrangePorts(unary(x + y + z), y)


def orange_rows(gathered: Grid) -> tuple[OrangePorts, ...]:
    if len(gathered) != 4 or any(len(row) != 4 for row in gathered):
        raise ValueError('The first orange layer expects a 4x4 gathered face.')
    return tuple(orange(*row) for row in gathered)


def orange_columns(rows: tuple[OrangePorts, ...]) -> tuple[OrangePorts, ...]:
    """Apply the same tile at 90 degrees to the three unary columns.

    The fourth column is already the C line, so it is not summed a second time.
    The repeated middle rows make the two middle inputs of each column equal.
    """
    return tuple(orange(*(row.compacted[c] for row in rows)) for c in range(3))


def packed_interior(columns: tuple[OrangePorts, ...]) -> Grid:
    raw = tuple(tuple(columns[c].compacted[r] for c in range(3)) for r in range(3))
    return rotate(rotate(raw))


def is_packed(grid: Grid) -> bool:
    """Both axes are nondecreasing: all 1s are pushed toward bottom/right."""
    return (
        len(grid) == 3 and all(len(row) == 3 for row in grid)
        and all(bit in (0, 1) for row in grid for bit in row)
        and all(grid[r][c] <= grid[r][c + 1] for r in range(3) for c in range(2))
        and all(grid[r][c] <= grid[r + 1][c] for r in range(2) for c in range(3))
    )


@dataclass(frozen=True)
class PurpleTile:
    name: str
    category: str
    mask: Mask


# These are the eight connector patterns in the post's final reduction.
PURPLE_TILES = (
    PurpleTile('P0', '0–2', ('X00', 'X00', '0XX')),
    PurpleTile('P3a', '3', ('000', '000', '111')),
    PurpleTile('P3b', '3', ('000', '001', '011')),
    PurpleTile('P4a', '4', ('001', '001', '011')),
    PurpleTile('P4b', '4', ('000', '001', '111')),
    PurpleTile('P4c', '4', ('000', '011', '011')),
    PurpleTile('P5a', '5–9', ('XX1', 'XX1', '111')),
    PurpleTile('P5b', '5–9', ('XX1', 'X11', 'XX1')),
)


def mask_fits(mask, bits: Grid) -> bool:
    return all(mask[r][c] == 'X' or int(mask[r][c]) == bits[r][c]
               for r in range(3) for c in range(3))


def purple_matches(interior: Grid):
    if not is_packed(interior):
        raise ValueError('Purple expects the compressed face produced by the orange layers.')
    matches = []
    for tile in PURPLE_TILES:
        for quarter_turns, mask in enumerate(all_rotations(tuple(tuple(r) for r in tile.mask))):
            if mask_fits(mask, interior):
                matches.append((tile, quarter_turns, mask))
    categories = {tile.category for tile, _, _ in matches}
    if len(categories) != 1:
        raise ValueError(f'Missing or conflicting purple constraints: {categories}')
    return tuple(matches)


# Four logical B/W cases. Exact physical connector shapes need separate modelling.
BW_CASES = (('3', 'X', 1), ('4', '0', 0), ('4', '1', 1), ('other', 'X', 0))


def black_white(category: str, centre: int) -> int:
    if centre not in (0, 1) or category not in {'0–2', '3', '4', '5–9'}:
        raise ValueError('Invalid final-layer ports.')
    normalized = category if category in {'3', '4'} else 'other'
    outputs = {output for kind, c, output in BW_CASES
               if kind == normalized and (c == 'X' or int(c) == centre)}
    if len(outputs) != 1:
        raise ValueError('Final-layer constraint is not determined.')
    return outputs.pop()


def validate_neighbourhood(grid: Grid):
    if len(grid) != 3 or any(len(row) != 3 for row in grid):
        raise ValueError('Supply a 3x3 neighbourhood.')
    if any(bit not in (0, 1) for row in grid for bit in row):
        raise ValueError('Neighbourhood states must be zero or one.')


def reference_life(grid: Grid) -> int:
    """Independent B3/S23 oracle: count only the eight neighbours."""
    neighbours = sum(grid[r][c] for r in range(3) for c in range(3) if (r, c) != (1, 1))
    return int(neighbours == 3 or (grid[1][1] == 1 and neighbours == 2))


@dataclass(frozen=True)
class Trace:
    input: Grid
    blue: Grid
    rows: tuple[OrangePorts, ...]
    columns: tuple[OrangePorts, ...]
    interior: Grid
    category: str
    matches: tuple
    centre: int
    output: int


def compute(neighbourhood: Grid) -> Trace:
    blue = blue_gather(neighbourhood)
    rows = orange_rows(blue)
    columns = orange_columns(rows)
    interior = packed_interior(columns)
    matches = purple_matches(interior)
    # The real centre is carried by the C ports of the duplicated middle rows.
    if rows[1].centre != rows[2].centre:
        raise ValueError('The duplicated centre ports disagree.')
    centre = rows[1].centre
    category = matches[0][0].category
    return Trace(neighbourhood, blue, rows, columns, interior, category, matches,
                 centre, black_white(category, centre))


def verify() -> dict:
    """Check actual tile constraints, packing invariants and an independent rule."""
    assert len(blue_catalogue()) == 6
    for bits in product((0, 1), repeat=4):
        face = (bits[:2], bits[2:])
        assert blue_tile(rotate(face)) == rotate(blue_tile(face))
        assert sum(map(sum, blue_tile(face))) == 4 * sum(bits)
    stated_examples = (
        ((0, 1, 1, 0), (1, 0, 0), 1),
        ((0, 0, 0, 1), (1, 0, 0), 0),
        ((1, 1, 1, 0), (1, 1, 0), 1),
    )
    for inputs, packed, centre in stated_examples:
        assert orange(*inputs) == OrangePorts(packed, centre)
    for x, y, z in product((0, 1), repeat=3):
        ports = orange(x, y, y, z)
        assert sum(ports.compacted) + ports.centre == x + 2*y + z
    try:
        orange(0, 0, 1, 0)
    except ValueError:
        pass
    else:
        raise AssertionError('Mismatched duplicated inputs were accepted.')
    interiors, categories, outputs = set(), Counter(), Counter()
    for bits in product((0, 1), repeat=9):
        grid = tuple(bits[i:i+3] for i in (0, 3, 6))
        trace = compute(grid)
        indices = (0, 1, 1, 2)
        assert trace.blue == tuple(tuple(grid[r][c] for c in indices) for r in indices)
        assert sum(map(sum, trace.interior)) == sum(bits)
        assert trace.centre == grid[1][1]
        assert trace.output == reference_life(grid), f'Incorrect Life output: {grid}'
        for rotated in all_rotations(grid):
            assert compute(rotated).output == trace.output
        interiors.add(trace.interior)
        categories[trace.category] += 1
        outputs[trace.output] += 1
    all_packed = set()
    for bits in product((0, 1), repeat=9):
        grid = tuple(bits[i:i+3] for i in (0, 3, 6))
        if is_packed(grid):
            all_packed.add(grid)
            m = sum(bits)
            expected = '0–2' if m <= 2 else str(m) if m in (3, 4) else '5–9'
            assert {tile.category for tile, _, _ in purple_matches(grid)} == {expected}
    assert interiors == all_packed and len(interiors) == 20
    assert categories == {'0–2': 46, '3': 84, '4': 126, '5–9': 256}
    assert outputs == {0: 372, 1: 140}
    return {
        'neighbourhoods_checked': 512,
        'packed_interiors_checked': len(interiors),
        'orange_post_examples_checked': len(stated_examples),
        'families': {'blue_rotational_classes': 6, 'orange_input_cases': 8,
                     'purple_masks': 8, 'black_white_logical_cases': 4},
        'purple_categories': dict(categories),
        'life_outputs': dict(outputs),
        'result': 'All logical checks passed.',
        'scope': 'Reconstructed routing and logical ports; not a physical-fit/CAD proof.',
        'source': 'https://conwaylife.com/forums/viewtopic.php?p=73033#p73033',
    }


class Svg:
    def __init__(self, width: int, height: int):
        self.items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
                      f'height="{height}" viewBox="0 0 {width} {height}" role="img">',
                      '<style>text{font-family:DejaVu Sans,Arial,sans-serif}</style>',
                      f'<rect width="100%" height="100%" fill="{PAPER}"/>']

    def text(self, x, y, value, size=16, color=INK, weight='normal', anchor='start'):
        self.items.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
                          f'font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    def rect(self, x, y, width, height, fill='white', stroke='#ccd3ce', radius=3):
        self.items.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
                          f'rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def line(self, x1, y1, x2, y2, color=INK, dashed=False):
        dash = ' stroke-dasharray="5 5"' if dashed else ''
        self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                          f'stroke="{color}" stroke-width="2"{dash}/>')

    def arrow(self, x1, y, x2, color=INK):
        self.line(x1, y, x2, y, color)
        self.polygon(((x2, y), (x2-8, y-4), (x2-8, y+4)), color, color)

    def polygon(self, points, fill, stroke='#62747c'):
        joined = ' '.join(f'{x:.2f},{y:.2f}' for x, y in points)
        self.items.append(f'<polygon points="{joined}" fill="{fill}" stroke="{stroke}"/>')

    def grid(self, x, y, values, color, cell=34, centre=None):
        for r, row in enumerate(values):
            for c, value in enumerate(row):
                is_flag = isinstance(value, str) and value.startswith('C')
                fill = color if value in (1, '1') else '#e4e9e4' if value == 'X' else '#fffefa'
                self.rect(x+c*cell, y+r*cell, cell-3, cell-3, fill,
                          '#315d5e' if is_flag else '#ccd3ce')
                self.text(x+c*cell+(cell-3)/2, y+r*cell+cell*.64, value,
                          size=cell*.43, color='white' if value in (1, '1') else INK,
                          anchor='middle', weight='bold' if is_flag else 'normal')
                if centre == (r, c):
                    self.rect(x+c*cell-2, y+r*cell-2, cell+1, cell+1,
                              fill='none', stroke='#213e42', radius=2)

    def save(self, path: Path):
        path.write_text('\n'.join(self.items + ['</svg>']), encoding='utf8')


def draw_pipeline(trace: Trace, output: Path):
    svg = Svg(1380, 580)
    svg.text(35, 48, 'Computational Life tiles · follow one neighbourhood', 28, weight='bold')
    svg.text(35, 80, 'Two unary packing passes, then connector constraints. C ports carry a state; they are not counted again.', 16)
    panels = (
        ('Input', trace.input, BLUE, 'Centre outlined'),
        ('Blue routing', trace.blue, BLUE, 'Middle row/column duplicated'),
        ('Orange: rows', tuple(p.face() for p in trace.rows), ORANGE, 'Three unary bits + C per row'),
        ('Orange: columns', trace.interior, ORANGE, 'Packed nine-cell total'),
    )
    for i, (title, grid, color, note) in enumerate(panels):
        x = 35 + i*235
        svg.text(x, 128, title, 19, weight='bold')
        svg.grid(x, 150, grid, color, cell=39, centre=(1, 1) if i == 0 else None)
        svg.text(x, 335, note, 12)
        svg.arrow(x+191, 230, x+224)
    svg.text(780, 311, f'Real centre: C{trace.centre}', 16, weight='bold')
    tile, turns, mask = trace.matches[0]
    svg.text(990, 128, 'Purple constraint', 19, weight='bold')
    svg.grid(990, 150, mask, PURPLE, cell=39)
    svg.text(990, 303, f'{tile.name} · {turns*90}° rotation', 14)
    svg.text(990, 335, f'Category: {trace.category}', 16, weight='bold')
    svg.arrow(1168, 230, 1193)
    svg.text(1205, 128, 'B/W', 19, weight='bold')
    svg.grid(1205, 172, ((trace.output,),), INK, cell=80)
    svg.text(1205, 280, 'Next state', 15)
    svg.text(35, 405, 'Orange function', 20, weight='bold')
    svg.text(35, 436, '(x, y, y, z) -> (unary(x + y + z), C_y)', 20)
    svg.text(35, 469, 'Second pass: use the same function at 90°. Leave the C line out of the summation.', 16)
    svg.text(35, 507, 'X is a logical mask; its FULL-FIT geometry is unresolved. The final layer combines the category with C.', 16)
    svg.text(35, 548, 'Logical schematic: routing reconstructed from the text; manufactured tile bodies and notch shapes are not shown.', 13, '#657477')
    svg.save(output / '01_pipeline.svg')


def draw_catalogue(output: Path):
    svg = Svg(1400, 1120)
    svg.text(35, 45, 'Computational tile catalogue · 6 + 8 + 8 + 4', 28, weight='bold')
    svg.text(35, 76, 'Logical input/output faces. Rotations identify blue types; purple patterns are the eight masks from the post.', 16)
    svg.text(35, 119, 'BLUE · six types: input and copied output face', 20, BLUE, 'bold')
    for i, grid in enumerate(blue_catalogue()):
        x = 40+i*205
        svg.grid(x, 164, grid, BLUE, 24)
        svg.arrow(x+57, 185, x+79)
        svg.grid(x+88, 140, blue_tile(grid), BLUE, 24)
        svg.text(x, 253, f'B{i} · {sum(map(sum, grid))} live inputs', 13)
    svg.text(35, 287, 'ORANGE · eight directed input cases', 20, ORANGE, 'bold')
    for i, (x, y, z) in enumerate(product((0, 1), repeat=3)):
        px = 40+(i % 4)*330
        py = 315+(i // 4)*123
        ports = orange(x, y, y, z)
        svg.text(px, py, f'O{i}: {x} {y} {y} {z} ->', 15, weight='bold')
        svg.grid(px, py+15, (ports.face(),), ORANGE, 42)
    svg.text(35, 574, 'PURPLE · eight masks, each usable in four rotations', 20, PURPLE, 'bold')
    for i, tile in enumerate(PURPLE_TILES):
        px, py = 40+(i % 4)*330, 615+(i // 4)*163
        svg.text(px, py, f'{tile.name} · total {tile.category}', 16, weight='bold')
        svg.grid(px, py+14, tile.mask, PURPLE, 38)
    svg.text(35, 969, 'BLACK / WHITE · four logical cases', 20, weight='bold')
    for i, (category, centre, value) in enumerate(BW_CASES):
        x = 40+i*330
        svg.rect(x, 993, 292, 54, INK if value else '#fffefa')
        svg.text(x+14, 1026, f'total {category}; C={centre} -> {value}', 16,
                 color='white' if value else INK)
    svg.text(35, 1088, 'B/W is a logical normal form. X ignores a bit logically; FULL-FIT physical geometry is not established.', 13, '#657477')
    svg.save(output / '02_catalogue.svg')


def draw_exploded(trace: Trace, output: Path):
    svg = Svg(1100, 980)
    svg.text(35, 46, 'Five computational layers · exploded logical schematic', 27, weight='bold')
    svg.text(35, 79, 'The second orange pass is perpendicular to the first. The original centre travels separately to the rule layer.', 14)
    tile, turns, mask = trace.matches[0]
    stages = (
        ('1  Blue: gather', trace.blue, BLUE),
        ('2  Orange: pack rows', tuple(p.face() for p in trace.rows), ORANGE),
        ('3  Orange: pack columns (90°)', trace.interior, ORANGE),
        (f'4  Purple: {tile.name}, category {trace.category}', mask, PURPLE),
        (f'5  Black/white: next state {trace.output}', ((trace.output,),), INK),
    )
    for layer, (title, grid, color) in enumerate(stages):
        origin_x, origin_y = 220, 835-layer*157
        rows, cols = len(grid), len(grid[0])
        dx, dy = 310/cols, 200/rows
        def point(c, r):
            return origin_x+c*dx+r*dy*.65, origin_y+r*dy*.32-c*dx*.16
        svg.polygon((point(0, 0), point(cols, 0), point(cols, rows), point(0, rows)), '#edf0ea')
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                points = (point(c, r), point(c+1, r), point(c+1, r+1), point(c, r+1))
                fill = color if value in (1, '1') else '#d6dcd6' if value == 'X' else '#fffefa'
                svg.polygon(points, fill)
                tx, ty = point(c+.5, r+.5)
                svg.text(tx, ty+5, value, 17, 'white' if value in (1, '1') else INK, anchor='middle')
        svg.text(700, origin_y+15, title, 17, weight='bold')
        if layer in (1, 2):
            svg.text(700, origin_y+43, 'C ports are separate state channels', 13)
    svg.line(670, 714, 670, 222, ORANGE, dashed=True)
    svg.text(688, 469, f'C{trace.centre}', 18, ORANGE, 'bold')
    svg.text(35, 944, 'Planes illustrate computation and channel flow. They are not CAD of the actual interlocking piece shapes.', 14, '#657477')
    svg.save(output / '03_exploded_layers.svg')


def parse_pattern(value: str) -> Grid:
    rows = value.split('/')
    if len(rows) != 3 or any(len(row) != 3 or set(row)-{'0', '1'} for row in rows):
        raise argparse.ArgumentTypeError('Use three binary rows, e.g. 010/110/001.')
    return tuple(tuple(int(bit) for bit in row) for row in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--pattern', type=parse_pattern, default=parse_pattern('010/110/001'))
    parser.add_argument('--out', type=Path, default=Path(__file__).resolve().parent / 'computational-schematics')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    report = verify()
    print(f"PASS: {report['neighbourhoods_checked']} neighbourhoods, "
          f"{report['packed_interiors_checked']} packed interiors, all eight purple masks.")
    if args.check_only:
        return
    trace = compute(args.pattern)
    args.out.mkdir(parents=True, exist_ok=True)
    draw_pipeline(trace, args.out)
    draw_catalogue(args.out)
    draw_exploded(trace, args.out)
    report['example'] = {
        'input': trace.input, 'blue_gathered': trace.blue,
        'orange_rows': [p.face() for p in trace.rows],
        'orange_columns': [p.face() for p in trace.columns],
        'packed_interior': trace.interior, 'carried_centre': trace.centre,
        'purple_category': trace.category,
        'matching_purple_tiles': [{'name': t.name, 'rotation': r*90} for t, r, _ in trace.matches],
        'next_cell': trace.output,
    }
    (args.out / 'verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf8')
    print(f'Example: m={sum(map(sum, trace.input))}, C={trace.centre}, next={trace.output}')
    print(f'Wrote three SVG schematics and verification.json to {args.out}')


if __name__ == '__main__':
    main()
