import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlBonus1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# wallet load + one-time split of old free coins from paid coins
rep('async function loadWallet(){if(!me.wl){me.wl={coins:0,cashed:0,vc:100};try{const D=await claude.use("db");if(D&&me.uid){const x=await D.collection("data/users/"+me.uid).doc("wallet").get();if(x.exists)me.wl=Object.assign(me.wl,x.data())}}catch(e){}}',
'''async function loadWallet(){if(!me.wl){/*wlBonus1*/me.wl={coins:0,cashed:0,vc:0};let ex=false,got=false;try{const D=await claude.use("db");if(D&&me.uid){const x=await D.collection("data/users/"+me.uid).doc("wallet").get();got=true;if(x.exists){ex=true;me.wl=Object.assign(me.wl,x.data())}}}catch(e){}
  if(me.wl.bn===undefined){if(ex){const paid=(me.wl.buys||[]).filter(b=>b&&!b.test).reduce((n,b)=>n+(b.coins||0),0),tot=me.wl.vc||0,bn=Math.max(0,tot-paid);me.wl.bn=bn;me.wl.vc=tot-bn}else me.wl.bn=got||!me.uid?100:0}}''')
# boosts use bonus coins first
rep('Your coins: <b id="bc">${me.wl.vc}</b>','Your coins: <b id="bc">${me.wl.vc+(me.wl.bn||0)}</b>')
rep('if(me.wl.vc<o[0]){n.textContent="You need "+(o[0]-me.wl.vc)+" more coins. Tap Buy coins.";return}','const tot=me.wl.vc+(me.wl.bn||0);if(tot<o[0]){n.textContent="You need "+(o[0]-tot)+" more coins. Tap Buy coins.";return}')
rep('me.wl.vc-=o[0];(me.wl.spent','{const u=Math.min(me.wl.bn||0,o[0]);me.wl.bn=(me.wl.bn||0)-u;me.wl.vc-=o[0]-u}(me.wl.spent')
rep('$("#bc").textContent=me.wl.vc;','$("#bc").textContent=me.wl.vc+(me.wl.bn||0);')
# welcome coins are bonus coins
rep('me.wl.fc=1;me.wl.vc=(me.wl.vc||0)+300;','me.wl.fc=1;me.wl.bn=(me.wl.bn||0)+300;')
# show bonus beside paid coins
bn='${me.wl.bn?` <span class="mute" style="font-size:12px">(+${me.wl.bn} bonus coins, for boosts only)</span>`:""}'
rep('Your coins: <b>🪙 ${me.wl.vc}</b></p><input class="in" id="pem"','Your coins: <b>🪙 ${me.wl.vc}</b>'+bn+'</p><input class="in" id="pem"')
rep('Your coins: <b>🪙 ${me.wl.vc}</b></p><div style="display:grid;grid-template-columns:repeat(4,1fr)','Your coins: <b>🪙 ${me.wl.vc}</b>'+bn+'</p><div style="display:grid;grid-template-columns:repeat(4,1fr)')
rep('you got <b>300 bonus coins</b> 🪙 to send as gifts.','you got <b>300 bonus coins</b> 🪙 to boost your videos.')
s=s.replace('2026.10.30-T','2026.10.30-U')
open(P,"w",encoding="utf8").write(s);print("ok")
