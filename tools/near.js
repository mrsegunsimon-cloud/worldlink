/* ===== Places near you (app only): real places from OpenStreetMap around the phone's location ===== */
const NP={
 restaurant:["Restaurants","🍽️",'["amenity"~"^(restaurant|fast_food)$"]',4000],
 park:["Parks","🌳",'["leisure"~"^(park|garden|nature_reserve)$"]',6000],
 attraction:["Attractions","🎡",'["tourism"~"^(attraction|museum|zoo|theme_park|gallery|viewpoint)$"]',20000],
 hotel:["Hotels","🏨",'["tourism"~"^(hotel|guest_house|hostel|motel)$"]',6000],
 airport:["Airports","✈️",'["aeroway"="aerodrome"]',100000],
 train:["Train stations","🚆",'["railway"="station"]',40000],
 bus:["Bus terminals","🚌",'["amenity"="bus_station"]',25000],
 atm:["ATMs","🏧",'["amenity"="atm"]',3000],
 beach:["Beaches","🏖️",'["natural"="beach"]',40000]};
const NPH={beach:"greatbarrier"};
const NPS=[["restaurant","Restaurants","Where to eat near you"],["park","Parks","Green spaces to relax in"],["attraction","Attractions","Things to see and do"],["hotel","Hotels","Places to stay"],["airport","Airports","Flights and transfers"],["train","Train stations","Rail travel"],["bus","Bus terminals","Buses and coaches"],["atm","ATMs","Cash machines nearby"],["beach","Beaches","Sand, sea and sunsets"]];
function nearGrid(){
 return `<p class="note" style="margin:10px 0 0">Tap a place type to list places near you. Tap one to open it in Maps.</p><div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:10px">${NPS.map(it=>{const g=GRAD[hsh(it[1])%GRAD.length];const pk=PH[it[0]]?it[0]:NPH[it[0]];return `<a href="#" data-np="${it[0]}" style="display:block;color:inherit;text-decoration:none${NPS.length%2&&it===NPS[NPS.length-1]?";grid-column:span 2":""}">${PH[pk]?`<img src="${PH[pk]}" alt="${esc(it[1])}" loading="lazy" style="display:block;width:100%;height:104px;object-fit:cover;border-radius:14px">`:`<div style="height:104px;border-radius:14px;background:linear-gradient(160deg,${g[0]},${g[1]});display:grid;place-items:center;font-size:48px">${NP[it[0]][1]}</div>`}<div style="font-weight:700;margin-top:6px">${esc(it[1])}</div><div class="mute" style="font-size:13px;line-height:1.3">${esc(it[2])}</div></a>`}).join("")}</div>`;
}
async function netGet(url,sec){
 sec=sec||25;
 const job=window.WLAuth?WLN("get",{url:url,timeout:sec}).then(r=>{if(r.error)throw new Error(r.error);return r.body}):fetch(url).then(r=>{if(!r.ok)throw new Error("HTTP "+r.status);return r.text()});
 return Promise.race([job,new Promise((_,no)=>setTimeout(()=>no(new Error("The places service is slow right now.")),(sec+3)*1000))])}
const NQ={restaurant:"restaurant",park:"park",attraction:"tourist attraction",hotel:"hotel",airport:"airport",train:"train station",bus:"bus station",atm:"atm",beach:"beach"};
async function overpassRows(key,C,loc,rad){
 const q=`[out:json][timeout:15];nwr${C[2]}(around:${rad},${loc.lat},${loc.lng});out center 60;`;
 const hosts=["https://overpass-api.de/api/interpreter","https://overpass.kumi.systems/api/interpreter","https://overpass.private.coffee/api/interpreter"];
 const txt=await Promise.any(hosts.map(h=>netGet(h+"?data="+encodeURIComponent(q),15)));
 return(JSON.parse(txt).elements||[]).map(e=>({la:e.lat??(e.center&&e.center.lat),lo:e.lon??(e.center&&e.center.lon),t:e.tags||{}}))}
