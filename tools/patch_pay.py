"""Buy coins with Paystack (TEST MODE). Usage: patch_pay.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'function buyCoins' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]);s=s.replace(a,b)
fn='''const PSK="pk_test_1ad0688b5e46c91db88d4cd865d8846a75ce5b74",PACKS=[[100,500],[250,1000],[600,2000],[1500,5000]];
function psLoad(){return new Promise((ok,no)=>{if(window.PaystackPop)return ok();const sc=document.createElement("script");sc.src="https://js.paystack.co/v1/inline.js";sc.onload=ok;sc.onerror=()=>no(new Error("Could not load the payment page. Check your internet."));document.head.appendChild(sc)})}
async function buyCoins(back){
 await loadWallet();let em="";try{em=localStorage.getItem("wl_pem")||""}catch(e){}
 open(`<h2 style="text-align:center">Buy coins</h2><p class="note" style="text-align:center;margin:0 0 8px">🧪 TEST MODE: payments use fake money. Use Paystack's test card, no real money is taken.</p><p style="text-align:center;margin:0 0 10px">Your coins: <b>🪙 ${me.wl.vc}</b></p><input class="in" id="pem" type="email" placeholder="Your email for the receipt" value="${esc(em)}" aria-label="Email"><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0">${PACKS.map((p,k)=>`<button data-pk="${k}" style="background:var(--bg);border-radius:12px;padding:12px 4px;border:1px solid var(--line);color:inherit"><b style="font-size:18px">🪙 ${p[0]}</b><span style="display:block;color:var(--acc);font-weight:700">₦${p[1].toLocaleString()}</span></button>`).join("")}</div><p class="note" id="st"></p><button class="btn ghost" id="x">Close</button>`);
 $("#panel").querySelectorAll("[data-pk]").forEach(b=>b.onclick=async()=>{
  const p=PACKS[+b.dataset.pk],e=$("#pem").value.trim(),st=$("#st");
  if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(e)){st.textContent="Type a correct email first.";return}
  try{localStorage.setItem("wl_pem",e)}catch(_){ }
  st.textContent="Opening payment…";
  try{await psLoad();const ref="wl"+Date.now()+Math.floor(Math.random()*1e4);
   PaystackPop.setup({key:PSK,email:e,amount:p[1]*100,currency:"NGN",ref,metadata:{uid:me.uid||"",coins:p[0]},
    callback:function(r){me.wl.vc+=p[0];(me.wl.buys=me.wl.buys||[]).push({ref:r.reference||ref,coins:p[0],naira:p[1],ts:Date.now(),test:true});saveWallet();buyCoins();setTimeout(()=>{const s2=$("#st");if(s2)s2.textContent="✅ Payment received (test). "+p[0]+" coins added."},50)},
    onClose:function(){const s2=$("#st");if(s2&&!/received/.test(s2.textContent))s2.textContent="Payment closed. No coins were added."}}).openIframe()
  }catch(err){st.textContent=err.message||"Payment could not start."}
 });
}
'''
rep('async function giftSheet(i){',fn+'async function giftSheet(i){')
rep('<button class="btn ghost" id="tp">Get 500 free demo coins</button>','<button class="btn" id="bc2">Buy coins (test mode)</button><button class="btn ghost" id="tp">Get 500 free demo coins</button>')
rep('  $("#tp").onclick=()=>{me.wl.vc+=500;saveWallet();draw()};','  $("#bc2").onclick=()=>buyCoins();$("#tp").onclick=()=>{me.wl.vc+=500;saveWallet();draw()};')
rep('<button class="btn ghost" id="iv2">','<button class="btn ghost" id="bc3">🪙 Buy coins (test mode)</button><button class="btn ghost" id="iv2">')
rep(' $("#iv2").onclick=inviteFriends;',' $("#bc3").onclick=()=>buyCoins();$("#iv2").onclick=inviteFriends;')
open(sys.argv[2],'w',encoding='utf8').write(s)
