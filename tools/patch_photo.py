"""News cards show the story photo with a slow zoom. Usage: patch_photo.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if '.nimg{' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('const g=GRAD[hsh(n[1])%GRAD.length],ph=sportPh(kind,n),em=kind==="w"?worldEmoji(n[1],n[0]):sportEmoji(n[0]+" "+n[1]);return `<section data-ns="${kind}${i}" style="height:100%;',
    'const g=GRAD[hsh(n[1])%GRAD.length],ph=sportPh(kind,n),em=kind==="w"?worldEmoji(n[1],n[0]):sportEmoji(n[0]+" "+n[1]),im=n[5]&&/^https:\\/\\//.test(n[5])?n[5]:"";return `<section data-ns="${kind}${i}" style="isolation:isolate;height:100%;')
rep('${ph&&PH[ph]?"":`<div style="position:absolute;top:8%;left:0;right:0;text-align:center;font-size:110px">${em}</div>`}',
    '${im?`<div class="nimg" style="background-image:linear-gradient(rgba(0,0,0,.05) 25%,rgba(0,0,0,.82)),url(&quot;${esc(im)}&quot;)"></div>`:ph&&PH[ph]?"":`<div style="position:absolute;top:8%;left:0;right:0;text-align:center;font-size:110px">${em}</div>`}')
rep(':cover(tl,em,Math.round(innerHeight*.34),lab,sportPh(key&&key[0],n))}',
    ':(n[5]&&/^https:\\/\\//.test(n[5])?`<img src="${esc(n[5])}" alt="" referrerpolicy="no-referrer" style="width:100%;border-radius:14px;max-height:34vh;object-fit:cover;background:#111">`:cover(tl,em,Math.round(innerHeight*.34),lab,sportPh(key&&key[0],n)))}')
rep('</style>','.nimg{position:absolute;inset:-6%;z-index:-1;background-size:cover;background-position:center;animation:nz 16s ease-in-out infinite alternate}@keyframes nz{from{transform:scale(1)}to{transform:scale(1.12) translate(-1.5%,-1%)}}@media(prefers-reduced-motion:reduce){.nimg{animation:none}}</style>') if s.count('</style>')==1 else None
if '.nimg{' not in s:
    i=s.rfind('</style>');s=s[:i]+'.nimg{position:absolute;inset:-6%;z-index:-1;background-size:cover;background-position:center;animation:nz 16s ease-in-out infinite alternate}@keyframes nz{from{transform:scale(1)}to{transform:scale(1.12) translate(-1.5%,-1%)}}@media(prefers-reduced-motion:reduce){.nimg{animation:none}}'+s[i:]
open(sys.argv[2],'w',encoding='utf8').write(s)
