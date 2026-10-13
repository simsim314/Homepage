"""Render Golly HashLife snapshots of Michael Simkin's original 23-cell seed.

Requires installed bgolly and Pillow. At zoomed-out scales, a lit pixel means
its corresponding square contains live cells. No cells are invented or moved.
"""
from functools import lru_cache
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / 'research/switch-engine-ping-pong/seed.rle'
CACHE = Path('/tmp/homepage-switch-engine-frames')
CACHE.mkdir(exist_ok=True)

def read_macrocell(path):
    nodes = [None]
    populations = [0]
    generation = 0
    for line in path.read_text().splitlines():
        if line.startswith('#G '):
            generation = int(line[3:])
        if not line or line.startswith(('[', '#')):
            continue
        if line[0] in '.*$':
            x = y = 0
            cells = []
            for char in line:
                if char == '$':
                    x = 0
                    y += 1
                else:
                    if char == '*':
                        cells.append((x, y))
                    x += 1
            assert all(0 <= x < 8 and 0 <= y < 8 for x, y in cells)
            nodes.append((3, cells))
            populations.append(len(cells))
        else:
            level, *children = map(int, line.split())
            assert len(children) == 4 and level >= 4
            assert all(0 <= child < len(nodes) for child in children)
            assert all(nodes[child][0] == level - 1 for child in children if child)
            nodes.append((level, children))
            populations.append(sum(populations[c] for c in children))
    return nodes, populations, generation

def bounds(nodes):
    @lru_cache(None)
    def local(index):
        level, data = nodes[index]
        if level == 3:
            return (min(x for x, y in data), min(y for x, y in data),
                    max(x for x, y in data) + 1, max(y for x, y in data) + 1)
        half = 2 ** (level - 1)
        boxes = []
        for child, (dx, dy) in zip(data, [(0, 0), (half, 0), (0, half), (half, half)]):
            if child:
                box = local(child)
                boxes.append((box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy))
        return (min(b[0] for b in boxes), min(b[1] for b in boxes),
                max(b[2] for b in boxes), max(b[3] for b in boxes))
    box = local(len(nodes) - 1)
    half = 2 ** (nodes[-1][0] - 1)
    return (box[0] - half, box[1] + 1 - half, box[2] - half, box[3] + 1 - half)

