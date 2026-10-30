import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlHLfix" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep('''  const n=$("#hn").value.trim(),ids=[...$("#panel").querySelectorAll("[data-v]:checked")].map(x=>x.dataset.v);
  if(n.length<2){$("#st").textContent="Give the highlight a name.";return}
  if(!ids.length){$("#st").textContent="Pick at least one video.";return}
  (me.hl=me.hl||[]).push({n,e:em,ids});await saveHL();profile();''','''  const ids=[...$("#panel").querySelectorAll("[data-v]:checked")].map(x=>x.dataset.v);
  if(!ids.length){$("#st").textContent="Pick at least one video.";$("#st").scrollIntoView({block:"center"});return}
  /*wlHLfix*/let n=$("#hn").value.trim();if(n.length<2){const c=CLIPS.find(x=>x.id===ids[0]);n=((c&&c.c)||"Highlight").trim().slice(0,14)||"Highlight"}
  (me.hl=me.hl||[]).push({n,e:em,ids});$("#hs").disabled=true;$("#hs").textContent="Saving…";await saveHL();profile();''')
# watermark jumps to a new place now and then (no sliding)
rep('line-height:1.15;opacity:.9}/*wlStory2*/','line-height:1.15;opacity:.9;animation:wlwm 18s steps(1,end) infinite}@keyframes wlwm{0%{left:14px;top:92px}16%{left:calc(100% - 215px);top:92px}33%{left:14px;top:46%}50%{left:calc(100% - 215px);top:58%}66%{left:14px;top:30%}83%{left:calc(100% - 215px);top:38%}}/*wlStory2*/')
s=s.replace('2026.10.30-H','2026.10.30-I')
open(P,"w",encoding="utf8").write(s);print("ok")
