"""Moderator payout list: see cash-out requests, copy bank details, mark paid. Usage: patch_payouts.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'data-pd=' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
rep('let D=null,mods=[],rs=[];','let D=null,mods=[],rs=[],po=[];')
rep('rs=s.docs.map(d=>d.data()).filter(r=>r&&r.type).sort((a,b)=>b.ts-a.ts)}','const all=s.docs.map(d=>d.data());rs=all.filter(r=>r&&r.type).sort((a,b)=>b.ts-a.ts);po=all.filter(r=>r&&r.kind==="payout").sort((a,b)=>b.ts-a.ts)}')
rep('''open(`<h2>Moderation</h2><p class="mute">${openN} open report${openN===1?"":"s"}, ${rs.length} in total</p>''','''const poN=po.filter(r=>r.st!=="paid").length;
 open(`<h2>Payout requests</h2><p class="mute">${poN} waiting to be paid, ${po.length} in total. Send the money from your bank app, then tap Mark paid.</p>${po.length?po.map((r,i)=>`<div class="cm"><b>${naira(r.amt)} · @${esc(r.name)}</b> <span class="mute" style="font-size:13px">${ago(r.ts)} · ${r.st==="paid"?"PAID":"waiting"}</span><div>${esc(r.legal||"")}</div><div>Bank: ${esc(r.bank||"")}</div><div>Account: <b>${esc(r.acct||"")}</b></div><div class="mute" style="font-size:13px">${esc(r.idType||"")} checked by you · ${r.coins||0} coins</div>${r.st==="paid"?"":`<button class="btn" style="width:auto;margin:8px 0 0;padding:8px 14px" data-pd="${i}">Mark paid</button>`}</div>`).join(""):'<p class="mute">No payout requests yet.</p>'}<h2 style="margin-top:18px">Moderation</h2><p class="mute">${openN} open report${openN===1?"":"s"}, ${rs.length} in total</p>''')
rep(''' $("#panel").querySelectorAll("[data-dm]")''',''' $("#panel").querySelectorAll("[data-pd]").forEach(b=>b.onclick=async()=>{
  const r=po[+b.dataset.pd];r.st="paid";r.paid=Date.now();
  try{await D.collection("reports").doc(r.id).set(r)}catch(e){}
  modScreen();
 });
 $("#panel").querySelectorAll("[data-dm]")''')
open(sys.argv[2],'w',encoding='utf8').write(s)
