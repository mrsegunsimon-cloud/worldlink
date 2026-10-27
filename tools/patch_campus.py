"""Adds Campus life + Learn how to the prototype html. Usage: patch_campus.py in.html campus2.js out.html"""
import sys
src, js, dst = sys.argv[1:4]
s = open(src, encoding='utf8').read()
m = open(js, encoding='utf8').read()
if 'function campusLife(' in s:
    open(dst, 'w', encoding='utf8').write(s); sys.exit(0)
k = 'function sell(){'
assert s.count(k) == 1
s = s.replace(k, m + '\n' + k)
a = '"https://www.google.com/maps/search/universities+near+me"]])}`;'
assert s.count(a) == 1
s = s.replace(a, '"https://www.google.com/maps/search/universities+near+me"]])}<button class="btn" id="clf" style="margin-top:12px">🎓 Campus life: what is happening at schools</button>`;')
b = 'const ng=$("#ng");if(ng)ng.onclick=()=>{'
assert s.count(b) == 1
s = s.replace(b, 'const clf=$("#clf");if(clf)clf.onclick=()=>campusLife();' + b)
c = '["Video Call","📹"'
assert s.count(c) == 1
s = s.replace(c, '["Learn how","📚","Everyday skills with theory, steps and videos.","Now"],' + c)
d = 'if(m[0]==="Campus")return campus();'
assert s.count(d) == 1
s = s.replace(d, d + 'if(m[0]==="Learn how")return learnHow();')
open(dst, 'w', encoding='utf8').write(s)
