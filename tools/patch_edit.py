import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function editVideo' in s: print('already');sys.exit()
a='<button class="btn ghost" id="pmu" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">'
assert s.count(a)==1
s=s.replace(a,'<button class="btn ghost" id="ved" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">✂ Trim, crop &amp; shape</button>'+a)
b=' $("#go").onclick=()=>postWithFilter(f,$("#cp").value.trim());\n $("#pmu").onclick=()=>soundPicker('
assert s.count(b)==1
s=s.replace(b,' $("#ved").onclick=()=>editVideo(f);\n'+b)
code=r'''
/* ===== Video editor: trim to the exact second, crop to a shape ===== */
const VSHAPES=[["Original",0],["Tall 9:16",9/16],["Square 1:1",1],["Photo 4:5",4/5],["Wide 16:9",16/9]];
function vFmt(t){t=Math.max(0,t||0);const m=Math.floor(t/60),r=t-m*60;return m+":"+(r<10?"0":"")+r.toFixed(1)}
function vDur(v){return new Promise(ok=>{if(isFinite(v.duration)&&v.duration>0)return ok(v.duration);v.currentTime=1e7;const h=()=>{v.removeEventListener("timeupdate",h);const d=v.duration;v.currentTime=0;ok(isFinite(d)?d:v.currentTime||0)};v.addEventListener("timeupdate",h)})}
function trimCrop(f,st,en,ratio,pos,prog){
 return new Promise((ok,no)=>{
  try{
   if(!window.MediaRecorder)return no(new Error("This phone cannot edit videos."));
   const v=document.createElement("video");v.src=URL.createObjectURL(f);v.playsInline=true;v.preload="auto";v.onerror=()=>no(new Error("The video could not be read."));
   v.onloadedmetadata=async()=>{
    try{
     const vw=v.videoWidth||720,vh=v.videoHeight||1280,r=ratio||vw/vh;
     let sw=vw,sh=vh;if(vw/vh>r)sw=vh*r;else sh=vw/r;
     const sx=(vw-sw)*(vw/vh>r?pos:.5),sy=(vh-sh)*(vw/vh>r?.5:pos);
     const k=Math.min(1,960/Math.max(sw,sh)),W=Math.round(sw*k)&~1||720,H=Math.round(sh*k)&~1||1280,c=document.createElement("canvas");c.width=W;c.height=H;const x=c.getContext("2d");
     const AC=window.AudioContext||window.webkitAudioContext;let ac=null,tracks=[];
     if(AC){try{ac=new AC();const d=ac.createMediaStreamDestination();ac.createMediaElementSource(v).connect(d);tracks=d.stream.getAudioTracks()}catch(e){ac=null}}
     const out=new MediaStream([...c.captureStream(25).getVideoTracks(),...tracks]);
     const mt=["video/mp4","video/webm;codecs=vp9,opus","video/webm"].find(m=>MediaRecorder.isTypeSupported(m))||"";
     const rc=new MediaRecorder(out,mt?{mimeType:mt,videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{}),ch=[];
     rc.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};
     let run=true;const draw=()=>{if(!run)return;x.drawImage(v,sx,sy,sw,sh,0,0,W,H);if(prog)prog(Math.max(0,v.currentTime-st),en-st);if(v.currentTime>=en-.03){run=false;v.pause();if(rc.state==="recording")rc.stop();return}requestAnimationFrame(draw)};
     rc.onstop=()=>{run=false;try{ac&&ac.close()}catch(e){}const type=(rc.mimeType||mt||"video/webm").split(";")[0];ok(new File(ch,"edited."+(type.includes("mp4")?"mp4":"webm"),{type}))};
     v.onended=()=>{if(rc.state==="recording")rc.stop()};
     await new Promise(res=>{v.onseeked=res;v.currentTime=st});
     rc.start();draw();await v.play()
    }catch(e){no(e)}
   };
  }catch(e){no(e)}
 })
}
function editVideo(f){
 const url=URL.createObjectURL(f);let st=0,en=0,du=0,sh=0,pos=.5;
 const hd=document.createElement("video");hd.src=url;hd.preload="metadata";
 openFull(`<div style="height:100%;overflow-y:auto;background:#000;color:#fff;padding:14px 16px calc(16px + env(safe-area-inset-bottom))"><h2 style="margin:0 0 10px;font-size:17px;text-align:center">Edit your video</h2><div id="vbox" style="margin:0 auto;max-height:46vh;aspect-ratio:9/16;max-width:100%;border-radius:12px;overflow:hidden;background:#111"><video id="evv" src="${url}" playsinline loop muted style="width:100%;height:100%;object-fit:cover"></video></div><p id="evt" class="note" style="color:#fff;text-align:center;margin:8px 0 2px">Loading…</p><label style="display:block;font-size:13px;margin-top:6px">Start<input id="es" type="range" min="0" max="100" step="0.1" value="0" style="width:100%"></label><label style="display:block;font-size:13px">End<input id="ee" type="range" min="0" max="100" step="0.1" value="100" style="width:100%"></label><div style="font-size:13px;margin-top:6px">Shape</div><div id="esh" style="display:flex;gap:6px;overflow-x:auto;padding:4px 0">${VSHAPES.map((q,k)=>`<button data-sh="${k}" style="flex:none;padding:7px 12px;border-radius:999px;font-weight:700;font-size:13px;background:${k===0?"#fff":"rgba(255,255,255,.18)"};color:${k===0?"#000":"#fff"}">${q[0]}</button>`).join("")}</div><label id="epw" style="display:none;font-size:13px">Move the picture<input id="ep" type="range" min="0" max="100" value="50" style="width:100%"></label><p class="note" id="est" style="color:#fff"></p><div style="display:flex;gap:8px"><button class="btn ghost" id="ebk" style="margin:0;flex:1;color:#fff;border-color:rgba(255,255,255,.5)">Back</button><button class="btn" id="edn" style="margin:0;flex:2">Done</button></div></div>`,true);
 const v=$("#evv"),S=$("#es"),E=$("#ee"),T=$("#evt");
 const show=()=>{T.textContent=vFmt(st)+" to "+vFmt(en)+"  ·  "+(en-st).toFixed(1)+" seconds"};
 const box=()=>{const r=VSHAPES[sh][1]||((v.videoWidth||9)/(v.videoHeight||16));$("#vbox").style.aspectRatio=String(r);v.style.objectPosition=(r>=(v.videoWidth/v.videoHeight||1)?"50% "+Math.round(pos*100)+"%":Math.round(pos*100)+"% 50%");$("#epw").style.display=sh?"block":"none"};
 v.onloadedmetadata=async()=>{du=await vDur(v);en=du;S.max=E.max=String(du);S.value="0";E.value=String(du);show();box();v.currentTime=0;v.play().catch(()=>{})};
 v.ontimeupdate=()=>{if(v.currentTime>=en||v.currentTime<st){v.currentTime=st}};
 S.oninput=()=>{st=Math.min(+S.value,en-.5);S.value=String(st);v.currentTime=st;show()};
 E.oninput=()=>{en=Math.max(+E.value,st+.5);E.value=String(en);v.currentTime=Math.max(st,en-1);show()};
 $("#esh").onclick=e=>{const b=e.target.closest("[data-sh]");if(!b)return;sh=+b.dataset.sh;$("#esh").querySelectorAll("button").forEach(x=>{const on=x===b;x.style.background=on?"#fff":"rgba(255,255,255,.18)";x.style.color=on?"#000":"#fff"});box()};
 $("#ep").oninput=e=>{pos=+e.target.value/100;box()};
 $("#ebk").onclick=()=>postForm(f);
 $("#edn").onclick=async()=>{
  if(!du){return}
  if(!sh&&st<.05&&en>=du-.05){postForm(f);return}
  $("#edn").disabled=true;v.pause();
  $("#est").textContent="Editing… keep this screen open. It takes about as long as the clip.";
  try{const nf=await trimCrop(f,st,en,VSHAPES[sh][1],pos,(t,d)=>{if(d>0)$("#est").textContent="Editing… "+Math.min(100,Math.round(100*t/d))+"%"});postForm(nf,"Edited: "+(en-st).toFixed(1)+" seconds")}
  catch(err){$("#edn").disabled=false;$("#est").textContent="Could not edit: "+(err.message||"try again")}
 };
}
'''
c='function postForm(f,note){'
assert s.count(c)==1
s=s.replace(c,code+c)
open(p,'w',encoding='utf8').write(s);print('patched')
