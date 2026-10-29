"""Live like counts and view counts on profile tiles; count views; keep other people's likes when saving. Usage: patch_counts.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'bumpViews' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
rep('<span class="vw">▷ ${fmt(c.l||0)}</span>','<span class="vw">♥ ${fmt(cnt(i))} &nbsp; ▷ ${fmt(vcnt(i))}</span>')
rep('const lk=mineI.reduce((n,i)=>n+(CLIPS[i].l||0),0);','const lk=mineI.reduce((n,i)=>n+cnt(i),0);')
old_save='''async function saveR(i){
 const c=CLIPS[i],r=R[c.id]=R[c.id]||{likes:[],comments:[]};
 r.id=c.id;r.likes=(r.likes||[]).filter(u=>u!==me.uid);if(liked[i]&&me.uid)r.likes.push(me.uid);
 try{const D=await claude.use("db");if(D&&me.uid)await D.collection("reactions").doc(c.id).set(r)}catch(e){}
}'''
new_save='''const vcnt=i=>(CLIPS[i].vws||0);
async function saveR(i){
 const c=CLIPS[i],r=R[c.id]=R[c.id]||{likes:[],comments:[]};
 try{const D=await claude.use("db");if(D&&me.uid){
  try{const f=await D.collection("reactions").doc(c.id).get();if(f.exists){const d=f.data()||{};r.likes=d.likes||[];r.views=d.views||r.views||0;if((d.comments||[]).length>=(r.comments||[]).length)r.comments=d.comments||[]}}catch(e){}
  r.id=c.id;r.likes=(r.likes||[]).filter(u=>u!==me.uid);if(liked[i])r.likes.push(me.uid);
  c.o=r.likes.filter(u=>u!==me.uid).length;c.vws=r.views||c.vws||0;
  await D.collection("reactions").doc(c.id).set(r)}}catch(e){}
}
const SEEN={};
async function bumpViews(i){
 const c=CLIPS[i];if(!c||!c.uid||!me.uid)return;
 try{const D=await claude.use("db");if(!D)return;
  let r={likes:[],comments:[]};const f=await D.collection("reactions").doc(c.id).get();if(f.exists)r=Object.assign(r,f.data()||{});
  r.id=c.id;r.views=(r.views||0)+1;c.vws=r.views;R[c.id]=r;
  await D.collection("reactions").doc(c.id).set(r)}catch(e){}
}
function viewed(i){const c=CLIPS[i];if(!c||SEEN[c.id])return;SEEN[c.id]=1;if(c.uid&&c.uid===me.uid)return;c.vws=(c.vws||0)+1;bumpViews(i)}'''
rep(old_save,new_save)
rep('c.sc=r.comments||[]});','c.sc=r.comments||[];c.vws=r.views||0});')
rep('if(e.isIntersecting)v.play().catch(()=>{});else v.pause()}','if(e.isIntersecting){v.play().catch(()=>{});clearTimeout(e.target.__vt);e.target.__vt=setTimeout(()=>viewed(+e.target.dataset.i),2000)}else{v.pause();clearTimeout(e.target.__vt)}}')
open(sys.argv[2],'w',encoding='utf8').write(s)
