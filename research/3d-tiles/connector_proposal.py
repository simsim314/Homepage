#!/usr/bin/env python3
"""New connector proposal for the computational Life tile study.

Standalone, standard-library-only: python connector_proposal.py

The union-cavity wildcard proposal has been REJECTED by Michael: require
FULL FIT, not merely no collision. This script now demonstrates the failure.
This is NOT a recovered 2019 connector design, nor print-ready CAD. It tests
ideal aligned square-cell cross-sections extruded vertically. An output plug
on a tile's TOP fully fits an input cavity on the next tile's BOTTOM exactly
when their occupied/cavity regions are equal, at equal extrusion depth.
This is nominal geometry; print clearance is not a logical wildcard.
Tile registration is assumed, not established here.

The proposed ordinary plugs are a plus and a diagonal cross. A wildcard
socket was their union: it admits either plug but leaves gaps, so FAILS
the full-fit requirement. Centre-state plugs use a square collar and a smaller
internal plus/cross, with an empty moat separating the two. All profiles
are invariant under quarter-turns. The moat prevents ordinary bit plugs
from accidentally fitting centre sockets; the collar prevents the reverse.

Checks cover every family/value pairing in all four registered rotations.
They do not prove the geometry of entire tiles, arbitrary displacement or
angle, tolerances, mechanical strength, or suitability for 3D printing.
"""

from __future__ import annotations

import argparse
from html import escape
from itertools import product
import json
from pathlib import Path

Profile = frozenset[tuple[int, int]]


def cross(diagonal: bool, radius: int) -> Profile:
    return frozenset(
        {(i, i) for i in range(-radius, radius + 1)}
        | {(i, -i) for i in range(-radius, radius + 1)}
        if diagonal else
        {(i, 0) for i in range(-radius, radius + 1)}
        | {(0, i) for i in range(-radius, radius + 1)}
    )


def collar(radius: int) -> Profile:
    return frozenset((x, y) for x, y in product(range(-radius, radius + 1), repeat=2)
                     if max(abs(x), abs(y)) == radius)


def plug(value: int, centre: bool = False) -> Profile:
    if value not in (0, 1):
        raise ValueError('A plug must output 0 or 1.')
    return cross(bool(value), 1) | collar(3) if centre else cross(bool(value), 2)


def socket(value: int | None, centre: bool = False) -> Profile:
    """None means wildcard: a cavity accepting either value of this family."""
    return plug(0, centre) | plug(1, centre) if value is None else plug(value, centre)


def rotate(profile: Profile) -> Profile:
    return frozenset((-y, x) for x, y in profile)


def fits(output: Profile, underside_cavity: Profile) -> bool:
    """Full fit at equal extrusion depth: no collision AND no unused cavity."""
    return output == underside_cavity


def unused_cavity(output: Profile, underside_cavity: Profile) -> Profile:
    return underside_cavity - output


PLUGS = {name: plug(value, centre) for centre in (False, True)
         for value in (0, 1) for name in [f'C{value}' if centre else str(value)]}
SOCKETS = {name: socket(value, centre) for centre in (False, True)
           for value in (0, 1, None)
           for name in [('C' if centre else '') + ('*' if value is None else str(value))]}


def verify() -> dict:
    rows = {}
    checked = 0
    for name, original in PLUGS.items():
        rows[name] = {}
        profile = original
        for quarter_turn in range(4):
            assert profile == original, (name, quarter_turn, 'Rotation changed a value')
            for input_name, cavity in SOCKETS.items():
                expected = name == input_name
                actual = fits(profile, cavity)
                assert actual == expected, (name, input_name, quarter_turn)
                rows[name][input_name] = actual
                checked += 1
            profile = rotate(profile)
    rejected_wildcards = {}
    for name, profile in PLUGS.items():
        wildcard_name = 'C*' if name.startswith('C') else '*'
        cavity = SOCKETS[wildcard_name]
        assert profile <= cavity  # Old non-collision test incorrectly accepted it.
        assert unused_cavity(profile, cavity)
        assert not fits(profile, cavity)
        rejected_wildcards[name] = len(unused_cavity(profile, cavity))
    return {'pairings_checked_including_rotations': checked,
            'fit_matrix': rows,
            'rejected_union_cavities_unused_cells': rejected_wildcards,
            'result': 'Full-fit checks passed. Every union-cavity wildcard is rejected.',
            'scope': 'Nominal registered extrusions at equal depth; not full tile CAD. Previous wildcard proposal rejected.'}


