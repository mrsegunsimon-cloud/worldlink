"""Real cash-out requests (paid by hand). Usage: patch_cash.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'MINPAY' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
rep('let KYC={};','let KYC={};const MINPAY=5000;')
# wallet: show available + requests
rep('<p class="note">Demo only. No real money is held or sent.','${(me.wl.payouts||[]).length?`<h3 style="font-size:15px;margin:12px 0 4px">Payout requests</h3>${me.wl.payouts.slice().reverse().map(x=>`<div class="cm" style="display:flex;justify-content:space-between"><span>${ago(x.ts)}</span><b>${naira(x.amt)} · ${esc(x.st||"pending")}</b></div>`).join("")}`:""}<p class="note">Available to cash out: <b>${naira(Math.max(0,mine-(me.wl.cashed||0)))}</b> (minimum ${naira(MINPAY)}).</p><p class="note">Demo only. No real money is held or sent.')
rep('''  const mine=(me.wl.coins+(me.wl.fv||0))*COIN*SHARE;
  open(`<h2>Check and request</h2>''','''  const mine=Math.max(0,(me.wl.coins+(me.wl.fv||0))*COIN*SHARE-(me.wl.cashed||0));
  open(`<h2>Check and request</h2>''')
rep('''<p class="note" id="st"></p><button class="btn" id="nx">Request payout</button><button class="btn ghost" id="bk">Back</button>`);
  $("#bk").onclick=()=>cashOut(2);''','''<p class="note">${mine<MINPAY?"The minimum payout is "+naira(MINPAY)+". Keep earning and come back.":"We pay by bank transfer after checking your request. This usually takes a few days."}</p><p class="note" id="st"></p><button class="btn" id="nx" ${mine<MINPAY?"disabled":""}>Request payout</button><button class="btn ghost" id="bk">Back</button>`);
  $("#bk").onclick=()=>cashOut(2);''')
rep('''  $("#nx").onclick=()=>{$("#nx").disabled=true;$("#st").textContent="Demo only: in the real app this request goes to review and your identity is checked before any money is sent. Nothing was sent now."};''','''  $("#nx").onclick=async()=>{
   if(!me.uid){$("#st").textContent="Sign in first so we know who to pay.";return}
   if(mine<MINPAY)return;
   $("#nx").disabled=true;$("#st").textContent="Sending…";
   const id="po"+Date.now()+me.uid.slice(0,4),rq={id,kind:"payout",uid:me.uid,name:me.name,legal:KYC.n,idType:KYC.t,bank:KYC.b,acct:KYC.a,amt:Math.round(mine),coins:me.wl.coins+(me.wl.fv||0),ts:Date.now(),st:"pending"};
   try{const D=await claude.use("db");if(!D)throw 0;await D.collection("reports").doc(id).set(rq)}catch(e){$("#nx").disabled=false;$("#st").textContent="Could not send. Check your internet and try again.";return}
   me.wl.cashed=(me.wl.cashed||0)+Math.round(mine);(me.wl.payouts=me.wl.payouts||[]).push({id,amt:Math.round(mine),ts:rq.ts,st:"pending"});await saveWallet();
   $("#st").textContent="✅ Request sent. We will pay "+naira(Math.round(mine))+" to "+KYC.b+" ending "+KYC.a.slice(-4)+" after checking it.";
  };''')
open(sys.argv[2],'w',encoding='utf8').write(s)
