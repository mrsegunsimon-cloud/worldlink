import sys,os
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlSeries1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"series.js"),encoding="utf8").read()
rep('<button id="t2">Community</button>','<button id="t2">Community</button><button id="t3">Series</button>')
rep('$("#t0").onclick=()=>tab(0);','$("#t3").onclick=()=>seriesOpen();$("#t0").onclick=()=>tab(0);')
rep('await loadWallet();const c=CLIPS[i];\n const draw=','await loadWallet();const c=typeof i==="object"?i:CLIPS[i];\n const draw=')
rep('function newPhotoPost(){',js+'\nfunction newPhotoPost(){')
rep('.sheet{position:fixed;','body.spo #sheet{z-index:95}\n.sheet{position:fixed;')
rep('.top{gap:4px}.tabs{gap:14px;flex:1;','.top{gap:2px}.tabs{gap:7px;font-size:13px;flex:1;')
rep('.sheet{position:fixed;','.top .ib{padding:6px 4px}.tabs button{padding:6px 0}.top{padding-left:8px;padding-right:8px}\n.sheet{position:fixed;')
rep('@media (max-width:380px){.tabs{gap:9px;font-size:14px}','@media (max-width:380px){.tabs{gap:6px;font-size:13px}')
open(P,"w",encoding="utf8").write(s);print("ok")
