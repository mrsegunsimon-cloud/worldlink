/* ===== Places near you (app only): real places from OpenStreetMap around the phone's location ===== */
const NP={
 restaurant:["Restaurants","🍽️",'["amenity"~"^(restaurant|fast_food)$"]',4000],
 park:["Parks","🌳",'["leisure"~"^(park|garden|nature_reserve)$"]',6000],
 attraction:["Attractions","🎡",'["tourism"~"^(attraction|museum|zoo|theme_park|gallery|viewpoint)$"]',20000],
 hotel:["Hotels","🏨",'["tourism"~"^(hotel|guest_house|hostel|motel)$"]',6000],
 airport:["Airports","✈️",'["aeroway"="aerodrome"]',100000],
 train:["Train stations","🚆",'["railway"="station"]',40000],
 bus:["Bus terminals","🚌",'["amenity"="bus_station"]',25000],
 atm:["ATMs","🏧",'["amenity"="atm"]',3000]};
const NPS=[["restaurant","Restaurants","Where to eat near you"],["park","Parks","Green spaces to relax in"],["attraction","Attractions","Things to see and do"],["hotel","Hotels","Places to stay"],["airport","Airports","Flights and transfers"],["train","Train stations","Rail travel"],["bus","Bus terminals","Buses and coaches"],["atm","ATMs","Cash machines nearby"]];
function nearGrid(){
 return `<p class="note" style="margin:10px 0 0">Tap a place type to list places near you. Tap one to open it in Maps.</p><div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-top:10px">${NPS.map(it=>{const g=GRAD[hsh(it[1])%GRAD.length];return `<a href="#" data-np="${it[0]}" style="display:block;color:inherit;text-decoration:none">${PH[it[0]]?`<img src="${PH[it[0]]}" alt="${esc(it[1])}" loading="lazy" style="display:block;width:100%;height:104px;object-fit:cover;border-radius:14px">`:`<div style="height:104px;border-radius:14px;background:linear-gradient(160deg,${g[0]},${g[1]});display:grid;place-items:center;font-size:48px">${NP[it[0]][1]}</div>`}<div style="font-weight:700;margin-top:6px">${esc(it[1])}</div><div class="mute" style="font-size:13px;line-height:1.3">${esc(it[2])}</div></a>`}).join("")}</div>`;
}
async function netGet(url,sec){
 sec=sec||25;
 const job=window.WLAuth?WLN("get",{url:url,timeout:sec}).then(r=>{if(r.error)throw new Error(r.error);return r.body}):fetch(url).then(r=>{if(!r.ok)throw new Error("HTTP "+r.status);return r.text()});
 return Promise.race([job,new Promise((_,no)=>setTimeout(()=>no(new Error("The places service is slow right now.")),(sec+3)*1000))])}
const NQ={restaurant:"restaurant",park:"park",attraction:"tourist attraction",hotel:"hotel",airport:"airport",train:"train station",bus:"bus station",atm:"atm"};
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
function openUrl(u){if(window.WLAuth)WLN("open",{url:u});else window.open(u,"_blank","noopener")}
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
  open(head(top.length+" found within "+npFmt(rad/1000)+" of "+esc(loc.label))+(top.length?li:'<p class="mute" style="padding:20px 0">Nothing found nearby. Try another city.</p>')+`<button class="btn ghost" id="npc">Search another city</button><p class="note">Places come from OpenStreetMap contributors. Tap a place to open it in Maps.</p><button class="btn ghost" id="x">Close</button>`);
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
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-np]");if(b){e.preventDefault();e.stopPropagation();nearList(b.dataset.np)}},true);
