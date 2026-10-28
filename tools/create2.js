/* Create 2: genre+search music picker, photo posting, filters for photos and videos */
const GEN=[["Afrobeat","afrobeats",""],["Amapiano","amapiano",""],["Gospel","gospel worship",""],["Highlife","highlife",""],["Hip-hop","hip hop","Hip-Hop/Rap"],["R&B","r&b soul","R&B/Soul"],["Pop","pop","Pop"],["Reggae","reggae","Reggae"],["Dancehall","dancehall","Dancehall"],["Country","country","Country"],["Blues","blues","Blues"],["Jazz","jazz","Jazz"],["Rock","rock","Rock"],["Latin","latin","Latin"],["Lo-fi","lofi","Lo-Fi"],["Classical","classical","Classical"]];
let SPL=[];
async function spLoad(q,genre){
 const box=$("#spr");if(!box)return;
 box.innerHTML='<p class="mute">Loading music…</p>';
 const E=encodeURIComponent(q||"");
 const u=(genre&&!q)?`https://api.audius.co/v1/tracks/trending?app_name=WorldLink&limit=15&time=week&genre=${encodeURIComponent(genre)}`:`https://api.audius.co/v1/tracks/search?query=${E}&app_name=WorldLink&limit=15`;
 let d=typeof dsGet==="function"?await dsGet(u):null;
 if(!$("#spr"))return;
 let A=((d&&d.data)||[]).filter(x=>x&&x.id&&x.is_streamable!==false);
 if(!A.length&&genre&&!q&&typeof dsGet==="function"){d=await dsGet(`https://api.audius.co/v1/tracks/search?query=${encodeURIComponent(genre)}&app_name=WorldLink&limit=15`);A=((d&&d.data)||[]).filter(x=>x&&x.id&&x.is_streamable!==false)}
 if(!$("#spr"))return;
 SPL=A.map(x=>({t:x.title||"Untitled",a:(x.user&&x.user.name)||"",url:`https://api.audius.co/v1/tracks/${encodeURIComponent(x.id)}/stream?app_name=WorldLink`}));
 box.innerHTML=SPL.length?SPL.map((x,k)=>`<div class="cm" style="display:flex;align-items:center;gap:8px"><div style="flex:1;min-width:0"><b>${esc(x.t)}</b><div class="mute" style="font-size:12px">${esc(x.a)}</div></div><button class="btn ghost" data-xp="${k}" style="width:auto;margin:0;padding:8px 12px">▶</button><button class="btn" data-xu="${k}" style="width:auto;margin:0;padding:8px 12px">Use</button></div>`).join(""):'<p class="mute">No free songs found. Try another word or genre.</p>';
 box.querySelectorAll("[data-xp]").forEach(b=>b.onclick=()=>sndPrev(SPL[+b.dataset.xp].url));
 box.querySelectorAll("[data-xu]").forEach(b=>b.onclick=()=>{const x=SPL[+b.dataset.xu];SND={name:x.t+(x.a?" · "+x.a:""),url:x.url};spBack()});
}
let spBack=()=>{};
function soundPicker(cb){
 const L=songList();
 open(`<h2>Choose music</h2><p class="note" style="margin:0 0 6px">Pick a type of music, or search any song or artist. Free songs only.</p>${SND?`<button class="btn ghost" id="sno">Remove music (${esc(SND.name)})</button>`:""}<div style="display:flex;gap:8px"><input class="in" id="sq" maxlength="60" placeholder="Search music" aria-label="Search music" style="margin:0"><button class="btn" id="sg" style="width:auto;margin:0;padding:8px 16px">Search</button></div><div style="display:flex;gap:6px;overflow-x:auto;padding:10px 0">${GEN.map((g,i)=>`<button data-gn="${i}" style="flex:none;padding:8px 14px;border-radius:999px;border:1px solid var(--line);color:inherit;font-weight:600">${g[0]}</button>`).join("")}</div><div id="spr"></div><h3 style="margin:14px 0 4px;font-size:15px">WorldLink free library</h3>${L.map((x,k)=>`<div class="cm" style="display:flex;align-items:center;gap:8px"><div style="flex:1;min-width:0"><b>${esc(x.t)}</b><div class="mute" style="font-size:12px">${esc(x.a||"")}</div></div><button class="btn ghost" data-sp="${k}" style="width:auto;margin:0;padding:8px 12px">▶</button><button class="btn" data-su="${k}" style="width:auto;margin:0;padding:8px 12px">Use</button></div>`).join("")||'<p class="mute">No sounds yet.</p>'}<button class="btn ghost" id="sbk">Back</button>`);
 const back=()=>{sndPrev(null);cb?cb():recorder()};spBack=back;
 $("#sbk").onclick=back;
 const so=$("#sno");if(so)so.onclick=()=>{SND=null;back()};
 $("#panel").querySelectorAll("[data-sp]").forEach(b=>b.onclick=()=>sndPrev(L[+b.dataset.sp].url));
 $("#panel").querySelectorAll("[data-su]").forEach(b=>b.onclick=()=>{const x=L[+b.dataset.su];SND={name:x.t+(x.a?" · "+x.a:""),url:x.url};back()});
 $("#panel").querySelectorAll("[data-gn]").forEach(b=>b.onclick=()=>{const g=GEN[+b.dataset.gn];$("#panel").querySelectorAll("[data-gn]").forEach(x=>x.style.background="");b.style.background="var(--bg)";spLoad(g[1],"");if(g[2])spLoad("",g[2])});
 const go=()=>{const q=$("#sq").value.trim();if(q)spLoad(q,"")};
 $("#sg").onclick=go;$("#sq").onkeydown=e=>{if(e.key==="Enter")go()};
 spLoad("","Pop");
}
/* ---- filters ---- */
let PFX="";
const fxStrip=()=>`<div id="fxs" style="display:flex;gap:6px;overflow-x:auto;padding:6px 0">${FX.map((f,i)=>`<button data-pf="${i}" style="flex:none;padding:6px 12px;border-radius:999px;border:1px solid rgba(128,128,128,.5);font-weight:600;font-size:13px;color:inherit;background:${f[1]===PFX?"rgba(128,128,128,.35)":"transparent"}">${f[0]}</button>`).join("")}</div>`;
function fxWire(el){
 document.querySelectorAll("[data-pf]").forEach(b=>b.onclick=()=>{PFX=FX[+b.dataset.pf][1];if(el)el.style.filter=PFX;document.querySelectorAll("[data-pf]").forEach(x=>x.style.background=FX[+x.dataset.pf][1]===PFX?"rgba(128,128,128,.35)":"transparent")});
}
function bakePhoto(f,css){
 return new Promise(ok=>{
  if(!css)return ok(f);
  try{const im=new Image();im.onerror=()=>ok(f);im.onload=()=>{try{const m=Math.min(1,1600/Math.max(im.width,im.height)),c=document.createElement("canvas");c.width=Math.round(im.width*m);c.height=Math.round(im.height*m);const x=c.getContext("2d");if(!("filter" in x))return ok(f);x.filter=css;x.drawImage(im,0,0,c.width,c.height);c.toBlob(b=>ok(b?new File([b],"photo.jpg",{type:"image/jpeg"}):f),"image/jpeg",.88)}catch(e){ok(f)}};im.src=URL.createObjectURL(f)}catch(e){ok(f)}
 });
}
function filterVideo(f,css,prog){
 return new Promise((ok,no)=>{
  try{
   if(!window.MediaRecorder)return no(new Error("This phone cannot add filters."));
   const v=document.createElement("video");v.src=URL.createObjectURL(f);v.playsInline=true;v.preload="auto";v.onerror=()=>no(new Error("The video could not be read."));
   v.onloadedmetadata=async()=>{
    try{
     const k=Math.min(1,960/Math.max(v.videoWidth,v.videoHeight)),W=Math.round(v.videoWidth*k)||720,H=Math.round(v.videoHeight*k)||1280,c=document.createElement("canvas");c.width=W;c.height=H;const x=c.getContext("2d");
     if(!("filter" in x))return no(new Error("Filters on videos need Chrome or the Android app."));
     const AC=window.AudioContext||window.webkitAudioContext;let ac=null,tracks=[];
     if(AC){try{ac=new AC();const d=ac.createMediaStreamDestination();ac.createMediaElementSource(v).connect(d);tracks=d.stream.getAudioTracks()}catch(e){ac=null}}
     const out=new MediaStream([...c.captureStream(25).getVideoTracks(),...tracks]);
     const mt=["video/mp4","video/webm;codecs=vp9,opus","video/webm"].find(m=>MediaRecorder.isTypeSupported(m))||"";
     const rc=new MediaRecorder(out,mt?{mimeType:mt,videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{}),ch=[];
     rc.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};
     let run=true;const draw=()=>{if(!run)return;x.filter=css;x.drawImage(v,0,0,W,H);if(prog)prog(v.currentTime,v.duration);requestAnimationFrame(draw)};
     rc.onstop=()=>{run=false;try{ac&&ac.close()}catch(e){}const type=(rc.mimeType||mt||"video/webm").split(";")[0];ok(new File(ch,"filtered."+(type.includes("mp4")?"mp4":"webm"),{type}))};
     v.onended=()=>{if(rc.state==="recording")rc.stop()};
     rc.start();draw();await v.play()
    }catch(e){no(e)}
   };
  }catch(e){no(e)}
 })
}
async function postWithFilter(f,cap){
 if(!PFX)return postVideo(f,cap);
 const css=PFX;
 open(`<h2>Adding your filter</h2><p class="mute">This takes about as long as the video. Keep this screen open.</p><div style="height:8px;border-radius:4px;background:var(--line)"><div id="mb" style="height:100%;width:0;border-radius:4px;background:var(--acc)"></div></div>`);
 try{const nf=await filterVideo(f,css,(t,d)=>{const b=$("#mb");if(b&&d)b.style.width=Math.min(100,Math.round(100*t/d))+"%"});PFX="";postFormPost(nf,cap)}
 catch(e){PFX="";postForm(f,"Could not add the filter: "+(e.message||"try again"))}
}
function postFormPost(nf,cap){open('<h2>Posting…</h2><p class="note" id="st"></p><button class="btn" id="go" style="display:none">x</button>');postVideo(nf,cap)}
