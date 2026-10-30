import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlSize" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
i=s.index("function captionVideo(f,css,cap,prog){")
j=s.index("videoBitsPerSecond:1500000,audioBitsPerSecond:128000",i)
old="mt?{mimeType:mt,videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{}"
k=s.rindex("new MediaRecorder(out,",i,j)
seg_start=k
seg_end=j+len("videoBitsPerSecond:1500000,audioBitsPerSecond:128000}:{}")
seg=s[seg_start:seg_end]
new=seg.replace("videoBitsPerSecond:1500000,audioBitsPerSecond:128000","videoBitsPerSecond:/*wlSize*/(isFinite(v.duration)&&v.duration>0?Math.max(250000,Math.min(1500000,Math.floor(16*1048576*8/v.duration)-100000)):1500000),audioBitsPerSecond:96000")
s=s[:seg_start]+new+s[seg_end:]
rep("job.burned=nf;await jPut(job)}","if(!(job.css||job.tx)&&job.f&&job.f.size<=20*1048576&&nf.size>job.f.size)nf=job.f;job.burned=nf;await jPut(job)}")
s=s.replace('2026.10.30-N','2026.10.30-O')
open(P,"w",encoding="utf8").write(s);print("ok")
