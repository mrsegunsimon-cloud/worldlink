import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'function injectCards' in s: print('already');sys.exit()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70])
    s=s.replace(a,b)
code=r'''
/* ===== Home update cards: news, sports, social, market, events, music... shown between videos; tap opens that section ===== */
function homeCards(){
 const out=[],T=(x,n)=>{x=String(x==null?"":x);return x.length>n?x.slice(0,n-1)+"…":x};
 const go=fn=>()=>{secFull=true;FM=true;fn()};
 const add=(k,ic,lab,ph,h,sub,fn)=>out.push({k,ic,lab,ph,h,sub,fn:go(fn)});
 try{if(typeof WN!=="undefined"&&WN.length)add("news","📰","World news","w_world",T(WN[0][1],110),T(WN[0][3]||"Top story",60),()=>worldNews())}catch(e){}
 try{if(typeof NEWS!=="undefined"&&NEWS.length)add("sports","⚽","Sports","ev_sport",T(NEWS[0][1],110),T(NEWS[0][0]||"Latest scores, tables and news",60),()=>football("scores"))}catch(e){}
 try{const x=PS.filter(y=>y&&!y.del&&!blocked(y.o,y.u)&&(y.t||y.img))[0];add("social","💬","Social","ev_community",x?"@"+x.u+": "+T(x.t||"shared a photo",110):"See what your community is posting",x?"New in Social":"Posts, photos and comments",()=>social())}catch(e){}
 try{const x=LS.filter(y=>y&&!blocked(y.o,y.u))[0];add("market","🛍️","Market","m_market",x?T(x.t,90)+(x.p?" · "+x.p:""):"Buy and sell near you",x?"New in Market":"Products, services and jobs",()=>{MKV={v:"home"};market()})}catch(e){}
 try{const x=EV.slice().sort((a,b)=>String(a.dt).localeCompare(String(b.dt)))[0];add("events","🎉","Events","ev_music",x?T(x.t,90):"Find events near you",x?T((x.pl?x.pl+" · ":"")+(x.dt||""),70):"Join what is happening",()=>explore("events"))}catch(e){}
 try{const x=TR[0];add("music","🎵","Music","ev_music",x?T(x.t,80)+(x.u?" by @"+x.u:""):"Discover new music",x?"New in Entertainment":"Songs, music videos and artists",()=>music())}catch(e){}
 try{const x=GR[0];add("campus","🎓","Campus","c_hall",x?T(x.name,80):"Study groups and campus life",x?T(x.sub||"Study groups",70):"Find your classmates",()=>campus())}catch(e){}
 add("explore","🏖️","Explore","santorini","Beaches, places and trips near you","Find your next spot",()=>explore());
 add("learn","📚","Learn how","learning","Learn a new everyday skill","Short lessons with steps and videos",()=>learnHow());
 add("play","🎰","Play zone","pz","Free games and a daily bonus","Tap to play",()=>playZone());
 return out;
}
let HCGO={};
function injectCards(){
 try{
  const f=$("#feed"),t1=$("#t1");if(!f||!t1||!t1.classList.contains("on"))return;
  const clips=[...f.querySelectorAll(".clip[data-i]")];if(clips.length<2)return;
  const cards=homeCards();if(!cards.length)return;HCGO={};
  let n=0;
  for(let k=Math.min(1,clips.length-1);k<clips.length&&n<cards.length*2;k+=3){
   const c=cards[n%cards.length];n++;HCGO[c.k+n]=c.fn;
   const bg=(typeof PH!=="undefined"&&PH[c.ph])?`<img src="${PH[c.ph]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">`:"";
   const el=document.createElement("section");el.className="clip hc";el.setAttribute("role","button");el.tabIndex=0;el.dataset.hc=c.k+n;
   el.style.background="linear-gradient(165deg,#12307F,#FF7A1A)";
   el.innerHTML=`${bg}<div class="shade"></div><div style="position:absolute;left:18px;right:18px;bottom:120px;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.6)"><span style="display:inline-block;background:rgba(0,0,0,.45);padding:5px 12px;border-radius:999px;font-weight:700;font-size:13px">${c.ic} ${esc(c.lab)}</span><h2 style="font-size:25px;line-height:1.2;margin:12px 0 6px;color:#fff">${esc(c.h)}</h2><p style="margin:0;opacity:.92">${esc(c.sub)}</p><span style="display:inline-block;margin-top:14px;background:#FF7A1A;padding:11px 22px;border-radius:999px;font-weight:800;text-shadow:none">Open ${esc(c.lab)} →</span></div>`;
   clips[k].after(el);
  }
 }catch(e){}
}
$("#feed").addEventListener("click",e=>{const h=e.target.closest(".hc");if(h&&HCGO[h.dataset.hc])HCGO[h.dataset.hc]()});
$("#feed").addEventListener("keydown",e=>{if(e.key==="Enter"){const h=e.target.closest(".hc");if(h&&HCGO[h.dataset.hc])HCGO[h.dataset.hc]()}});
'''
rep('function tab(n){',code+'function tab(n){')
rep('</section>`}).join("");watch();','</section>`}).join("");injectCards();watch();')
rep('const clip=e.target.closest(".clip");if(!clip)return;','const clip=e.target.closest(".clip");if(!clip||clip.classList.contains("hc"))return;')
open(p,'w',encoding='utf8').write(s);print('patched')
