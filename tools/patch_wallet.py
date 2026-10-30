import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlWallet1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
# gifts: tell the person who got the gift (in-app list and phone alert)
rep('.set({to:c.uid,from:me.uid,c:g[2],g:g[1],ts:Date.now()})}catch(e){}}','.set({to:c.uid,from:me.uid,c:g[2],g:g[1],ts:Date.now()});notify(c.uid,"sent you "+g[0]+" "+g[1]+" ("+g[2]+" coins)")}catch(e){}}')
rep('.set({to:h.uid,from:me.uid,c:g[2],g:g[1],ts:Date.now()})}catch(e){}','.set({to:h.uid,from:me.uid,c:g[2],g:g[1],ts:Date.now()});notify(h.uid,"sent you "+g[0]+" "+g[1]+" ("+g[2]+" coins) in your live")}catch(e){}')
# coins arrive: say so on screen
rep('if(n)await saveWallet();','if(n){await saveWallet();try{wlNote("🪙 "+n+" coins added to your wallet")}catch(e){}}')
# wallet screen: show the real balance
rep('async function wallet(){\n await loadWallet();','async function wallet(){\n /*wlWallet1*/await loadWallet();try{await claimCredits()}catch(e){}')
rep('open(`<h2>Wallet and earnings</h2><div style="background:var(--bg);border-radius:16px;padding:16px;text-align:center"><div class="mute" style="font-size:13px">Gift coins received</div>',
 'const buys=(me.wl.buys||[]).filter(b=>b&&!b.test).slice(-3).reverse();\n open(`<h2>Wallet and earnings</h2><div style="display:flex;gap:8px"><div class="cm" style="flex:1;text-align:center;margin:0"><div class="mute" style="font-size:12px">Coins to spend</div><b style="font-size:24px">🪙 ${me.wl.vc||0}</b></div><div class="cm" style="flex:1;text-align:center;margin:0"><div class="mute" style="font-size:12px">Bonus (boosts only)</div><b style="font-size:24px">🪙 ${me.wl.bn||0}</b></div></div><button class="btn" id="wbc" style="margin:8px 0">Buy coins</button>${buys.length?`<div class="mute" style="font-size:13px;margin:0 0 4px">Recent purchases</div>${buys.map(b=>`<div class="cm" style="display:flex;justify-content:space-between"><span>${ago(b.ts)}</span><b>+${b.coins} coins · ${naira(b.naira||0)}</b></div>`).join("")}`:""}<h3 style="font-size:15px;margin:14px 0 6px">Earnings from gifts</h3><div style="background:var(--bg);border-radius:16px;padding:16px;text-align:center"><div class="mute" style="font-size:13px">Gift coins received</div>')
rep('(${naira(COIN)} per coin, demo rate)','(${naira(COIN)} per coin)')
rep('<p class="note">Demo only. No real money is held or sent. The coin rate and the split are examples. Before launch you set the real rate, the app\'s share, and the payout rules with a licensed payment provider, and check how Google Play\'s payment rules apply to buying coins.</p>','<p class="note">You earn 60% of the value of gift coins people send you. We check every payout request before paying it to your bank account. Bonus coins have no cash value.</p>')
rep('$("#co").onclick=()=>cashOut(1);$("#bk").onclick=()=>profMenu();','$("#co").onclick=()=>cashOut(1);$("#bk").onclick=()=>profMenu();if($("#wbc"))$("#wbc").onclick=()=>buyCoins(wallet);')
s=s.replace('2026.10.30-V','2026.10.30-W')
open(P,"w",encoding="utf8").write(s);print("ok")
