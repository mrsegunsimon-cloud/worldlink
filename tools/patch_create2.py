"""Create 2. Usage: patch_create2.py in out"""
import sys,os
s=open(sys.argv[1],encoding='utf8').read()
if 'function postWithFilter' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]);s=s.replace(a,b)
js=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'create2.js'),encoding='utf8').read()
# replace old soundPicker with the new block
i=s.index('function soundPicker(cb){');j=s.index('function mixSound(src){')
s=s[:i]+js+'\n'+s[j:]
# create sheet: photo button
rep('<label class="btn ghost" style="cursor:pointer">Choose a video from phone<input id="cf" type="file" accept="video/*" hidden></label>',
    '<label class="btn ghost" style="cursor:pointer">Choose a video from phone<input id="cf" type="file" accept="video/*" hidden></label><label class="btn ghost" style="cursor:pointer">📷 Choose a photo from phone<input id="cpi" type="file" accept="image/*" hidden></label>')
rep(' $("#gl").onclick=goLive;\n $("#cr").onclick=recorder;',' PFX="";$("#gl").onclick=goLive;\n $("#cr").onclick=recorder;\n $("#cpi").onchange=e=>{if(e.target.files[0])photoForm(e.target.files[0])};')
# photoForm
rep('<img src="${url}" alt="Your photo" style="width:100%;max-height:44vh;object-fit:contain;border-radius:12px;background:#000">','<img id="pimg" src="${url}" alt="Your photo" style="width:100%;max-height:40vh;object-fit:contain;border-radius:12px;background:#000;filter:${PFX||"none"}">${fxStrip()}')
rep('>♪ Post as a video with music</button>','>🎬 Turn into a video with music</button>')
rep(' $("#bk").onclick=recorder;\n $("#pmp").onclick=()=>soundPicker(()=>{',' $("#bk").onclick=recorder;fxWire($("#pimg"));\n $("#pmp").onclick=()=>soundPicker(()=>{')
rep('photoToVideo(f,sd,15,p=>{const b=$("#mb");if(b)b.style.width=Math.round(p*100)+"%"}).then(vf=>','bakePhoto(f,PFX).then(g=>photoToVideo(g,sd,15,p=>{const b=$("#mb");if(b)b.style.width=Math.round(p*100)+"%"})).then(vf=>')
rep('l:[],cm:[],img:url};\n  try{','l:[],cm:[],img:url};f=await bakePhoto(f,PFX);it.img=URL.createObjectURL(f);PFX="";\n  try{')
rep('  PS.unshift(it);social();\n };','  PS.unshift(it);notify("*","posted a photo in Social"+(it.t?": "+it.t.slice(0,40):""));social();\n };')
rep('PS.unshift(it);$("#pt").value="";social();','PS.unshift(it);notify("*","posted in Social"+(t?": "+t.slice(0,40):" a photo"));$("#pt").value="";social();')
# postForm
rep('<button class="btn ghost" id="pmu" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">','${fxStrip()}<button class="btn ghost" id="pmu" style="margin:0;color:#fff;border-color:rgba(255,255,255,.5)">')
rep(' $("#bk").onclick=create;\n $("#go").onclick=()=>postVideo(f,$("#cp").value.trim());',' $("#bk").onclick=create;{const pv=$("#pvv");if(pv)pv.style.filter=PFX;fxWire(pv)}\n $("#go").onclick=()=>postWithFilter(f,$("#cp").value.trim());')
# home
rep('if(b.dataset.n==="Home")return close();','if(b.dataset.n==="Home"){close();const fd=$("#feed");if(fd)fd.scrollTo({top:0,behavior:"smooth"});return}')
# notifications
rep('.filter(n=>n&&n.to===id)','.filter(n=>n&&(n.to===id||(n.to==="*"&&n.from!==me.name&&Date.now()-n.ts<12096e5)))')
open(sys.argv[2],'w',encoding='utf8').write(s)
