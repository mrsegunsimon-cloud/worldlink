import sys
p=sys.argv[1] if len(sys.argv)>1 else '/mnt/user-data/outputs/worldlink2.html'
s=open(p,encoding='utf8').read()
if 'data-nt=' in s: print('already');sys.exit()
a='list.map(n=>`<div class="cm" style="${n.ts>seen?"background:var(--bg);border-radius:10px;padding:8px":""}">'
assert s.count(a)==1
s=s.replace(a,'list.map((n,ni)=>`<div class="cm" role="button" tabindex="0" data-nt="${ni}" style="cursor:pointer;${n.ts>seen?"background:var(--bg);border-radius:10px;padding:8px":""}">')
b=' me.ns=Date.now();badge();'
assert s.count(b)==1
c='''  $("#panel").querySelectorAll("[data-nt]").forEach(el=>{const go=()=>{const n=list[+el.dataset.nt];if(!n)return;const t=(n.text||"").toLowerCase();
   if(/your video/.test(t)){close();tab(1)}
   else if(/following/.test(t)){close();profile()}
   else if(/message/.test(t)){secFull=true;inbox()}
   else if(/going to/.test(t)){explore("events")}
   else{secFull=true;social()}};
   el.onclick=go;el.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();go()}}});
'''
s=s.replace(b,c+b)
open(p,'w',encoding='utf8').write(s);print('patched')
