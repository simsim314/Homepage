"""Difficult routing and close-clearance tests from original Caterloopillar sources.

Only native Golly cells are drawn. Annotation arrows show the direction of
exact detected gliders; the camera does not change the simulation.
"""
import importlib.util, json, hashlib, re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mechanisms',ROOT/'scripts/render-caterloopillar-mechanisms.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r=m.r;h=m.h
SRC=ROOT/'research/caterloopillar';OUT=ROOT/'public/images'
F=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
BG=m.BG;GREEN=m.CELL;AMBER=m.AMBER;CYAN='#68c5df'
BASE={(1,0),(2,1),(0,2),(1,2),(2,2)};SHAPES=set()
for _ in range(4):
 for sx in (-1,1):
  for sy in(-1,1):
   for swap in(False,True):SHAPES.add(h.norm({(sy*y,sx*x)if swap else(sx*x,sy*y)for x,y in BASE}))
 BASE=r.sparse_step(BASE)

def coords(source):
 live=r.rle_cells(source);pos=re.search(r'#CXRLE Pos=(-?\d+),(-?\d+)',source.read_text())
 if pos:live={(x+int(pos[1]),y+int(pos[2]))for x,y in live}
 return live

def validate(name,source,points):
 live=coords(source);checks={}
 for g in range(max(points)+1):
  if g in points:
   n,p=r.native(name,source,g);assert live==r.all_cells(n),(name,g)
   checks[g]={'population':p,'exact_independent_Life_match':True}
  live=r.sparse_step(live)
 return checks

def signals(cells):
 out=[]
 for a in h.gliders(cells,SHAPES):
  b=set(a)
  for _ in range(4):b=r.sparse_step(b)
  out.append((a,(min(x for x,y in b)-min(x for x,y in a),min(y for x,y in b)-min(y for x,y in a))))
 return out

def frame(title,caption,g,cells,view,marks=(),arrows=()):
 im=Image.new('RGB',(800,620),BG);d=ImageDraw.Draw(im)
 d.text((24,16),title,font=F(24),fill=AMBER);d.text((24,57),caption,font=F(17),fill=GREEN)
 x0,y0,x1,y1=view;scale=min(744/(x1-x0),466/(y1-y0));ox=28+(744-(x1-x0)*scale)/2;oy=100+(466-(y1-y0)*scale)/2
 for x,y in cells:
  if x0<=x<x1 and y0<=y<y1:
   px=round(ox+(x-x0)*scale);py=round(oy+(y-y0)*scale)
   d.rectangle((px,py,round(ox+(x+1-x0)*scale)-1,round(oy+(y+1-y0)*scale)-1),fill=GREEN)
 for obj,color in marks:
  if obj and obj<=cells:
   xs=[x for x,y in obj];ys=[y for x,y in obj];d.rectangle((ox+(min(xs)-x0)*scale-4,oy+(min(ys)-y0)*scale-4,ox+(max(xs)+1-x0)*scale+3,oy+(max(ys)+1-y0)*scale+3),outline=color,width=2)
 for a,(dx,dy) in arrows:
  cx=sum(x for x,y in a)/5;cy=sum(y for x,y in a)/5
  if x0+3<cx<x1-3 and y0+3<cy<y1-3:
   ax=ox+(cx-x0)*scale;ay=oy+(cy-y0)*scale
   # A separate direction marker, never rendered as Life cells.
   ex=ax+dx*28;ey=ay+dy*28;d.line((ax+dx*12,ay+dy*12,ex,ey),fill=AMBER,width=2)
   d.line((ex,ey,ex-dx*9-dy*4,ey-dy*9+dx*4),fill=AMBER,width=2)
   d.line((ex,ey,ex-dx*9+dy*4,ey-dy*9-dx*4),fill=AMBER,width=2)
 d.text((24,584),f'Generation {g:,} · native Golly evolution · loop resets',font=F(16),fill=m.MUTED)
 return im

REPORT=[]
def save(name,source,gs,frames,views,checks,still=0):
 durations=[650 if i in(0,len(frames)-1) else 75 for i in range(len(frames))]
 m.save_gif(OUT/(name+'.gif'),frames,durations);frames[still].save(OUT/(name+'-still.png'))
 REPORT.append(dict(id=name,source_file=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),generations=gs,views=views,checks=checks))
 print(name,len(frames),'frames',flush=True)

