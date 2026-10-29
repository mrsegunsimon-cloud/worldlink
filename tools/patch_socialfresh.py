import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'wlFresh' in s: print('already');sys.exit()
a='$("#t2").onclick=()=>{secFull=true;social()};'
assert s.count(a)==1
s=s.replace(a,'$("#t2").onclick=()=>{secFull=true;social();loadPS().then(()=>{/*wlFresh*/if(document.querySelector("#pt")&&!$("#pt").value)social()})};')
open(p,'w',encoding='utf8').write(s);print('patched')
