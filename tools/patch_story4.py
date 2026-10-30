import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlStory4" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# ---------- status replies and emoji reactions ----------
HELP=r'''/* wlStory4: reply to a status or react with an emoji (goes to their messages) */
async function dmQuick(uid,name,text){
 if(!me.uid||!uid||uid===me.uid)return false;
 const id=[me.uid,uid].sort().join("_");let d=DMS.find(x=>x.id===id);
 if(!d){const ab=[me.uid,uid].sort(),a=ab[0],b=ab[1];d={id,a,b,na:a===me.uid?me.name:name,nb:b===me.uid?me.name:name,m:[]};DMS.unshift(d)}
 try{const D=await claude.use("db");if(!D)return false;
  try{const x=await D.collection("dms").doc(id).get();if(x.exists){const r=x.data();if(r.m&&r.m.length>d.m.length)d.m=r.m}}catch(e){}
  d.m.push({f:me.uid,n:me.name,ts:Date.now(),t:text});d.m=d.m.slice(-200);
  await D.collection("dms").doc(id).set(d);return true}catch(e){return false}
}
async function storySend(s,text,kind){
 const ok=await dmQuick(s.o,s.u,(kind==="emoji"?"Reacted "+text+" to your status":"↩️ Status reply: "+text));
 if(ok)notify(s.o,kind==="emoji"?"reacted "+text+" to your status":"replied to your status");
 return ok;
}
'''
rep('function showS(){\n',HELP+'function showS(){\n')
rep('const v=o.querySelector("video");\n if(v){v.muted=false',r''' if(!mine&&s.o&&me.uid){
  const bar=document.createElement("div");bar.id="stbar";bar.style.cssText="position:absolute;left:0;right:0;bottom:0;z-index:6;padding:8px 12px calc(12px + env(safe-area-inset-bottom));background:linear-gradient(transparent,rgba(0,0,0,.7))";
  bar.innerHTML='<div id="stem" style="display:flex;justify-content:space-around;margin-bottom:8px">'+["❤️","😂","😮","😢","🙏","👏","🔥"].map(e=>'<button data-em="'+e+'" style="font-size:28px;padding:4px 6px">'+e+'</button>').join("")+'</div><div style="display:flex;gap:8px"><input id="stin" maxlength="200" placeholder="Reply to @'+esc(s.u)+'…" aria-label="Reply to status" style="flex:1;min-width:0;border-radius:999px;border:1px solid rgba(255,255,255,.5);background:rgba(0,0,0,.45);color:#fff;padding:11px 16px;font-size:16px"><button id="stsd" style="background:#FE2C55;color:#fff;font-weight:800;border-radius:999px;padding:0 18px">Send</button></div><div id="stms" style="font-size:13px;text-align:center;min-height:16px;margin-top:6px"></div>';
  o.appendChild(bar);
  const cur=s,ms=bar.querySelector("#stms"),inp=bar.querySelector("#stin");
  const stop=()=>{clearTimeout(stT);const vv=o.querySelector("video");if(vv)vv.pause()},go=()=>{const vv=o.querySelector("video");if(vv)vv.play().catch(()=>{});else{clearTimeout(stT);stT=setTimeout(()=>{si++;showS()},5000)}};
  inp.onfocus=stop;inp.onblur=()=>{if(!inp.value)go()};
  ["click","touchstart"].forEach(ev=>bar.addEventListener(ev,e=>e.stopPropagation()));
  bar.querySelectorAll("[data-em]").forEach(b=>b.onclick=async e=>{e.stopPropagation();b.style.transform="scale(1.5)";setTimeout(()=>{b.style.transform=""},300);ms.textContent="Sending…";const ok=await storySend(cur,b.dataset.em,"emoji");ms.textContent=ok?"Sent "+b.dataset.em:"Could not send. Check your internet."});
  const sendTxt=async()=>{const t=inp.value.trim();if(!t)return;ms.textContent="Sending…";const ok=await storySend(cur,t,"text");if(ok){inp.value="";ms.textContent="Reply sent ✓";inp.blur()}else ms.textContent="Could not send. Check your internet."};
  bar.querySelector("#stsd").onclick=e=>{e.stopPropagation();sendTxt()};inp.onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();sendTxt()}};
 }
const v=o.querySelector("video");
 if(v){v.muted=false''')