async function nominatimRows(key,loc,rad){
 const d=rad/111000,vb=[loc.lng-d,loc.lat+d,loc.lng+d,loc.lat-d].join(",");
 const j=JSON.parse(await netGet("https://nominatim.openstreetmap.org/search?format=jsonv2&limit=40&bounded=1&viewbox="+vb+"&q="+encodeURIComponent(NQ[key]),15));
 return j.map(r=>{const p=(r.display_name||"").split(",").map(x=>x.trim());return{la:+r.lat,lo:+r.lon,t:{name:r.name||p[0],"addr:full":p.slice(1,3).join(", ")}}})}
async function getLoc(){
 if(window.WLAuth){const r=await WLN("location");if(r.error)throw new Error(r.error);return{lat:r.lat,lng:r.lng,label:"your location"}}
 return new Promise((ok,no)=>{if(!navigator.geolocation)return no(new Error("Location is not available here."));navigator.geolocation.getCurrentPosition(p=>ok({lat:p.coords.latitude,lng:p.coords.longitude,label:"your location"}),()=>no(new Error("Location was not allowed.")),{timeout:15000})})}
function openUrl(u){if(window.WLAuth&&!window.__wlWeb)WLN("open",{url:u});else if(typeof openExt==="function")openExt(u);else window.open(u,"_blank","noopener")}
const npDist=(a,b,c,d)=>{const R=6371,t=x=>x*Math.PI/180,dl=t(c-a),dg=t(d-b),h=Math.sin(dl/2)**2+Math.cos(t(a))*Math.cos(t(c))*Math.sin(dg/2)**2;return 2*R*Math.asin(Math.sqrt(h))};
const npFmt=k=>k<1?Math.round(k*100)*10+" m":(k<10?k.toFixed(1):Math.round(k))+" km";
async function nearList(key,loc){
 const C=NP[key];if(!C)return;
 const head=(sub)=>`<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><button id="npb" style="font-size:22px;padding:4px 10px">←</button><div><b style="font-size:18px">${C[1]} ${C[0]} near you</b><div class="mute" style="font-size:13px">${sub}</div></div></div>`;
 const back=()=>explore("places");
 open(head("Finding your location…")+'<p class="mute" style="padding:20px 0">Please wait…</p><button class="btn ghost" id="x">Close</button>');$("#npb").onclick=back;
 try{
  loc=loc||window.__loc||await getLoc();window.__loc=loc;
  open(head("Searching around "+esc(loc.label)+"…")+'<p class="mute" style="padding:20px 0">Looking for places…</p><button class="btn ghost" id="x">Close</button>');$("#npb").onclick=back;
  let rad=C[3],els=[];
  for(let tries=0;tries<3;tries++){
   let got=null,fb=false;
   try{got=await overpassRows(key,C,loc,rad)}catch(e){fb=true;try{got=await nominatimRows(key,loc,rad*2)}catch(e2){got=null}}
   if(got===null)throw new Error("The places service is busy. Check your internet and try again in a minute.");
   const named=got.filter(e=>e.t&&(e.t.name||(key==="atm"&&(e.t.operator||e.t.brand))));
   if(named.length>=6||tries===2||fb){els=named;if(fb)rad*=2;break}
   rad*=3}
  const seen={},rows=[];
  els.forEach(e=>{const la=e.la,lo=e.lo;if(la==null||lo==null||isNaN(la))return;const t=e.t,name=t.name||t.operator||t.brand||C[0].replace(/s$/,"");const k=name+"|"+la.toFixed(3)+"|"+lo.toFixed(3);if(seen[k])return;seen[k]=1;
   const adr=t["addr:full"]||[t["addr:housenumber"],t["addr:street"],t["addr:suburb"]||t["addr:city"]].filter(Boolean).join(" ");
   rows.push({name,la,lo,d:npDist(loc.lat,loc.lng,la,lo),adr,ph:t.phone||t["contact:phone"]||"",oh:t.opening_hours||""})});
  rows.sort((a,b)=>a.d-b.d);const top=rows.slice(0,40);
  const li=top.map((r,i)=>`<div style="display:flex;gap:10px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)"><button data-nr="${i}" style="flex:1;min-width:0;text-align:left;color:inherit;padding:0"><b>${C[1]} ${esc(r.name)}</b><div class="mute" style="font-size:13px">${npFmt(r.d)} away${r.adr?" · "+esc(r.adr):""}</div>${r.oh?`<div class="mute" style="font-size:12px">Hours: ${esc(r.oh.slice(0,60))}</div>`:""}</button><button class="btn ghost" data-nd="${i}" style="width:auto;margin:0;padding:8px 12px">Directions</button></div>`).join("");
  open(head(top.length+" found, up to "+npFmt(top.length?Math.max(...top.map(r=>r.d)):0)+" from "+esc(loc.label))+(top.length?li:'<p class="mute" style="padding:20px 0">Nothing found nearby. Try another city.</p>')+`<button class="btn ghost" id="npc">Search another city</button><p class="note">Places come from OpenStreetMap contributors. Tap a place to open it in Maps.</p><button class="btn ghost" id="x">Close</button>`);
  $("#npb").onclick=back;
  $("#panel").querySelectorAll("[data-nr]").forEach(b=>b.onclick=()=>{const r=top[+b.dataset.nr];openUrl("https://www.google.com/maps/search/?api=1&query="+r.la+","+r.lo)});
  $("#panel").querySelectorAll("[data-nd]").forEach(b=>b.onclick=()=>{const r=top[+b.dataset.nd];openUrl("https://www.google.com/maps/dir/?api=1&destination="+r.la+","+r.lo)});
  $("#npc").onclick=()=>{
   open(`<h2>Search another city</h2><input class="in" id="npq" placeholder="City or town, e.g. Abuja" aria-label="City"><p class="note" id="st"></p><button class="btn" id="npg">Search</button><button class="btn ghost" id="npb2">Back</button>`);
   $("#npb2").onclick=()=>nearList(key,loc);
   $("#npg").onclick=async()=>{const q=$("#npq").value.trim();if(q.length<2){$("#st").textContent="Type a city name.";return}$("#st").textContent="Searching…";
    try{const j=JSON.parse(await netGet("https://nominatim.openstreetmap.org/search?format=json&limit=1&q="+encodeURIComponent(q)));if(!j.length){$("#st").textContent="City not found.";return}window.__loc={lat:+j[0].lat,lng:+j[0].lon,label:j[0].display_name.split(",")[0]};nearList(key,window.__loc)}catch(e){$("#st").textContent="Could not search right now."}}}
 }catch(e){
  open(head("")+`<p style="padding:14px 0">${esc(e.message||"Something went wrong.")}</p><button class="btn" id="npr">Try again</button><button class="btn ghost" id="npc2">Search a city instead</button><button class="btn ghost" id="x">Close</button>`);
  $("#npb").onclick=back;$("#npr").onclick=()=>{window.__loc=null;nearList(key)};
  $("#npc2").onclick=()=>{open(`<h2>Search a city</h2><input class="in" id="npq" placeholder="City or town, e.g. Lagos" aria-label="City"><p class="note" id="st"></p><button class="btn" id="npg">Search</button><button class="btn ghost" id="x">Close</button>`);
   $("#npg").onclick=async()=>{const q=$("#npq").value.trim();if(q.length<2){$("#st").textContent="Type a city name.";return}$("#st").textContent="Searching…";
    try{const j=JSON.parse(await netGet("https://nominatim.openstreetmap.org/search?format=json&limit=1&q="+encodeURIComponent(q)));if(!j.length){$("#st").textContent="City not found.";return}window.__loc={lat:+j[0].lat,lng:+j[0].lon,label:j[0].display_name.split(",")[0]};nearList(key,window.__loc)}catch(e){$("#st").textContent="Could not search right now."}}}}
}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-np]");if(b){e.preventDefault();e.stopPropagation();if(b.dataset.np==="beach")beachHome();else nearList(b.dataset.np)}},true);

