import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlActivity" in s: print("already");sys.exit(0)
i=s.find("async function notifs(){");j=s.find('$("#bell").onclick=notifs;',i);assert i>0 and j>i
NEW=r'''/* wlActivity: TikTok-style Activity page (bell and Inbox > Activity open this) */
let ACT_TAB=0,ACT_ALL=false,ACT_HIDE=[];
async function notifs(tab){
 if(typeof tab==="number")ACT_TAB=tab;else ACT_TAB=0;ACT_ALL=false;
 await loadNF();try{if(typeof PROF!=="undefined"&&!PROF.length)await loadProfs()}catch(e){}
 const seen=me.ns||0;actDraw(seen);
 me.ns=Date.now();badge();
 try{const D=await claude.use("db");if(D&&me.uid)await D.collection("data/users/"+me.uid).doc("notifseen").set({ts:me.ns})}catch(e){}
}
function actDraw(seen){
 const COL="#1E6FFF,#FF7A1A,#7C5CFF,#0E9F6E".split(",");
 const prof=n=>(typeof PROF!=="undefined"?PROF:[]).find(x=>x.name===n);
 const av=n=>{const p=prof(n);return p&&p.pic?`<img src="${esc(p.pic)}" alt="" style="width:54px;height:54px;border-radius:50%;object-fit:cover;flex:none">`:`<div style="width:54px;height:54px;border-radius:50%;flex:none;display:grid;place-items:center;font-size:22px;font-weight:800;color:#fff;background:${COL[(n||"?").charCodeAt(0)%4]}">${esc((n||"?")[0].toUpperCase())}</div>`};
 const icon=t=>/like/.test(t)?"❤️":/comment/.test(t)?"💬":/follow/.test(t)?"👤":/message/.test(t)?"✉️":/going to/.test(t)?"📅":/gift/.test(t)?"🎁":"🔔";
 const all=NF.filter(n=>!blocked(null,n.from));
 const isFol=n=>/follow/.test((n.text||"").toLowerCase());
 const fol=all.filter(isFol);
 const following=n=>(me.f||[]).includes(n);
 const fbtn=(n,lab)=>following(n)?`<span class="mute" style="font-size:14px;flex:none">Following</span>`:`<button data-af="${esc(n)}" style="flex:none;background:#FE2C55;color:#fff;font-weight:800;border-radius:8px;padding:9px 16px;font-size:14px">${lab}</button>`;
 const row=(n,k)=>`<div data-nt="${k}" role="button" tabindex="0" style="display:flex;align-items:center;gap:12px;padding:10px 16px;cursor:pointer;${n.ts>seen?"background:rgba(37,199,240,.10)":""}"><span style="width:8px;flex:none">${n.ts>seen?'<i style="display:block;width:8px;height:8px;border-radius:50%;background:#25C7F0"></i>':""}</span><span data-pn="${esc(n.from)}">${av(n.from)}</span><div style="flex:1;min-width:0;font-size:16px;line-height:1.3"><b>${esc(n.from)}</b> ${esc(n.text)} <span class="mute" style="font-size:14px">${ago(n.ts)}</span></div>${isFol(n)?fbtn(n.from,"Follow back"):`<span style="font-size:24px;flex:none">${icon((n.text||"").toLowerCase())}</span>`}</div>`;
 const pri=all.filter(n=>n.ts>seen),oth=all.filter(n=>n.ts<=seen);
 const idx=n=>all.indexOf(n);
 let body="";
 if(ACT_TAB===1){body=fol.length?fol.map(n=>row(n,idx(n))).join(""):'<p class="mute" style="padding:30px 20px;text-align:center">No new followers yet.</p>'}
 else{
  if(!all.length)body='<p class="mute" style="padding:30px 20px;text-align:center">Nothing yet. When someone likes, comments, follows you or messages you, you will see it here.</p>';
  else{
   if(pri.length)body+=`<div class="mute" style="padding:14px 16px 6px;font-size:17px;font-weight:700">Priority</div>`+pri.map(n=>row(n,idx(n))).join("");
   if(oth.length){const shown=ACT_ALL?oth:oth.slice(0,5);body+=`<div class="mute" style="padding:14px 16px 6px;font-size:17px;font-weight:700">Earlier</div>`+shown.map(n=>row(n,idx(n))).join("");if(oth.length>5&&!ACT_ALL)body+=`<button id="actva" class="mute" style="display:block;width:100%;padding:14px;font-size:16px;font-weight:700">View all ⌄</button>`}
  }
  const sug=(typeof PROF!=="undefined"?PROF:[]).filter(p=>p.name&&p.uid!==me.uid&&p.name!==me.name&&!following(p.name)&&!ACT_HIDE.includes(p.name)).slice(0,6);
  if(sug.length)body+=`<div style="padding:18px 16px 6px;font-size:19px;font-weight:800">Suggested accounts</div>`+sug.map(p=>`<div style="display:flex;align-items:center;gap:12px;padding:10px 16px"><span data-pn="${esc(p.name)}" data-pu="${esc(p.uid)}">${av(p.name)}</span><div style="flex:1;min-width:0"><b style="font-size:17px">${esc(p.name)}</b><div class="mute" style="font-size:14px">WorldLink member</div></div>${fbtn(p.name,"Follow")}<button data-ax="${esc(p.name)}" aria-label="Dismiss" style="font-size:22px;padding:6px 8px;flex:none" class="mute">✕</button></div>`).join("");
 }
 const tb=(k,l,b)=>`<button data-at="${k}" style="flex:1;padding:14px 6px 12px;white-space:nowrap;font-size:17px;font-weight:${ACT_TAB===k?800:600};border-bottom:3px solid ${ACT_TAB===k?"currentColor":"transparent"};opacity:${ACT_TAB===k?1:.55}">${l}${b?` <span style="display:inline-block;min-width:22px;padding:1px 6px;border-radius:999px;background:#FE2C55;color:#fff;font-size:14px;font-weight:800">${b}</span>`:""}</button>`;
 const nnew=fol.filter(n=>n.ts>seen).length;
 openFull(`<div class="hd" style="gap:0"><button id="actb" aria-label="Back" style="font-size:28px;padding:0 14px">←</button><div style="flex:1;display:flex">${tb(0,"Activity",0)}${tb(1,"New followers",nnew)}</div></div><div class="pgx" style="padding:0 0 30px">${body}</div>`);
 const P=$("#panel");
 $("#actb").onclick=()=>{close()};
 P.querySelectorAll("[data-at]").forEach(b=>b.onclick=()=>{ACT_TAB=+b.dataset.at;actDraw(seen)});
 const va=$("#actva");if(va)va.onclick=()=>{ACT_ALL=true;actDraw(seen)};
 P.querySelectorAll("[data-ax]").forEach(b=>b.onclick=e=>{e.stopPropagation();ACT_HIDE.push(b.dataset.ax);actDraw(seen)});
 P.querySelectorAll("[data-af]").forEach(b=>b.onclick=async e=>{e.stopPropagation();const n=b.dataset.af;if(!(me.f||[]).includes(n))me.f=(me.f||[]).concat(n);
  try{const D=await claude.use("db");if(D&&me.uid)await D.collection("follows").doc(me.uid).set({list:me.f})}catch(er){}
  try{const pr=prof(n);if(pr)notify(pr.uid,"started following you")}catch(er){}
  actDraw(seen)});
 P.querySelectorAll("[data-pn]").forEach(el=>el.onclick=e=>{e.stopPropagation();personSheet(el.dataset.pn,el.dataset.pu||"",()=>{notifs(ACT_TAB)})});
 P.querySelectorAll("[data-nt]").forEach(el=>{const go=()=>{const n=all[+el.dataset.nt];if(!n)return;const t=(n.text||"").toLowerCase();
   if(/your video/.test(t)){close();tab(1)}
   else if(/follow/.test(t)){personSheet(n.from,"",()=>{notifs(ACT_TAB)})}
   else if(/message/.test(t)){secFull=true;inbox()}
   else if(/going to/.test(t)){explore("events")}
   else{secFull=true;social()}};
   el.onclick=go;el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();go()}}});
}
'''
s=s[:i]+NEW+s[j:]
s=s.replace('$("#bell").onclick=notifs;','$("#bell").onclick=()=>notifs();',1)
s=s.replace('$("#qa").onclick=()=>notifs();','$("#qa").onclick=()=>notifs();')
open(P,"w",encoding="utf8").write(s);print("ok")
