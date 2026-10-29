import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function bgPost' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70])
    s=s.replace(a,b)
code=r'''
/* ===== Background posting: tap Post, keep using the app; a progress circle at the top shows the upload ===== */
let BGB=false;
function bgRing(p,state,txt){
 let el=$("#bgr");
 if(!el){el=document.createElement("div");el.id="bgr";el.setAttribute("role","status");el.style.cssText="position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 62px);transform:translateX(-50%);z-index:99999;display:flex;align-items:center;gap:8px;background:rgba(10,14,30,.92);color:#fff;border-radius:999px;padding:6px 14px 6px 6px;box-shadow:0 4px 16px rgba(0,0,0,.4);font:700 13px system-ui,sans-serif";document.body.appendChild(el)}
 clearTimeout(el.__t);
 const C=2*Math.PI*16,pc=Math.max(0,Math.min(1,p||0)),col=state==="err"?"#E5233A":state==="ok"?"#34C759":"#FF7A1A";
 const mid=state==="err"?"!":state==="ok"?"✓":Math.round(pc*100)+"%";
 el.innerHTML=`<svg width="40" height="40" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="16" fill="none" stroke="rgba(255,255,255,.2)" stroke-width="4"/><circle cx="20" cy="20" r="16" fill="none" stroke="${col}" stroke-width="4" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C*(1-(state?1:pc))}" transform="rotate(-90 20 20)"${state?"":' style="transition:stroke-dashoffset .3s"'}/><text x="20" y="24.5" text-anchor="middle" font-size="${state?15:11}" font-weight="800" fill="#fff" font-family="system-ui,sans-serif">${mid}</text></svg><span>${esc(txt||"")}</span>`;
 el.style.display="flex";
 if(state==="ok")el.__t=setTimeout(()=>{el.style.display="none"},2600);
 return el;
}
async function bgPost(f,cap){
 if(BGB){bgRing(0,"err","Another video is still uploading");return}
 const css=PFX,tx=CAP;PFX="";CAP=null;BGB=true;
 close();
 const fail=(msg,retry)=>{BGB=false;const el=bgRing(0,"err",msg);el.onclick=()=>{el.onclick=null;el.style.display="none";retry&&retry()}};
 const run=async src=>{
  try{
   let nf=src;const burn=!!(css||tx);
   if(burn){bgRing(0,"","Adding your edits");nf=await captionVideo(src,css,tx,(t,d)=>bgRing(d?.45*t/d:0,"","Adding your edits"))}
   if(nf.size>20*1048576)return fail("Video is over 20 MB. Tap to trim it",()=>{secFull=true;editVideo(nf,true)});
   bgRing(burn?.45:0,"","Uploading");
   const it={id:"v"+Date.now(),u:me.name,uid:me.uid,c:cap||"My first WorldLink video",m:"Original sound - "+me.name,l:0,g:["#222","#444"],e:"🎬",cm:[],src:URL.createObjectURL(nf)};
   let saved=false;
   try{const A=await claude.use("assets"),D=await claude.use("db");
    if(A&&D){const r=await A.upload(nf,q=>bgRing((burn?.45:0)+q*(burn?.55:1),"","Uploading"));it.src=r.url;await D.collection("videos").doc(it.id).set({id:it.id,url:r.url,c:it.c,u:me.name,uid:me.uid||null,ts:Date.now()});saved=true}}
   catch(e){if(me.uid)return fail("Upload failed. Tap to try again",()=>run(nf))}
   add(it);BGB=false;
   bgRing(1,"ok",saved?"Posted":"Posted on this screen only");
  }catch(e){fail("Could not finish. Tap to try again",()=>run(src))}
 };
 run(f);
}
'''
rep('function postForm(f,note){',code+'function postForm(f,note){')
rep(' $("#go").onclick=()=>postWithFilter(f,$("#cp").value.trim());',' $("#go").onclick=()=>{if(f.size>20*1048576&&!(PFX||CAP)){postVideo(f,$("#cp").value.trim());return}bgPost(f,$("#cp").value.trim())};')
# build stamp in main menu
rep('<p class="mute">Everything in one app.</p>','<p class="mute">Everything in one app.</p><p class="note" style="margin:-8px 0 8px;font-size:11px;opacity:.6">Version 2026.10.29-d</p>')
open(p,'w',encoding='utf8').write(s);print('patched')
