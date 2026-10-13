"""Synchronized views of both ends and the tape, from original Golly states."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from functools import lru_cache
import importlib.util,json,subprocess,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('heads',ROOT/'scripts/render-geminoid-heads.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
r=h.r;CACHE=h.CACHE
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def read_nodes(path):
    nodes=[None]
    for line in path.read_text().splitlines():
        if line and not line.startswith(('[','#')):
            d=list(map(int,line.split()));nodes.append((d[0],d[1:]))
    return nodes

def tape_pixels(nodes,view,width,height):
    """Exact occupancy under explicitly different horizontal/vertical scales."""
    lit=set()
    def project(x,y):return(int((x-view[0])*width/(view[2]-view[0])),int((y-view[1])*height/(view[3]-view[1])))
    @lru_cache(None)
    def columns(i):
        if not i:return frozenset()
        level,data=nodes[i]
        if level==1:return frozenset(dx for state,dx in zip(data,[0,1,0,1]) if state)
        half=2**(level-1)
        return frozenset(x+dx for child,dx in zip(data,[0,half,0,half]) for x in columns(child))
    def visit(i,x,y):
        if not i:return
        level,data=nodes[i];size=2**level
        if x+size<=view[0] or y+size<=view[1] or x>=view[2] or y>=view[3]:return
        a=project(x,y);b=project(x+size-1,y+size-1)
        if a[1]==b[1] and y>=view[1] and y+size<=view[3]:
            if 0<=a[1]<height:
                for cx in columns(i):
                    if view[0]<=x+cx<view[2]:lit.add((project(x+cx,y)[0],a[1]))
            return
        if a==b:
            if 0<=a[0]<width and 0<=a[1]<height:lit.add(a)
            return
        if level==1:
            for s,(dx,dy) in zip(data,[(0,0),(1,0),(0,1),(1,1)]):
                if s and view[0]<=x+dx<view[2] and view[1]<=y+dy<view[3]:lit.add(project(x+dx,y+dy))
        else:
            half=size//2
            for j,(dx,dy) in zip(data,[(0,0),(half,0),(0,half),(half,half)]):visit(j,x+dx,y+dy)
    half=2**(nodes[-1][0]-1);visit(len(nodes)-1,-half,1-half)
    return lit

def make(name):
    ser=name=='serizawa';source=r.SRC/('SerizawaGeminoid.rle' if ser else 'GeminoidParticles.rle')
    step=262144 if ser else 384;end=25165824 if ser else 49152
    offset=(2444,-3219) if ser else (148,-112)
    second=(1716,3338237) if ser else (75,9002)
    base=h.stable_head(name)
    if ser:
        # Reference head circuitry excludes startup targets and signal cells
        # that do not stay fixed in the operating parent.
        working=Path('/tmp/serizawa-8388608.mc')
        if not working.exists():working=r.snapshot('serizawa-head-full-check',source,8388608,True)
        parent,_=r.state_cells(working,(0,0,2400,1000),1)
        base={p:s for p,s in base.items() if parent.get(p)==s}
    tape_view=(-500,-10000,9000,7000000) if ser else (-25,-500,750,18500)
    frames=[];records=[];complete=[None,None]
    previous=CACHE/f'{name}-0.mc'
    if not previous.exists():previous=r.CACHE/('serizawa-geminoid-circuit-0.mc' if ser else 'geminoid-particles-construction-0.mc')
    title=ImageFont.truetype(FONT,25);font=ImageFont.truetype(FONT,17);small=ImageFont.truetype(FONT,14)
    for i,g in enumerate(range(0,end+1,step)):
        p=CACHE/f'{name}-{g}.mc'
        if g==0:p=previous
        elif not p.exists():
            subprocess.run(['bgolly','-a','RuleLoader','-s',str(r.SRC)+'/','-q','-q','-m',str(g),'-i',str(step),'-M','1536','-T','40','-o',str(p),str(previous)],check=True,timeout=48,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            if not p.exists():raise RuntimeError(f'Golly did not finish {name} {g}')
        previous=p
        nodes=read_nodes(p)
        im=Image.new('RGB',(1100,760),'#102f39');d=ImageDraw.Draw(im)
        d.text((22,15),'Two ends, one instruction tape',font=title,fill='#efbf61')
        d.text((22,53),'Push / pull move the arm targets; shoot sends construction signals.',font=font,fill='#cce5dc')
        d.text((22,96),'The whole pattern',font=font,fill='#efbf61')
        d.text((22,122),'Tape height compressed',font=small,fill='#89afa2')
        for x,y in tape_pixels(nodes,tape_view,180,520):
            d.rectangle((22+x,155+y,23+x,156+y),fill='#b5e8d1')
        d.line((220,95,220,686),fill='#35616a',width=1)
        checks=[];views=[];arm_records=[]
        for j,(anchor,label) in enumerate([((0,0),'Upper end'),(second,'Lower end')]):
            original_x,original_y=anchor
            period=13362290 if ser else 18092
            delay=1048576 if ser else 2304
            owner=0 if complete[j] is None or g<complete[j]+delay else 1+(g-complete[j]-delay)//period
            ox=original_x+owner*offset[0];oy=original_y+owner*offset[1]
            local=(-120,-3360,4860,1500) if ser else (-20,-155,390,155)
            px0=250+j*425;py0=175
            d.text((px0,100),label,font=font,fill='#efbf61')
            if owner:d.text((px0,128),f'Following head {owner+1}',font=small,fill='#89afa2')
            else:d.text((px0,128),'First construction cycle',font=small,fill='#89afa2')
            factor=min(400/(local[2]-local[0]),480/(local[3]-local[1]))
            def project(x,y):return(px0+(x-ox-local[0])*factor,py0+(y-oy-local[1])*factor)
            view=(local[0]+ox,local[1]+oy,local[2]+ox,local[3]+oy)
            c,actual=r.state_cells(p,view,1);assert actual==g
            check=sum(c.get((x+original_x+offset[0]-view[0],y+original_y+offset[1]-view[1]))==state for (x,y),state in base.items())
            if check==len(base) and complete[j] is None:complete[j]=g
            checks.append(check);views.append(view)
            boxes=[((0,0,2200,1000) if ser else (0,0,219,110),'Operating head','#82b6ac'),
                   ((2444,-3219,4644,-2219) if ser else (148,-112,367,-2),'New head','#efbf61')]
            for (x0,y0,x1,y1),label2,col in boxes:
                aa=project(x0+ox,y0+oy);bb=project(x1+ox,y1+oy)
                d.rounded_rectangle((aa[0]-5,aa[1]-5,bb[0]+5,bb[1]+5),radius=6,outline=col,width=1)
                d.text((aa[0],aa[1]-21),label2,font=small,fill=col)
            for (x,y),state in c.items():
                px,py=project(x+view[0],y+view[1])
                if px0<px<px0+400 and py0<py<py0+480:
                    rad=1.6;col=r.PALETTE[state]
                    if ser and state==2:rad=1.8;col='#efbf61'
                    if not ser and state==7:rad=3.1;col='#a0d5f2'
                    d.ellipse((px-rad,py-rad,px+rad,py+rad),fill=col)
            targets=[]
            if ser:
                def isolated(x,y):return all((x+dx,y+dy) not in c for dx in range(-2,3) for dy in range(-2,3) if dx or dy)
                vertical=[];horizontal=[]
                for (x,y),state in c.items():
                    wx,wy=x+view[0],y+view[1]
                    if state!=1:continue
                    if wx==ox+516 and wy<=oy+175 and isolated(x,y):vertical.append((wx,wy))
                    if wy==oy+878 and wx>=ox+2152 and isolated(x,y):horizontal.append((wx,wy))
                for candidates,label2 in [(vertical,'Arm 1'),(horizontal,'Arm 2')]:
                    if not candidates:continue
                    wx,wy=min(candidates,key=lambda point:point[1]) if label2=='Arm 1' else max(candidates)
                    px,py=project(wx,wy)
                    if px0+5<px<px0+385 and py0+5<py<py0+465:
                        d.ellipse((px-6,py-6,px+6,py+6),outline='#efbf61',width=2)
                        d.text((px+9,py-8),label2,font=small,fill='#efbf61');targets.append([wx,wy])
            arm_records.append(targets)
            d.text((px0,651),'Amber rings: arm targets' if ser else 'Blue: movable construction blocks',font=small,fill='#89afa2')
        subtitle='Both ends have built their next heads.' if all(v is not None for v in complete) else 'Both ends are building: watch the circuitry and returning tape.'
        d.text((250,681),subtitle,font=font,fill='#cce5dc')
        d.text((22,719),f'Golly · {"Serizawa" if ser else "Geminoid Particles"} · generation {g:,}',font=font,fill='#cce5dc')
        d.text((22,744),'Actual cells enlarged · views follow successive heads · accelerated playback',font=small,fill='#89afa2')
        frames.append(im);records.append({'generation':g,'head_matches':checks,'reference_cells':len(base),'end_views':views,'actual_arm_target_cells':arm_records})
        if i%16==0:print(name,'both ends',i+1,g,checks,len(base),flush=True)
    assert all(v is not None for v in complete), 'Both ends must finish their head circuitry'
    slug='serizawa-geminoid-whole' if ser else 'geminoid-particles-whole'
    dest=ROOT/'public/images'/f'{slug}.gif';dur=[200]*len(frames);dur[0]=1500;dur[-1]=2400
    hold=max(complete);index=next(i for i,r in enumerate(records) if r['generation']==hold);dur[index]=1800
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=dur,loop=0,disposal=2,optimize=True)
    frames[index].save(dest.with_name(dest.stem+'-still.png'))
    report={'source':str(source.relative_to(ROOT)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'engine':'Golly 3.3 / RuleLoader','rule':'Serizawa' if ser else 'GeminoidParticles','dimensions':[1100,760],'generations':[0,end],'second_end_anchor':second,'head_translation':offset,'first_completed_head_circuitry_at_each_end':complete,'reference_cells':len(base),'validation':'Exact source states at both translated head regions match the original fixed circuitry; Serizawa excludes startup targets/transient signal cells by comparing the operating parent. Full-pattern states, not clipped simulations.','tape_view':tape_view,'tape_rendering':'Exact occupied pixels with independently scaled axes. Height is explicitly compressed; cells enlarged. End panels preserve upright geometry and follow successive heads, sharing the same generation.','frames':records}
    (r.SRC/f'{slug}-check.json').write_text(json.dumps(report,indent=2)+'\n');print(dest,'both completed',complete,flush=True)

if __name__=='__main__':make(sys.argv[1])
