"""Render the documented 29-cell Simkin glider gun using B3/S23.
Optional development utility; needs Python and Pillow. Not required for builds.
"""
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw
RLE = '2o5b2o$2o5b2o2$4b2o$4b2o5$22bo3bo$21bo4b2o$20b2o5b2o2b2o$21b2o4bo3b2o$22bo!'
W,H,S=66,35,10
live=set();x,y=13,10;digits=''
for c in RLE:
    if c.isdigit(): digits+=c;continue
    n=int(digits or 1);digits=''
    if c=='o':
        live.update((x+i,y) for i in range(n));x+=n
    elif c=='b':x+=n
    elif c=='$':x=13;y+=n
assert len(live)==29
frames=[]
for generation in range(480):
    if generation%4==0:
        image=Image.new('RGB',(W*S,H*S),'#102f39');draw=ImageDraw.Draw(image)
        for gx in range(W+1):draw.line((gx*S,0,gx*S,H*S),fill='#214049')
        for gy in range(H+1):draw.line((0,gy*S,W*S,gy*S),fill='#214049')
        for x,y in live:draw.rectangle((x*S+1,y*S+1,x*S+8,y*S+8),fill='#a1ddcb')
        frames.append(image.convert('P',palette=Image.Palette.ADAPTIVE,colors=4))
    counts=Counter((x+dx,y+dy) for x,y in live for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and 0<=x+dx<W and 0<=y+dy<H)
    live={p for p,n in counts.items() if n==3 or (n==2 and p in live)}
output=Path(__file__).resolve().parents[1]/'public/images/simkin-glider-gun.gif'
frames[0].save(output,save_all=True,append_images=frames[1:],duration=55,loop=0,optimize=True)
print(f'{output}: {len(frames)} frames, {output.stat().st_size} bytes')
