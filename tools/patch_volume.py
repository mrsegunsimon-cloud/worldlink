import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlVolume" in s: print("already");sys.exit(0)
# 1. mixMusic takes options (original volume, music volume) and a missing song means "volume only"
a='function mixMusic(f,song,prog){'
assert a in s
s=s.replace(a,'/*wlVolume*/function mixMusic(f,song,prog,opt){opt=opt||{};const VO=opt.vo==null?1:opt.vo,VM=opt.vm==null?.6:opt.vm;',1)
a='ac.createMediaElementSource(v).connect(d);\n     const au=new Audio(song.url);au.crossOrigin="anonymous";au.loop=true;const g=ac.createGain();g.gain.value=.6;ac.createMediaElementSource(au).connect(g);g.connect(d);'
assert a in s
s=s.replace(a,'const vg=ac.createGain();vg.gain.value=VO;ac.createMediaElementSource(v).connect(vg);vg.connect(d);\n     const au=new Audio(song?song.url:"");if(song){au.crossOrigin="anonymous";au.loop=true;const g=ac.createGain();g.gain.value=VM;ac.createMediaElementSource(au).connect(g);g.connect(d)}',1)
a='rc.start();await au.play().catch(()=>{});await v.play()'
assert a in s
s=s.replace(a,'rc.start();if(song)await au.play().catch(()=>{});await v.play()',1)
# 2. editor: state, speaker button, panel, live preview
a='/*wlVFull*/'
assert a in s
s=s.replace(a,'''if(!VMIX||VMIX.f!==f)VMIX={f,vo:1,vm:.6,song:null};
  try{if(window.VAU){VAU.pause();VAU=null}}catch(e){}
  v.volume=VMIX.vo;
  if(VMIX.song){const au=new Audio(VMIX.song.url);au.loop=true;au.volume=VMIX.vm;window.VAU=au;v.addEventListener("play",()=>au.play().catch(()=>{}));v.addEventListener("pause",()=>au.pause());au.play().catch(()=>{})}
  {const sb=document.createElement("button");sb.id="vvl";sb.setAttribute("aria-label","Volume");sb.textContent=VMIX.vo===0&&(!VMIX.song||VMIX.vm===0)?"🔇":"🔊";sb.style.cssText="position:absolute;right:12px;top:18px;width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.16);color:#fff;font-size:22px;z-index:6";fr.parentNode.parentNode.appendChild(sb);
   const pn=document.createElement("div");pn.id="vvp";pn.style.cssText="display:none;position:absolute;right:12px;top:72px;width:min(300px,86%);background:rgba(10,10,12,.96);color:#fff;border-radius:16px;padding:14px 16px;z-index:7";
   const sl=(id,l,val,dis)=>`<label style="display:block;font-size:14px;font-weight:700;margin:6px 0 2px">${l} <span id="${id}n" style="font-weight:600;opacity:.8">${Math.round(val*100)}%</span><input id="${id}" type="range" min="0" max="100" value="${Math.round(val*100)}" ${dis?"disabled":""} style="width:100%"></label>`;
   pn.innerHTML=sl("vvo","Video sound",VMIX.vo,false)+(VMIX.song?sl("vvm","Music: "+esc(String(VMIX.song.name).slice(0,20)),VMIX.vm,false):'<p style="font-size:13px;margin:8px 0 0;opacity:.8">Tap ♪ Add sound to pick music, then adjust it here.</p>');
   sb.parentNode.appendChild(pn);
   sb.onclick=()=>{pn.style.display=pn.style.display==="none"?"block":"none"};
   const ic=()=>{sb.textContent=VMIX.vo===0&&(!VMIX.song||VMIX.vm===0)?"🔇":"🔊"};
   const vo=pn.querySelector("#vvo");vo.oninput=()=>{VMIX.vo=+vo.value/100;v.volume=VMIX.vo;pn.querySelector("#vvon").textContent=vo.value+"%";ic()};
   const vm=pn.querySelector("#vvm");if(vm)vm.oninput=()=>{VMIX.vm=+vm.value/100;if(window.VAU)VAU.volume=VMIX.vm;pn.querySelector("#vvmn").textContent=vm.value+"%";ic()}}
  /*wlVFull*/''',1)
# 3. choosing a song no longer mixes right away: it is remembered and mixed in the background when you post
a='''  const sd=SND;SND=null;
  open(`<h2>Adding music</h2>'''
assert a in s
i=s.find(a);j=s.find('\n });',i)
s=s[:i]+'''  const sd=SND;SND=null;VMIX=VMIX&&VMIX.f===f?VMIX:{f,vo:1,vm:.6,song:null};VMIX.song={url:sd.url,name:sd.name};vedit(f,"Music added: "+sd.name)'''+s[j:]
# 4. global + background job
s=s.replace('let BGB=false;','let BGB=false;var VMIX=null;',1)
a='VTRIM=null;\n try{document.querySelectorAll("#panel video")'
a2='if(VTRIM&&VTRIM.f===f)job.trim={st:VTRIM.st,en:VTRIM.en,sh:VTRIM.sh,pos:VTRIM.pos};VTRIM=null;'
assert a2 in s
s=s.replace(a2,a2+'if(VMIX&&VMIX.f===f&&(VMIX.song||VMIX.vo!==1))job.mix={song:VMIX.song,vo:VMIX.vo,vm:VMIX.vm};VMIX=null;try{window.VAU&&VAU.pause()}catch(e){}',1)
a='const burn=!!(job.css'
assert a in s
s=s.replace(a,'''  if(job.mix){const M=job.mix;bgRing(0,"","Adding sound");try{job.f=await mixMusic(job.f,M.song,(t,d)=>bgRing(d?.4*Math.min(1,t/d):0,"","Adding sound"),{vo:M.vo,vm:M.vm})}catch(e){}job.mix=null;job.burned=null;await jPut(job)}
'''+a,1)
open(P,"w",encoding="utf8").write(s);print("ok")
