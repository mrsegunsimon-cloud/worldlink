"""Story screen plays a short preview video by itself. Usage: patch_prev.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'const vd=VID[key]' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('const tl=n[1],em=key&&key[0]==="w"?worldEmoji(tl,n[0]):sportEmoji(n[0]+" "+tl),lab=key&&key[0]==="w"?"":n[0];\n open(`<button class="btn ghost" id="sb" style="width:auto;margin:0 0 10px;padding:8px 16px">← Back</button>${VID[key]?`',
    'const tl=n[1],em=key&&key[0]==="w"?worldEmoji(tl,n[0]):sportEmoji(n[0]+" "+tl),lab=key&&key[0]==="w"?"":n[0];\n const vd=VID[key]||(/^[\\w-]{11}$/.test(n[6]||"")?n[6]:""),auto=!VID[key]&&!!vd;\n open(`<button class="btn ghost" id="sb" style="width:auto;margin:0 0 10px;padding:8px 16px">← Back</button>${vd?`')
rep('src="https://www.youtube.com/embed/${VID[key]}?rel=0&playsinline=1"','src="https://www.youtube.com/embed/${vd}?rel=0&playsinline=1${auto?"&autoplay=1&mute=1&end=45":""}"')
rep('<a href="https://www.youtube.com/watch?v=${VID[key]}" target="_blank" rel="noopener" style="display:block;margin-top:6px;font-size:13px;color:var(--acc)">Video not playing? Open it on YouTube</a>',
    '${auto&&n[7]?`<div class="note" style="margin:6px 0 0">▶ Preview: ${esc(n[7])}. Tap the speaker to hear it.</div>`:""}<a href="https://www.youtube.com/watch?v=${vd}" target="_blank" rel="noopener" style="display:block;margin-top:6px;font-size:13px;color:var(--acc)">Video not playing? Open it on YouTube</a>')
rep('<button class="btn ghost" id="sv1">▶ Watch video coverage</button>','${vd?"":`<button class="btn ghost" id="sv1">▶ Watch video coverage</button>`}')
rep('$("#sv1").onclick=()=>go(ytq(tl));','{const sv=$("#panel").querySelector("#sv1");if(sv)sv.onclick=()=>go(ytq(tl))}')
rep('${sportPh(key&&key[0],n)?"The photo shows the topic in general, not this exact story. ":"The picture is an illustration made by WorldLink. "}Photos and videos from this story stay on the publisher\'s page and on YouTube, so we link to them and do not copy them.',
    '${n[5]?"Photo from the publisher. ":sportPh(key&&key[0],n)?"The photo shows the topic in general, not this exact story. ":"The picture is an illustration made by WorldLink. "}Photos and videos stay on the publisher\'s page and on YouTube, so we link to them and do not copy them. The preview video may be related coverage, not an exact match.')
# card button on the swipe list
rep('else go(ytq(n[1]),"Video coverage: "+n[1],"Opens YouTube search results for this story. Choose an official news channel to watch.");return}','else storyView(n,back,kind+i);return}')
rep('▶ Watch video</button></div></section>','▶ Play preview</button></div></section>')
open(sys.argv[2],'w',encoding='utf8').write(s)
