import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlFollowCt" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep('${stat(0,"Followers")}','<div id="mfw">${stat(0,"Followers")}</div>')
rep(' $("#hn1").onclick=newHL;$("#panel").querySelectorAll("[data-hl]")',
 ' /*wlFollowCt*/(async()=>{try{if(!FOLLOWS||Date.now()-(window.__flAt||0)>120000){await loadFollowsAll();window.__flAt=Date.now()}if(!FOLLOWS)return;const n=FOLLOWS.filter(d=>d.uid!==me.uid&&(d.list||[]).includes(me.name)).length;const e=$("#mfw");if(e)e.innerHTML=stat(fmt(n),"Followers")}catch(e){}})();\n $("#hn1").onclick=newHL;$("#panel").querySelectorAll("[data-hl]")')
s=s.replace('2026.10.30-O','2026.10.30-P')
open(P,"w",encoding="utf8").write(s);print("ok")
