import sys
P=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/outputs/worldlink2.html"
s=open(P,encoding="utf8").read()
if "wlEgress1" in s: print("already");sys.exit(0)
def rep(a,b):
    global s
    assert s.count(a)>=1,a[:70]
    s=s.replace(a,b)   # all occurrences
# thumbnails must not download video files just to draw a picture
rep('<video src="${esc(c.src)}" muted playsinline preload="metadata"></video>',
    '<!--wlEgress1--><video src="${esc(c.src)}" muted playsinline preload="none" style="background:linear-gradient(165deg,#12307F,#0b1020)"></video><span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);color:#fff;font-size:22px;opacity:.85;pointer-events:none">▶</span>')
rep('<video src="${esc(z.url)}#t=0.3" muted playsinline preload="metadata" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;pointer-events:none"></video>',
    '<video src="${esc(z.url)}" muted playsinline preload="none" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;pointer-events:none;background:#12307F"></video>')
rep('<video src="${esc(z.url)}#t=0.3" muted playsinline preload="metadata" style="width:100%;height:100%;object-fit:cover;display:block;pointer-events:none"></video>',
    '<video src="${esc(z.url)}" muted playsinline preload="none" style="width:100%;height:100%;object-fit:cover;display:block;pointer-events:none;background:#12307F"></video>')
rep('<video src="${esc(x.url)}#t=1" preload="metadata" muted playsinline','<video src="${esc(x.url)}" preload="none" muted playsinline')
rep('<video src="${esc(c.src)}" controls playsinline preload="metadata"></video>','<video src="${esc(c.src)}" controls playsinline preload="none"></video>')
rep('controls playsinline preload="metadata" style="display:block;max-width:100%;border-radius:12px;background:#000"','controls playsinline preload="none" style="display:block;max-width:100%;border-radius:12px;background:#000"')
open(P,"w",encoding="utf8").write(s)
print("ok")
