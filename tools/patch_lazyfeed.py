import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLazy" in s: print("already");sys.exit(0)
a='${c.src?`<video src="${esc(c.src)}" muted loop playsinline preload="metadata"></video>`:`<div class="big">${c.e}</div>`}<div class="shade"></div>'
assert a in s
s=s.replace(a,'${c.src?`<video data-lz="${esc(c.src)}" muted loop playsinline preload="metadata"></video>`:`<div class="big">${c.e}</div>`}<div class="shade"></div>',1)
a='function watch(){if(io)io.disconnect();io=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target.querySelector("video");if(!v)return;if(e.isIntersecting){v.play()'
assert a in s
s=s.replace(a,'/*wlLazy*/var lzio=null;const lzGo=v=>{if(v&&v.dataset.lz&&!v.getAttribute("src")){v.src=v.dataset.lz}};\nfunction watch(){if(lzio)lzio.disconnect();try{lzio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)lzGo(e.target.querySelector("video"))}),{root:$("#feed"),rootMargin:"120% 0px"});document.querySelectorAll(".clip").forEach(c=>lzio.observe(c))}catch(e){document.querySelectorAll(".clip video").forEach(lzGo)}if(io)io.disconnect();io=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target.querySelector("video");if(!v)return;if(e.isIntersecting){lzGo(v);v.play()',1)
open(P,"w",encoding="utf8").write(s);print("ok")
