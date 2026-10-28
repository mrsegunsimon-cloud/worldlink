"""Full-screen post preview, and open / delete your own posts from the profile grid. Usage: patch_manage.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function myPost(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)

# 1. Post screen fills the whole phone screen
old=' open(`<h2>Post your video</h2><video src="${url}" controls playsinline style="width:100%;max-height:40vh;border-radius:12px;background:#000"></video><button class="btn ghost" id="pmu" style="margin-top:8px">♪ ${note?"Change music":"Add music"}</button><input class="in" id="cp" type="text" maxlength="100" placeholder="Write a caption" aria-label="Caption"><p class="note" id="st">${note?esc(note):""}</p><button class="btn" id="go">Post</button><button class="btn ghost" id="bk">Back</button>`);'
new=''' openFull(`<div style="position:relative;height:100%;background:#000;color:#fff"><video id="pvv" src="${url}" autoplay loop playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video><button id="pvt" aria-label="Play or pause" style="position:absolute;inset:0;width:100%;background:none"></button><div style="position:absolute;left:0;right:0;bottom:0;padding:40px 16px calc(16px + env(safe-area-inset-bottom));background:linear-gradient(transparent,rgba(0,0,0,.85));display:flex;flex-direction:column;gap:8px"><button class="btn ghost" id="pmu" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">♪ ${note?"Change music":"Add music"}</button><input class="in" id="cp" type="text" maxlength="100" placeholder="Write a caption" aria-label="Caption" style="margin:0"><p class="note" id="st" style="margin:0;color:#fff">${note?esc(note):""}</p><div style="display:flex;gap:8px"><button class="btn ghost" id="bk" style="margin:0;flex:1;color:#fff;border-color:rgba(255,255,255,.5)">Back</button><button class="btn" id="go" style="margin:0;flex:2">Post</button></div></div></div>`,true);
 {const pv=$("#pvv");if(pv){pv.play().catch(()=>{});$("#pvt").onclick=()=>{pv.paused?pv.play().catch(()=>{}):pv.pause()}}}'''
rep(old,new)

# 2. Profile tiles can be opened
rep('const tile=i=>{const c=CLIPS[i];return `<div>${c.src?','const tile=i=>{const c=CLIPS[i];return `<div data-ci="${i}" style="cursor:pointer">${c.src?')
rep(' $("#panel").querySelectorAll("[data-pt]").forEach(b=>b.onclick=()=>profile(b.dataset.pt));',
    ' $("#panel").querySelectorAll("[data-pt]").forEach(b=>b.onclick=()=>profile(b.dataset.pt));\n $("#panel").querySelectorAll("[data-ci]").forEach(d=>d.onclick=()=>myPost(+d.dataset.ci,tabk));')

fn='''function myPost(i,tabk,ask){
 const c=CLIPS[i];if(!c)return;
 const mine=!!(c.src&&(!c.uid||c.uid===me.uid));
 const bar=mine?(ask?`<p style="margin:0;font-weight:700">Delete this for everyone? This cannot be undone.</p><div style="display:flex;gap:8px"><button class="btn ghost" id="dn" style="margin:0;flex:1;color:#fff;border-color:rgba(255,255,255,.5)">Keep it</button><button class="btn red" id="dy" style="margin:0;flex:1">Yes, delete</button></div>`:`<button class="btn red" id="dl" style="margin:0">Delete</button>`):"";
 openFull(`<div style="position:relative;height:100%;background:#000;color:#fff">${c.src?`<video id="mpv" src="${esc(c.src)}" autoplay loop playsinline controls style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain"></video>`:`<div style="position:absolute;inset:0;display:grid;place-items:center;font-size:90px;background:linear-gradient(165deg,${c.g[0]},${c.g[1]})">${c.e}</div>`}<button id="mpx" aria-label="Close" style="position:absolute;top:12px;left:12px;width:42px;height:42px;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;font-size:20px">✕</button><div style="position:absolute;left:0;right:0;bottom:0;padding:44px 16px calc(16px + env(safe-area-inset-bottom));background:linear-gradient(transparent,rgba(0,0,0,.85));display:flex;flex-direction:column;gap:8px"><p style="margin:0">${esc(c.c||"")}</p>${bar}</div></div>`,true);
 const v=$("#mpv");if(v)v.play().catch(()=>{});
 $("#mpx").onclick=()=>profile(tabk);
 if($("#dl"))$("#dl").onclick=()=>myPost(i,tabk,true);
 if($("#dn"))$("#dn").onclick=()=>myPost(i,tabk,false);
 if($("#dy"))$("#dy").onclick=async()=>{
  $("#dy").disabled=true;$("#dy").textContent="Deleting…";
  try{const D=await claude.use("db");if(D&&c.id){const r=await D.collection("videos").doc(c.id).get();if(r.exists)await D.collection("videos").doc(c.id).set(Object.assign(r.data(),{del:true}))}}catch(e){}
  const k=CLIPS.indexOf(c);if(k>=0)CLIPS.splice(k,1);
  for(const m of [liked,saved]){const o={};Object.keys(m).forEach(q=>{q=+q;if(q<k)o[q]=m[q];else if(q>k)o[q-1]=m[q]});Object.keys(m).forEach(q=>delete m[q]);Object.assign(m,o)}
  profile(tabk);
 };
}
'''
rep('function authSheet(mode,how){',fn+'function authSheet(mode,how){')
open(sys.argv[2],'w',encoding='utf8').write(s)
