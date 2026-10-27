"""Embeds downloaded marketplace photos. Usage: embed_mk.py <mk dir> <market2.js in> <market2.js out>"""
import sys, json, os, io, base64, re
from PIL import Image
d, src, dst = sys.argv[1:4]
meta = json.load(open(os.path.join(d, 'meta.json')))
ph, cr = {}, {}
rj = os.path.join(d, 'reject.json')
reject = set(json.load(open(rj))) if os.path.exists(rj) else set()
for key, m in meta.items():
    f = os.path.join(d, 'img', key + '.jpg')
    if m.get('none') or key in reject or not os.path.exists(f):
        continue
    im = Image.open(f).convert('RGB')
    kind = key[0]
    tw, th, q = {'s': (420, 260, 60), 'b': (300, 200, 60), 'p': (200, 200, 55)}[kind]
    r = max(tw / im.width, th / im.height)
    im = im.resize((max(tw, round(im.width * r)), max(th, round(im.height * r))), Image.LANCZOS)
    l = (im.width - tw) // 2; t = (im.height - th) // 2
    im = im.crop((l, t, l + tw, t + th))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True)
    ph[key] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    cr[key] = [m.get('artist', ''), m.get('lic', '')]
s = open(src, encoding='utf8').read()
s = re.sub(r'/\*MKPH\*/.*?/\*ENDMKPH\*/', lambda _: '/*MKPH*/const MKPH=' + json.dumps(ph) + ';/*ENDMKPH*/', s, flags=re.S)
s = re.sub(r'/\*MKCR\*/.*?/\*ENDMKCR\*/', lambda _: '/*MKCR*/const MKCR=' + json.dumps(cr) + ';/*ENDMKCR*/', s, flags=re.S)
open(dst, 'w', encoding='utf8').write(s)
print(len(ph), 'photos,', sum(len(v) for v in ph.values()) // 1024, 'KB')
