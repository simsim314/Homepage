"""Render a static, syntax-colored LifeAPI example without UI/scrollbars."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
im=Image.new('RGB',(640,360),'#102f39');d=ImageDraw.Draw(im)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',28)
lines=[[("New",'#d2a8ff'),('();','#cfede4')],[("char",'#ff7b72'),(' rle[] = ','#cfede4'),('"bo$2bo$3o!"','#a5d6ff'),(';','#cfede4')],[("LifeState",'#79c0ff'),('* state =','#cfede4')],[('    NewState','#d2a8ff'),('(rle);','#cfede4')],[('Evolve','#d2a8ff'),('(state, ','#cfede4'),('4','#79c0ff'),(');','#cfede4')],[('PrintRLE','#d2a8ff'),('(state);','#cfede4')]]
for i,line in enumerate(lines):
 x=40
 for s,color in line:d.text((x,48+i*42),s,font=f,fill=color);x+=d.textlength(s,font=f)
im.save(root/'src/assets/images/lifeapi-code.png')
