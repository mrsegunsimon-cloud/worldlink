"""If the preview video is blocked in the viewer's country, show the photo instead. Usage: patch_prev2.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'listening",id:1' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('?rel=0&playsinline=1${auto?"&autoplay=1&mute=1&end=45":""}"','?rel=0&playsinline=1${auto?"&autoplay=1&mute=1&end=45&enablejsapi=1":""}"')
rep(' $("#sb").onclick=back;const u=n[4];',''' if(auto){const f=$("#panel").querySelector("iframe");if(f){
  const h=e=>{if(e.source!==f.contentWindow)return;let d=e.data;if(typeof d==="string"){try{d=JSON.parse(d)}catch(_){return}}
   if(d&&d.event==="onError"){window.removeEventListener("message",h);const bx=f.parentNode;
    if(bx&&bx.parentNode){const nt=bx.nextElementSibling;if(nt&&/Preview:/.test(nt.textContent))nt.textContent="This video is blocked in your country, so here is the story photo instead.";
     bx.outerHTML=n[5]&&/^https:\\/\\//.test(n[5])?`<img src="${esc(n[5])}" alt="" referrerpolicy="no-referrer" style="width:100%;border-radius:14px;max-height:34vh;object-fit:cover;background:#111">`:cover(tl,em,Math.round(innerHeight*.34),lab,sportPh(key&&key[0],n))}}};
  window.addEventListener("message",h);
  f.addEventListener("load",()=>{try{f.contentWindow.postMessage(JSON.stringify({event:"listening",id:1,channel:"widget"}),"*")}catch(e){}})}}
 $("#sb").onclick=back;const u=n[4];''')
open(sys.argv[2],'w',encoding='utf8').write(s)
