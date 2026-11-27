# python3 strip.py out.png frame1.png frame2.png ...  — кадры в одну полосу слева направо (подписи — время из имени)
import sys,re
from PIL import Image,ImageDraw
fs=sys.argv[2:];ims=[Image.open(f).convert('RGB') for f in fs]
h=max(i.height for i in ims)+18;w=sum(i.width for i in ims)+6*(len(ims)-1)
o=Image.new('RGB',(w,h),(255,255,255));d=ImageDraw.Draw(o);x=0
for f,i in zip(fs,ims):
    o.paste(i,(x,18));d.text((x+4,3),re.search(r'(\d+)ms',f).group(1)+' ms',fill=(0,0,0));x+=i.width+6
o.save(sys.argv[1])
