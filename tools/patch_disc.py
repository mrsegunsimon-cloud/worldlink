"""Music Discover tab. Usage: patch_disc.py in out"""
import sys,os
s=open(sys.argv[1],encoding='utf8').read()
if 'function discHtml(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'discover.js'),encoding='utf8').read()
rep(' t=t||"tracks";\n const L={tracks:"🎵 Music",',' t=t||"disc";\n const L={disc:"🌍 Discover",tracks:"🎵 Music",')
rep('let body="";\n if(t==="search")body=musicSearch();','let body="";\n if(t==="disc")body=discHtml();else if(t==="search")body=musicSearch();')
rep(' musicWire(t);wireMedia();',' musicWire(t);wireMedia();if(t==="disc")discWire();')
rep('function music(t){',js+'\nfunction music(t){')
open(sys.argv[2],'w',encoding='utf8').write(s)
