import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlLegal1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('${row("md","🛡️","Moderator tools")}${row("lg","🌐","Language")}${row("th","◐","Theme")}</div></div>`;',
    '${row("md","🛡️","Moderator tools")}${row("lg","🌐","Language")}${row("th","◐","Theme")}</div><div class="pmg">${row("pp","📄","Privacy policy")}${row("tc","📜","Terms of use")}${row("da","🗑️","Delete my account")}</div></div>`;')
rep('lg:langSheet,th:theme};','lg:langSheet,th:theme,pp:()=>wlLegal("privacy"),tc:()=>wlLegal("terms"),da:()=>{if(window.wlDeleteAccount)wlDeleteAccount();else window.open("https://worldlink.app/delete-account.html","_blank")}};')
rep('function profMenu(){','/*wlLegal1*/\nfunction wlLegal(k){const u="https://worldlink.app/"+k+".html";if(typeof openUrl==="function")openUrl(u);else window.open(u,"_blank","noopener")}\nfunction profMenu(){')
open(P,"w",encoding="utf8").write(s);print("ok")
