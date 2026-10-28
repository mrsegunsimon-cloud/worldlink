"""Latest official music videos per artist from their YouTube channels (free channel feeds). Usage: fetch_music.py out.json"""
import sys,json,re,time,html,urllib.request,xml.etree.ElementTree as ET
WHY=[]
from concurrent.futures import ThreadPoolExecutor
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","Accept-Language":"en-US,en;q=0.9","Cookie":"SOCS=CAI; CONSENT=YES+cb"}
ARTISTS=[("Burna Boy","burnaboy"),("Wizkid","wizkidofficial"),("Davido","davido"),("Rema","rema"),("Asake","asakemusic"),("Tems","temsbaby"),("Ayra Starr","ayrastarr"),("Tiwa Savage","tiwasavage"),("Olamide","olamide"),("Fireboy DML","fireboydml"),("Omah Lay","omahlay"),("Kizz Daniel","kizzdaniel"),("Joeboy","joeboyofficial"),("CKay","ckay_yo"),("Mr Eazi","mreazi"),
 ("Taylor Swift","taylorswift"),("Beyoncé","beyonce"),("Drake","drake"),("Ed Sheeran","edsheeran"),("Rihanna","rihanna"),("The Weeknd","theweeknd"),("Bruno Mars","brunomars"),("Coldplay","coldplay"),("Adele","adele"),("Dua Lipa","dualipa"),("Billie Eilish","billieeilish"),("Shakira","shakira"),("BLACKPINK","BLACKPINK"),("Bad Bunny","badbunny"),("Kendrick Lamar","kendricklamar"),("Ariana Grande","arianagrande")]
def get(u,n=600000):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=20).read(n).decode("utf8","ignore")
def one(a):
    name,handle=a
    try:
        h=get("https://www.youtube.com/@"+handle)
        m=re.search(r'"channelId":"(UC[\w-]{22})"',h) or re.search(r'channel/(UC[\w-]{22})',h)
        if not m:WHY.append(name+": no channel id in page ("+str(len(h))+" bytes)");return None
        root=ET.fromstring(get("https://www.youtube.com/feeds/videos.xml?channel_id="+m.group(1),400000))
        v=[]
        for e in root.iter("{http://www.w3.org/2005/Atom}entry"):
            vid=e.findtext("{http://www.youtube.com/xml/schemas/2015}videoId") or ""
            t=html.unescape(e.findtext("{http://www.w3.org/2005/Atom}title") or "")
            if re.fullmatch(r"[\w-]{11}",vid) and "#shorts" not in t.lower():v.append([vid,t[:90]])
            if len(v)>=8:break
        return {"n":name,"v":v} if v else None
    except Exception as ex:
        WHY.append(name+": "+str(ex)[:60]);return None
with ThreadPoolExecutor(8) as ex:res=[r for r in ex.map(one,ARTISTS) if r]
print("::notice title=music::%d artists, %d videos. %s"%(len(res),sum(len(r["v"]) for r in res)," | ".join(WHY[:4])))
if len(res)<6:
    print("Too little came back; keeping the previous version.");sys.exit(0)
json.dump({"updated":int(time.time()),"artists":res},open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False)
