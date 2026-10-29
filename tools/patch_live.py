import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLive" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# --- hook into the host screen
rep(' if($("#li"))$("#li").onkeydown=e=>{if(e.key==="Enter"&&e.target.value.trim()){say("@"+me.name+": "+e.target.value.trim());e.target.value=""}};',
    ' if($("#li"))$("#li").onkeydown=e=>{if(e.key==="Enter"&&e.target.value.trim()){say("@"+me.name+": "+e.target.value.trim());e.target.value=""}};\n try{liveHost(title,aud,say,got0=>{got+=got0;const g=$("#gt");if(g)g.textContent=got})}catch(e){}')
NEW=r'''/* wlLive: real live streaming. The host's camera goes straight to each viewer (up to 8 at once), chat, hearts and gifts travel over the realtime socket. */
let LIVEH=null,LIVEV=null,LIVES=[],LRT2=false;
const lrt=()=>window.WLCloud&&WLCloud.rt;
function liveInit(){
 if(LRT2||!me.uid||!lrt())return;LRT2=true;
 WLCloud.rt.on((t,ev,p)=>{
  if(!p)return;
  if(t==="wlc-"+me.uid){
   if(ev==="lv-offer"&&LIVEH)hostAnswer(p);
   if(ev==="lv-answer"&&LIVEV&&p.hid===LIVEV.uid&&LIVEV.pc&&!LIVEV.pc.remoteDescription){LIVEV.pc.setRemoteDescription({type:"answer",sdp:p.answer}).catch(()=>{})}
   if(ev==="lv-full"&&LIVEV&&p.hid===LIVEV.uid){const s=$("#lvs");if(s)s.textContent="This live is full right now. Try again in a minute."}
   return}
  const hid=LIVEH?me.uid:LIVEV?LIVEV.uid:null;if(!hid||t!=="live-"+hid)return;
  if(ev==="chat")liveSay("@"+p.fn+": "+p.t);
  else if(ev==="gift"){liveSay("@"+p.fn+" sent "+p.e+" "+p.g);livePop(p.e,p.c);if(LIVEH&&LIVEH.addGot)LIVEH.addGot(p.c)}
  else if(ev==="heart")livePop("❤️",1);
  else if(ev==="count"&&LIVEV){const n=$("#lvn");if(n)n.textContent=p.n+" watching"}
  else if(ev==="end"&&LIVEV){liveLeave("The live has ended.")}
 });
 WLCloud.rt.listen("wlc-"+me.uid)}
setInterval(liveInit,1500);
function liveSay(t){const L=$("#lc")||$("#lvc");if(!L)return;const d=document.createElement("div");d.textContent=t;L.appendChild(d);while(L.children.length>6)L.firstChild.remove()}
function livePop(e,c){const f=document.createElement("div");f.className="pop";f.textContent=e;f.style.left=(25+Math.random()*50)+"%";f.style.top="55%";f.style.fontSize=(c||1)>=200?"150px":(c||1)>=20?"110px":"80px";const L=$("#lf")||$("#lvf");if(L){L.appendChild(f);setTimeout(()=>f.remove(),1100)}}
async function livePut(on){try{const D=await claude.use("db");if(D&&me.uid&&LIVEH)await D.collection("calls").doc("live-"+me.uid).set({uid:me.uid,name:me.name,title:LIVEH.title,aud:LIVEH.aud,ts:Date.now(),st:on?"on":"off"})}catch(e){}}
function liveHost(title,aud,say,addGot){
 if(!me.uid||!lrt()||!window.__wlUser)return;liveInit();
 LIVEH={title,aud,pcs:{},addGot};wlPause();window.CALLON=true;
 WLCloud.rt.listen("live-"+me.uid);
 const lg=$("#lg");if(lg)lg.style.display="none";
 const sp=[...document.querySelectorAll("#panel span")].find(x=>/watching/.test(x.textContent));LIVEH.cnt=sp;
 const st=$("#st");if(st)st.textContent="";
 livePut(true);LIVEH.hb=setInterval(()=>livePut(true),20000);
 (async()=>{try{if(!FOLLOWS)await loadFollowsAll();(FOLLOWS||[]).filter(f=>f.uid!==me.uid&&(f.list||[]).includes(me.name)).slice(0,100).forEach(f=>notify(f.uid,"is live now: "+title))}catch(e){}})();
 const li=$("#li");if(li)li.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.value.trim()){const t=e.target.value.trim();if(window.modScan&&modScan("chat",{t})){return}WLCloud.rt.send("live-"+me.uid,"chat",{fn:me.name,t})}},true);
 const le=$("#le");if(le)le.addEventListener("click",()=>liveEnd(),true);
}
async function hostAnswer(p){
 try{
  if(!LIVEH||!rs)return;
  if(!LIVEH.pcs[p.from]&&Object.keys(LIVEH.pcs).length>=8){WLCloud.rt.send("wlc-"+p.from,"lv-full",{hid:me.uid});return}
  try{LIVEH.pcs[p.from]&&LIVEH.pcs[p.from].close()}catch(e){}
  const pc=new RTCPeerConnection(Object.assign({iceCandidatePoolSize:2},ICE));LIVEH.pcs[p.from]=pc;
  rs.getTracks().forEach(t=>pc.addTrack(t,rs));
  pc.onconnectionstatechange=()=>{const st=pc.connectionState;if(st==="failed"||st==="closed"||st==="disconnected"){if(LIVEH&&LIVEH.pcs[p.from]===pc){delete LIVEH.pcs[p.from];liveCount()}}if(st==="connected"){liveCount();try{pc.getSenders().forEach(sd=>{if(sd.track&&sd.track.kind==="video"){const q=sd.getParameters();if(!q.encodings||!q.encodings.length)q.encodings=[{}];q.encodings[0].maxBitrate=600000;sd.setParameters(q).catch(()=>{})}})}catch(e){}}};
  await pc.setRemoteDescription({type:"offer",sdp:p.offer});
  const an=await pc.createAnswer();await pc.setLocalDescription(an);await iceDone(pc);
  WLCloud.rt.send("wlc-"+p.from,"lv-answer",{hid:me.uid,answer:pc.localDescription.sdp});
 }catch(e){}
}
function liveCount(){if(!LIVEH)return;const n=Object.values(LIVEH.pcs).filter(x=>x.connectionState==="connected").length;if(LIVEH.cnt)LIVEH.cnt.textContent=n+" watching";try{WLCloud.rt.send("live-"+me.uid,"count",{n})}catch(e){}}
function liveEnd(){
 if(!LIVEH)return;clearInterval(LIVEH.hb);try{WLCloud.rt.send("live-"+me.uid,"end",{})}catch(e){}
 Object.values(LIVEH.pcs).forEach(x=>{try{x.close()}catch(e){}});livePut(false);LIVEH=null;window.CALLON=false;setTimeout(wlResume,300)}
function liveLeave(msg){
 if(!LIVEV)return;try{LIVEV.pc&&LIVEV.pc.close()}catch(e){}clearTimeout(LIVEV.to);LIVEV=null;window.CALLON=false;
 if(msg){open(`<h2>${esc(msg)}</h2><button class="btn" id="x">Close</button>`)}else close();setTimeout(wlResume,300)}
async function watchLive(h){
 if(!me.uid||!lrt()||!window.__wlUser||!window.RTCPeerConnection){open(`<h2>Live</h2><p class="mute">Sign in on the website or app to watch lives.</p><button class="btn ghost" id="x">Close</button>`);return}
 if(h.uid===me.uid){open(`<h2>This is your own live</h2><button class="btn ghost" id="x">Close</button>`);return}
 liveInit();await loadWallet();wlPause();window.CALLON=true;wlPauseAll();
 LIVEV={uid:h.uid,name:h.name,pc:null};
 openFull(`<div style="flex:1;position:relative;background:#000;overflow:hidden;min-height:0"><video id="rv" autoplay playsinline style="width:100%;height:100%;object-fit:cover"></video><div style="position:absolute;top:12px;left:12px;right:12px;display:flex;align-items:center;gap:8px;color:#fff;text-shadow:0 1px 4px #000"><span style="background:#E5233A;padding:3px 10px;border-radius:999px;font-weight:700;font-size:13px">LIVE</span><b>@${esc(h.name)}</b><span id="lvn" style="font-size:13px">watching</span><span style="flex:1"></span><button id="lvx" style="background:rgba(0,0,0,.5);color:#fff;border-radius:999px;padding:6px 14px;font-weight:700">Leave</button></div><div style="position:absolute;top:50px;left:12px;right:12px;color:#fff;font-weight:700;text-shadow:0 1px 4px #000">${esc(h.title||"")}</div><div id="lvf" style="position:absolute;inset:0;pointer-events:none;overflow:hidden"></div><p id="lvs" style="position:absolute;left:12px;right:12px;top:42%;margin:0;color:#fff;text-align:center;font-size:15px;text-shadow:0 1px 4px #000">Joining the live…</p><div id="lvc" style="position:absolute;left:12px;right:70px;bottom:62px;max-height:28%;overflow:hidden;color:#fff;font-size:14px;text-shadow:0 1px 4px #000"></div><div id="tray" style="display:none;position:absolute;left:0;right:0;bottom:0;background:rgba(10,10,20,.94);color:#fff;padding:12px 10px 14px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><b>Send a gift</b><span style="font-size:13px">Your coins: 🪙 <b id="lvk">${me.wl.vc}</b></span><button id="tc" style="color:#fff;font-size:20px">✕</button></div><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">${GIFTS.map((g,k)=>`<button data-g="${k}" style="background:rgba(255,255,255,.1);border-radius:12px;padding:8px 2px;color:#fff"><span style="font-size:30px;display:block">${g[0]}</span><span style="font-size:12px">${g[1]}</span><span style="font-size:12px;display:block;color:#FFB454">${g[2]}</span></button>`).join("")}</div><p id="lvg" style="font-size:12px;color:#ccc;margin:8px 0 0"></p></div><div style="position:absolute;left:10px;right:10px;bottom:10px;display:flex;gap:8px"><input id="lvi" maxlength="100" placeholder="Say something..." aria-label="Comment" style="flex:1;border:0;border-radius:999px;padding:11px 16px;background:rgba(255,255,255,.2);color:#fff;font:inherit;outline:0"><button id="lvh" aria-label="Heart" style="width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.2);font-size:22px">❤️</button><button id="lvgb" aria-label="Send a gift" style="width:46px;height:46px;border-radius:50%;background:#FF2D55;font-size:22px">🎁</button></div></div>`,true);
 WLCloud.rt.listen("live-"+h.uid);
 const v=$("#rv"),pc=new RTCPeerConnection(Object.assign({iceCandidatePoolSize:2},ICE));LIVEV.pc=pc;
 pc.ontrack=e=>{v.srcObject=e.streams[0];v.play().catch(()=>{});const s=$("#lvs");if(s)s.style.display="none"};
 pc.addTransceiver("video",{direction:"recvonly"});pc.addTransceiver("audio",{direction:"recvonly"});
 try{const off=await pc.createOffer();await pc.setLocalDescription(off);await iceDone(pc);
  WLCloud.rt.send("wlc-"+h.uid,"lv-offer",{from:me.uid,fn:me.name,offer:pc.localDescription.sdp});
  WLCloud.rt.send("live-"+h.uid,"chat",{fn:me.name,t:"joined 👋"});
  LIVEV.to=setTimeout(()=>{const s=$("#lvs");if(s&&s.style.display!=="none"){s.textContent="Could not connect. The live may have ended."}},15000);
 }catch(e){const s=$("#lvs");if(s)s.textContent="Could not join the live."}
 $("#lvx").onclick=()=>liveLeave();
 $("#lvi").onkeydown=e=>{if(e.key==="Enter"&&e.target.value.trim()){const t=e.target.value.trim();if(window.modScan&&modScan("chat",{t})){modBlock(modScan("chat",{t}));return}WLCloud.rt.send("live-"+h.uid,"chat",{fn:me.name,t});liveSay("@"+me.name+": "+t);e.target.value=""}};
 $("#lvh").onclick=()=>{WLCloud.rt.send("live-"+h.uid,"heart",{});livePop("❤️",1)};
 $("#lvgb").onclick=()=>{$("#tray").style.display="block"};$("#tc").onclick=()=>{$("#tray").style.display="none"};
 $("#panel").querySelectorAll("[data-g]").forEach(b=>b.onclick=async()=>{
  const g=GIFTS[+b.dataset.g];
  if(me.wl.vc<g[2]){$("#lvg").textContent="Not enough coins for a "+g[1]+". Buy or get free coins from the gift button on any video.";return}
  me.wl.vc-=g[2];const k=$("#lvk");if(k)k.textContent=me.wl.vc;
  try{const D=await claude.use("db");if(D)await D.collection("gifts").doc("g"+Date.now()+me.uid.slice(0,4)).set({to:h.uid,from:me.uid,c:g[2],g:g[1],ts:Date.now()})}catch(e){}
  WLCloud.rt.send("live-"+h.uid,"gift",{fn:me.name,e:g[0],g:g[1],c:g[2]});livePop(g[0],g[2]);liveSay("You sent "+g[0]+" "+g[1]);saveWallet();$("#tray").style.display="none"});
}
/* who is live now: a red LIVE row on Home */
async function liveScan(){
 try{if(!me.uid||!window.__wlUser||document.hidden)return;const D=await claude.use("db");const q=await D.collection("calls").get();
  LIVES=q.docs.map(d=>Object.assign({id:d.id},d.data())).filter(x=>x&&/^live-/.test(x.id)&&x.st==="on"&&x.uid!==me.uid&&Date.now()-x.ts<120000);liveBar()}catch(e){}}
function liveBar(){
 let el=document.getElementById("livebar");
 const show=LIVES.length&&$("#t1")&&$("#t1").classList.contains("on")&&!$("#sheet").classList.contains("on")&&!window.CALLON;
 if(!show){if(el)el.style.display="none";return}
 if(!el){el=document.createElement("div");el.id="livebar";el.style.cssText="position:fixed;left:8px;right:8px;top:104px;z-index:6;display:flex;gap:8px;overflow-x:auto";document.body.appendChild(el);
  el.onclick=e=>{const b=e.target.closest("[data-lv]");if(b){const l=LIVES.find(x=>x.uid===b.dataset.lv);if(l)watchLive({uid:l.uid,name:l.name,title:l.title})}}}
 el.style.display="flex";
 el.innerHTML=LIVES.map(l=>`<button data-lv="${esc(l.uid)}" style="flex:none;display:flex;align-items:center;gap:6px;background:rgba(0,0,0,.6);color:#fff;border-radius:999px;padding:6px 12px 6px 6px;font-weight:700;font-size:13px"><span style="background:#E5233A;border-radius:999px;padding:3px 8px;font-size:11px">LIVE</span>${esc(l.name)}</button>`).join("")}
setInterval(liveScan,15000);setTimeout(liveScan,4000);setInterval(()=>{try{liveBar()}catch(e){}},2500);
'''
rep('let RTL=false;',NEW+'let RTL=false;')
# notification tap opens the live
rep('   if(/your video/.test(t)){close();tab(1)}\n   else if(/follow/.test(t))','   if(/is live now/.test(t)){const l=LIVES.find(x=>x.name===n.from);if(l)watchLive({uid:l.uid,name:l.name,title:l.title});else open(`<h2>That live has ended</h2><button class="btn ghost" id="x">Close</button>`)}\n   else if(/your video/.test(t)){close();tab(1)}\n   else if(/follow/.test(t))')
open(P,"w",encoding="utf8").write(s);print("ok")
