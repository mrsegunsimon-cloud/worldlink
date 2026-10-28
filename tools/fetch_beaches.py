"""Beaches per country from OpenStreetMap (Overpass) into assets/beaches.json. Usage: fetch_beaches.py out.json
Keeps what is already in the file; a country that fails keeps its old list."""
import sys,json,re,os,time,urllib.request,urllib.parse
HOSTS=["https://overpass-api.de/api/interpreter","https://overpass.kumi.systems/api/interpreter","https://overpass.private.coffee/api/interpreter"]
UA={"User-Agent":"WorldLink beach list (mrsegunsimon@gmail.com)"}
KEEP=["description","access","fee","surface","lifeguard","toilets","opening_hours","website","contact:website","phone","contact:phone"]
near=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"near.js"),encoding="utf8").read()
codes=re.findall(r'\["([A-Z]{2})","',re.search(r"const BCO=\[(.*?)\];",near,re.S).group(1))
out=json.load(open(sys.argv[1])) if os.path.exists(sys.argv[1]) else {}
BOX={"US":[(24.4,-87.7,31,-79.9),(31,-82,45,-66),(25.5,-97.5,31,-87.7),(32.5,-124.6,42,-117),(42,-125,49,-122),(18.8,-160.5,22.4,-154.7)],
"FR":[(41.3,-2,43.5,3.3),(43.0,3.0,43.9,7.8),(43.3,-2.2,46.5,-0.8),(46.4,-4.9,48.9,-1.0),(48.4,-5.2,51.1,2.6),(41.3,8.5,43.1,9.6),(48.8,-2.5,49.8,1.5)],"CN":[(21.5,108,41,122.5),(18,108.5,20.2,111.2)],"MV":[(-0.8,72.6,7.2,73.8)],
"CM":[(2,8.3,5,10)],"GA":[(-4,8.6,0.5,11.5)],"BJ":[(6.1,1.4,6.6,2.8)]}
def qbox(cc):
    res=[]
    for (s_,w,n,e) in BOX[cc]:
        q='''SELECT ?bLabel ?bDescription ?coord ?sl WHERE { SERVICE wikibase:box { ?b wdt:P625 ?coord. bd:serviceParam wikibase:cornerSouthWest "Point(%s %s)"^^geo:wktLiteral. bd:serviceParam wikibase:cornerNorthEast "Point(%s %s)"^^geo:wktLiteral. } ?b wdt:P31 wd:Q40080; wikibase:sitelinks ?sl. SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } } LIMIT 300'''%(w,s_,e,n)
        u="https://query.wikidata.org/sparql?format=json&query="+urllib.parse.quote(q)
        for k in range(3):
            try:
                r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA["User-Agent"],"Accept":"application/sparql-results+json"}),timeout=70).read()
                res+=json.loads(r)["results"]["bindings"];break
            except Exception as ex:
                print("::notice title=beaches-error::%s box try %d %s"%(cc,k+1,str(ex)[:70]));time.sleep(6)
        time.sleep(2)
    if not res:return None
    res.sort(key=lambda x:-int(x["sl"]["value"]))
    if cc=="CN":res=[x for x in res if not re.search(r"Point\(12[0-2][.\d]* 2[2-5]",x["coord"]["value"])]
    return res[:300]
def query(cc):
    if cc in BOX:return qbox(cc)
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
