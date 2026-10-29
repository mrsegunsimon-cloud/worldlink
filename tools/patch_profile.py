import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'id="pfgrid"' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70])
    s=s.replace(a,b)
# 1) sound: piano-like notes, no voice
i=s.find('function cChime(kind){');j=s.find('function cSpeak',i)
new_chime=r'''function cChime(kind){try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;CAU=CAU||new AC();if(CAU.state==="suspended")CAU.resume();
 const Q={news:[[392,0],[523,.16]],sports:[[523,0],[659,.12],[784,.24]],social:[[523,0],[659,.14],[784,.28]],market:[[784,0],[1047,.14]],events:[[523,0],[659,.12],[784,.24],[1047,.36]],music:[[440,0],[523,.14],[659,.28]],campus:[[392,0],[494,.14],[587,.28]],explore:[[587,0],[740,.14],[880,.28]],learn:[[523,0],[659,.16]],play:[[659,0],[784,.1],[988,.2]]}[kind]||[[523,0],[659,.14]];
 Q.forEach(([f,t])=>{const t0=CAU.currentTime+t;[[1,.22,"sine"],[2,.07,"sine"],[3,.025,"sine"]].forEach(([m,v,ty])=>{const o=CAU.createOscillator(),g=CAU.createGain();o.type=ty;o.frequency.value=f*m;g.gain.setValueAtTime(0,t0);g.gain.linearRampToValueAtTime(v,t0+.006);g.gain.exponentialRampToValueAtTime(.0008,t0+1.1);o.connect(g);g.connect(CAU.destination);o.start(t0);o.stop(t0+1.2)})})}catch(e){}}
'''
s=s[:i]+new_chime+s[j:]
rep('function cPlay(el){if(!CSND||!el)return;cChime(el.dataset.kind);cSpeak(el.dataset.say||"")}','function cPlay(el){if(!CSND||!el)return;cChime(el.dataset.kind)}')
# 2) profile screen
i=s.find('function personSheet(n,uid){');j=s.find('\nconst NEWS=[',i);assert 0<i<j
prof=r'''let FOLLOWS=null;
async function loadFollowsAll(){try{const D=await claude.use("db");if(!D)return;const q=await D.collection("follows").get();FOLLOWS=q.docs.map(d=>({uid:d.id,list:(d.data().list||[])}))}catch(e){}}
function personSheet(n,uid,back){
 back=back||close;
 if(n===me.name&&me.name!=="you"){secFull=true;return profile()}
 const pr=(typeof PROF!=="undefined"?PROF:[]).find(x=>x.name===n);if(!uid&&pr)uid=pr.uid;
 const person=PEOPLE.find(x=>x[0]===n),f=(me.f||[]).includes(n);
 const idx=CLIPS.map((c,i)=>i).filter(i=>CLIPS[i].u===n&&CLIPS[i].src&&!blocked(CLIPS[i].uid,CLIPS[i].u));
 const likes=idx.reduce((a,i)=>a+cnt(i),0),bio=(pr&&pr.bio)||(person?person[1]:"")||"New on WorldLink";
 const pic=pr&&pr.pic?`<img src="${esc(pr.pic)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:50%">`:esc(n[0].toUpperCase());
 const tile=i=>`<div data-pv="${i}" style="position:relative;cursor:pointer;aspect-ratio:3/4;background:#222;overflow:hidden"><video src="${esc(CLIPS[i].src)}" muted playsinline preload="metadata" style="width:100%;height:100%;object-fit:cover"></video><span style="position:absolute;left:6px;bottom:4px;color:#fff;font-weight:700;font-size:13px;text-shadow:0 1px 3px #000">▷ ${fmt(vcnt(i))}</span></div>`;
 secFull=true;FM=false;
 open(`<div style="padding:0 2px 24px"><div style="display:flex;align-items:center;justify-content:space-between"><button id="pbk" aria-label="Back" style="font-size:28px;padding:6px 10px;color:inherit">←</button></div><div style="display:flex;gap:12px;align-items:center;justify-content:space-between;margin:6px 6px 14px"><div style="min-width:0"><div style="font-size:30px;font-weight:900;line-height:1.1;overflow-wrap:anywhere">${esc(n)}</div><div class="mute" style="font-size:15px;margin-top:2px">@${esc(n)}</div></div><div class="av" style="width:92px;height:92px;font-size:38px;flex:none;overflow:hidden">${pic}</div></div><div style="display:flex;gap:26px;margin:0 6px 14px"><div><b id="pst1" style="font-size:20px">–</b><div class="mute" style="font-size:14px">Following</div></div><div><b id="pst2" style="font-size:20px">–</b><div class="mute" style="font-size:14px">Followers</div></div><div><b style="font-size:20px">${fmt(likes)}</b><div class="mute" style="font-size:14px">Likes</div></div></div><div style="display:flex;gap:8px;margin:0 6px 12px"><button id="pf" style="flex:2;padding:13px;border-radius:999px;font-weight:800;font-size:16px;background:${f?"var(--line,#eee)":"#FE2C55"};color:${f?"inherit":"#fff"}">${f?"Following":"Follow"}</button><button id="pm" style="flex:2;padding:13px;border-radius:999px;font-weight:800;font-size:16px;background:var(--line,#eee);color:inherit">Message</button></div><p style="margin:0 6px 14px;white-space:pre-wrap;overflow-wrap:anywhere">${esc(bio)}</p><div style="text-align:center;border-bottom:1px solid var(--line,#ddd);padding:6px 0;font-size:20px">▥</div><div id="pfgrid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:2px">${idx.length?idx.map(tile).join(""):'<p class="mute" style="grid-column:1/-1;text-align:center;padding:30px 0">No videos yet</p>'}</div></div>`);
 $("#pbk").onclick=back;
 $("#pm").onclick=()=>{if(uid)dmOpen(uid,n,"");else if(person)chat(n);else{const b=$("#pm");b.textContent="Messaging needs their account"}};
 $("#pf").onclick=async()=>{const was=(me.f||[]).includes(n);me.f=was?me.f.filter(x=>x!==n):(me.f||[]).concat(n);try{const D=await claude.use("db");if(D&&me.uid)await D.collection("follows").doc(me.uid).set({list:me.f})}catch(e){}if(!was&&uid)try{notify(uid,"started following you")}catch(e){}personSheet(n,uid,back)};
 $("#panel").querySelectorAll("[data-pv]").forEach(t=>t.onclick=()=>{const i=+t.dataset.pv;close();tab(1);setTimeout(()=>{const c=document.querySelector(`.clip[data-i="${i}"]`);if(c)c.scrollIntoView()},120)});
 (async()=>{if(!FOLLOWS)await loadFollowsAll();if(!FOLLOWS)return;const fr=FOLLOWS.filter(d=>d.list.includes(n)).length,mine=uid?FOLLOWS.find(d=>d.uid===uid):null;const a=$("#pst1"),b=$("#pst2");if(a)a.textContent=fmt(mine?mine.list.length:0);if(b)b.textContent=fmt(fr+(f&&me.uid&&!FOLLOWS.some(d=>d.uid===me.uid&&d.list.includes(n))?1:0))})();
 if(typeof loadProfs==="function"&&!(typeof PROF!=="undefined"&&PROF.length))loadProfs().then(()=>{const q=(PROF||[]).find(x=>x.name===n);if(q&&(q.pic||q.bio)&&$("#pfgrid"))personSheet(n,uid||q.uid,back)});
}
'''
s=s[:i]+prof+s[j:]
# 3) name taps
rep('<div class="av" style="width:38px;height:38px;flex:none">${esc((x.u||"?")[0].toUpperCase())}</div><div style="flex:1;min-width:0"><div><b>@${esc(x.u)}</b>','<div class="av" data-pn="${esc(x.u)}" data-pu="${esc(x.o||"")}" style="width:38px;height:38px;flex:none;cursor:pointer">${esc((x.u||"?")[0].toUpperCase())}</div><div style="flex:1;min-width:0"><div><b data-pn="${esc(x.u)}" data-pu="${esc(x.o||"")}" style="cursor:pointer">@${esc(x.u)}</b>')
rep('<b>@${esc(n.from)}</b>','<b data-pn="${esc(n.from)}" style="cursor:pointer;text-decoration:underline">@${esc(n.from)}</b>')
rep('<b>@${esc(c.u)}</b><p id="cp${i}">','<b data-pn="${esc(c.u)}" data-pu="${esc(c.uid||"")}" style="cursor:pointer">@${esc(c.u)}</b><p id="cp${i}">')
rep('<div class="av">${c.uid&&c.uid===me.uid&&me.pic?','<div class="av" data-pn="${esc(c.u)}" data-pu="${esc(c.uid||"")}" style="cursor:pointer">${c.uid&&c.uid===me.uid&&me.pic?')
rep('let HCGO={};','''let HCGO={};
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-pn]");if(!b)return;e.stopPropagation();e.preventDefault();
 const panel=document.getElementById("panel"),inPanel=panel&&panel.contains(b);let back=close;
 if(inPanel){if(panel.querySelector("#pt"))back=()=>{secFull=true;social()};else if(/Notifications/.test((panel.querySelector("h2")||{}).textContent||""))back=()=>{secFull=true;notifs()}}
 personSheet(b.dataset.pn,b.dataset.pu||"",back)},true);''')
rep('Version 2026.10.29-e','Version 2026.10.29-f')
a='if(d.p!==undefined)personSheet(d.p,d.u);'
if a in s: s=s.replace(a,'if(d.p!==undefined)personSheet(d.p,d.u,searchAll);')
open(p,'w',encoding='utf8').write(s);print('patched')
