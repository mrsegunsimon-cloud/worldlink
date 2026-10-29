import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlVFull" in s: print("already");sys.exit(0)
a='<div id="vst" style="position:absolute;left:0;right:0;top:78px;bottom:100px">'
assert a in s
s=s.replace(a,'<div id="vst" style="position:absolute;left:0;right:0;top:0;bottom:0">',1)
a='<video id="vev" src="${url}" autoplay loop muted playsinline'
assert a in s
s=s.replace(a,'<video id="vev" src="${url}" autoplay loop playsinline',1)
a='const v=$("#vev"),fr=$("#vfr"),st=$("#vst");'
assert a in s
s=s.replace(a,a+'/*wlVFull*/v.muted=false;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})});',1)
open(P,"w",encoding="utf8").write(s);print("ok")