/* ===== Beaches by country: pick a country, see its beaches with stars, open one for details and directions ===== */
const BCO=[["NG","Nigeria"],["GH","Ghana"],["ZA","South Africa"],["KE","Kenya"],["TZ","Tanzania"],["EG","Egypt"],["MA","Morocco"],["SN","Senegal"],["CV","Cape Verde"],["MU","Mauritius"],["SC","Seychelles"],["MZ","Mozambique"],["MG","Madagascar"],["NA","Namibia"],["AO","Angola"],["CM","Cameroon"],["GA","Gabon"],["CI","Ivory Coast"],["BJ","Benin"],["TG","Togo"],["SL","Sierra Leone"],["LR","Liberia"],["GM","Gambia"],["ES","Spain"],["PT","Portugal"],["FR","France"],["IT","Italy"],["GR","Greece"],["HR","Croatia"],["TR","Turkey"],["GB","United Kingdom"],["IE","Ireland"],["US","United States"],["CA","Canada"],["MX","Mexico"],["BR","Brazil"],["CO","Colombia"],["AR","Argentina"],["PE","Peru"],["CL","Chile"],["JM","Jamaica"],["BS","Bahamas"],["CU","Cuba"],["DO","Dominican Republic"],["BB","Barbados"],["TT","Trinidad and Tobago"],["AU","Australia"],["NZ","New Zealand"],["ID","Indonesia"],["TH","Thailand"],["PH","Philippines"],["MY","Malaysia"],["VN","Vietnam"],["IN","India"],["LK","Sri Lanka"],["MV","Maldives"],["JP","Japan"],["KR","South Korea"],["CN","China"],["AE","United Arab Emirates"],["OM","Oman"],["SA","Saudi Arabia"],["IL","Israel"],["CY","Cyprus"],["MT","Malta"]];
const bFlag=c=>String.fromCodePoint(...[...c].map(x=>127397+x.charCodeAt(0)));
const BINFO={
 "Elegushi Beach":"A lively Lekki beach known for music, parties and events, busiest on weekends and holidays. Expect an entry fee and food and drink stalls.",
 "Tarkwa Bay":"A sheltered bay near Lagos harbour that you reach by a short boat ride. Calm water makes it popular for swimming and beginner surfing.",
 "Landmark Beach":"A resort-style beach at Oniru, Victoria Island, with restaurants, events and a paid entry. Good for an organised day out.",
 "Alpha Beach":"A quieter Lekki beach, usually less crowded than the big party beaches. Ask locals about sea conditions before swimming.",
 "Badagry Beach":"A long, open Atlantic beach near the historic town of Badagry, close to the Benin border. Strong waves, so swim with care.",
 "Eleko Beach":"A wide, open beach in Ibeju-Lekki, popular with day visitors and events. The sea can be rough.",
 "Ibeno Beach":"A very long sandy beach in Akwa Ibom State, often described as one of the longest in West Africa.",
 "La Campagne Tropicana":"A beach resort in Ibeju-Lekki with lodging and activities. Check current opening and prices before you go."};
