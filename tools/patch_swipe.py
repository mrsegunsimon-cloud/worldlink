import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlSwipe" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert a in s,a[:70]
    s=s.replace(a,b,1)
HELP=r'''/* wlSwipe: slide a row left to archive or delete it (hidden on this phone only) */
let INB_ARCH=false;
const wlHK=()=>"wl_hid_"+(me.uid||"x");
function wlHS(){try{return JSON.parse(localStorage.getItem(wlHK())||"{}")}catch(e){return{}}}
function wlHSave(o){try{localStorage.setItem(wlHK(),JSON.stringify(o))}catch(e){}}
const wlLast=d=>d.m&&d.m.length?(d.m[d.m.length-1].ts||0):0;
function wlVis(d){const h=wlHS()["dm:"+d.id];if(!h)return 0;if(wlLast(d)>h.t)return 0;return h.a?2:1}
const wlNH=n=>!!(n&&n.id&&wlHS()["nf:"+n.id]);
function swipeRows(root,sel,actsOf,onAct){
 root.querySelectorAll(sel).forEach(el=>{
  const acts=actsOf(el);if(!acts||!acts.length)return;
  const W=acts.length*84,w=document.createElement("div");w.style.cssText="position:relative;overflow:hidden";
  el.parentNode.insertBefore(w,el);
  const ab=document.createElement("div");ab.style.cssText="position:absolute;right:0;top:0;bottom:0;display:flex;opacity:0";
  acts.forEach(a=>{const b=document.createElement("button");b.type="button";b.textContent=a.l;b.style.cssText="width:84px;color:#fff;font-weight:800;font-size:15px;background:"+a.c;b.onclick=e=>{e.stopPropagation();onAct(a.k,el)};ab.appendChild(b)});
  w.appendChild(ab);w.appendChild(el);
  el.style.position="relative";el.style.touchAction="pan-y";if(!el.style.background&&!el.style.backgroundColor)el.style.background="var(--card)";
  let x0=0,y0=0,dx=0,mode=0;
  el.addEventListener("touchstart",e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;dx=0;mode=0;el.style.transition="none"},{passive:true});
  el.addEventListener("touchmove",e=>{const mx=e.touches[0].clientX-x0,my=e.touches[0].clientY-y0;if(!mode){if(Math.abs(mx)>10&&Math.abs(mx)>Math.abs(my))mode=1;else if(Math.abs(my)>10)mode=2}if(mode!==1)return;dx=Math.max(-W,Math.min(0,mx+(el._o?-W:0)));el.style.transform="translateX("+dx+"px)";ab.style.opacity=dx<0?1:0},{passive:true});
  el.addEventListener("touchend",()=>{el.style.transition="transform .18s";if(mode===1){const o=dx<-W/2;el._o=o;el.style.transform=o?"translateX("+(-W)+"px)":"";if(!o)setTimeout(()=>{ab.style.opacity=0},190);el._sw=Date.now()}},{passive:true});
  el.addEventListener("click",e=>{if(Date.now()-(el._sw||0)<400||el._o){e.stopImmediatePropagation();e.preventDefault();if(el._o&&Date.now()-(el._sw||0)>=400){el._o=false;el.style.transform="";setTimeout(()=>{ab.style.opacity=0},190)}}},true);
 });
}
'''
rep('function inbox(){\n',HELP+'function inbox(){\n')
# DM row builder (also shows voice messages)
rep(' const nf=parseInt($("#bd").textContent)||0;\n const seen=new Set(DMS.map(d=>dmOther(d).n));\n',
 ' const nf=parseInt($("#bd").textContent)||0;\n const seen=new Set(DMS.map(d=>dmOther(d).n));\n const DMROW=d=>{const o=dmOther(d);return row(`data-dm="${esc(d.id)}"`,av(o.n||"?"),o.n||"user",d.m.length?(x=>x.t?x.t.slice(0,50):x.au?"🎤 Voice message":x.img?"📷 Photo":"🎥 Video")(d.m[d.m.length-1]):"Say hi to "+(o.n||"them"),"")};\n')
OLD='${DMS.map(d=>{const o=dmOther(d);return row(`data-dm="${esc(d.id)}"`,av(o.n||"?"),o.n||"user",d.m.length?(x=>x.t?x.t.slice(0,50):x.img?"📷 Photo":"🎥 Video")(d.m[d.m.length-1]):"Say hi to "+(o.n||"them"),"")}).join("")}'
NEW='${DMS.filter(d=>wlVis(d)===0).map(DMROW).join("")}${(()=>{const ar=DMS.filter(d=>wlVis(d)===2);if(!ar.length)return"";return row(\'id="arc"\',circ("#6B7280","🗄️"),"Archived",ar.length+(ar.length>1?" chats":" chat"),INB_ARCH?"▲":"▼")+(INB_ARCH?ar.map(DMROW).join(""):"")})()}'
rep(OLD,NEW)
rep(' $("#panel").querySelectorAll("[data-dm]").forEach(b=>b.onclick=()=>dmOpenById(b.dataset.dm));\n}',
 ''' $("#panel").querySelectorAll("[data-dm]").forEach(b=>b.onclick=()=>dmOpenById(b.dataset.dm));
 const arc=$("#arc");if(arc)arc.onclick=()=>{INB_ARCH=!INB_ARCH;inbox()};
 swipeRows($("#panel"),"[data-dm]",el=>{const d=DMS.find(x=>x.id===el.dataset.dm);if(!d)return null;return wlVis(d)===2?[{k:"un",l:"Unarchive",c:"#6B7280"},{k:"del",l:"Delete",c:"#E5233A"}]:[{k:"arc",l:"Archive",c:"#6B7280"},{k:"del",l:"Delete",c:"#E5233A"}]},(k,el)=>{const d=DMS.find(x=>x.id===el.dataset.dm);if(!d)return;const h=wlHS();if(k==="un")delete h["dm:"+d.id];else h["dm:"+d.id]={t:wlLast(d)||Date.now(),a:k==="arc"?1:0};wlHSave(h);inbox()});
}''')
# notifications: hide deleted ones everywhere (also the red badge)
rep('NF=rows.filter(n=>n&&(n.to===id||','NF=rows.filter(n=>!wlNH(n)).filter(n=>n&&(n.to===id||')
rep(' P.querySelectorAll("[data-pn]").forEach(el=>el.onclick=e=>{e.stopPropagation();personSheet(el.dataset.pn,el.dataset.pu||"",()=>{notifs(ACT_TAB)})});\n',
 ' P.querySelectorAll("[data-pn]").forEach(el=>el.onclick=e=>{e.stopPropagation();personSheet(el.dataset.pn,el.dataset.pu||"",()=>{notifs(ACT_TAB)})});\n swipeRows(P,"[data-nt]",()=>[{k:"del",l:"Delete",c:"#E5233A"}],(k,el)=>{const n=all[+el.dataset.nt];if(!n)return;if(n.id){const h=wlHS();h["nf:"+n.id]=1;wlHSave(h)}NF=NF.filter(x=>x!==n);badge();actDraw(seen)});\n')
s=s.replace('2026.10.30-D','2026.10.30-E')
open(P,"w",encoding="utf8").write(s);print("ok")
