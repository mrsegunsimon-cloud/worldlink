"""Make chat Send reliable on phones: Enter key, touch fallback. Usage: patch_send.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function wireSend(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
fn='''function wireSend(){
 const b=$("#ms"),i=$("#mi");if(!b||!i)return;
 i.setAttribute("enterkeyhint","send");
 i.addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();b.click()}});
 b.style.touchAction="manipulation";
 b.addEventListener("touchend",e=>{e.preventDefault();b.click()},{passive:false});
}
'''
rep('async function chat(p){',fn+'async function chat(p){')
rep(' $("#bk").onclick=inbox;\n $("#vc").onclick=()=>{close();startCall(p,false)};',' $("#bk").onclick=inbox;wireSend();\n $("#vc").onclick=()=>{close();startCall(p,false)};')
rep(' $("#bk").onclick=()=>{dmCur=null;loadDMS().then(inbox)};\n $("#ms").onclick',' $("#bk").onclick=()=>{dmCur=null;loadDMS().then(inbox)};wireSend();\n $("#ms").onclick')
open(sys.argv[2],'w',encoding='utf8').write(s)
