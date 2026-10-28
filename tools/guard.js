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
 HTMLMediaElement.prototype.play=function(){
  if(feed(this)&&away()){this.__wlp=1;return Promise.resolve()}
  return P.apply(this,arguments)};
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
