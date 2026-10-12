"""Illustrate combinatorial placement of actual block/beehive still lifes.
No search results are asserted. Optional Pillow tooling, not needed to build.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
W,H,S=48,24,12
block={(0,0),(1,0),(0,1),(1,1)}
beehive={(1,0),(2,0),(0,1),(3,1),(1,2),(2,2)}
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
frames=[]
for i in range(24):
 im=Image.new('RGB',(576,342),'#102f39');d=ImageDraw.Draw(im)
 for x in range(W+1):d.line((x*S,0,x*S,H*S),fill='#214049')
 for y in range(H+1):d.line((0,y*S,W*S,y*S),fill='#214049')
 # A lexicographic product of placements; all three patterns remain still lifes.
 positions=[(5,5),(15+(i//6)*5,5),(8+(i%6)*6,15)]
 patterns=[block,beehive,block]
 for (px,py),pat in zip(positions,patterns):
  for x,y in pat:d.rectangle(((px+x)*S+1,(py+y)*S+1,(px+x)*S+10,(py+y)*S+10),fill='#a1ddcb')
 d.text((22,309),f'Candidate arrangement {i+1:02d} / 24',font=f,fill='#cfede4')
 frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE,colors=12))
frames[0].save(root/'public/images/catforce-combinations.gif',save_all=True,append_images=frames[1:],duration=450,loop=0,optimize=True)
frames[0].convert('RGB').save(root/'public/images/catforce-combinations-still.png')
