"""Fresh scores, fixtures and tables from ESPN's public feeds into sports.json. Usage: fetch_sports.py out.json
A feed that fails is skipped. If nothing useful comes back, nothing is written."""
import sys,json,time,datetime,urllib.request
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36","Accept":"application/json, text/plain, */*","Accept-Language":"en-US,en;q=0.9"}
def get(url):
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=25).read())
    except Exception as e:
        print("::notice title=sports-error::%s -> %s"%(url.split("espn.com")[-1][:70],str(e)[:120]));return None
LG=[("epl","soccer/eng.1",True,4328),("la","soccer/esp.1",True,4335),("it","soccer/ita.1",True,4332),("de","soccer/ger.1",True,4331),("fr","soccer/fra.1",True,4334),("cl","soccer/uefa.champions",True,4480),
    ("nba","basketball/nba",False,4387),("nfl","football/nfl",False,4391),("mlb","baseball/mlb",False,4424),("nhl","hockey/nhl",False,4380),("mls","soccer/usa.1",False,4346),("mma","mma/ufc",False,0)]
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
    evs=[];seen=set()
    for off in range(-4,5):
        d=(today+datetime.timedelta(days=off)).strftime("%Y%m%d")
        j=get("https://site.api.espn.com/apis/site/v2/sports/%s/scoreboard?dates=%s"%(code,d))
        for ev in (j or {}).get("events",[]):
            if ev.get("id") in seen:continue
            seen.add(ev.get("id"));evs.append(ev)
        if j is None and off==-4:break
    j={"events":evs}
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

SDB="https://www.thesportsdb.com/api/v1/json/3/"
def sdb_games(lid):
    out=[]
    for ep,default in (("eventspastleague.php?id=%d"%lid,"ft"),("eventsnextleague.php?id=%d"%lid,"sch")):
        j=get(SDB+ep)
        for e in (j or {}).get("events") or []:
            try:
                h,a=e.get("strHomeTeam"),e.get("strAwayTeam")
                if not h or not a:continue
                hs,as_=e.get("intHomeScore"),e.get("intAwayScore")
                state="ft" if (default=="ft" and hs is not None) else "sch"
                ts=e.get("strTimestamp") or ((e.get("dateEvent") or "")+"T"+(e.get("strTime") or "00:00:00"))
                if ts and not ts.endswith("Z") and "+" not in ts[10:]:ts+="Z"
                out.append([h,a,int(hs or 0),int(as_ or 0),state,ts])
            except Exception:continue
    sch=sorted([g for g in out if g[4]=="sch"],key=lambda g:g[5])[:20]
    ft=sorted([g for g in out if g[4]=="ft"],key=lambda g:g[5],reverse=True)[:20]
    return sch+ft
def sdb_table(lid):
    y=today.year if today.month>=7 else today.year-1
    j=get(SDB+"lookuptable.php?l=%d&s=%d-%d"%(lid,y,y+1))
    rows=[]
    for e in (j or {}).get("table") or []:
        try:rows.append([int(e["intRank"]),e["strTeam"],int(e["intWin"]),int(e["intDraw"]),int(e["intLoss"]),int(e["intPoints"])])
        except Exception:continue
    rows.sort(key=lambda r:r[0]);return rows
res={};ng=0;SUM=[]
for key,code,tab,lid in LG:
    g=games(code);t=table(code) if tab else []
    src="espn"
    if len(g)<2 and lid:g=sdb_games(lid);src="sportsdb"
    if tab and len(t)<8 and lid:t=sdb_table(lid)
    print("%s games %d table %d (%s)"%(key,len(g),len(t),src));SUM.append("%s %d/%d"%(key,len(g),len(t)))
    ent={}
    if len(g)>=2:ent["games"]=g;ng+=1
    if len(t)>=8:ent["table"]=t
    if ent:res[key]=ent
print("::notice title=sports::"+", ".join(SUM))
if ng<4:
    print("Too little came back; keeping the previous version.");sys.exit(0)
json.dump({"updated":int(time.time()),"leagues":res},open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False)
