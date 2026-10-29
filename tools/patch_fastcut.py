import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function fastCut' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
code=r'''
/* ===== Fast cut: stream-copy trimming with ffmpeg (loaded once from the website; falls back to the slow editor) ===== */
const FFB="https://worldlink.app/ffmpeg/";let FFP=null;
function ffScript(u){return new Promise((ok,no)=>{const e=document.createElement("script");e.src=u;e.onload=ok;e.onerror=()=>no(new Error("cutter download failed"));document.head.appendChild(e)})}
function ffLoad(){
 if(FFP)return FFP;
 FFP=(async()=>{
  const man=await (await fetch(FFB+"files.json",{cache:"no-cache"})).json();
  await ffScript(FFB+"ffmpeg.js");
  const FF=window.FFmpegWASM&&window.FFmpegWASM.FFmpeg;if(!FF)throw new Error("cutter missing");
  const ff=new FF();
  await Promise.race([ff.load({coreURL:FFB+"core/ffmpeg-core.js",wasmURL:FFB+"core/ffmpeg-core.wasm",classWorkerURL:FFB+man.worker}),new Promise((_,no)=>setTimeout(()=>no(new Error("cutter too slow to start")),90000))]);
  return ff;
 })();
 FFP.catch(()=>{FFP=null});
 return FFP;
}
async function fastCut(f,st,en,prog){
 const ff=await ffLoad();
 const webm=/webm/.test(f.type||"")||/\.webm$/i.test(f.name||""),ext=webm?"webm":"mp4",a="in."+ext,b="out."+ext;
 const h=({progress})=>{if(prog&&progress>=0)prog(Math.min(1,progress))};ff.on("progress",h);
 try{
  await ff.writeFile(a,new Uint8Array(await f.arrayBuffer()));
  const rc=await ff.exec(["-ss",String(st),"-i",a,"-t",String(en-st),"-c","copy","-avoid_negative_ts","make_zero","-y",b]);
  if(rc!==0)throw new Error("cut failed");
  const d=await ff.readFile(b);
  if(!d||!d.length)throw new Error("cut was empty");
  try{await ff.deleteFile(a);await ff.deleteFile(b)}catch(e){}
  return new File([d],"cut."+ext,{type:webm?"video/webm":"video/mp4"});
 }finally{try{ff.off("progress",h)}catch(e){}}
}
'''
rep('function editVideo(f,big){',code+'function editVideo(f,big){')
old='''  try{const nf=await trimCrop(f,st,en,VSHAPES[sh][1],pos,(t,d)=>{if(d>0)$("#est").textContent="Editing… "+Math.min(100,Math.round(100*t/d))+"%"});postForm(nf,"Edited: "+(en-st).toFixed(1)+" seconds")}'''
new='''  try{
   let nf=null;
   if(!sh){
    try{$("#est").textContent="Getting the fast cutter (one time only, about 30 MB)…";nf=await fastCut(f,st,en,q=>{$("#est").textContent="Cutting… "+Math.round(q*100)+"%"})}catch(e){nf=null}
   }
   if(!nf){$("#est").textContent="Editing… keep this screen open. It takes about as long as the clip.";nf=await trimCrop(f,st,en,VSHAPES[sh][1],pos,(t,d)=>{if(d>0)$("#est").textContent="Editing… "+Math.min(100,Math.round(100*t/d))+"%"})}
   postForm(nf,"Edited: "+(en-st).toFixed(1)+" seconds")}'''
rep(old,new)
open(p,'w',encoding='utf8').write(s);print('patched')
