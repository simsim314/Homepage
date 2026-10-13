"""Show actual two-arm construction through a completed new head, using Golly.

Render source cells in a fixed view containing the parent, construction arms,
and new head. Cell marks are enlarged for readability; no circuitry is drawn
between them. Original instruction streams continue beyond the displayed crop.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import importlib.util,subprocess,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gallery',ROOT/'scripts/render-ca-gallery.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
CACHE=Path('/tmp/homepage-head-construction');CACHE.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def stable_head(name):
    view=(0,0,2400,1000) if name=='serizawa' else (0,0,219,110)
    phases=[]
    for g in [0,128,256,384,480]:
        prefix='serizawa-geminoid-circuit' if name=='serizawa' else 'geminoid-particles-construction'
        p=r.snapshot(prefix,r.SRC/('SerizawaGeminoid.rle' if name=='serizawa' else 'GeminoidParticles.rle'),g,True)
        c,a=r.state_cells(p,view,1)
        phases.append({p:s for p,s in c.items() if s==1} if name=='serizawa' else {p:s for p,s in c.items() if s>=5})
    return {p:s for p,s in phases[0].items() if all(c.get(p)==s for c in phases)}

def make(name):
    ser=name=='serizawa'
    source=r.SRC/('SerizawaGeminoid.rle' if ser else 'GeminoidParticles.rle')
    view=(-120,-3360,4860,1500) if ser else (-20,-155,390,155)
    step=131072 if ser else 192
    end=16777216 if ser else 24576
    samples=list(range(0,end+1,step))
    offset=(2444,-3219) if ser else (148,-112)
    base=stable_head(name)
    frames=[];records=[];first_complete=None
    previous=r.CACHE/('serizawa-geminoid-circuit-0.mc' if ser else 'geminoid-particles-construction-0.mc')
    title=ImageFont.truetype(FONT,25);font=ImageFont.truetype(FONT,17);small=ImageFont.truetype(FONT,14)
    for i,g in enumerate(samples):
        path=CACHE/f'{name}-{g}.mc'
        if g==0:path=previous
        elif not path.exists():
            subprocess.run(['bgolly','-a','RuleLoader','-s',str(r.SRC)+'/', '-q','-q','-m',str(g),'-i',str(step),'-M','1536','-T','40','-o',str(path),str(previous)],check=True,timeout=48,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            if not path.exists():raise RuntimeError(f'Golly did not finish {name} generation {g}')
        cells,actual=r.state_cells(path,view,1)
        assert actual==g
        previous=path
        child={(x+offset[0],y+offset[1]):s for (x,y),s in base.items()}
        matches=sum(cells.get((x-view[0],y-view[1]))==s for (x,y),s in child.items())
        if matches==len(base) and first_complete is None:first_complete=g
        # Preserve aspect ratio, use the full frame, and enlarge the marks.
        factor=min(744/(view[2]-view[0]),500/(view[3]-view[1]))
        ox=400-(view[2]-view[0])*factor/2;oy=95
        def point(x,y):return(ox+(x-view[0])*factor,oy+(y-view[1])*factor)
        im=Image.new('RGB',(800,660),'#102f39');d=ImageDraw.Draw(im)
        d.text((22,16),'Two construction arms build a new head',font=title,fill='#efbf61')
        subtitle='The completed head takes over.' if first_complete is not None else 'Watch the new circuitry appear above the parent.'
        d.text((22,53),subtitle,font=font,fill='#cce5dc')
        # Exact stable head extents give visual orientation, not imaginary wires.
        boxes=[((0,0,2200,1000) if ser else (0,0,219,110),'Parent head','#82b6ac'),
               ((2444,-3219,4644,-2219) if ser else (148,-112,367,-2),'New head','#efbf61')]
        for (x0,y0,x1,y1),label,color in boxes:
            a=point(x0,y0);b=point(x1,y1)
            d.rounded_rectangle((a[0]-8,a[1]-8,b[0]+8,b[1]+8),radius=8,outline=color,width=1)
            d.text((a[0],a[1]-31),label,font=font,fill=color)
        for (x,y),state in cells.items():
            px,py=point(x+view[0],y+view[1])
            if not (20<px<780 and 85<py<600):continue
            radius=1.7 if ser else 2
            color=r.PALETTE[state]
            if ser and state==2:color='#efbf61';radius=2.2
            d.ellipse((px-radius,py-radius,px+radius,py+radius),fill=color)
        d.text((22,613),f'Golly · {"Serizawa" if ser else "Geminoid Particles"} · generation {g:,}',font=font,fill='#cce5dc')
        d.text((22,639),'Actual cells, enlarged marks · fixed view · accelerated construction playback',font=small,fill='#89afa2')
        frames.append(im);records.append({'generation':g,'stable_head_matches':matches,'stable_head_reference_cells':len(base)})
        if i%16==0:print(name,i+1,len(samples),g,matches,len(base),flush=True)
    assert first_complete is not None, f'{name}: new head must be completed, not merely started'
    # Independent full-source snapshot comparison at a useful checkpoint.
    check_g=8388608 if ser else 18432
    cached=CACHE/f'{name}-{check_g}.mc'
    fresh=Path('/tmp/serizawa-8388608.mc') if ser else Path('/tmp/particles-18432.mc')
    if not fresh.exists():fresh=r.snapshot(name+'-head-full-check',source,check_g,True)
    a,ga=r.state_cells(cached,view,1);b,gb=r.state_cells(fresh,view,1)
    assert ga==gb==check_g and a==b
    slug='serizawa-geminoid-building' if ser else 'geminoid-particles-building'
    dest=ROOT/'public/images'/f'{slug}.gif'
    durations=[180]*len(frames);durations[0]=1200;durations[-1]=2200
    complete_i=samples.index(first_complete);durations[complete_i]=1500
    frames[0].save(dest,save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=True)
    frames[complete_i].save(dest.with_name(dest.stem+'-still.png'))
    report={'engine':'Golly 3.3 / RuleLoader','source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'rule':'Serizawa' if ser else 'GeminoidParticles','generations':[0,end],'viewport':view,'dimensions':[800,660],'first_complete_stable_head':first_complete,'head_translation':offset,'reference':'Head cells stable across generations 0,128,256,384,480; exact states match at the reported translated location. This checks the head region at its initial phase; startup targets can move once the new head operates. Long input tapes are not part of this check.','full_source_comparison_generation':check_g,'full_source_comparison':'All displayed cell states agree with independent full-source Golly evolution.','rendering':'Fixed framing; exact cells with enlarged circular marks; boxes label head regions. No invented connecting circuitry.','frames':records}
    (r.SRC/f'{slug}-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(dest,'completed head at',first_complete,flush=True)

if __name__=='__main__':make(sys.argv[1])
