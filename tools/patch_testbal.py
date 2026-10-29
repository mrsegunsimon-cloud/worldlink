"""Moderator-only test earnings button. Usage: patch_testbal.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'data-tb="1"' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
rep('<h2 style="margin-top:18px">Moderation</h2>','<div class="cm"><b>Test earnings</b><div class="mute" style="font-size:13px">Adds 3,000 coins to your own wallet (about ₦9,000 to cash out) so you can try a payout. Remove them before real launch.</div><div><b>Your coins now: ${me.wl.coins||0}</b></div><div style="display:flex;gap:8px"><button class="btn ghost" style="width:auto;margin:8px 0 0;padding:8px 14px" data-tb="1">Add test earnings</button><button class="btn ghost" style="width:auto;margin:8px 0 0;padding:8px 14px" data-tb="-1">Reset my wallet to 0</button></div></div><h2 style="margin-top:18px">Moderation</h2>')
rep(' $("#panel").querySelectorAll("[data-pay]")',' $("#panel").querySelectorAll("[data-tb]").forEach(b=>b.onclick=async()=>{if(+b.dataset.tb<0){me.wl.coins=0;me.wl.fv=0;me.wl.cashed=0;me.wl.payouts=[]}else me.wl.coins=(me.wl.coins||0)+3000;await saveWallet();modScreen()});\n $("#panel").querySelectorAll("[data-pay]")')
open(sys.argv[2],'w',encoding='utf8').write(s)
