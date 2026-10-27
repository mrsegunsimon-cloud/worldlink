"""Photos and videos in chat; photo posts with music. Usage: patch_media.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function vidPut(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70])
    s=s.replace(a,b)
rep('overflow-wrap:anywhere">${esc(b.t)}</span>','overflow-wrap:anywhere">${bodyOf(b)}</span>',3)
rep('d.m[d.m.length-1].t.slice(0,50)','(x=>x.t?x.t.slice(0,50):x.img?"📷 Photo":"🎥 Video")(d.m[d.m.length-1])')
# chat(p): one send function that text, photos and videos share
rep('''$("#ms").onclick=async()=>{
  const v=$("#mi").value.trim();if(!v)return;
  m.push({t:v,ts:Date.now()});
  try{const D=await claude.use("db");if(D&&me.uid)await D.collection("data/users/"+me.uid).doc("chat-"+p).set({m:m.slice(-100)})}catch(e){}
  chat(p);
 };''','''const sendObj=async o=>{
  m.push(Object.assign({ts:Date.now()},o));
  try{const D=await claude.use("db");if(D&&me.uid)await D.collection("data/users/"+me.uid).doc("chat-"+p).set({m:m.slice(-100)})}catch(e){}
  chat(p);
 };window.__sendMsg=sendObj;
 $("#ms").onclick=()=>{const v=$("#mi").value.trim();if(!v)return;sendObj({t:v})};''')
rep('''$("#ms").onclick=async()=>{
  const v=$("#mi").value.trim();if(!v)return;
  try{const D=await claude.use("db");if(D){const s=await D.collection("dms").doc(d.id).get();if(s.exists){const r=s.data();if(r.m&&r.m.length>d.m.length)d.m=r.m}}}catch(e){}
  d.m.push({f:me.uid,n:me.name,t:v,ts:Date.now()});d.m=d.m.slice(-200);''','''const sendObj=async o=>{
  try{const D=await claude.use("db");if(D){const s=await D.collection("dms").doc(d.id).get();if(s.exists){const r=s.data();if(r.m&&r.m.length>d.m.length)d.m=r.m}}}catch(e){}
  d.m.push(Object.assign({f:me.uid,n:me.name,ts:Date.now()},o));d.m=d.m.slice(-200);''')
rep('''  notify(dmOther(d).u,"sent you a message");
  dmShow(d);
 };''','''  notify(dmOther(d).u,"sent you a message");
  dmShow(d);
 };window.__sendMsg=sendObj;
 $("#ms").onclick=()=>{const v=$("#mi").value.trim();if(!v)return;sendObj({t:v})};''')
helpers='''function vdb(){return new Promise((ok,no)=>{const r=indexedDB.open("wl-vid",1);r.onupgradeneeded=()=>r.result.createObjectStore("v");r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error)})}
async function vidPut(b){const d=await vdb(),id="vd"+Date.now().toString(36)+Math.random().toString(36).slice(2,5);await new Promise((ok,no)=>{const t=d.transaction("v","readwrite");t.objectStore("v").put(b,id);t.oncomplete=ok;t.onerror=()=>no(t.error)});return id}
async function vidGet(id){try{const d=await vdb();return await new Promise(ok=>{const q=d.transaction("v").objectStore("v").get(id);q.onsuccess=()=>ok(q.result||null);q.onerror=()=>ok(null)})}catch(e){return null}}
async function hydVid(){for(const v of document.querySelectorAll("[data-vid]")){if(v.getAttribute("src"))continue;const b=await vidGet(v.dataset.vid);if(b)v.src=URL.createObjectURL(b);else v.outerHTML='<span class="mute">Video not available on this phone</span>'}}
const bodyOf=b=>b.img?`<img src="${b.img}" alt="Photo" style="display:block;max-width:100%;border-radius:12px">`:b.vid?`<video data-vid="${esc(b.vid)}" controls playsinline preload="metadata" style="display:block;max-width:100%;border-radius:12px;background:#000"></video>`:esc(b.t||"");
'''
rep('function wireSend(){',helpers+'function wireSend(){')
rep(' i.setAttribute("enterkeyhint","send");','''i.setAttribute("enterkeyhint","send");
 const at=document.createElement("button");at.id="at";at.setAttribute("aria-label","Send a photo or video");at.textContent="📎";at.style.cssText="font-size:24px;padding:0 6px;flex:none";i.parentNode.insertBefore(at,i);
 const fi=document.createElement("input");fi.type="file";fi.accept="image/*,video/*";fi.hidden=true;i.parentNode.appendChild(fi);
 at.onclick=()=>fi.click();
 fi.onchange=async()=>{const f=fi.files[0];fi.value="";if(!f)return;const n=$("#cin .note");
  try{if(f.type.startsWith("image/")){window.__sendMsg({img:await cPhoto(f,720)})}else if(f.type.startsWith("video/")){if(f.size>25*1048576){n.textContent="That video is over 25 MB.";return}n.textContent="Sending…";window.__sendMsg({vid:await vidPut(f)})}else n.textContent="Choose a photo or a video."}catch(e){n.textContent="That file could not be sent."}};
 hydVid();''')
# photo posts can carry music: the photo becomes a short video with the song
fn='''function photoToVideo(f,song,secs,prog){
 return new Promise((ok,no)=>{
  try{
   const AC=window.AudioContext||window.webkitAudioContext;if(!AC||!window.MediaRecorder)return no(new Error("This phone cannot add music."));
   const im=new Image();im.onerror=()=>no(new Error("The photo could not be read."));
   im.onload=async()=>{
    try{
     const W=720,H=1280,c=document.createElement("canvas");c.width=W;c.height=H;const x=c.getContext("2d");
     x.fillStyle="#000";x.fillRect(0,0,W,H);const k=Math.min(W/im.width,H/im.height),w=im.width*k,h=im.height*k;x.drawImage(im,(W-w)/2,(H-h)/2,w,h);
     const ac=new AC(),d=ac.createMediaStreamDestination(),au=new Audio(song.url);au.crossOrigin="anonymous";au.loop=true;ac.createMediaElementSource(au).connect(d);
     const cs=c.captureStream(15),out=new MediaStream([...cs.getVideoTracks(),...d.stream.getAudioTracks()]);
     const mt=["video/mp4","video/webm;codecs=vp9,opus","video/webm"].find(m=>MediaRecorder.isTypeSupported(m))||"";
     const rc=new MediaRecorder(out,mt?{mimeType:mt,videoBitsPerSecond:1000000,audioBitsPerSecond:128000}:{}),ch=[];
     rc.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};
     const t0=Date.now(),tk=setInterval(()=>{x.drawImage(im,(W-w)/2,(H-h)/2,w,h);if(prog)prog(Math.min(1,(Date.now()-t0)/(secs*1000)))},200);
     rc.onstop=()=>{clearInterval(tk);try{au.pause();ac.close()}catch(e){}const type=(rc.mimeType||mt||"video/webm").split(";")[0];ok(new File(ch,"photo."+(type.includes("mp4")?"mp4":"webm"),{type}))};
     rc.start();await au.play().catch(()=>{});setTimeout(()=>{if(rc.state==="recording")rc.stop()},secs*1000)
    }catch(e){no(e)}
   };
   im.src=URL.createObjectURL(f);
  }catch(e){no(e)}
 })
}
'''
rep('function photoForm(f){',fn+'function photoForm(f){')
rep('<p class="note" id="st">Photos are shared in Social, up to 5 MB.</p><button class="btn" id="go">Post to Social</button>','<button class="btn ghost" id="pmp" style="margin-top:8px">♪ Post as a video with music</button><p class="note" id="st">Photos are shared in Social, up to 5 MB.</p><button class="btn" id="go">Post to Social</button>')
rep(' $("#bk").onclick=recorder;\n $("#go").onclick=async()=>{\n  if(f.size>5*1048576',''' $("#bk").onclick=recorder;
 $("#pmp").onclick=()=>soundPicker(()=>{
  if(!SND)return photoForm(f);
  const sd=SND;SND=null;
  open(`<h2>Making your video</h2><p class="mute">Putting "${esc(sd.name)}" with your photo for 15 seconds. Keep this screen open.</p><div style="height:8px;border-radius:4px;background:var(--line)"><div id="mb" style="height:100%;width:0;border-radius:4px;background:var(--acc)"></div></div>`);
  photoToVideo(f,sd,15,p=>{const b=$("#mb");if(b)b.style.width=Math.round(p*100)+"%"}).then(vf=>postForm(vf,"Photo with music: "+sd.name)).catch(e=>{photoForm(f);const st=$("#st");if(st)st.textContent="Could not add music: "+(e.message||"try again")})
 });
 $("#go").onclick=async()=>{
  if(f.size>5*1048576''')
open(sys.argv[2],'w',encoding='utf8').write(s)
