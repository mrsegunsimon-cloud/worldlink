import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlRtCalls" in s: print("already");sys.exit(0)
def rep(a,b,c=1):
    global s
    assert a in s,a[:60]
    s=s.replace(a,b,c)
rep('const t=setTimeout(r,2200);','const t=setTimeout(r,1500);')
# caller: tell the other phone straight away over the realtime socket
rep('await cPut(uid,{from:me.uid,fn:me.name,v:!!video,st:"ring",ts,offer:PC.localDescription.sdp});',
    '/*wlRtCalls*/rtSendTo(uid,"ring",{from:me.uid,fn:me.name,v:!!video,ts,offer:PC.localDescription.sdp});\n  cPut(uid,{from:me.uid,fn:me.name,v:!!video,st:"ring",ts,offer:PC.localDescription.sdp});')
rep('await cPut(me.uid,{from:d.from,fn:d.fn,v:!!d.v,ts:d.ts,st:"on",offer:d.offer,answer:PC.localDescription.sdp});',
    'rtSendTo(d.from,"answer",{ts:d.ts,answer:PC.localDescription.sdp});\n  cPut(me.uid,{from:d.from,fn:d.fn,v:!!d.v,ts:d.ts,st:"on",offer:d.offer,answer:PC.localDescription.sdp});')
# hanging up or declining
rep('if(D0&&why!=="remote"){cPut(D0.id,','if(D0&&why!=="remote"){rtSendTo(D0.from===me.uid?D0.id:D0.from,"end",{ts:D0.ts});cPut(D0.id,')
rep('else if(!D0&&why==="declined"){const d=$("#call").__d;if(d)cPut(','else if(!D0&&why==="declined"){const d=$("#call").__d;if(d)rtSendTo(d.from,"end",{ts:d.ts});if(d)cPut(')
# helpers and the listener
rep('const cGet=async id=>',r'''const rtSendTo=(uid,ev,p)=>{try{if(window.WLCloud&&WLCloud.rt&&uid)WLCloud.rt.send("wlc-"+uid,ev,p)}catch(e){}};
let RTL=false;
setInterval(()=>{if(RTL||!me.uid||!window.__wlUser||!window.WLCloud||!WLCloud.rt)return;RTL=true;
 WLCloud.rt.on((topic,ev,p)=>{if(topic!=="wlc-"+me.uid||!p)return;
  if(ev==="ring"){if(!PC&&!RING&&p.ts!==LASTRING&&Date.now()-p.ts<40000){LASTRING=p.ts;showIncoming(p)}}
  else if(ev==="answer"){if(PC&&CDOC&&p.ts===CDOC.ts&&!PC.remoteDescription&&p.answer){clearTimeout(CTMO);PC.setRemoteDescription({type:"answer",sdp:p.answer}).then(()=>cSay("Connecting…")).catch(()=>cSay("Could not connect"))}}
  else if(ev==="end"){if(PC&&CDOC&&p.ts===CDOC.ts){cSay(PC.remoteDescription?"Call ended":"Declined");setTimeout(()=>endCall("remote"),900)}else if(RING&&LASTRING===p.ts){clearInterval(RING);RING=null;window.CALLON=false;$("#call").classList.remove("on");setTimeout(wlResume,150)}}
 });
 WLCloud.rt.listen("wlc-"+me.uid)},1500);
const cGet=async id=>''')
open(P,"w",encoding="utf8").write(s);print("ok")
