import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlPush" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
VP="BMGhFI0Jh4o69Cesc3iH5iUIDkxkovHKZ1dFXhDn-NYm61_TKSWg65tvku8OAY6j7klZhDJnQHOPZ_ewI4g9HdM"
NEW=r'''/* wlPush: phone alerts when the app is closed (website, Chrome) */
const VAPID_PUB="__VP__";
const b64u=t=>{const p="=".repeat((4-t.length%4)%4),b=(t+p).replace(/-/g,"+").replace(/_/g,"/"),r=atob(b),o=new Uint8Array(r.length);for(let i=0;i<r.length;i++)o[i]=r.charCodeAt(i);return o};
const pushOK=()=>!!(window.WLCloud&&WLCloud.fn&&"serviceWorker"in navigator&&"PushManager"in window&&"Notification"in window&&window.__wlUser);
async function pushSub(ask){
 try{
  if(!pushOK())return"unsupported";
  if(Notification.permission==="denied")return"denied";
  if(Notification.permission!=="granted"){if(!ask)return"off";const r=await Notification.requestPermission();if(r!=="granted")return"denied"}
  const reg=await navigator.serviceWorker.ready;
  let sub=await reg.pushManager.getSubscription();
  if(!sub)sub=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:b64u(VAPID_PUB)});
  const r=await WLCloud.fn("push-alerts",{a:"sub",sub:sub.toJSON()});
  if(r&&r.ok)return"on";window.__pushWhy="server said "+(r?(r._s+" "+(r.why||"")):"nothing");return"error"
 }catch(e){window.__pushWhy=(e&&e.name||"error")+": "+(e&&e.message||"");return"error"}
}
function pushTo(uid,title,body,tag){try{if(uid&&window.WLCloud&&WLCloud.fn&&window.__wlUser)WLCloud.fn("push-alerts",{a:"send",to:uid,t:title,b:body,tag:tag||"wl"}).catch(()=>{})}catch(e){}}
setInterval(()=>{if(!window.__wlPS&&pushOK()&&Notification.permission==="granted"){window.__wlPS=1;pushSub(false).then(r=>{window.__pushState=r})}},4000);
'''.replace("__VP__",VP)
rep('let RTL=false;',NEW+'let RTL=false;')
rep('await D.collection("notifs").doc(id).set({id,to,from:me.name,text,ts:Date.now()})}catch(e){}}','await D.collection("notifs").doc(id).set({id,to,from:me.name,text,ts:Date.now()});pushTo(to,"@"+me.name,text,"n")}catch(e){}}')
rep('/*wlRtCalls*/rtSendTo(uid,"ring",','/*wlRtCalls*/pushTo(uid,"📞 "+me.name,video?"Incoming video call":"Incoming voice call","call");rtSendTo(uid,"ring",')
rep(' let body="";\n if(ACT_TAB===1)',' let body=window.__pushState==="on"||!pushOK()||Notification.permission==="denied"?"":`<button id="actpush" style="display:block;width:calc(100% - 32px);margin:10px 16px 0;padding:13px;border-radius:12px;background:#FE2C55;color:#fff;font-weight:800;font-size:15px">🔔 Turn on phone alerts</button><p class="mute" style="margin:6px 16px 0;font-size:13px">Get calls, messages and lives on your phone even when WorldLink is closed.</p>`;\n if(ACT_TAB===1)')
rep(' P.querySelectorAll("[data-lv2]")',' const ap=$("#actpush");if(ap)ap.onclick=async()=>{ap.textContent="Turning on…";const r=await pushSub(true);window.__pushState=r;if(r==="on"){ap.textContent="✅ Phone alerts are on"}else if(r==="denied"){ap.textContent="Blocked. Allow notifications for worldlink.app in Chrome settings."}else{ap.textContent="Could not turn on ("+(window.__pushWhy||"unknown")+")"}};\n P.querySelectorAll("[data-lv2]")')
open(P,"w",encoding="utf8").write(s);print("ok")
