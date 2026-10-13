"""Animate the original Life results with full-plane Golly evolution.

Small patterns are independently checked cell-for-cell with sparse B3/S23.
The growth clips aggregate occupied squares; Caterloopillar's end views
follow its c/8 motion while its labelled overview compresses tape height.
"""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
import importlib.util
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('gallery', ROOT/'scripts/render-ca-gallery.py')
gallery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gallery)
ping = gallery.ping
SOURCES = gallery.SRC


def rle_cells(path):
    body = ''.join(line.strip() for line in path.read_text().splitlines()
                   if line and not line.startswith(('#', 'x =')))
    live = set()
    x = y = 0
    digits = ''
    for char in body:
        if char.isdigit():
            digits += char
            continue
        count = int(digits or 1)
        digits = ''
        if char == 'o':
            live.update((x+i, y) for i in range(count))
            x += count
        elif char == 'b':
            x += count
        elif char == '$':
            x = 0
            y += count
        elif char == '!':
            break
    return live


def sparse_step(live):
    counts = Counter((x+dx, y+dy) for x, y in live
                     for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
    return {p for p, n in counts.items() if n == 3 or (n == 2 and p in live)}


def native(name, source, generation):
    nodes, pops, actual = ping.read_macrocell(gallery.snapshot('life-'+name, source, generation))
    assert actual == generation
    return nodes, pops[-1]


def all_cells(nodes):
    box = ping.bounds(nodes)
    return {(x+box[0], y+box[1]) for x, y in ping.pixels(nodes, 0, box)}


def validate(name, ticks, period=None, population=None):
    source = SOURCES/(name+'.rle')
    live = rle_cells(source)
    initial = set(live)
    if population:
        assert len(live) == population
    for _ in range(ticks):
        live = sparse_step(live)
    nodes, pop = native(name, source, ticks)
    assert all_cells(nodes) == live
    if period:
        assert live == initial
    return {'initial_population': len(initial), 'generation': ticks,
            'final_population': pop, 'independent_sparse_match': True,
            'exact_period_return': period}


def small_results():
    results = {}
    for name, ticks, view, label, period in [
        ('b60', 60, (-8, -5, 26, 25), 'B60 · Herschel turns back', None),
        ('bne14t30', 144, (-5, -7, 36, 27), 'BNE14T30 · B-heptomino to glider', None),
        ('brx46b', 46, (-5, -5, 19, 30), 'BRx46B · B-heptomino turns right', None),
        ('ocellus', 114, (-4, -4, 35, 29), 'Ocellus · one 114-generation cycle', 114),
        ('simkins-p60', 60, (-4, -4, 37, 35), 'Simkin’s p60 · one oscillator cycle', 60),
    ]:
        results[name] = validate(name, ticks, period)
        gallery.make('life-'+name, SOURCES/(name+'.rle'), list(range(ticks+1)),
                     view, label, duration=100)
    (SOURCES/'life-small-validation.json').write_text(json.dumps(results, indent=2)+'\n')


def growth_results():
    results = {}
    for name, population in [('24-cell-quadratic-growth', 24), ('25-cell-quadratic-growth', 25)]:
        results[name] = validate(name, 64, population=population)
        nodes, pop = native(name, SOURCES/(name+'.rle'), 2**24)
        box = ping.bounds(nodes)
        # Root pixel grid has y origin 1. Keep view aligned for exact occupancy.
        scale = 16384
        x0 = (box[0]//scale-2)*scale
        y0 = ((box[1]-1)//scale-2)*scale+1
        x1 = ((box[2]+scale-1)//scale+2)*scale
        y1 = ((box[3]-1+scale-1)//scale+2)*scale+1
        gallery.make('life-'+name, SOURCES/(name+'.rle'),
                     list(range(2**22, 2**24+1, 2**18)), (x0, y0, x1, y1),
                     f'{population}-cell seed · later growth', scale=scale, duration=190)
        results[name].update({'final_generation': 2**24, 'full_final_population': pop,
                              'occupied_square_side': scale})
    (SOURCES/'life-growth-validation.json').write_text(json.dumps(results, indent=2)+'\n')


def panel(nodes, view, size, power=0, compress=False):
    scale = 2**power
    width, height = (view[2]-view[0])//scale, (view[3]-view[1])//scale
    im = Image.new('RGB', (width, height), '#102f39')
    for x, y in ping.pixels(nodes, power, view):
        if 0 <= x < width and 0 <= y < height:
            im.putpixel((x, y), (181, 232, 209))
    if compress:
        # Reduce by maximum occupancy so no thin tape section disappears.
        out = Image.new('RGB', size, '#102f39')
        d = ImageDraw.Draw(out)
        for x, y in ping.pixels(nodes, power, view):
            px, py = x*size[0]//width, y*size[1]//height
            d.rectangle((px, py, min(size[0]-1, px+max(1,size[0]//width)), py+1),
                        fill='#b5e8d1')
        return out
    factor = min(size[0]/width, size[1]/height)
    im = im.resize((round(width*factor), round(height*factor)), Image.Resampling.NEAREST)
    out = Image.new('RGB', size, '#102f39')
    out.paste(im, ((size[0]-im.width)//2, (size[1]-im.height)//2))
    return out


def caterloopillar():
    source = ROOT/'research/caterloopillar/Caterloopillar_c8.rle'
    first, pop = native('caterloopillar', source, 0)
    last, endpop = native('caterloopillar', source, 2000)
    assert pop == endpop == 238189
    assert all_cells(last) == {(x, y-250) for x, y in all_cells(first)}
    frames = []
    generations = list(range(0, 2000, 20))
    for g in generations:
        nodes, _ = native('caterloopillar', source, g)
        shift = g//8
        frame = Image.new('RGB', (800, 520), '#102f39')
        d = ImageDraw.Draw(frame)
        for x, text in [(20, 'Tape overview'), (150, 'Front-end detail'), (480, 'Back-end detail')]:
            d.text((x, 18), text, font=gallery.FONT, fill='#cce5dc')
        frame.paste(panel(nodes, (-128, 1-512, 896, 515585), (100, 412), 8, True), (20, 52))
        frame.paste(panel(nodes, (220, 1360-shift, 340, 1520-shift), (310, 412)), (150, 52))
        frame.paste(panel(nodes, (430, 506760-shift, 550, 506920-shift), (310, 412)), (480, 52))
        d.text((20, 480), f'c/8 Caterloopillar · generation {g:,} · following both ends',
               font=gallery.FONT, fill='#cce5dc')
        d.text((20, 502), 'Overview height compressed; end views preserve geometry.',
               font=gallery.FONT, fill='#a0bdb8')
        frames.append(frame)
        if g % 400 == 0:
            print('caterloopillar', g, flush=True)
    dest = ROOT/'public/images/life-caterloopillar-c8-details.gif'
    frames[0].save(dest, save_all=True, append_images=frames[1:], loop=0,
                   duration=130, disposal=2, optimize=True)
    frames[50].save(dest.with_name(dest.stem+'-still.png'))
    report = {'source_file': str(source.relative_to(ROOT)),
              'source': 'https://raw.githubusercontent.com/simsim314/Caterloopilar/master/Caterloopillar_c8.rle',
              'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'engine': 'Golly 3.3 / HashLife', 'rule': 'B3/S23',
              'generations': generations, 'dimensions': [800, 520],
              'exact_translation_at_2000': [0, -250], 'population': pop,
              'initial_detail_views': [[220, 1360, 340, 1520], [430, 506760, 550, 506920]],
              'description': 'Full pattern simulated. Two end crops follow c/8 translation. Tape height explicitly compressed. Loop resets after one period.'}
    (SOURCES/'life-caterloopillar-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(dest, flush=True)


if __name__ == '__main__':
    choice = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if choice in ('all', 'small'):
        small_results()
    if choice in ('all', 'growth'):
        growth_results()
    if choice in ('all', 'caterloopillar'):
        caterloopillar()
