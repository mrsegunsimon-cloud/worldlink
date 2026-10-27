"""Makes the website build from the app page. Usage: make_web.py assets/web/index.html assets/firebase_config.json out.html"""
import sys,json
src,cfg,dst=sys.argv[1:4]
s=open(src,encoding='utf8').read()
c=json.load(open(cfg))
fc={"apiKey":c["apiKey"],"authDomain":c["projectId"]+".firebaseapp.com","projectId":c["projectId"],"appId":c.get("webAppId") or c["appId"],"messagingSenderId":c.get("messagingSenderId","")}
shim=open(__file__.replace('make_web.py','webshim.js'),encoding='utf8').read().replace('__FIREBASE_CONFIG__',json.dumps(fc))
csp=("default-src 'none'; script-src 'self' 'unsafe-inline' https://www.gstatic.com; style-src 'self' 'unsafe-inline'; "
 "img-src 'self' data: blob: https:; media-src 'self' data: blob: https:; font-src 'self' data:; "
 "connect-src https:; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'none'")
head='<meta http-equiv="Content-Security-Policy" content="%s"><meta name="referrer" content="no-referrer"><script>%s</script>'%(csp,shim)
assert '<head>' in s
s=s.replace('<head>','<head>'+head,1)
open(dst,'w',encoding='utf8').write(s)
