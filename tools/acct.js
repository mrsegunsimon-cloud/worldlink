/* Account deletion (Google Play + NDPA): asks for the password, wipes the person's own records, then removes the sign-in. */
(function(){
 var COLS=["videos","posts","stories","listings","events","groups","gchats","tracks","mvideos","reactions","campuslife","howto","gifts","series","episodes"];
 async function wipe(uid,say){
  var C=window.WLCloud;if(!C)return;
  var n=0;
  for(var i=0;i<COLS.length;i++){
   say("Removing your "+COLS[i]+"...");
   var seen={};
   for(var f of ["o","uid"]){
    var rows=[];try{rows=await C.byField(COLS[i],f,uid)}catch(e){}
    for(var r of rows){if(seen[r.id])continue;seen[r.id]=1;try{await C.del(COLS[i]+"/"+encodeURIComponent(r.id));n++}catch(e){}}}
  }
  say("Removing messages...");
  for(var f2 of ["a","b"]){var ds=[];try{ds=await C.byField("dms",f2,uid)}catch(e){}for(var d of ds){try{await C.del("dms/"+encodeURIComponent(d.id))}catch(e){}}}
  var ns=[];try{ns=await C.byField("notifs","to",uid)}catch(e){}
  for(var x of ns){try{await C.del("notifs/"+encodeURIComponent(x.id))}catch(e){}}
  try{var ids=await C.sub("data/users/"+encodeURIComponent(uid));for(var k of ids){try{await C.del("data/users/"+encodeURIComponent(uid)+"/"+encodeURIComponent(k))}catch(e){}}}catch(e){}
  try{await C.del("profiles/"+encodeURIComponent(uid))}catch(e){}
  try{await C.del("follows/"+encodeURIComponent(uid))}catch(e){}
  try{await C.fn("send-mail",{a:"wipe"})}catch(e){}
 }
 window.wlDeleteAccount=function(){
  var u=window.__wlUser;
  if(!u){open('<h2>Delete my account</h2><p class="mute">Log in first, then you can delete your account here.</p><button class="btn ghost" id="x">Close</button>');$("#x").onclick=close;return}
  var needPw=!!(u.email&&u.email.indexOf("@")>0);
  open('<h2>Delete my account</h2><p class="mute">This permanently removes your profile, videos, posts, series, messages, followers and saved settings. Coins and gifts cannot be refunded. This cannot be undone.</p>'+(needPw?'<input class="in" id="dpw" type="password" autocomplete="current-password" placeholder="Type your password to confirm" aria-label="Password">':'')+'<p class="note" id="dst"></p><button class="btn" id="dgo" style="background:#d62828;color:#fff">Delete everything</button><button class="btn ghost" id="x">Keep my account</button>');
  $("#x").onclick=close;
  $("#dgo").onclick=async function(){
   var st=$("#dst"),b=$("#dgo");
   var pw=needPw?$("#dpw").value:"";
   if(needPw&&!pw){st.textContent="Type your password first.";return}
   b.disabled=true;st.textContent="Checking...";
   var r=await WLN("reauth",{password:pw});
   if(r&&r.error){st.textContent=r.error;b.disabled=false;return}
   try{await wipe(u.uid,function(m){st.textContent=m})}catch(e){}
   st.textContent="Closing your account...";
   r=await WLN("delete");
   if(r&&r.error){st.textContent=r.error;b.disabled=false;return}
   try{await WLN("logout")}catch(e){}
   window.__wlUser=null;me.uid=null;me.name="you";
   open('<h2>Account deleted</h2><p class="mute">Your WorldLink account and data have been removed. Thank you for being here.</p><button class="btn" id="x">Close</button>');
   $("#x").onclick=function(){close();profile()};
  };
 };
})();
