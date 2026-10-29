import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlModText" in s: print("already");sys.exit(0)
NEW=r'''/* wlModText: house rules filter. Blocks abuse, sexual words, hate and extremist calls before anything is saved. */
(function(){
 const L={
  abuse:"fuck fucker fucking motherfucker shit bullshit bitch bastard asshole dickhead cunt whore slut prostitute idiot stupid moron imbecile dumbass fool mumu ashawo oloshi olosho ogbeni ode ọmọ aja yeye mad dog pig".split(" ").filter(w=>!["fool","mad","dog","pig","stupid","idiot","moron","ode","yeye","ogbeni","mumu"].includes(w)),
  sexual:"porn porno pornography nude nudes naked sex tape blowjob handjob boobs tits pussy dick cock penis vagina anal orgasm masturbate masturbation horny xxx hentai nsfw erotic stripper escort onlyfans".split(" ").filter(w=>w!=="sex"&&w!=="escort"),
  hate:"nigger nigga faggot retard kike chink spic tranny coon".split(" "),
  extreme:["kill the infidels","death to infidels","kill all christians","kill all muslims","kill all jews","kill the kafir","holy war against","convert or die","join isis","isis is great","join boko haram","boko haram is good","behead them","suicide bomb","blow up the church","blow up the mosque","jihad against","crusade against","burn the church","burn the mosque","sharia or death","death to all"]
 };
 const norm=t=>(" "+String(t||"").toLowerCase().replace(/[@4]/g,"a").replace(/[3]/g,"e").replace(/[1!|]/g,"i").replace(/[0]/g,"o").replace(/[$5]/g,"s").replace(/[^a-z\s]/g," ").replace(/(.)\1{2,}/g,"$1$1").replace(/\s+/g," ")+" ");
 const RX={};for(const k in L){RX[k]=new RegExp("\\b("+L[k].map(w=>w.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")).join("|")+")\\b","i")}
 window.modScan=function(n,v){
  if(!v||typeof v!=="object")return null;
  if(["credits","reports","calls","notifs","follows","reactions","data"].some(x=>n.indexOf(x)===0))return null;
  const t=[];
  ["c","t","text","title","d","n","name","bio","about","desc","q","msg","cap"].forEach(k=>{if(typeof v[k]==="string")t.push(v[k])});
  ["m","cm","sc"].forEach(k=>{const a=v[k];if(Array.isArray(a)&&a.length){const x=a[a.length-1];if(x&&typeof x==="object"){if(typeof x.t==="string")t.push(x.t);if(typeof x.c==="string")t.push(x.c);if(typeof x.text==="string")t.push(x.text)}else if(typeof x==="string")t.push(x)}});
  const z=norm(t.join(" . "));
  for(const k in RX){if(RX[k].test(z))return k}
  const sq=z.replace(/ +/g," ");for(const p of L.extreme){if(sq.indexOf(" "+p+" ")>=0||sq.indexOf(p)>=0)return "extreme"}
  return null};
 window.modBlock=function(k){
  const why={abuse:"abusive or insulting words",sexual:"sexual or nude content",hate:"hateful words",extreme:"calls for violence or extreme religious hatred"}[k]||"words that break our rules";
  let el=document.getElementById("modtoast");if(!el){el=document.createElement("div");el.id="modtoast";el.style.cssText="position:fixed;left:14px;right:14px;top:70px;z-index:200;background:#7f1d1d;color:#fff;padding:14px 16px;border-radius:14px;font-size:15px;line-height:1.35;box-shadow:0 6px 24px rgba(0,0,0,.4)";document.body.appendChild(el)}
  el.innerHTML="<b>Not posted.</b> It has "+why+". WorldLink does not allow abuse, nudity, vile language or extreme religion. Please change it and try again.";el.style.display="block";clearTimeout(el.__t);el.__t=setTimeout(()=>{el.style.display="none"},6500)};
 try{const o=claude.use.bind(claude);
  const wrapDoc=(n,d)=>new Proxy(d,{get:(t,p)=>p==="set"?async v=>{const w=modScan(n,v);if(w){modBlock(w);throw new Error("blocked by house rules")}return t.set(v)}:(typeof t[p]==="function"?t[p].bind(t):t[p])});
  const wrapCol=(c,n)=>new Proxy(c,{get:(t,p)=>p==="doc"?id=>wrapDoc(n,t.doc(id)):(typeof t[p]==="function"?t[p].bind(t):t[p])});
  claude.use=async function(k){const r=await o(k);if(k!=="db"||!r||r.__wm)return r;return new Proxy(r,{get:(t,p)=>p==="__wm"?true:p==="collection"?n=>wrapCol(t.collection(n),n):(typeof t[p]==="function"?t[p].bind(t):t[p])})}
 }catch(e){}
})();
'''
a="let NF=[];"
assert a in s
s=s.replace(a,NEW+a,1)
open(P,"w",encoding="utf8").write(s);print("ok")
