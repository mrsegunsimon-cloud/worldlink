import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlTrimStrip2" in s: print("already");sys.exit(0)
a='try{c=await fastCut(job.f,T.st,T.en,q=>bgRing(.4*q,"","Trimming"))}catch(e){c=null}'
assert a in s
s=s.replace(a,'/*wlTrimStrip2*/try{c=await Promise.race([fastCut(job.f,T.st,T.en,q=>bgRing(.4*q,"","Trimming")),new Promise((_,no)=>setTimeout(()=>no(new Error("slow")),25000))])}catch(e){c=null}',1)
open(P,"w",encoding="utf8").write(s);print("ok")