function bRate(){try{return JSON.parse(localStorage.getItem("wl-brate")||"{}")}catch(e){return{}}}
function bSave(o){try{localStorage.setItem("wl-brate",JSON.stringify(o))}catch(e){}}
const bKey=(cc,n)=>cc+"|"+n;
function bAvg(k){const r=bRate()[k];return r&&r.n?{avg:r.s/r.n,n:r.n,me:r.me||0}:{avg:0,n:0,me:0}}
const bStarTxt=(a,n)=>n?`<span style="color:#F5B301">${"★".repeat(Math.round(a))}${"☆".repeat(5-Math.round(a))}</span> ${a.toFixed(1)} (${n})`:`<span class="mute">☆☆☆☆☆ No ratings yet</span>`;
function beachHome(pin){
 const list=BCO.slice().sort((a,b)=>a[1]<b[1]?-1:1);
 if(pin){const i=list.findIndex(x=>x[0]===pin);if(i>0)list.unshift(list.splice(i,1)[0])}
 open(`<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><button id="npb" style="font-size:22px;padding:4px 10px">←</button><div><b style="font-size:18px">🏖️ Beaches</b><div class="mute" style="font-size:13px">Choose a country</div></div></div><input class="in" id="bcq" placeholder="Search a country" aria-label="Search a country" style="margin-top:0"><div id="bcl">${list.map((c,i)=>`<button data-bc="${c[0]}" data-bn="${esc(c[1])}" style="display:flex;width:100%;align-items:center;gap:12px;text-align:left;color:inherit;padding:12px 0;border-bottom:1px solid var(--line)"><span style="font-size:28px">${bFlag(c[0])}</span><b style="flex:1">${esc(c[1])}${pin&&i===0?' <span class="mute" style="font-weight:400;font-size:12px">· your country</span>':""}</b><span class="mute">›</span></button>`).join("")}</div><button class="btn ghost" id="x">Close</button>`);
 $("#npb").onclick=()=>explore("places");
 const wire=()=>$("#panel").querySelectorAll("[data-bc]").forEach(b=>b.onclick=()=>beachCountry(b.dataset.bc,b.dataset.bn));wire();
 $("#bcq").oninput=e=>{const q=e.target.value.trim().toLowerCase();$("#panel").querySelectorAll("[data-bc]").forEach(b=>b.style.display=!q||b.dataset.bn.toLowerCase().includes(q)?"flex":"none")};
 if(!pin&&!window.__cc){window.__cc="?";(async()=>{try{const l=window.__loc||await getLoc();window.__loc=l;const j=JSON.parse(await netGet("https://nominatim.openstreetmap.org/reverse?format=json&zoom=3&lat="+l.lat+"&lon="+l.lng,10));window.__cc=(j.address&&j.address.country_code||"").toUpperCase();if($("#bcl")&&window.__cc.length===2)beachHome(window.__cc)}catch(e){window.__cc=""}})()}
 else if(!pin&&window.__cc&&window.__cc.length===2){beachHome(window.__cc)}
}

