import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlMailSend" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)>=1,a[:70]
    s=s.replace(a,b,1)
# 1. after sign-in is known, save the email privately and send the welcome email once
rep('try{const U=await claude.use("user");if(U){me.uid=await U.id();',
 'try{const U=await claude.use("user");if(U){me.uid=await U.id();/*wlMailHello*/try{if(window.WLCloud&&WLCloud.fn&&window.__wlUser&&!localStorage.getItem("wl-mail-"+me.uid)){WLCloud.fn("send-mail",{a:"hello",name:me.name}).then(r=>{if(r&&r.ok)try{localStorage.setItem("wl-mail-"+me.uid,"1")}catch(e){}})}}catch(e){}')
# 2. moderator screen: email everyone
rep('open(`<h2>Payout requests</h2>','open(`<button class="btn" id="wlem" style="margin:0 0 12px">✉️ Email all users</button><h2>Payout requests</h2>')
rep(' const rid=r=>r.id||"r"+r.ts;',' const rid=r=>r.id||"r"+r.ts;\n {const e=$("#wlem");if(e)e.onclick=wlMailScreen}')
rep('async function modScreen(){','''/*wlMailSend*/function wlMailScreen(){
 open(`<h2>✉️ Email all users</h2><p class="mute">Sent from hello@worldlink.app to everyone who has an email saved and has not unsubscribed. Every message has an unsubscribe link. Free limit: 100 emails a day.</p><input class="in" id="wls" maxlength="150" placeholder="Subject" aria-label="Subject"><textarea class="in" id="wlt" rows="8" maxlength="5000" placeholder="Write your message. Leave a blank line between paragraphs." aria-label="Message" style="resize:vertical"></textarea><p class="note" id="wln"></p><button class="btn ghost" id="wltest">Send a test to me</button><button class="btn" id="wlgo">Send to everyone</button><button class="btn ghost" id="wlb">Back</button>`);
 $("#wlb").onclick=modScreen;
 const run=async(a)=>{
  const sub=$("#wls").value.trim(),tx=$("#wlt").value.trim(),n=$("#wln");
  if(!sub||!tx){n.textContent="Write a subject and a message first.";return}
  if(a==="broadcast"&&!confirm("Send this email to everyone now?"))return;
  $("#wltest").disabled=$("#wlgo").disabled=true;n.textContent="Sending...";
  let r=null;try{r=await WLCloud.fn("send-mail",{a,subject:sub,text:tx})}catch(e){}
  $("#wltest").disabled=$("#wlgo").disabled=false;
  n.textContent=r&&r.ok?(a==="test"?"Test sent. Check your inbox and spam folder.":"Sent to "+r.sent+" of "+r.total+" people."):"Not sent: "+((r&&r.why)||"the email service did not answer.");
 };
 $("#wltest").onclick=()=>run("test");$("#wlgo").onclick=()=>run("broadcast");
}
async function modScreen(){''')
open(P,"w",encoding="utf8").write(s)
print("ok")
