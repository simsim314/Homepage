"""Show a complete actual ping-pong exchange, keeping both streams visible.

The display rotates the diagonal streams by 45 degrees and pans only along
them. It never follows a single object horizontally: both sides of the gap
remain on screen. Amber locators and faint trails annotate exact detected
signals. The Life states are original Golly HashLife snapshots.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util
import json
import hashlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('crossings', ROOT/'scripts/render-ping-pong-crossings.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

START = 4685824
PERIOD = 2326656
END = START + PERIOD
CONTACT = 5454713
RETURN_REFERENCE = (777562, -392050)
REFERENCE_GENERATION = 5472256

def render():
    # Cover a whole exchange and the start of the next identical local cycle.
    samples = list(range(START, END, 32768)) + [END]
    frames, durations, records = [], [], []
    title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 25)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
    small_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    previous_stage = None
    center_v = -785127
    history = []
    outbound, returning = 0, 0
    for i,g in enumerate(samples):
        nodes, pops = r.ping.snapshot(g)
        objects = r.find_ships(nodes)
        # Identify this cycle's MWSS and its actual returning NW glider.
        # The return prediction only selects among detected exact phases;
        # it never supplies a substitute position when detection fails.
        ships = [s for s in objects if len(s)>5 and -5000 < sum(min(s)) < 405000
                 and abs(min(y for x,y in s) - (-387698 if g<CONTACT else -581586)) < 8]
        target = None
        if ships:
            target = min(ships, key=lambda s: abs(sum(min(s))-200000))
            stage = 'ping'
            title = 'PING → The spaceship crosses the gap.'
            subtitle = 'Keep your eye on the amber marker between the two streams.'
            outbound += 1
        elif CONTACT < g < 6300000:
            delta = (g-REFERENCE_GENERATION)//4
            expected = (RETURN_REFERENCE[0]-delta,RETURN_REFERENCE[1]-delta)
            candidates = [s for s in objects if len(s)==5 and -10000 < sum(min(s)) < 405000]
            if candidates:
                candidate = min(candidates, key=lambda s: abs(min(s)[0]-expected[0])+abs(min(s)[1]-expected[1]))
                if abs(min(candidate)[0]-expected[0])+abs(min(candidate)[1]-expected[1]) < 100:
                    target = candidate
            stage = 'pong'
            title = '← PONG: gliders return to the first stream.'
            subtitle = 'The return signal crosses the same gap in the opposite direction.'
            returning += int(target is not None)
        else:
            stage = 'restart'
            title = 'The first stream prepares the next PING.'
            subtitle = 'The exchange repeats as the engines continue moving.'
        if target:
            tx,ty = min(target)
            center_v = ty-tx
            history.append((tx,ty,stage))

        # u=x+y, v=y-x: a pure rotation with equal scale on both axes.
        # Keep horizontal framing constant, panning along the streams only.
        unit = 625
        umin, umax = -40000, 435000
        vmin, vmax = center_v-137500, center_v+137500
        scale = 512
        vx = int((umin-vmax)//(2*scale))*scale
        vy = int(((umin+vmin)/2-1)//scale)*scale+1
        right = int((umax-vmin)/(2*scale)+2)*scale
        bottom = int(((umax+vmax)/2-1)/scale+2)*scale+1
        view = (vx,vy,right,bottom)
        frame = Image.new('RGB',(800,600),'#102f39')
        draw = ImageDraw.Draw(frame)
        draw.text((22,15),title,font=title_font,fill='#efbf61')
        draw.text((22,52),subtitle,font=font,fill='#cce5dc')

        def project(x,y):
            return (20+(x+y-umin)/unit,100+(y-x-vmin)/unit)

        # Render the actual occupied squares from the full source state.
        for x,y in r.ping.pixels(nodes,9,view):
            wx,wy = vx+x*scale+scale/2,vy+y*scale+scale/2
            px,py = project(wx,wy)
            if 20<=px<780 and 100<=py<540:
                draw.rectangle((int(px),int(py),int(px)+1,int(py)+1),fill='#a1ddcb')
        for location,label in [(1200,'Stream 1'),(394200,'Stream 2')]:
            px=20+(location-umin)/unit
            draw.text((px-36,78),label,font=font,fill='#cce5dc')
        # Past actual positions, grouped separately by outward/return leg.
        for a,b in zip(history,history[1:]):
            if a[2]!=b[2]:continue
            pa,pb=project(a[0],a[1]),project(b[0],b[1])
            if all(20<p[0]<780 and 100<p[1]<540 for p in (pa,pb)):
                draw.line((*pa,*pb),fill='#806f49',width=2)
        if target:
            px,py=project(tx,ty)
            draw.ellipse((px-7,py-7,px+7,py+7),fill='#efbf61',outline='#fff0bd',width=1)
            direction='→' if stage=='ping' else '←'
            draw.text((px+14,py-13),direction,font=title_font,fill='#efbf61')
        draw.text((22,557),'Both streams stay visible · rotated view · amber marker magnifies the real signal',
                  font=small_font,fill='#89afa2')
        draw.text((22,580),f'Golly generation {g:,}',font=small_font,fill='#cce5dc')
        frames.append(frame)
        durations.append(1600 if stage!=previous_stage else 180)
        previous_stage=stage
        records.append({'generation':g,'stage':stage,'viewport':view,'camera_v':center_v,
                        'tracked_cells':sorted(target) if target else []})
        if i%15==0:print('Round trip',i+1,len(samples),g,stage,flush=True)
    assert outbound>10 and returning>10, 'Both legs must be visible in the full exchange'
    assert records[-1]['stage']=='ping', 'Clip must reach the next outward crossing'
    durations[-1]=1200
    dest=ROOT/'public/images/switch-engine-ping-pong-cycle.gif'
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True,disposal=2)
    frames[20].save(dest.with_name(dest.stem+'-still.png'))
    report={'engine':'Golly 3.3 / HashLife','rule':'B3/S23',
            'source':'research/switch-engine-ping-pong/seed.rle',
            'source_sha256':hashlib.sha256(r.ping.SEED.read_bytes()).hexdigest(),
            'generations':[START,END],'dimensions':[800,600],
            'description':'One complete exchange through the next ping. Both diagonal streams remain visible, rotated into vertical columns. Camera pans along the streams; amber locators and trails annotate exact detected source cells. Source pixels aggregate occupied 512×512-cell squares.',
            'validation':{'outbound_frames':outbound,'return_frames':returning,'next_ping_visible':True},
            'frames':records}
    (ROOT/'research/switch-engine-ping-pong/cycle-animation-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(dest,dest.stat().st_size,flush=True)

if __name__=='__main__':render()
