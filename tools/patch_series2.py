import sys,os
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlSeries2" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"series.js"),encoding="utf8").read()
i=s.index("/*wlSeries1*/");j=s.index("\nfunction newPhotoPost(){")
s=s[:i]+js+s[j:]
# editor hook for the series trim
rep('$("#ebk").onclick=()=>{dead=true;vedit(f)};','$("#ebk").onclick=()=>{dead=true;if(window.__edHook){const h=window.__edHook;window.__edHook=null;return h.cancel()}vedit(f)};')
rep(' if(!du)return;dead=true;\n  if(!sh&&st<.05&&en>=du-.05){VTRIM=null;vedit(f);return}',' if(!du)return;dead=true;\n  if(window.__edHook){const h=window.__edHook;window.__edHook=null;return h.done({st,en,sh,pos,full:!sh&&st<.05&&en>=du-.05})}\n  if(!sh&&st<.05&&en>=du-.05){VTRIM=null;vedit(f);return}')
# gifts remember which series
rep('.set({to:c.uid,from:me.uid,c:g[2],g:g[1],ts:Date.now()})','.set({to:c.uid,from:me.uid,c:g[2],g:g[1],s:c.sid||"",ts:Date.now()})')
open(P,"w",encoding="utf8").write(s);print("ok")
