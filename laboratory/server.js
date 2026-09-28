'use strict';
const http=require('http'),fs=require('fs'),path=require('path'),cp=require('child_process'),{safeRelative,hash}=require('./operations.js');
function createServer({root=__dirname,mounts=[],port=43177}={}){
 const allowed=new Set(['index.html','style.css','app.js','models.js',...['labs','skills','projects','roster','research','model-contracts','intake-card','integration','skills-1','skills-2','skills-3'].map(n=>'data/'+n+'.json')]);
 return http.createServer((req,res)=>{
  const host=req.headers.host||'';if(![`127.0.0.1:${port}`,`localhost:${port}`].includes(host)){res.writeHead(403);return res.end('Host refused');}
  res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Cache-Control','no-store');res.setHeader('Referrer-Policy','no-referrer');
  if(req.method!=='GET'&&req.method!=='HEAD'){res.writeHead(405);return res.end('Read-only service');}
  let p;try{p=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\//,'')||'index.html';}catch{res.writeHead(400);return res.end('Bad path');}
  if(!safeRelative(p)){res.writeHead(400);return res.end('Path refused');}
  if(p==='api/intake-card'){
   const db=process.env.GHC_LAB_DB,pin=process.env.GHC_LAB_PIN;
   if(!db||!pin){res.writeHead(503);return res.end('Persistent evidence readback is not configured');}
   const python=path.join(require('os').homedir(),'AppData/Local/Programs/Python/Python312/python.exe');
   cp.execFile(python,['-X','utf8','-B',path.join(__dirname,'intake_store.py'),'read',db,pin],{encoding:'utf8',maxBuffer:1048576,timeout:15000,windowsHide:true},(error,output)=>{
    if(error){res.writeHead(409);return res.end('Evidence integrity check failed');}
    res.setHeader('Content-Type','application/json; charset=utf-8');res.end(req.method==='HEAD'?'':output);
   });return;
  }
  const legacy=/^legacy\/(L\d+)\/index\.html$/.exec(p);
  if(legacy){const mount=mounts.find(m=>m.id===legacy[1]);if(!mount){res.writeHead(404);return res.end('Unknown source');}if(!/^[a-f0-9]{40}$/.test(mount.commit)||!safeRelative(mount.path)||!mount.path.endsWith('.html')){res.writeHead(500);return res.end('Invalid mount');}
   res.setHeader('Content-Security-Policy',"sandbox allow-scripts; default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; frame-ancestors 'self'");
   cp.execFile('git',['-C',mount.checkout,'show',mount.commit+':'+mount.path],{encoding:null,maxBuffer:8*1024*1024,timeout:15000,windowsHide:true},(err,b)=>{if(err){res.writeHead(503);return res.end('Exact source temporarily unavailable');}if(hash(b)!==mount.sha256){res.writeHead(409);return res.end('Source digest mismatch');}res.setHeader('Content-Type','text/html; charset=utf-8');res.end(req.method==='HEAD'?'':b);});return;
  }
  if(!allowed.has(p)){res.writeHead(404);return res.end('Not in laboratory allowlist');}
  res.setHeader('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'");
  const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.json':'application/json'};res.setHeader('Content-Type',(types[path.extname(p)]||'text/plain')+'; charset=utf-8');fs.readFile(path.join(root,p),(e,b)=>{if(e){res.writeHead(404);res.end('Missing laboratory artifact');}else res.end(req.method==='HEAD'?'':b);});
 });
}
module.exports={createServer};
if(require.main===module){const port=Number(process.env.GHC_LAB_PORT||43177);if(!Number.isInteger(port)||port<1024||port>65535)throw Error('Invalid port');const mountFile=process.env.GHC_LAB_MOUNTS;const mounts=mountFile?JSON.parse(fs.readFileSync(mountFile,'utf8')):[];createServer({mounts,port}).listen(port,'127.0.0.1',()=>console.log('GHC Family Laboratory listening on http://127.0.0.1:'+port));}
