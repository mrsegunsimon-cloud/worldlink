"""Add music after recording / to gallery videos on the post screen. Usage: patch_mix.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function mixMusic(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('function soundPicker(){','function soundPicker(cb){')
rep('const back=()=>{sndPrev(null);recorder()};','const back=()=>{sndPrev(null);cb?cb():recorder()};')
# a recorded clip already contains its song, so clear the pick before the post screen
rep('postForm(new File(chunks,"clip."+(type.includes("mp4")?"mp4":"webm"),{type}))};','SND=null;postForm(new File(chunks,"clip."+(type.includes("mp4")?"mp4":"webm"),{type}))};')
fn='''function mixMusic(f,song,prog){
 return new Promise((ok,no)=>{
  try{
   const AC=window.AudioContext||window.webkitAudioContext;if(!AC||!window.MediaRecorder)return no(new Error("This phone cannot add music after recording."));
   const v=document.createElement("video");v.src=URL.createObjectURL(f);v.playsInline=true;v.preload="auto";
   v.onerror=()=>no(new Error("The video could not be read."));
   v.onloadedmetadata=async()=>{
    try{
     const ac=new AC(),d=ac.createMediaStreamDestination();
     ac.createMediaElementSource(v).connect(d);
     const au=new Audio(song.url);au.crossOrigin="anonymous";au.loop=true;const g=ac.createGain();g.gain.value=.6;ac.createMediaElementSource(au).connect(g);g.connect(d);
     const cap=v.captureStream?v.captureStream():v.mozCaptureStream();
     const out=new MediaStream([...cap.getVideoTracks(),...d.stream.getAudioTracks()]);
     const mt=["video/mp4","video/webm;codecs=vp9,opus","video/webm"].find(m=>MediaRecorder.isTypeSupported(m))||"";
     const rc=new MediaRecorder(out,mt?{mimeType:mt,videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{});const ch=[];
     rc.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};
     const fin=()=>{try{au.pause();ac.close()}catch(e){}clearInterval(tk)};
     rc.onstop=()=>{fin();const type=(rc.mimeType||mt||"video/webm").split(";")[0];ok(new File(ch,"mixed."+(type.includes("mp4")?"mp4":"webm"),{type}))};
     v.onended=()=>{if(rc.state==="recording")rc.stop()};
     const tk=setInterval(()=>{if(prog)prog(v.currentTime,v.duration)},300);
     rc.start();await au.play().catch(()=>{});await v.play()
    }catch(e){no(e)}
   };
  }catch(e){no(e)}
 })
}
'''
rep('function postForm(f){',fn+'function postForm(f,note){')
rep(' open(`<h2>Post your video</h2><video src="${url}" controls playsinline style="width:100%;max-height:40vh;border-radius:12px;background:#000"></video><input class="in" id="cp" type="text" maxlength="100" placeholder="Write a caption" aria-label="Caption"><p class="note" id="st"></p><button class="btn" id="go">Post</button>',
 ' open(`<h2>Post your video</h2><video src="${url}" controls playsinline style="width:100%;max-height:40vh;border-radius:12px;background:#000"></video><button class="btn ghost" id="pmu" style="margin-top:8px">♪ ${note?"Change music":"Add music"}</button><input class="in" id="cp" type="text" maxlength="100" placeholder="Write a caption" aria-label="Caption"><p class="note" id="st">${note?esc(note):""}</p><button class="btn" id="go">Post</button>')
rep(' $("#bk").onclick=create;\n $("#go").onclick=()=>postVideo(f,$("#cp").value.trim());',''' $("#bk").onclick=create;
 $("#go").onclick=()=>postVideo(f,$("#cp").value.trim());
 $("#pmu").onclick=()=>soundPicker(()=>{
  if(!SND)return postForm(f,note);
  const sd=SND;SND=null;
  open(`<h2>Adding music</h2><p class="mute" id="mp">Mixing "${esc(sd.name)}" into your video. Keep this screen open. It takes about as long as the video.</p><div style="height:8px;border-radius:4px;background:var(--line)"><div id="mb" style="height:100%;width:0;border-radius:4px;background:var(--acc)"></div></div>`);
  mixMusic(f,sd,(t,dur)=>{const b=$("#mb");if(b&&dur)b.style.width=Math.min(100,Math.round(100*t/dur))+"%"}).then(nf=>postForm(nf,"Music added: "+sd.name)).catch(e=>{postForm(f,"Could not add music: "+(e.message||"try again"))})
 });''')
open(sys.argv[2],'w',encoding='utf8').write(s)
