"""Live scores and tables from sports.json (rebuilt by the website every 30 minutes). Usage: patch_sports.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'async function liveSports(' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('Snapshots saved on Oct 25 and 26, 2026. Live updates need a licensed sports data feed in the full app.','${SPAT?SPAT+" Tennis and cricket scores, and the NBA, NHL and MLS tables, are still saved copies.":"Snapshots saved on Oct 25 and 26, 2026."}')
rep('x[4]==="live"?"Live when this was saved":x[4]==="ft"?"Full time, "+when(x[5]):when(x[5])}${x[6]?". "+x[6]:""}','x[4]==="live"?(SPAT?"Live now":"Live when this was saved"):x[4]==="ft"?"Full time, "+when(x[5]):when(x[5])}${x[6]?". "+x[6]:""}')
fn='''let SPAT="";
async function liveSports(){
 try{
  const r=await WLN("get",{url:"https://worldlink.app/sports.json?t="+Date.now()});
  if(!r||r.error||!r.body)return;
  const j=JSON.parse(r.body);if(!j||!j.leagues)return;
  const okG=g=>Array.isArray(g)&&g.length>=2&&g.every(x=>Array.isArray(x)&&x.length>=6&&typeof x[0]==="string"&&typeof x[1]==="string"&&["sch","live","ft"].includes(x[4]));
  const okT=t=>Array.isArray(t)&&t.length>=8&&t.every(x=>Array.isArray(x)&&x.length===6&&typeof x[1]==="string");
  let n=0;
  Object.keys(j.leagues).forEach(k=>{const L=LG[k],e=j.leagues[k];if(!L||!e)return;
   if(okG(e.games)){L[1]=e.games;n++}
   if(["epl","la","it","de","fr","cl"].includes(k)&&okT(e.table)){L[2]=true;L[3]=e.table;L[4]=undefined}});
  if(!n)return;
  const d=new Date(j.updated*1000);
  SPAT="Scores updated "+d.toLocaleString([],{month:"short",day:"numeric",hour:"numeric",minute:"2-digit"})+".";
 }catch(e){}
}
setTimeout(liveSports,700);setInterval(liveSports,600000);
'''
rep('let NEWSAT="";',fn+'let NEWSAT="";')
open(sys.argv[2],'w',encoding='utf8').write(s)
