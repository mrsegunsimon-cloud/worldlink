"""Profile pictures. Usage: patch_pic.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function picResize(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('.av{width:46px;','.av img{width:100%;height:100%;object-fit:cover;border-radius:50%;display:block}.av{overflow:hidden;width:46px;')
# remember the picture on this phone and in the profile record
rep('me.name=d.name||me.name;me.bio=d.bio||""}','me.name=d.name||me.name;me.bio=d.bio||"";if(d.pic)me.pic=d.pic}')
rep('D.collection("profiles").doc(me.uid).set({name:me.name,bio:me.bio})','D.collection("profiles").doc(me.uid).set({name:me.name,bio:me.bio,pic:me.pic||""})')
fn='''function picResize(file){return new Promise((ok,no)=>{const fr=new FileReader();fr.onerror=no;fr.onload=()=>{const im=new Image();im.onerror=no;im.onload=()=>{const S=256,k=Math.max(S/im.width,S/im.height),w=im.width*k,h=im.height*k,c=document.createElement("canvas");c.width=S;c.height=S;c.getContext("2d").drawImage(im,(S-w)/2,(S-h)/2,w,h);ok(c.toDataURL("image/jpeg",.8))};im.src=fr.result};fr.readAsDataURL(file)})}
try{const q=localStorage.getItem("wl-pic");if(q)me.pic=q}catch(e){}
const meAv=(sz,fs,ex)=>`<div class="av" style="width:${sz}px;height:${sz}px;font-size:${fs}px;${ex||""}">${me.pic?`<img src="${me.pic}" alt="Your photo">`:esc((me.name||"y")[0].toUpperCase())}</div>`;
'''
rep('function editProfile(){',fn+'function editProfile(){')
rep('<div class="av" style="width:104px;height:104px;font-size:42px;border-color:var(--line)">${esc(me.name[0].toUpperCase())}</div>','${meAv(104,42,"border-color:var(--line)")}')
rep('  <div class="av">${c.u[0].toUpperCase()}</div>','  <div class="av">${c.uid&&c.uid===me.uid&&me.pic?`<img src="${me.pic}" alt="">`:c.u[0].toUpperCase()}</div>')
rep(' open(`<h2>Edit profile</h2><input class="in" id="nm"',' open(`<h2>Edit profile</h2><div style="text-align:center;margin-bottom:6px" id="pv">${meAv(96,40,"margin:0 auto")}</div><label class="btn ghost" style="display:block;text-align:center">📷 Choose a photo<input type="file" id="pf" accept="image/*" style="display:none"></label>${me.pic?\'<button class="btn ghost" id="pr">Remove photo</button>\':""}<input class="in" id="nm"')
rep('  const n=$("#nm").value.trim().replace(/[^a-zA-Z0-9._]/g,"");','''  const n=$("#nm").value.trim().replace(/[^a-zA-Z0-9._]/g,"");''')
rep(' $("#sv").onclick=async()=>{\n  const n=$("#nm")',''' $("#pf").onchange=async e=>{const f=e.target.files[0];if(!f)return;try{me.pic=await picResize(f);try{localStorage.setItem("wl-pic",me.pic)}catch(x){}$("#pv").innerHTML=meAv(96,40,"margin:0 auto");$("#st").textContent="Photo ready. Tap Save profile."}catch(x){$("#st").textContent="That photo could not be read."}};
 const pr=$("#pr");if(pr)pr.onclick=()=>{me.pic="";try{localStorage.removeItem("wl-pic")}catch(x){}$("#pv").innerHTML=meAv(96,40,"margin:0 auto");pr.remove()};
 $("#sv").onclick=async()=>{\n  const n=$("#nm")''')
open(sys.argv[2],'w',encoding='utf8').write(s)
