# python3 norm_logged.py raw_dir out_dir — живые копии страниц под логином (outerHTML из браузера) -> фикстуры корпуса:
# без <script>/<noscript>, без #custom_css (там тема владельца аккаунта) и стилей расширений браузера,
# с <base href> на сайт и меткой <!--THEME--> перед </head>, как у snap.js
import re,glob,os,sys
src,dst=sys.argv[1:3];os.makedirs(dst,exist_ok=True)
for f in sorted(glob.glob(os.path.join(src,'*_l_*.html'))):
    h=open(f,encoding='utf-8').read()
    h=re.sub(r'<script\b[^>]*>.*?</script>','',h,flags=re.S|re.I)
    h=re.sub(r'<noscript\b[^>]*>.*?</noscript>','',h,flags=re.S|re.I)
    h=re.sub(r'<style\b[^>]*id="custom_css"[^>]*>.*?</style>','',h,flags=re.S)
    h=re.sub(r'<style\b[^>]*(id="ysTextCssRule"|class="mb-style-tag")[^>]*>.*?</style>','',h,flags=re.S)
    name=os.path.basename(f);origin='https://shikimori.io/' if name.startswith('io_') else 'https://shikimori.rip/'
    if '<base' not in h: h=re.sub(r'<head([^>]*)>',lambda m:'<head%s><base href="%s">'%(m.group(1),origin),h,count=1,flags=re.I)
    if '<!--THEME-->' not in h: h=re.sub(r'</head>','<!--THEME--></head>',h,count=1,flags=re.I)
    if not h.lstrip().lower().startswith('<!doctype'): h='<!DOCTYPE html>\n'+h
    open(os.path.join(dst,name),'w',encoding='utf-8').write(h);print(name,len(h))
