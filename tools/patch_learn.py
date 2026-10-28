"""WorldLink Learn labelled channel. Usage: patch_learn.py in out"""
import sys,json
s=open(sys.argv[1],encoding='utf8').read()
if 'wllearn-' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
man=json.load(open('assets/learn.json',encoding='utf8'))
a='let order=mk(1),liked={},saved={};'
assert s.count(a)==1
B="https://mrsegunsimon-cloud.github.io/worldlink/starter/"
code='/*learn*/(function(){const B="'+B+'";'+json.dumps(man,ensure_ascii=False)+'.forEach(([k,c])=>CLIPS.push({u:"WorldLink Learn (made by WorldLink)",c:c+" 📚 #learn",m:"Music: Tanner Helland (CC BY 4.0)",l:0,g:["#0f766e","#1d4ed8"],e:"📚",cm:[],uid:"worldlink-learn",id:"wllearn-"+k,src:B+k+".mp4"}))})();\n'
s=s.replace(a,code+a)
open(sys.argv[2],'w',encoding='utf8').write(s)
