import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLivePause" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:60]
    s=s.replace(a,b,1)
rep('function goLive(){\n','function goLive(){\n open(`<h2>Live is paused</h2><p class="mute">Live video is switched off while we add safety checks for everyone. You can still post videos and send voice messages.</p><button class="btn ghost" id="x">Close</button>`);$("#x").onclick=close;return;/*wlLivePause*/\n')
rep('async function liveScan(){\n','async function liveScan(){\n LIVES=[];return;/*wlLivePause*/\n')
open(P,"w",encoding="utf8").write(s);print("ok")
