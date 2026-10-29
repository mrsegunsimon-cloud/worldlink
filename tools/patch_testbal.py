"""Moderator-only test earnings button. Usage: patch_testbal.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'data-tb="1"' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
rep('<h2 style="margin-top:18px">Moderation</h2>','<div class="cm"><b>Test earnings</b><div class="mute" style="font-size:13px">Adds 3,000 coins to your own wallet (about ₦9,000 to cash out) so you can try a payout. Remove them before real launch.</div><div style="display:flex;gap:8px"><button class="btn ghost" style="width:auto;margin:8px 0 0;padding:8px 14px" data-tb="1">Add test earnings</button><button class="btn ghost" style="width:auto;margin:8px 0 0;padding:8px 14px" data-tb="-1">Remove</button></div></div><h2 style="margin-top:18px">Moderation</h2>')
rep(' $("#panel").querySelectorAll("[data-pay]")',' $("#panel").querySelectorAll("[data-tb]").forEach(b=>b.onclick=async()=>{me.wl.coins=Math.max(0,(me.wl.coins||0)+3000*+b.dataset.tb);await saveWallet();modScreen()});\n $("#panel").querySelectorAll("[data-pd]")')
open(sys.argv[2],'w',encoding='utf8').write(s)