# ---------- saved sounds ----------
SH=r'''/* wlSnd: save sounds from videos so anyone can use them in their own videos */
function sndKey(){return "wl_snd_"+(me.uid||"x")}
function sndMine(){try{return JSON.parse(localStorage.getItem(sndKey())||"[]")}catch(e){return[]}}
async function sndSave(x){const L=sndMine();if(!L.some(y=>y.url===x.url)){L.unshift({name:x.name,url:x.url});try{localStorage.setItem(sndKey(),JSON.stringify(L.slice(0,40)))}catch(e){}}return true}
function sndDel(url){const L=sndMine().filter(y=>y.url!==url);try{localStorage.setItem(sndKey(),JSON.stringify(L))}catch(e){}}
function sndFromVideos(){const seen={},out=[];for(let i=CLIPS.length-1;i>=0&&out.length<30;i--){const c=CLIPS[i];if(!c.src||!c.uid||seen[c.src])continue;seen[c.src]=1;const sd=clipSound(i);if(sd)out.push({name:sd.name+" · @"+c.u,url:sd.url})}return out}
'''
rep('function soundSheet(i){\n',SH+'function soundSheet(i){\n')
rep('<button class="btn" id="su">🎬 Use this sound</button>`','<button class="btn" id="su">🎬 Use this sound</button><button class="btn ghost" id="ss">💾 Save this sound</button>`')
rep(' const su=$("#su");if(su)su.onclick=()=>{sndPrev(null);SND=sd;',' const ss=$("#ss");if(ss)ss.onclick=async()=>{await sndSave(sd);ss.textContent="✓ Saved. Find it under Add music";ss.disabled=true};\n const su=$("#su");if(su)su.onclick=()=>{sndPrev(null);SND=sd;')
rep('<h3 style="margin:14px 0 4px;font-size:15px">WorldLink free library</h3>','${(()=>{const mine=sndMine(),vs=sndFromVideos();window.__sm=mine;window.__sv=vs;const row=(x,k,a)=>`<div class="cm" style="display:flex;align-items:center;gap:8px"><div style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"><b>${esc(x.name)}</b></div><button class="btn ghost" data-pp="${a}${k}" style="width:auto;margin:0;padding:8px 12px">▶</button><button class="btn" data-pu="${a}${k}" style="width:auto;margin:0;padding:8px 12px">Use</button>${a==="m"?`<button class="btn ghost" data-pd="${k}" style="width:auto;margin:0;padding:8px 10px" aria-label="Remove">🗑</button>`:`<button class="btn ghost" data-ps="${k}" style="width:auto;margin:0;padding:8px 10px" aria-label="Save">💾</button>`}</div>`;return (mine.length?`<h3 style="margin:14px 0 4px;font-size:15px">💾 My saved sounds</h3>`+mine.map((x,k)=>row(x,k,"m")).join(""):"")+(vs.length?`<h3 style="margin:14px 0 4px;font-size:15px">🎬 Sounds from videos</h3>`+vs.map((x,k)=>row(x,k,"v")).join(""):"")})()}<h3 style="margin:14px 0 4px;font-size:15px">WorldLink free library</h3>')
rep(' $("#panel").querySelectorAll("[data-gn]").forEach(b=>b.onclick=()=>{const g=GEN',r''' const arr=k=>(k[0]==="m"?window.__sm:window.__sv)[+k.slice(1)];
 $("#panel").querySelectorAll("[data-pp]").forEach(b=>b.onclick=()=>sndPrev(arr(b.dataset.pp).url));
 $("#panel").querySelectorAll("[data-pu]").forEach(b=>b.onclick=()=>{const x=arr(b.dataset.pu);SND={name:x.name,url:x.url};back()});
 $("#panel").querySelectorAll("[data-ps]").forEach(b=>b.onclick=async()=>{await sndSave(window.__sv[+b.dataset.ps]);b.textContent="✓";b.disabled=true});
 $("#panel").querySelectorAll("[data-pd]").forEach(b=>b.onclick=()=>{sndDel(window.__sm[+b.dataset.pd].url);soundPicker(cb)});
 $("#panel").querySelectorAll("[data-gn]").forEach(b=>b.onclick=()=>{const g=GEN''')
s=s.replace('2026.10.30-I','2026.10.30-J')
open(P,"w",encoding="utf8").write(s);print("ok")
