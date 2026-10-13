"""Actual forward reading-head step from the author's WSSStapler generator.

The source uses a seven-cell loaf as its tape symbol. It is activated, carried
as a glider, reflected, and rebuilt 250 cells forward. Full-plane Golly runs
are checked against independent sparse Life; the camera only changes views.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('results', ROOT/'scripts/render-life-results.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
CODE = ROOT/'research/caterloopillar/source-code/Code-WSSStapler.py'
SOURCE = ROOT/'research/caterloopillar/forward-reading-head.rle'
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
SMALL = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
BG, CELL, AMBER = '#102f39', '#b5e8d1', '#efbf61'


def norm(cells):
    x0, y0 = min(x for x, y in cells), min(y for x, y in cells)
    return frozenset((x-x0, y-y0) for x, y in cells)


def assemble():
    # Read only literal RLEs; never execute the downloaded Golly/Python script.
    parts = {}
    temp = Path('/tmp/homepage-caterloopillar-part.rle')
    for name, body, x, y in re.findall(
        r'(\w+) = g.parse\("([^"]+)"\s*,\s*(-?\d+),\s*(-?\d+)\)', CODE.read_text()
    ):
        temp.write_text('x = 1, y = 1, rule = B3/S23\n'+body)
        parts[name] = {(px+int(x), py+int(y)) for px, py in r.rle_cells(temp)}
    # MakeForwardSalvo(distance=250): d=(250-98)/2=76. These are precisely
    # the tape-reading parts and the first tape symbol; helices/erasers omitted.
    d = 76
    live = set()
    for name, dx, dy in [('frontFrontPart', d, d), ('frontReflectingPart', 0, 2*d),
                         ('frontBackPart', d, 3*d), ('frontSL', d, d)]:
        live |= {(x+dx, y+dy) for x, y in parts[name]}
    loaf = {(x+d, y+d) for x, y in parts['frontSL']}
    x0, y0 = min(x for x, y in live), min(y for x, y in live)
    x1, y1 = max(x for x, y in live), max(y for x, y in live)
    rows = []
    for y in range(y0, y1+1):
        row, last = '', x0
        for x in sorted(x for x, yy in live if yy == y):
            if x > last:
                row += str(x-last)+'b'
            row += 'o'
            last = x+1
        rows.append(row)
    SOURCE.write_text(f'#CXRLE Pos={x0},{y0}\n#C Original WSSStapler reading parts; distance250, d76.\n'
                      f'x = {x1-x0+1}, y = {y1-y0+1}, rule = B3/S23\n'+'$'.join(rows)+'!\n')
    return live, loaf


def gliders(cells, shapes):
    remaining, found = set(cells), []
    while remaining:
        stack = [remaining.pop()]
        group = set(stack)
        while stack:
            x, y = stack.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    p = x+dx, y+dy
                    if p in remaining:
                        remaining.remove(p)
                        group.add(p)
                        stack.append(p)
        if len(group) == 5 and norm(group) in shapes:
            found.append(group)
    return found


def stage(g):
    if g < 256:
        return '1 · Spaceships activate the tape symbol'
    if g < 712:
        return '2 · A glider carries the signal forward'
    if g < 840:
        return '3 · The reading head reflects the glider'
    if g < 1288:
        return '4 · The signal approaches its new position'
    if g < 1408:
        return '5 · The next tape symbol is rebuilt'
    return '6 · Tape advances 250 cells; an output glider leaves'


def main():
    initial, loaf = assemble()
    assert len(initial) == 138 and len(loaf) == 7
    moved = {(x, y-250) for x, y in loaf}
    expected = set(initial)
    checks = {}
    for g in range(2049):
        if g in (0, 256, 768, 1408, 1440, 2048):
            nodes, population = r.native('reading-head', SOURCE, g)
            assert r.all_cells(nodes) == expected
            checks[g] = {'population': population, 'sparse_match': True,
                         'original_symbol_present': loaf <= expected,
                         'shifted_symbol_present': moved <= expected}
        expected = r.sparse_step(expected)
    assert checks[1408]['shifted_symbol_present'] and checks[2048]['shifted_symbol_present']
    final_nodes, _ = r.native('reading-head', SOURCE, 2048)
    final_cells = r.all_cells(final_nodes)
    convoy = {(x, y-1024) for x, y in initial-loaf}
    assert convoy <= final_cells
    output = final_cells-convoy-moved
    assert len(output) == 5
    base = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
    shapes = set()
    for _ in range(4):
        for sx in (-1, 1):
            for sy in (-1, 1):
                for swap in (False, True):
                    shapes.add(norm({(sy*y, sx*x) if swap else (sx*x, sy*y) for x, y in base}))
        base = r.sparse_step(base)
    samples = sorted(set([*range(0, 257, 4), *range(256, 713, 16),
                          *range(712, 841, 4), *range(840, 1289, 16),
                          *range(1288, 1441, 4), 1408]))
    frames, durations, positions = [], [], []
    previous = (209, 390)
    for i, g in enumerate(samples):
        nodes, _ = r.native('reading-head', SOURCE, g)
        cells = r.all_cells(nodes)
        signals = gliders(cells, shapes)
        signal = min(signals, key=lambda s: min((x-previous[0])**2+(y-previous[1])**2 for x, y in s)) if signals else None
        if g < 256:
            centre = (209, 390)
        elif g >= 1288:
            centre = (209, 142)
        elif signal:
            centre = (sum(x for x, y in signal)//5, sum(y for x, y in signal)//5)
        else:
            centre = previous
        previous = centre
        positions.append({'generation': g, 'camera': centre,
                          'glider': sorted(signal) if signal else None})
        frame = Image.new('RGB', (800, 660), BG)
        d = ImageDraw.Draw(frame)
        d.text((20, 16), 'Caterloopillar · one forward reading-head step', font=FONT, fill=CELL)
        # Overview rotated 90 degrees: left is forward/up in the source.
        # All lit pixels are native cells; dots only enlarge occupied pixels.
        for x, y in cells:
            if 60 <= x < 280 and 100 <= y < 820:
                px, py = 150+round((y-100)*.7), 46+round((x-60)*.7)
                d.point((px, py), fill=CELL)
        for symbol, label in [(loaf, 'Start'), (moved, '+250 cells')]:
            cx = 150+round((sum(y for x, y in symbol)/7-100)*.7)
            cy = 46+round((sum(x for x, y in symbol)/7-60)*.7)
            d.ellipse((cx-7, cy-7, cx+7, cy+7), outline=AMBER if symbol <= cells else '#58747c', width=2)
            d.text((cx-25, cy+12), label, font=SMALL, fill='#a0bdb8')
        if signal:
            x0, y0 = min(x for x, y in signal), min(y for x, y in signal)
            px, py = 150+round((y0-100)*.7), 46+round((x0-60)*.7)
            d.rectangle((px-3, py-3, px+5, py+5), outline=AMBER, width=2)
        d.text((20, 222), '← Forward · overview rotated 90° · zoom below uses original orientation', font=SMALL, fill='#a0bdb8')
        d.text((20, 260), stage(g), font=FONT, fill=AMBER)
        view = (centre[0]-27, centre[1]-14, centre[0]+28, centre[1]+14)
        scale = 12
        xoff, yoff = 70, 292
        for x, y in cells:
            if view[0] <= x < view[2] and view[1] <= y < view[3]:
                px, py = xoff+(x-view[0])*scale, yoff+(y-view[1])*scale
                d.rectangle((px, py, px+scale-1, py+scale-1), fill=CELL)
        d.text((20, 638), f'Generation {g:,} · original source evolved in Golly · loop resets', font=SMALL, fill=CELL)
        frames.append(frame)
        durations.append(850 if g in (0, 712, 840, 1408, 1440) else 110)
        if i % 40 == 0:
            print('reader', i, len(samples), g, flush=True)
    dest = ROOT/'public/images/caterloopillar-reading-head.gif'
    frames[0].save(dest, save_all=True, append_images=frames[1:], loop=0,
                   duration=durations, disposal=2, optimize=True)
    frames[samples.index(1408)].save(dest.with_name(dest.stem+'-still.png'))
    report = {'source': 'https://github.com/simsim314/Caterloopilar/blob/master/Code/WSSStapler.py',
              'source_code_sha256': hashlib.sha256(CODE.read_bytes()).hexdigest(),
              'pattern_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'engine': 'Golly 3.3 / HashLife', 'rule': 'B3/S23', 'distance': 250,
              'source_parts': ['frontFrontPart', 'frontReflectingPart', 'frontBackPart', 'frontSL'],
              'initial_tape_symbol': sorted(loaf), 'rebuilt_tape_symbol': sorted(moved),
              'independent_checks': checks, 'generations': samples, 'dimensions': [800, 660],
              'reading_convoy_intact_at_2048': True,
              'exact_output_glider_at_2048': sorted(output),
              'camera_and_actual_signals': positions,
              'description': 'Full isolated original reading-head mechanism simulated. Uses a loaf, not a four-cell block. Exact glider detection controls camera. Overview rotated with unchanged geometry. Loop resets after successful symbol reconstruction.'}
    (ROOT/'research/caterloopillar/reading-head-animation-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(dest, flush=True)


if __name__ == '__main__':
    main()
