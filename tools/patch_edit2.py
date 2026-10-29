import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'wlEd2' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:50]
    s=s.replace(a,b)
# resume audio so playback does not stall
rep('const out=new MediaStream([...c.captureStream(25).getVideoTracks(),...tracks]);\n     const mt=["video/mp4","video/webm;codecs=vp9,opus","video/webm"].find(m=>MediaRecorder.isTypeSupported(m))||"";\n     const rc=new MediaRecorder(out,mt?{mimeType:mt,videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{}),ch=[];\n     rc.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};\n     let run=true;const draw=()=>{if(!run)return;x.drawImage(v,sx,sy',
    'const out=new MediaStream([...c.captureStream(25).getVideoTracks(),...tracks]);/*wlEd2*/try{ac&&ac.resume()}catch(e){}\n     const mt=["video/mp4","video/webm;codecs=vp9,opus","video/webm"].find(m=>MediaRecorder.isTypeSupported(m))||"";\n     const rc=new MediaRecorder(out,mt?{mimeType:mt,videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{}),ch=[];\n     rc.ondataavailable=e=>{if(e.data&&e.data.size)ch.push(e.data)};\n     let run=true;const draw=()=>{if(!run)return;x.drawImage(v,sx,sy')
# too big: tell what to do and open the editor
rep(' if(f.size>20*1048576){st.textContent="That video is over 20 MB. Record a shorter one.";return}\n $("#go").disabled=true;st.textContent="Posting…";\n const it={id:"v"+Date.now(),u:me.name,uid:me.uid,c:cap||"My first WorldLink video"',
    ' if(f.size>20*1048576){st.textContent="That video is over 20 MB ("+Math.round(f.size/1048576)+" MB). Opening the editor so you can cut it shorter…";setTimeout(()=>editVideo(f,true),900);return}\n $("#go").disabled=true;st.textContent="Posting…";\n const it={id:"v"+Date.now(),u:me.name,uid:me.uid,c:cap||"My first WorldLink video"')
rep('function editVideo(f){','function editVideo(f,big){')
# big file: after editing, if still too big say so; show hint on top
rep('<p id="evt" class="note" style="color:#fff;text-align:center;margin:8px 0 2px">Loading…</p>','<p id="evt" class="note" style="color:#fff;text-align:center;margin:8px 0 2px">Loading…</p>${big?\'<p class="note" style="color:#FFB454;text-align:center;margin:0">This video is over 20 MB. Move the End slider to keep a shorter part (about 30 to 60 seconds), then tap Done.</p>\':""}')
open(p,'w',encoding='utf8').write(s);print('patched')
