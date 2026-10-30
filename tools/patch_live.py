import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLive1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
rep('const PSK="pk_test_1ad0688b5e46c91db88d4cd865d8846a75ce5b74"','/*wlLive1*/const PSK="pk_live_84d6621a7c198e0e9801e7fba01523c192a1024a"')
rep('🧪 TEST MODE: payments use fake money. Use Paystack\'s test card, no real money is taken.','🔒 Secure payment by Paystack. Your coins are added a few seconds after you pay.')
rep('<button class="btn" id="bc2">Buy coins (test mode)</button><button class="btn ghost" id="tp">Get 500 free demo coins</button><p class="note">Demo only. These coins are free and have no money value. In the real app coins are bought through Google Play.</p>','<button class="btn" id="bc2">Buy coins</button>')
rep('$("#bc2").onclick=()=>buyCoins();$("#tp").onclick=()=>{me.wl.vc+=500;saveWallet();draw()};','$("#bc2").onclick=()=>buyCoins();')
rep('Your demo coins:','Your coins:')
rep('Not enough demo coins for a "+g[1]+". Tap the button below to get more.','Not enough coins for a "+g[1]+". Tap Buy coins below.')
rep('me.wl={coins:0,cashed:0,vc:500}','me.wl={coins:0,cashed:0,vc:100}')
s=s.replace('2026.10.30-S','2026.10.30-T')
open(P,"w",encoding="utf8").write(s);print("ok")
