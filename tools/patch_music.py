"""Adds free CC BY 4.0 tracks (Tanner Helland, 35 s clips) to the song library. Usage: patch_music.py in out"""
import sys,json,base64,os
src,dst=sys.argv[1:3]
s=open(src,encoding='utf8').read()
if 'lib-th_daybreak' in s:
    open(dst,'w',encoding='utf8').write(s);sys.exit(0)
T=[("daybreak","Daybreak","santorini"),("home","Home","lagos"),("wild_waters","Wild Waters","iguazu"),("find_you","Find You","paris"),("now_or_never","Now or Never","tokyo"),("syntheticity","Syntheticity","dubai"),("thugs","Thugs","nyc"),("honkytonk_villain","Honky-Tonk Villain","grandcanyon"),("deserve_to_be_loved","Deserve to be Loved","seychelles"),("remember","Remember","lisbon"),("fate","Fate","fuji"),("crossroads","Crossroads","sahara")]
here=os.path.dirname(os.path.abspath(__file__))
out=[]
for k,t,cv in T:
    b=base64.b64encode(open(os.path.join(here,'music',k+'.mp3'),'rb').read()).decode()
    out.append({"id":"lib-th_"+k,"t":t,"a":"Tanner Helland","url":"data:audio/mpeg;base64,"+b,"cv":cv,"lic":"Music by Tanner Helland, CC BY 4.0 (tannerhelland.com/music). Shortened to 35 seconds.","d":35})
a=s.index('/*LIB*/const LIB={"songs":[')+len('/*LIB*/const LIB={"songs":[')
j=s.index('],"videos":[',a)
add=','.join(json.dumps(x,ensure_ascii=False,separators=(',',':')) for x in out)
s=s[:j]+','+add+s[j:]
open(dst,'w',encoding='utf8').write(s)
