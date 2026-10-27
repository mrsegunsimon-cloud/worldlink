/* ===== Sign-in gate: anyone can watch the Home videos, everything else needs an account ===== */
(function(){
 if(!window.__wlGate)return;
 var SEL='#menu,#bell,#srch,#t2,#t0,nav button:not([data-n="Home"]),#feed button[data-a],#feed .rail .av';
 function gateSheet(){
  open('<h2>Create a free account</h2><p class="mute">You can watch videos without an account. To like, comment, post, chat, search, shop or use any other part of WorldLink, please sign up or log in.</p><button class="btn" id="gu">Create account</button><button class="btn ghost" id="gi">I already have an account</button><button class="btn ghost" id="x">Keep watching</button>');
  $("#gu").onclick=function(){authSheet("up")};
  $("#gi").onclick=function(){authSheet("in")};
 }
 document.addEventListener("click",function(e){
  if(window.__wlUser)return;
  var t=e.target.closest&&e.target.closest(SEL);if(!t)return;
  e.preventDefault();e.stopPropagation();e.stopImmediatePropagation();gateSheet();
 },true);
 /* If the account is removed or the user logs out while a panel is open, close everything private. */
 window.__wlGateCheck=function(){if(!window.__wlUser){try{close()}catch(e){}}};
})();
