import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLive2" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# host sees why people can or cannot find the live
rep('async function livePut(on){try{const D=await claude.use("db");if(D&&me.uid&&LIVEH)await D.collection("calls").doc("live-"+me.uid).set({uid:me.uid,name:me.name,title:LIVEH.title,aud:LIVEH.aud,ts:Date.now(),st:on?"on":"off"})}catch(e){}}',
    '/*wlLive2*/async function livePut(on){try{const D=await claude.use("db");if(!D||!me.uid||!LIVEH)throw new Error("no account");await D.collection("calls").doc("live-"+me.uid).set({uid:me.uid,name:me.name,title:LIVEH.title,aud:LIVEH.aud,ts:Date.now(),st:on?"on":"off"});if(on)liveStatus("✅ You are live. Your followers have been told and a LIVE chip shows on Home.")}catch(e){if(on)liveStatus("⚠️ People cannot see your live yet ("+(e.message||"error")+"). Check your internet and make sure you are signed in.")}}\nfunction liveStatus(t){const s=$("#st");if(s)s.textContent=t}')
rep(' if(!me.uid||!lrt()||!window.__wlUser)return;liveInit();\n LIVEH=',
    ' if(!me.uid||!lrt()||!window.__wlUser){liveStatus("⚠️ Nobody can see this live. "+(!me.uid||!window.__wlUser?"Sign in first, then start again.":"Update the app: close it fully and open worldlink.app again."));return}liveInit();\n LIVEH=')
rep('const st=$("#st");if(st)st.textContent="";\n livePut(true);','livePut(true);')
# faster discovery and a LIVE section on the Activity page
rep('setInterval(liveScan,15000);setTimeout(liveScan,4000);','setInterval(liveScan,8000);setTimeout(liveScan,2500);')
rep('   if(pri.length)body+=','   if(LIVES.length)body+=`<div style="padding:14px 16px 6px;font-size:17px;font-weight:700">Live now</div>`+LIVES.map(l=>`<div data-lv2="${esc(l.uid)}" role="button" style="display:flex;align-items:center;gap:12px;padding:10px 16px;cursor:pointer"><span style="background:#E5233A;color:#fff;border-radius:999px;padding:4px 10px;font-weight:800;font-size:12px">LIVE</span><b style="flex:1">${esc(l.name)}</b><span class="mute" style="font-size:14px">${esc(l.title||"")}</span></div>`).join("");\n   if(pri.length)body+=')
rep(' P.querySelectorAll("[data-at]")',' P.querySelectorAll("[data-lv2]").forEach(el=>el.onclick=()=>{const l=LIVES.find(x=>x.uid===el.dataset.lv2);if(l)watchLive({uid:l.uid,name:l.name,title:l.title})});\n P.querySelectorAll("[data-at]")')
rep('async function notifs(tab){','async function notifs(tab){try{await liveScan()}catch(e){}')
open(P,"w",encoding="utf8").write(s);print("ok")
