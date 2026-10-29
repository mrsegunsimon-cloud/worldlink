import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlPause" in s: print("already");sys.exit(0)
a='function open(h){'
assert a in s
s=s.replace(a,'/*wlPause*/function wlPause(){try{document.querySelectorAll("#feed video").forEach(v=>v.pause())}catch(e){}}\nfunction wlResume(){try{if(($("#sheet").classList.contains("on"))||$("#call").classList.contains("on"))return;const f=$("#feed"),r=f.getBoundingClientRect(),cy=r.top+r.height/2;for(const c of f.querySelectorAll(".clip")){const q=c.getBoundingClientRect();if(q.top<=cy&&q.bottom>=cy){const v=c.querySelector("video");if(v)v.play().catch(()=>{});break}}}catch(e){}}\nfunction open(h){wlPause();',1)
a='$("#sheet").classList.remove("on","full","cam","sec");document.body.classList.remove("lt");document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x.dataset.n==="Home"));try{stopCam()}catch(e){}}'
assert a in s
s=s.replace(a,a[:-1]+'setTimeout(wlResume,150)}',1)
a='async function startCall(p,video){\n const c=$("#call");'
assert a in s
s=s.replace(a,'async function startCall(p,video){\n wlPause();const c=$("#call");',1)
a='$("#call").classList.remove("on")}'
assert a in s
s=s.replace(a,'$("#call").classList.remove("on");setTimeout(wlResume,150)}',1)
open(P,"w",encoding="utf8").write(s);print("ok")
