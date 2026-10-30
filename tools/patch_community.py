import sys,re
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlCommunity" in s: print("already");sys.exit(0)
a=s.index("function social(){");b=s.index("\n}\nasync function saveB",a)
NEW=r'''/* wlCommunity: photo-only Community feed (stories row, big photo posts) */
let CM_MORE={};
function social(){
 const P0=$("#panel"),sc=P0?P0.scrollTop:0;
 const COL=["#1E6FFF","#FF7A1A","#7C5CFF","#0E9F6E"];
 const prof=n=>(typeof PROF!=="undefined"?PROF:[]).find(x=>x.name===n);
 const av=(n,sz,ring)=>{const p=prof(n);const inner=p&&p.pic?`<img src="${esc(p.pic)}" alt="" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block">`:`<div style="width:100%;height:100%;border-radius:50%;display:grid;place-items:center;font-weight:800;color:#fff;background:${COL[(n||"?").charCodeAt(0)%4]};font-size:${Math.round(sz*.4)}px">${esc((n||"?")[0].toUpperCase())}</div>`;return `<div style="width:${sz}px;height:${sz}px;border-radius:50%;padding:${ring?3:0}px;flex:none;background:${ring?"linear-gradient(45deg,#7C5CFF,#FF2D55)":"transparent"}"><div style="width:100%;height:100%;border-radius:50%;overflow:hidden;border:${ring?2:0}px solid var(--card)">${inner}</div></div>`};
 const g={};activeS().forEach(x=>{const k=x.o||x.u;(g[k]=g[k]||[]).push(x)});window.__cg=g;
 const stRow=`<div style="display:flex;gap:12px;overflow-x:auto;padding:4px 2px 14px"><button id="cas" style="flex:none;width:68px;text-align:center;color:inherit"><div style="width:64px;height:64px;border-radius:50%;margin:0 auto;border:2px dashed var(--line);display:grid;place-items:center;font-size:28px;color:var(--acc)">+</div><span style="display:block;font-size:12px;margin-top:4px">Your story</span></button>${Object.keys(g).map(k=>{const L=g[k],z=L[L.length-1],nm=L[0].u||k;const th=z.kind==="video"?`<video src="${esc(z.url)}#t=0.3" muted playsinline preload="metadata" style="width:100%;height:100%;object-fit:cover;display:block;pointer-events:none"></video>`:`<img src="${esc(z.url)}" alt="" style="width:100%;height:100%;object-fit:cover;display:block;pointer-events:none">`;return `<button data-sk="${esc(k)}" style="flex:none;width:68px;text-align:center;color:inherit"><div style="width:64px;height:64px;border-radius:50%;padding:3px;margin:0 auto;background:linear-gradient(45deg,#7C5CFF,#FF2D55)"><div style="width:100%;height:100%;border-radius:50%;overflow:hidden;border:2px solid var(--card);background:#222">${th}</div></div><span style="display:block;font-size:12px;margin-top:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(nm)}</span></button>`}).join("")}</div>`;
 const nb=parseInt(($("#bd")||{}).textContent)||0;
 const head=`<div style="display:flex;align-items:center;gap:8px;padding:2px 0 12px"><h2 style="flex:1;margin:0;font-size:30px;letter-spacing:-.02em">Community</h2><button id="cfr" aria-label="Find friends" style="width:44px;height:44px;border-radius:50%;background:var(--bg);font-size:20px">👤</button><button id="cbl" aria-label="Notifications" style="position:relative;width:44px;height:44px;border-radius:50%;background:var(--bg);font-size:20px">🔔${nb?'<i style="position:absolute;top:8px;right:9px;width:10px;height:10px;border-radius:50%;background:#FE2C55"></i>':""}</button></div>`;
 const card=x=>{const l=x.l||[],liked=me.uid&&l.includes(me.uid),cm=x.cm||[],mine=x.o&&x.o===me.uid;
  return `<div style="margin:0 0 22px"><div style="display:flex;align-items:center;gap:10px;padding:0 2px 8px"><span data-pn="${esc(x.u)}" data-pu="${esc(x.o||"")}" style="cursor:pointer">${av(x.u,46,true)}</span><div style="flex:1;min-width:0"><b data-pn="${esc(x.u)}" data-pu="${esc(x.o||"")}" style="font-size:17px;cursor:pointer">${esc(x.u)}</b><div class="mute" style="font-size:13px">${ago(x.ts)==="now"?"now":ago(x.ts)+" ago"}</div></div><button data-mn="${esc(x.id)}" aria-label="More" style="font-size:24px;padding:4px 10px;color:var(--mute)">⋯</button></div>${CM_MORE[x.id]?`<div style="display:flex;gap:8px;flex-wrap:wrap;padding:0 2px 8px">${x.t?`<button class="btn ghost" style="width:auto;margin:0;padding:8px 14px" data-tr="${esc(x.id)}">${TRN[x.id]?"Original":"Translate"}</button>`:""}${mine?`<button class="btn ghost" style="width:auto;margin:0;padding:8px 14px" data-d="${esc(x.id)}">Delete</button>`:`<button class="btn ghost" style="width:auto;margin:0;padding:8px 14px" data-r="${esc(x.id)}">Report</button>`}</div>`:""}<img src="${esc(x.img)}" alt="Photo by ${esc(x.u)}" loading="lazy" style="width:100%;max-height:460px;object-fit:cover;border-radius:16px;display:block;background:#222">${x.t?`<div style="white-space:pre-wrap;overflow-wrap:anywhere;margin:10px 2px 4px;font-size:15px;line-height:1.35">${esc(TRN[x.id]||x.t)}</div>${TRN[x.id]?`<div class="mute" style="font-size:12px;margin:0 2px">Translated to ${esc(LANG)}</div>`:""}`:""}<div style="display:flex;gap:4px;margin:2px 0 0 -8px"><button style="padding:8px 12px;font-size:16px;${liked?"color:#FE2C55;font-weight:700":"color:var(--mute)"}" data-l="${esc(x.id)}">${liked?"♥":"♡"} ${l.length}</button><button style="padding:8px 12px;font-size:16px;color:var(--mute)" data-o="${esc(x.id)}">💬 ${cm.length}</button><button style="padding:8px 12px;font-size:16px;color:var(--mute)" data-sh="${esc(x.id)}" aria-label="Share">➤</button></div>${popen[x.id]?`<div style="border-top:1px solid var(--line);padding-top:6px">${cm.filter(c=>!blocked(null,c.n)).map(c=>`<div style="margin-bottom:4px"><b>@${esc(c.n)}</b> ${esc(c.t)}</div>`).join("")}<div style="display:flex;gap:6px"><input class="in" style="margin:4px 0 0" maxlength="140" placeholder="Write a comment" aria-label="Comment" data-ci="${esc(x.id)}"><button class="btn" style="width:auto;margin:4px 0 0;padding:8px 14px" data-cs="${esc(x.id)}">Send</button></div></div>`:""}</div>`};
 const list=PS.filter(x=>x.img&&!blocked(x.o,x.u));
 open(head+stRow+(list.length?list.map(card).join(""):'<p class="mute" style="text-align:center;padding:30px 10px">No photos yet. Tap + to share the first one.</p>')+`<button id="cnp" aria-label="New photo post" style="position:sticky;bottom:16px;margin-left:auto;display:grid;place-items:center;width:58px;height:58px;border-radius:50%;background:#FE2C55;color:#fff;font-size:32px;box-shadow:0 4px 16px rgba(0,0,0,.4)">+</button>`);
 $("#panel").scrollTop=sc;
 const P=$("#panel"),find=id=>PS.find(y=>y.id===id);
 $("#cfr").onclick=()=>friends();$("#cbl").onclick=()=>notifs();$("#cnp").onclick=newPhotoPost;$("#cas").onclick=addStory;
 P.querySelectorAll("[data-sk]").forEach(b=>b.onclick=()=>{const q=(window.__cg||{})[b.dataset.sk];if(q){SQ=q;si=0;close();showS()}});
 P.querySelectorAll("[data-pn]").forEach(el=>el.onclick=e=>{e.stopPropagation();personSheet(el.dataset.pn,el.dataset.pu||"",()=>{secFull=true;social()})});
 P.querySelectorAll("[data-mn]").forEach(b=>b.onclick=()=>{CM_MORE[b.dataset.mn]=!CM_MORE[b.dataset.mn];social()});
 P.querySelectorAll("[data-l]").forEach(b=>b.onclick=async()=>{const x=find(b.dataset.l);if(!x||!me.uid)return;const was=(x.l||[]).includes(me.uid);x.l=was?x.l.filter(u=>u!==me.uid):(x.l||[]).concat(me.uid);await saveP(x);if(!was)notify(x.o,"liked your post");social()});
 P.querySelectorAll("[data-o]").forEach(b=>b.onclick=()=>{popen[b.dataset.o]=!popen[b.dataset.o];social()});
 P.querySelectorAll("[data-sh]").forEach(b=>b.onclick=async()=>{const x=find(b.dataset.sh);if(!x)return;const u="https://worldlink.app/";try{if(navigator.share)await navigator.share({title:"WorldLink",text:(x.t||"A photo by @"+x.u)+" on WorldLink",url:u});else{await navigator.clipboard.writeText(u);b.textContent="✓"}}catch(e){}});
 P.querySelectorAll("[data-r]").forEach(b=>b.onclick=()=>{const x=find(b.dataset.r);if(x)reportFlow("post",x.id,x.o,x.u,()=>{secFull=true;social()})});
 P.querySelectorAll("[data-tr]").forEach(b=>b.onclick=async()=>{const x=find(b.dataset.tr);if(!x||!x.t)return;if(TRN[x.id]){delete TRN[x.id];social();return}b.textContent="Translating…";try{TRN[x.id]=await tr(x.t)}catch(e){b.textContent="Not available";return}social()});
 P.querySelectorAll("[data-d]").forEach(b=>b.onclick=async()=>{const x=find(b.dataset.d);if(!x)return;x.del=true;await saveP(x);PS=PS.filter(y=>y!==x);social()});
 P.querySelectorAll("[data-cs]").forEach(b=>b.onclick=async()=>{const x=find(b.dataset.cs),i=P.querySelector(`[data-ci="${b.dataset.cs}"]`),v=i?i.value.trim():"";if(!x||!v)return;(x.cm=x.cm||[]).push({n:me.name,t:v});await saveP(x);notify(x.o,"commented on your post: "+v.slice(0,40));social()});
}
function newPhotoPost(){
 open(`<h2>New photo post</h2><p class="mute">Community is for photos only. Videos go on Home.</p><input class="in" id="pf" type="file" accept="image/*" aria-label="Choose a photo"><img id="pv" alt="" style="display:none;width:100%;max-height:260px;object-fit:cover;border-radius:14px;margin-bottom:8px"><input class="in" id="pt" maxlength="280" placeholder="Write a caption (optional)" aria-label="Caption"><p class="note" id="st"></p><button class="btn" id="pp">Post photo</button><button class="btn ghost" id="pb">Cancel</button>`);
 $("#pb").onclick=()=>{secFull=true;social()};
 $("#pf").onchange=()=>{const f=$("#pf").files[0];if(f&&f.type.startsWith("image/")){$("#pv").src=URL.createObjectURL(f);$("#pv").style.display="block"}};
 $("#pp").onclick=async()=>{
  const t=$("#pt").value.trim(),f=$("#pf").files[0],st=$("#st");
  if(!f){st.textContent="Choose a photo first.";return}
  if(!f.type.startsWith("image/")){st.textContent="Only photos can be posted here. Post videos from the + button on Home.";return}
  if(f.size>5*1048576){st.textContent="That photo is over 5 MB. Choose a smaller one.";return}
  $("#pp").disabled=true;st.textContent="Posting…";
  const it={id:"p"+Date.now(),t,u:me.name,o:me.uid,ts:Date.now(),l:[],cm:[],img:URL.createObjectURL(f)};
  try{const D=await claude.use("db");const A=await claude.use("assets");const r=await A.upload(f);it.img=r.url;if(D&&me.uid)await D.collection("posts").doc(it.id).set(it)}catch(e){}
  PS.unshift(it);notify("*","shared a photo in Community"+(t?": "+t.slice(0,40):""));secFull=true;social();
 };
}'''
s=s[:a]+NEW+s[b+2:]
s=s.replace('if(document.querySelector("#pt")&&!$("#pt").value)social()','if(document.querySelector("#cnp"))social()')
s=s.replace('if(panel.querySelector("#pt"))back=','if(panel.querySelector("#pt")||panel.querySelector("#cnp"))back=')
s=s.replace('2026.10.30-K','2026.10.30-L')
open(P,"w",encoding="utf8").write(s);print("ok")
