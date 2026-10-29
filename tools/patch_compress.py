import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlCompress" in s: print("already");sys.exit(0)
a='const burn=!!(job.css||job.tx);'
assert a in s
s=s.replace(a,'const burn=!!(job.css||job.tx||(job.f&&job.f.size>4*1048576&&window.MediaRecorder));/*wlCompress: big videos are shrunk to 960px so they play fast for everyone*/',1)
a='bgRing(0,"","Adding your edits");nf=await captionVideo(job.f,job.css,job.tx,(t,d)=>bgRing(d?.45*t/d:0,"","Adding your edits"))'
assert a in s
s=s.replace(a,'bgRing(0,"","Preparing video");try{nf=await captionVideo(job.f,job.css,job.tx,(t,d)=>bgRing(d?.45*t/d:0,"","Preparing video"))}catch(e){if(job.css||job.tx)throw e;nf=job.f}',1)
open(P,"w",encoding="utf8").write(s);print("ok")
