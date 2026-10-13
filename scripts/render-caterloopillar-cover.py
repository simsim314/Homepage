"""Pair the credited architecture schematic with the original forward reaction.

Rebuild the native reaction with render-ca-gallery.py caterloopillar first.
This cover shows the early interaction, not a full spaceship simulation.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
original = Image.open(ROOT/'public/images/caterloopillar-forward-reaction.gif')
diagram = Image.open(ROOT/'src/assets/images/caterloopillar-lifewiki.png').convert('RGB')
diagram.thumbnail((205, 420))
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
frames, durations = [], []
for i in range(original.n_frames):
    original.seek(i)
    im = Image.new('RGB', (800, 520), '#102f39')
    d = ImageDraw.Draw(im)
    d.text((24, 16), 'Caterloopillar · mutual construction and its first forward reaction', font=font, fill='#cce5dc')
    im.paste(diagram, (24+(205-diagram.width)//2, 48))
    detail = original.convert('RGB').crop((240, 20, 560, 470))
    detail.thumbnail((480, 420))
    im.paste(detail, (290+(480-detail.width)//2, 48))
    d.text((24, 480), 'LifeWiki architecture schematic', font=small, fill='#cce5dc')
    d.text((290, 480), 'Original reaction · generation '+str(i*2), font=font, fill='#cce5dc')
    d.text((290, 502), 'Cells evolved with Golly · loop resets after 140 ticks', font=small, fill='#a0bdb8')
    frames.append(im)
    durations.append(original.info.get('duration', 130))
dest = ROOT/'public/images/life-caterloopillar.gif'
frames[0].save(dest, save_all=True, append_images=frames[1:], loop=0,
               duration=durations, disposal=2, optimize=True)
frames[len(frames)//2].save(dest.with_name(dest.stem+'-still.png'))
