/*wlSeries1*//*wlSeries2*/
var SER=[],EPS=[],SERL=false;
async function loadSeries(){try{const D=await claude.use("db");if(!D)return;const a=await D.collection("series").get(),b=await D.collection("episodes").get();SER=a.docs.map(d=>d.data()).filter(x=>x&&x.id&&!x.del).sort((p,q)=>q.ts-p.ts);EPS=b.docs.map(d=>d.data()).filter(x=>x&&x.id&&x.url&&!x.del).sort((p,q)=>(p.n||0)-(q.n||0));SERL=true}catch(e){}}
const serEps=id=>EPS.filter(e=>e.sid===id).sort((a,b)=>(a.n||0)-(b.n||0));
const serGrad=t=>{const g=GRAD[hsh(t||"x")%GRAD.length];return `linear-gradient(160deg,${g[0]},${g[1]})`};
const isMod2=()=>{try{return !!(me.uid&&window.__mods&&window.__mods.includes(me.uid))}catch(e){return false}};
async function serMods(){try{if(window.__mods||!me.uid)return;const D=await claude.use("db");const d=await D.collection("admin").doc("mods").get();window.__mods=d.exists?((d.data()||{}).list||[]):[]}catch(e){window.__mods=[]}}
function seriesHome(){
 secFull=true;
 const L=SER.filter(s=>!blocked(s.o,s.u));
 const card=s=>{const n=serEps(s.id).length;return `<button data-sv="${esc(s.id)}" style="display:flex;gap:12px;width:100%;align-items:center;text-align:left;color:inherit;padding:10px 0;border-bottom:1px solid var(--line)"><span style="width:84px;height:112px;border-radius:14px;background:${serGrad(s.t)};display:grid;place-items:center;color:#fff;font-size:34px;flex:none;position:relative">🎬<span style="position:absolute;left:6px;bottom:6px;right:6px;font-size:11px;font-weight:700;text-align:center;background:rgba(0,0,0,.45);border-radius:6px;padding:1px 0">${n} ep</span></span><span style="flex:1;min-width:0"><b style="display:block;font-size:17px;line-height:1.25">${esc(s.t)}</b><span class="mute" style="display:block;font-size:13px;margin:2px 0 4px">by @${esc(s.u)} · ${ago(s.ts)==="now"?"now":ago(s.ts)+" ago"}</span><span style="display:block;font-size:13px;opacity:.85;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical">${esc(s.d||"")}</span></span></button>`};
 open(`<div style="display:flex;align-items:center;gap:8px;padding:2px 0 8px"><h2 style="flex:1;margin:0;font-size:30px;letter-spacing:-.02em">Series</h2><button id="sn" class="btn" style="width:auto;margin:0;padding:10px 16px">+ New series</button></div><p class="note" style="margin:0 0 6px">Watch movie series, episode by episode. Send a gift to the creator, or download an episode with the WorldLink watermark.</p>${L.length?L.map(card).join(""):`<p class="mute" style="text-align:center;padding:30px 10px">${SERL?"No series yet. Tap + New series to post the first one.":"Loading…"}</p>`}<button class="btn ghost" id="x" style="margin-top:12px">Close</button>`);
 $("#sn").onclick=()=>newSeries();
 $("#panel").querySelectorAll("[data-sv]").forEach(b=>b.onclick=()=>seriesPage(b.dataset.sv));
}
async function seriesOpen(){secFull=true;seriesHome();await Promise.all([loadSeries(),serMods()]);if(document.querySelector("#sn")&&!document.querySelector("[data-sv-open]"))seriesHome()}
function seriesPage(id){
 secFull=true;const s=SER.find(x=>x.id===id);if(!s){seriesHome();return}
 const E=serEps(id),mine=s.o&&s.o===me.uid,mod=isMod2();
 open(`<div style="display:flex;align-items:center;gap:8px"><button id="sb" aria-label="Back" style="font-size:26px;padding:4px 8px;color:inherit">←</button><h2 style="flex:1;margin:0;font-size:22px;line-height:1.2" data-sv-open="1">${esc(s.t)}</h2></div><div style="height:120px;border-radius:16px;background:${serGrad(s.t)};display:grid;place-items:center;color:#fff;font-size:44px;margin:10px 0">🎬</div><div class="mute" style="font-size:13px">by <b data-pn="${esc(s.u)}" data-pu="${esc(s.o||"")}" style="cursor:pointer">@${esc(s.u)}</b> · ${E.length} episode${E.length===1?"":"s"} · 👁 ${E.reduce((m,x)=>m+(x.v||0),0)}</div>${s.d?`<p style="margin:8px 0">${esc(s.d)}</p>`:""}${mine?`<button class="btn" id="ae">+ Add episode</button>`:`<button class="btn" id="sg">🎁 Gift this series</button>`}${E.length?E.map((e,k)=>`<div style="display:flex;align-items:center;gap:8px;padding:10px 0;border-bottom:1px solid var(--line)"><button data-ep="${k}" style="flex:1;min-width:0;display:flex;align-items:center;gap:10px;text-align:left;color:inherit"><span style="width:38px;height:38px;border-radius:50%;background:var(--acc);color:var(--accink);display:grid;place-items:center;flex:none">▶</span><span style="min-width:0"><b style="display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">Episode ${e.n||k+1}${e.t?": "+esc(e.t):""}</b></span></button>${(mine||mod)?`<button data-ed="${k}" aria-label="Delete episode" style="font-size:18px;opacity:.6;padding:6px">🗑️</button>`:""}</div>`).join(""):'<p class="mute">No episodes yet.</p>'}<div style="display:flex;gap:8px;margin-top:10px">${!mine?`<button class="btn ghost" id="sr" style="margin:0">Report</button>`:""}${(mine||mod)?`<button class="btn ghost" id="sd" style="margin:0">Delete series</button>`:""}</div><button class="btn ghost" id="x" style="margin-top:8px">Close</button>`);
 $("#sb").onclick=seriesHome;
 $("#panel").querySelectorAll("[data-ep]").forEach(b=>b.onclick=()=>epPlay(id,+b.dataset.ep));
 $("#panel").querySelectorAll("[data-pn]").forEach(el=>el.onclick=()=>personSheet(el.dataset.pn,el.dataset.pu||"",()=>seriesPage(id)));
 const ae=$("#ae");if(ae)ae.onclick=()=>addEpisode(s);
 const sg=$("#sg");if(sg)sg.onclick=()=>giftSheet({uid:s.o,u:s.u,sid:s.id});const sr=$("#sr");if(sr)sr.onclick=()=>reportFlow("video",s.id,s.o,s.u,()=>seriesPage(id));
 const sd=$("#sd");if(sd)sd.onclick=async()=>{if(!confirm("Delete this whole series?"))return;s.del=true;try{const D=await claude.use("db");await D.collection("series").doc(s.id).set(s)}catch(e){}SER=SER.filter(x=>x!==s);seriesHome()};
 $("#panel").querySelectorAll("[data-ed]").forEach(b=>b.onclick=async()=>{const e=E[+b.dataset.ed];if(!e||!confirm("Delete this episode?"))return;e.del=true;try{const D=await claude.use("db");await D.collection("episodes").doc(e.id).set(e)}catch(x){}EPS=EPS.filter(y=>y!==e);seriesPage(id)});
}
function epForm(title,withMeta,s,go,pre){
 pre=pre||{};
 open(`<h2>${title}</h2>${withMeta?`<input class="in" id="stt" maxlength="60" placeholder="Series title" aria-label="Series title" value="${esc(pre.t||"")}"><input class="in" id="std" maxlength="200" placeholder="What is it about? (optional)" aria-label="Description" value="${esc(pre.d||"")}">`:""}<input class="in" id="ept" maxlength="60" placeholder="Episode title (optional)" aria-label="Episode title" value="${esc(pre.e||"")}"><p class="note" style="margin:0 0 4px">Choose the episode video. Up to 20 MB. If it is bigger, you can cut it shorter. Post only videos you made or have the rights to share.</p><input class="in" id="epf" type="file" accept="video/*" aria-label="Choose the episode video"><p class="note" id="st">${esc(pre.msg||"")}</p><button class="btn" id="epp">Post</button><button class="btn ghost" id="epb">Cancel</button>`);
 if(pre.f){try{const dt=new DataTransfer();dt.items.add(pre.f);$("#epf").files=dt.files}catch(x){}}
 $("#epb").onclick=()=>s?seriesPage(s.id):seriesHome();
 $("#epf").onchange=()=>{const f=$("#epf").files[0];if(f)$("#st").textContent=(f.size/1048576).toFixed(1)+" MB"+(f.size>20*1048576?". That is over 20 MB. Tap Post and you can cut it shorter.":"")};
 $("#epp").onclick=()=>{
  const f=$("#epf").files[0],v={t:withMeta?$("#stt").value.trim():"",d:withMeta?$("#std").value.trim():"",e:$("#ept").value.trim()};
  if(f&&f.type.startsWith("video")&&f.size>20*1048576){serTrim(f,(f2,msg)=>epForm(title,withMeta,s,go,Object.assign({},v,{f:f2||f,msg:msg})));return}
  go(f,v.e,v.t,v.d,$("#st"),$("#epp"));
 };
}
function serTrim(f,back){
 window.__edHook={cancel:()=>back(null,"Your video is still over 20 MB. Cut it shorter to post it."),done:async T=>{
  secFull=true;open(`<h2 style="text-align:center">Cutting your video…</h2><p id="trp" class="mute" style="text-align:center">Please keep this screen open.</p>`);
  let c=null;
  try{
   if(T.full){c=f}
   if(!c&&!T.sh){try{c=await Promise.race([fastCut(f,T.st,T.en,q=>{const p=$("#trp");if(p)p.textContent="Cutting… "+Math.round(q*100)+"%"}),new Promise((_,no)=>setTimeout(()=>no(new Error("slow")),25000))])}catch(x){c=null}}
   if(!c)c=await trimCrop(f,T.st,T.en,VSHAPES[T.sh||0][1],T.pos==null?.5:T.pos,(t,d)=>{const p=$("#trp");if(p)p.textContent="Cutting… "+Math.round(100*Math.min(1,t/(d||1)))+"%"});
  }catch(x){c=null}
  if(!c||!c.size){back(null,"Could not cut this video on this phone. Try a shorter video.");return}
  if(c.size>20*1048576){serTrim(c,back);return}
  back(c,"Cut to "+(c.size/1048576).toFixed(1)+" MB. Tap Post.");
 }};
 secFull=true;editVideo(f,true);
}
async function epUpload(f,st,btn){
 if(!f){st.textContent="Choose a video first.";return null}
 if(!f.type.startsWith("video")){st.textContent="Choose a video file.";return null}
 if(f.size>20*1048576){st.textContent="That video is over 20 MB. Choose a shorter one.";return null}
 if(!me.uid){st.textContent="Please sign in first.";return null}
 btn.disabled=true;st.textContent="Uploading… keep this screen open.";
 for(let t=0;t<2;t++){try{const A=await claude.use("assets");const r=await A.upload(f);if(r&&r.url)return r.url}catch(e){}}
 btn.disabled=false;st.textContent="Upload failed. Check your connection and try again.";return null;
}
function newSeries(){
 if(!me.uid){open(`<h2>Sign in first</h2><p class="mute">Sign in or create an account to post a series.</p><button class="btn" id="x">OK</button>`);return}
 epForm("New series",true,null,async(f,et,t,d,st,btn)=>{
  if(!t){st.textContent="Give your series a title.";return}
  const url=await epUpload(f,st,btn);if(!url)return;
  const s={id:"sr"+Date.now(),t,d,u:me.name,o:me.uid,ts:Date.now()},e={id:"ep"+Date.now(),sid:s.id,n:1,t:et,url,u:me.name,o:me.uid,ts:Date.now()};
  try{const D=await claude.use("db");await D.collection("series").doc(s.id).set(s);await D.collection("episodes").doc(e.id).set(e)}catch(x){btn.disabled=false;st.textContent="Could not save. Try again.";return}
  SER.unshift(s);EPS.push(e);seriesPage(s.id);
 });
}
function addEpisode(s){
 epForm("Add episode to "+s.t,false,s,async(f,et,_t,_d,st,btn)=>{
  const url=await epUpload(f,st,btn);if(!url)return;
  const n=serEps(s.id).reduce((m,x)=>Math.max(m,x.n||0),0)+1,e={id:"ep"+Date.now(),sid:s.id,n,t:et,url,u:me.name,o:me.uid,ts:Date.now()};
  try{const D=await claude.use("db");await D.collection("episodes").doc(e.id).set(e);s.ts=Date.now();await D.collection("series").doc(s.id).set(s)}catch(x){btn.disabled=false;st.textContent="Could not save. Try again.";return}
  EPS.push(e);seriesPage(s.id);
 });
}
const serAv=(n,sz)=>{const p=(typeof PROF!=="undefined"?PROF:[]).find(x=>x.name===n),C=["#1E6FFF","#FF7A1A","#7C5CFF","#0E9F6E"];return p&&p.pic?`<img src="${esc(p.pic)}" alt="" style="width:${sz}px;height:${sz}px;border-radius:50%;object-fit:cover;flex:none;display:block">`:`<span style="width:${sz}px;height:${sz}px;border-radius:50%;display:grid;place-items:center;flex:none;font-weight:800;color:#fff;background:${C[(n||"?").charCodeAt(0)%4]};font-size:${Math.round(sz*.42)}px">${esc((n||"?")[0].toUpperCase())}</span>`};
async function epSave(e){try{const D=await claude.use("db");if(D&&me.uid)await D.collection("episodes").doc(e.id).set(e)}catch(x){}}
function epPlay(sid,k){
 const s=SER.find(x=>x.id===sid),E=serEps(sid),e=E[k];if(!s||!e)return;
 try{PL.a.pause()}catch(x){}
 let o=document.getElementById("spv");if(o)o.remove();
 document.body.classList.add("spo");$("#sheet").classList.remove("on");
 o=document.createElement("div");o.id="spv";o.style.cssText="position:fixed;inset:0;z-index:92;background:#0b0e1e;color:#fff;display:flex;flex-direction:column";
 o.innerHTML=`<div style="position:relative;flex:none;height:40vh;min-height:210px;background:#000"><video id="spvv" src="${esc(e.url)}" controls playsinline autoplay controlsList="nodownload" style="width:100%;height:100%;object-fit:contain;background:#000"></video><div id="spwm" aria-hidden="true" style="position:absolute;left:14px;top:60px;pointer-events:none;text-shadow:0 1px 5px rgba(0,0,0,.85);font-size:14px;line-height:1.15;opacity:.9;transition:all .6s"><b>🌍 WorldLink</b><div style="font-size:11px">@${esc(e.u)} · worldlink.app</div></div><button id="spx" aria-label="Close" style="position:absolute;top:max(8px,env(safe-area-inset-top,0px));left:8px;width:40px;height:40px;border-radius:50%;background:rgba(0,0,0,.5);color:#fff;font-size:22px">←</button></div><div id="spb" style="flex:1;min-height:0;overflow-y:auto;padding:12px 14px calc(14px + env(safe-area-inset-bottom,0px))"></div>`;
 document.body.appendChild(o);
 const v=$("#spvv"),wm=$("#spwm"),pos=[[14,60],[null,60],[14,null],[null,null]];let pi=0;
 const mv=setInterval(()=>{if(!document.getElementById("spv")){clearInterval(mv);return}pi=(pi+1)%4;const p=pos[pi];wm.style.left=p[0]===null?"auto":p[0]+"px";wm.style.right=p[0]===null?"14px":"auto";wm.style.top=p[1]===null?"auto":p[1]+"px";wm.style.bottom=p[1]===null?"56px":"auto"},6000);
 const close2=()=>{clearInterval(mv);v.pause();o.remove();document.body.classList.remove("spo")};
 $("#spx").onclick=()=>{close2();secFull=true;seriesPage(sid)};
 v.onended=()=>{if(k+1<E.length){close2();epPlay(sid,k+1)}};
 window.__epv=window.__epv||{};if(me.uid&&!window.__epv[e.id]){window.__epv[e.id]=1;e.v=(e.v||0)+1;epSave(e)}
 const mod=isMod2(),can=c=>c.o===me.uid||e.o===me.uid||mod;
 const draw=()=>{
  const l=e.l||[],liked=me.uid&&l.includes(me.uid),cm=e.cm||[],bt="flex:none;padding:9px 14px;border-radius:999px;background:rgba(255,255,255,.12);color:#fff;font-weight:700;font-size:14px;white-space:nowrap";
  const sc=$("#spb").scrollTop;
  $("#spb").innerHTML=`<b style="display:block;font-size:17px;line-height:1.3">${esc(s.t)} · Episode ${e.n||k+1}${e.t?": "+esc(e.t):""}</b><div style="font-size:13px;opacity:.7;margin:3px 0 10px">👁 ${e.v||0} view${(e.v||0)===1?"":"s"} · ${ago(e.ts)==="now"?"now":ago(e.ts)+" ago"}</div><div style="display:flex;align-items:center;gap:10px;margin-bottom:12px">${serAv(e.u,38)}<b style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">@${esc(e.u)}</b></div><div style="display:flex;gap:8px;overflow-x:auto;padding-bottom:6px"><button id="sl" style="${bt};${liked?"background:#FE2C55":""}">${liked?"❤️":"🤍"} ${l.length}</button><button id="scm" style="${bt}">💬 ${cm.length}</button><button id="ssh" style="${bt}">↗ Share</button><button id="spg" style="${bt};background:#FF7A1A">🎁 Gift</button><button id="spd" style="${bt}">⬇ Download</button>${k+1<E.length?`<button id="spn" style="${bt}">Next ▶</button>`:""}</div><p id="spm" class="note" style="margin:4px 0 0;color:#ffd0a8;display:none"></p><h3 id="scmh" style="margin:14px 0 8px;font-size:16px">Comments · ${cm.length}</h3><div style="display:flex;gap:10px;align-items:center;margin-bottom:12px">${serAv(me.name,34)}<input id="sci" maxlength="300" placeholder="${me.uid?"Add a comment…":"Sign in to comment"}" aria-label="Add a comment" style="flex:1;min-width:0;padding:11px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);color:#fff;font-size:15px"><button id="scs" style="padding:10px 14px;border-radius:999px;background:#FF7A1A;color:#fff;font-weight:700">Post</button></div>${cm.length?cm.slice().reverse().map(c=>`<div style="display:flex;gap:10px;margin-bottom:14px">${serAv(c.n,36)}<div style="flex:1;min-width:0"><div style="font-size:13px"><b>@${esc(c.n)}</b> <span style="opacity:.6">${c.ts?(ago(c.ts)==="now"?"now":ago(c.ts)+" ago"):""}</span></div><div style="font-size:15px;line-height:1.35;overflow-wrap:anywhere">${esc(c.t)}</div></div>${can(c)?`<button data-cd="${cm.indexOf(c)}" aria-label="Delete comment" style="opacity:.6;padding:4px 6px">✕</button>`:""}</div>`).join(""):'<p style="opacity:.6">No comments yet. Be the first.</p>'}${E.length>1?`<h3 style="margin:16px 0 8px;font-size:16px">All episodes</h3>${E.map((x,q)=>`<button data-go="${q}" style="display:flex;align-items:center;gap:10px;width:100%;text-align:left;color:#fff;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.12);${q===k?"color:#FF7A1A;font-weight:700":""}"><span>${q===k?"▶":"•"}</span><span>Episode ${x.n||q+1}${x.t?": "+esc(x.t):""}</span></button>`).join("")}`:""}`;
  $("#spb").scrollTop=sc;
  const need=()=>{if(me.uid)return true;const m=$("#spm");m.style.display="block";m.textContent="Please sign in first.";return false};
  $("#sl").onclick=()=>{if(!need())return;const was=(e.l||[]).includes(me.uid);e.l=was?e.l.filter(u=>u!==me.uid):(e.l||[]).concat(me.uid);epSave(e);if(!was)notify(e.o,"liked your episode of "+s.t);draw()};
  $("#scm").onclick=()=>{$("#scmh").scrollIntoView({behavior:"smooth",block:"start"});setTimeout(()=>{try{$("#sci").focus()}catch(x){}},350)};
  $("#ssh").onclick=async()=>{const u="https://worldlink.app/";try{if(navigator.share)await navigator.share({title:s.t,text:s.t+" · Episode "+(e.n||k+1)+" on WorldLink",url:u});else{await navigator.clipboard.writeText(u);const m=$("#spm");m.style.display="block";m.textContent="Link copied."}}catch(x){}};
  $("#spg").onclick=()=>{v.pause();giftSheet({uid:e.o,u:e.u,sid:s.id})};
  $("#spd").onclick=()=>epDownload(s,e,k,v,$("#spm"),$("#spd"));
  const nx=$("#spn");if(nx)nx.onclick=()=>{close2();epPlay(sid,k+1)};
  const post=()=>{if(!need())return;const t=$("#sci").value.trim();if(!t)return;(e.cm=e.cm||[]).push({n:me.name,o:me.uid,t,ts:Date.now()});epSave(e);notify(e.o,"commented on your episode: "+t.slice(0,40));draw()};
  $("#scs").onclick=post;$("#sci").onkeydown=ev=>{if(ev.key==="Enter"){ev.preventDefault();post()}};
  $("#spb").querySelectorAll("[data-cd]").forEach(b=>b.onclick=()=>{e.cm.splice(+b.dataset.cd,1);epSave(e);draw()});
  $("#spb").querySelectorAll("[data-go]").forEach(b=>b.onclick=()=>{close2();epPlay(sid,+b.dataset.go)});
 };
 draw();
}
async function epDownload(s,e,k,pv,msg,btn){
 const say=t=>{msg.style.display="block";msg.textContent=t};
 if(typeof MediaRecorder==="undefined"){say("Downloads with the watermark are not supported on this phone's browser.");return}
 pv.pause();btn.disabled=true;
 try{
  const v=document.createElement("video");v.crossOrigin="anonymous";v.playsInline=true;v.src=e.url;v.preload="auto";
  await new Promise((ok,no)=>{v.onloadedmetadata=ok;v.onerror=()=>no(new Error("load"))});
  const W=v.videoWidth||720,H=v.videoHeight||1280,sc=Math.min(1,960/Math.max(W,H)),cw=Math.round(W*sc/2)*2,ch=Math.round(H*sc/2)*2;
  const cv=document.createElement("canvas");cv.width=cw;cv.height=ch;const g=cv.getContext("2d");
  const cs=cv.captureStream(30);let vs=null;
  try{vs=v.captureStream?v.captureStream():(v.mozCaptureStream?v.mozCaptureStream():null)}catch(x){}
  if(vs)vs.getAudioTracks().forEach(t=>cs.addTrack(t));
  const types=["video/mp4;codecs=avc1.42E01E,mp4a.40.2","video/mp4","video/webm;codecs=vp9,opus","video/webm;codecs=vp8,opus","video/webm"];
  const mt=types.find(t=>MediaRecorder.isTypeSupported(t))||"";
  const rec=new MediaRecorder(cs,mt?{mimeType:mt,videoBitsPerSecond:2500000}:{videoBitsPerSecond:2500000}),parts=[];
  rec.ondataavailable=ev=>{if(ev.data&&ev.data.size)parts.push(ev.data)};
  const done=new Promise(ok=>rec.onstop=ok);
  const draw=()=>{try{g.drawImage(v,0,0,cw,ch);
   const s1=Math.max(14,Math.round(cw/26)),ph=Math.floor((v.currentTime/6)%4),right=ph%2===1,bot=ph>=2;
   g.save();g.globalAlpha=.9;g.shadowColor="rgba(0,0,0,.85)";g.shadowBlur=6;g.fillStyle="#fff";g.textAlign=right?"right":"left";
   const x=right?cw-s1:s1,y=bot?ch-s1*4.2:s1*3.2;
   g.font="bold "+s1+"px Arial,sans-serif";g.fillText("🌍 WorldLink",x,y);
   g.font=Math.round(s1*.75)+"px Arial,sans-serif";g.fillText("@"+e.u+" · worldlink.app",x,y+s1*1.15);
   g.restore();
   g.save();g.fillStyle="rgba(0,0,0,.45)";g.fillRect(0,ch-s1*2.2,cw,s1*2.2);g.fillStyle="#fff";g.font="bold "+Math.round(s1*.8)+"px Arial,sans-serif";g.textAlign="center";g.fillText(s.t+" · Episode "+(e.n||k+1)+" · worldlink.app",cw/2,ch-s1*.75);g.restore()}catch(x){}};
  const iv=setInterval(()=>{draw();if(v.duration)say("Saving with the WorldLink watermark… "+Math.min(99,Math.round(v.currentTime/v.duration*100))+"%. Keep this screen open.")},33);
  rec.start(1000);v.currentTime=0;await v.play();
  await new Promise(ok=>{v.onended=ok;v.onerror=ok});
  clearInterval(iv);draw();rec.stop();await done;
  const ext=/mp4/.test(rec.mimeType||mt)?"mp4":"webm",blob=new Blob(parts,{type:rec.mimeType||mt||"video/webm"});
  if(!blob.size)throw new Error("empty");
  const nm=("WorldLink-"+s.t.replace(/[^\w]+/g,"-")+"-ep"+(e.n||k+1)+"."+ext).replace(/-+/g,"-");
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=nm;a.setAttribute("data-direct","1");document.body.appendChild(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href),60000);
  say("✓ Saved "+nm+" to your downloads.");
 }catch(x){say("Could not make the watermarked download on this phone. Please try again, or use a newer browser.")}
 btn.disabled=false;
}
