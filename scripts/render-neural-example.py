"""Render saved, genuine ONNX intermediate outputs; optional Pillow tooling."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/neural-ca-example.json').read_text())
canvas=Image.new('RGB',(828,204),'#102f39');draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for i,sample in enumerate(data['samples']):
    im=Image.new('L',(28,28));im.putdata([round(max(0,min(1,v))*255) for v in sample['pixels']]);im=im.resize((112,112),Image.Resampling.NEAREST)
    canvas.paste(im,(28+i*132,34));draw.text((28+i*132,162),sample['label'],fill='#cfede4',font=font)
canvas.save(root/'src/assets/images/neural-ca-evolution.png')
print('Rendered actual ONNX states, one input and five model steps.')
