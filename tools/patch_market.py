"""Adds the sectioned marketplace (sections, stores, products) to the prototype html. Usage: patch_market.py in.html market2.js out.html"""
import sys
src, js, dst = sys.argv[1:4]
s = open(src, encoding='utf8').read()
m = open(js, encoding='utf8').read()
if 'const MKS=' in s:
    open(dst, 'w', encoding='utf8').write(s); sys.exit(0)
i = s.index('function market(){'); j = s.index('function sell(){')
old = s[i:j].replace('function market(){', 'function market0(){').replace('market()', 'market0()')
old = old.replace('<button class="btn" id="sl">Sell something</button>', '<button class="btn ghost" id="bkm">← Back to stores</button><button class="btn" id="sl">Sell something</button>', 1)
old = old.replace('$("#sl").onclick=sell;', '$("#sl").onclick=sell;$("#bkm").onclick=()=>{MKV={v:"home"};market()};', 1)
s = s[:i] + old + '\n' + m + '\n' + s[j:]
a = 'if(m[0]==="Market")return market();'
assert s.count(a) == 1
s = s.replace(a, 'if(m[0]==="Market"){MKV={v:"home"};return market()}')
b = 'msq=raw.toLowerCase();mcat="All";market()}'
assert s.count(b) == 1
s = s.replace(b, 'msq=raw.toLowerCase();mcat="All";market0()}')
open(dst, 'w', encoding='utf8').write(s)
