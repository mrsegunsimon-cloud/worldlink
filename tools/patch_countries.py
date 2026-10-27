"""Adds the Countries (politics and history) section to the Language sheet. Usage: patch_countries.py in.html countries2.js out.html"""
import sys
src, js, dst = sys.argv[1:4]
s = open(src, encoding='utf8').read()
m = open(js, encoding='utf8').read()
if 'const CTR=' in s:
    open(dst, 'w', encoding='utf8').write(s); sys.exit(0)
k = 'function sell(){'
assert s.count(k) == 1
s = s.replace(k, m + '\n' + k)
a = '<button class="btn" id="ln">Learn a language</button>'
assert s.count(a) == 1
s = s.replace(a, a + '<button class="btn" id="ct">🌍 Countries: politics and history</button>')
b = '$("#ln").onclick=learnHome;'
assert s.count(b) == 1
s = s.replace(b, b + '$("#ct").onclick=()=>countries();')
open(dst, 'w', encoding='utf8').write(s)
