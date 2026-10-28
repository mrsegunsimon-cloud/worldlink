"""Story preview: try backup videos before the photo. Usage: patch_alt.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'ALT=' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
a='''   if(d&&d.event==="onError"){window.removeEventListener("message",h);const bx=f.parentNode;'''
b='''   if(d&&d.event==="onError"&&ALT.length){const nx=ALT.shift();f.src="https://www.youtube.com/embed/"+nx+"?rel=0&playsinline=1&autoplay=1&mute=1&end=30&enablejsapi=1";return}
   if(d&&d.event==="onError"){window.removeEventListener("message",h);const bx=f.parentNode;'''
assert s.count(a)==1
s=s.replace(a,b)
a=''' if(auto){const f=$("#panel").querySelector("iframe");if(f){'''
b=''' if(auto){const f=$("#panel").querySelector("iframe");if(f){const ALT=(Array.isArray(n[8])?n[8]:[]).filter(x=>/^[\\w-]{11}$/.test(x)&&x!==vd).slice(0,3);'''
assert s.count(a)==1
s=s.replace(a,b)
open(sys.argv[2],'w',encoding='utf8').write(s)
