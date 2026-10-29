import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLazy2" in s: print("already");sys.exit(0)
a='<video data-lz="${esc(c.src)}" muted loop playsinline preload="metadata"></video>'
assert a in s
s=s.replace(a,'<video src="${esc(c.src)}" muted loop playsinline preload="none"></video>',1)
a='const lzGo=v=>{if(v&&v.dataset.lz&&!v.getAttribute("src")){v.src=v.dataset.lz}};'
assert a in s
s=s.replace(a,'/*wlLazy2*/const lzGo=v=>{if(v&&v.preload!=="auto"){v.preload="auto";}};',1)
open(P,"w",encoding="utf8").write(s);print("ok")
