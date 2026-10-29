/* WorldLink service worker: finishes video uploads in the background and shows a phone notification. */
function idb(){return new Promise(function(ok,no){var r=indexedDB.open("wl_jobs",1);r.onupgradeneeded=function(){r.result.createObjectStore("j",{keyPath:"id"})};r.onsuccess=function(){ok(r.result)};r.onerror=function(){no(r.error)}})}
function tx(mode,fn){return idb().then(function(d){return new Promise(function(ok,no){var t=d.transaction("j",mode),r=fn(t.objectStore("j"));t.oncomplete=function(){ok(r&&r.result)};t.onerror=function(){no(t.error)}})}).catch(function(){return null})}
function getJob(id){return tx("readonly",function(o){return o.get(id)})}
function putJob(j){return tx("readwrite",function(o){return o.put(j)})}
function delJob(id){return tx("readwrite",function(o){return o.delete(id)})}
self.addEventListener("install",function(){self.skipWaiting()});
self.addEventListener("activate",function(e){e.waitUntil(clients.claim())});
async function anyVisible(){var l=await clients.matchAll({type:"window",includeUncontrolled:true});return l.some(function(c){return c.visibilityState==="visible"})}
async function say(title,body,tag){if(await anyVisible())return;try{await self.registration.showNotification(title,{body:body,tag:tag||"wl-upload",renotify:true})}catch(e){}}
async function tell(msg){(await clients.matchAll({includeUncontrolled:true})).forEach(function(c){c.postMessage(msg)})}
self.addEventListener("backgroundfetchsuccess",function(e){
 var bf=e.registration;
 e.waitUntil((async function(){
  var job=await getJob(bf.id),done=false;
  if(job&&job.meta){
   var m=job.meta;
   try{
    var r=await fetch(m.doc,{method:"PATCH",headers:{"Authorization":"Bearer "+m.token,"Content-Type":"application/json"},body:JSON.stringify({fields:{id:{stringValue:job.id},url:{stringValue:m.pub},c:{stringValue:job.cap||""},u:{stringValue:m.u||""},uid:{stringValue:m.uid||""},ts:{integerValue:String(Date.now())}}})});
    done=r.ok;
   }catch(err){done=false}
   if(done)await delJob(job.id);else{job.uploaded=true;await putJob(job)}
  }
  try{e.updateUI({title:done?"Video posted":"Video uploaded"})}catch(err){}
  await say(done?"Your video is posted":"Your video is uploaded",done?"Open WorldLink to see it.":"Open WorldLink to finish posting it.");
  await tell({type:"posted",id:bf.id,done:done});
 })());
});
self.addEventListener("backgroundfetchfail",function(e){
 var bf=e.registration;
 e.waitUntil((async function(){await say("Video upload stopped","Open WorldLink to try again.");await tell({type:"upfail",id:bf.id})})());
});
self.addEventListener("backgroundfetchclick",function(e){e.waitUntil(clients.openWindow("/"))});
self.addEventListener("notificationclick",function(e){
 e.notification.close();
 e.waitUntil((async function(){
  var l=await clients.matchAll({type:"window",includeUncontrolled:true});
  if(l.length){try{await l[0].focus();return}catch(err){}}
  await clients.openWindow("/");
 })());
});
