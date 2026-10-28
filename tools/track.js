/* Visitor counter (GoatCounter, no cookies, no personal data). One count per visit, plus one when someone comes back after 30 minutes. */
(function(){
 var C="https://worldlink.goatcounter.com/count",last=0;
 function hit(path,title){
  try{
   if(location.protocol==="file:")return;
   var q=new URLSearchParams(location.search),ref=q.get("ref")?"https://invite.worldlink/"+q.get("ref"):document.referrer;
   var u=C+"?p="+encodeURIComponent(path)+"&t="+encodeURIComponent(title||"WorldLink")+"&r="+encodeURIComponent(ref||"")+"&s="+screen.width+","+screen.height+",1&rnd="+Math.random().toString(36).slice(2);
   new Image().src=u;last=Date.now();
  }catch(e){}}
 hit(window.__wlWeb?"/web":"/app","WorldLink");
 document.addEventListener("visibilitychange",function(){if(document.visibilityState==="visible"&&Date.now()-last>1800000)hit(window.__wlWeb?"/web":"/app","WorldLink")});
 window.wlTrack=hit;
})();
