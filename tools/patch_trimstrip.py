import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlTrimStrip" in s: print("already");sys.exit(0)
i=s.find("function editVideo(f,big){")
j=s.find("\n/* ===== Text on videos",i)
assert i>0 and j>i
NEW=r'''/* wlTrimStrip: film-strip trimmer (WhatsApp style). The cut itself happens later in the background, so Done is instant. */
var VTRIM=null;
function editVideo(f,big){
 const url=URL.createObjectURL(f);const pv=(VTRIM&&VTRIM.f===f)?VTRIM:null;
 let st=pv?pv.st:0,en=pv?pv.en:0,du=0,sh=pv?pv.sh:0,pos=pv?pv.pos:.5,W=0;
 const hd=document.createElement("video");hd.muted=true;hd.playsInline=true;hd.preload="auto";hd.src=url;
 const sz=b=>b>=1048576?(b/1048576).toFixed(1)+" MB":Math.max(1,Math.round(b/1024))+" KB";
 const hh=`position:absolute;top:-3px;bottom:-3px;width:16px;background:#fff;touch-action:none;display:grid;place-items:center`;
 openFull(`<div style="height:100%;display:flex;flex-direction:column;background:#000;color:#fff;padding:0 0 calc(12px + env(safe-area-inset-bottom))"><div style="display:flex;align-items:center;justify-content:space-between;padding:10px 12px"><button id="ebk" aria-label="Cancel" style="color:#fff;font-size:26px;width:44px;height:44px">✕</button><b id="evt" style="font-size:15px;background:rgba(255,255,255,.14);padding:7px 14px;border-radius:999px">Loading…</b><button id="edn" aria-label="Done" style="width:44px;height:44px;border-radius:50%;background:#25D366;color:#fff;font-size:22px;font-weight:800">✓</button></div><div style="flex:1;min-height:0;display:grid;place-items:center;padding:0 10px"><div id="vbox" style="max-height:100%;max-width:100%;height:100%;aspect-ratio:9/16;border-radius:10px;overflow:hidden;background:#111"><video id="evv" src="${url}" playsinline loop muted autoplay style="width:100%;height:100%;object-fit:cover"></video></div></div><p id="est" class="note" style="color:#FFB454;text-align:center;margin:6px 12px 0;min-height:16px"></p><div id="stw" style="position:relative;height:58px;margin:10px 26px 8px;touch-action:none"><div id="stt" style="position:absolute;inset:0;display:flex;overflow:hidden;border-radius:4px;background:#222"></div><div id="sel" style="position:absolute;top:0;bottom:0;left:0;right:0;border-top:3px solid #fff;border-bottom:3px solid #fff;box-shadow:0 0 0 100vmax rgba(0,0,0,.55);clip-path:inset(-3px -100vmax)"><div id="shl" style="${hh};left:-16px;border-radius:6px 0 0 6px"><i style="width:3px;height:20px;background:#999;border-radius:2px"></i></div><div id="shr" style="${hh};right:-16px;border-radius:0 6px 6px 0"><i style="width:3px;height:20px;background:#999;border-radius:2px"></i></div></div></div><div id="esh" style="display:flex;gap:6px;overflow-x:auto;padding:4px 12px">${VSHAPES.map((q,k)=>`<button data-sh="${k}" style="flex:none;padding:6px 12px;border-radius:999px;font-weight:700;font-size:12px;background:${k===sh?"#fff":"rgba(255,255,255,.18)"};color:${k===sh?"#000":"#fff"}">${q[0]}</button>`).join("")}</div><label id="epw" style="display:none;font-size:12px;padding:0 14px">Move the picture<input id="ep" type="range" min="0" max="100" value="${Math.round(pos*100)}" style="width:100%"></label></div>`,true);
 const v=$("#evv"),T=$("#evt"),sel=$("#sel"),stw=$("#stw"),stt=$("#stt");
 const show=()=>{const n=du?f.size*(en-st)/du:0;T.textContent=vFmt(en-st)+" • "+sz(n);const o=$("#est");o.textContent=(n>20*1048576)?"Still over 20 MB. Drag the handles to keep about 30 to 60 seconds.":(big&&!pv&&n>20*1048576?"":"")};
 const place=()=>{W=stw.clientWidth;if(!du)return;sel.style.left=(st/du*W)+"px";sel.style.right=(W-en/du*W)+"px";show()};
 const box=()=>{const r=VSHAPES[sh][1]||((v.videoWidth||9)/(v.videoHeight||16));$("#vbox").style.aspectRatio=String(r);v.style.objectPosition=(r>=(v.videoWidth/v.videoHeight||1)?"50% "+Math.round(pos*100)+"%":Math.round(pos*100)+"% 50%");$("#epw").style.display=sh?"block":"none"};
 v.onloadedmetadata=async()=>{du=await vDur(v);if(!en||en>du)en=du;if(st>=en)st=0;place();box();v.currentTime=st;v.play().catch(()=>{});thumbs()};
 v.ontimeupdate=()=>{if(v.currentTime>=en||v.currentTime<st){v.currentTime=st}};
 let dead=false;
 const thumbs=async()=>{
  try{
   const w=stw.clientWidth||300,hgt=58,ar=9/16,n=Math.max(4,Math.ceil(w/(hgt*ar)));
   const cs=[];for(let k=0;k<n;k++){const c=document.createElement("canvas");c.width=Math.round(w/n*2);c.height=hgt*2;c.style.cssText="flex:1;min-width:0;height:100%;object-fit:cover;background:#333";stt.appendChild(c);cs.push(c)}
   await new Promise(r=>{if(hd.readyState>=1)r();else{hd.onloadedmetadata=r;setTimeout(r,4000)}});
   const d=hd.duration||du;if(!isFinite(d)||!d)return;
   for(let k=0;k<n&&!dead;k++){
    await new Promise(r=>{let t=setTimeout(r,2500);hd.onseeked=()=>{clearTimeout(t);r()};hd.currentTime=Math.min(d-.05,(k+.5)/n*d)});
    try{const c=cs[k],x=c.getContext("2d"),vw=hd.videoWidth,vh=hd.videoHeight;if(!vw)continue;const q=Math.max(c.width/vw,c.height/vh),dw=vw*q,dh=vh*q;x.drawImage(hd,(c.width-dw)/2,(c.height-dh)/2,dw,dh)}catch(e){}
   }
  }catch(e){}
 };
 const drag=(el,which)=>{
  el.onpointerdown=e=>{
   e.preventDefault();e.stopPropagation();try{el.setPointerCapture(e.pointerId)}catch(_){}
   const r=stw.getBoundingClientRect();v.pause();
   el.onpointermove=m=>{
    if(!du)return;const t=Math.max(0,Math.min(du,(m.clientX-r.left)/r.width*du)),gap=Math.min(.5,du/2);
    if(which==="l"){st=Math.min(t,en-gap);v.currentTime=st}else{en=Math.max(t,st+gap);v.currentTime=Math.max(st,en-.3)}
    place()};
   const up=()=>{el.onpointermove=null;el.onpointerup=el.onpointercancel=null;v.currentTime=st;v.play().catch(()=>{})};
   el.onpointerup=el.onpointercancel=up};
 };
 drag($("#shl"),"l");drag($("#shr"),"r");
 $("#esh").onclick=e=>{const b=e.target.closest("[data-sh]");if(!b)return;sh=+b.dataset.sh;$("#esh").querySelectorAll("button").forEach(x=>{const on=x===b;x.style.background=on?"#fff":"rgba(255,255,255,.18)";x.style.color=on?"#000":"#fff"});box()};
 $("#ep").oninput=e=>{pos=+e.target.value/100;box()};
 window.addEventListener("resize",place);
 $("#ebk").onclick=()=>{dead=true;vedit(f)};
 $("#edn").onclick=()=>{
  if(!du)return;dead=true;
  if(!sh&&st<.05&&en>=du-.05){VTRIM=null;vedit(f);return}
  VTRIM={f,st,en,sh,pos};
  vedit(f,"Trimmed: "+(en-st).toFixed(1)+" seconds");
 };
}
'''
s=s[:i]+NEW+s[j:]
# vedit preview loops over the chosen part
a=' $("#vnx").onclick=()=>postForm(f,note);'
assert a in s
s=s.replace(a,' if(VTRIM&&VTRIM.f===f){const T=VTRIM;v.addEventListener("loadedmetadata",()=>{v.currentTime=T.st});v.addEventListener("timeupdate",()=>{if(v.currentTime>=T.en||v.currentTime<T.st-.3)v.currentTime=T.st})}else if(VTRIM&&VTRIM.f!==f)VTRIM=null;\n'+a,1)
# bgPost carries the trim
a='const job={id:"v"+Date.now(),cap,css:PFX,tx:OV(),f,burned:null,ts:Date.now()};'
assert a in s
s=s.replace(a,a+'if(VTRIM&&VTRIM.f===f)job.trim={st:VTRIM.st,en:VTRIM.en,sh:VTRIM.sh,pos:VTRIM.pos};VTRIM=null;',1)
# bgRun cuts first, in the background
a=' const burn=!!(job.css||job.tx);let nf=job.burned||job.f;'
assert a in s
s=s.replace(a,'''  if(job.trim){const T=job.trim;bgRing(0,"","Trimming");let c=null;
   if(!T.sh){try{c=await fastCut(job.f,T.st,T.en,q=>bgRing(.4*q,"","Trimming"))}catch(e){c=null}}
   if(!c)c=await trimCrop(job.f,T.st,T.en,VSHAPES[T.sh||0][1],T.pos==null?.5:T.pos,(t,d)=>bgRing(d?.4*Math.min(1,t/d):0,"","Trimming"));
   job.f=c;job.trim=null;job.burned=null;await jPut(job)}
'''+a,1)
open(P,"w",encoding="utf8").write(s)
print("ok")
