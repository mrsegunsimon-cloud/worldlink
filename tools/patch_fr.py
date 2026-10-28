"""Friends full screen + video-fallback wording. Usage: patch_fr.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:60]);s=s.replace(a,b)
if 'id="frx"' not in s:
    rep(''' open(`<h2 style="text-align:center;font-size:17px">Friends</h2><div style="display:flex;border-bottom:1px solid var(--line)">''',''' openFull(`<div class="hd"><button id="x" aria-label="Close" style="font-size:22px">✕</button><b id="frx" style="font-size:20px">Friends</b><span style="width:40px"></span></div><div class="pgx" style="padding:0 16px"><div style="display:flex;border-bottom:1px solid var(--line)">''')
    rep('''Open Suggested to find people.</p>'}<button class="btn ghost" id="x">Close</button>`);
 $("#panel").querySelectorAll("[data-ft]")''','''Open Suggested to find people.</p>'}</div>`);
 $("#panel").querySelectorAll("[data-ft]")''')
s=s.replace("This video is blocked in your country or cannot be shown here.","This video cannot be played inside the app.").replace("This video is blocked in your country, so here is the story photo instead.","This video cannot be played inside the app, so here is the story photo instead.")
open(sys.argv[2],'w',encoding='utf8').write(s)
