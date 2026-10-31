import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlMailMedia" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70])
    s=s.replace(a,b)
# picker + in-app notice option in the moderator email screen
rep('<p class="note" id="wln"></p><button class="btn ghost" id="wltest">',
    '<label class="mute" style="display:block;margin:6px 0 4px">Picture or video (optional, up to 20 MB)</label><input class="in" id="wlf" type="file" accept="image/*,video/*" aria-label="Attach a picture or video"><label style="display:flex;gap:8px;align-items:center;margin:8px 0"><input type="checkbox" id="wlnt" checked> <span>Also show as a notice in the app (Activity)</span></label><p class="note" id="wln"></p><button class="btn ghost" id="wltest">')
rep('''  $("#wltest").disabled=$("#wlgo").disabled=true;n.textContent="Sending...";
  let r=null;try{r=await WLCloud.fn("send-mail",{a,subject:sub,text:tx})}catch(e){}''',
'''  $("#wltest").disabled=$("#wlgo").disabled=true;n.textContent="Sending...";
  /*wlMailMedia*/let img="",vid="";const f=$("#wlf").files[0];
  if(f){
   if(f.size>20*1048576){n.textContent="That file is over 20 MB.";$("#wltest").disabled=$("#wlgo").disabled=false;return}
   n.textContent="Uploading the file...";
   try{const A=await claude.use("assets"),u=(await A.upload(f)).url;if(f.type.startsWith("video"))vid=u;else img=u}catch(e){}
   if(!img&&!vid){n.textContent="The file did not upload. Try again.";$("#wltest").disabled=$("#wlgo").disabled=false;return}
   n.textContent="Sending...";
  }
  let r=null;try{r=await WLCloud.fn("send-mail",{a,subject:sub,text:tx,img,vid})}catch(e){}
  if(a==="broadcast"&&r&&r.ok&&$("#wlnt").checked){try{const D=await claude.use("db"),id="n"+Date.now()+"a";await D.collection("notifs").doc(id).set({id,to:"*",from:me.name,text:"📢 "+sub+": "+tx.slice(0,300),ts:Date.now(),img,vid})}catch(e){}}''')
# tapping an announcement with a picture or video opens it
rep('const go=()=>{const n=all[+el.dataset.nt];if(!n)return;const t=(n.text||"").toLowerCase();',
    'const go=()=>{const n=all[+el.dataset.nt];if(!n)return;const t=(n.text||"").toLowerCase();if(n.img||n.vid){open(`<h2>📢 Announcement</h2><p>${esc(n.text||"")}</p>${n.vid?`<video src="${esc(n.vid)}" controls playsinline preload="metadata" style="width:100%;border-radius:12px;background:#000"></video>`:`<img src="${esc(n.img)}" alt="" style="width:100%;border-radius:12px">`}<button class="btn ghost" id="x">Close</button>`);return}')
open(P,"w",encoding="utf8").write(s)
print("ok")
