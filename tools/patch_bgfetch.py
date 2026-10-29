import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function bgfUp' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70])
    s=s.replace(a,b)
code=r'''async function bgfUp(nf,job,prog){
 try{
  if(!(window.WLCloud&&WLCloud.spec&&navigator.serviceWorker&&location.protocol==="https:"))return null;
  const reg=await Promise.race([navigator.serviceWorker.ready,new Promise(r=>setTimeout(()=>r(null),4000))]);
  if(!reg||!reg.backgroundFetch)return null;
  let bf=await reg.backgroundFetch.get(job.id);
  if(!bf){
   const sp=WLCloud.spec(nf),t=await WLN("token");if(!sp||!t||!t.token)return null;
   job.meta={doc:WLCloud.docUrl("videos",job.id),token:t.token,pub:sp.pub,u:me.name,uid:me.uid||""};await jPut(job);
   bf=await reg.backgroundFetch.fetch(job.id,new Request(sp.url,{method:"POST",headers:sp.headers,body:nf}),{title:"Uploading your video to WorldLink",downloadTotal:4096,uploadTotal:nf.size});
  }
  return await new Promise(ok=>{
   let last=-1,t0=Date.now();const stall=setInterval(()=>{const u=bf.uploaded||0;if(u!==last){last=u;t0=Date.now()}else if(u===0&&Date.now()-t0>25000){clearInterval(stall);try{bf.abort()}catch(e){}ok(null)}},3000);
   const chk=()=>{prog(Math.min(1,(bf.uploaded||0)/nf.size));if(bf.result==="success"){clearInterval(stall);ok({url:job.meta.pub})}else if(bf.result==="failure"){clearInterval(stall);ok(null)}};
   bf.addEventListener("progress",chk);chk()})
 }catch(e){return null}
}
try{if(navigator.serviceWorker)navigator.serviceWorker.addEventListener("message",e=>{const d=e.data||{};if(d.type==="posted"||d.type==="upfail"){try{window.wlRefresh&&wlRefresh()}catch(x){}}})}catch(e){}
'''
rep('async function bgRun(job){',code+'async function bgRun(job){')
rep('  const base=burn?.45:0;bgRing(base,"","Uploading");',
'''  if(job.uploaded&&job.meta){try{const D=await claude.use("db");await D.collection("videos").doc(job.id).set({id:job.id,url:job.meta.pub,c:job.cap||"My first WorldLink video",u:me.name,uid:me.uid||null,ts:Date.now()});await jDel(job.id);BGB=false;try{wlRefresh()}catch(e){}return bgRing(1,"ok","Posted")}catch(e){return fail("Tap to finish posting",()=>bgRun(job))}}
  const base=burn?.45:0;bgRing(base,"","Uploading");''')
rep('const r=await A.upload(nf,q=>bgRing(base+q*(1-base),"","Uploading"));','const pg=q=>bgRing(base+q*(1-base),"","Uploading");const r=(await bgfUp(nf,job,pg))||await A.upload(nf,pg);')
open(p,'w',encoding='utf8').write(s);print('patched')
