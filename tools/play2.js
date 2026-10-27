/* ===== Play zone: free-play lottery and casino-style games. Points only, no real money. ===== */
function pzGet(){try{const o=JSON.parse(localStorage.getItem("wl-pz")||"null");if(o&&typeof o.p==="number")return o}catch(e){}return{p:1000,day:"",hist:[]}}
function pzSave(o){try{localStorage.setItem("wl-pz",JSON.stringify(o))}catch(e){}}
function pzRnd(n){const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0]%n}
const pzToday=()=>new Date().toISOString().slice(0,10);
function pzHead(sub){const o=pzGet();return `<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">${sub?'<button id="pb" style="font-size:22px;padding:4px 10px">←</button>':""}<div style="flex:1"><b style="font-size:18px">🎰 Play zone</b><div class="mute" style="font-size:13px">Free play. Points have no cash value.</div></div><b style="font-size:16px">⭐ ${o.p}</b></div>`}
function playZone(g){
 const o=pzGet();
 if(!g){
  const canBonus=o.day!==pzToday();
  open(pzHead(false)+`<div class="cm" style="display:block"><b>Play money only</b><div class="mute" style="font-size:13px">These games use free points. You cannot win or lose real money here. 18+ only. Real-money betting needs a gambling licence and age checks, which WorldLink does not have yet.</div></div>${canBonus||o.p<50?'<button class="btn" id="pbn">🎁 Claim free daily '+(o.p<50?"refill":"500 points")+"</button>":""}<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px"><button data-pg="lotto" class="cm" style="display:block;text-align:center;color:inherit"><div style="font-size:30px">🎟️</div><b>Lucky draw</b><div class="mute" style="font-size:12px">Pick 5 numbers, 50 points</div></button><button data-pg="slots" class="cm" style="display:block;text-align:center;color:inherit"><div style="font-size:30px">🎰</div><b>Slots</b><div class="mute" style="font-size:12px">Spin for 20 points</div></button></div><button class="btn ghost" id="pbs" style="margin-top:8px">🏆 Betting sites in Nigeria, the UK and worldwide</button><p class="note">If gambling is hurting you or someone you know, please talk to someone you trust or a local support service.</p><button class="btn ghost" id="x">Close</button>`);
  const bn=$("#pbn");if(bn)bn.onclick=()=>{const q=pzGet();q.p+=500;q.day=pzToday();pzSave(q);playZone()};
  $("#panel").querySelectorAll("[data-pg]").forEach(b=>b.onclick=()=>playZone(b.dataset.pg));$("#pbs").onclick=()=>pzBets();return}
 if(g==="lotto"){pzLotto([]);return}
 if(g==="slots"){pzSlots(null);return}
}
function pzLotto(pick,res){
 const o=pzGet(),COST=50;
 open(pzHead(true)+`<h3 style="margin:8px 0 2px">🎟️ Lucky draw</h3><p class="note" style="margin:0 0 6px">Choose 5 numbers from 1 to 40. ${COST} points per ticket. Prizes: 2 matches 100, 3 matches 500, 4 matches 5,000, 5 matches 50,000 points.</p><div style="display:grid;grid-template-columns:repeat(8,1fr);gap:4px">${Array.from({length:40},(_,i)=>i+1).map(n=>`<button data-n="${n}" class="btn${pick.includes(n)?"":" ghost"}" style="margin:0;padding:8px 0;min-width:0">${n}</button>`).join("")}</div><div style="margin:8px 0">Your numbers: <b>${pick.slice().sort((a,b)=>a-b).join(", ")||"none yet"}</b></div>${res?`<div class="cm" style="display:block"><b>Draw: ${res.draw.join(", ")}</b><div>${res.m} match${res.m===1?"":"es"}${res.win?" — you win "+res.win+" points!":" — no prize this time."}</div></div>`:""}<button class="btn" id="pq">Quick pick</button><button class="btn" id="pd"${pick.length===5&&o.p>=COST?"":" disabled"}>Buy ticket and draw (${COST})</button><button class="btn ghost" id="x">Close</button>`);
 $("#pb").onclick=()=>playZone();
 $("#panel").querySelectorAll("[data-n]").forEach(b=>b.onclick=()=>{const n=+b.dataset.n;let p=pick.slice();if(p.includes(n))p=p.filter(x=>x!==n);else if(p.length<5)p.push(n);pzLotto(p)});
 $("#pq").onclick=()=>{const s=new Set();while(s.size<5)s.add(1+pzRnd(40));pzLotto([...s])};
 $("#pd").onclick=()=>{const q=pzGet();if(q.p<COST||pick.length!==5)return;q.p-=COST;const s=new Set();while(s.size<5)s.add(1+pzRnd(40));const draw=[...s].sort((a,b)=>a-b),m=pick.filter(n=>s.has(n)).length,win=[0,0,100,500,5000,50000][m];q.p+=win;pzSave(q);pzLotto(pick,{draw,m,win})};
}
const PZS=["🍒","🍋","🔔","⭐","7️⃣","🍉"];
function pzSlots(r){
 const o=pzGet(),COST=20;
 open(pzHead(true)+`<h3 style="margin:8px 0 2px">🎰 Slots</h3><p class="note" style="margin:0 0 6px">${COST} points per spin. Three of a kind pays 200 (7️⃣ pays 1,000). Two of a kind pays 40.</p><div style="display:flex;justify-content:center;gap:10px;font-size:48px;padding:14px 0">${(r?r.s:["❔","❔","❔"]).map(x=>`<span>${x}</span>`).join("")}</div>${r?`<div class="cm" style="display:block;text-align:center"><b>${r.win?"You win "+r.win+" points!":"No win this time."}</b></div>`:""}<button class="btn" id="ps"${o.p>=COST?"":" disabled"}>Spin (${COST})</button><button class="btn ghost" id="x">Close</button>`);
 $("#pb").onclick=()=>playZone();
 $("#ps").onclick=()=>{const q=pzGet();if(q.p<COST)return;q.p-=COST;const s=[0,0,0].map(()=>PZS[pzRnd(PZS.length)]);let win=0;if(s[0]===s[1]&&s[1]===s[2])win=s[0]==="7️⃣"?1000:200;else if(s[0]===s[1]||s[1]===s[2]||s[0]===s[2])win=40;q.p+=win;pzSave(q);pzSlots({s,win})};
}

