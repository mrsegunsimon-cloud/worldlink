import subprocess,os,sys
from PIL import Image,ImageDraw,ImageFont
W,H=720,1280
OUT="assets/starter"; TMP="/tmp/st_frames"; os.makedirs(TMP,exist_ok=True)
def font(sz,b=True):
    for p in ["/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf","/usr/share/fonts/truetype/poppins/Poppins-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):return ImageFont.truetype(p,sz)
    return ImageFont.load_default()
VIDS=[
 ("welcome","Welcome to WorldLink","Share your day with the world","Music: Home - Tanner Helland (CC BY 4.0)","home",("#0f766e","#1d4ed8"),["Welcome to WorldLink","Share videos, photos","and daily life","with people everywhere","Official WorldLink Team"]),
 ("howpost","How to post a video","Tap + , record or pick a clip","Music: Daybreak - Tanner Helland (CC BY 4.0)","daybreak",("#7c3aed","#db2777"),["How to post","1. Tap the + button","2. Record or choose a clip","3. Add a caption","4. Tap Post - done!"]),
 ("explore","Explore the world","News, sports, music, beaches","Music: Wild Waters - Tanner Helland (CC BY 4.0)","wild_waters",("#0369a1","#0d9488"),["Explore","Live world news","Sports scores","Music and beaches","All in one app"]),
 ("safe","Your videos are yours","Delete any time from Profile","Music: Remember - Tanner Helland (CC BY 4.0)","remember",("#b45309","#be123c"),["You are in control","Open Profile","Tap your video","Tap Delete","Gone from WorldLink"]),
 ("invite","Invite your friends","Be one of the first creators","Music: Find You - Tanner Helland (CC BY 4.0)","find_you",("#4338ca","#0891b2"),["Be an early creator","Post your first video","Invite 3 friends","Earn free coins","Thank you!"]),
 ("music","Music on WorldLink","Free songs and music videos","Music: Fate - Tanner Helland (CC BY 4.0)","fate",("#be185d","#6d28d9"),["Open Discover","Free full songs","Music videos","30-second previews","Add them to your video"]),
]
def hx(c):return tuple(int(c[i:i+2],16) for i in (1,3,5))
def grad(a,b):
    im=Image.new("RGB",(W,H));d=ImageDraw.Draw(im);A,B=hx(a),hx(b)
    for y in range(H):
        t=y/H;d.line([(0,y),(W,y)],fill=tuple(int(A[i]*(1-t)+B[i]*t) for i in range(3)))
    return im
def wrap(d,t,f,mw):
    w=t.split();l="";o=[]
    for x in w:
        if d.textlength((l+" "+x).strip(),font=f)>mw and l:o.append(l);l=x
        else:l=(l+" "+x).strip()
    return o+[l]
for k,title,sub,cred,mus,(c1,c2),lines in VIDS:
    bg=grad(c1,c2);segs=[]
    n=len(lines)
    for i in range(n):
        im=bg.copy();d=ImageDraw.Draw(im)
        # badge
        f0=font(30);d.rounded_rectangle([40,60,40+d.textlength("OFFICIAL · WorldLink Team",font=f0)+40,120],20,fill=(255,255,255))
        d.text((60,68),"OFFICIAL · WorldLink Team",font=f0,fill=hx(c1))
        # progress lines shown cumulatively
        y=330
        for j in range(i+1):
            f=font(74 if j==0 else 54)
            for ln in wrap(d,lines[j],f,W-100):
                d.text((50,y),ln,font=f,fill=(255,255,255));y+=int(f.size*1.3)
            y+=20
        d.text((50,H-170),cred,font=font(24),fill=(255,255,255))
        d.text((50,H-120),"Made by the WorldLink Team, not AI-faked people",font=font(22),fill=(255,255,255))
        p=f"{TMP}/{k}{i}.png";im.save(p);segs.append(p)
    per=2.4;lst=f"{TMP}/{k}.txt"
    with open(lst,"w") as fh:
        for p in segs:fh.write(f"file '{p}'\nduration {per}\n")
        fh.write(f"file '{segs[-1]}'\n")
    dur=per*n
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-i",f"tools/music/{mus}.mp3","-t",str(dur),"-vf","fps=25,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","28","-c:a","aac","-b:a","96k","-af",f"afade=t=out:st={dur-1}:d=1","-movflags","+faststart",f"{OUT}/{k}.mp4"],check=True)
    print(k,os.path.getsize(f"{OUT}/{k}.mp4"))
