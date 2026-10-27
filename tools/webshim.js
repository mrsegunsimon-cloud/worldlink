/* Web version bridge: same WLAuth messages as the Android app, answered with the Firebase web SDK and the browser. */
(function(){
 if(window.WLAuth)return;
 if(window.top!==window.self){try{window.top.location=window.self.location}catch(e){document.documentElement.innerHTML=""}}
 var CFG=__FIREBASE_CONFIG__;
 var V="10.14.1",fb=null,fails=0,lockUntil=0;
 function lib(){if(!fb)fb=Promise.all([import("https://www.gstatic.com/firebasejs/"+V+"/firebase-app.js"),import("https://www.gstatic.com/firebasejs/"+V+"/firebase-auth.js")]).then(function(m){var app=m[0].initializeApp(CFG);return{A:m[1],auth:m[1].getAuth(app)}});return fb}
 function usr(u){return u?{uid:u.uid,email:u.email||u.phoneNumber||"",name:u.displayName||((u.email||"").split("@")[0])||"you"}:null}
 function human(e){var c=(e&&e.code)||"";
  if(c==="auth/email-already-in-use")return"That email already has an account. Log in instead.";
  if(c==="auth/invalid-credential"||c==="auth/wrong-password"||c==="auth/user-not-found"||c==="auth/invalid-login-credentials")return"Wrong email or password.";
  if(c==="auth/weak-password")return"Choose a stronger password (at least 8 characters).";
  if(c==="auth/invalid-email")return"That email address does not look right.";
  if(c==="auth/too-many-requests")return"Too many tries. Please wait a few minutes and try again.";
  if(c==="auth/network-request-failed")return"No internet connection. Check it and try again.";
  if(c==="auth/operation-not-allowed")return"Email sign-up is not switched on yet.";
  if(c==="auth/unauthorized-domain")return"This website address is not allowed in Firebase yet. The owner must add it under Authentication, Settings, Authorized domains.";
  if(c==="auth/api-key-not-valid.-please-pass-a-valid-api-key."||c==="auth/invalid-api-key"||c==="auth/requests-from-referer-"||/referer|blocked/i.test(String(e&&e.message)))return"This website is not allowed to use the sign-in service yet. The owner must allow it in Firebase.";
  return"Could not complete that ("+(c||"error")+").";}
 function pw(p){return typeof p==="string"&&p.length>=8&&p.length<=128}
 function fetchT(url,sec){var c=new AbortController(),t=setTimeout(function(){c.abort()},(sec||25)*1000);return fetch(url,{signal:c.signal}).then(function(r){clearTimeout(t);if(!r.ok)throw new Error("HTTP "+r.status);return r.text()})}
 async function handle(m){
  switch(m.op){
   case"state":{var l=await lib();await l.auth.authStateReady();return{user:usr(l.auth.currentUser)}}
   case"signup":{if(!pw(m.password))return{error:"Choose a password of at least 8 characters."};var l=await lib();var c=await l.A.createUserWithEmailAndPassword(l.auth,String(m.email).trim(),m.password);try{await l.A.sendEmailVerification(c.user)}catch(e){}return{user:usr(c.user)}}
   case"login":{if(Date.now()<lockUntil)return{error:"Too many wrong tries. Wait a minute and try again."};var l=await lib();try{var c=await l.A.signInWithEmailAndPassword(l.auth,String(m.email).trim(),m.password);fails=0;return{user:usr(c.user)}}catch(e){if(++fails>=5){lockUntil=Date.now()+60000;fails=0}throw e}}
   case"reset":{var l=await lib();await l.A.sendPasswordResetEmail(l.auth,String(m.email).trim());return{ok:true}}
   case"logout":{var l=await lib();await l.A.signOut(l.auth);return{ok:true}}
   case"phone_send":case"phone_verify":return{error:"Phone sign-in is only in the Android app for now. Please use your email."};
   case"location":return new Promise(function(ok){if(!navigator.geolocation)return ok({error:"Location is not available here."});navigator.geolocation.getCurrentPosition(function(p){ok({lat:p.coords.latitude,lng:p.coords.longitude})},function(){ok({error:"Location was not allowed."})},{timeout:15000})});
   case"open":{if(/^https?:\/\//i.test(m.url))window.open(m.url,"_blank","noopener,noreferrer");return{ok:true}}
   case"get":{try{if(!/^https:\/\//i.test(m.url))return{error:"Blocked."};return{body:await fetchT(m.url,m.timeout)}}catch(e){return{error:"The service did not answer."}}}
  }
  return{error:"Not supported here."};
 }
 window.WLAuth={postMessage:function(s){var m;try{m=JSON.parse(s)}catch(e){return}
  handle(m).then(function(r){window.__wlReply(m.id,r)},function(e){window.__wlReply(m.id,{error:human(e)})})}};
})();
