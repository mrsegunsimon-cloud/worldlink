"""Menu: photo tiles for Learn how / Play zone / Emergency; Video Call and Stories move to Inbox. Usage: patch_menu.py in out"""
import sys,base64,urllib.parse
src,dst=sys.argv[1:3]
s=open(src,encoding='utf8').read()
if 'const PHX=' in s:
    open(dst,'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
casino='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"><defs><radialGradient id="g" cx=".5" cy=".4" r=".8"><stop offset="0" stop-color="#1b8a5a"/><stop offset="1" stop-color="#06271a"/></radialGradient></defs><rect width="400" height="240" fill="url(#g)"/><g><rect x="95" y="40" width="210" height="130" rx="18" fill="#c0262d" stroke="#ffd34d" stroke-width="6"/><rect x="115" y="62" width="170" height="70" rx="8" fill="#fff"/><g font-family="Arial Black,sans-serif" font-size="52" font-weight="900" fill="#d11" text-anchor="middle"><text x="145" y="115">7</text><text x="200" y="115">7</text><text x="255" y="115">7</text></g><circle cx="200" cy="152" r="7" fill="#ffd34d"/><rect x="318" y="60" width="9" height="60" rx="4" fill="#ddd"/><circle cx="322" cy="56" r="12" fill="#e11"/></g><g><circle cx="52" cy="190" r="30" fill="#e11" stroke="#fff" stroke-width="5" stroke-dasharray="10 8"/><circle cx="92" cy="208" r="26" fill="#1E6FFF" stroke="#fff" stroke-width="5" stroke-dasharray="9 7"/><circle cx="352" cy="200" r="30" fill="#111" stroke="#ffd34d" stroke-width="5" stroke-dasharray="10 8"/><rect x="300" y="170" width="44" height="44" rx="8" fill="#fff" transform="rotate(14 322 192)"/><g fill="#111" transform="rotate(14 322 192)"><circle cx="311" cy="181" r="4"/><circle cx="333" cy="181" r="4"/><circle cx="322" cy="192" r="4"/><circle cx="311" cy="203" r="4"/><circle cx="333" cy="203" r="4"/></g></g></svg>'''
emerg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 240"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0a12"/><stop offset="1" stop-color="#8a1020"/></linearGradient></defs><rect width="400" height="240" fill="url(#g)"/><g opacity=".35"><path d="M200 70 L20 0 L120 0Z" fill="#ff4d5e"/><path d="M200 70 L380 0 L280 0Z" fill="#4d8cff"/></g><rect y="190" width="400" height="50" fill="#1a1a22"/><g><rect x="90" y="100" width="190" height="80" rx="10" fill="#fff"/><path d="M280 115 h40 l24 30 v35 h-64z" fill="#fff"/><path d="M296 125 h20 l14 20 h-34z" fill="#8fd0ff"/><rect x="90" y="140" width="190" height="10" fill="#e11"/><rect x="170" y="108" width="14" height="40" fill="#e11" transform="translate(-6 -8)"/><rect x="157" y="121" width="40" height="14" fill="#e11" transform="translate(-6 -8)"/><rect x="170" y="86" width="40" height="14" rx="5" fill="#ff3b4d"/><rect x="215" y="86" width="40" height="14" rx="5" fill="#2f7bff"/><circle cx="130" cy="182" r="20" fill="#222" stroke="#999" stroke-width="5"/><circle cx="310" cy="182" r="20" fill="#222" stroke="#999" stroke-width="5"/></g></svg>'''
def uri(x): return 'data:image/svg+xml;charset=utf-8,'+urllib.parse.quote(x)
extra='/*PHX*/const PHX={"pz":"%s","em":"%s"};Object.assign(PH,PHX);\n'%(uri(casino),uri(emerg))
k='/*ENDPH*/'
assert s.count(k)==1
s=s.replace(k,k+'\n'+extra)
rep('const MP0=n=>["Social","Sports","Campus","Entertainment","Market","Explore"].includes(n);','const MP0=n=>["Social","Sports","Campus","Entertainment","Market","Explore","Learn how","Play zone","Video Call"].includes(n);')
rep('Explore:"santorini"};','Explore:"santorini","Learn how":"learning","Play zone":"pz"};')
rep('${t("news","World News","w_world")}${t("lang","Language","l_dict")}</div>','${t("news","World News","w_world")}${t("lang","Language","l_dict")}${t("sos","Emergency","em").replace(\'style="position\',\'style="grid-column:1/-1;position\')}</div>')
rep('<button data-m="stories"><span class="ic">📸</span>Stories</button><button data-m="sos"><span class="ic">🚑</span>Emergency</button><button data-m="theme">','<button data-m="theme">')
open(dst,'w',encoding='utf8').write(s)
