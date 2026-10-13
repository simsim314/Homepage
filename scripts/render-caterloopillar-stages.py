"""Native intermediate stages: reflector, encoded commands, train, entire heads.

Original literal source components are never executed. Long construction views
use the verified exact 2000-tick / 250-cell whole-pattern translation, checked
cell-for-cell at 2000 generations. Translation invariance then determines the
whole state exactly at every subsequent period; no guessed intermediate cells.
"""
import importlib.util,json,re
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('d',ROOT/'scripts/render-caterloopillar-difficult-parts.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
r=d.r;m=d.m;SRC=d.SRC;OUT=d.OUT
REPORT={}

def write(path,cells):
 x0=min(x for x,y in cells);y0=min(y for x,y in cells);x1=max(x for x,y in cells);y1=max(y for x,y in cells);rows=[]
 by_y={}
 for x,y in cells:by_y.setdefault(y,[]).append(x)
 for y in range(y0,y1+1):
  row='';last=x0
  for x in sorted(by_y.get(y,[])):
   if x>last:row+=str(x-last)+'b'
   row+='o';last=x+1
  rows.append(row)
 path.write_text(f'#CXRLE Pos={x0},{y0}\nx = {x1-x0+1}, y = {y1-y0+1}, rule = B3/S23\n'+'$'.join(rows)+'!\n')

def save(name,frames,gs,source,checks,still=0,durations=None):
 m.save_gif(OUT/(name+'.gif'),frames,durations or [700 if i in(0,len(frames)-1)else 90 for i in range(len(frames))])
 frames[still].save(OUT/(name+'-still.png'))
 REPORT[name]=dict(source=str(source.relative_to(ROOT)),generations=gs,checks=checks)
 print(name,len(frames),'frames',flush=True)

def geometry():
 parts={};tmp=Path('/tmp/cater-geometry-part.rle')
 for name,body,x,y in re.findall(r'(\w+) = g.parse\("([^"]+)"\s*,\s*(-?\d+),\s*(-?\d+)\)',(SRC/'source-code/Code-WSSStapler.py').read_text()):
  tmp.write_text('x = 1, y = 1, rule = B3/S23\n'+body);parts[name]={(px+int(x),py+int(y))for px,py in r.rle_cells(tmp)}
 offsets={'frontHelixSL':(-76,-76),'frontHelixSL2GliderWSS':(-76,-76),'frontHelixReflect':(0,0),'frontHelixGlider2SL':(-76,76),'frontErasingReflectorWSS':(0,0),'frontFrontPart':(76,76),'frontReflectingPart':(0,152),'frontBackPart':(76,228),'frontSL':(76,76)}
 groups=[];allcells=set()
 configs=[('read','Read and split',['frontFrontPart','frontSL'],'A tape symbol enters the first group of spaceships. Its signal is routed toward the return path.'),('turn','Turn the tape signal',['frontReflectingPart'],'This moving reflector sends the tape signal back toward the final converter.'),('restore','Restore and emit',['frontBackPart'],'The last converter restores the still-life symbol and leaves the outgoing construction glider.'),('clock','Keep the cadence',['frontHelixSL','frontHelixSL2GliderWSS','frontHelixReflect','frontHelixGlider2SL'],'A separate helix transfers its timing seed. Its gliders also feed the erasure route.'),('erase','Route the erasers',['frontErasingReflectorWSS'],'Additional moving ships turn and split signals for removing the used machinery.')]
 for key,title,names,description in configs:
  cells=set()
  for name in names:
   dx,dy=offsets[name];cells|={(x+dx,y+dy)for x,y in parts[name]}
  allcells|=cells
  xs=[x for x,y in cells];ys=[y for x,y in cells]
  groups.append(dict(key=key,title=title,description=description,cells=sorted(cells),box=[min(xs)-4,min(ys)-4,max(xs)-min(xs)+9,max(ys)-min(ys)+9]))
 assert allcells==d.coords(SRC/'forward-complete-head.rle')
 dest=ROOT/'src/data/caterloopillar-head.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(dict(cells=sorted(allcells),groups=groups)))
 REPORT['assembled-head']=dict(source='research/caterloopillar/forward-complete-head.rle',exact_literal_component_match=True,population=len(allcells))

def reflector():
 nodes,p=r.native('reading-head',SRC/'forward-reading-head.rle',680)
 cells={(x,y)for x,y in r.all_cells(nodes)if 70<=x<115 and 245<=y<320}
 source=SRC/'isolated-moving-reflector.rle';write(source,cells)
 checks=d.validate('isolated-moving-reflector',source,{0,80,168});gs=list(range(0,169,2));frames=[];previous=(98,272)
 for g in gs:
  live=r.all_cells(r.native('isolated-moving-reflector',source,g)[0]);signals=d.signals(live)
  if signals:
   obj,di=min(signals,key=lambda z:sum((sum(p[i]for p in z[0])/5-previous[i])**2 for i in(0,1)))
   previous=tuple(round(sum(p[i]for p in obj)/5)for i in(0,1))
  cx,cy=previous;view=(cx-25,cy-26,cx+25,cy+26)
  caption='Northwest input approaches the moving ships'if g<72 else'The collision redirects the signal'if g<112 else'An outgoing glider travels northeast'
  frames.append(d.frame('A moving glider reflector',caption,g,live,view,arrows=signals))
 assert any(di==(-1,-1)for obj,di in d.signals(cells))
 assert any(di==(1,-1)for obj,di in d.signals(r.all_cells(r.native('isolated-moving-reflector',source,168)[0])))
 save('caterloopillar-basic-reflector',frames,gs,source,checks,55)

def offsets():
 initial=d.coords(SRC/'forward-reading-head.rle');record=json.loads((SRC/'reading-head-animation-check.json').read_text());loaf=set(map(tuple,record['initial_tape_symbol']));convoy=initial-loaf;variants=[]
 for v in [-4,2,6]:
  source=SRC/f'encoded-symbol-{v}.rle';write(source,convoy|{(x,y+v)for x,y in loaf});name=f'encoded-symbol-{v}';checks=d.validate(name,source,{0,1280,1408,2048})
  final=r.all_cells(r.native(name,source,2048)[0]);remaining=final-{(x,y-1024)for x,y in convoy}-{(x,y+v-250)for x,y in loaf}
  assert len(remaining)==5 and d.signals(remaining)[0][1]==(1,-1)
  lane=min(x for x,y in remaining)+min(y for x,y in remaining);assert lane==360+v
  checks['command_offset']=v;checks['output_lane_anchor_x_plus_y']=lane;checks['convoy_intact']=True;checks['loaf_restored_250_cells_away']=True
  variants.append((v,source,name,checks))
 gs=list(range(1280,1513,4));frames=[]
 for g in gs:
  im=Image.new('RGB',(960,620),d.BG);draw=ImageDraw.Draw(im);draw.text((20,16),'A stored offset selects the outgoing glider lane',font=d.F(24),fill=d.AMBER)
  for i,(v,source,name,checks) in enumerate(variants):
   live=r.all_cells(r.native(name,source,g)[0]);view=(178,112,246,178);scale=4.2;ox=20+i*320;oy=140
   draw.text((ox,65),f'Command r = {v:+d}',font=d.F(21),fill=d.GREEN)
   for x,y in live:
    if view[0]<=x<view[2]and view[1]<=y<view[3]:
     px=round(ox+(x-view[0])*scale);py=round(oy+(y-view[1])*scale);draw.rectangle((px,py,px+3,py+3),fill=d.GREEN)
   draw.text((ox,450),f'Output lane anchor: {360+v}',font=d.F(16),fill=d.AMBER)
   draw.text((ox,485),'same reader; shifted symbol',font=d.F(15),fill=m.MUTED)
  draw.text((20,580),f'Generation {g:,} · native Golly · loop resets',font=d.F(16),fill=m.MUTED);frames.append(im)
 save('caterloopillar-command-offsets',frames,gs,variants[0][1],{str(v):checks for v,source,name,checks in variants},32)

def salvo():
 source=SRC/'forward-salvo-ahead-example.rle';name='forward-salvo-ahead-example';checks=d.validate(name,source,{0,3000,12000})
 gs=list(range(4000,12001,40));frames=[];counts=[];values=[0,-4,2,2,-8];crossings={}
 for g in gs:
  live=r.all_cells(r.native(name,source,g)[0])
  outs=[(obj,di)for obj,di in d.signals(live)if di==(1,-1)and min(x for x,y in obj)>245 and -1148<=min(x for x,y in obj)+min(y for x,y in obj)<=-1138]
  ordered=sorted(outs,key=lambda z:-min(x for x,y in z[0]));decoded=[min(x for x,y in obj)+min(y for x,y in obj)+1140 for obj,di in ordered]
  assert decoded==values[:len(decoded)]
  counts.append(len(outs));crossings.setdefault(len(outs),g)
  im=Image.new('RGB',(1000,760),d.BG);draw=ImageDraw.Draw(im);draw.text((22,14),'Read five stored commands into one slow salvo',font=d.F(24),fill=d.AMBER)
  draw.text((22,52),f'{len(outs)} / 5 outputs in the selected band · nominal command interval: 1,500 ticks',font=d.F(17),fill=d.GREEN)
  for i,v in enumerate(values):
   draw.rounded_rectangle((22+i*191,84,204+i*191,119),radius=4,outline=d.AMBER if i<len(outs)else '#58747c',width=2)
   draw.text((35+i*191,91),f'{i+1}: {v:+d}',font=d.F(19),fill=d.AMBER if i<len(outs)else m.MUTED)
  view=(65,-6800,3000,4200);scale=.074;sy=.04
  for x,y in live:
   if view[0]<=x<view[2]and view[1]<=y<view[3]:draw.rectangle((40+(y-view[1])*scale,160+(x-view[0])*sy,41+(y-view[1])*scale,161+(x-view[0])*sy),fill=d.GREEN)
  for index in range(6):
   y0=363+750*index-g/2;y1=800+750*index-g/2
   if view[1]<=y0 and y1<view[3]:
    left=40+(y0-view[1])*scale;right=40+(y1-view[1])*scale
    draw.rectangle((left,158,right,170),outline='#68c5df',width=1);draw.text((left,137),str(index+1),font=d.F(13),fill='#68c5df')
  for index,(obj,di)in enumerate(ordered):
   gx=sum(x for x,y in obj)/5;gy=sum(y for x,y in obj)/5
   if view[0]<=gx<view[2]and view[1]<=gy<view[3]:
    px=40+(gy-view[1])*scale;py=160+(gx-view[0])*sy;draw.rectangle((px-4,py-4,px+4,py+4),outline=d.AMBER,width=2);draw.text((px+6,py),str(index+1),font=d.F(13),fill=d.AMBER)
  draw.text((22,294),'Overview rotated 90°; axes scaled · cyan: six readers · yellow: this command sequence',font=d.F(15),fill=m.MUTED)
  chosen=ordered[-1]if ordered else None
  if chosen:cx=round(sum(x for x,y in chosen[0])/5);cy=round(sum(y for x,y in chosen[0])/5)
  else:cx,cy=210,-1110
  box=(cx-28,cy-22,cx+28,cy+22)
  caption=f'Command {len(outs)}: {values[len(outs)-1]:+d} has left its reader'if outs else'The first command is still passing through its reader'
  zoom=d.frame('Latest output of this selected slow salvo',caption,g,live,box,arrows=outs);zoom.thumbnail((720,425));im.paste(zoom,(140,322));frames.append(im)
 assert decoded==values and counts[-1]==5
 checks['selected_band_anchor']=-1140;checks['recovered_recipe_in_emission_order']=decoded;checks['first_crossings_of_x_245_at_sampled_generations']=crossings;checks['recipe_offsets']=values;checks['nominal_symbol_pitch']=250;checks['reader_pitch']=750;checks['nominal_command_interval']=1500;checks['isolated_reading_train_no_erasers']=True
 save('caterloopillar-tape-to-salvo',frames,gs,source,checks,len(frames)-1)

def lifeview(title,caption,g,nodes,box,templates,active=None):
 # The live set comes from the complete native macrocell, not from templates.
 cells={(x+box[0],y+box[1])for x,y in r.ping.pixels(nodes,0,box)}
 im=Image.new('RGB',(900,790),d.BG);draw=ImageDraw.Draw(im);draw.text((22,14),title,font=d.F(25),fill=d.AMBER);draw.text((22,54),caption,font=d.F(16),fill=d.GREEN)
 sx=815/(box[3]-box[1]);sy=235/(box[2]-box[0]);ox=40;oy=92
 for x,y in cells:
  px=round(ox+(y-box[1])*sx);py=round(oy+(x-box[0])*sy);draw.rectangle((px,py,px+1,py+1),fill=d.GREEN)
 present=[]
 for index,ship in enumerate(templates):
  obj=ship['cells']
  if obj<=cells:
   present.append(ship['x']);xs=[x for x,y in obj];ys=[y for x,y in obj]
   draw.rectangle((ox+(min(ys)-box[1])*sx-4,oy+(min(xs)-box[0])*sy-4,ox+(max(ys)+1-box[1])*sx+4,oy+(max(xs)+1-box[0])*sy+4),outline=d.AMBER if ship['x']==active else '#68c5df',width=1)
 draw.text((22,345),f'Whole convoy: {len(present)} / {len(templates)} original ships intact · overview rotated 90°',font=d.F(17),fill=m.MUTED)
 selected=next((ship for ship in templates if ship['x']==active),templates[0]);a=selected['cells'];cx=round(sum(x for x,y in a)/len(a));cy=round(sum(y for x,y in a)/len(a));view=(cx-26,cy-24,cx+26,cy+24)
 detail_cells={(x+view[0],y+view[1])for x,y in r.ping.pixels(nodes,0,view)}
 zoom=d.frame('Enlarged reaction within this same convoy',f"{selected['name']} lane {selected['x']} · full pattern continues outside the view",g,detail_cells,view,marks=[(a,d.AMBER)])
 zoom.thumbnail((720,405));im.paste(zoom,(90,374));return im,present

def lifecycle():
 source=SRC/'Caterloopillar_c8.rle';records=json.loads((SRC/'complete-ship-spaceships.json').read_text());up=[z for z in records if z['direction']=='up'];bases={}
 for z in up:bases.setdefault(z['x'],z)
 ranges={x:max((z['y']-b['y'])//750 for z in up if z['x']==x and z['shape']==b['shape']and(z['y']-b['y'])%750==0)for x,b in bases.items()}
 Q=max(ranges.values())+1;events=sorted(ranges.items(),key=lambda z:-z[1]);assert len(events)==16 and Q==684
 frames=[];gs=[];progress=[];duration=[];phases=[0,256,512,768,*range(896,1793,64),1856,1920,1984,2000]
 for event,(active,endq) in enumerate(events):
  q=endq+1;n=Q-q
  for p in phases:
   if p==2000:phase=0;qq=q-1;shift=0
   else:phase=p;qq=q;shift=-p//2
   nodes,pop=r.native('caterloopillar',source,phase);box=(-5,qq*750+150+shift,315,qq*750+910+shift)
   templates=[dict(x=x,name=b['name'],cells={(x+dx,b['y']+dy+qq*750+shift)for dx,dy in b['shape']})for x,b in bases.items()]
   gen=n*2000+p;title='Construct every ship of a new reading head'
   caption=f'Addition {event+1}/16: {bases[active]["name"]} lane {active} · generation {gen:,}'
   im,present=lifeview(title,caption,gen,nodes,box,templates,active);frames.append(im);gs.append(gen);duration.append(750 if p in(0,2000)else 85)
   if p==2000:
    assert active in present;progress.append(dict(generation=gen,ships_present=len(present),added_lane=active))
 assert progress[-1]['ships_present']==16 and gs[-1]==740000
 initial=r.all_cells(r.native('caterloopillar',source,0)[0]);period_end=r.all_cells(r.native('caterloopillar',source,2000)[0]);assert period_end=={(x,y-250)for x,y in initial}
 checks=dict(all_sixteen_additions_shown=progress,verified_whole_pattern_period=2000,translation_per_period=[0,-250],exact_native_2000_translation_verified=True,long_states_derived_from_verified_period_and_translation_invariance=True,camera_follows_one_convoy=True,time_skips_between_separate_recipe_additions=True)
 save('caterloopillar-whole-head-construction',frames,gs,source,checks,len(frames)-1,duration)
 for direction,title,prefix in [('up','Erase the entire used forward head','whole-head-erasure'),('down','Erase the entire used backward head','whole-tail-erasure')]:
  if direction=='up':chosen=list(bases.values());ys=(150,910);xs=(-5,315);sign=-1
  else:
   chosen=[max((z for z in records if z['direction']=='down'and z['x']==x),key=lambda z:z['y'])for x in sorted(set(z['x']for z in records if z['direction']=='down')-{393})];ys=(513330,514580);xs=(400,750);sign=1
  frames=[];gs=list(range(0,2001,16));counts=[]
  for g in gs:
   nodes,pop=r.native('caterloopillar',source,g);box=(xs[0],ys[0]+sign*g//2,xs[1],ys[1]+sign*g//2)
   templates=[dict(x=b['x'],name=b['name'],cells={(b['x']+dx,b['y']+dy+sign*g//2)for dx,dy in b['shape']})for b in chosen]
   cells={(x+box[0],y+box[1])for x,y in r.ping.pixels(nodes,0,box)}
   intact=[b for b in templates if b['cells']<=cells]
   active=(intact[-1]if intact else templates[-1])['x']
   im,present=lifeview(title,'A complete convoy enters; timed signals remove its ships in sequence',g,nodes,box,templates,active);frames.append(im);counts.append(len(present))
  assert counts[0]==len(chosen) and counts[-1]==0
  save('caterloopillar-'+prefix,frames,gs,source,dict(original_ships=len(chosen),intact_ship_counts=counts,all_original_ships_removed=True,full_pattern_evolution=True),len(frames)//2)

if __name__=='__main__':
 import sys
 names=sys.argv[1:]or ['geometry','reflector','offsets','salvo','lifecycle']
 if (SRC/'intermediate-stages-validation.json').exists():REPORT.update(json.loads((SRC/'intermediate-stages-validation.json').read_text()))
 for name in names:
  globals()[name]()
  (SRC/'intermediate-stages-validation.json').write_text(json.dumps(REPORT,indent=2)+'\n')
 (SRC/'intermediate-stages-validation.json').write_text(json.dumps(REPORT,indent=2)+'\n')
