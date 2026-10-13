"""Short native Golly mechanism clips beside the original architecture schematic.

The cover leads with tight insertions in both streams of the complete c/8
ship. Head/tail erasure comes from that same ship; a 2014 one-symbol reader
explains the input chain. All patterns evolve on the full plane.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util, json, hashlib, subprocess

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('head',ROOT/'scripts/render-caterloopillar-reader.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
r=h.r
SRC=ROOT/'research/caterloopillar'; OUT=ROOT/'public/images'
BG='#102f39'; CELL='#b5e8d1'; AMBER='#efbf61'; MUTED='#a0bdb8'
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
TITLE=font(26); BODY=font(20); SMALL=font(16)
STAGES=[
 dict(id='block-to-glider',name='Block → glider',part='Read the stream',text=['A passing spaceship activates a block.', 'The tape symbol becomes a glider signal.'],source='block-reading-head',cache='block-reader',gs=list(range(0,145,4)),view=(0,98,90,158),url='https://conwaylife.com/forums/viewtopic.php?p=14297#p14297'),
 dict(id='block-reflector',name='Reflect the glider',part='Inside the stream reader',text=['More spaceships turn the signal around.', 'One glider returns toward the next block.'],source='block-reading-head',cache='block-reader',gs=list(range(208,281,2)),view=(-35,130,55,190),url='https://conwaylife.com/forums/viewtopic.php?p=14297#p14297'),
 dict(id='glider-to-block',name='Glider → block',part='Restore the tape symbol',text=['The returning glider meets a converter.', 'A new block remains 59 cells farther along.'],source='block-reading-head',cache='block-reader',gs=list(range(272,417,4)),view=(0,155,90,215),url='https://conwaylife.com/forums/viewtopic.php?p=14297#p14297'),
 dict(id='forward-inserter',name='Forward-stream inserter',part='Tight LWSS insertion · actual c/8 ship',text=['The new LWSS forms beside a passing LWSS.', 'Their offsets are only 3 lanes and 9 cells.'],source='Caterloopillar_c8',cache='caterloopillar',gs=list(range(1040,1601,8)),view=(103,433452,193,433542),full_ship=True,old_box=(145,433949,149,433954),direction=-1,offset=(3,-9),url='https://github.com/simsim314/Caterloopilar/blob/master/Caterloopillar_c8.rle'),
 dict(id='backward-inserter',name='Backward-stream inserter',part='Tight MWSS insertion · actual c/8 ship',text=['The opposite stream is built while moving.', 'The MWSS pair differs by 9 lanes and 15 cells.'],source='Caterloopillar_c8',cache='caterloopillar',gs=list(range(800,1401,8)),view=(397,171919,487,172009),full_ship=True,old_box=(445,171961,450,171967),direction=1,offset=(-9,-15),url='https://github.com/simsim314/Caterloopilar/blob/master/Caterloopillar_c8.rle'),
 dict(id='head-deletion',name='Delete the head',part='Used forward reader · actual c/8 ship',text=['Timed signals remove the used front machinery.', 'This close view follows its LWSS pair.'],source='Caterloopillar_c8',cache='caterloopillar',gs=list(range(920,1409,8)),view=(103,-52,193,38),full_ship=True,deletion=True,old_box=(145,449,149,454),direction=-1,camera_x=148,url='https://github.com/simsim314/Caterloopilar/blob/master/Caterloopillar_c8.rle'),
 dict(id='tail-deletion',name='Delete the tail',part='Used backward reader · actual c/8 ship',text=['The other end has its own deletion sequence.', 'Passing ships are removed after doing their work.'],source='Caterloopillar_c8',cache='caterloopillar',gs=list(range(600,1057,8)),view=(409,514565,499,514655),full_ship=True,deletion=True,old_box=(451,514315,455,514320),direction=1,camera_x=454,url='https://github.com/simsim314/Caterloopilar/blob/master/Caterloopillar_c8.rle'),

]

STAGES=STAGES[3:5]+STAGES[:3]+STAGES[5:]

def full_view(stage,g):
 x0,y0,x1,y1=stage['old_box']
 cy=(y0+y1)//2+stage['direction']*g//2
 cx=stage.get('camera_x',148 if stage['id']=='forward-inserter' else 442)
 half=45
 if not stage.get('deletion'):
  begin=1120 if stage['id']=='forward-inserter' else 960
  half=45-round(15*max(0,min(1,(g-begin)/160)))
 return (cx-half,cy-half,cx+half,cy+half)

def native_cells(stage,g):
 if stage.get('full_ship'):
  target=r.gallery.CACHE/f'life-caterloopillar-{g}.mc'
  if not target.exists():
   previous=[(int(p.stem.rsplit('-',1)[1]),p) for p in r.gallery.CACHE.glob('life-caterloopillar-*.mc') if int(p.stem.rsplit('-',1)[1])<g]
   if not previous:
    r.native(stage['cache'],SRC/(stage['source']+'.rle'),g)
   else:
    start,checkpoint=max(previous)
    subprocess.run(['bgolly','-h','-q','-q','-m',str(g),'-i',str(g-start),'-M','512','-o',str(target),str(checkpoint)],check=True,timeout=55,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  nodes,pops,actual=r.ping.read_macrocell(target)
  assert actual==g
  pop=pops[-1]
 else:nodes,pop=r.native(stage['cache'],SRC/(stage['source']+'.rle'),g)
 if stage.get('full_ship'):
  v=full_view(stage,g)
  return {(x+v[0],y+v[1]) for x,y in r.ping.pixels(nodes,0,v)},pop
 return r.all_cells(nodes),pop

def crop(stage,g,cells,size=(680,450)):
 view=stage['view']
 if stage.get('full_ship'):view=full_view(stage,g)
 x0,y0,x1,y1=view
 scale=min(size[0]/(x1-x0),size[1]/(y1-y0))
 im=Image.new('RGB',size,BG);d=ImageDraw.Draw(im)
 dx=(size[0]-(x1-x0)*scale)/2;dy=(size[1]-(y1-y0)*scale)/2
 for x,y in cells:
  if x0<=x<x1 and y0<=y<y1:
   px=round(dx+(x-x0)*scale);py=round(dy+(y-y0)*scale)
   d.rectangle((px,py,round(dx+(x+1-x0)*scale)-1,round(dy+(y+1-y0)*scale)-1),fill=CELL)
 if stage.get('full_ship'):
  old={(x,y+stage['direction']*g//2) for x,y in stage['reference_ship']}
  objects=[(old,'#68c5df')]
  if not stage.get('deletion'):
   objects.append(({(x+stage['offset'][0],y+stage['offset'][1]) for x,y in old},AMBER))
  for obj,color in objects:
   if obj<=cells:
    bx0=min(x for x,y in obj);by0=min(y for x,y in obj);bx1=max(x for x,y in obj)+1;by1=max(y for x,y in obj)+1
    d.rectangle((round(dx+(bx0-x0)*scale)-5,round(dy+(by0-y0)*scale)-5,round(dx+(bx1-x0)*scale)+4,round(dy+(by1-y0)*scale)+4),outline=color,width=2)
 return im,view

def validate(stage):
 if stage.get('full_ship'):
  original,_=native_cells(stage,0)
  x0,y0,x1,y1=stage['old_box']
  old={(x,y) for x,y in original if x0<=x<x1 and y0<=y<y1}
  assert len(old)==(11 if stage['id']=='backward-inserter' else 12)
  stage['reference_ship']=old
  if stage.get('deletion'):
   first,_=native_cells(stage,stage['gs'][0]);g=stage['gs'][0]
   assert {(x,y+stage['direction']*g//2) for x,y in old}<=first
   final,_=native_cells(stage,stage['gs'][-1]);assert not final
   return {'whole_pattern':'Original complete c/8 ship, full-plane Golly evolution','original_ship_present_at_start':True,'display_region_empty_at_end':True,'generations':[stage['gs'][0],stage['gs'][-1]]}
  g=stage['gs'][-1];actual,_=native_cells(stage,g)
  moved={(x,y+stage['direction']*g//2) for x,y in old}
  new={(x+stage['offset'][0],y+stage['offset'][1]) for x,y in moved}
  assert moved<=actual and new<=actual
  assert not {(x+stage['offset'][0],y+stage['offset'][1]) for x,y in old}<=original
  # Independent Life verifies the identified ships and their local motion.
  for name,ship in [('old',moved),('new',new)]:
   evolved=set(ship)
   for _ in range(4):evolved=r.sparse_step(evolved)
   assert evolved=={(x,y+stage['direction']*2) for x,y in ship}
   later,_=native_cells(stage,g+4);assert evolved<=later
  return {'whole_pattern':'Original complete c/8 ship, full-plane Golly evolution',
          'existing_ship_preserved':True,'new_ship_exact_match':True,
          'relative_offset':stage['offset'],'ship_cells':len(old),
          'independent_four_generation_motion':True,'final_generation':g}
 source=SRC/(stage['source']+'.rle')
 live=r.rle_cells(source)
 points={0,stage['gs'][0],stage['gs'][-1]};checks={}
 for g in range(max(points)+1):
  if g in points:
   actual,pop=native_cells(stage,g);assert actual==live,(stage['id'],g)
   checks[g]={'population':pop,'independent_sparse_match':True}
  live=r.sparse_step(live)
 if stage['id']=='glider-to-block':
  native,_=native_cells(stage,416)
  original=r.rle_cells(source);block={(42+dx,130+dy) for dx in (0,1) for dy in (0,1)}
  shifted={(x,y+59) for x,y in block};convoy={(x,y+208) for x,y in original-block}
  assert shifted<=native and convoy<=native and len(native-convoy-shifted)==5
  checks['output']={'block_displacement':[0,59],'original_convoy_intact':True,'extra_output_glider_cells':5}
 return checks

def save_gif(path,frames,durations):
 # A shared palette keeps the static diagram identical, so GIF frames need
 # encode only the changing right panel. Save atomically for the dev server.
 palette=frames[0].quantize(colors=96,method=Image.Quantize.FASTOCTREE)
 encoded=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
 temp=Path('/tmp')/path.name
 encoded[0].save(temp,save_all=True,append_images=encoded[1:],duration=durations,loop=0,disposal=1,optimize=False)
 temp.replace(path)

def main():
 diagram=Image.open(OUT/'caterloopillar-architecture.png').convert('RGB')
 diagram.thumbnail((310,624),Image.Resampling.LANCZOS)
 base=Image.new('RGB',(1100,760),BG);d=ImageDraw.Draw(base)
 d.rounded_rectangle((16,66,346,710),radius=8,fill='white')
 base.paste(diagram,(181-diagram.width//2,74))
 d.text((24,20),'Caterloopillar',font=TITLE,fill=CELL)
 d.text((24,724),'Architecture: dvgrn · LifeWiki · GFDL 1.2',font=font(13),fill=MUTED)
 d.line((362,16,362,742),fill='#35505a',width=1)
 frames=[];durations=[];report=[]
 for index,stage in enumerate(STAGES):
  checks=validate(stage);details=[];views=[]
  for k,g in enumerate(stage['gs']):
   cells,pop=native_cells(stage,g);panel,view=crop(stage,g,cells)
   frame=base.copy();d=ImageDraw.Draw(frame)
   d.text((390,22),f"{index+1}/{len(STAGES)} · {stage['name']}",font=TITLE,fill=AMBER)
   d.text((390,62),stage['part'],font=BODY,fill=CELL)
   for j,line in enumerate(stage['text']):d.text((390,105+29*j),line,font=BODY,fill=CELL)
   frame.paste(panel,(390,186))
   d.text((390,654),f'Generation {g:,} · native Life simulation',font=SMALL,fill=MUTED)
   d.text((390,685),('Cyan: existing ship · amber: inserted ship' if not stage.get('deletion') else 'Close view of used reading-head machinery') if stage.get('full_ship') else 'Original forum patterns · enlarged mechanism examples',font=font(14),fill=MUTED)
   for j in range(len(STAGES)):
    d.rounded_rectangle((390+j*96,725,476+j*96,729),radius=2,fill=AMBER if j==index else '#35505a')
   frames.append(frame)
   durations.append(600 if k in (0,len(stage['gs'])-1) else 80)
   detail=Image.new('RGB',(800,620),BG);dd=ImageDraw.Draw(detail)
   dd.text((25,15),stage['name'],font=TITLE,fill=AMBER)
   for j,line in enumerate(stage['text']):dd.text((25,55+j*27),line,font=BODY,fill=CELL)
   detail.paste(panel,(60,123));dd.text((25,590),f'Generation {g:,} · original pattern in Golly · loop resets',font=SMALL,fill=MUTED)
   details.append(detail);views.append({'generation':g,'view':view,'population':pop})
  name='caterloopillar-'+stage['id']
  save_gif(OUT/(name+'.gif'),details,durations[-len(details):])
  still_g={'block-to-glider':0,'block-reflector':240,'glider-to-block':400,'forward-inserter':1440,'backward-inserter':1000,'head-deletion':1120,'tail-deletion':800}[stage['id']]
  details[min(range(len(details)),key=lambda k:abs(stage['gs'][k]-still_g))].save(OUT/(name+'-still.png'))
  report.append({'id':stage['id'],'source_file':str((SRC/(stage['source']+'.rle')).relative_to(ROOT)),'source':stage['url'],'sha256':hashlib.sha256((SRC/(stage['source']+'.rle')).read_bytes()).hexdigest(),'checks':checks,'frames':views})
  print(stage['id'],len(details),'frames checked',flush=True)
 save_gif(OUT/'caterloopillar-mechanisms.gif',frames,durations)
 frames[min(range(len(STAGES[0]['gs'])),key=lambda k:abs(STAGES[0]['gs'][k]-1280))].save(OUT/'caterloopillar-mechanisms-still.png')
 (SRC/'mechanisms-animation-check.json').write_text(json.dumps({'engine':'Golly 3.3 / HashLife','rule':'B3/S23','dimensions':[1100,760],'detail_dimensions':[800,620],'full_plane_simulation':True,'stages':report},indent=2)+'\n')

if __name__=='__main__':main()
