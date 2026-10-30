import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlFollowCt2" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep('Date.now()-(window.__flAt||0)>120000){await loadFollowsAll();window.__flAt=Date.now()}if(!FOLLOWS)return;const n=FOLLOWS.filter(d=>d.uid!==me.uid&&(d.list||[]).includes(me.name)).length;',
    'Date.now()-(window.__flAt||0)>30000){await loadFollowsAll();window.__flAt=Date.now()}if(!FOLLOWS)return;/*wlFollowCt2*/const nm=x=>String(x||"").trim().toLowerCase(),mn=nm(me.name);const n=FOLLOWS.filter(d=>d.uid!==me.uid&&(d.list||[]).some(x=>nm(x)===mn)).length;')
rep('const fr=FOLLOWS.filter(d=>d.list.includes(n)).length','const fr=FOLLOWS.filter(d=>d.list.some(x=>String(x||"").trim().toLowerCase()===String(n||"").trim().toLowerCase())).length')
s=s.replace('2026.10.30-Q','2026.10.30-R')
open(P,"w",encoding="utf8").write(s);print("ok")
