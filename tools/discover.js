/* Discover: free full songs (Audius), 30-second previews of any hit (Apple iTunes), official music videos (YouTube embeds) */
var DSA=null,DSK="",DSU={},DSV=null;
const DS_SITE="https://worldlink.app/";
async function dsGet(u){if(typeof WLN!=="function")return null;const r=await WLN("get",{url:u,timeout:20});if(!r||r.error||!r.body)return null;try{return JSON.parse(r.body)}catch(e){return null}}
const dsOk=u=>typeof u==="string"&&/^https:\/\//.test(u);
setInterval(()=>{const sh=document.getElementById("sheet");if(DSA&&!DSA.paused&&!(sh&&sh.classList.contains("on")))DSA.pause()},500);
function dsPlay(k,btn){
 if(DSA&&DSK===k&&!DSA.paused){DSA.pause();btn.textContent="▶";return}
 if(DSA)DSA.pause();
 document.querySelectorAll("[data-dsp]").forEach(b=>b.textContent="▶");
 DSA=new Audio(DSU[k]);DSK=k;
 DSA.play().then(()=>{btn.textContent="❚❚"}).catch(()=>{btn.textContent="▶"});
 DSA.onended=()=>{btn.textContent="▶"};
 DSA.onerror=()=>{btn.textContent="▶"};
}
function dsRow(k,img,t,a,note,extra){
 return `<div class="cm" style="display:flex;align-items:center;gap:10px">${dsOk(img)?`<img src="${esc(img)}" alt="" loading="lazy" referrerpolicy="no-referrer" style="width:46px;height:46px;border-radius:8px;object-fit:cover;background:#222;flex:none">`:`<span style="width:46px;height:46px;border-radius:8px;background:#222;display:grid;place-items:center;flex:none">🎵</span>`}<div style="flex:1;min-width:0"><b style="display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(t)}</b><div class="mute" style="font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${esc(a)}${note?" · "+esc(note):""}</div>${extra||""}</div><button class="btn ghost" data-dsp="${k}" aria-label="Play or pause" style="width:auto;margin:0;padding:8px 12px">▶</button></div>`;
}
function discHtml(){
 return `<p class="note" style="margin:10px 0 4px">Search any song or artist. Full free songs play here. For hits from big labels you get a 30-second preview and a link to the full song.</p><div style="display:flex;gap:8px"><input class="in" id="dq" maxlength="80" placeholder="Song or artist" aria-label="Search music" style="margin:0;flex:1"><button class="btn" id="dgo" style="width:auto;margin:0;padding:0 18px">Search</button></div><div id="dsr"><p class="mute">Loading…</p></div><h3 style="margin:18px 0 6px;font-size:17px">🎬 Official music videos</h3><div id="dsv"><p class="mute">Loading…</p></div>`;
}
async function dsSearch(q){
 const box=$("#dsr");if(!box)return;
 box.innerHTML='<p class="mute">Searching…</p>';
 const E=encodeURIComponent(q);
 const [au,it]=await Promise.all([
  dsGet(q?`https://api.audius.co/v1/tracks/search?query=${E}&app_name=WorldLink&limit=12`:`https://api.audius.co/v1/tracks/trending?app_name=WorldLink&limit=12&time=week`),
  q?dsGet(`https://itunes.apple.com/search?term=${E}&media=music&entity=song&limit=12`):Promise.resolve(null)]);
 if(!$("#dsr"))return;
 DSU={};let h="";
 const A=((au&&au.data)||[]).filter(x=>x&&x.id&&x.is_streamable!==false).slice(0,12);
 A.forEach(x=>{const k="a"+x.id;DSU[k]=`https://api.audius.co/v1/tracks/${encodeURIComponent(x.id)}/stream?app_name=WorldLink`;
  const d=x.duration?Math.floor(x.duration/60)+":"+String(x.duration%60).padStart(2,"0"):"";
  h+=dsRow(k,x.artwork&&(x.artwork["150x150"]||x.artwork["480x480"]),x.title||"Untitled",(x.user&&x.user.name)||"",d)});
 const I=((it&&it.results)||[]).filter(x=>x&&dsOk(x.previewUrl)).slice(0,12);
 let h2="";
 I.forEach((x,i)=>{const k="i"+i;DSU[k]=x.previewUrl;
  h2+=dsRow(k,x.artworkUrl100,x.trackName||"",x.artistName||"","30 s preview",dsOk(x.trackViewUrl)?`<a href="${esc(x.trackViewUrl)}" target="_blank" rel="noopener" style="font-size:12px;color:var(--acc)">Full song on Apple Music</a>`:"")});
 box.innerHTML=(q?`<h3 style="margin:14px 0 4px;font-size:16px">Full songs (free)</h3>`:`<h3 style="margin:14px 0 4px;font-size:16px">Trending this week (free)</h3>`)+(h||'<p class="mute">No free full songs found for that. Try the previews below, or another spelling.</p>')+(q?`<h3 style="margin:14px 0 4px;font-size:16px">Hits (30-second previews)</h3>${h2||'<p class="mute">No previews found.</p>'}`:"")+`<p class="note">Free songs are from independent artists on Audius. Previews are from Apple iTunes. WorldLink does not copy any music. Songs play from their own services.</p>`;
 box.querySelectorAll("[data-dsp]").forEach(b=>b.onclick=()=>dsPlay(b.dataset.dsp,b));
}
function dsVideo(id,title,artist){
 const bx=$("#dsvp");if(!bx||!/^[\w-]{11}$/.test(id))return;
 bx.innerHTML=`<div style="position:relative;padding-top:56.25%;border-radius:14px;overflow:hidden;background:#000"><iframe id="dsfr" src="https://www.youtube.com/embed/${id}?rel=0&playsinline=1&autoplay=1&enablejsapi=1" title="${esc(title)}" style="position:absolute;inset:0;width:100%;height:100%;border:0" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div><div class="note" style="margin:6px 0 0">${esc(artist)}: ${esc(title)}</div><a href="https://www.youtube.com/watch?v=${id}" target="_blank" rel="noopener" style="display:block;font-size:13px;color:var(--acc)">Video not playing? Open it on YouTube</a>`;
 const f=$("#dsfr");if(!f)return;
 const h=e=>{if(e.source!==f.contentWindow)return;let d=e.data;if(typeof d==="string"){try{d=JSON.parse(d)}catch(_){return}}
  if(d&&d.event==="onError"){window.removeEventListener("message",h);bx.innerHTML=`<p class="note">This video is blocked in your country or cannot be shown here.</p><a class="btn ghost" href="https://www.youtube.com/watch?v=${id}" target="_blank" rel="noopener">Open on YouTube</a>`}};
 window.addEventListener("message",h);
 f.addEventListener("load",()=>{try{f.contentWindow.postMessage(JSON.stringify({event:"listening",id:1,channel:"widget"}),"*")}catch(e){}});
 bx.scrollIntoView({block:"nearest"});
}
async function dsVideos(sel){
 const box=$("#dsv");if(!box)return;
 if(!DSV)DSV=await dsGet(DS_SITE+"music.json?t="+Date.now());
 if(!$("#dsv"))return;
 const L=(DSV&&Array.isArray(DSV.artists)?DSV.artists:[]).filter(a=>a&&a.n&&Array.isArray(a.v)&&a.v.length);
 const q=($("#dq")&&$("#dq").value.trim())||"";
 const find=`<button class="btn ghost" id="dyt" style="margin:8px 0 0">Search YouTube for ${q?esc(q):"music videos"}</button>`;
 if(!L.length){box.innerHTML=`<p class="mute">Music videos from official channels will show here after the next update.</p>${find}`}
 else{
  const i=Math.min(Math.max(sel||0,0),L.length-1),a=L[i];
  box.innerHTML=`<div style="display:flex;gap:8px;overflow-x:auto;padding:2px 0 8px">${L.map((x,k)=>`<button class="btn${k===i?"":" ghost"}" data-da="${k}" style="margin:0;width:auto;flex:none;padding:8px 14px;white-space:nowrap">${esc(x.n)}</button>`).join("")}</div><div id="dsvp"></div><div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px">${a.v.slice(0,8).map((v,k)=>`<button data-dv="${k}" style="display:block;text-align:left;color:inherit;padding:0;min-width:0"><span style="display:block;position:relative;height:100px;border-radius:12px;overflow:hidden;background:#000"><img src="https://i.ytimg.com/vi/${esc(v[0])}/mqdefault.jpg" alt="" loading="lazy" referrerpolicy="no-referrer" style="width:100%;height:100%;object-fit:cover"><span style="position:absolute;inset:0;display:grid;place-items:center"><span style="width:38px;height:38px;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;display:grid;place-items:center">▶</span></span></span><b style="display:block;margin-top:4px;font-size:13px;line-height:1.25;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical">${esc(v[1])}</b></button>`).join("")}</div>${find}`;
  box.querySelectorAll("[data-da]").forEach(b=>b.onclick=()=>dsVideos(+b.dataset.da));
  box.querySelectorAll("[data-dv]").forEach(b=>b.onclick=()=>{const v=a.v[+b.dataset.dv];dsVideo(v[0],v[1],a.n)});
 }
 const y=$("#dyt");if(y)y.onclick=()=>{const t=($("#dq")&&$("#dq").value.trim())||"";openExt("https://www.youtube.com/results?search_query="+encodeURIComponent((t||"new")+" official music video"))};
}
function discWire(){
 const go=()=>{const q=$("#dq").value.trim();dsSearch(q);dsVideos(0)};
 $("#dgo").onclick=go;$("#dq").onkeydown=e=>{if(e.key==="Enter"){e.preventDefault();go()}};
 dsSearch("");dsVideos(0);
}