def draw(path: Path, report: dict) -> None:
    items = ['<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="900" '
             'viewBox="0 0 1180 900" role="img">',
             '<title>Proposed keyed top plugs and bottom input sockets</title>',
             '<style>text{font-family:DejaVu Sans,Arial,sans-serif}</style>',
             '<rect width="1180" height="900" fill="#f6f5ef"/>']

    def text(x, y, message, size=16, bold=False, fill='#233c43'):
        items.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
                     f'font-weight="{"bold" if bold else "normal"}">{escape(str(message))}</text>')

    def rect(x, y, w, h, fill, stroke='none'):
        items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                     f'fill="{fill}" stroke="{stroke}"/>')

    def profile(x, y, cells, color):
        cell = 19
        for gx, gy in product(range(-3, 4), repeat=2):
            rect(x + (gx + 3) * cell, y + (gy + 3) * cell, cell, cell,
                 color if (gx, gy) in cells else '#fffefa', '#ced6d1')

    text(32, 43, 'Full fit: why the previous wildcard proposal fails', 27, True)
    text(32, 74, 'Top plugs protrude upwards; matching recesses are on the bottom of the next tile.', 17)
    text(32, 101, 'These are plan views in the same assembly coordinates, not views looking up from underneath.', 14)

    columns = [32, 247, 462, 677, 892]
    examples = [('Output 0', PLUGS['0'], '#5188b4', 'Plus-shaped plug'),
                ('Output 1', PLUGS['1'], '#5188b4', 'Diagonal-cross plug'),
                ('Rejected input *', SOCKETS['*'], '#d49b9b', 'Unused grooves: NOT full fit'),
                ('Output C0', PLUGS['C0'], '#d7a15c', 'Collar + small plus'),
                ('Output C1', PLUGS['C1'], '#d7a15c', 'Collar + small cross')]
    for x, (title, cells, color, caption) in zip(columns, examples):
        text(x, 137, title, 19, True)
        profile(x, 151, cells, color)
        text(x, 308, caption, 13)
    text(32, 340, 'Input 0/1 cavities copy the corresponding plug profile. C sockets copy only C profiles.', 16)
    text(32, 365, 'A logical * mask has no full-fit physical realization here. A union cavity cannot implement it.', 15)

    text(32, 415, 'Vertical fit: aligned section through a 0 connector', 20, True)
    # Nominal cavity equals the plug section after closing the 26-unit gap.
    rect(50, 436, 385, 36, '#a8cbbf')
    rect(50, 472, 137, 64, '#a8cbbf')
    rect(298, 472, 137, 64, '#a8cbbf')
    text(463, 464, 'Upper tile: input cavity on BOTTOM', 17, True)
    text(463, 492, 'Recess accepts the entire protruding profile.', 15)
    rect(50, 562, 385, 49, '#5188b4')
    rect(187, 498, 111, 64, '#5188b4')
    text(463, 562, 'Lower tile: output plug on TOP', 17, True)
    text(463, 590, 'Nominal plug volume must equal recess volume once seated.', 15)
    text(50, 635, 'Exploded vertically for clarity; assembly closes the gap between the two face planes.', 14)

    text(32, 680, 'Verified FULL-fit matrix: * columns correctly fail', 20, True)
    inputs = list(SOCKETS)
    for j, name in enumerate(inputs):
        text(204 + j * 91, 710, name, 16, True)
    for i, (name, row) in enumerate(report['fit_matrix'].items()):
        y = 738 + i * 27
        text(32, y, f'Output {name}', 16, True)
        for j, input_name in enumerate(inputs):
            text(204 + j * 91, y, 'yes' if row[input_name] else '-', 16,
                 fill='#286959' if row[input_name] else '#899691')
    text(814, 719, 'C collar blocks ordinary sockets.', 14)
    text(814, 746, 'Inner moat blocks ordinary plugs', 14)
    text(814, 767, 'from entering C sockets.', 14)
    text(32, 876, 'Assumes registered tile positions. Full tile alignment, clearances and printable dimensions remain to be designed.', 14)
    items.append('</svg>')
    path.write_text('\n'.join(items), encoding='utf8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path(__file__).parent / 'connector-proposal')
    args = parser.parse_args()
    report = verify()
    args.out.mkdir(parents=True, exist_ok=True)
    draw(args.out / 'connectors.svg', report)
    (args.out / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
    print(report['result'])
    print(f"Checked {report['pairings_checked_including_rotations']} pairings; diagram: {args.out / 'connectors.svg'}")


if __name__ == '__main__':
    main()
