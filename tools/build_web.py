"""Builds assets/web/index.html from the prototype html: adds the storage shim, the native login bridge, and real sign-up/login."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf8').read()

SHIM = r'''<script>
(function(){
 function load(){try{return JSON.parse(localStorage.getItem("wl_db")||"{}")}catch(e){return {}}}
 function save(d){try{localStorage.setItem("wl_db",JSON.stringify(d))}catch(e){}}
 var uid=null;try{uid=localStorage.getItem("wl_uid");if(!uid){uid="u"+Math.random().toString(36).slice(2,10);localStorage.setItem("wl_uid",uid)}}catch(e){uid="u0"}
 var pend={},nid=0;
 window.__wlReply=function(id,r){var p=pend[id];if(p){delete pend[id];p(r)}};
 window.WLN=function(op,data){return new Promise(function(res){
  if(!window.WLAuth){res({error:"native"});return}
  var id=++nid;pend[id]=res;
  WLAuth.postMessage(JSON.stringify(Object.assign({id:id,op:op},data||{})))})};
 window.__wlUser=null;
 var db={collection:function(n){return{
  get:async function(){var m=load()[n]||{};return{docs:Object.keys(m).map(function(k){return{id:k,data:function(){return JSON.parse(JSON.stringify(m[k]))}}})}},
  doc:function(id){return{
   get:async function(){var m=load()[n]||{};return{exists:id in m,data:function(){return JSON.parse(JSON.stringify(m[id]||{}))}}},
   set:async function(v){var d=load();(d[n]=d[n]||{})[id]=JSON.parse(JSON.stringify(v));save(d);return true}}}}}};
 window.claude={use:async function(k){
  if(k==="db")return db;
  if(k==="user")return{id:async function(){var r=await WLN("state");if(r&&r.user){window.__wlUser=r.user;return r.user.uid}return uid}};
  return null}};
})();
</script>'''
assert '<head>' in s
s = s.replace('<head>', '<head>' + SHIM, 1)

def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

rep('function authSheet(mode,how){', 'function authSheet0(mode,how){')
rep('<p class="note">Demo screens only. Real sign-up arrives with the Android app. Nothing you type here is sent anywhere.</p>',
    '<p class="note">${window.WLAuth?"Your account is stored securely online.":"Demo screens only. Real sign-up arrives with the Android app. Nothing you type here is sent anywhere."}</p>')
rep('if(fg)fg.onclick=e=>{e.preventDefault();$("#st").textContent="In the app we email you a link to reset your password."};',
    'if(fg)fg.onclick=e=>{e.preventDefault();if(window.WLAuth){const em=$("#ae").value.trim();if(!/^\\S+@\\S+\\.\\S+$/.test(em)){$("#st").textContent="Type your email above first, then tap Forgot password.";return}WLN("reset",{email:em}).then(r=>{$("#st").textContent=r.error?r.error:"Reset link sent to "+em+". Check your inbox."});return}$("#st").textContent="In the app we email you a link to reset your password."};')
rep('   st.textContent=up?"Looks good. In the app we would now email you a link to confirm this address.":"Looks good. In the app you would now be logged in."}',
    '''   if(window.WLAuth){st.textContent="Please wait...";WLN(up?"signup":"login",{email:e,password:pw}).then(function(r){if(r.error){st.textContent=r.error;return}window.__wlUser=r.user;me.uid=r.user.uid;if(me.name==="you")me.name=(r.user.name||"you");st.textContent=up?"Account created. A confirmation email was sent to "+e+".":"Welcome back!";setTimeout(function(){close();profile()},900)});return}
   st.textContent=up?"Looks good. In the app we would now email you a link to confirm this address.":"Looks good. In the app you would now be logged in."}''')
rep('function editProfile(){', '''function authSheet(mode,how){
 if(window.__wlUser){
  open(`<h2>Signed in</h2><p class="mute">${esc(window.__wlUser.email||"")}</p><p class="note">Your account is stored securely online.</p><button class="btn" id="lo">Log out</button><button class="btn ghost" id="x">Close</button>`);
  $("#lo").onclick=()=>{WLN("logout").then(()=>{window.__wlUser=null;me.uid=null;me.name="you";close();profile()})};
  return}
 authSheet0(mode,how)}
function editProfile(){''')

rep('   st.textContent="Looks good. In the app we would now text a 6-digit code to "+n+"."}',
r'''   if(window.WLAuth){st.textContent="Sending code...";WLN("phone_send",{phone:n}).then(function(r){if(r.error){st.textContent=r.error;return}
    var done=function(u){window.__wlUser=u;me.uid=u.uid;if(me.name==="you")me.name=u.name||"you";st.textContent="Welcome!";setTimeout(function(){close();profile()},700)};
    if(r.user){done(r.user);return}
    $("#ap2").insertAdjacentHTML("afterend",'<input class="in" id="ac" inputmode="numeric" maxlength="6" placeholder="6-digit code" aria-label="Code">');
    st.textContent="Code sent to "+n+". Enter it below.";
    var g=$("#go1");g.textContent="Verify code";
    g.onclick=function(){var c=$("#ac").value.trim();if(!/^\d{6}$/.test(c)){st.textContent="Enter the 6-digit code.";return}st.textContent="Checking...";WLN("phone_verify",{code:c}).then(function(v){if(v.error){st.textContent=v.error;return}done(v.user)})}});return}
   st.textContent="Looks good. In the app we would now text a 6-digit code to "+n+"."}''')

rep('font-weight:700;color:inherit">Sign in or create account</button>', 'font-weight:700;color:inherit">${window.__wlUser?"Signed in · Log out":"Sign in or create account"}</button>')

rep('</style>', 'nav{flex:none!important;min-height:fit-content}</style>') if s.count('</style>')==1 else None
if s.count('</style>')!=1:
    i=s.rfind('</style>'); s=s[:i]+'nav{flex:none!important}'+s[i:]

RESTORE = """<script>
window.addEventListener("load",function(){setTimeout(function(){
 WLN("state").then(function(r){if(!r||!r.user)return;
  window.__wlUser=r.user;me.uid=r.user.uid;
  if(me.name==="you")me.name=(r.user.name||"you");
  var on=document.querySelector("nav button.on");
  if(on&&/Profile/.test(on.textContent))profile();
 })},1500)});
</script>"""
i=s.rfind('</body>')
s=s[:i]+RESTORE+s[i:]

# Flutter's SafeArea already keeps the page clear of the status and navigation bars,
# so the page must not add its own safe-area padding on top (that doubled the gaps).
for side in ("top","bottom","left","right"):
    s = s.replace("env(safe-area-inset-%s,0px)" % side, "0px")
open(dst, 'w', encoding='utf8').write(s)
