"""Follow actual MWSS crossings, detected from exact Life cells, in Golly output."""
from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import importlib.util
import json
from functools import lru_cache

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ping',ROOT/'scripts/render-switch-engine-ping-pong.py')
ping=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ping)

def step(live):
    counts=Counter((x+dx,y+dy) for x,y in live for dx in (-1,0,1) for dy in (-1,0,1) if dx or dy)
    return {p for p,n in counts.items() if n==3 or (n==2 and p in live)}

def normalize(cells):
    x=min(x for x,y in cells);y=min(y for x,y in cells)
    return frozenset((a-x,b-y) for a,b in cells)

def forms(live=None):
    if live is None:
        live={(3,0),(1,1),(5,1),(0,2),(0,3),(5,3),*((x,4) for x in range(5))}
    result=set()
    for _ in range(4):
        for a,b,c,d in [(1,0,0,1),(0,-1,1,0),(-1,0,0,-1),(0,1,-1,0),
                        (1,0,0,-1),(-1,0,0,1),(0,1,1,0),(0,-1,-1,0)]:
            result.add(normalize({(a*x+b*y,c*x+d*y) for x,y in live}))
        live=step(live)
    return result

MWSS=forms()
LWSS=forms({(1,0),(4,0),(0,1),(0,2),(4,2),*((x,3) for x in range(4))})
HWSS=forms({(3,0),(4,0),(1,1),(6,1),(0,2),(0,3),(6,3),*((x,4) for x in range(6))})
glider={(1,0),(2,1),(0,2),(1,2),(2,2)}
NW_GLIDER=set()
for _ in range(4):
    NW_GLIDER.add(normalize({(-x,-y) for x,y in glider}))
    glider=step(glider)
FORMS=MWSS|LWSS|HWSS|NW_GLIDER
NEIGHBORS=[(x,y) for x in range(-2,3) for y in range(-2,3) if x or y]

def detect(cells):
    remaining=set(cells)
    ships=[]
    while remaining:
        point=remaining.pop(); group={point}; stack=[point]
        while stack:
            x,y=stack.pop()
            for dx,dy in NEIGHBORS:
                p=(x+dx,y+dy)
                if p in remaining:
                    remaining.remove(p);group.add(p);stack.append(p)
        if len(group) in (5,9,11,12,13,15,18) and normalize(group) in FORMS:
            ships.append(group)
    return ships

def find_ships(nodes):
    """Search unique local macrocell nodes, rather than billions of cells."""
    @lru_cache(None)
    def local(index):
        if not index:
            return frozenset()
        level,data=nodes[index]
        if level==3:
            return frozenset(data)
        half=2**(level-1)
        return frozenset((x+dx,y+dy) for child,(dx,dy) in
            zip(data,[(0,0),(half,0),(0,half),(half,half)])
            for x,y in local(child))
    matches={}
    for i,node in enumerate(nodes):
        if node and node[0] in (6,7):
            found=detect(local(i))
            if found:matches[i]=found
    @lru_cache(None)
    def contains(index):
        if not index:return False
        if index in matches:return True
        level,data=nodes[index]
        return level>6 and any(contains(c) for c in data)
    result=[]
    def visit(index,x,y):
        if not contains(index):return
        if index in matches:
            result.extend({(a+x,b+y) for a,b in s} for s in matches[index]);return
        level,data=nodes[index];half=2**(level-1)
        for child,(dx,dy) in zip(data,[(0,0),(half,0),(0,half),(half,half)]):visit(child,x+dx,y+dy)
    half=2**(nodes[-1][0]-1)
    visit(len(nodes)-1,-half,1-half)
    return result

def animate():
    frames=[]; report=[]
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    samples=list(range(4456448,8126465,32768))
    for i,g in enumerate(samples):
        nodes,pops=ping.snapshot(g)
        ships=find_ships(nodes)
        scale=1024
        cx=g//12+100000;cy=100000-g//12
        vx=(cx//scale-400)*scale;vy=((cy-1)//scale-260)*scale+1
        view=(vx,vy,vx+800*scale,vy+520*scale)
        # The two parallel original glider streams enclose this band.
        # Reject unrelated outward gliders rather than following them.
        visible=[s for s in ships if 2000 < sum(min(s)) < 392000
                 and vx < min(x for x,y in s) < view[2]
                 and vy < min(y for x,y in s) < view[3]-50*scale]
        craft=[s for s in visible if len(s)>5]
        targets=craft or visible
        frame=ping.render(nodes,g,view,10,pops[-1])
        draw=ImageDraw.Draw(frame)
        draw.rectangle((0,480,800,520),fill='#102f39')
        draw.text((16,489),f'Ping-pong crossings  ·  generation {g:,}',font=font,fill='#cce5dc')
        if targets:
            target=min(targets,key=lambda s:abs(min(x for x,y in s)-cx)+abs(min(y for x,y in s)-cy))
            tx=min(x for x,y in target);ty=min(y for x,y in target)
            px=(tx-vx)//scale;py=(ty-vy)//scale
            label='MWSS' if len(target)>5 else 'Return glider'
            draw.ellipse((px-7,py-7,px+7,py+7),outline='#efbf61',width=2)
            draw.text((min(px+12,640),max(12,py-15)),label,font=font,fill='#efbf61')
            # Magnify the actual current cells, without changing the overview.
            inset=(tx-5,ty-5,tx+11,ty+11)
            detail=ping.pixels(nodes,0,inset)
            draw.rectangle((648,325,784,468),fill='#143e48',outline='#527769',width=1)
            draw.text((660,335),'Cell detail',font=font,fill='#cce5dc')
            for x,y in detail:
                color='#efbf61' if (x+inset[0],y+inset[1]) in target else '#a1ddcb'
                draw.rectangle((660+x*7,360+y*6,665+x*7,364+y*6),fill=color)
        else:
            draw.text((20,24),'Between crossings',font=font,fill='#89afa2')
        frames.append(frame)
        report.append({'generation':g,'viewport':view,
                       'tracked_cells':[sorted(s) for s in targets]})
        if i%10==0:print('Crossings',i+1,len(samples),g,flush=True)
    dest=ROOT/'public/images/switch-engine-ping-pong-crossings.gif'
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=[900]+[190]*(len(frames)-2)+[1400],
                   loop=0,disposal=2,optimize=True)
    frames[20].save(dest.with_name(dest.stem+'-still.png'))
    (ROOT/'research/switch-engine-ping-pong/crossings-animation-check.json').write_text(json.dumps({
        'engine':'Golly 3.3 / HashLife','rule':'B3/S23','source':'research/switch-engine-ping-pong/seed.rle',
        'description':'Actual source evolution. Camera follows the moving interaction region. Each overview pixel contains 1024×1024 cells. Amber locators identify exact detected MWSS/return-glider phases; the inset shows actual individual cells.',
        'frame_duration_ms':190,'frames':report},indent=2)+'\n')
    print(dest,dest.stat().st_size,flush=True)

if __name__=='__main__':
    import sys
    if '--render' in sys.argv:
        animate()
        sys.exit()
    for g in map(int,sys.argv[1:]):
        n,p=ping.snapshot(g)
        ships=find_ships(n)
        print('MWSS',g,[(min(s),len(s)) for s in ships],flush=True)
        (ROOT/'research/switch-engine-ping-pong'/f'crossings-{g}.json').write_text(json.dumps([sorted(s) for s in ships]))
