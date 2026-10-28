"""Founding Creator welcome gift. Usage: patch_fc.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'grantFC' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
rep('<div class="mute" style="font-size:17px">@${esc(me.name)}</div><div style="display:flex;gap:26px;margin-top:18px">',
    '<div class="mute" style="font-size:17px">@${esc(me.name)}</div>${me.wl&&me.wl.fc?\'<div style="display:inline-block;margin-top:8px;padding:4px 12px;border-radius:99px;background:linear-gradient(90deg,#f59e0b,#ef4444);color:#fff;font-size:13px;font-weight:700">🌟 Founding Creator</div>\':""}<div style="display:flex;gap:26px;margin-top:18px">')
fn='''async function grantFC(){try{if(!me.uid||Date.now()>Date.UTC(2027,0,31))return;await loadWallet();if(!me.wl||me.wl.fc)return;me.wl.fc=1;me.wl.vc=(me.wl.vc||0)+300;await saveWallet();
 open(`<h2 style="text-align:center">🌟 Welcome, Founding Creator!</h2><p style="text-align:center">You joined WorldLink early. Your profile now has a <b>Founding Creator</b> badge and you got <b>300 bonus coins</b> 🪙 to send as gifts.</p><p class="mute" style="text-align:center;font-size:13px">Post your first video and invite 3 friends - thank you for helping WorldLink grow.</p><button class="btn" id="x">Let's go</button>`)}catch(e){}}
'''
rep('function music(t){',fn+'function music(t){') if 'function music(t){' in s else None
rep('try{await loadR(D)}catch(e){}order=mk(1);build()}catch(e){}})();','try{await loadR(D)}catch(e){}order=mk(1);build();setTimeout(grantFC,2500)}catch(e){}})();')
open(sys.argv[2],'w',encoding='utf8').write(s)
