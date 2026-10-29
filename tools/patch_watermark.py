import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlWM" in s: print("already");sys.exit(0)
# 1. feed overlay
a='<div class="shade"></div>'
i=s.find('<section class="clip" data-i'); j=s.find(a,i); assert i>0 and j>i
s=s[:j]+'${c.src?`<div class="wlwm" aria-hidden="true"><b>🌍 WorldLink</b><span>@${esc(c.u)}</span></div>`:""}'+s[j:]
css='.clip .wlwm{position:absolute;z-index:2;left:14px;top:92px;pointer-events:none;color:#fff;text-shadow:0 1px 5px rgba(0,0,0,.85);font-size:15px;line-height:1.15;opacity:.9;animation:wlwm 12s ease-in-out infinite}.clip .wlwm b{display:block;font-weight:900;letter-spacing:.3px}.clip .wlwm span{font-size:12px;font-weight:700;opacity:.85}@keyframes wlwm{0%,30%{left:14px;top:92px}38%,64%{left:calc(100% - 215px);top:46%}72%,100%{left:14px;top:92px}}/*wlWM*/'
k=s.find('.clip video{position:absolute'); assert k>0
s=s[:k]+css+s[k:]
# 2. burn watermark into saved copies
a='function drawCap(x,W,H,c){\n'
assert a in s
s=s.replace(a,a+' if(c&&c.wm){x.save();const fs=Math.max(12,Math.round(W*.045));x.font="900 "+fs+"px system-ui,Arial,sans-serif";x.textAlign="right";x.textBaseline="alphabetic";x.shadowColor="rgba(0,0,0,.8)";x.shadowBlur=fs*.3;x.fillStyle="rgba(255,255,255,.92)";x.fillText("\\u{1F30D} WorldLink",W-W*.04,H*.9);x.font="700 "+Math.round(fs*.75)+"px system-ui,Arial,sans-serif";x.fillText("@"+c.wm,W-W*.04,H*.9+fs*.95);x.restore()}\n',1)
a='try{let out=f;const ov=OV();\n   if(PFX||ov){'
assert a in s
s=s.replace(a,'try{let out=f;const ov=Object.assign({},OV()||{},{wm:me.name});\n   if(1){',1)
open(P,"w",encoding="utf8").write(s);print("ok")