const PZB=[["🇳🇬 Nigeria",[["SportyBet","https://www.sportybet.com"],["Bet9ja","https://www.bet9ja.com"],["BetKing","https://www.betking.com"],["NairaBet","https://www.nairabet.com"],["MSport","https://www.msport.com"],["Betway Nigeria","https://www.betway.com.ng"]]],["🇬🇧 United Kingdom",[["Bet365","https://www.bet365.com"],["William Hill","https://www.williamhill.com"],["Ladbrokes","https://www.ladbrokes.com"],["Paddy Power","https://www.paddypower.com"],["Betfred","https://www.betfred.com"],["Sky Bet","https://www.skybet.com"],["Coral","https://www.coral.co.uk"]]],["🌍 Worldwide",[["Betway","https://www.betway.com"],["Betfair","https://www.betfair.com"],["1xBet","https://1xbet.com"],["Betano","https://www.betano.com"],["DraftKings (USA)","https://www.draftkings.com"],["FanDuel (USA)","https://www.fanduel.com"]]]];
function pzBets(){
 open(pzHead(true)+`<h3 style="margin:8px 0 2px">🏆 Betting sites</h3><div class="cm" style="display:block"><b>Before you go</b><div class="mute" style="font-size:13px">These are separate companies. WorldLink is not connected to them and does not handle your money. You must be 18 or older. Betting is only legal with a licence, and the rules differ by country and state, so check that a site is licensed where you live. Never bet money you cannot afford to lose.</div></div>${PZB.map(g=>`<h3 style="margin:14px 0 4px">${g[0]}</h3>${g[1].map(s=>`<a class="cm" target="_blank" rel="noopener" href="${s[1]}" style="display:flex;align-items:center;gap:8px;color:inherit;text-decoration:none"><b style="flex:1">${s[0]}</b><span class="mute">Open ›</span></a>`).join("")}`).join("")}<p class="note">More sites can be added. Tell us the ones your community uses.</p><button class="btn ghost" id="x">Close</button>`);
 $("#pb").onclick=()=>playZone();
}
