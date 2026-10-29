"""Restyle: profile header + tabs + tiles, and the profile menu as a slide-in panel of grouped cards. Usage: patch_ui.py in out"""
import sys,re
s=open(sys.argv[1],encoding='utf8').read()
if 'id="pmenu"' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
# 1. profile menu
i=s.index('function profMenu(){');j=s.index('function profile(tabk){')
new_menu='''function profMenu(){
 const old=document.getElementById("pmenu");if(old)old.remove();
 const ch='<span class="ch">›</span>';
 const row=(id,ic,l)=>`<button class="pmr" data-pr="${id}"><span class="pi">${ic}</span>${l}${ch}</button>`;
 const el=document.createElement("div");el.id="pmenu";
 el.innerHTML=`<div class="pp"><div class="pmg">${row("wl","👛","Balance and earnings")}</div><div class="pmg">${row("bc","🪙","Buy coins")}${row("iv","📨","Invite friends")}</div><div class="pmg">${row("au","👤","Sign in or create account")}${row("bl","🚫","Blocked accounts ("+me.b.length+")")}</div><div class="pmg">${row("md","🛡️","Moderator tools")}${row("lg","🌐","Language")}${row("th","◐","Theme")}</div></div>`;
 document.body.appendChild(el);
 const shut=()=>el.remove();
 el.onclick=e=>{if(e.target===el)shut()};
 const A={wl:wallet,bc:()=>buyCoins(),iv:inviteFriends,au:()=>authSheet("up"),bl:blockedList,md:modScreen,lg:langSheet,th:theme};
 el.querySelectorAll("[data-pr]").forEach(b=>b.onclick=()=>{shut();A[b.dataset.pr]()});
}
'''
s=s[:i]+new_menu+s[j:]
rep('.sx{position:sticky;','''#pmenu{position:fixed;inset:0;z-index:150;background:rgba(0,0,0,.4);display:flex;justify-content:flex-end}
#pmenu .pp{width:86%;max-width:390px;height:100%;background:#f4f4f5;overflow-y:auto;padding:max(16px,env(safe-area-inset-top)) 14px 24px;color:#111;animation:ppin .22s ease-out}
@keyframes ppin{from{transform:translateX(100%)}to{transform:none}}
@media (prefers-reduced-motion:reduce){#pmenu .pp{animation:none}}
#pmenu .pmg{display:flex;flex-direction:column;background:#fff;border-radius:18px;margin:0 0 12px;padding:4px 0}
#pmenu .pmr{display:flex;align-items:center;gap:14px;width:100%;padding:17px 16px;font-size:17px;font-weight:600;text-align:left;color:#111;background:none;border:0}
#pmenu .pmr .pi{width:26px;text-align:center;font-size:20px}
#pmenu .pmr .ch{margin-left:auto;font-size:24px;opacity:.4;font-weight:400}
.hd.ph{position:sticky;top:0;z-index:5;background:var(--card)}
.hd.ph b{font-size:18px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:60%}
.pgt{gap:1px}
.pgt .vw{font-size:15px;left:8px;bottom:7px}
.sx{position:sticky;''')
# 2. profile header
rep('<div class="hd"><button id="ed" aria-label="Edit profile">✎</button><button id="pm" aria-label="Settings">☰</button></div><div class="pgx">','<div class="hd ph"><button id="ed" aria-label="Edit profile">✎</button><b>${esc(me.name)}</b><button id="pm" aria-label="Settings">☰</button></div><div class="pgx">')
# 3. tabs: short underline under the icon
rep('''style="flex:1;padding:12px 0;display:grid;place-items:center;border-bottom:2px solid ${tabk===k?"var(--ink)":"transparent"};opacity:${tabk===k?1:.5};color:inherit">${ic[k]}</button>`;''','''style="flex:1;padding:10px 0 0;display:grid;place-items:center;opacity:${tabk===k?1:.5};color:inherit"><span style="display:inline-block;padding:0 6px 8px;border-bottom:3px solid ${tabk===k?"var(--ink)":"transparent"}">${ic[k]}</span></button>`;''')
open(sys.argv[2],'w',encoding='utf8').write(s)