def routing():
 source=SRC/'forward-complete-head.rle';name='forward-complete-head';gs=list(range(480,921,4));checks=validate(name,source,{0,480,560,720,800,920});frames=[];views=[];previous=(60,-190)
 for g in gs:
  n,p=r.native(name,source,g);cells=r.all_cells(n);sigs=[(a,d)for a,d in signals(cells)if min(y for x,y in a)<0]
  direction=(1,-1)if g<550 else (1,1)if g<700 else(-1,1)if g<770 else(1,-1)
  candidates=[(a,d)for a,d in sigs if d==direction]
  if candidates:
   chosen=min(candidates,key=lambda z:(sum(x for x,y in z[0])/5-previous[0])**2+(sum(y for x,y in z[0])/5-previous[1])**2)
   previous=tuple(round(sum(c[k]for c in chosen[0])/5)for k in(0,1))
  cx,cy=previous;view=(cx-23,cy-16,cx+23,cy+16)
  caption='Incoming signal reaches the moving splitter'if g<550 else'One branch returns; another takes the deletion route'if g<700 else'The erasure branch turns through another convoy'if g<770 else'Another split supplies the outgoing signals'
  frames.append(frame('Splitting, returning, and routing a signal',caption,g,cells,view,arrows=sigs));views.append(view)
 checks['directions']={str(g):[d for a,d in signals(r.all_cells(r.native(name,source,g)[0]))if min(y for x,y in a)<0]for g in(520,560,720,800)}
 save('caterloopillar-signal-routing',source,gs,frames,views,checks,gs.index(720))

def reversal():
 source=SRC/'forward-complete-head.rle';name='forward-complete-head'
 gs=list(range(712,833,2));checks=validate(name,source,{0,712,760,800,832});frames=[];views=[]
 view=(54,-183,98,-137)
 def local_directions(g):
  cells=r.all_cells(r.native(name,source,g)[0])
  return [d for a,d in signals(cells) if all(view[0]<=x<view[2] and view[1]<=y<view[3] for x,y in a)]
 assert local_directions(720)==[(-1,1)]
 assert sorted(local_directions(800))==[(1,-1),(1,1)]
 for g in gs:
  cells=r.all_cells(r.native(name,source,g)[0]);sigs=signals(cells)
  caption='Incoming glider travels southwest' if g<748 else 'Moving ships redirect and split the signal' if g<788 else 'Return output: northeast · second output: southeast'
  frames.append(frame('Reverse the glider and split an output',caption,g,cells,view,arrows=sigs));views.append(view)
 checks['incoming_direction_at_720']=[-1,1];checks['output_directions_at_800']=[[1,-1],[1,1]]
 save('caterloopillar-glider-reversal',source,gs,frames,views,checks,gs.index(768))

