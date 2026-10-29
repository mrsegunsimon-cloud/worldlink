import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlNotifPriv" in s: print("already");sys.exit(0)
a='const s=await D.collection("notifs").get();NF=s.docs.map(d=>d.data()).filter(n=>n&&'
assert a in s
s=s.replace(a,'/*wlNotifPriv*/let rows;if(window.WLCloud&&window.WLCloud.byField&&window.__wlUser){const [x,y]=await Promise.all([WLCloud.byField("notifs","to",id),WLCloud.byField("notifs","to","*")]);rows=x.concat(y).map(r=>r.data)}else{const s=await D.collection("notifs").get();rows=s.docs.map(d=>d.data())}NF=rows.filter(n=>n&&',1)
open(P,"w",encoding="utf8").write(s);print("ok")
