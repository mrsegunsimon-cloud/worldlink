"""Sound button on videos (use this sound) + sound picker mixed into recordings. Usage: patch_sound.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function soundSheet(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('<div class="disc" aria-hidden="true">♪</div>','<button class="disc" data-a="snd" data-i="${i}" aria-label="Use this sound">♪</button>')
rep('  else if(a==="sh")shareSheet(i);\n  return}','  else if(a==="sh")shareSheet(i);\n  else if(a==="snd")soundSheet(i);\n  return}')
js='''
let SND=null,stopSnd=null,SNDA=null;
function sndPrev(url){try{if(SNDA){SNDA.pause();SNDA=null}if(url){SNDA=new Audio(url);SNDA.play().catch(()=>{})}}catch(e){}}
function clipSound(i){const c=CLIPS[i],nm=(c.m||"").replace(/^♪\\s*/,"");const sg=songList().find(x=>x.t&&nm.includes(x.t));if(sg)return{name:sg.t+" · "+sg.a,url:sg.url};if(c.src)return{name:nm,url:c.src};return null}
function soundSheet(i){
 const c=CLIPS[i],sd=clipSound(i);
 open(`<div style="text-align:center"><div style="font-size:44px">♪</div><h2 style="margin:4px 0">${esc((c.m||"").replace(/^♪\\s*/,""))}</h2><p class="mute" style="margin:0">Sound from @${esc(c.u)}</p></div>${sd?`<button class="btn ghost" id="sp">▶ Preview sound</button><button class="btn" id="su">🎬 Use this sound</button>`:'<p class="note">This post has no sound that can be reused.</p>'}<button class="btn ghost" id="x">Close</button>`);
 const sp=$("#sp");if(sp)sp.onclick=()=>sndPrev(sd.url);
 const su=$("#su");if(su)su.onclick=()=>{sndPrev(null);SND=sd;close();secFull=false;recorder();const st=$("#st");if(st)st.textContent="Sound ready: "+sd.name+". Tap the red button to record with it."};
 const x=$("#x");if(x)x.onclick=()=>{sndPrev(null);close()};
}
function soundPicker(){
 const L=songList();
 open(`<h2>Choose a sound</h2><p class="note" style="margin:0 0 6px">Sounds play while you record and are mixed into your video.</p>${SND?`<button class="btn ghost" id="sno">Remove sound (${esc(SND.name)})</button>`:""}${L.map((x,k)=>`<div class="cm" style="display:flex;align-items:center;gap:8px"><div style="flex:1;min-width:0"><b>${esc(x.t)}</b><div class="mute" style="font-size:12px">${esc(x.a||"")}</div></div><button class="btn ghost" data-sp="${k}" style="width:auto;margin:0;padding:8px 12px">▶</button><button class="btn" data-su="${k}" style="width:auto;margin:0;padding:8px 12px">Use</button></div>`).join("")||'<p class="mute">No sounds yet.</p>'}<button class="btn ghost" id="sbk">Back to camera</button>`);
 const back=()=>{sndPrev(null);recorder()};
 $("#sbk").onclick=back;
 const so=$("#sno");if(so)so.onclick=()=>{SND=null;back()};
 $("#panel").querySelectorAll("[data-sp]").forEach(b=>b.onclick=()=>sndPrev(L[+b.dataset.sp].url));
 $("#panel").querySelectorAll("[data-su]").forEach(b=>b.onclick=()=>{const x=L[+b.dataset.su];SND={name:x.t+(x.a?" · "+x.a:""),url:x.url};back()});
}
function mixSound(src){
 if(!SND||!window.AudioContext&&!window.webkitAudioContext)return src;
 try{const ac=new(window.AudioContext||window.webkitAudioContext)(),d=ac.createMediaStreamDestination();
  if(rs&&rs.getAudioTracks().length)ac.createMediaStreamSource(new MediaStream(rs.getAudioTracks())).connect(d);
  const au=new Audio(SND.url);au.crossOrigin="anonymous";const g=ac.createGain();g.gain.value=.8;ac.createMediaElementSource(au).connect(g);g.connect(d);g.connect(ac.destination);
  au.play().catch(()=>{});stopSnd=()=>{try{au.pause();ac.close()}catch(e){}stopSnd=null};
  return new MediaStream([...src.getVideoTracks(),...d.stream.getAudioTracks()])}catch(e){return src}
}
'''
rep('function recorder(){',js+'function recorder(){')
rep('$("#sn").onclick=()=>{$("#st").textContent="Adding a sound to your video arrives with the Android app."};','$("#sn").onclick=()=>{if(rec&&rec.state==="recording")return;soundPicker()};if(SND)$("#sn").textContent="♪ "+SND.name.slice(0,22);')
rep('  try{const long=lim>=600;rec=new MediaRecorder(src,','  src=mixSound(src);\n  try{const long=lim>=600;rec=new MediaRecorder(src,')
rep('rec.onstop=()=>{clearInterval(rt);if(stopLoop)stopLoop();','rec.onstop=()=>{clearInterval(rt);if(stopLoop)stopLoop();if(stopSnd)stopSnd();')
open(sys.argv[2],'w',encoding='utf8').write(s)
