"""Beaches per country from OpenStreetMap (Overpass) into assets/beaches.json. Usage: fetch_beaches.py out.json
Keeps what is already in the file; a country that fails keeps its old list."""
import sys,json,re,os,time,urllib.request,urllib.parse
HOSTS=["https://overpass-api.de/api/interpreter","https://overpass.kumi.systems/api/interpreter","https://overpass.private.coffee/api/interpreter"]
UA={"User-Agent":"WorldLink beach list (mrsegunsimon@gmail.com)"}
KEEP=["description","access","fee","surface","lifeguard","toilets","opening_hours","website","contact:website","phone","contact:phone"]
near=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"near.js"),encoding="utf8").read()
codes=re.findall(r'\["([A-Z]{2})","',re.search(r"const BCO=\[(.*?)\];",near,re.S).group(1))
out=json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
def query(cc):
    q='''SELECT ?bLabel ?bDescription ?coord ?sl WHERE { ?b wdt:P31 wd:Q40080; wdt:P17 ?c; wdt:P625 ?coord; wikibase:sitelinks ?sl. ?c wdt:P297 "%s". SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } ORDER BY DESC(?sl) LIMIT 300'''%cc
    u="https://query.wikidata.org/sparql?format=json&query="+urllib.parse.quote(q)
    for k in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA["User-Agent"],"Accept":"application/sparql-results+json"}),timeout=70).read()
            return json.loads(r)["results"]["bindings"]
        except Exception as e:
            print("::notice title=beaches-error::%s try %d %s"%(cc,k+1,str(e)[:70]));time.sleep(6)
    return None
ok=0;T0=time.time()
for cc in codes:
    if time.time()-T0>75*60:
        print("::notice title=beaches-stop::time limit reached before "+cc);break
    el=query(cc)
    if el is None:continue
    seen=set();rows=[]
    for e in el:
        try:
            n=e["bLabel"]["value"]
            if re.fullmatch(r"Q\d+",n):continue
            m=re.match(r"Point\(([-\d.eE]+) ([-\d.eE]+)\)",e["coord"]["value"])
            if not m:continue
            lo,la=float(m.group(1)),float(m.group(2))
            k="%s|%.2f|%.2f"%(n,la,lo)
            if k in seen:continue
            seen.add(k)
            d=(e.get("bDescription") or {}).get("value","")
            rows.append([n[:80],round(la,5),round(lo,5),"",({"description":d[:200]} if d else {})])
        except Exception:continue
    if rows:
        out[cc]=rows;ok+=1
        json.dump(out,open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False,separators=(",",":"))
    time.sleep(2)
print("::notice title=beaches::%d of %d countries updated, %d beaches in file"%(ok,len(codes),sum(len(v) for v in out.values())))
if ok:json.dump(out,open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False,separators=(",",":"))
