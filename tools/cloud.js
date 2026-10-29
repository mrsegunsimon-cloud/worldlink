/* ===== Online storage: Firestore (records) and Cloud Storage (photos, videos) over HTTPS with the user's sign-in token ===== */
(function(){
 var P="__PROJECT__",B="__BUCKET__",SB={url:"__SBURL__",key:"__SBKEY__"};
 if(SB.url.indexOf("__")===0)SB.url="";
 var FS="https://firestore.googleapis.com/v1/projects/"+P+"/databases/(default)/documents";
 function tok(){return WLN("token").then(function(r){return r&&r.token||null}).catch(function(){return null})}
 function enc(v){
  if(v===null||v===undefined)return{nullValue:null};
  if(typeof v==="string")return{stringValue:v};
  if(typeof v==="boolean")return{booleanValue:v};
  if(typeof v==="number")return Number.isInteger(v)?{integerValue:String(v)}:{doubleValue:v};
  if(Array.isArray(v))return{arrayValue:{values:v.map(enc)}};
  if(typeof v==="object"){var f={};for(var k in v)if(v[k]!==undefined)f[k]=enc(v[k]);return{mapValue:{fields:f}}}
  return{nullValue:null}}
 function dec(x){
  if("stringValue" in x)return x.stringValue;if("integerValue" in x)return Number(x.integerValue);if("doubleValue" in x)return x.doubleValue;
  if("booleanValue" in x)return x.booleanValue;if("nullValue" in x)return null;
  if("arrayValue" in x)return(x.arrayValue.values||[]).map(dec);
  if("mapValue" in x){var o={},f=x.mapValue.fields||{};for(var k in f)o[k]=dec(f[k]);return o}
  if("timestampValue" in x)return x.timestampValue;return null}
 function decDoc(d){var o={},f=d.fields||{};for(var k in f)o[k]=dec(f[k]);return o}
 function idOf(d){return d.name.split("/").pop()}
 async function call(method,path,body,auth){
  var h={"Content-Type":"application/json"};
  if(auth){var t=await tok();if(t)h.Authorization="Bearer "+t}
  var r=await fetch(path.indexOf("http")===0?path:FS+"/"+path,{method:method,headers:h,body:body?JSON.stringify(body):undefined});
  if(r.status===404)return null;
  if(!r.ok)throw new Error("cloud "+r.status);
  var t2=await r.text();return t2?JSON.parse(t2):{}}
 async function byField(col,field,val){
  var j=await call("POST",FS.replace(/\/documents$/,"/documents")+":runQuery",{structuredQuery:{from:[{collectionId:col}],where:{fieldFilter:{field:{fieldPath:field},op:"EQUAL",value:{stringValue:val}}}}},true);
  return(j||[]).filter(function(x){return x.document}).map(function(x){return{id:idOf(x.document),data:decDoc(x.document)}})}
 window.WLCloud={
  byField:byField,
  spec:function(file){
   if(!SB.url||!window.__wlUser)return null;
   var ext=((file.name||"").split(".").pop()||"").toLowerCase().replace(/[^a-z0-9]/g,"").slice(0,5)||(file.type.split("/")[1]||"bin").replace(/[^a-z0-9]/g,"").slice(0,5);
   var name="u/"+window.__wlUser.uid+"/"+Date.now().toString(36)+Math.random().toString(36).slice(2,7)+"."+ext;
   var h={"apikey":SB.key,"Content-Type":file.type||"application/octet-stream","x-upsert":"false"};if(SB.key.indexOf("sb_")!==0)h.Authorization="Bearer "+SB.key;
   return{url:SB.url+"/storage/v1/object/media/"+name,headers:h,pub:SB.url+"/storage/v1/object/public/media/"+name}},
  docUrl:function(col,id){return FS+"/"+col+"/"+encodeURIComponent(id)},
  on:function(col){return !!window.__wlUser||col==="videos"},
  list:async function(col){
   if(col==="dms"&&window.__wlUser){var u=window.__wlUser.uid,a=await byField("dms","a",u),b=await byField("dms","b",u),seen={},out=[];a.concat(b).forEach(function(d){if(!seen[d.id]){seen[d.id]=1;out.push(d)}});return out}
   var out=[],pt="";
   for(var i=0;i<10;i++){
    var j=await call("GET",col+"?pageSize=300"+(pt?"&pageToken="+encodeURIComponent(pt):""),null,!!window.__wlUser);
    if(!j)break;(j.documents||[]).forEach(function(d){out.push({id:idOf(d),data:decDoc(d)})});
    if(!j.nextPageToken)break;pt=j.nextPageToken}
   return out},
  get:async function(col,id){var j=await call("GET",col+"/"+encodeURIComponent(id),null,!!window.__wlUser);return j?decDoc(j):null},
  set:async function(col,id,v){var f={};for(var k in v)if(v[k]!==undefined)f[k]=enc(v[k]);await call("PATCH",col+"/"+encodeURIComponent(id),{fields:f},true)},
  upload:async function(file,onp){
   var t=await tok();if(!t||!window.__wlUser)throw new Error("Sign in first");
   var ext=((file.name||"").split(".").pop()||"").toLowerCase().replace(/[^a-z0-9]/g,"").slice(0,5)||(file.type.split("/")[1]||"bin").replace(/[^a-z0-9]/g,"").slice(0,5);
   var name="u/"+window.__wlUser.uid+"/"+Date.now().toString(36)+Math.random().toString(36).slice(2,7)+"."+ext;
   function sbh(f){var h={"apikey":SB.key,"Content-Type":f.type||"application/octet-stream","x-upsert":"false"};if(SB.key.indexOf("sb_")!==0)h.Authorization="Bearer "+SB.key;return h}
   if(SB.url){
    if(onp&&window.XMLHttpRequest){
     await new Promise(function(ok,no){var x=new XMLHttpRequest();x.open("POST",SB.url+"/storage/v1/object/media/"+name);var h=sbh(file);for(var k in h)x.setRequestHeader(k,h[k]);
      x.upload.onprogress=function(e){if(e.lengthComputable)try{onp(e.loaded/e.total)}catch(_){}};
      x.onload=function(){x.status>=200&&x.status<300?ok():no(new Error("upload "+x.status))};x.onerror=function(){no(new Error("upload failed"))};x.send(file)})}
    else{var r2=await fetch(SB.url+"/storage/v1/object/media/"+name,{method:"POST",headers:sbh(file),body:file});
    if(!r2.ok)throw new Error("upload "+r2.status)}
    return{url:SB.url+"/storage/v1/object/public/media/"+name}}
   var r=await fetch("https://firebasestorage.googleapis.com/v0/b/"+B+"/o?name="+encodeURIComponent(name),{method:"POST",headers:{"Authorization":"Firebase "+t,"Content-Type":file.type||"application/octet-stream"},body:file});
   if(!r.ok)throw new Error("upload "+r.status);
   var j=await r.json();
   return{url:"https://firebasestorage.googleapis.com/v0/b/"+B+"/o/"+encodeURIComponent(j.name)+"?alt=media&token="+(j.downloadTokens||"")}}
 };
})();
