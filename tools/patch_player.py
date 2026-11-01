import sys,re
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlPlayer1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
# 1. tracks keep artwork url; cover supports https artwork
rep('const trk=x=>({id:x.id,t:x.t,a:x.a||("@"+(x.u||"me")),url:x.url,cv:x.cv||"",lic:x.lic||"",d:x.d||0});',
    '/*wlPlayer1*/const trk=x=>({id:x.id,t:x.t,a:x.a||("@"+(x.u||"me")),url:x.url,cv:x.cv||"",lic:x.lic||"",d:x.d||0,img:x.img||""});')
rep('return c.cv&&PH[c.cv]?`<img src=',
    'return c.img&&/^https:\\/\\//.test(c.img)?`<img src="${esc(c.img)}" alt="" referrerpolicy="no-referrer" style="display:block;width:${sz}px;height:${sz}px;object-fit:cover;border-radius:${r}px;background:#222">`:c.cv&&PH[c.cv]?`<img src=')
# 2. repeat all by default so it plays on by itself and loops
rep('const PL={q:[],i:-1,a:new Audio(),shuf:false,rep:0,spd:1};','const PL={q:[],i:-1,a:new Audio(),shuf:false,rep:1,spd:1,err:0};')
# 3. lock-screen controls, artwork, state
rep('navigator.mediaSession.metadata=new MediaMetadata({title:c.t,artist:c.a});',
    'navigator.mediaSession.metadata=new MediaMetadata(Object.assign({title:c.t,artist:c.a,album:"WorldLink"},c.img&&/^https:/.test(c.img)?{artwork:[{src:c.img,sizes:"150x150"},{src:c.img,sizes:"480x480"}]}:{}));')
rep('PL.a.onplay=PL.a.onpause=()=>{miniUp();npIcons();rowMarks()};',
    'PL.a.onplay=PL.a.onpause=()=>{try{navigator.mediaSession.playbackState=PL.a.paused?"paused":"playing"}catch(e){}miniUp();npIcons();rowMarks()};PL.a.onplaying=()=>{PL.err=0};')
# 4. a broken track skips to the next one by itself
rep('PL.a.onerror=()=>{const s=$("#npe");if(s)s.textContent="This track could not load. Try the next one."};',
    'PL.a.onerror=()=>{const s=$("#npe");if(s)s.textContent="This track could not load. Skipping to the next one.";if(PL.q.length>1&&++PL.err<PL.q.length)setTimeout(()=>{if(PL.q.length)nextT(true)},900);else PL.a.pause()};')
