'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),models=require('./models.js');
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
function canonical(x){if(Array.isArray(x))return'['+x.map(canonical).join(',')+']';if(x&&typeof x==='object')return'{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';return JSON.stringify(x);}
function exactKeys(q,keys){if(!q||Object.getPrototypeOf(q)!==Object.prototype||Object.keys(q).some(k=>!keys.includes(k)))throw Error('Unexpected request fields');}
function safeRelative(p){return typeof p==='string'&&p.length>0&&p.length<=500&&!p.includes('\\')&&!p.includes('\0')&&!p.startsWith('/')&&!/^[a-z]:/i.test(p)&&p.split('/').every(x=>x!=='.'&&x!=='..'&&x.length>0);}
function queryCatalogue(q,catalogue){exactKeys(q,['query','limit']);if(typeof q.query!=='string'||q.query.length>200||!Number.isInteger(q.limit)||q.limit<1||q.limit>50)throw Error('Invalid catalogue query');const tokens=q.query.toLowerCase().trim().split(/\s+/).filter(Boolean);return catalogue.filter(r=>tokens.every(t=>(r.id+' '+r.description).toLowerCase().includes(t))).slice(0,q.limit);}
function routeGuard(q){exactKeys(q,['owner','phase','canonical','unique','direct_controls','accepted','uncertain','usage_open']);const bools=['canonical','unique','direct_controls','accepted','uncertain','usage_open'];if(bools.some(k=>typeof q[k]!=='boolean')||typeof q.owner!=='string'||typeof q.phase!=='string')throw Error('Invalid route input');return{admitted:q.owner==='Caelen Ash'&&q.phase==='v707-v7'&&q.canonical&&q.unique&&q.direct_controls&&q.usage_open&&!q.accepted&&!q.uncertain,send_performed:false};}
function integrity(q){exactKeys(q,['path','bytes','sha256','content']);if(!safeRelative(q.path)||typeof q.content!=='string'||q.content.length>1000000||!Number.isSafeInteger(q.bytes)||q.bytes<0||!/^[a-f0-9]{64}$/.test(q.sha256))throw Error('Invalid integrity input');return{valid:Buffer.byteLength(q.content)===q.bytes&&hash(q.content)===q.sha256,path:q.path};}
function execute(operation,q,dataDir=path.join(__dirname,'data')){
 if(operation==='model')return models.simulate(q);
 if(operation==='catalogue'){const index=JSON.parse(fs.readFileSync(path.join(dataDir,'skills.json'),'utf8'));const rows=Array.isArray(index)?index:index.chunks.flatMap(c=>{if(!/^skills-[1-9][0-9]*\.json$/.test(c.file))throw Error('Invalid catalogue chunk');const b=fs.readFileSync(path.join(dataDir,c.file));if(hash(b)!==c.sha256)throw Error('Catalogue digest mismatch');return JSON.parse(b);});return queryCatalogue(q,rows);}
 if(operation==='route')return routeGuard(q);
 if(operation==='integrity')return integrity(q);
 if(operation==='claim')return models.claimCheck(q);
 throw Error('Unsupported operation');
}
module.exports={hash,canonical,safeRelative,queryCatalogue,routeGuard,integrity,execute};
