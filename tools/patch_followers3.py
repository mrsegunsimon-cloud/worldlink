import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlFollowCt3" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# people follow the name shown on your videos; count every name you have posted under
rep('const nm=x=>String(x||"").trim().toLowerCase(),mn=nm(me.name);const n=FOLLOWS.filter(d=>d.uid!==me.uid&&(d.list||[]).some(x=>nm(x)===mn)).length;',
    '/*wlFollowCt3*/const nm=x=>String(x||"").trim().toLowerCase(),mn=new Set([nm(me.name)]);CLIPS.forEach(c=>{if(c&&c.uid&&c.uid===me.uid&&c.u)mn.add(nm(c.u))});const n=FOLLOWS.filter(d=>d.uid!==me.uid&&(d.list||[]).some(x=>mn.has(nm(x)))).length;')
s=s.replace('2026.10.30-U','2026.10.30-V')
open(P,"w",encoding="utf8").write(s);print("ok")