async function beachData(){
 if(window.__bd!==undefined)return window.__bd;
 window.__bd=null;
 try{window.__bd=JSON.parse(await netGet("https://mrsegunsimon-cloud.github.io/worldlink/beaches.json?t="+Date.now(),25))}catch(e){window.__bd=null}
 return window.__bd}

const BDO=[[/swim/i,"Swimming"],[/surf/i,"Surfing"],[/snorkel|div(e|ing)\b/i,"Snorkelling and diving"],[/event|party|parties|music|\bdj\b|concert|festival/i,"Parties and events"],[/restaurant|\bbar\b|food|drink|cafe|café/i,"Food and drinks"],[/horse/i,"Horse riding"],[/jet ?ski|boat|kayak|paddle|water ?sport|sail/i,"Water sports and boat rides"],[/sunset|sunrise/i,"Watching the sunset"],[/fishing/i,"Fishing"],[/camp/i,"Camping"],[/walk|hike|trail/i,"Walking"],[/volleyball|football|games?\b/i,"Beach games"],[/picnic|relax|sunbath/i,"Picnics and relaxing"],[/resort|hotel|lodg/i,"Stay nearby"]];
async function beachPhotos(r){
 const u="https://commons.wikimedia.org/w/api.php?action=query&generator=geosearch&ggscoord="+r.la+"%7C"+r.lo+"&ggsradius=3000&ggsnamespace=6&ggslimit=40&prop=imageinfo&iiprop=url%7Cmime&iiurlwidth=500&format=json&origin=*";
 const j=JSON.parse(await netGet(u,15));
 const P=Object.values((j.query&&j.query.pages)||{}).filter(p=>p.imageinfo&&p.imageinfo[0]&&/^image\/(jpeg|png)$/.test(p.imageinfo[0].mime)&&/^https:\/\//.test(p.imageinfo[0].thumburl||""));
 const tk=r.n.toLowerCase().replace(/beach|resort|bay/g,"").split(/\W+/).filter(x=>x.length>3);
 P.forEach(p=>{const ti=p.title.toLowerCase();p.sc=tk.reduce((n,x)=>n+(ti.includes(x)?1:0),0)});
 P.sort((a,b)=>b.sc-a.sc);
 return {imgs:P.slice(0,6).map(p=>({u:p.imageinfo[0].thumburl,full:p.imageinfo[0].url,t:p.title.replace(/^File:/,"")})),named:P.some(p=>p.sc>0)}}
function beachLight(u,t){
 const o=document.createElement("div");o.style.cssText="position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,.92);display:grid;place-items:center;padding:12px";
 o.innerHTML=`<img src="${esc(u)}" alt="" referrerpolicy="no-referrer" style="max-width:100%;max-height:82vh;border-radius:10px"><div style="color:#fff;font-size:12px;margin-top:8px;text-align:center">${esc(t)}</div><button style="position:absolute;top:14px;right:14px;width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,.2);color:#fff;font-size:20px">✕</button>`;
 o.onclick=()=>o.remove();document.body.appendChild(o)}
async function beachExtra(r,cname,about){
 try{
  const ph=await beachPhotos(r);const b=$("#bph");if(!b)return;
  b.innerHTML=ph.imgs.length?`<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4px">${ph.imgs.map((x,i)=>`<button data-bi="${i}" style="padding:0;border-radius:8px;overflow:hidden;aspect-ratio:1/1;background:#222"><img src="${esc(x.u)}" alt="${esc(x.t)}" loading="lazy" referrerpolicy="no-referrer" style="width:100%;height:100%;object-fit:cover"></button>`).join("")}</div><p class="note" style="margin:4px 0 0">${ph.named?"Photos":"Photos taken near this beach"} from Wikimedia Commons. Tap a photo to enlarge.</p>`:'<p class="mute" style="margin:0">No photos found for this beach yet.</p>';
  b.querySelectorAll("[data-bi]").forEach(x=>x.onclick=()=>{const q=ph.imgs[+x.dataset.bi];beachLight(q.u,q.t)});
 }catch(e){const b=$("#bph");if(b)b.innerHTML='<p class="mute" style="margin:0">Photos could not load. Check your connection.</p>'}
 let text=about;
 try{
  const first=r.n.toLowerCase().replace(/beach|resort|bay/g,"").split(/\W+/).filter(x=>x.length>3)[0]||r.n.toLowerCase();
  const u="https://en.wikipedia.org/w/api.php?action=query&generator=search&gsrsearch="+encodeURIComponent(r.n+" "+cname)+"&gsrlimit=1&prop=extracts%7Cinfo&inprop=url&exintro=1&explaintext=1&exchars=700&format=json&origin=*";
  const j=JSON.parse(await netGet(u,12));const p=Object.values((j.query&&j.query.pages)||{})[0];
  if(p&&p.extract&&p.title.toLowerCase().includes(first)){
   text=p.extract;const a=$("#bab");if(a&&!BINFO[r.n])a.textContent=p.extract;
   const sr=$("#bsrc");if(sr&&/^https:\/\//.test(p.fullurl||""))sr.innerHTML=`<a href="${esc(p.fullurl)}" target="_blank" rel="noopener" style="font-size:12px;color:var(--acc)">Read more on Wikipedia</a>`}
 }catch(e){}
 const todo=BDO.filter(x=>x[0].test(text+" "+about)).map(x=>x[1]);
 const th=$("#bth");if(th&&todo.length)th.innerHTML=`<h3 style="margin:14px 0 4px">What you can do here</h3><div style="display:flex;flex-wrap:wrap;gap:6px">${todo.map(x=>`<span style="border:1px solid var(--line);border-radius:999px;padding:6px 12px;font-size:14px">${esc(x)}</span>`).join("")}</div><p class="note" style="margin:4px 0 0">Based on the description of this beach.</p>`;
}
async function beachCountry(cc,name){
 const head=s=>`<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><button id="npb" style="font-size:22px;padding:4px 10px">←</button><div><b style="font-size:18px">${bFlag(cc)} Beaches in ${esc(name)}</b><div class="mute" style="font-size:13px">${s}</div></div></div>`;
 open(head("Loading the list…")+'<p class="mute" style="padding:20px 0">Please wait…</p><button class="btn ghost" id="x">Close</button>');$("#npb").onclick=()=>beachHome();
 try{
  const seen={},rows=[];
  const BD=await beachData(),pre=BD&&BD[cc];
  if(pre&&pre.length){pre.forEach(p=>rows.push({n:p[0],la:p[1],lo:p[2],t:p[4]||{},area:p[3]||"",key:bKey(cc,p[0])}))}
  else{
  const q=`[out:json][timeout:25];area["ISO3166-1"="${cc}"][admin_level=2]->.a;nwr["natural"="beach"]["name"](area.a);out center 300;`;
  const hosts=["https://overpass-api.de/api/interpreter","https://overpass.kumi.systems/api/interpreter","https://overpass.private.coffee/api/interpreter"];
  const txt=await Promise.any(hosts.map(h=>netGet(h+"?data="+encodeURIComponent(q),28)));

  (JSON.parse(txt).elements||[]).forEach(e=>{const la=e.lat??(e.center&&e.center.lat),lo=e.lon??(e.center&&e.center.lon);if(la==null||lo==null)return;const t=e.tags||{},n=t.name;if(!n)return;const k=n+"|"+la.toFixed(2)+"|"+lo.toFixed(2);if(seen[k])return;seen[k]=1;
   rows.push({n,la,lo,t,area:t["addr:city"]||t["addr:state"]||t["is_in:state"]||t["is_in"]||"",key:bKey(cc,n)})});
  }
  const L=window.__loc;rows.forEach(r=>r.d=L?npDist(L.lat,L.lng,r.la,r.lo):null);
  rows.sort((a,b)=>{const ca=BINFO[a.n]?0:1,cb=BINFO[b.n]?0:1;if(ca!==cb)return ca-cb;const ra=bAvg(a.key).avg,rb=bAvg(b.key).avg;if(ra!==rb)return rb-ra;if(a.d!=null&&b.d!=null)return a.d-b.d;return a.n<b.n?-1:1});
  const show=rows.slice(0,120);
  const li=r=>{const s=bAvg(r.key);return `<button data-br="${rows.indexOf(r)}" style="display:block;width:100%;text-align:left;color:inherit;padding:12px 0;border-bottom:1px solid var(--line)"><div style="display:flex;justify-content:space-between;gap:8px"><b>🏖️ ${esc(r.n)}</b><span class="mute" style="white-space:nowrap">${r.d!=null?npFmt(r.d):""}</span></div><div style="font-size:13px">${bStarTxt(s.avg,s.n)}</div><div class="mute" style="font-size:12px">${r.area?esc(r.area)+" · ":""}${r.la.toFixed(3)}, ${r.lo.toFixed(3)}</div></button>`};
  open(head(rows.length?rows.length+" beaches"+(rows.length>120?" (showing 120)":"")+(L?", nearest first":""):"")+(rows.length?`<input class="in" id="bq" placeholder="Search beaches" aria-label="Search beaches" style="margin-top:0"><div id="bl">${show.map(li).join("")}</div>`:'<p class="mute" style="padding:20px 0">No named beaches found for this country on the map yet.</p>')+`<p class="note">Beaches come from OpenStreetMap contributors. Star ratings come from WorldLink users.</p><button class="btn ghost" id="x">Close</button>`);
  $("#npb").onclick=()=>beachHome();
  $("#panel").querySelectorAll("[data-br]").forEach(b=>b.onclick=()=>beachDetail(rows[+b.dataset.br],cc,name));
  const bq=$("#bq");if(bq)bq.oninput=e=>{const v=e.target.value.trim().toLowerCase();$("#panel").querySelectorAll("[data-br]").forEach(b=>b.style.display=!v||rows[+b.dataset.br].n.toLowerCase().includes(v)?"block":"none")};
 }catch(e){
  open(head("")+'<p style="padding:14px 0">The map servers are busy or slow. Try again in a minute.</p><button class="btn" id="npr">Try again</button><button class="btn ghost" id="x">Close</button>');
  $("#npb").onclick=()=>beachHome();$("#npr").onclick=()=>beachCountry(cc,name)}
}
function beachDetail(r,cc,name){
 const s=bAvg(r.key),t=r.t||{};
 const about=BINFO[r.n]||t.description||"A beach listed on the map. Check sea conditions, safety and any entry fee locally before you go.";
 const fee=t.fee?(/^yes$/i.test(t.fee)?"There is an entry fee. Ask at the gate for the price.":/^no$/i.test(t.fee)?"Free entry.":t.fee):(/fee|ticket|paid|entry/i.test(about)?"An entry fee is mentioned in the description above. Ask at the gate for today's price.":"Not listed. Ask at the gate or check the beach's own page before you go.");
 const facts=[["Access",t.access],["Surface",t.surface],["Lifeguard",t.lifeguard],["Toilets",t.toilets],["Opening hours",t.opening_hours],["Website",t.website||t["contact:website"]],["Phone",t.phone||t["contact:phone"]]].filter(x=>x[1]);
 open(`<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><button id="npb" style="font-size:22px;padding:4px 10px">←</button><div><b style="font-size:20px">🏖️ ${esc(r.n)}</b><div class="mute" style="font-size:13px">${bFlag(cc)} ${esc(name)}${r.area?" · "+esc(r.area):""}</div></div></div>
 <div id="bph" style="margin:8px 0"><p class="mute" style="margin:0">Loading photos…</p></div>
 <div style="font-size:16px;margin:6px 0" id="bst">${bStarTxt(s.avg,s.n)}</div>
 <div style="display:flex;gap:6px;align-items:center;margin:6px 0"><span class="mute" style="font-size:13px">${s.me?"Your rating":"Rate it"}:</span>${[1,2,3,4,5].map(i=>`<button data-rt="${i}" aria-label="${i} star" style="font-size:28px;color:${i<=s.me?"#F5B301":"var(--mute)"};padding:0 2px">${i<=s.me?"★":"☆"}</button>`).join("")}</div>
 <p class="note" style="margin:0 0 6px">Stars come from WorldLink visitors. Tap a star after you visit.</p>
 <h3 style="margin:14px 0 4px">About</h3><p style="margin:0" id="bab">${esc(about)}</p><div id="bsrc"></div>
 <div id="bth"></div>
 <h3 style="margin:14px 0 4px">Gate fee</h3><p style="margin:0">${esc(fee)}</p>
 ${facts.length?`<h3 style="margin:14px 0 4px">Details</h3>${facts.map(f=>`<div style="padding:6px 0;border-bottom:1px solid var(--line)"><span class="mute">${f[0]}:</span> ${esc(String(f[1]))}</div>`).join("")}`:""}
 <h3 style="margin:14px 0 4px">Location</h3><p class="mute" style="margin:0">${r.la.toFixed(5)}, ${r.lo.toFixed(5)}${r.d!=null?" · "+npFmt(r.d)+" from you":""}</p>
 <button class="btn" id="bdr" style="margin-top:12px">Get directions</button><p class="note" style="margin:4px 0 0">Opens Google Maps with the route from where you are.</p><button class="btn ghost" id="bmp">See it on the map</button><button class="btn ghost" id="x">Close</button>`);
 beachExtra(r,name,about);
 $("#npb").onclick=()=>beachCountry(cc,name);
 $("#bdr").onclick=()=>openUrl("https://www.google.com/maps/dir/?api=1&destination="+r.la+","+r.lo+"&travelmode=driving");
 $("#bmp").onclick=()=>openUrl("https://www.google.com/maps/search/?api=1&query="+r.la+","+r.lo);
 $("#panel").querySelectorAll("[data-rt]").forEach(b=>b.onclick=()=>{const v=+b.dataset.rt,o=bRate(),x=o[r.key]||{s:0,n:0,me:0};if(x.me){x.s-=x.me}else x.n+=1;x.s+=v;x.me=v;o[r.key]=x;bSave(o);beachDetail(r,cc,name)});
}
