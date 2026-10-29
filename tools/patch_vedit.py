import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function vedit' in s: print('already');sys.exit()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80])
    s=s.replace(a,b)
code=r'''
/* ===== TikTok-style editor screen: Add sound, Edit, Text, Stickers, Filters, Save, Next ===== */
let STKL=[],VF=null;
const EMO=["😀","😂","🤣","😍","🥰","😎","🤩","😭","😡","😱","🤔","🙄","😴","🥳","🤯","🙏","👍","👏","🙌","💪","🔥","❤️","💯","✨","🎉","🎁","👑","💎","🌹","🌍","⭐","🏆","⚽","🏀","🎵","🎤","📸","🚀","💰","🍕","🍔","🎂","☀️","🌙","🌈","💥","👀","🤝","😘","🤗"];
function OV(){return (CAP||STKL.length)?Object.assign({},CAP||{t:""},{stk:STKL.map(x=>Object.assign({},x))}):null}
function vedit(f,note){
 stopCam();VF=f;const url=URL.createObjectURL(f);let sel=-1;
 const side=(id,ic,l)=>`<button id="${id}" aria-label="${l}" style="display:flex;align-items:center;justify-content:flex-end;gap:10px;width:100%;color:#fff;font-weight:700;font-size:14px;padding:8px 0;text-shadow:0 1px 4px #000"><span>${l}</span><span style="display:grid;place-items:center;width:44px;height:44px;border-radius:12px;background:rgba(255,255,255,.14);font-size:21px">${ic}</span></button>`;
 openFull(`<div style="position:relative;height:100%;background:#000;color:#fff;overflow:hidden"><div id="vst" style="position:absolute;left:0;right:0;top:78px;bottom:100px"><div id="vfr" style="position:absolute;left:0;top:0;width:100%;height:100%;overflow:hidden"><video id="vev" src="${url}" autoplay loop muted playsinline style="width:100%;height:100%;object-fit:contain;display:block;filter:${PFX||"none"}"></video></div></div><button id="vbk" aria-label="Back" style="position:absolute;left:10px;top:18px;width:46px;height:46px;font-size:28px;color:#fff">←</button><button id="vsn" style="position:absolute;left:50%;top:20px;transform:translateX(-50%);background:rgba(255,255,255,.16);color:#fff;border-radius:999px;padding:11px 20px;font-weight:700;font-size:15px;max-width:60%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">♪ ${note&&/Music/.test(note)?esc(note.replace("Music added: ","").slice(0,22)):"Add sound"}</button><div style="position:absolute;right:12px;top:96px;width:120px;z-index:4">${side("ved2","✂","Edit")}${side("vtx","Aa","Text")}${side("vsk","😊","Stickers")}${side("vfl","◎","Filters")}${side("vsv","⬇","Save")}</div><p id="vnt" style="position:absolute;left:14px;right:140px;bottom:112px;margin:0;color:#fff;font-size:13px;text-shadow:0 1px 4px #000">${note?esc(note):""}</p><div id="vfp" style="display:none;position:absolute;left:0;right:0;bottom:100px;background:rgba(0,0,0,.65);padding:10px 0;z-index:5"><div style="display:flex;gap:8px;overflow-x:auto;padding:2px 12px">${FX.map((q,k)=>`<button data-vf="${k}" style="flex:none;padding:8px 14px;border-radius:999px;font-weight:700;font-size:13px;background:${q[1]===PFX?"#fff":"rgba(255,255,255,.18)"};color:${q[1]===PFX?"#000":"#fff"}">${q[0]}</button>`).join("")}</div></div><div id="vsp" style="display:none;position:absolute;left:0;right:0;bottom:0;height:46%;background:#1c1c20;border-radius:18px 18px 0 0;z-index:6;padding:12px 12px 20px;overflow-y:auto"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px"><b>Stickers</b><button id="vspx" aria-label="Close" style="color:#fff;font-size:22px;padding:4px 10px">✕</button></div><div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px">${EMO.map((e,k)=>`<button data-ve="${k}" style="font-size:30px;padding:6px 0">${e}</button>`).join("")}</div></div><div id="vstb" style="display:none;position:absolute;left:50%;transform:translateX(-50%);bottom:112px;background:rgba(0,0,0,.7);border-radius:999px;padding:4px 8px;gap:4px;z-index:5"><button id="vsm" style="color:#fff;font-size:22px;padding:4px 12px">–</button><button id="vsp2" style="color:#fff;font-size:22px;padding:4px 12px">+</button><button id="vsd" style="color:#fff;font-size:18px;padding:4px 12px">🗑</button></div><div id="vds" style="display:none;position:absolute;left:12px;top:70px;background:#fff;color:#111;border-radius:14px;padding:6px;z-index:7;min-width:190px"><button id="vdc" style="display:block;width:100%;text-align:left;padding:12px;color:#E5233A;font-weight:700">🗑 Discard</button><button id="vdk" style="display:block;width:100%;text-align:left;padding:12px;font-weight:700">Keep editing</button></div><div style="position:absolute;left:12px;right:12px;bottom:calc(16px + env(safe-area-inset-bottom));z-index:3"><button id="vnx" style="width:100%;padding:15px;border-radius:999px;font-weight:800;font-size:17px;color:#fff;background:linear-gradient(90deg,#FE2C55,#c01a3a)">Next</button></div></div>`,true);
 const v=$("#vev"),fr=$("#vfr"),st=$("#vst");
 const fit=()=>{const vw=v.videoWidth,vh=v.videoHeight;if(!vw)return;const W=st.clientWidth,H=st.clientHeight,k=Math.min(W/vw,H/vh),w=Math.round(vw*k),h=Math.round(vh*k);fr.style.left=Math.round((W-w)/2)+"px";fr.style.top=Math.round((H-h)/2)+"px";fr.style.width=w+"px";fr.style.height=h+"px";draw()};
 const draw=()=>{const vw=v.videoWidth,vh=v.videoHeight;capLayer(fr,vw,vh,"contain",CAP);rs()};
 function rs(){
  fr.querySelectorAll(".stkd").forEach(x=>x.remove());
  STKL.forEach((q,i)=>{const d=document.createElement("div");d.className="stkd";d.textContent=q.e;
   d.style.cssText=`position:absolute;left:${q.x*100}%;top:${q.y*100}%;transform:translate(-50%,-50%);font-size:${Math.round(fr.clientWidth*q.s)}px;line-height:1;touch-action:none;cursor:grab;${i===sel?"outline:2px dashed #fff;outline-offset:4px;border-radius:8px":""}`;
   let dn=false,mv=false;
   d.addEventListener("pointerdown",e=>{dn=true;mv=false;sel=i;try{d.setPointerCapture(e.pointerId)}catch(_){};$("#vstb").style.display="flex";[...fr.querySelectorAll(".stkd")].forEach((x,j)=>x.style.outline=j===i?"2px dashed #fff":"none")});
   d.addEventListener("pointermove",e=>{if(!dn)return;mv=true;const r=fr.getBoundingClientRect();q.x=Math.min(1,Math.max(0,(e.clientX-r.left)/r.width));q.y=Math.min(1,Math.max(0,(e.clientY-r.top)/r.height));d.style.left=q.x*100+"%";d.style.top=q.y*100+"%"});
   d.addEventListener("pointerup",()=>{dn=false});d.addEventListener("pointercancel",()=>{dn=false});
   fr.appendChild(d)});
 }
 v.addEventListener("loadedmetadata",fit);if(v.videoWidth)fit();addEventListener("resize",fit);
 fr.onclick=e=>{if(!e.target.closest(".stkd")){sel=-1;$("#vstb").style.display="none";fr.querySelectorAll(".stkd").forEach(x=>x.style.outline="none")}};
 $("#vsm").onclick=()=>{if(sel>=0){STKL[sel].s=Math.max(.06,STKL[sel].s-.04);rs()}};
 $("#vsp2").onclick=()=>{if(sel>=0){STKL[sel].s=Math.min(.7,STKL[sel].s+.04);rs()}};
 $("#vsd").onclick=()=>{if(sel>=0){STKL.splice(sel,1);sel=-1;$("#vstb").style.display="none";rs()}};
 $("#vbk").onclick=()=>{const m=$("#vds");m.style.display=m.style.display==="none"?"block":"none"};
 $("#vdk").onclick=()=>{$("#vds").style.display="none"};
 $("#vdc").onclick=()=>{PFX="";CAP=null;STKL=[];create()};
 $("#ved2").onclick=()=>editVideo(f);
 $("#vtx").onclick=()=>capEditor(f,false,()=>vedit(f,note));
 $("#vfl").onclick=()=>{const q=$("#vfp");q.style.display=q.style.display==="none"?"block":"none";$("#vsp").style.display="none"};
 $("#vfp").onclick=e=>{const b=e.target.closest("[data-vf]");if(!b)return;PFX=FX[+b.dataset.vf][1];v.style.filter=PFX||"none";$("#vfp").querySelectorAll("button").forEach(x=>{const on=x===b;x.style.background=on?"#fff":"rgba(255,255,255,.18)";x.style.color=on?"#000":"#fff"})};
 $("#vsk").onclick=()=>{$("#vsp").style.display="block";$("#vfp").style.display="none"};
 $("#vspx").onclick=()=>{$("#vsp").style.display="none"};
 $("#vsp").onclick=e=>{const b=e.target.closest("[data-ve]");if(!b)return;STKL.push({e:EMO[+b.dataset.ve],x:.5,y:.5,s:.2});sel=STKL.length-1;$("#vsp").style.display="none";$("#vstb").style.display="flex";rs()};
 $("#vsn").onclick=()=>soundPicker(()=>{
  if(!SND)return vedit(f,note);
  const sd=SND;SND=null;
  open(`<h2>Adding music</h2><p class="mute" id="mp">Mixing "${esc(sd.name)}" into your video. Keep this screen open. It takes about as long as the video.</p><div style="height:8px;border-radius:4px;background:var(--line)"><div id="mb" style="height:100%;width:0;border-radius:4px;background:var(--acc)"></div></div>`);
  mixMusic(f,sd,(t,dur)=>{const b=$("#mb");if(b&&dur)b.style.width=Math.min(100,Math.round(100*t/dur))+"%"}).then(nf=>vedit(nf,"Music added: "+sd.name)).catch(e=>{vedit(f,"Could not add music: "+(e.message||"try again"))})
 });
 $("#vsv").onclick=async()=>{
  try{let out=f;const ov=OV();
   if(PFX||ov){bgRing(0,"","Saving");out=await captionVideo(f,PFX,ov,(t,d)=>bgRing(d?t/d:0,"","Saving"))}
   const a=document.createElement("a");a.href=URL.createObjectURL(out);a.download="worldlink-"+Date.now()+"."+((out.type||"").includes("mp4")?"mp4":"webm");document.body.appendChild(a);a.click();a.remove();bgRing(1,"ok","Saved")}
  catch(e){bgRing(0,"err","Could not save")}
 };
 $("#vnx").onclick=()=>postForm(f,note);
}
'''
rep('function postForm(f,note){',code+'function postForm(f,note){')
# stickers drawn by drawCap
rep(' const t=(c&&c.t||"").trim();if(!t)return;',' if(c&&c.stk&&c.stk.length){c.stk.forEach(q=>{x.save();x.font=Math.round(W*q.s)+"px serif";x.textAlign="center";x.textBaseline="middle";x.fillText(q.e,W*q.x,H*q.y);x.restore()})}\n const t=(c&&c.t||"").trim();if(!t)return;')
# capShow uses overlay
rep(' if(!CAP||!media)return;\n const go=()=>capLayer(host,media.videoWidth||media.naturalWidth,media.videoHeight||media.naturalHeight,fit,CAP);',' const o=OV();if(!o||!media)return;\n const go=()=>capLayer(host,media.videoWidth||media.naturalWidth,media.videoHeight||media.naturalHeight,fit,OV());')
# entries
rep('$("#cc").onchange=e=>{if(e.target.files[0])postForm(e.target.files[0])};','$("#cc").onchange=e=>{if(e.target.files[0])vedit(e.target.files[0])};')
rep('$("#cf").onchange=e=>{if(e.target.files[0])postForm(e.target.files[0])};','$("#cf").onchange=e=>{if(e.target.files[0])vedit(e.target.files[0])};')
rep('SND=null;postForm(new File(chunks,','SND=null;vedit(new File(chunks,')
rep('.then(vf=>postForm(vf,"Photo with music: "+sd.name))','.then(vf=>vedit(vf,"Photo with music: "+sd.name))')
rep('$("#ebk").onclick=()=>postForm(f);','$("#ebk").onclick=()=>vedit(f);')
rep('{postForm(f);return}','{vedit(f);return}')
rep('postForm(nf,"Edited: "+(en-st).toFixed(1)+" seconds")}','vedit(nf,"Edited: "+(en-st).toFixed(1)+" seconds")}')
# postForm becomes the Next/Post screen
rep(' $("#ved").onclick=()=>editVideo(f);',' {const fx=$("#fxs");if(fx)fx.style.display="none";["vcp","ved","pmu"].forEach(i=>{const e=$("#"+i);if(e)e.style.display="none"})}\n $("#ved").onclick=()=>editVideo(f);')
rep(' $("#bk").onclick=create;{const pv=$("#pvv");if(pv)pv.style.filter=PFX;fxWire(pv)}',' $("#bk").onclick=()=>vedit(f,note);{const pv=$("#pvv");if(pv)pv.style.filter=PFX;fxWire(pv)}')
# post job carries overlay (text + stickers)
rep('const job={id:"v"+Date.now(),cap,css:PFX,tx:CAP,f,burned:null,ts:Date.now()};PFX="";CAP=null;','const job={id:"v"+Date.now(),cap,css:PFX,tx:OV(),f,burned:null,ts:Date.now()};PFX="";CAP=null;STKL=[];')
rep(' PFX="";CAP=null;$("#gl").onclick=goLive;',' PFX="";CAP=null;STKL=[];$("#gl").onclick=goLive;')
rep('Version 2026.10.29-f','Version 2026.10.29-g')
open(p,'w',encoding='utf8').write(s);print('patched')
