import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlHomeUX" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# 1. tap to pause / play
rep('else{tt=setTimeout(()=>{const v=clip.querySelector("video");if(v)v.muted=!v.muted},320)}',
    'else{tt=setTimeout(()=>{const v=clip.querySelector("video");if(!v)return;/*wlHomeUX*/if(v.paused){v._hold=false;v.play().catch(()=>{});wlPI(clip,0)}else{v._hold=true;v.pause();wlPI(clip,1)}},320)}')
rep('/*wlPause*/function wlPause(){',
    'function wlPI(clip,on){let i=clip.querySelector(".wlpi");if(!i){i=document.createElement("div");i.className="wlpi";i.textContent="▶";i.style.cssText="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:64px;color:#fff;background:rgba(0,0,0,.35);width:104px;height:104px;border-radius:50%;display:grid;place-items:center;pointer-events:none;z-index:4";clip.appendChild(i)}i.style.display=on?"grid":"none"}\n/*wlPause*/function wlPause(){')
rep('const v=c.querySelector("video");if(v)v.play().catch(()=>{});break}}}catch(e){}}','const v=c.querySelector("video");if(v&&!v._hold)v.play().catch(()=>{});break}}}catch(e){}}')
rep('}else{v.pause();clearTimeout(e.target.__vt)}}),{root:$("#feed"),threshold:.6})','}else{v.pause();v._hold=false;wlPI(e.target,0);clearTimeout(e.target.__vt)}}),{root:$("#feed"),threshold:.6})')
rep("if(window.CALLON)return;lzGo(v);v.play().catch(()=>{});","if(window.CALLON)return;lzGo(v);if(!v._hold)v.play().catch(()=>{});")
# 2. pull down on the first video to load the latest
PULL=r'''
/* wlHomeUX: pull down on the first video to load the latest videos */
(function(){const f=document.getElementById("feed");if(!f)return;let y0=0,on=false,dy=0,last=0;
 const pill=document.createElement("div");pill.id="wlpull";pill.style.cssText="position:fixed;left:50%;top:92px;transform:translateX(-50%);background:rgba(0,0,0,.75);color:#fff;padding:9px 16px;border-radius:999px;font:700 14px system-ui,sans-serif;z-index:7;display:none";document.body.appendChild(pill);
 f.addEventListener("touchstart",e=>{on=f.scrollTop<=2;y0=e.touches[0].clientY;dy=0},{passive:true});
 f.addEventListener("touchmove",e=>{if(!on)return;dy=e.touches[0].clientY-y0;if(f.scrollTop>2){on=false;pill.style.display="none";return}if(dy>30){pill.textContent=dy>90?"Release to load the latest ↑":"↓ Pull to load the latest";pill.style.display="block"}else pill.style.display="none"},{passive:true});
 f.addEventListener("touchend",()=>{if(!on)return;on=false;if(dy>90&&Date.now()-last>4000){last=Date.now();pill.textContent="Loading the latest videos…";pill.style.display="block";try{window.wlRefresh&&wlRefresh()}catch(e){}setTimeout(()=>{pill.textContent="Up to date ✓";setTimeout(()=>{pill.style.display="none"},900);try{f.scrollTo({top:0})}catch(e){f.scrollTop=0}},1800)}else pill.style.display="none"},{passive:true});
})();
'''
rep('window.wlRefresh=function(){', PULL+'window.wlRefresh=function(){')
# 3. real people's statuses at the top of the Inbox
rep('${PEOPLE.slice(0,5).map(p=>story(\'data-st="1"\',ring(p[0]),p[0])).join("")}',
    '${(()=>{const g={};activeS().forEach(x=>{const k=x.o||x.u;(g[k]=g[k]||[]).push(x)});window.__stG=g;return Object.keys(g).map(k=>story(`data-sk="${esc(k)}"`,ring(g[k][0].u||k),g[k][0].u||k)).join("")})()}')
rep(' $("#panel").querySelectorAll("[data-st]").forEach(b=>b.onclick=stories);\n',
    ' $("#panel").querySelectorAll("[data-sk]").forEach(b=>b.onclick=()=>{const q=(window.__stG||{})[b.dataset.sk];if(q){SQ=q;si=0;close();showS()}});\n window.__stN=activeS().length;loadST().then(()=>{if($("#sa")&&activeS().length!==window.__stN){window.__stN=activeS().length;inbox()}});\n')
s=s.replace('2026.10.30-F','2026.10.30-G')
open(P,"w",encoding="utf8").write(s);print("ok")
