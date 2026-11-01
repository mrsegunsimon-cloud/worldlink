import sys,os
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlSeries3" in s: print("already");sys.exit(0)
js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"series.js"),encoding="utf8").read()
i=s.index("/*wlSeries1*/");j=s.index("\nfunction newPhotoPost(){")
s=s[:i]+js+s[j:]
open(P,"w",encoding="utf8").write(s);print("ok")
