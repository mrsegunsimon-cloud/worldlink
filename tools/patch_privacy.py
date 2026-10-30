import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlPrivacy1" in s: print("already");sys.exit(0)
def rep(a,b,cnt=1):
    global s
    assert s.count(a)>=1,a[:70]
    s=s.replace(a,b,1)
# load own settings
rep('if(d.pic)me.pic=d.pic}const fs=await D.collection("follows")','if(d.pic)me.pic=d.pic;me.priv=d.priv||null}const fs=await D.collection("follows")')
rep('doc(me.uid).set({name:me.name,bio:me.bio,pic:me.pic||""})','doc(me.uid).set({name:me.name,bio:me.bio,pic:me.pic||"",priv:me.priv||{m:"a",c:"a",p:0}})')
# menu row
rep('${row("bl","🚫","Blocked accounts ("+me.b.length+")")}','${row("pv","🔒","Privacy")}${row("bl","🚫","Blocked accounts ("+me.b.length+")")}')
rep('bl:blockedList,md:modScreen','pv:privacy,bl:blockedList,md:modScreen')
# helpers + settings screen
rep('function profMenu(){','''/*wlPrivacy1*/function wlNote(t){const o=document.getElementById("wlnote");if(o)o.remove();const e=document.createElement("div");e.id="wlnote";e.textContent=t;e.style.cssText="position:fixed;left:50%;bottom:90px;transform:translateX(-50%);max-width:86%;background:rgba(0,0,0,.85);color:#fff;padding:11px 16px;border-radius:14px;font:600 14px system-ui,sans-serif;z-index:99999;text-align:center";document.body.appendChild(e);setTimeout(()=>e.remove(),3500)}
function privOf(uid){const x=(typeof PROF!=="undefined"?PROF:[]).find(y=>y.uid===uid);return(x&&x.priv)||{}}
async function followsMe(uid){try{if(!FOLLOWS||Date.now()-(window.__flAt||0)>60000){await loadFollowsAll();window.__flAt=Date.now()}const e=(FOLLOWS||[]).find(d=>d.uid===uid);const mn=String(me.name||"").trim().toLowerCase();return !!(e&&(e.list||[]).some(x=>String(x||"").trim().toLowerCase()===mn))}catch(e){return true}}
async function wlMayMsg(uid){const p=privOf(uid);if(!uid||p.m!=="f")return true;return await followsMe(uid)}
async function wlMayCmt(uid){const p=privOf(uid);if(!uid||!p.c||p.c==="a")return true;if(p.c==="n")return false;return await followsMe(uid)}
function wlPrivHide(c){try{return !!(c&&c.uid&&c.uid!==me.uid&&privOf(c.uid).p&&!(me.f||[]).includes(c.u))}catch(e){return false}}
function privacy(){
 me.priv=Object.assign({m:"a",c:"a",p:0},me.priv||{});
 const seg=(k,opts)=>`<div style="display:flex;flex-direction:column;gap:6px;margin:8px 0 16px">${opts.map(o=>`<button class="btn${String(me.priv[k])===String(o[0])?"":" ghost"}" data-pk="${k}" data-pv="${o[0]}" style="margin:0;text-align:left">${String(me.priv[k])===String(o[0])?"✓ ":""}${o[1]}</button>`).join("")}</div>`;
 open(`<h2 style="text-align:center">🔒 Privacy</h2><b>Private account</b><p class="mute" style="margin:2px 0 0;font-size:14px">Only people you follow back and who follow you see your videos on Home and on your profile.</p>${seg("p",[[0,"Public. Everyone can see my videos"],[1,"Private. Only my followers"]])}<b>Who can message me</b>${seg("m",[["a","Everyone"],["f","Only people I follow"]])}<b>Who can comment on my videos</b>${seg("c",[["a","Everyone"],["f","Only people I follow"],["n","No one"]])}<p class="note" id="pvn" style="text-align:center"></p><button class="btn ghost" id="pvx">Close</button>`);
 $("#pvx").onclick=close;
 $("#panel").querySelectorAll("[data-pk]").forEach(b=>b.onclick=async()=>{
  const k=b.dataset.pk,v=b.dataset.pv;me.priv[k]=k==="p"?+v:v;
  try{const D=await claude.use("db");if(D&&me.uid){const r=await D.collection("profiles").doc(me.uid).get();await D.collection("profiles").doc(me.uid).set(Object.assign(r.exists?r.data():{name:me.name,bio:me.bio||""},{priv:me.priv}));try{const q=PROF.find(x=>x.uid===me.uid);if(q)q.priv=me.priv}catch(e){}}}catch(e){}
  privacy();const n=$("#pvn");if(n)n.textContent="Saved ✓";
 });
}
function profMenu(){''')
# enforce: messages
rep(''' const sendObj=async o=>{
  try{const D=await claude.use("db");if(D){const s=await D.collection("dms")''',''' const sendObj=async o=>{
  if(!(await wlMayMsg(dmOther(d).u))){wlNote("This person only accepts messages from people they follow.");return}
  try{const D=await claude.use("db");if(D){const s=await D.collection("dms")''')
# enforce: comments
rep('''  const v=$("#ci").value.trim();if(!v)return;
  (c.sc=c.sc||[]).push''','''  const v=$("#ci").value.trim();if(!v)return;
  if(c.uid&&c.uid!==me.uid&&!(await wlMayCmt(c.uid))){wlNote("Comments are limited on this video by its owner.");return}
  (c.sc=c.sc||[]).push''')
# enforce: private accounts in the feed and on their profile
rep('.filter(i=>!blocked(CLIPS[i].uid,CLIPS[i].u)).sort(','.filter(i=>!blocked(CLIPS[i].uid,CLIPS[i].u)&&!wlPrivHide(CLIPS[i])).sort(')
rep('try{await loadR(D)}catch(e){}order=mk(1);build()','try{await loadR(D)}catch(e){}try{if(!PROF.length)await loadProfs()}catch(e){}order=mk(1);build()')
rep('const idx=CLIPS.map((c,i)=>i).filter(i=>CLIPS[i].u===n&&CLIPS[i].src&&!blocked(CLIPS[i].uid,CLIPS[i].u));','const idx=CLIPS.map((c,i)=>i).filter(i=>CLIPS[i].u===n&&CLIPS[i].src&&!blocked(CLIPS[i].uid,CLIPS[i].u)&&!wlPrivHide(CLIPS[i]));')
s=s.replace('2026.10.30-R','2026.10.30-S')
open(P,"w",encoding="utf8").write(s);print("ok")
