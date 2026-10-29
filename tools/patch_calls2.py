import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlCalls2" in s: print("already");sys.exit(0)
# --- faster ICE and polling
a='const iceDone=pc=>new Promise(r=>{if(pc.iceGatheringState==="complete")return r();const t=setTimeout(r,5000);'
assert a in s
s=s.replace(a,'/*wlCalls2*/const iceDone=pc=>new Promise(r=>{if(pc.iceGatheringState==="complete")return r();const t=setTimeout(r,2200);',1)
s=s.replace('PC=new RTCPeerConnection(ICE);','PC=new RTCPeerConnection(Object.assign({iceCandidatePoolSize:4},ICE));',1)
s=s.replace('clearInterval(CPOLL);CPOLL=setInterval(async()=>{\n   if(!PC)return;const d=await cGet(uid);if(!d||d.ts!==ts)return;','clearInterval(CPOLL);CPOLL=setInterval(async()=>{\n   if(!PC)return;const d=await cGet(uid);if(!d||d.ts!==ts)return;',1)
s=s.replace('  },1500);\n }catch(e){cSay("Could not start the call.")}','  },800);\n }catch(e){cSay("Could not start the call.")}',1)
s=s.replace('},5000);\nfunction endCall(why){','},2000);\nfunction endCall(why){',1)
# --- new WhatsApp-style screen
i=s.find("function callUI(");j=s.find("const cSay=",i);assert i>0 and j>i
UI=r'''let CTM=null,CT0=0,FACE="user";
function callUI(name,status,video,incoming){
 const c=$("#call");c.classList.add("on");window.CALLON=true;wlPauseAll();
 const COL="#1E6FFF,#FF7A1A,#7C5CFF,#0E9F6E".split(",");
 const rb=(k,ic,l,bg,extra)=>`<button data-k="${k}" aria-label="${l}" style="display:flex;flex-direction:column;align-items:center;gap:6px;color:#fff;font-size:13px;${extra||""}"><span style="display:grid;place-items:center;width:62px;height:62px;border-radius:50%;background:${bg||"rgba(255,255,255,.16)"};font-size:26px">${ic}</span>${l}</button>`;
 const ctl=incoming?`<div style="display:flex;justify-content:space-around;width:100%">${rb("no","✕","Decline","#ef4444")}${rb("yes",video?"📹":"📞","Accept","#22c55e")}</div>`:`<div style="display:flex;justify-content:space-around;width:100%">${video?rb("flip","🔄","Flip"):""}${video?rb("cam","📷","Camera"):""}${rb("mic","🎤","Mute")}${rb("end","📞","End","#ef4444","")}</div>`;
 c.style.background=video?"#000":"linear-gradient(180deg,#0b141a 0%,#1f2c34 100%)";
 c.innerHTML=`<video id="rv" autoplay playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000;display:none"></video>
<div style="position:absolute;left:0;right:0;top:calc(env(safe-area-inset-top,0px) + 44px);text-align:center;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.6);z-index:2"><div style="font-size:12px;opacity:.8;letter-spacing:.3px">🔒 WorldLink ${video?"video":"voice"} call</div><h2 style="margin:6px 0 2px;font-size:26px;font-weight:700">${esc(name)}</h2><p id="cs2" style="margin:0;font-size:16px;opacity:.9">${esc(status)}</p></div>
<div id="cvv" style="position:absolute;left:0;right:0;top:34%;display:flex;justify-content:center;z-index:1"><div class="wlrip" style="width:150px;height:150px;border-radius:50%;display:grid;place-items:center;font-size:64px;font-weight:700;color:#fff;background:${COL[(name||"?").charCodeAt(0)%4]}">${esc((name||"?")[0].toUpperCase())}</div></div>
${video?'<video id="me" class="pip" muted playsinline autoplay style="top:auto;bottom:calc(150px + env(safe-area-inset-bottom,0px));right:14px;width:104px;z-index:3"></video>':""}
<div style="position:absolute;left:0;right:0;bottom:0;padding:22px 14px calc(26px + env(safe-area-inset-bottom,0px));background:linear-gradient(transparent,rgba(0,0,0,.55));z-index:3">${ctl}</div>
<style>@keyframes wlrip{0%{box-shadow:0 0 0 0 rgba(255,255,255,.35)}100%{box-shadow:0 0 0 38px rgba(255,255,255,0)}}.wlrip{animation:wlrip 1.6s infinite}</style>`;
 c.onclick=e=>{const b=e.target.closest("button");if(!b)return;const k=b.dataset.k;
  if(k==="end"||k==="no"){endCall(k==="no"?"declined":"");return}
  if(k==="yes"){acceptCall(c.__d);return}
  if(k==="flip"){flipCam();return}
  const sp=b.firstElementChild;const off=sp.dataset.off!=="1";sp.dataset.off=off?"1":"0";sp.style.background=off?"#fff":"rgba(255,255,255,.16)";sp.style.color=off?"#111":"#fff";
  if(k==="mic"&&stream)stream.getAudioTracks().forEach(t=>t.enabled=!off);
  if(k==="cam"&&stream)stream.getVideoTracks().forEach(t=>t.enabled=!off)}
}
async function flipCam(){try{FACE=FACE==="user"?"environment":"user";const ns=await navigator.mediaDevices.getUserMedia({video:{facingMode:FACE,width:{ideal:640},height:{ideal:480}}});const nt=ns.getVideoTracks()[0];const sd=PC&&PC.getSenders().find(x=>x.track&&x.track.kind==="video");if(sd)await sd.replaceTrack(nt);stream.getVideoTracks().forEach(t=>{t.stop();stream.removeTrack(t)});stream.addTrack(nt);const m=$("#me");if(m)m.srcObject=stream}catch(e){}}
function wlPauseAll(){try{document.querySelectorAll("video,audio").forEach(v=>{if(v.id!=="rv"&&v.id!=="me")v.pause()})}catch(e){}try{if(typeof cStop==="function")cStop()}catch(e){}try{if(typeof CAU!=="undefined"&&CAU&&CAU.state==="running")CAU.suspend()}catch(e){}}
setInterval(()=>{if(window.CALLON)wlPauseAll()},1500);
'''
s=s[:i]+UI+s[j:]
# --- lighter media for smoother calls
a='stream=await navigator.mediaDevices.getUserMedia({audio:true,video:video?{facingMode:"user"}:false});'
assert a in s
s=s.replace(a,'FACE="user";stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true},video:video?{facingMode:"user",width:{ideal:640},height:{ideal:480},frameRate:{ideal:24,max:30}}:false});',1)
a='PC.ontrack=e=>{const rv=$("#rv");if(rv){rv.srcObject=e.streams[0];'
assert a in s
s=s.replace(a,'PC.ontrack=e=>{const rv=$("#rv");if(rv){rv.srcObject=e.streams[0];rv.play().catch(()=>{});',1)
a='if(st==="connected")cSay("Connected");'
assert a in s
s=s.replace(a,'if(st==="connected"){cSay("Connected");clearInterval(CTM);CT0=Date.now();CTM=setInterval(()=>{const t=Math.floor((Date.now()-CT0)/1000);cSay(String(Math.floor(t/60)).padStart(2,"0")+":"+String(t%60).padStart(2,"0"))},1000);try{PC.getSenders().forEach(sd=>{if(sd.track&&sd.track.kind==="video"){const p=sd.getParameters();if(!p.encodings||!p.encodings.length)p.encodings=[{}];p.encodings[0].maxBitrate=700000;sd.setParameters(p).catch(()=>{})}})}catch(e){}}',1)
# end of call cleans up
a='function endCall(why){\n clearInterval(CPOLL);'
assert a in s
s=s.replace(a,'function endCall(why){\n clearInterval(CTM);window.CALLON=false;try{if(typeof CAU!=="undefined"&&CAU&&CAU.state==="suspended")CAU.resume()}catch(e){}$("#call").style.background="";\n clearInterval(CPOLL);',1)
# feed must not start while calling
a='if(e.isIntersecting){lzGo(v);v.play()'
assert a in s
s=s.replace(a,'if(e.isIntersecting){if(window.CALLON)return;lzGo(v);v.play()',1)
open(P,"w",encoding="utf8").write(s);print("ok")
