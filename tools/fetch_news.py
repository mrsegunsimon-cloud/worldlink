"""Collect fresh headlines from public news feeds into news.json. Usage: fetch_news.py out.json
Runs in GitHub Actions (every few hours). A feed that fails is skipped; if too little comes back nothing is written."""
import sys,json,re,html,time,urllib.request,xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
UA={"User-Agent":"Mozilla/5.0 (WorldLink news fetcher)"}
def feed(url,limit=12):
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=25).read()
        root=ET.fromstring(r);out=[]
        for it in root.iter("item"):
            g=lambda t:(it.findtext(t) or "").strip()
            title=html.unescape(g("title"));link=g("link")
            d=re.sub(r"<[^>]+>","",html.unescape(g("description"))).strip()
            d=re.sub(r"\s+"," ",d)
            try:ts=parsedate_to_datetime(g("pubDate")).timestamp()
            except Exception:ts=0
            if title and link.startswith("http"):out.append((ts,title,d[:320],link))
            if len(out)>=limit:break
        return out
    except Exception as e:
        print("skip",url,e);return []
def pick(sources,tags,cap):
    rows=[]
    for name,url in sources:
        for ts,t,d,l in feed(url):rows.append((ts,tags,t,d or t,name,l))
    rows.sort(key=lambda r:-r[0]);seen=set();out=[]
    for ts,tg,t,d,n,l in rows:
        k=re.sub(r"\W+","",t.lower())[:60]
        if k in seen:continue
        seen.add(k);out.append([tg,t,d,n,l])
        if len(out)>=cap:break
    return out
world=[]
world+=pick([("BBC News","https://feeds.bbci.co.uk/news/world/rss.xml"),("Al Jazeera","https://www.aljazeera.com/xml/rss/all.xml")],"top",8)
world+=pick([("BBC News","https://feeds.bbci.co.uk/news/world/africa/rss.xml")],"africa",8)
world+=pick([("BBC News","https://feeds.bbci.co.uk/news/business/rss.xml")],"biz",8)
world+=pick([("BBC News","https://feeds.bbci.co.uk/news/health/rss.xml"),("BBC News","https://feeds.bbci.co.uk/news/technology/rss.xml")],"sci",8)
KW=[("PREMIER LEAGUE",r"premier league|arsenal|chelsea|liverpool|man(chester)? (city|united|utd)|tottenham|newcastle|aston villa"),("LA LIGA",r"la liga|real madrid|barcelona|atl[eé]tico"),("NBA",r"\bnba\b"),("NFL",r"\bnfl\b"),("MLB",r"\bmlb\b|baseball"),("UFC",r"\bufc\b|\bmma\b")]
def tag(t,d,default):
    x=(t+" "+d).lower()
    for k,p in KW:
        if re.search(p,x):return k
    return default
raw=[]
for name,url,dflt in [("BBC Sport","https://feeds.bbci.co.uk/sport/football/rss.xml","FOOTBALL"),("BBC Sport","https://feeds.bbci.co.uk/sport/rss.xml","SPORT"),("ESPN","https://www.espn.com/espn/rss/nba/news","NBA"),("ESPN","https://www.espn.com/espn/rss/nfl/news","NFL"),("ESPN","https://www.espn.com/espn/rss/mlb/news","MLB"),("ESPN","https://www.espn.com/espn/rss/soccer/news","FOOTBALL")]:
    for ts,t,d,l in feed(url,10):raw.append((ts,tag(t,d,dflt),t,d or t,name,l))
raw.sort(key=lambda r:-r[0]);seen=set();sports=[]
for ts,tg,t,d,n,l in raw:
    k=re.sub(r"\W+","",t.lower())[:60]
    if k in seen:continue
    seen.add(k);sports.append([tg,t,d,n,l])
    if len(sports)>=24:break
print("world",len(world),"sports",len(sports))
if len(world)<8 or len(sports)<6:
    print("Too little came back; keeping the previous version.");sys.exit(0)
json.dump({"updated":int(time.time()),"world":world,"sports":sports},open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False)
