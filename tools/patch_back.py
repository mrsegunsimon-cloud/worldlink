"""Back arrow (to the main menu) on every screen opened from the menu. Usage: patch_back.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'id="sxb"' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep('function open(h){','let FM=false;\nfunction open(h){')
rep('''$("#panel").innerHTML=secFull?`<button class="sx" id="sxc" aria-label="Close">✕</button>`+h:h;''','''$("#panel").innerHTML=secFull?`<button class="sx" id="sxc" aria-label="Close">✕</button>${FM?`<button class="sx sb" id="sxb" aria-label="Back to menu">←</button>`:""}`+h:h;''')
rep('$("#sxc").onclick=close;','$("#sxc").onclick=close;const sb=$("#sxb");if(sb)sb.onclick=()=>{FM=false;secFull=false;$("#menu").click()};')
rep('function close(){secFull=false;','function close(){FM=false;secFull=false;')
rep('$("#menu").onclick=()=>{\n open(','$("#menu").onclick=()=>{FM=false;\n open(')
rep('const k=b.dataset.m;if(k!=="theme")secFull=true;','const k=b.dataset.m;if(k!=="theme"){secFull=true;FM=true}')
rep('.sx{position:sticky;','.sb{float:left!important;margin:0 8px 6px 0!important}\n.sx{position:sticky;')
open(sys.argv[2],'w',encoding='utf8').write(s)
