/* Home videos only play while the Home screen is showing and nothing is open on top of it */
(function(){
 function away(){
  var on=document.querySelector("nav button.on"),sh=document.getElementById("sheet");
  var notHome=on&&on.getAttribute("data-n")&&on.getAttribute("data-n")!=="Home";
  var open=sh&&sh.classList.contains("on");
  var vis=document.visibilityState==="hidden";
  return !!(notHome||open||vis)}
 function feed(v){return v&&v.closest&&v.closest("#feed")}
 var P=HTMLMediaElement.prototype.play;
 /* Sound: Home videos start WITH sound. If the browser refuses, start muted and unmute on the first tap. The person's own mute choice is remembered. */
 var userMuted=false;try{userMuted=localStorage.getItem("wl_muted")==="1"}catch(e){}
 var prog=false;
 function setM(v,m){v.__wlm=m;try{v.muted=m}catch(e){}}
 function pill(show){
  var p=document.getElementById("wlsnd");
  if(!show){if(p)p.remove();return}
  if(p)return;
  p=document.createElement("div");p.id="wlsnd";p.textContent="\uD83D\uDD0A Tap for sound";
  p.setAttribute("style","position:fixed;left:50%;transform:translateX(-50%);bottom:calc(var(--nh,64px) + 14px);z-index:60;background:rgba(0,0,0,.72);color:#fff;border-radius:999px;padding:10px 18px;font:700 14px system-ui,sans-serif;pointer-events:none");
  document.body.appendChild(p)}
 document.addEventListener("volumechange",function(e){var v=e.target;if(!feed(v)||v.__wlm===v.muted)return;v.__wlm=v.muted;userMuted=!!v.muted;try{localStorage.setItem("wl_muted",userMuted?"1":"0")}catch(_){ }if(!userMuted){window.__wlNeed=false;pill(false)}},true);
 function unlock(e){
  if(!window.__wlNeed)return;
  window.__wlNeed=false;pill(false);
  if(userMuted)return;
  document.querySelectorAll("#feed video").forEach(function(v){setM(v,false)});
  if(e&&e.type==="click"&&e.target&&e.target.closest&&e.target.closest(".clip")&&!e.target.closest("button,a,input")){e.stopImmediatePropagation();e.preventDefault()}}
 ["click","keydown"].forEach(function(t){document.addEventListener(t,unlock,true)});
 HTMLMediaElement.prototype.play=function(){
  var v=this;
  if(feed(v)&&away()){v.__wlp=1;return Promise.resolve()}
  if(!feed(v))return P.apply(v,arguments);
  setM(v,userMuted||!!window.__wlNeed);
  var pr=P.apply(v,arguments);
  if(pr&&pr.catch)return pr.catch(function(err){
   if(!v.muted){setM(v,true);window.__wlNeed=true;pill(true);return P.call(v)}
   throw err});
  return pr};
 var was=false;
 function tick(){
  var a=away();
  if(a){document.querySelectorAll("#feed video").forEach(function(v){if(!v.paused){v.__wlp=1;v.pause()}})}
  else if(was){
   var f=document.getElementById("feed"),best=null,bd=1e9;
   document.querySelectorAll("#feed .clip").forEach(function(c){var r=c.getBoundingClientRect(),d=Math.abs(r.top);if(r.height&&d<bd){bd=d;best=c}});
   if(best){var v=best.querySelector("video");if(v&&v.__wlp){v.__wlp=0;P.call(v).catch(function(){})}}}
  was=a}
 setInterval(tick,300);
 document.addEventListener("visibilitychange",tick);
 document.addEventListener("click",function(){setTimeout(tick,60)},true);
})();
