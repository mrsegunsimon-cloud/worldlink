"""Live news: read news.json (rebuilt every few hours on the website) and replace the saved headlines. Usage: patch_live.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'async function liveNews(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('Saved on October 26, 2026. Tap a story to open it.','${NEWSAT||"Saved on October 26, 2026."} Tap a story to open it.')
rep('Top sports stories from October 25 and 26, 2026. Tap a story to open it.','${NEWSAT||"Top sports stories from October 25 and 26, 2026."} Tap a story to open it.')
fn='''let NEWSAT="";
async function liveNews(){
 try{
  const r=await WLN("get",{url:"https://worldlink.app/news.json?t="+Date.now()});
  if(!r||r.error||!r.body)return;
  const j=JSON.parse(r.body);
  const ok=a=>Array.isArray(a)&&a.every(x=>Array.isArray(x)&&x.length>=5&&typeof x[1]==="string"&&/^https:\\/\\//.test(x[4]));
  if(!j||!ok(j.world)||!ok(j.sports)||j.world.length<8||j.sports.length<6)return;
  WN.length=0;j.world.forEach(x=>WN.push(x));NEWS.length=0;j.sports.forEach(x=>NEWS.push(x));
  Object.keys(VID).forEach(k=>delete VID[k]);Object.keys(TRN).forEach(k=>delete TRN[k]);
  const d=new Date(j.updated*1000);
  NEWSAT="Updated "+d.toLocaleString([],{month:"short",day:"numeric",hour:"numeric",minute:"2-digit"})+".";
 }catch(e){}
}
setTimeout(liveNews,600);setInterval(liveNews,600000);
'''
rep('function worldNews(t){',fn+'function worldNews(t){')
open(sys.argv[2],'w',encoding='utf8').write(s)
