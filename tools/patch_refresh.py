import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'wlRefresh' in s: print('already');sys.exit()
a='(async()=>{try{const D=await claude.use("db");if(!D)return;try{const U=await claude.use("user");if(U){me.uid=await U.id();'
assert s.count(a)==1
s=s.replace(a,'async function wlBoot(){try{const D=await claude.use("db");if(!D)return;try{const U=await claude.use("user");if(U){me.uid=await U.id();')
b='s.docs.map(d=>d.data()).filter(v=>v&&!v.del).sort((a,b)=>a.ts-b.ts).forEach(v=>CLIPS.push('
assert s.count(b)==1
s=s.replace(b,'s.docs.map(d=>d.data()).filter(v=>v&&!v.del&&!CLIPS.some(c=>c.id===(v.id||"o"+v.ts))).sort((a,b)=>a.ts-b.ts).forEach(v=>CLIPS.push(')
c='order=mk(1);build();setTimeout(grantFC,2500)}catch(e){}})();\nloadGR();loadTR();loadMV();loadLS();loadEV();loadPS();loadST();loadNF();'
assert s.count(c)==1
s=s.replace(c,'order=mk(1);build();setTimeout(grantFC,2500)}catch(e){}}\nwlBoot();\nwindow.wlRefresh=function(){try{loadGR();loadTR();loadMV();loadLS();loadEV();loadPS();loadST();loadNF();wlBoot()}catch(e){}};\nloadGR();loadTR();loadMV();loadLS();loadEV();loadPS();loadST();loadNF();')
open(p,'w',encoding='utf8').write(s);print('patched')