# 5. leaving Entertainment stops the music and removes the player; closing the app stops it
rep('function miniUp(){','''function plStop(){try{PL.a.pause();PL.a.removeAttribute("src");PL.a.load()}catch(e){}PL.q=[];PL.i=-1;PL.err=0;const n=document.getElementById("np");if(n)n.remove();miniUp();try{rowMarks();navigator.mediaSession.playbackState="none";navigator.mediaSession.metadata=null}catch(e){}}
var plMiss=0;
setInterval(()=>{if(!PL.q.length){plMiss=0;return}const sh=document.getElementById("sheet");const inEnt=sh&&sh.classList.contains("on")&&document.querySelector('#panel [data-t="disc"]');if(inEnt){plMiss=0;return}if(++plMiss>=2){plMiss=0;plStop()}},500);
addEventListener("pagehide",()=>{try{PL.a.pause()}catch(e){}});
function miniUp(){''')
# 6. mini X uses same stop
rep('$("#mx").onclick=()=>{PL.a.pause();PL.q=[];PL.i=-1;const n=document.getElementById("np");if(n)n.remove();miniUp();rowMarks()};','$("#mx").onclick=plStop;')
# 7. rowMarks also marks Discover rows
rep('function rowMarks(){','function rowMarks(){document.querySelectorAll("[data-dsp]").forEach(b=>{const c=PL.q[PL.i];b.textContent=c&&c.id===DSU[b.dataset.dsp]&&!PL.a.paused?"❚❚":"▶"});')
# 8. Discover plays through the same player
rep('setInterval(()=>{const sh=document.getElementById("sheet");if(DSA&&!DSA.paused&&!(sh&&sh.classList.contains("on")))DSA.pause()},500);','var DST={};')
i=s.index('function dsPlay(k,btn){');j=s.index('function dsRow(')
s=s[:i]+'''function dsPlay(k){
 const grp=k[0],keys=Object.keys(DST).filter(x=>x[0]===grp),idx=keys.indexOf(k),c=PL.q[PL.i];
 if(idx<0)return;
 if(c&&c.id===DST[k].id){if(PL.a.paused)PL.a.play().catch(()=>{});else nowPlaying();return}
 playQ(keys.map(x=>DST[x]),idx);
}
'''+s[j:]
# 9. Discover search: more songs, genres, track objects
i=s.index('async function dsSearch(q){');j=s.index('function dsVideo(')
s=s[:i]+'''async function dsSearch(q,g){
 const box=$("#dsr");if(!box)return;
 box.innerHTML='<p class="mute">Searching…</p>';
 const E=encodeURIComponent(q||"");
 let u0=q?`https://api.audius.co/v1/tracks/search?query=${E}&app_name=WorldLink&limit=30`:(g&&g[2]?`https://api.audius.co/v1/tracks/trending?app_name=WorldLink&limit=30&time=week&genre=${encodeURIComponent(g[2])}`:(g?`https://api.audius.co/v1/tracks/search?query=${encodeURIComponent(g[1])}&app_name=WorldLink&limit=30`:`https://api.audius.co/v1/tracks/trending?app_name=WorldLink&limit=30&time=week`));
 const [au,it,au2,au3]=await Promise.all([
  dsGet(u0),
  q?dsGet(`https://itunes.apple.com/search?term=${E}&media=music&entity=song&limit=25`):Promise.resolve(null),
  (!q&&!g)?dsGet(`https://api.audius.co/v1/tracks/search?query=afrobeats&app_name=WorldLink&limit=20`):Promise.resolve(null),
  (!q&&g&&g[2])?dsGet(`https://api.audius.co/v1/tracks/search?query=${encodeURIComponent(g[1])}&app_name=WorldLink&limit=20`):Promise.resolve(null)]);
 if(!$("#dsr"))return;
 DSU={};DST={};let h="";const seen={};
 const A=[].concat((au&&au.data)||[],(au2&&au2.data)||[],(au3&&au3.data)||[]).filter(x=>x&&x.id&&x.is_streamable!==false&&!seen[x.id]&&(seen[x.id]=1)).slice(0,45);
 A.forEach(x=>{const k="a"+x.id;DSU[k]=`https://api.audius.co/v1/tracks/${encodeURIComponent(x.id)}/stream?app_name=WorldLink`;
  const im=x.artwork&&(x.artwork["480x480"]||x.artwork["150x150"]);
  DST[k]={id:DSU[k],t:x.title||"Untitled",a:(x.user&&x.user.name)||"",url:DSU[k],img:dsOk(im)?im:"",d:x.duration||0};
  const d=x.duration?Math.floor(x.duration/60)+":"+String(x.duration%60).padStart(2,"0"):"";
  h+=dsRow(k,x.artwork&&(x.artwork["150x150"]||x.artwork["480x480"]),x.title||"Untitled",(x.user&&x.user.name)||"",d)});
 const I=((it&&it.results)||[]).filter(x=>x&&dsOk(x.previewUrl)).slice(0,25);
 let h2="";
 I.forEach((x,i)=>{const k="i"+i;DSU[k]=x.previewUrl;
  DST[k]={id:x.previewUrl,t:x.trackName||"",a:x.artistName||"",url:x.previewUrl,img:dsOk(x.artworkUrl100)?x.artworkUrl100.replace("100x100","300x300"):"",d:30};
  h2+=dsRow(k,x.artworkUrl100,x.trackName||"",x.artistName||"","30 s preview",dsOk(x.trackViewUrl)?`<a href="${esc(x.trackViewUrl)}" target="_blank" rel="noopener" style="font-size:12px;color:var(--acc)">Full song on Apple Music</a>`:"")});
 const head=q?"Full songs (free)":(g?esc(g[0])+" (free)":"Trending this week (free)");
 box.innerHTML=`<h3 style="margin:14px 0 4px;font-size:16px">${head}</h3>`+(h||'<p class="mute">No free full songs found for that. Try the previews below, or another spelling.</p>')+(q?`<h3 style="margin:14px 0 4px;font-size:16px">Hits (30-second previews)</h3>${h2||'<p class="mute">No previews found.</p>'}`:"")+`<p class="note">Free songs are from independent artists on Audius. Previews are from Apple iTunes. WorldLink does not copy any music. Songs play from their own services. Tap a song to play. The next song plays by itself.</p>`;
 box.querySelectorAll("[data-dsp]").forEach(b=>b.onclick=()=>dsPlay(b.dataset.dsp));
 rowMarks();
}
'''+s[j:]
# 10. genre chips in Discover
rep('<div id="dsr"><p class="mute">Loading…</p></div>','<div style="display:flex;gap:6px;overflow-x:auto;padding:10px 0 0">${GEN.map((g,i)=>`<button data-dg="${i}" class="btn ghost" style="flex:none;width:auto;margin:0;padding:7px 13px;font-size:14px">${g[0]}</button>`).join("")}</div><div id="dsr"><p class="mute">Loading…</p></div>')
rep(' $("#dgo").onclick=go;',' $("#dgo").onclick=go;$("#panel").querySelectorAll("[data-dg]").forEach(b=>b.onclick=()=>{$("#dq").value="";$("#panel").querySelectorAll("[data-dg]").forEach(x=>x.classList.add("ghost"));b.classList.remove("ghost");dsSearch("",GEN[+b.dataset.dg])});')
# 11. Music tab points to the bigger free library
rep('<p class="note">Songs from record labels play in their own apps:</p>','<button class="btn" data-tab="disc" style="margin:10px 0 0">🌍 Find thousands more free songs</button><p class="note">Songs from record labels play in their own apps:</p>')
open(P,"w",encoding="utf8").write(s)
print("ok")
