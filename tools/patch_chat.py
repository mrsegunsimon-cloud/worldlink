"""Chat screens fill the whole screen (like Inbox). Usage: patch_chat.py in out"""
import sys,re
s=open(sys.argv[1],encoding='utf8').read()
if 'id="cin"' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
# chat(p)
a=s.index('async function chat(p){');i=s.index(' open(`',a);j=s.index('`);',i)
old=s[i:j+3]
msgs=re.search(r'<div id="ml"[^>]*>(\$\{m\.length\?.*?)</div><div style="display:flex;gap:8px">',old,re.S).group(1)
note=re.search(r'<p class="note">(.*?)</p>',old,re.S).group(1)
new=''' openFull(`<div class="hd"><button id="bk" aria-label="Back">←</button><b style="font-size:18px;flex:1;margin-left:6px;overflow:hidden;text-overflow:ellipsis">@${p}</b><button class="ib" id="vc" aria-label="Voice call">📞</button><button class="ib" id="vd" aria-label="Video call">📹</button></div><div id="ml" class="pgx" style="padding:8px 14px">'''+msgs+'''</div><div id="cin" style="padding:8px 14px 12px;border-top:1px solid var(--line)"><div style="display:flex;gap:8px"><input class="in" id="mi" maxlength="500" placeholder="Write a message" aria-label="Message" style="margin:0"><button class="btn" id="ms" style="width:auto;margin:0">Send</button></div><p class="note" style="margin:6px 0 0">'''+note+'''</p></div>`);'''
s=s.replace(old,new)
# dmShow(d,pre)
a=s.index('function dmShow(d,pre){');i=s.index(' open(`',a);j=s.index('`);',i)
old=s[i:j+3]
msgs=re.search(r'<div id="ml"[^>]*>(\$\{d\.m\.length\?.*?)</div><div style="display:flex;gap:8px">',old,re.S).group(1)
note=re.search(r'<p class="note">(.*?)</p>',old,re.S).group(1)
new=''' openFull(`<div class="hd"><button id="bk" aria-label="Back">←</button><b style="font-size:18px;flex:1;margin-left:6px;overflow:hidden;text-overflow:ellipsis">@${esc(o.n)}</b><button class="ib" id="vc" aria-label="Voice call">📞</button><button class="ib" id="vd" aria-label="Video call">📹</button></div><div id="ml" class="pgx" style="padding:8px 14px">'''+msgs+'''</div><div id="cin" style="padding:8px 14px 12px;border-top:1px solid var(--line)"><div style="display:flex;gap:8px"><input class="in" id="mi" maxlength="500" placeholder="Write a message" aria-label="Message" value="${esc(pre||"")}" style="margin:0"><button class="btn" id="ms" style="width:auto;margin:0">Send</button></div><p class="note" style="margin:6px 0 0">'''+note+'''</p></div>`);
 $("#vc").onclick=()=>{close();startCall(o.n,false)};$("#vd").onclick=()=>{close();startCall(o.n,true)};'''
s=s.replace(old,new)
open(sys.argv[2],'w',encoding='utf8').write(s)
