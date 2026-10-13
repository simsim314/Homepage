"""A cell-scale collision, with captions and pauses, from the original seed.

The starting Golly snapshot is cropped with a causal margin wider than the
entire 720-generation clip. Its final displayed cells are also checked against
a full-pattern Golly run. Captions never replace or interpolate cell states.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util
import subprocess
import json

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('crossings',ROOT/'scripts/render-ping-pong-crossings.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
START=5454592
CONTACT=5454713
VIEW=(781800,-387750,781950,-387650)
CACHE=Path('/tmp/homepage-ping-collision');CACHE.mkdir(exist_ok=True)

def encode(cells,view,generation,path):
    rows={}
    for x,y in cells:rows.setdefault(y,[]).append(x)
    parts=[];last=0
    for y,xs in sorted(rows.items()):
        if y>last:parts.append((str(y-last) if y-last>1 else '')+'$')
        cursor=0
        for x in sorted(xs):
            if x>cursor:parts.append((str(x-cursor) if x-cursor>1 else '')+'b')
            parts.append('o');cursor=x+1
        last=y
    body=''.join(parts)+'!'
    path.write_text(f'#CXRLE Pos={view[0]},{view[1]} Gen={generation}\n'
                    f'x = {view[2]-view[0]}, y = {view[3]-view[1]}, rule = B3/S23\n'+
                    '\n'.join(body[i:i+70] for i in range(0,len(body),70))+'\n')

def evolve(source,g,path):
    subprocess.run(['bgolly','-h','-q','-q','-m',str(g),'-i',str(max(1,g-START)),
                    '-M','512','-o',str(path),str(source)],check=True,timeout=30,
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    n,p,actual=r.ping.read_macrocell(path);assert actual==g
    return n

if __name__=='__main__':
    # START is an already researched exact snapshot, not an altered setup.
    nodes,_=r.ping.snapshot(START)
    margin=2048
    expanded=(VIEW[0]-margin,VIEW[1]-margin,VIEW[2]+margin,VIEW[3]+margin)
    source=ROOT/'research/switch-engine-ping-pong/collision-window.rle'
    encode(r.ping.pixels(nodes,0,expanded),expanded,START,source)
    final=START+720
    cropped=evolve(source,final,CACHE/'check.mc')
    # Use a nearby complete snapshot to reach the exact final generation.
    r.ping.snapshot(5454688)
    base=r.ping.CACHE/'5454688.mc'
    out=CACHE/'full-check.mc'
    subprocess.run(['bgolly','-h','-q','-q','-m',str(final),'-i',str(final-5454688),
                    '-M','512','-o',str(out),str(base)],check=True,timeout=30,
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    full,_,actual=r.ping.read_macrocell(out);assert actual==final
    search_view=(781416,-388134,782334,-387266)
    assert r.ping.pixels(cropped,0,search_view)==r.ping.pixels(full,0,search_view)
    titlefont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    frames=[];durations=[];report=[];return_seen=False;previous='';target=None
    for i,g in enumerate(range(START+88,final+1,4)):
        n=evolve(source,g,CACHE/f'{g}.mc')
        search_cells=r.ping.pixels(n,0,search_view)
        gliders=[s for s in r.detect(search_cells) if r.normalize(s) in r.NW_GLIDER]
        # The inset follows one actual return glider after it forms. Before
        # then, its tight camera stays fixed on the contact location.
        close_view=(781850,-387712,781900,-387680)
        if gliders and g>CONTACT:
            previous_target=target or (781875,-387696)
            candidates=[(min(x for x,y in s)+search_view[0],min(y for x,y in s)+search_view[1]) for s in gliders]
            target=min(candidates,key=lambda p:abs(p[0]-previous_target[0])+abs(p[1]-previous_target[1]))
            return_seen=True
            close_view=(target[0]-24,target[1]-15,target[0]+26,target[1]+17)
        cells=r.ping.pixels(n,0,close_view)
        if g<CONTACT:
            title='1 / The spaceship approaches.'
            subtitle='It is about to meet the other glider stream.'
        elif return_seen:
            title='3 / Follow the return glider.'
            subtitle='It travels back toward the first stream to continue the exchange.'
        else:
            title='2 / The collision unfolds.'
            subtitle='Watch the cells rearrange into the outgoing signals.'
        frame=Image.new('RGB',(800,600),'#102f39');draw=ImageDraw.Draw(frame)
        draw.text((24,17),title,font=titlefont,fill='#efbf61')
        draw.text((24,53),subtitle,font=font,fill='#cce5dc')
        for x,y in cells:
            draw.rectangle((25+x*15,88+y*15,37+x*15,100+y*15),fill='#a1ddcb')
        draw.text((24,576),f'Actual Life cells · generation {g:,}',font=font,fill='#cce5dc')
        frames.append(frame)
        durations.append(2300 if title!=previous else 110)
        previous=title
        report.append({'generation':g,'caption':title,'viewport':close_view,'visible_population':len(cells)})
    durations[-1]=2300
    dest=ROOT/'public/images/switch-engine-ping-pong-collision.gif'
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True,disposal=2)
    frames[45].save(dest.with_name(dest.stem+'-still.png'))
    (ROOT/'research/switch-engine-ping-pong/collision-animation-check.json').write_text(json.dumps({
        'engine':'Golly 3.3 / HashLife','rule':'B3/S23','source':'original 23-cell seed',
        'generations':[START+88,final],'cell_scale':15,
        'validation':'2048-cell causal margin around a 720-generation clip; the final complete search region equals a full-pattern Golly run. Camera follows an exact detected NW glider after the collision.',
        'return_glider_detected':return_seen,'frames':report},indent=2)+'\n')
    print(dest,dest.stat().st_size,'return glider detected:',return_seen,flush=True)
