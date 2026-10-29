"""Makes the website build from the app page. Usage: make_web.py assets/web/index.html assets/firebase_config.json out.html"""
import sys,json
src,cfg,dst=sys.argv[1:4]
s=open(src,encoding='utf8').read()
c=json.load(open(cfg))
fc={"apiKey":c["apiKey"],"authDomain":c["projectId"]+".firebaseapp.com","projectId":c["projectId"],"appId":c.get("webAppId") or c["appId"],"messagingSenderId":c.get("messagingSenderId","")}
shim=open(__file__.replace('make_web.py','webshim.js'),encoding='utf8').read().replace('__FIREBASE_CONFIG__',json.dumps(fc))
csp=("default-src 'none'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval' https://www.gstatic.com https://js.paystack.co https://worldlink.app; worker-src 'self' blob: https://worldlink.app;  style-src 'self' 'unsafe-inline'; "
 "img-src 'self' data: blob: https:; media-src 'self' data: blob: https:; font-src 'self' data:; "
 "connect-src https: wss:; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src https://www.youtube.com https://www.youtube-nocookie.com https://checkout.paystack.com")
head='<meta http-equiv="Content-Security-Policy" content="%s"><meta name="referrer" content="no-referrer"><script>%s</script>'%(csp,shim)
assert '<head>' in s
s=s.replace('<head>','<head>'+head,1)
# Move big embedded songs, pictures and videos out of the page so it downloads fast
import re,os,base64,hashlib
BASE=os.environ.get('WL_BASE','https://worldlink.app/')
EXT={'audio/mpeg':'mp3','image/jpeg':'jpg','video/mp4':'mp4','image/png':'png','audio/wav':'wav','image/webp':'webp'}
md=os.path.join(os.path.dirname(os.path.abspath(dst)),'m');made={}
def mv(m):
    t=m.group(1)
    if t not in EXT:return m.group(0)
    raw=base64.b64decode(m.group(2));h=hashlib.sha256(raw).hexdigest()[:20]+'.'+EXT[t]
    os.makedirs(md,exist_ok=True)
    if h not in made:open(os.path.join(md,h),'wb').write(raw);made[h]=len(raw)
    return BASE+'m/'+h
s=re.sub(r'data:([a-z]+/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]{2000,})',mv,s)
print('moved',len(made),'files',sum(made.values()),'bytes; page now',len(s))
open(dst,'w',encoding='utf8').write(s)
