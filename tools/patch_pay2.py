"""Coins arrive only after the payment checker records them (when PAYSRV is true). Usage: patch_pay2.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'claimCredits' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
fn='''const PAYSRV=true;
async function claimCredits(){
 try{
  if(!me.uid)return 0;await loadWallet();const pend=(me.wl.pend||[]).slice();if(!pend.length)return 0;
  const D=await claude.use("db");if(!D)return 0;let n=0;
  for(const ref of pend){
   try{const x=await D.collection("credits").doc(ref).get();
    if(x.exists){const c=x.data();if(c&&c.uid===me.uid&&c.coins>0){me.wl.vc+=c.coins;(me.wl.buys=me.wl.buys||[]).push({ref,coins:c.coins,naira:c.naira,ts:c.ts,test:!!c.test});me.wl.pend=me.wl.pend.filter(r=>r!==ref);n+=c.coins}}
   }catch(e){}
  }
  if(n)await saveWallet();return n}catch(e){return 0}}
async function waitCredit(ref,st){
 for(let i=0;i<20;i++){
  await new Promise(r=>setTimeout(r,2500));
  const n=await claimCredits();
  if(n){const s2=$("#st");if(s2)s2.textContent="✅ Payment confirmed. "+n+" coins added.";return}
 }
 const s2=$("#st");if(s2)s2.textContent="We are still confirming your payment. Your coins will appear in your wallet within a few minutes."}
'''
rep('async function buyCoins(back){',fn+'async function buyCoins(back){')
rep('callback:function(r){me.wl.vc+=p[0];','callback:function(r){if(PAYSRV){(me.wl.pend=me.wl.pend||[]).push(r.reference||ref);saveWallet();const s2=$("#st");if(s2)s2.textContent="Payment received. Confirming…";waitCredit(r.reference||ref);return}me.wl.vc+=p[0];')
# check pending on opening wallet and buy sheet
rep(' await loadWallet();let em="";try{em=localStorage.getItem("wl_pem")||""}catch(e){}',' await loadWallet();if(PAYSRV)await claimCredits();let em="";try{em=localStorage.getItem("wl_pem")||""}catch(e){}')
open(sys.argv[2],'w',encoding='utf8').write(s)
