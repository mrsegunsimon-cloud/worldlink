import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlCalls" in s: print("already");sys.exit(0)
i=s.find("async function startCall(p,video){");j=s.find("function videoCalls(){",i);assert i>0 and j>i
NEW=r'''/* wlCalls: real voice and video calls between two signed-in people (WebRTC, signalling through the calls collection) */
let PC=null,CDOC=null,CPOLL=null,CTMO=null,LASTRING=0,RING=null;
const ICE={iceServers:[{urls:"stun:stun.l.google.com:19302"},{urls:["turn:openrelay.metered.ca:80","turn:openrelay.metered.ca:443","turns:openrelay.metered.ca:443?transport=tcp"],username:"openrelayproject",credential:"openrelayproject"}]};
const cGet=async id=>{try{const D=await claude.use("db");const q=await D.collection("calls").doc(id).get();return q.exists?q.data():null}catch(e){return null}};
const cPut=async(id,o)=>{try{const D=await claude.use("db");await D.collection("calls").doc(id).set(o)}catch(e){}};
const iceDone=pc=>new Promise(r=>{if(pc.iceGatheringState==="complete")return r();const t=setTimeout(r,5000);pc.addEventListener("icegatheringstatechange",()=>{if(pc.iceGatheringState==="complete"){clearTimeout(t);r()}})});
const uidOf=n=>{try{const d=DMS.find(x=>dmOther(x).n===n);if(d)return dmOther(d).u;const c=CLIPS.find(x=>x.u===n&&x.uid);if(c)return c.uid;for(const k in PROF)if(PROF[k]&&PROF[k].name===n)return k}catch(e){}return null};
function callUI(name,status,video,incoming){
 const c=$("#call");c.classList.add("on");
 c.innerHTML=`<video id="rv" autoplay playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;background:#000;display:none"></video><div class="cv" id="cvv" style="position:relative"><div class="av" style="width:96px;height:96px;font-size:40px">${esc((name||"?")[0].toUpperCase())}</div><h2>@${esc(name)}</h2><p id="cs2">${esc(status)}</p></div>${video?'<video id="me" class="pip" muted playsinline autoplay></video>':""}<div class="ctl" style="position:relative">${incoming?'<button class="end" data-k="no" aria-label="Decline" style="background:#ef4444">✕</button><button data-k="yes" aria-label="Accept" style="background:#22c55e;font-size:30px">📞</button>':`<button data-k="mic" aria-label="Mute">🎤</button>${video?'<button data-k="cam" aria-label="Camera">📷</button>':""}<button class="end" data-k="end" aria-label="End call">✕</button>`}</div>`;
 c.onclick=e=>{const b=e.target.closest("button");if(!b)return;const k=b.dataset.k;
  if(k==="end"||k==="no"){endCall(k==="no"?"declined":"");return}
  if(k==="yes"){acceptCall(c.__d);return}
  b.classList.toggle("off");const off=b.classList.contains("off");
  if(k==="mic"&&stream)stream.getAudioTracks().forEach(t=>t.enabled=!off);
  if(k==="cam"&&stream)stream.getVideoTracks().forEach(t=>t.enabled=!off)}
}
const cSay=t=>{const s=$("#cs2");if(s)s.textContent=t};
async function cMedia(video){
 stream=await navigator.mediaDevices.getUserMedia({audio:true,video:video?{facingMode:"user"}:false});
 const m=$("#me");if(m)m.srcObject=stream;
}
function cPeer(video){
 PC=new RTCPeerConnection(ICE);
 stream.getTracks().forEach(t=>PC.addTrack(t,stream));
 PC.ontrack=e=>{const rv=$("#rv");if(rv){rv.srcObject=e.streams[0];if(video){rv.style.display="block";const cv=$("#cvv");if(cv)cv.style.display="none"}else{rv.play().catch(()=>{});}}};
 PC.onconnectionstatechange=()=>{const st=PC&&PC.connectionState;if(st==="connected")cSay("Connected");if(st==="failed"){cSay("Call failed. Check your network.");setTimeout(()=>endCall("failed"),1800)}};
}
async function startCall(p,video,uid){
 wlPause();uid=uid||uidOf(p);
 if(!uid||!me.uid||!window.RTCPeerConnection||!navigator.mediaDevices){
  callUI(p,uid?"Calls are not available on this phone.":"Camera test: calls need the other person to have a WorldLink account.",video,false);
  if(video){try{stream=await navigator.mediaDevices.getUserMedia({video:true});const m=$("#me");if(m)m.srcObject=stream}catch(e){cSay("Camera not available here")}}
  return}
 callUI(p,"Starting…",video,false);
 try{await cMedia(video)}catch(e){cSay("Allow the microphone"+(video?" and camera":"")+" in your browser, then try again.");return}
 try{
  cPeer(video);const off=await PC.createOffer();await PC.setLocalDescription(off);await iceDone(PC);
  const ts=Date.now();CDOC={id:uid,from:me.uid,fn:me.name,v:!!video,ts};
  await cPut(uid,{from:me.uid,fn:me.name,v:!!video,st:"ring",ts,offer:PC.localDescription.sdp});
  cSay("Ringing…");
  CTMO=setTimeout(()=>{cSay("No answer");setTimeout(()=>endCall("noanswer"),1500)},45000);
  clearInterval(CPOLL);CPOLL=setInterval(async()=>{
   if(!PC)return;const d=await cGet(uid);if(!d||d.ts!==ts)return;
   if(d.st==="on"&&d.answer&&!PC.remoteDescription){clearTimeout(CTMO);try{await PC.setRemoteDescription({type:"answer",sdp:d.answer});cSay("Connecting…")}catch(e){cSay("Could not connect")}}
   if(d.st==="end"){cSay(PC.remoteDescription?"Call ended":"Declined");setTimeout(()=>endCall("remote"),1200)}
  },1500);
 }catch(e){cSay("Could not start the call.")}
}
async function acceptCall(d){
 clearInterval(RING);RING=null;const video=!!d.v;
 callUI(d.fn,"Connecting…",video,false);
 try{await cMedia(video);cPeer(video);
  await PC.setRemoteDescription({type:"offer",sdp:d.offer});
  const an=await PC.createAnswer();await PC.setLocalDescription(an);await iceDone(PC);
  CDOC={id:me.uid,from:d.from,fn:d.fn,v:d.v,ts:d.ts};
  await cPut(me.uid,{from:d.from,fn:d.fn,v:!!d.v,ts:d.ts,st:"on",offer:d.offer,answer:PC.localDescription.sdp});
  clearInterval(CPOLL);CPOLL=setInterval(async()=>{if(!PC)return;const x=await cGet(me.uid);if(x&&x.ts===d.ts&&x.st==="end"){cSay("Call ended");setTimeout(()=>endCall("remote"),1000)}},2000);
 }catch(e){cSay("Could not connect the call.");setTimeout(()=>endCall("failed"),1500)}
}
function showIncoming(d){
 if(PC)return;wlPause();callUI(d.fn||"Someone",d.v?"Incoming video call…":"Incoming call…",!!d.v,true);$("#call").__d=d;
 clearInterval(RING);let n=0;RING=setInterval(async()=>{n++;try{cChime("ring")}catch(e){}
  if(n%2===0){const x=await cGet(me.uid);if(!x||x.ts!==d.ts||x.st!=="ring"||n>20){clearInterval(RING);RING=null;if(!PC){$("#call").classList.remove("on");setTimeout(wlResume,150)}}}},1500);
}
setInterval(async()=>{
 if(document.hidden||!me.uid||!window.__wlUser||PC||RING)return;
 const d=await cGet(me.uid);
 if(d&&d.st==="ring"&&d.from!==me.uid&&d.ts!==LASTRING&&Date.now()-d.ts<40000){LASTRING=d.ts;showIncoming(d)}
},5000);
function endCall(why){
 clearInterval(CPOLL);CPOLL=null;clearTimeout(CTMO);clearInterval(RING);RING=null;
 const D0=CDOC;CDOC=null;
 if(D0&&why!=="remote"){cPut(D0.id,{from:D0.from,fn:D0.fn,v:!!D0.v,ts:D0.ts,st:"end"})}
 else if(!D0&&why==="declined"){const d=$("#call").__d;if(d)cPut(me.uid,{from:d.from,fn:d.fn,v:!!d.v,ts:d.ts,st:"end"})}
 try{PC&&PC.close()}catch(e){}PC=null;
 if(stream){stream.getTracks().forEach(t=>t.stop());stream=null}
 $("#call").classList.remove("on");$("#call").innerHTML="";setTimeout(wlResume,150)}
'''
s=s[:i]+NEW+s[j:]
# drop the old endCall
a='function endCall(){if(stream){stream.getTracks().forEach(t=>t.stop());stream=null}$("#call").classList.remove("on");setTimeout(wlResume,150)}'
assert a in s
s=s.replace(a,"",1)
s=s.replace('startCall(o.n,false)','startCall(o.n,false,o.u)').replace('startCall(o.n,true)','startCall(o.n,true,o.u)')
open(P,"w",encoding="utf8").write(s);print("ok")
