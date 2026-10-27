"""Adds the free-play Play zone. Usage: patch_play.py in.html play2.js out.html"""
import sys
src, js, dst = sys.argv[1:4]
s = open(src, encoding='utf8').read()
m = open(js, encoding='utf8').read()
if 'function playZone(' in s:
    open(dst, 'w', encoding='utf8').write(s); sys.exit(0)
k = 'function sell(){'
assert s.count(k) == 1
s = s.replace(k, m + '\n' + k)
c = '["Video Call","📹"'
assert s.count(c) == 1
s = s.replace(c, '["Play zone","🎰","Free-play lottery and casino-style games.","Now"],' + c)
d = 'if(m[0]==="Learn how")return learnHow();'
assert s.count(d) == 1
s = s.replace(d, d + 'if(m[0]==="Play zone")return playZone();')
open(dst, 'w', encoding='utf8').write(s)
