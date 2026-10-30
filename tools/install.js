/* WorldLink: "Add to home screen" banner (website only) */
(function(){
 var dp=null,KEY="wl_inst_hide";
 function hid(){try{return localStorage.getItem(KEY)==="1"}catch(e){return false}}
 function hide(){try{localStorage.setItem(KEY,"1")}catch(e){}var b=document.getElementById("wlinst");if(b)b.remove()}
 function standalone(){return matchMedia("(display-mode: standalone)").matches||navigator.standalone===true}
 function show(txt,btn,fn){
  if(hid()||standalone()||document.getElementById("wlinst"))return;
  var b=document.createElement("div");b.id="wlinst";
  b.style.cssText="position:fixed;left:10px;right:10px;bottom:84px;z-index:50;background:#12307F;color:#fff;border-radius:16px;padding:12px 14px;display:flex;align-items:center;gap:10px;box-shadow:0 6px 24px rgba(0,0,0,.4);font:600 14px system-ui,sans-serif";
  b.innerHTML='<img src="/icon-192.png" width="40" height="40" alt="" style="border-radius:10px"><span style="flex:1">'+txt+'</span>'+(btn?'<button id="wlin1" style="background:#FE2C55;color:#fff;border:0;border-radius:10px;padding:9px 14px;font-weight:800">'+btn+'</button>':'')+'<button id="wlin2" aria-label="Close" style="background:none;border:0;color:#fff;font-size:20px;padding:4px 6px">✕</button>';
  document.body.appendChild(b);
  document.getElementById("wlin2").onclick=hide;
  var o=document.getElementById("wlin1");if(o)o.onclick=fn;
 }
 addEventListener("beforeinstallprompt",function(e){e.preventDefault();dp=e;setTimeout(function(){show("Add WorldLink to your home screen","Install",function(){dp.prompt();dp.userChoice.then(function(){dp=null;hide()})})},8000)});
 addEventListener("appinstalled",hide);
 var ua=navigator.userAgent,ios=/iphone|ipad|ipod/i.test(ua)&&!window.MSStream;
 if(ios)setTimeout(function(){show("To install: tap Share, then “Add to Home Screen”","",null)},10000);
})();
