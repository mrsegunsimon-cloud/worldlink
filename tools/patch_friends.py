import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlFriends" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep(''' tk=tk||"s";
 const list=tk==="f"?PEOPLE.filter(p=>me.f.includes(p[0])):PEOPLE;''',''' tk=tk||"s";me.f=me.f||[];
 /*wlFriends*/const all=(()=>{const m=new Map();PEOPLE.forEach(p=>m.set(p[0],p[1]));(typeof PROF!=="undefined"?PROF:[]).forEach(x=>{if(x&&x.name&&x.name!==me.name&&!m.has(x.name))m.set(x.name,x.bio||"WorldLink member")});me.f.forEach(n=>{if(!m.has(n))m.set(n,"WorldLink member")});return [...m.entries()]})();
 if(!friends._l&&typeof PROF!=="undefined"&&!PROF.length&&typeof loadProfs==="function"){friends._l=1;loadProfs().then(()=>{if($("#frx"))friends(tk)})}
 const list=tk==="f"?all.filter(p=>me.f.includes(p[0])):all;''')
s=s.replace('2026.10.30-M','2026.10.30-N')
open(P,"w",encoding="utf8").write(s);print("ok")
