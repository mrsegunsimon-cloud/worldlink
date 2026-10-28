"""Fresh scores, fixtures and tables from ESPN's public feeds into sports.json. Usage: fetch_sports.py out.json
A feed that fails is skipped. If nothing useful comes back, nothing is written."""
import sys,json,time,datetime,urllib.request
UA={"User-Agent":"Mozilla/5.0 (WorldLink sports fetcher)"}
def get(url):
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=25).read())
    except Exception as e:
        print("skip",url,e);return None
LG=[("epl","soccer/eng.1",True),("la","soccer/esp.1",True),("it","soccer/ita.1",True),("de","soccer/ger.1",True),("fr","soccer/fra.1",True),("cl","soccer/uefa.champions",True),
    ("nba","basketball/nba",False),("nfl","football/nfl",False),("mlb","baseball/mlb",False),("nhl","hockey/nhl",False),("mls","soccer/usa.1",False),("mma","mma/ufc",False)]
today=datetime.datetime.utcnow().date()
d1=(today-datetime.timedelta(days=7)).strftime("%Y%m%d");d2=(today+datetime.timedelta(days=7)).strftime("%Y%m%d")
STATE={"pre":"sch","in":"live","post":"ft"}
def name(c):
    t=c.get("team") or c.get("athlete") or {}
    return t.get("displayName") or t.get("shortDisplayName") or t.get("fullName") or ""
def score(c):
    try:return int(float(c.get("score")))
    except Exception:return 0
def games(code):
    j=get("https://site.api.espn.com/apis/site/v2/sports/%s/scoreboard?dates=%s-%s&limit=300"%(code,d1,d2))
    out=[]
    for ev in (j or {}).get("events",[]):
        for comp in ev.get("competitions",[]) or []:
            cs=comp.get("competitors") or []
            if len(cs)<2:continue
            home=next((c for c in cs if c.get("homeAway")=="home"),cs[0]);away=next((c for c in cs if c.get("homeAway")=="away"),cs[1])
            st=(comp.get("status") or ev.get("status") or {}).get("type") or {}
            state=STATE.get(st.get("state"),"")
            if not state or not name(home) or not name(away):continue
            row=[name(home),name(away),score(home),score(away),state,comp.get("date") or ev.get("date") or ""]
            if code.startswith("mma"):row.append((ev.get("shortName") or ev.get("name") or "")[:60]);row[2]=row[3]=0
            out.append(row)
    sch=sorted([g for g in out if g[4]=="sch"],key=lambda g:g[5])[:20]
    live=[g for g in out if g[4]=="live"]
    ft=sorted([g for g in out if g[4]=="ft"],key=lambda g:g[5],reverse=True)[:20]
    return live+sch+ft
def table(code):
    j=get("https://site.api.espn.com/apis/v2/sports/%s/standings"%code)
    rows=[]
    try:
        ch=(j or {}).get("children") or []
        ent=ch[0]["standings"]["entries"] if ch else (j or {}).get("standings",{}).get("entries",[])
        for e in ent:
            st={s.get("name"):s.get("value") for s in e.get("stats",[])}
            rows.append([int(st.get("rank") or 0),e["team"]["displayName"],int(st.get("wins") or 0),int(st.get("ties") or 0),int(st.get("losses") or 0),int(st.get("points") or 0)])
    except Exception as ex:
        print("table parse",code,ex);return []
    rows.sort(key=lambda r:r[0] or 99)
    return rows
res={};ng=0
for key,code,tab in LG:
    g=games(code);t=table(code) if tab else []
    print("::notice title=sports::%s games %d table %d"%(key,len(g),len(t)))
    ent={}
    if len(g)>=2:ent["games"]=g;ng+=1
    if len(t)>=8:ent["table"]=t
    if ent:res[key]=ent
if ng<4:
    print("Too little came back; keeping the previous version.");sys.exit(0)
json.dump({"updated":int(time.time()),"leagues":res},open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False)
