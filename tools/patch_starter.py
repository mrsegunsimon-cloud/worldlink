"""Official WorldLink Team starter videos. Usage: patch_starter.py in out"""
import sys
s=open(sys.argv[1],encoding='utf8').read()
if 'worldlink-team' in s:
    open(sys.argv[2],'w',encoding='utf8').write(s);sys.exit(0)
a='let order=mk(1),liked={},saved={};'
assert s.count(a)==1
B="https://worldlink.app/starter/"
code='''/*starter*/(function(){const B="'''+B+'''";[["welcome","Welcome to WorldLink! Share your day with the world 🌍 #welcome"],["howpost","How to post your first video: tap + , record, add a caption, post 🎬 #howto"],["explore","Explore live news, sports, music and beaches in one app ⚽🏖️🎵 #explore"],["safe","Your videos are yours - delete any time from your Profile 🔒 #privacy"],["music","Free songs and music videos in Discover 🎶 #music"],["invite","Be an early creator - invite 3 friends and earn free coins 🎁 #invite"]].forEach(([k,c])=>CLIPS.push({u:"WorldLink Team ✔ (official)",c:c+" · Official WorldLink video",m:"Music: Tanner Helland (CC BY 4.0)",l:0,g:["#0f766e","#1d4ed8"],e:"🌍",cm:[],uid:"worldlink-team",id:"wlteam-"+k,src:B+k+".mp4"}))})();
'''
s=s.replace(a,code+a)
open(sys.argv[2],'w',encoding='utf8').write(s)
