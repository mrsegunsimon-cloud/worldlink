import sys,os
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLoud1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
loud=r'''/*wlLoud1*/
var WLSND=(()=>{try{return localStorage.getItem("wl_snd")!=="0"}catch(e){return true}})();
var WLCTX=null,WLG=null;
function wlAudio(){try{if(!WLCTX){const AC=window.AudioContext||window.webkitAudioContext;WLCTX=new AC();WLG=WLCTX.createGain();WLG.gain.value=1.7;const cp=WLCTX.createDynamicsCompressor();cp.threshold.value=-10;cp.knee.value=12;cp.ratio.value=8;cp.attack.value=.003;cp.release.value=.2;WLG.connect(cp);cp.connect(WLCTX.destination)}if(WLCTX.state==="suspended")WLCTX.resume();return WLCTX}catch(e){return null}}
function wlBoost(v){try{if(v._bs||!v.hasAttribute("crossorigin"))return;if(!wlAudio())return;WLCTX.createMediaElementSource(v).connect(WLG);v._bs=1}catch(e){}}
function wlUnmute(v){try{if(!WLSND)return;if(navigator.userActivation&&!navigator.userActivation.hasBeenActive)return;if(v.muted){v.muted=false;v.volume=1}wlBoost(v)}catch(e){}}
document.addEventListener("playing",e=>{const v=e.target;if(v&&v.tagName==="VIDEO"&&v.closest&&(v.closest("#feed")||v.id==="spvv"))wlUnmute(v)},true);
document.addEventListener("error",e=>{const v=e.target;if(v&&v.tagName==="VIDEO"&&v.hasAttribute("crossorigin")&&!v._cf&&!v._bs){v._cf=1;v.removeAttribute("crossorigin");try{v.load();v.play().catch(()=>{})}catch(x){}}},true);
function wlSndUi(){const b=document.getElementById("sndt");if(b)b.textContent=WLSND?"🔊":"🔇"}
function wlSndSet(on){WLSND=on;try{localStorage.setItem("wl_snd",on?"1":"0")}catch(e){}document.querySelectorAll("#feed video").forEach(v=>{if(on)wlUnmute(v);else v.muted=true});wlSndUi();if(on)wlPing()}
function wlPing(){try{if(!WLSND)return;const c=wlAudio();if(!c)return;const t=c.currentTime,g=c.createGain();g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.45,t+.02);g.gain.exponentialRampToValueAtTime(.0001,t+.7);g.connect(c.destination);[[880,0],[1318,.14]].forEach(a=>{const o=c.createOscillator();o.type="sine";o.frequency.value=a[0];o.connect(g);o.start(t+a[1]);o.stop(t+a[1]+.45)})}catch(e){}}
setTimeout(()=>{wlSndUi();const b=document.getElementById("sndt");if(b)b.onclick=()=>wlSndSet(!WLSND)},300);
'''
rep('/*PLAYER*/',loud+'/*PLAYER*/')
rep('<div id="feed"></div>','<div id="feed"></div>\n  <button id="sndt" aria-label="Sound on or off" style="position:absolute;left:10px;top:112px;z-index:6;width:38px;height:38px;border-radius:50%;background:rgba(0,0,0,.45);color:#fff;font-size:18px">🔊</button>')
rep('<video src="${esc(c.src)}" muted loop playsinline preload="none"></video>`:`<div class="big">','<video src="${esc(c.src)}" crossorigin="anonymous" muted loop playsinline preload="none"></video>`:`<div class="big">')
rep('function badge(){const n=NF.filter(x=>x.ts>me.ns&&!blocked(null,x.from)).length,b=$("#bd");','function badge(){const n=NF.filter(x=>x.ts>me.ns&&!blocked(null,x.from)).length,b=$("#bd");if(window.__lb!==undefined&&n>window.__lb&&document.visibilityState==="visible")wlPing();window.__lb=n;')
# notification rows: show the series picture and open the series
rep('<span style="font-size:24px;flex:none">${icon((n.text||"").toLowerCase())}</span>`}</div>`;','${n.th?`<img src="${esc(n.th)}" alt="" style="width:54px;height:54px;border-radius:10px;object-fit:cover;flex:none">`:`<span style="font-size:24px;flex:none">${icon((n.text||"").toLowerCase())}</span>`}`}</div>`;')
rep('const go=()=>{const n=all[+el.dataset.nt];if(!n)return;const t=(n.text||"").toLowerCase();if(n.img||n.vid){','const go=()=>{const n=all[+el.dataset.nt];if(!n)return;const t=(n.text||"").toLowerCase();if(n.sid){secFull=true;serDeep(n.sid);return}if(n.img||n.vid){')
open(P,"w",encoding="utf8").write(s);print("ok")
