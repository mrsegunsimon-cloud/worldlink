import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlStoryKeep" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)>=1,a[:70]
    s=s.replace(a,b,1)
# loadST: keep unsaved local stories; never wipe on failed read
rep('const s=await D.collection("stories").get();ST=s.docs.map(d=>d.data()).filter(x=>x&&x.id&&x.url&&!x.del)}catch(e){}}',
 '/*wlStoryKeep*/const s=await D.collection("stories").get();const cl=s.docs.map(d=>d.data()).filter(x=>x&&x.id&&x.url&&!x.del);const ids=new Set(cl.map(x=>x.id));ST=cl.concat(ST.filter(x=>x&&x._l&&!ids.has(x.id)&&!x.del))}catch(e){}}')
# addStory: retry, honest error, keep text
rep('''  try{const A=await claude.use("assets"),D=await claude.use("db");if(A&&D&&me.uid){const r=await A.upload(f);it.url=r.url;await D.collection("stories").doc(it.id).set(it)}}catch(e){}
  ST.push(it);stories();''','''  let ok=false,err="";
  for(let t=0;t<2&&!ok;t++){try{const A=await claude.use("assets"),D=await claude.use("db");if(!(A&&D&&me.uid)){err="Please sign in first.";break}const r=await A.upload(f);const loc=it.url;it.url=r.url;await D.collection("stories").doc(it.id).set(it);ok=true}catch(e){err="Upload failed. Check your connection and try again.";if(!/^https?:/.test(it.url))it.url=it.url}}
  if(!ok){$("#sp").disabled=false;st.textContent=err||"Could not post. Try again.";return}
  ST=ST.filter(x=>x.id!==it.id);ST.push(it);stories();''')
open(P,"w",encoding="utf8").write(s)
print("ok")