def failure():
 source=SRC/'clearance-test-eight-recipes.rle';name='clearance-test-eight';gs=list(range(5200,5801,8));checks=validate(name,source,{0,5200,5600,5800});initial=coords(source);old={(x,y)for x,y in initial if 7222<=x<7226 and 3962<=y<3967};assert len(old)==12;frames=[];views=[]
 for g in gs:
  n,p=r.native(name,source,g);cells=r.all_cells(n);moved={(x,y-g//2)for x,y in old};cy=3964-g//2;view=(7180,cy-35,7260,cy+35)
  caption='The old LWSS passes beside the developing insertion'if moved<=cells else'The recipe has destroyed the passing LWSS'
  frames.append(frame('Why an inserter must have enough clearance',caption,g,cells,view,marks=[(moved,CYAN)]));views.append(view)
 assert {(x,y-2600)for x,y in old}<=r.all_cells(r.native(name,source,5200)[0]);assert not {(x,y-2900)for x,y in old}<=r.all_cells(r.native(name,source,5800)[0])
 checks['existing_ship_preserved_at_5200']=True;checks['existing_ship_destroyed_at_5800']=True
 save('caterloopillar-insertion-clearance-failure',source,gs,frames,views,checks,gs.index(5520))

def crowded():
 source=SRC/'Caterloopillar_c8.rle';name='caterloopillar';gs=list(range(1280,1761,8));frames=[];views=[]
 n,p=r.native(name,source,0);v=(276,259770,302,260545);orig={(x+v[0],y+v[1])for x,y in r.ping.pixels(n,0,v)}
 old={(x,y)for x,y in orig if 282<=x<287 and 260534<=y<260541};ref={(x,y)for x,y in orig if 293<=x<298 and 259775<=y<259781};assert len(old)==13 and len(ref)==11
 for g in gs:
  stage=dict(full_ship=True,old_box=(282,260534,287,260541),id='crowded',direction=-1,camera_x=290,cache=name,source='Caterloopillar_c8')
  cells,p=m.native_cells(stage,g);cy=260533-g//2;view=(269,cy-22,313,cy+22);moving={(x,y-g//2)for x,y in old};new={(x,y+750-g//2)for x,y in ref}
  caption='An MWSS is built beside an already passing HWSS'
  frames.append(frame('Thread a new ship beside a larger passing ship',caption,g,cells,view,marks=[(moving,CYAN),(new,AMBER)]));views.append(view)
 assert moving<=cells and new<=cells
 for a in(moving,new):
  b=set(a)
  for _ in range(4):b=r.sparse_step(b)
  assert b=={(x,y-2)for x,y in a}
 save('caterloopillar-mwss-beside-hwss',source,gs,frames,views,dict(existing_HWSS_intact=True,new_MWSS_exact_match=True,reference_offset=[11,-9],independent_four_generation_motion=True),gs.index(1480))

def close_streams():
 # Reuse the full-pattern checks, but enlarge the actual close pair and its
 # temporary reaction rather than spending most of the view on empty space.
 for base_stage in m.STAGES:
  if base_stage['id'] not in ('forward-inserter','backward-inserter'):continue
  stage=dict(base_stage);checks=m.validate(stage);frames=[];views=[]
  source=SRC/(stage['source']+'.rle');gs=stage['gs'];direction=stage['direction']
  x0,y0,x1,y1=stage['old_box'];cx=round((x0+x1)/2+stage['offset'][0]/2)
  for g in gs:
   cells,pop=m.native_cells(stage,g)
   cy=round((y0+y1)/2+direction*g/2+stage['offset'][1]/2)
   view=(cx-22,cy-24,cx+22,cy+24)
   old={(x,y+direction*g//2)for x,y in stage['reference_ship']}
   new={(x+stage['offset'][0],y+stage['offset'][1])for x,y in old}
   title='Insert beside the forward-stream LWSS' if direction<0 else 'Insert beside the backward-stream MWSS'
   caption='Cyan: existing ship · amber: new ship once complete'
   frames.append(frame(title,caption,g,cells,view,marks=[(old,CYAN),(new,AMBER)]));views.append(view)
  save('caterloopillar-'+stage['id'],source,gs,frames,views,checks,len(gs)//2)

def reader():
 source=SRC/'forward-complete-head.rle';name='forward-complete-head';gs=list(range(72,281,4));checks=validate(name,source,{0,72,160,280});frames=[];views=[]
 for g in gs:
  cells=r.all_cells(r.native(name,source,g)[0]);view=(173,353,243,423)
  frames.append(frame('The reading head activates a tape symbol','A stable loaf becomes a glider signal',g,cells,view));views.append(view)
 save('caterloopillar-working-reader',source,gs,frames,views,checks,gs.index(160))

def cover():
 diagram=Image.open(OUT/'caterloopillar-architecture.png').convert('RGB');diagram.thumbnail((310,624),Image.Resampling.LANCZOS)
 base=Image.new('RGB',(1100,760),BG);d=ImageDraw.Draw(base)
 d.rounded_rectangle((16,66,346,710),radius=8,fill='white');base.paste(diagram,(181-diagram.width//2,74))
 d.text((24,20),'Caterloopillar',font=F(28),fill=GREEN)
 d.text((24,724),'Architecture: dvgrn · LifeWiki · GFDL 1.2',font=F(13),fill=m.MUTED)
 d.line((362,16,362,742),fill='#35505a',width=1)
 parts=[('glider-reversal','Reverse and split the signal'),('mwss-beside-hwss','Insert beside a passing HWSS'),('forward-inserter','Construct the forward stream'),('backward-inserter','Construct the backward stream'),('tape-rebuild','Restore the construction tape'),('head-deletion','Erase used head machinery'),('tail-deletion','Erase the opposite end')]
 frames=[];durations=[]
 for index,(name,title) in enumerate(parts):
  gif=Image.open(OUT/('caterloopillar-'+name+'.gif'))
  selected=sorted(set(list(range(0,gif.n_frames,2))+[gif.n_frames-1]))
  for i in selected:
   gif.seek(i);detail=gif.convert('RGB');detail.thumbnail((700,570),Image.Resampling.LANCZOS)
   im=base.copy();draw=ImageDraw.Draw(im)
   draw.text((390,24),f'{index+1}/{len(parts)} · {title}',font=F(23),fill=AMBER)
   im.paste(detail,(390,92))
   draw.text((390,682),'Original patterns evolved in Golly · enlarged details',font=F(17),fill=m.MUTED)
   for j in range(len(parts)):draw.rounded_rectangle((390+j*96,725,476+j*96,729),radius=2,fill=AMBER if j==index else '#35505a')
   frames.append(im);durations.append(650 if i in(0,gif.n_frames-1)else 150)
 m.save_gif(OUT/'caterloopillar-mechanisms.gif',frames,durations)
 frames[14].save(OUT/'caterloopillar-mechanisms-still.png')
 print('Updated cover',len(frames),'frames',flush=True)
 return dict(frames=len(frames),source_clips=[name for name,title in parts],architecture='public/images/caterloopillar-architecture.png',presentation='Composite of the native detail clips and credited original diagram; card-only, not shown above article components.')

if __name__=='__main__':
 routing();reversal();failure();crowded();reader();close_streams();cover_report=cover()
 (SRC/'difficult-parts-validation.json').write_text(json.dumps(dict(engine='Golly3.3/HashLife',full_plane=True,clips=REPORT,cover=cover_report),indent=2)+'\n')
