import subprocess,os,json
from PIL import Image,ImageDraw,ImageFont
W,H=720,1280;OUT="assets/starter";TMP="/tmp/ln_frames";os.makedirs(TMP,exist_ok=True)
F="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def font(s):return ImageFont.truetype(F,s)
MUS=["daybreak","home","wild_waters","find_you","fate","remember"]
MN={"daybreak":"Daybreak","home":"Home","wild_waters":"Wild Waters","find_you":"Find You","fate":"Fate","remember":"Remember"}
PAL=[("#0f766e","#1d4ed8"),("#7c3aed","#db2777"),("#0369a1","#0d9488"),("#b45309","#be123c"),("#4338ca","#0891b2"),("#be185d","#6d28d9"),("#15803d","#0e7490"),("#9a3412","#a21caf")]
LANG=[("Yoruba","E ku aaro","Good morning"),("Swahili","Habari yako","How are you"),("Hausa","Sannu","Hello"),("French","Bonjour","Hello"),("Spanish","Buenos dias","Good morning"),("Portuguese","Obrigado","Thank you"),("Japanese","Konnichiwa","Hello"),("Hindi","Namaste","Greetings")]
TIPS=[("Study tip 1","Study 25 minutes","Rest 5 minutes","Repeat 4 times"),("Study tip 2","Put your phone","in another room","Focus doubles"),("Study tip 3","Teach what you learn","to a friend","You remember more"),("Study tip 4","Sleep 7-8 hours","Your brain saves","what you studied"),("Study tip 5","Write 3 questions","after every lesson","Test yourself"),("Study tip 6","Drink water","Short walk","Fresh mind"),("Study tip 7","Start with the","hardest subject","while you are fresh"),("Study tip 8","Plan tomorrow","tonight in 5 minutes","Less stress")]
FACT=[("World fact 1","Africa has","54 countries","More than any continent"),("World fact 2","Brazil has","the Amazon forest","Over 20% of Earth's oxygen cycle"),("World fact 3","Japan has","over 6,800 islands","Only 14 are big"),("World fact 4","Nigeria is","Africa's most populous","over 200 million people"),("World fact 5","The Pacific Ocean","is bigger than","all land combined"),("World fact 6","Iceland has","no mosquitoes","and lots of volcanoes"),("World fact 7","Canada has","the longest coastline","on Earth"),("World fact 8","India has","over 20 official","languages")]
items=[]
for i,(l,p,m) in enumerate(LANG):items.append((f"lang{i}",f"Say hello in {l}",["Learn a word",f"in {l}:",p,f"means: {m}"],f"{l}: {p} = {m}"))
for i,t in enumerate(TIPS):items.append((f"tip{i}",t[0],[t[0],t[1],t[2],t[3]],t[0]+": "+t[1]+" "+t[2]+", "+t[3]))
for i,t in enumerate(FACT):items.append((f"fact{i}",t[0],[t[0],t[1],t[2],t[3]],t[0]+": "+t[1]+" "+t[2]+", "+t[3]))
def hx(c):return tuple(int(c[i:i+2],16) for i in (1,3,5))
def grad(a,b):
    im=Image.new("RGB",(W,H));d=ImageDraw.Draw(im);A,B=hx(a),hx(b)
    for y in range(H):
        t=y/H;d.line([(0,y),(W,y)],fill=tuple(int(A[i]*(1-t)+B[i]*t) for i in range(3)))
    return im
def wrap(d,t,f,mw):
    o=[];l=""
    for x in t.split():
        if d.textlength((l+" "+x).strip(),font=f)>mw and l:o.append(l);l=x
        else:l=(l+" "+x).strip()
    return o+[l]
man=[]
for n,(k,title,lines,cap) in enumerate(items):
    c1,c2=PAL[n%len(PAL)];mus=MUS[n%len(MUS)];bg=grad(c1,c2);segs=[]
    for i in range(len(lines)):
        im=bg.copy();d=ImageDraw.Draw(im)
        f0=font(28);tx="WorldLink Learn · made by WorldLink"
        d.rounded_rectangle([40,60,40+d.textlength(tx,font=f0)+40,118],20,fill=(255,255,255));d.text((60,68),tx,font=f0,fill=hx(c1))
        y=380
        for j in range(i+1):
            f=font(60 if j!=len(lines)-1 or i<len(lines)-1 else 60)
            if j==2 and k.startswith("lang"):f=font(84)
            for ln in wrap(d,lines[j],f,W-100):d.text((50,y),ln,font=f,fill=(255,255,255));y+=int(f.size*1.3)
            y+=24
        d.text((50,H-150),f"Music: {MN[mus]} - Tanner Helland (CC BY 4.0)",font=font(22),fill=(255,255,255))
        d.text((50,H-105),"Made by WorldLink with templates, not a real person",font=font(22),fill=(255,255,255))
        p=f"{TMP}/{k}{i}.png";im.save(p);segs.append(p)
    lst=f"{TMP}/{k}.txt";per=2.3
    with open(lst,"w") as fh:
        for p in segs:fh.write(f"file '{p}'\nduration {per}\n")
        fh.write(f"file '{segs[-1]}'\n")
    dur=per*len(lines)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-i",f"tools/music/{mus}.mp3","-t",str(dur),"-vf","fps=25,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","29","-c:a","aac","-b:a","80k","-af",f"afade=t=out:st={dur-1}:d=1","-movflags","+faststart",f"{OUT}/{k}.mp4"],check=True)
    man.append([k,cap])
json.dump(man,open("assets/learn.json","w"),ensure_ascii=False)
print(len(man),sum(os.path.getsize(f"{OUT}/{k}.mp4") for k,_ in man))
