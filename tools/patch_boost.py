import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlBoost1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# boosted videos first
rep('.filter(i=>!blocked(CLIPS[i].uid,CLIPS[i].u));','.filter(i=>!blocked(CLIPS[i].uid,CLIPS[i].u)).sort((a,b)=>((CLIPS[b].bu>Date.now())-(CLIPS[a].bu>Date.now())));')
rep('uid:v.uid,id:v.id||"o"+v.ts,src:v.url}','uid:v.uid,bu:v.bu||0,id:v.id||"o"+v.ts,src:v.url}')
rep('style="cursor:pointer">@${esc(c.u)}</b><p id="cp${i}">','style="cursor:pointer">@${esc(c.u)}</b>${c.bu>Date.now()?\' <span style="font-size:11px;background:rgba(255,255,255,.22);padding:2px 8px;border-radius:99px;margin-left:6px">🚀 Boosted</span>\':""}<p id="cp${i}">')
rep('<button class="btn red" id="dl" style="margin:0">Delete</button>','<button class="btn" id="bst" style="margin:0 0 8px;background:linear-gradient(90deg,#f59e0b,#ef4444);color:#fff">🚀 Boost this video</button><button class="btn red" id="dl" style="margin:0">Delete</button>')
rep(' if($("#dl"))$("#dl").onclick=()=>myPost(i,tabk,true);',' /*wlBoost1*/if($("#bst"))$("#bst").onclick=()=>boostSheet(i,tabk);\n if($("#dl"))$("#dl").onclick=()=>myPost(i,tabk,true);')
rep('function myPost(i,tabk,ask){','''const BOOSTS=[[100,24,"24 hours"],[250,72,"3 days"],[500,168,"7 days"]];
async function boostSheet(i,tabk){
 const c=CLIPS[i];if(!c||!c.id)return;await loadWallet();
 open(`<h2 style="text-align:center">🚀 Boost this video</h2><p class="mute" style="text-align:center;margin:0 0 10px">Your video is shown first on Home for the time you choose. Your coins: <b id="bc">${me.wl.vc}</b></p>${BOOSTS.map((o,k)=>`<button class="btn" data-bo="${k}" style="display:flex;justify-content:space-between"><span>${o[2]}</span><span>${o[0]} coins</span></button>`).join("")}<button class="btn ghost" id="bbuy">Buy coins</button><p class="note" id="bnt" style="text-align:center"></p><button class="btn ghost" id="bx">Back</button>`);
 $("#bx").onclick=()=>{close();myPost(i,tabk)};
 $("#bbuy").onclick=()=>buyCoins(()=>boostSheet(i,tabk));
 $("#panel").querySelectorAll("[data-bo]").forEach(b=>b.onclick=async()=>{
  const o=BOOSTS[+b.dataset.bo],n=$("#bnt");
  if(me.wl.vc<o[0]){n.textContent="You need "+(o[0]-me.wl.vc)+" more coins. Tap Buy coins.";return}
  b.disabled=true;n.textContent="Boosting…";
  try{
   const D=await claude.use("db");const r=await D.collection("videos").doc(c.id).get();if(!r.exists)throw 0;
   const until=Math.max(Date.now(),r.data().bu||0)+o[1]*3600000;
   await D.collection("videos").doc(c.id).set(Object.assign(r.data(),{bu:until}));
   me.wl.vc-=o[0];(me.wl.spent=me.wl.spent||[]).push({k:"boost",id:c.id,coins:o[0],ts:Date.now()});await saveWallet();
   c.bu=until;$("#bc").textContent=me.wl.vc;
   n.textContent="✅ Boosted until "+new Date(until).toLocaleString([],{weekday:"short",hour:"2-digit",minute:"2-digit"})+". It shows first on Home.";
  }catch(e){n.textContent="Could not boost right now. No coins were taken. Try again."}
  b.disabled=false;
 });
}
function myPost(i,tabk,ask){''')
s=s.replace('2026.10.30-P','2026.10.30-Q')
open(P,"w",encoding="utf8").write(s);print("ok")