def pixels(nodes, scale_power, view):
    """Exact occupied scale-sized squares; root and viewport share alignment."""
    scale = 2 ** scale_power
    lit = set()
    def visit(index, x, y):
        if not index:
            return
        level, data = nodes[index]
        size = 2 ** level
        if x + size <= view[0] or y + size <= view[1] or x >= view[2] or y >= view[3]:
            return
        if level <= scale_power:
            lit.add(((x - view[0]) // scale, (y - view[1]) // scale))
        elif level == 3:
            for dx, dy in data:
                px, py = (x + dx - view[0]) // scale, (y + dy - view[1]) // scale
                if 0 <= px < (view[2]-view[0])//scale and 0 <= py < (view[3]-view[1])//scale:
                    lit.add((px, py))
        else:
            half = size // 2
            for child, (dx, dy) in zip(data, [(0, 0), (half, 0), (0, half), (half, half)]):
                visit(child, x + dx, y + dy)
    half = 2 ** (nodes[-1][0] - 1)
    visit(len(nodes) - 1, -half, 1 - half)
    return lit

def snapshot(generation):
    path = CACHE / f'{generation}.mc'
    if not path.exists():
        subprocess.run(['bgolly', '-h', '-q', '-q', '-m', str(generation), '-i', str(generation),
                        '-M', '512', '-T', '45', '-o', str(path), str(SEED)],
                       check=True, timeout=55, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    nodes, populations, actual = read_macrocell(path)
    assert actual == generation, f'Incomplete Golly run: requested {generation}, got {actual}'
    return nodes, populations

def render(nodes, generation, view, scale_power, population):
    scale = 2 ** scale_power
    width, height = (view[2] - view[0]) // scale, (view[3] - view[1]) // scale
    image = Image.new('RGB', (width, height), '#102f39')
    for x, y in pixels(nodes, scale_power, view):
        image.putpixel((x, y), (161, 221, 203))
    image = image.resize((800, round(height * 800 / width)), Image.Resampling.NEAREST)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
    draw.rectangle((0, image.height - 32, image.width, image.height), fill='#102f39')
    draw.text((16, image.height - 25), f'Generation {generation:,}  ·  {population:,} live cells',
              font=font, fill='#cce5dc')
    return image

def validate():
    """Compare decoded Golly output with an independent sparse Life update."""
    body = ''.join(line.strip() for line in SEED.read_text().splitlines()
                   if line and not line.startswith(('#', 'x =')))
    x = y = 0
    digits = ''
    live = set()
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
    assert len(live) == 23
    for _ in range(64):
        counts = Counter((x+dx, y+dy) for x,y in live
                         for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy)
        live = {p for p,n in counts.items() if n == 3 or (n == 2 and p in live)}
    nodes, populations = snapshot(64)
    half = 2 ** (nodes[-1][0]-1)
    view = (-half, 1-half, half, 1+half)
    decoded = {(x+view[0],y+view[1]) for x,y in pixels(nodes,0,view)}
    assert decoded == live, 'Macrocell decoder differs from independent Life evolution'
    assert populations[-1] == len(live)
    print(f'Validated 23-cell seed and all {len(live)} cells at generation 64.', flush=True)

if __name__ == '__main__':
    validate()
    final = 2 ** 26
    nodes, populations = snapshot(final)
    box = bounds(nodes)
    print('Final population and bounds:', populations[-1], box, flush=True)
    # A fixed close view of the growing fan, chosen after comparing whole-
    # pattern and close views. The simulation itself is never cropped.
    scale_power = 15
    scale = 2 ** scale_power
    width, height = 800, 520
    cx, cy = 3000000, 0
    vx, vy = (cx//scale-width//2)*scale, ((cy-1)//scale-height//2)*scale+1
    view = (vx, vy, vx+width*scale, vy+height*scale)
    samples = list(range(2 ** 25, final + 1, 2 ** 20))
    frames, report = [], []
    for generation in samples:
        nodes, populations = snapshot(generation)
        frames.append(render(nodes, generation, view, scale_power, populations[-1]))
        report.append({'generation':generation,'population':populations[-1]})
        print(f'Rendered {len(frames)}/{len(samples)}: {generation:,}', flush=True)
    dest = ROOT / 'public/images/switch-engine-ping-pong-growth.gif'
    # Start with a substantial visible growth structure; retain a readable hold.
    durations = [800] + [110] * (len(frames)-2) + [1200]
    frames[0].save(dest, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=True, disposal=2)
    frames[-1].save(dest.with_name(dest.stem+'-still.png'))
    frames[-1].save(ROOT / 'research/switch-engine-ping-pong/overview-final.png')
    data = {'engine':'bgolly 3.3 / HashLife','rule':'B3/S23',
            'seed_source':'Golly Patterns/Life/Breeders/switch-engine-ping-pong.rle',
            'seed_sha256':hashlib.sha256(SEED.read_bytes()).hexdigest(),
            'viewport':view,'cells_per_pixel':scale,'samples':report,
            'validation':'The 23-cell seed and decoded generation-64 output agree with an independent sparse B3/S23 implementation.',
            'description':'Fixed cropped viewport on the growing fan. The full pattern is simulated; each lit image pixel represents a square containing live cells. Sampled generations, not real-time playback.'}
    (ROOT / 'research/switch-engine-ping-pong/animation-check.json').write_text(json.dumps(data,indent=2)+'\n')
    print(dest, dest.stat().st_size, flush=True)
