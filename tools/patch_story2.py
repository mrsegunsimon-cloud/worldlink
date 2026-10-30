import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlStory2" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# 1. watermark stays in one place (no moving)
rep(';animation:wlwm 12s ease-in-out infinite}','}/*wlStory2*/')
rep('@keyframes wlwm{0%,30%{left:14px;top:92px}38%,64%{left:calc(100% - 215px);top:46%}72%,100%{left:14px;top:92px}}','')
# 2. the status circle shows the latest picture or video frame
rep('return Object.keys(g).map(k=>story(`data-sk="${esc(k)}"`,ring(g[k][0].u||k),g[k][0].u||k)).join("")})()}',
    'return Object.keys(g).map(k=>{const L=g[k],z=L[L.length-1],nm=L[0].u||k;const th=z.kind==="video"?`<video src="${esc(z.url)}#t=0.3" muted playsinline preload="metadata" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;pointer-events:none"></video>`:`<img src="${esc(z.url)}" alt="" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;pointer-events:none">`;return story(`data-sk="${esc(k)}"`,`<div style="width:68px;height:68px;border-radius:50%;padding:3px;margin:0 auto;background:linear-gradient(45deg,#25C7F0,#2EE59D)"><div style="width:100%;height:100%;border-radius:50%;overflow:hidden;border:3px solid var(--card);background:#222">${th}</div></div>`,nm)}).join("")})()}')
# 3. watching a status: home video stops, status plays with sound
rep(' clearTimeout(stT);\n const o=$("#story"),s=SQ[si];\n if(!s){o.classList.remove("on");o.innerHTML="";return}',
    ' clearTimeout(stT);\n const o=$("#story"),s=SQ[si];\n try{wlPause();window.__inStory=true}catch(e){}\n if(!s){o.classList.remove("on");o.innerHTML="";window.__inStory=false;try{wlResume()}catch(e){}return}')
rep('<video src="${esc(s.url)}" autoplay muted playsinline></video>','<video src="${esc(s.url)}" autoplay playsinline></video>')
rep(' const v=o.querySelector("video");\n if(v){v.onloadedmetadata','''const v=o.querySelector("video");
 if(v){v.muted=false;v.volume=1;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})})}
 if(v){v.onloadedmetadata''')
rep('if(window.CALLON)return;lzGo(v);if(!v._hold)v.play()','if(window.CALLON||window.__inStory)return;lzGo(v);if(!v._hold)v.play()')
rep('const f=$("#feed"),r=f.getBoundingClientRect(),cy=r.top+r.height/2;for(const c of f.querySelectorAll(".clip"))','if(window.__inStory)return;const f=$("#feed"),r=f.getBoundingClientRect(),cy=r.top+r.height/2;for(const c of f.querySelectorAll(".clip"))')
rep('$("#story").onclick=async e=>{','setInterval(()=>{if(window.__inStory)wlPause()},700);\n$("#story").onclick=async e=>{')
s=s.replace('2026.10.30-G','2026.10.30-H')
open(P,"w",encoding="utf8").write(s);print("ok")
