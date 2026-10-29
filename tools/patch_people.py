import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'loadProfs' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]
    s=s.replace(a,b)
rep('function searchAll(){','let PROF=[];async function loadProfs(){try{const D=await claude.use("db");if(!D)return;const s=await D.collection("profiles").get();PROF=s.docs.map(d=>Object.assign({uid:d.id},d.data())).filter(x=>x&&x.name)}catch(e){}}\nfunction searchAll(){\n loadProfs().then(()=>{const q=$("#sq");if(q&&q.value.trim().length>1)renderSR(q.value.trim())});')
rep(' const q=raw.toLowerCase(),box=$("#sr");',' raw=raw.replace(/^@+/,"");const q=raw.toLowerCase(),box=$("#sr");')
rep(' PEOPLE.forEach(p=>addP(p[0],null));',' PEOPLE.forEach(p=>addP(p[0],null));PROF.forEach(x=>addP(x.name,x.uid));')
open(p,'w',encoding='utf8').write(s);print('patched')
