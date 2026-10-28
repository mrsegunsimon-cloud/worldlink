"""Owners can delete their own videos. Usage: patch_owner.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function ownVideo(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('else if(a==="rp")reportFlow("video",CLIPS[i].id,CLIPS[i].uid,CLIPS[i].u);','else if(a==="rp"){const c=CLIPS[i];if(me.uid&&c.uid&&c.uid===me.uid)ownVideo(i);else reportFlow("video",c.id,c.uid,c.u)}')
fn='''function ownVideo(i){
 const c=CLIPS[i];
 open(`<h2>Your video</h2><p class="mute">${esc(c.c||"")}</p><p class="note" id="st">Deleting removes it for everyone. This cannot be undone.</p><button class="btn red" id="dv">Delete this video</button><button class="btn ghost" id="x">Keep it</button>`);
 $("#dv").onclick=async()=>{
  $("#dv").disabled=true;$("#st").textContent="Deleting…";
  try{const D=await claude.use("db");if(D&&c.id){const r=await D.collection("videos").doc(c.id).get();if(r.exists)await D.collection("videos").doc(c.id).set(Object.assign(r.data(),{del:true}))}}catch(e){}
  const k=CLIPS.indexOf(c);if(k>=0)CLIPS.splice(k,1);close();tab(1);
 };
}
'''
rep('function sell(){',fn+'function sell(){')
open(sys.argv[2],'w',encoding='utf8').write(s)
