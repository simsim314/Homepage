"""Render source patterns with Golly; never substitute rules or invent cells.

Requires bgolly 3.3 and Pillow. Source posts/rules are in research/ca-visuals.
Every clip has a still frame for the site's reduced-motion control.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util
import subprocess
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'research/ca-visuals'
CACHE = Path('/tmp/homepage-ca-gallery')
CACHE.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location('ping', ROOT/'scripts/render-switch-engine-ping-pong.py')
ping = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ping)
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
PALETTE = ['#102f39', '#b5e8d1', '#efbf61', '#f7de5a', '#ed6074', '#68d796', '#ff9557', '#a0d5f2', '#859ca8']

def state_cells(path, view, scale=1):
    """Decode RuleLoader's multistate M2 leaf nodes in a cropped viewport."""
    nodes = [None]
    generation = 0
    for line in path.read_text().splitlines():
        if line.startswith('#G '):
            generation = int(line[3:])
        if not line or line.startswith(('[', '#')):
            continue
        data = list(map(int, line.split()))
        assert len(data) == 5
        nodes.append((data[0], data[1:]))
    visible = {}
    def visit(index, x, y):
        if not index:
            return
        level, data = nodes[index]
        size = 2**level
        if x+size <= view[0] or y+size <= view[1] or x >= view[2] or y >= view[3]:
            return
        if size <= scale:
            # Macrocell nodes are nonempty. At coarse zoom, show occupancy
            # without expanding millions or billions of individual cells.
            visible[((x-view[0])//scale,(y-view[1])//scale)] = 1
            return
        if level == 1:
            for state, (dx,dy) in zip(data, [(0,0),(1,0),(0,1),(1,1)]):
                px,py=x+dx,y+dy
                if state and view[0] <= px < view[2] and view[1] <= py < view[3]:
                    visible[((px-view[0])//scale,(py-view[1])//scale)] = state
        else:
            half=size//2
            for child,(dx,dy) in zip(data,[(0,0),(half,0),(0,half),(half,half)]):
                visit(child,x+dx,y+dy)
    half=2**(nodes[-1][0]-1)
    visit(len(nodes)-1,-half,1-half)
    return visible,generation

def snapshot(name, source, generation, multistate=False):
    path=CACHE/f'{name}-{generation}.mc'
    if not path.exists():
        algorithm=['-a','RuleLoader','-s',str(SRC)+'/'] if multistate else ['-h']
        if generation == 0 and source.suffix == '.mc':
            return source
        subprocess.run(['bgolly',*algorithm,'-q','-q','-m',str(generation),'-i',str(max(1,generation)),
                        '-M','512','-o',str(path),str(source)],check=True,timeout=55,
                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return path

def render(cells, view, scale, label, generation):
    w,h=(view[2]-view[0])//scale,(view[3]-view[1])//scale
    im=Image.new('RGB',(w,h),PALETTE[0])
    for (x,y),state in cells.items():
        if 0 <= x < w and 0 <= y < h:
            im.putpixel((x,y),ImageColor(state))
    # Preserve the geometry, centering it inside a consistent card-sized frame.
    factor=min(760/w,450/h)
    im=im.resize((round(w*factor),round(h*factor)),Image.Resampling.NEAREST)
    frame=Image.new('RGB',(800,520),PALETTE[0])
    frame.paste(im,((800-im.width)//2,20+(450-im.height)//2))
    d=ImageDraw.Draw(frame)
    d.text((20,485),f'{label}  ·  generation {generation:,}',font=FONT,fill='#cce5dc')
    return frame

def ImageColor(state):
    s=PALETTE[state]
    return tuple(int(s[i:i+2],16) for i in (1,3,5))

def make(name,source,samples,view,label,multistate=False,scale=1,duration=130):
    frames=[]
    for i,g in enumerate(samples):
        path=snapshot(name,source,g,multistate)
        if multistate:
            cells,actual=state_cells(path,view,scale)
        else:
            nodes,pops,actual=ping.read_macrocell(path)
            cells={p:1 for p in ping.pixels(nodes,scale.bit_length()-1,view)}
        assert actual==g
        frames.append(render(cells,view,scale,label,g))
        if i%20==0: print(name,i+1,len(samples),g,flush=True)
    dest=ROOT/'public/images'/f'{name}.gif'
    frames[0].save(dest,save_all=True,append_images=frames[1:],loop=0,
                   duration=[1100]+[duration]*(len(frames)-2)+[1500],disposal=2,optimize=True)
    frames[len(frames)//2].save(dest.with_name(dest.stem+'-still.png'))
    report={'source_file':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'rule':next((l[3:] for l in source.read_text().splitlines() if l.startswith('#R ')),None) or
                   re.search(r'rule\s*=\s*([^\n\r]+)',source.read_text()).group(1),
            'engine':'Golly 3.3 / RuleLoader' if multistate else 'Golly 3.3 / HashLife',
            'generations':samples,'viewport':view,'cells_per_pixel':scale,
            'dimensions':[800,520],'frame_duration_ms':duration,
            'description':'Full source pattern evolved; only the displayed view is cropped. Loop resets to first sampled generation.'}
    (SRC/f'{name}-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(dest,dest.stat().st_size,flush=True)

if __name__=='__main__':
    import sys
    choice=sys.argv[1] if len(sys.argv)>1 else 'all'
    if choice in ('all','remini'):
        # The exact source window includes a 2400-cell margin in every
        # direction. Life's radius-one dependency cone guarantees identical
        # displayed cells through generation 2400. Compare generation 2048
        # against the complete original pattern as an additional check.
        view=(-100,-240,350,200)
        source=ROOT/'research/remini/activation-window.rle'
        check=snapshot('remini-window-check',source,2048)
        full=snapshot('remini-full-check',ROOT/'research/remini/Remini.mc',2048)
        a,_,_=ping.read_macrocell(check)
        b,_,_=ping.read_macrocell(full)
        assert ping.pixels(a,0,view)==ping.pixels(b,0,view)
        make('remini-activation',source,list(range(0,2401,12)),
             view,'Remini · activating p30 circuitry',duration=110)
    if choice in ('all','particles'):
        make('geminoid-particles-construction',SRC/'GeminoidParticles.rle',list(range(0,481,4)),
             (-10,-10,230,240),'Geminoid Particles · construction head',True,duration=130)
    if choice in ('all','serizawa'):
        make('serizawa-geminoid-circuit',SRC/'SerizawaGeminoid.rle',list(range(0,481,4)),
             (1450,-20,2400,600),'Serizawa · constructor circuitry',True,duration=130)
    if choice in ('all','growth'):
        make('serizawa-quadratic-evolution',SRC/'serizawa-quadratic.rle',list(range(262144,1048577,16384)),
             (-1048576,-1048575,1048576,1048577),'Serizawa · four-cell seed evolved',True,scale=2048,duration=220)
    if choice in ('all','ship'):
        make('lfod-c3-spaceship',SRC/'lfod-spaceship.rle',list(range(61)),
             (-30,-15,130,45),'Live Free or Die · c/3 spaceship',duration=160)
    if choice in ('all','caterloopillar'):
        make('caterloopillar-forward-reaction',ROOT/'research/caterloopillar/forward-glider-breakthrough.rle',
             list(range(0,141,2)),(-15,-40,45,50),'Caterloopillar · forward glider reaction',duration=170)
