import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlFit" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep('<button id="pvt" aria-label="Play or pause" style="position:absolute;inset:0;width:100%;background:none"></button>',
    '<button id="pvt" aria-label="Play or pause" style="position:absolute;inset:0;width:100%;background:none"></button><button id="pvf" aria-label="Fit or fill the screen" style="position:absolute;top:70px;right:14px;z-index:3;padding:9px 14px;border-radius:999px;background:rgba(0,0,0,.55);color:#fff;font-weight:800;font-size:14px;border:1px solid rgba(255,255,255,.4)">⤢ Fit</button>')
rep(' {const pv=$("#pvv");if(pv){pv.play().catch(()=>{});$("#pvt").onclick=()=>{pv.paused?pv.play().catch(()=>{}):pv.pause()}}}\n',
    ''' {const pv=$("#pvv");if(pv){pv.play().catch(()=>{});$("#pvt").onclick=()=>{pv.paused?pv.play().catch(()=>{}):pv.pause()}}}
 /*wlFit*/{const pv=$("#pvv"),fb=$("#pvf");if(pv&&fb){let fit=false;const set=v=>{fit=v;pv.style.objectFit=fit?"contain":"cover";fb.textContent=fit?"⤢ Fill":"⤢ Fit"};fb.onclick=()=>set(!fit);const auto=()=>{if(pv.videoWidth&&pv.videoHeight&&pv.videoWidth>pv.videoHeight*1.05)set(true)};pv.addEventListener("loadedmetadata",auto);auto()}}
''')
# the home feed: wide videos are not zoomed
rep('$("#feed").addEventListener("keydown",','document.addEventListener("loadedmetadata",e=>{const v=e.target;if(v&&v.tagName==="VIDEO"&&v.closest&&v.closest("#feed")&&v.videoWidth>v.videoHeight*1.05)v.style.objectFit="contain"},true);\n$("#feed").addEventListener("keydown",')
s=s.replace('2026.10.30-L','2026.10.30-M')
open(P,"w",encoding="utf8").write(s);print("ok")
