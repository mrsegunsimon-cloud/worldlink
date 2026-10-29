import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlTrimStrip3" in s: print("already");sys.exit(0)
a='<div style="flex:1;min-height:0;display:grid;place-items:center;padding:0 10px"><div id="vbox" style="max-height:100%;max-width:100%;height:100%;aspect-ratio:9/16;border-radius:10px;overflow:hidden;background:#111"><video id="evv" src="${url}" playsinline loop muted autoplay style="width:100%;height:100%;object-fit:cover"></video></div></div>'
assert a in s
s=s.replace(a,'<div style="flex:1;min-height:0;display:flex;justify-content:center;padding:0"><div id="vbox" style="width:100%;height:100%;overflow:hidden;background:#000"><video id="evv" src="${url}" playsinline loop autoplay style="width:100%;height:100%;object-fit:contain"></video></div></div>',1)
# box(): only force an aspect ratio when a shape is chosen
a='const box=()=>{const r=VSHAPES[sh][1]||((v.videoWidth||9)/(v.videoHeight||16));$("#vbox").style.aspectRatio=String(r);'
assert a in s
s=s.replace(a,'/*wlTrimStrip3*/const box=()=>{const r=VSHAPES[sh][1]||((v.videoWidth||9)/(v.videoHeight||16));const vb=$("#vbox");if(sh){vb.style.cssText="height:100%;max-width:100%;aspect-ratio:"+r+";overflow:hidden;background:#000";v.style.objectFit="cover"}else{vb.style.cssText="width:100%;height:100%;overflow:hidden;background:#000";v.style.objectFit="contain"}',1)
# start with sound (the Edit tap is a user gesture)
a='v.currentTime=st;v.play().catch(()=>{});thumbs()};'
assert a in s
s=s.replace(a,'v.currentTime=st;v.muted=false;v.play().catch(()=>{v.muted=true;v.play().catch(()=>{})});thumbs()};',1)
open(P,"w",encoding="utf8").write(s);print("ok")
