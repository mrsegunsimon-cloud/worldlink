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
    q='[out:json][timeout:120];area["ISO3166-1"="%s"][admin_level=2]->.a;nwr["natural"="beach"]["name"](area.a);out center 400;'%cc
    for h in HOSTS:
        try:
            r=urllib.request.urlopen(urllib.request.Request(h+"?data="+urllib.parse.quote(q),headers=UA),timeout=150).read()
            return json.loads(r).get("elements",[])
        except Exception as e:
            print("::notice title=beaches-error::%s %s %s"%(cc,h.split("//")[1][:14],str(e)[:60]));time.sleep(5)
    return None
ok=0
for cc in codes:
    el=query(cc)
    if el is None:continue
    seen=set();rows=[]
    for e in el:
        la=e.get("lat",(e.get("center") or {}).get("lat"));lo=e.get("lon",(e.get("center") or {}).get("lon"))
        t=e.get("tags") or {};n=t.get("name")
        if la is None or lo is None or not n:continue
        k="%s|%.2f|%.2f"%(n,la,lo)
        if k in seen:continue
        seen.add(k)
        area=t.get("addr:city") or t.get("addr:state") or t.get("is_in:state") or t.get("is_in") or ""
        tags={k2:str(t[k2])[:200] for k2 in KEEP if t.get(k2)}
        rows.append([n[:80],round(la,5),round(lo,5),str(area)[:60],tags])
    if rows:out[cc]=rows;ok+=1
    time.sleep(3)
print("::notice title=beaches::%d of %d countries updated, %d beaches in file"%(ok,len(codes),sum(len(v) for v in out.values())))
if ok:json.dump(out,open(sys.argv[1],"w",encoding="utf8"),ensure_ascii=False,separators=(",",":"))
