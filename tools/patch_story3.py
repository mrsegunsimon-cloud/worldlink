import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlStory3" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep('if(window.CALLON)return;lzGo(v);if(!v._hold)v.play()','if(window.CALLON||window.__inStory)return;lzGo(v);if(!v._hold)v.play()')
rep('const f=$("#feed"),r=f.getBoundingClientRect(),cy=r.top+r.height/2;for(const c of f.querySelectorAll(".clip"))','if(window.__inStory)return;const f=$("#feed"),r=f.getBoundingClientRect(),cy=r.top+r.height/2;for(const c of f.querySelectorAll(".clip"))')
rep('$("#story").onclick=async e=>{','setInterval(()=>{if(window.__inStory)wlPause()},700);/*wlStory3*/\n$("#story").onclick=async e=>{')
open(P,"w",encoding="utf8").write(s);print("ok")
