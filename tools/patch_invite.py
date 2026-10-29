"""Invite friends button (Friends screen + Settings). Usage: patch_invite.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function inviteFriends' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
fn='''function inviteFriends(){
 const url="https://worldlink.app/"+(me.name&&me.name!=="you"?"?ref="+encodeURIComponent(me.name):""),txt="Join me on WorldLink - videos, photos, news, sports, music and beaches from all over the world. Be one of the first creators and get a Founding Creator badge + free coins 🌍";
 if(navigator.share){navigator.share({title:"WorldLink",text:txt,url}).catch(()=>{});return}
 open(`<h2>Invite friends</h2><p class="mute">Copy this message and send it on WhatsApp, Instagram or Telegram.</p><textarea class="in" id="ivt" rows="5" readonly>${esc(txt+" "+url)}</textarea><button class="btn" id="ivc">Copy message</button><button class="btn ghost" id="x">Close</button>`);
 $("#ivc").onclick=async()=>{try{await navigator.clipboard.writeText($("#ivt").value);$("#ivc").textContent="Copied ✓"}catch(e){$("#ivt").select();$("#ivc").textContent="Select and copy the text"}};
}
'''
rep('function friends(tk){',fn+'function friends(tk){')
rep('<div class="pgx" style="padding:0 16px"><div style="display:flex;border-bottom:1px solid var(--line)">','<div class="pgx" style="padding:0 16px"><button class="btn" id="inv" style="margin:6px 0 8px">📨 Invite friends to WorldLink</button><div style="display:flex;border-bottom:1px solid var(--line)">')
rep(' $("#panel").querySelectorAll("[data-ft]").forEach(b=>b.onclick=()=>friends(b.dataset.ft));',' $("#inv").onclick=inviteFriends;$("#panel").querySelectorAll("[data-ft]").forEach(b=>b.onclick=()=>friends(b.dataset.ft));')
rep('<button class="btn ghost" id="au">Sign in or create account</button>','<button class="btn ghost" id="iv2">📨 Invite friends</button><button class="btn ghost" id="au">Sign in or create account</button>')
rep(' $("#wl").onclick=wallet;$("#au").onclick',' $("#iv2").onclick=inviteFriends;$("#wl").onclick=wallet;$("#au").onclick')
open(sys.argv[2],'w',encoding='utf8').write(s)
