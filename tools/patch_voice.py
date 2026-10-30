import sys,re
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlVoice" in s: print("already");sys.exit(0)
def rep(a,b,n=1):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,n)
# 1. no call buttons in chat headers
btn='<button class="ib" id="vc" aria-label="Voice call">📞</button><button class="ib" id="vd" aria-label="Video call">📹</button>'
assert s.count(btn)==2
s=s.replace(btn,'')
rep('$("#vc").onclick=()=>{close();startCall(p,false)};\n $("#vd").onclick=()=>{close();startCall(p,true)};\n','')
rep('$("#vc").onclick=()=>{close();startCall(o.n,false,o.u)};$("#vd").onclick=()=>{close();startCall(o.n,true,o.u)};\n','')
# 2. calls switched off everywhere (also if an old phone rings us)
rep('async function startCall(p,video,uid){\n','async function startCall(p,video,uid){\n return;/*wlVoice: calls removed*/\n')
rep('function showIncoming(d){\n','function showIncoming(d){\n return;/*wlVoice*/\n')
# 3. remove the Video Call menu entry
m=re.search(r',?\["Video Call","📹","[^"]*","Stage 1–2"\]',s);assert m
s=s[:m.start()]+s[m.end():]
rep(',"Video Call"].includes(n)',']'+'.includes(n)')
# 4. voice notes
rep('const bodyOf=b=>b.img?','const bodyOf=b=>b.au?`<audio controls preload="none" src="${esc(b.au)}" style="display:block;width:220px;max-width:100%"></audio>`:b.img?')
VN=r'''
 /*wlVoice*/const mic=document.createElement("button");mic.id="mic";mic.setAttribute("aria-label","Record a voice message");mic.textContent="🎤";mic.style.cssText="font-size:24px;padding:0 6px;flex:none";i.parentNode.insertBefore(mic,i);
 let MR=null,MCH=[],MT0=0,MTM=null,MST=null;
 const note=()=>$("#cin .note"),stopT=()=>{clearInterval(MTM);MTM=null};
 const reset=()=>{stopT();try{MST&&MST.getTracks().forEach(t=>t.stop())}catch(e){}MST=null;MR=null;MCH=[];mic.textContent="🎤";i.disabled=false;b.disabled=false;i.placeholder="Write a message"};
 const fin=async send=>{if(!MR)return;const r=MR;r.onstop=async()=>{const secs=Math.round((Date.now()-MT0)/1000),ty=r.mimeType||"audio/webm",ch=MCH.slice();reset();if(!send||secs<1)return;
   const n=note();try{n.textContent="Sending voice message…";const A=await claude.use("assets");const ext=/mp4|aac/.test(ty)?"m4a":/ogg/.test(ty)?"ogg":"webm";const f=new File([new Blob(ch,{type:ty})],"voice."+ext,{type:ty.split(";")[0]});const u=await A.upload(f);window.__sendMsg({au:u.url,d:secs})}catch(e){n.textContent="Voice message could not be sent. Check your internet."}};try{r.stop()}catch(e){reset()}};
 mic.onclick=async()=>{
  if(MR){fin(true);return}
  try{
   if(!navigator.mediaDevices||!window.MediaRecorder){note().textContent="Voice messages are not supported on this phone.";return}
   try{wlPauseAll&&wlPauseAll()}catch(e){}
   MST=await navigator.mediaDevices.getUserMedia({audio:true});
   const ty=["audio/webm;codecs=opus","audio/webm","audio/mp4","audio/ogg"].find(t=>MediaRecorder.isTypeSupported(t));
   MR=ty?new MediaRecorder(MST,{mimeType:ty}):new MediaRecorder(MST);MCH=[];MR.ondataavailable=e=>{if(e.data&&e.data.size)MCH.push(e.data)};
   MR.start(500);MT0=Date.now();mic.textContent="⏹️";i.disabled=true;b.disabled=true;
   MTM=setInterval(()=>{const s=Math.floor((Date.now()-MT0)/1000);i.placeholder="🔴 Recording "+Math.floor(s/60)+":"+String(s%60).padStart(2,"0")+" · tap ⏹️ to send";if(s>=120)fin(true)},400);
   const x=document.createElement("button");x.textContent="✕";x.setAttribute("aria-label","Cancel recording");x.style.cssText="font-size:20px;padding:0 8px;flex:none;color:#ef4444";mic.after(x);
   x.onclick=()=>{x.remove();fin(false)};const o=reset;
  }catch(e){reset();note().textContent="Allow the microphone to send voice messages."}
 };
 const cx=()=>{const x=mic.nextSibling;if(x&&x.textContent==="✕")x.remove()};setInterval(()=>{if(!MR)cx()},500);
'''
rep(' at.onclick=()=>fi.click();\n',' at.onclick=()=>fi.click();'+VN)
open(P,"w",encoding="utf8").write(s);print("ok")
