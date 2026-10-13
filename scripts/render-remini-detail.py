"""Render exact cells from the original Remini macrocell, without evolving it.

M2 format: Golly Help/formats.html, as distributed by the Golly project.
The cover crops one constructor; it does not depict the entire recipe tape.
"""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'research/remini/Remini.mc'
nodes = [None]
for line in source.read_text().splitlines():
    if not line or line.startswith(('[', '#')):
        continue
    if line[0] in '.*$':
        x = y = 0
        cells = []
        for c in line:
            if c == '$':
                x = 0
                y += 1
            else:
                if c == '*':
                    cells.append((x, y))
                x += 1
        assert all(0 <= x < 8 and 0 <= y < 8 for x, y in cells)
        nodes.append((3, cells))
    else:
        level, *children = map(int, line.split())
        assert level >= 4 and len(children) == 4
        assert all(0 <= child < len(nodes) for child in children)
        assert all(nodes[child][0] == level - 1 for child in children if child)
        nodes.append((level, children))

def decode(index, ox, oy):
    if not index:
        return
    level, data = nodes[index]
    if level == 3:
        for x, y in data:
            yield ox + x, oy + y
    else:
        half = 2 ** (level - 1)
        for child, (dx, dy) in zip(data, [(0, 0), (half, 0), (0, half), (half, half)]):
            yield from decode(child, ox + dx, oy + dy)

half = 2 ** (nodes[-1][0] - 1)
cells = list(decode(len(nodes) - 1, -half, 1 - half))
assert len(cells) == len(set(cells)) == 779984, 'Unexpected Remini population'
full_bounds = [min(x for x, y in cells), min(y for x, y in cells),
               max(x for x, y in cells) + 1, max(y for x, y in cells) + 1]

# The long tape overwhelms an overview. Find a dense circuit region, then show
# its surrounding 440-cell square without changing any cell coordinates.
bins = Counter((x // 400, y // 400) for x, y in cells)
bx, by = bins.most_common(1)[0][0]
cx, cy = bx * 400 + 100, by * 400 + 100
crop = [cx - 220, cy - 220, cx + 220, cy + 220]
visible = [(x, y) for x, y in cells if crop[0] <= x < crop[2] and crop[1] <= y < crop[3]]
image = Image.new('RGB', (880, 880), '#102f39')
draw = ImageDraw.Draw(image)
for x, y in visible:
    px, py = (x - crop[0]) * 2, (y - crop[1]) * 2
    draw.rectangle((px, py, px + 1, py + 1), fill='#a1ddcb')
dest = ROOT / 'src/assets/images/remini-constructor.png'
image.save(dest)
report = {'source': 'https://github.com/simsim314/GreyGooTheory/blob/master/P30Gemini/Remini.mc',
          'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
          'rule': 'B3/S23', 'generation': 0, 'population': len(cells),
          'full_bounds': full_bounds, 'crop': crop, 'visible_cells': len(visible),
          'description': 'Exact static constructor-area detail. Most of the recipe tape is outside the crop.'}
(ROOT / 'research/remini/render-check.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
