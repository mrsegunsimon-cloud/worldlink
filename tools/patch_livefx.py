import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'id="lfxb"' in s: print('already');sys.exit()
a=' startCam().then(ok=>{if(!ok&&$("#st"))$("#st").textContent="Camera not available in this preview. On your phone, allow the camera when asked."});\n const L=$("#lc");'
assert s.count(a)==1
add=r''' {const rv=$("#rv");if(rv&&rv.parentNode){
  rv.parentNode.insertAdjacentHTML("beforeend",`<div id="lsk" aria-hidden="true" style="position:absolute;top:22%;left:50%;transform:translateX(-50%);font-size:96px;pointer-events:none"></div><button id="lfxb" aria-label="Filters and stickers" style="position:absolute;right:12px;top:96px;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,.5);color:#fff;font-size:22px">✨</button><div id="lfp" style="display:none;position:absolute;left:0;right:0;bottom:64px;background:rgba(0,0,0,.6);padding:8px 0"><div style="display:flex;gap:6px;overflow-x:auto;padding:2px 10px">${FX.map((f,k)=>`<button data-lf="${k}" style="flex:none;padding:7px 12px;border-radius:999px;font-weight:700;font-size:13px;background:${k===0?"#fff":"rgba(255,255,255,.18)"};color:${k===0?"#000":"#fff"}">${f[0]}</button>`).join("")}</div><div style="display:flex;gap:6px;overflow-x:auto;padding:8px 10px 2px">${STK.map((e,k)=>`<button data-ls="${k}" style="flex:none;min-width:40px;padding:6px 10px;border-radius:999px;font-size:20px;background:${k===0?"#fff":"rgba(255,255,255,.18)"};color:${k===0?"#000":"#fff"}">${e||"None"}</button>`).join("")}</div></div>`);
  $("#lfxb").onclick=()=>{const q=$("#lfp");q.style.display=q.style.display==="none"?"block":"none"};
  const mark=(sel,on)=>document.querySelectorAll(sel).forEach(x=>{const y=x===on;x.style.background=y?"#fff":"rgba(255,255,255,.18)";x.style.color=y?"#000":"#fff"});
  $("#lfp").onclick=e=>{const f=e.target.closest("[data-lf]"),t=e.target.closest("[data-ls]");
   if(f){rv.style.filter=FX[+f.dataset.lf][1];mark("[data-lf]",f)}
   if(t){$("#lsk").textContent=STK[+t.dataset.ls];mark("[data-ls]",t)}};
 }}
'''
s=s.replace(a,a.split('\n')[0]+'\n'+add+' const L=$("#lc");')
open(p,'w',encoding='utf8').write(s);print('patched')
