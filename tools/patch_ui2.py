"""Home: follow badge on the poster's avatar + thin progress bar. Inbox: online dot, teal story rings, highlighted unread row. Usage: patch_ui2.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'class="fplus"' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# Home: follow badge
rep('''<div class="av">${c.uid&&c.uid===me.uid&&me.pic?`<img src="${me.pic}" alt="">`:c.u[0].toUpperCase()}</div>
  <button data-a="like"''','''<div class="av">${c.uid&&c.uid===me.uid&&me.pic?`<img src="${me.pic}" alt="">`:c.u[0].toUpperCase()}</div>${c.u&&c.u!==me.name&&!(me.f||[]).includes(c.u)?`<button data-a="fw" data-i="${i}" class="fplus" aria-label="Follow @${esc(c.u)}">+</button>`:""}
  <button data-a="like"''')
rep('else if(a==="gf")giftSheet(i);','else if(a==="gf")giftSheet(i);else if(a==="fw"){followFeed(i,b)}')
rep('let last=0,tt;','''async function followFeed(i,b){
 const c=CLIPS[i];if(!c||!c.u)return;
 if(!(me.f||[]).includes(c.u))me.f=(me.f||[]).concat(c.u);
 document.querySelectorAll('.fplus[data-i]').forEach(x=>{if(CLIPS[+x.dataset.i]&&CLIPS[+x.dataset.i].u===c.u)x.remove()});
 try{const D=await claude.use("db");if(D&&me.uid)await D.collection("follows").doc(me.uid).set({list:me.f})}catch(e){}
 try{notify(c.uid,"started following you")}catch(e){}
}
let last=0,tt;''')
# Home: progress bar
rep('.rail .av{width:48px;height:48px;border:3px solid #25C7F0;margin-bottom:4px}','''.rail .av{width:48px;height:48px;border:3px solid #25C7F0;margin-bottom:4px}
.fplus{width:22px;height:22px;border-radius:50%;background:#FF2D55;color:#fff;font-size:17px;font-weight:700;line-height:22px;padding:0;margin:-16px 0 0;position:relative;z-index:2;align-self:center}
#pbar{position:fixed;left:12px;right:12px;height:3px;border-radius:2px;background:rgba(255,255,255,.3);z-index:6;pointer-events:none}
#pbar i{display:block;height:100%;width:0;border-radius:2px;background:#fff}''')
rep('let last=0,tt;','''(function(){const p=document.createElement("div");p.id="pbar";p.innerHTML="<i></i>";document.body.appendChild(p);
 const place=()=>{const n=document.querySelector("nav");p.style.bottom=(n?n.offsetHeight+4:74)+"px";p.style.display=document.getElementById("sheet").classList.contains("on")?"none":"block"};
 place();addEventListener("resize",place);setInterval(place,1000);
 document.addEventListener("timeupdate",e=>{const v=e.target;if(!v||v.tagName!=="VIDEO"||!v.closest("#feed")||v.paused&&!v.currentTime)return;if(v.duration)p.firstChild.style.width=Math.min(100,v.currentTime/v.duration*100)+"%"},true)})();
let last=0,tt;''')
# Inbox polish
rep('<b style="font-size:20px">Inbox</b><button id="qs"','<b style="font-size:20px">Inbox <span aria-hidden="true" style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#22C55E;vertical-align:middle;margin-left:4px"></span></b><button id="qs"')
rep('background:linear-gradient(45deg,#1E6FFF,#FF2D55)"><div class="av" style="width:100%;height:100%;border:3px solid var(--card)','background:linear-gradient(45deg,#25C7F0,#2EE59D)"><div class="av" style="width:100%;height:100%;border:3px solid var(--card)')
rep('''row('id="qa"',circ("#FF2D55","⚡")''','''row('id="qa"'+(nf?' class="unr"':''),circ("#FF2D55","⚡")''')
rep('.sx{position:sticky;','.unr{background:var(--bg)}\n.sx{position:sticky;')
open(sys.argv[2],'w',encoding='utf8').write(s)
