import sys,re
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function capEditor' in s: print('already');sys.exit()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70])
    s=s.replace(a,b)
code=r'''
/* ===== Text on videos and photos: styles, colours, size, position (burned in when you post) ===== */
let CAP=null;
const CAPST=["Classic","Box","Highlight","Neon","Outline","Handwritten","Typewriter"],CAPCOL=["#ffffff","#FFD60A","#FF2D55","#2DE1FC","#34C759","#FF9F0A"];
function drawCap(x,W,H,c){
 const t=(c&&c.t||"").trim();if(!t)return;
 const st=c.st||0,fs=Math.max(12,Math.round(W*(c.sz||.07)));
 const fam=st===5?'"Brush Script MT","Segoe Script","Snell Roundhand",cursive':st===6?'"Courier New",Courier,monospace':'system-ui,"Segoe UI",Roboto,Arial,sans-serif';
 x.save();x.font=(st===5?"italic 700 ":"800 ")+fs+"px "+fam;x.textAlign="center";x.textBaseline="middle";x.lineJoin="round";
 const maxw=W*.84,src=st===4?t.toUpperCase():t,lines=[];
 src.split("\n").forEach(par=>{let cur="";par.split(" ").forEach(w=>{const tr=cur?cur+" "+w:w;if(x.measureText(tr).width>maxw&&cur){lines.push(cur);cur=w}else cur=tr});lines.push(cur)});
 const lh=fs*1.28,h=lines.length*lh,cy=Math.min(H-h/2-fs*.3,Math.max(h/2+fs*.3,H*(c.y==null?.8:c.y))),top=cy-h/2,col=c.c||"#fff";
 const box=(cx,cyy,w,hh,fill)=>{x.save();x.shadowColor="transparent";x.fillStyle=fill;const r=fs*.28,l=cx-w/2-fs*.35,tp=cyy-hh/2,ww=w+fs*.7;x.beginPath();if(x.roundRect)x.roundRect(l,tp,ww,hh,r);else x.rect(l,tp,ww,hh);x.fill();x.restore()};
 lines.forEach((ln,i)=>{
  const y=top+lh*i+lh/2,w=x.measureText(ln).width,cx=W/2;
  if(st===1)box(cx,y,w,lh*.96,"rgba(0,0,0,.68)");
  if(st===2)box(cx,y,w,lh*.96,col);
  if(st===6)box(cx,y,w,lh*.96,"rgba(0,0,0,.6)");
  x.shadowColor="transparent";x.shadowBlur=0;
  if(st===0||st===5){x.shadowColor="rgba(0,0,0,.85)";x.shadowBlur=fs*.22;x.shadowOffsetY=fs*.04;x.fillStyle=col;x.fillText(ln,cx,y)}
  else if(st===1||st===6){x.fillStyle=col;x.fillText(ln,cx,y)}
  else if(st===2){x.fillStyle="#111";x.fillText(ln,cx,y)}
  else if(st===3){x.shadowColor=col;x.shadowBlur=fs*.7;x.fillStyle="#fff";x.fillText(ln,cx,y);x.shadowBlur=fs*.3;x.fillStyle=col;x.globalAlpha=.55;x.fillText(ln,cx,y);x.globalAlpha=1}
  else if(st===4){x.strokeStyle="#000";x.lineWidth=fs*.2;x.strokeText(ln,cx,y);x.fillStyle=col;x.fillText(ln,cx,y)}
 });
 x.restore();
}
function capLayer(host,vw,vh,fit,cap){
 if(!host)return;let cv=host.querySelector("canvas.capl");
 if(!cv){cv=document.createElement("canvas");cv.className="capl";cv.setAttribute("aria-hidden","true");cv.style.cssText="position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none";host.appendChild(cv)}
 const r=host.getBoundingClientRect(),d=window.devicePixelRatio||1;cv.width=Math.max(1,Math.round(r.width*d));cv.height=Math.max(1,Math.round(r.height*d));
 const x=cv.getContext("2d");x.clearRect(0,0,cv.width,cv.height);
 if(!cap||!vw||!vh)return;
 const k=(fit==="cover"?Math.max:Math.min)(cv.width/vw,cv.height/vh);x.setTransform(k,0,0,k,(cv.width-vw*k)/2,(cv.height-vh*k)/2);drawCap(x,vw,vh,cap);
}
function capShow(media,host,fit){
 if(!CAP||!media)return;
 const go=()=>capLayer(host,media.videoWidth||media.naturalWidth,media.videoHeight||media.naturalHeight,fit,CAP);
 if(media.videoWidth||media.naturalWidth)go();
 media.addEventListener(media.tagName==="VIDEO"?"loadedmetadata":"load",go);
}
function capEditor(f,isImg,back){
 const url=URL.createObjectURL(f),c0=CAP||{t:"",st:0,c:CAPCOL[0],sz:.07,y:.8};let c=Object.assign({},c0);
 const media=isImg?`<img id="cem" src="${url}" alt="" style="width:100%;height:100%;object-fit:contain;display:block">`:`<video id="cem" src="${url}" autoplay loop muted playsinline style="width:100%;height:100%;object-fit:contain;display:block"></video>`;
 const chips=(attr,arr,sel,fn)=>arr.map((a,k)=>`<button ${attr}="${k}" style="flex:none;padding:7px 12px;border-radius:999px;font-weight:700;font-size:13px;background:${sel(k)?"#fff":"rgba(255,255,255,.18)"};color:${sel(k)?"#000":"#fff"}">${fn(a)}</button>`).join("");
 openFull(`<div style="height:100%;overflow-y:auto;background:#000;color:#fff;padding:14px 16px calc(16px + env(safe-area-inset-bottom))"><h2 style="margin:0 0 10px;font-size:17px;text-align:center">Add text</h2><div id="cst" style="position:relative;margin:0 auto;width:100%;height:42vh;background:#111;border-radius:12px;overflow:hidden">${media}</div><textarea id="ctx" class="in" rows="2" maxlength="140" placeholder="Type your text" aria-label="Text on your video" style="margin:10px 0 0;width:100%;box-sizing:border-box"></textarea><div style="font-size:13px;margin-top:8px">Style</div><div id="csty" style="display:flex;gap:6px;overflow-x:auto;padding:4px 0">${chips("data-cs",CAPST,k=>k===c.st,a=>a)}</div><div style="font-size:13px;margin-top:4px">Colour</div><div id="ccol" style="display:flex;gap:10px;padding:6px 0">${CAPCOL.map((k,i)=>`<button data-cc="${i}" aria-label="Colour ${i+1}" style="flex:none;width:34px;height:34px;border-radius:50%;background:${k};border:3px solid ${k===c.c?"#fff":"transparent"};outline:1px solid rgba(255,255,255,.4)"></button>`).join("")}</div><label style="display:block;font-size:13px">Size<input id="csz" type="range" min="4" max="14" step="0.5" value="${Math.round(c.sz*100*2)/2}" style="width:100%"></label><label style="display:block;font-size:13px">Up or down<input id="cy" type="range" min="8" max="92" value="${Math.round(c.y*100)}" style="width:100%"></label><div style="display:flex;gap:8px;margin-top:10px"><button class="btn ghost" id="cx" style="margin:0;flex:1;color:#fff;border-color:rgba(255,255,255,.5)">Back</button>${CAP?'<button class="btn ghost" id="crm" style="margin:0;flex:1;color:#fff;border-color:rgba(255,255,255,.5)">Remove</button>':""}<button class="btn" id="cdn" style="margin:0;flex:2">Done</button></div></div>`,true);
 const T=$("#ctx"),em=$("#cem"),stg=$("#cst");T.value=c.t;
 const size=()=>{const vw=em.videoWidth||em.naturalWidth,vh=em.videoHeight||em.naturalHeight;if(!vw)return;const w=Math.min(stg.parentNode.clientWidth-32,innerHeight*.42*vw/vh);stg.style.width=w+"px";stg.style.height=(w*vh/vw)+"px";stg.style.height=Math.round(w*vh/vw)+"px"};
 const draw=()=>{const vw=em.videoWidth||em.naturalWidth,vh=em.videoHeight||em.naturalHeight;capLayer(stg,vw,vh,"contain",c.t.trim()?c:null)};
 const ready=()=>{size();draw()};em.addEventListener(isImg?"load":"loadedmetadata",ready);if(em.videoWidth||em.naturalWidth)ready();
 T.oninput=()=>{c.t=T.value;draw()};
 $("#csty").onclick=e=>{const b=e.target.closest("[data-cs]");if(!b)return;c.st=+b.dataset.cs;$("#csty").querySelectorAll("button").forEach(x=>{const on=x===b;x.style.background=on?"#fff":"rgba(255,255,255,.18)";x.style.color=on?"#000":"#fff"});draw()};
 $("#ccol").onclick=e=>{const b=e.target.closest("[data-cc]");if(!b)return;c.c=CAPCOL[+b.dataset.cc];$("#ccol").querySelectorAll("button").forEach(x=>x.style.borderColor=x===b?"#fff":"transparent");draw()};
 $("#csz").oninput=e=>{c.sz=+e.target.value/100;draw()};
 $("#cy").oninput=e=>{c.y=+e.target.value/100;draw()};
 $("#cx").onclick=back;
 if($("#crm"))$("#crm").onclick=()=>{CAP=null;back()};
 $("#cdn").onclick=()=>{CAP=c.t.trim()?c:null;back()};
}
function captionVideo__PLACEHOLDER(){}
'''
# build captionVideo from filterVideo
i=s.find('function filterVideo(f,css,prog){');assert i>0
j=s.find('\nasync function postWithFilter',i);fv=s[i:j]
cv=fv.replace('function filterVideo(f,css,prog){','function captionVideo(f,css,cap,prog){',1)
assert 'if(!("filter" in x))return no(' in cv
cv=cv.replace('if(!("filter" in x))return no(','if(css&&!("filter" in x))return no(',1)
old='x.filter=css;x.drawImage(v,0,0,W,H);'
assert old in cv
cv=cv.replace(old,'x.filter=css||"none";x.drawImage(v,0,0,W,H);x.filter="none";if(cap)drawCap(x,W,H,cap);',1)
code=code.replace('function captionVideo__PLACEHOLDER(){}\n',cv+'\n')
rep('function postForm(f,note){',code+'function postForm(f,note){')
# postWithFilter
rep(' if(!PFX)return postVideo(f,cap);\n const css=PFX;',' if(!PFX&&!CAP)return postVideo(f,cap);\n const css=PFX,tx=CAP;')
rep('try{const nf=await filterVideo(f,css,(t,d)=>','try{const nf=await captionVideo(f,css,tx,(t,d)=>')
rep('PFX="";postFormPost(nf,cap)}','PFX="";CAP=null;postFormPost(nf,cap)}')
# postForm button + preview
rep('<button class="btn ghost" id="ved" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">','<button class="btn ghost" id="vcp" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">Aa ${CAP?"Change text":"Add text"}</button><button class="btn ghost" id="ved" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">')
rep(' $("#ved").onclick=()=>editVideo(f);',' $("#ved").onclick=()=>editVideo(f);\n $("#vcp").onclick=()=>capEditor(f,false,()=>postForm(f,note));{const pv=$("#pvv");if(pv)capShow(pv,pv.parentNode,"cover")}')
# photo
rep('<img id="pimg" src="${url}" alt="Your photo" style="width:100%;max-height:40vh;object-fit:contain;border-radius:12px;background:#000;filter:${PFX||"none"}">','<div id="phost" style="position:relative"><img id="pimg" src="${url}" alt="Your photo" style="width:100%;max-height:40vh;object-fit:contain;border-radius:12px;background:#000;filter:${PFX||"none"};display:block"></div>')
rep('<button class="btn ghost" id="pmp" style="margin-top:8px">','<button class="btn ghost" id="pcp" style="margin-top:8px">Aa ${CAP?"Change text":"Add text"}</button><button class="btn ghost" id="pmp" style="margin-top:8px">')
rep(' $("#bk").onclick=recorder;fxWire($("#pimg"));',' $("#bk").onclick=recorder;fxWire($("#pimg"));$("#pcp").onclick=()=>capEditor(f,true,()=>photoForm(f));capShow($("#pimg"),$("#phost"),"contain");')
rep('bakePhoto(f,PFX).then(g=>photoToVideo(g,sd,15,','bakePhoto(f,PFX).then(g=>{CAP=null;return g}).then(g=>photoToVideo(g,sd,15,')
rep('it.img=URL.createObjectURL(f);PFX="";','it.img=URL.createObjectURL(f);PFX="";CAP=null;')
# bakePhoto
rep(' if(!css)return ok(f);',' if(!css&&!CAP)return ok(f);')
rep('if(!("filter" in x))return ok(f);x.filter=css;x.drawImage(im,0,0,c.width,c.height);','if(css&&!("filter" in x))return ok(f);x.filter=css||"none";x.drawImage(im,0,0,c.width,c.height);x.filter="none";if(CAP)drawCap(x,c.width,c.height,CAP);')
rep(' PFX="";$("#gl").onclick=goLive;',' PFX="";CAP=null;$("#gl").onclick=goLive;')
open(p,'w',encoding='utf8').write(s);print('patched')
