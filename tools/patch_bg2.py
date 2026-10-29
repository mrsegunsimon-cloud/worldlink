import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function jPut' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70])
    s=s.replace(a,b)
i=s.find('/* ===== Background posting');j=s.find('function postForm(f,note){')
assert 0<i<j
code=r'''/* ===== Background posting: a small draggable circle shows the upload; survives page refresh ===== */
let BGB=false;
const JDB=()=>new Promise((ok,no)=>{try{const r=indexedDB.open("wl_jobs",1);r.onupgradeneeded=()=>r.result.createObjectStore("j",{keyPath:"id"});r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)}catch(e){no(e)}});
async function jTx(mode,fn){try{const d=await JDB();return await new Promise((ok,no)=>{const t=d.transaction("j",mode),r=fn(t.objectStore("j"));t.oncomplete=()=>ok(r&&r.result);t.onerror=()=>no(t.error)})}catch(e){return null}}
const jPut=j=>jTx("readwrite",o=>o.put(j)),jDel=id=>jTx("readwrite",o=>o.delete(id)),jAll=async()=>(await jTx("readonly",o=>o.getAll()))||[];
function bgPos(el){let q=null;try{q=JSON.parse(localStorage.getItem("wl_ring")||"null")}catch(e){}
 const W=innerWidth,H=innerHeight,x=q?Math.min(Math.max(0,q.x),W-56):W/2-28,y=q?Math.min(Math.max(0,q.y),H-56):70;el.style.left=x+"px";el.style.top=y+"px"}
function bgRing(p,state,txt){
 let el=$("#bgr");
 if(!el){
  el=document.createElement("div");el.id="bgr";el.setAttribute("role","status");
  el.style.cssText="position:fixed;z-index:99999;width:56px;height:56px;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none";
  document.body.appendChild(el);bgPos(el);
  let sx=0,sy=0,ox=0,oy=0,mv=false,dn=false;
  el.addEventListener("pointerdown",e=>{dn=true;mv=false;sx=e.clientX;sy=e.clientY;ox=el.offsetLeft;oy=el.offsetTop;try{el.setPointerCapture(e.pointerId)}catch(_){}});
  el.addEventListener("pointermove",e=>{if(!dn)return;const dx=e.clientX-sx,dy=e.clientY-sy;if(Math.abs(dx)+Math.abs(dy)>6)mv=true;if(mv){el.style.left=Math.min(Math.max(0,ox+dx),innerWidth-56)+"px";el.style.top=Math.min(Math.max(0,oy+dy),innerHeight-56)+"px"}});
  const up=()=>{if(!dn)return;dn=false;if(mv){try{localStorage.setItem("wl_ring",JSON.stringify({x:el.offsetLeft,y:el.offsetTop}))}catch(_){}}else if(el.__tap){const f=el.__tap;el.__tap=null;f()}};
  el.addEventListener("pointerup",up);el.addEventListener("pointercancel",()=>{dn=false});
 }
 clearTimeout(el.__t);
 const R=23,C=2*Math.PI*R,pc=Math.max(0,Math.min(1,p||0)),col=state==="err"?"#E5233A":state==="ok"?"#34C759":"#FF7A1A";
 const mid=state==="err"?"!":state==="ok"?"✓":Math.round(pc*100)+"%";
 el.setAttribute("aria-label",txt||"Uploading");el.title=txt||"";
 el.innerHTML=`<svg width="56" height="56" viewBox="0 0 56 56" style="display:block;border-radius:50%;background:#0E1330;box-shadow:0 4px 14px rgba(0,0,0,.45)" aria-hidden="true"><circle cx="28" cy="28" r="${R}" fill="none" stroke="#3a4170" stroke-width="5"/><circle cx="28" cy="28" r="${R}" fill="none" stroke="${col}" stroke-width="5" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C*(1-(state?1:pc))}" transform="rotate(-90 28 28)"/><text x="28" y="${state?34:32.5}" text-anchor="middle" font-size="${state?20:13}" font-weight="800" fill="#ffffff" font-family="system-ui,sans-serif">${mid}</text></svg>${state&&txt?`<span style="position:absolute;top:60px;left:50%;transform:translateX(-50%);white-space:nowrap;background:#0E1330;color:#fff;padding:4px 10px;border-radius:999px;font:700 12px system-ui,sans-serif">${esc(txt)}</span>`:""}`;
 el.style.display="block";el.__tap=null;
 if(state==="ok")el.__t=setTimeout(()=>{el.style.display="none"},2600);
 return el;
}
async function bgRun(job){
 BGB=true;
 const fail=(msg,retry)=>{BGB=false;const el=bgRing(0,"err",msg);el.__tap=()=>{el.style.display="none";retry&&retry()}};
 try{
  const burn=!!(job.css||job.tx);let nf=job.burned||job.f;
  if(burn&&!job.burned){bgRing(0,"","Adding your edits");nf=await captionVideo(job.f,job.css,job.tx,(t,d)=>bgRing(d?.45*t/d:0,"","Adding your edits"));job.burned=nf;await jPut(job)}
  if(nf.size>20*1048576){await jDel(job.id);BGB=false;return fail("Over 20 MB. Tap to trim",()=>{secFull=true;editVideo(nf,true)})}
  if(window.WLCloud&&!window.__wlUser){for(let i=0;i<24&&!window.__wlUser;i++)await new Promise(r=>setTimeout(r,500));if(!window.__wlUser)return fail("Sign in to finish",()=>bgRun(job))}
  const base=burn?.45:0;bgRing(base,"","Uploading");
  const it={id:job.id,u:me.name,uid:me.uid,c:job.cap||"My first WorldLink video",m:"Original sound - "+me.name,l:0,g:["#222","#444"],e:"🎬",cm:[],src:URL.createObjectURL(nf)};
  let saved=false;
  try{const A=await claude.use("assets"),D=await claude.use("db");
   if(A&&D){const r=await A.upload(nf,q=>bgRing(base+q*(1-base),"","Uploading"));it.src=r.url;await D.collection("videos").doc(it.id).set({id:it.id,url:r.url,c:it.c,u:me.name,uid:me.uid||null,ts:Date.now()});saved=true}}
  catch(e){return fail("Upload failed. Tap to retry",()=>bgRun(job))}
  if(!saved)return fail("Not saved. Tap to retry",()=>bgRun(job));
  await jDel(job.id);
  if(!CLIPS.some(c=>c.id===it.id))add(it);BGB=false;
  bgRing(1,"ok","Posted");
 }catch(e){fail("Could not finish. Tap to retry",()=>bgRun(job))}
}
async function bgPost(f,cap){
 if(BGB){bgRing(0,"err","Another upload is running");return}
 const job={id:"v"+Date.now(),cap,css:PFX,tx:CAP,f,burned:null,ts:Date.now()};PFX="";CAP=null;
 try{document.querySelectorAll("#panel video").forEach(v=>{v.pause();v.removeAttribute("src");v.load()})}catch(e){}
 close();try{$("#panel").innerHTML=""}catch(e){}
 bgRing(0,"","Starting");
 await jPut(job);bgRun(job);
}
async function bgResume(){
 try{const L=await jAll();if(!L.length||BGB)return;L.sort((a,b)=>a.ts-b.ts);const j=L[0];
  if(Date.now()-j.ts>7*864e5){await jDel(j.id);return}
  bgRing(0,"","Resuming");bgRun(j)}catch(e){}
}
window.addEventListener("load",()=>setTimeout(bgResume,2500));
'''
s=s[:i]+code+s[j:]
# card sound
a='let HCGO={};'
assert s.count(a)==1
snd=r'''let CSND=(()=>{try{return localStorage.getItem("wl_csnd")!=="0"}catch(e){return true}})(),CAU=null,CIO=null;
function cChime(kind){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;CAU=CAU||new AC();if(CAU.state==="suspended")CAU.resume();
 const Q={news:[[660,0],[880,.14]],sports:[[784,0],[784,.12],[1047,.26]],social:[[523,0],[659,.1],[784,.2]],market:[[1319,0],[1760,.09]],events:[[523,0],[659,.1],[784,.2],[1047,.3]],music:[[392,0],[494,.1],[587,.2],[784,.3]],campus:[[440,0],[554,.12],[659,.24]],explore:[[587,0],[740,.14],[880,.28]],learn:[[523,0],[784,.15]],play:[[880,0],[1109,.08],[1319,.16],[1760,.24]]}[kind]||[[660,0]];
 Q.forEach(([f,t])=>{const o=CAU.createOscillator(),g=CAU.createGain(),t0=CAU.currentTime+t;o.type="triangle";o.frequency.value=f;g.gain.setValueAtTime(0,t0);g.gain.linearRampToValueAtTime(.2,t0+.02);g.gain.exponentialRampToValueAtTime(.001,t0+.4);o.connect(g);g.connect(CAU.destination);o.start(t0);o.stop(t0+.45)})}catch(e){}}
function cSpeak(txt){try{if(!window.speechSynthesis)return;speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(txt);setTimeout(()=>{try{speechSynthesis.speak(u)}catch(e){}},600)}catch(e){}}
function cStop(){try{window.speechSynthesis&&speechSynthesis.cancel()}catch(e){}}
function cPlay(el){if(!CSND||!el)return;cChime(el.dataset.kind);cSpeak(el.dataset.say||"")}
function cSndBtn(){return `<button data-csnd="1" aria-label="Sound on or off" style="position:absolute;top:70px;right:14px;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,.5);color:#fff;font-size:20px;z-index:3">${CSND?"🔊":"🔇"}</button>`}
let HCGO={};'''
s=s.replace(a,snd)
rep('el.dataset.hc=c.k+n;','el.dataset.hc=c.k+n;el.dataset.kind=c.k;el.dataset.say=c.lab+". "+c.h+". "+c.sub;')
rep('<span style="display:inline-block;background:rgba(0,0,0,.45);padding:5px 12px;border-radius:999px;font-weight:700;font-size:13px">${c.ic} ${esc(c.lab)}</span>','${cSndBtn()}<span style="display:inline-block;background:rgba(0,0,0,.45);padding:5px 12px;border-radius:999px;font-weight:700;font-size:13px">${c.ic} ${esc(c.lab)}</span>')
rep('   clips[k].after(el);\n  }\n ','   clips[k].after(el);\n  }\n  try{if(CIO)CIO.disconnect();CIO=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)cPlay(e.target);else cStop()}),{root:f,threshold:.7});f.querySelectorAll(".hc").forEach(x=>CIO.observe(x))}catch(e){}\n ')
rep('$("#feed").addEventListener("click",e=>{const h=e.target.closest(".hc");if(h&&HCGO[h.dataset.hc])HCGO[h.dataset.hc]()});','$("#feed").addEventListener("click",e=>{const sb=e.target.closest("[data-csnd]");if(sb){e.stopPropagation();CSND=!CSND;try{localStorage.setItem("wl_csnd",CSND?"1":"0")}catch(_){}document.querySelectorAll("[data-csnd]").forEach(b=>b.textContent=CSND?"🔊":"🔇");if(CSND)cPlay(sb.closest(".hc"));else cStop();return}const h=e.target.closest(".hc");if(h&&HCGO[h.dataset.hc])HCGO[h.dataset.hc]()});')
rep('Version 2026.10.29-d','Version 2026.10.29-e')
open(p,'w',encoding='utf8').write(s);print('patched')
