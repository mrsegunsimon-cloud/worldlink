import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlEye" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:60]
    s=s.replace(a,b,1)
rep('<input class="in" id="ap" type="password" autocomplete="${up?"new-password":"current-password"}" placeholder="Password (8+ characters)" aria-label="Password">',
    '<div style="position:relative"><input class="in" id="ap" type="password" autocomplete="${up?"new-password":"current-password"}" placeholder="Password (8+ characters)" aria-label="Password" style="padding-right:52px"><button type="button" id="eye" aria-label="Show password" style="position:absolute;right:6px;top:50%;transform:translateY(-50%);background:none;border:0;font-size:22px;padding:8px;color:inherit">👁️</button></div>')
rep(' $("#sw").onclick=()=>authSheet(up?"in":"up",how);\n',' $("#sw").onclick=()=>authSheet(up?"in":"up",how);\n /*wlEye*/{const ey=$("#eye"),pw=$("#ap");if(ey&&pw)ey.onclick=()=>{const sh=pw.type==="password";pw.type=sh?"text":"password";ey.textContent=sh?"🙈":"👁️";ey.setAttribute("aria-label",sh?"Hide password":"Show password")}}\n')
s=s.replace('2026.10.30-C','2026.10.30-D')
open(P,"w",encoding="utf8").write(s);print("ok")
