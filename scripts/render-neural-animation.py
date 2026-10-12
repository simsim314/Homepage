"""Animate actual ONNX outputs retained in docs/neural-ca-example.json."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/neural-ca-example.json').read_text())
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
frames=[]
for sample in data['samples']:
 im=Image.new('RGB',(360,360),'#102f39');d=ImageDraw.Draw(im)
 digit=Image.new('L',(28,28));digit.putdata([round(max(0,min(1,v))*255) for v in sample['pixels']])
 digit=digit.resize((252,252),Image.Resampling.NEAREST);im.paste(digit,(54,26));d.text((54,305),sample['label'],fill='#cfede4',font=f)
 frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE,colors=64))
frames[0].save(root/'public/images/neural-ca-evolution.gif',save_all=True,append_images=frames[1:],duration=900,loop=0,optimize=True)
frames[0].convert('RGB').save(root/'public/images/neural-ca-evolution-still.png')
