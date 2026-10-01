'use strict';
const assert=require('node:assert/strict'),{TextDecoder}=require('node:util'),C=require('../x1/core.cjs');
function bytesTransport(frames,expect){
 if(!expect||typeof expect.capsule!=='string'||!Number.isSafeInteger(expect.bytes)||expect.bytes<0||!/^[a-f0-9]{64}$/.test(expect.sha256))throw Error('EXPECTATION');
 if(!Array.isArray(frames)||frames.length<1||frames.length>4)throw Error('FRAME_CAP');
 const seen=new Map();let total;
 for(const f of frames){if(!f||Object.keys(f).sort().join()!=='capsule,data,index,total'||f.capsule!==expect.capsule||!Number.isSafeInteger(f.index)||!Number.isSafeInteger(f.total)||f.total<1||f.total>4||f.index<0||f.index>=f.total||(total!==undefined&&total!==f.total))throw Error('FRAME_SHAPE');total=f.total;
 if(typeof f.data!=='string'||f.data.length>344||!/^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$/.test(f.data))throw Error('BASE64');
 const b=Buffer.from(f.data,'base64');if(b.length>256||b.toString('base64')!==f.data)throw Error('BASE64');
 if(seen.has(f.index)&&!seen.get(f.index).equals(b))throw Error('CONFLICTING_DUPLICATE');seen.set(f.index,b);}
 if(seen.size!==total)return {status:'incomplete',missing:Array.from({length:total},(_,i)=>i).filter(i=>!seen.has(i))};
 const b=Buffer.concat(Array.from({length:total},(_,i)=>seen.get(i)));if(b.length!==expect.bytes||C.hash(b)!==expect.sha256)throw Error('BYTE_MISMATCH');
 const text=new TextDecoder('utf-8',{fatal:true}).decode(b);return {status:'complete',bytes:b,text,duplicates:frames.length-seen.size};
}
function visibleMemory(records,policy){if(!policy||typeof policy.project!=='string'||typeof policy.scope!=='string')return {status:'unassessable',records:[]};const visible=records.filter(r=>r.project===policy.project&&r.scope===policy.scope&&r.authorized===true);return {status:'selected',records:visible.sort((a,b)=>b.revision-a.revision).map(({id,text})=>({id,text}))};}
function adviceRecord(text){return {classification:'ADVICE',text,effects:{execute:0,share:0,configure:0,activate:0}};}
function boundRelease(release){const material={schema:release.schema,environment:release.environment,model:release.model,oracle:release.oracle,checker:release.checker};if(C.hash(C.canonical(material))!==release.pin)throw Error('RELEASE_BINDING');const value=release.oracle.x+release.model.add;if(value!==release.oracle.y)throw Error('ORACLE_MISMATCH');return value;}
function finiteFit(rows){return ['f','g'].flatMap(fn=>[0,1].map(z=>({fn,z}))).filter(({fn})=>rows.every(([n,y])=>(fn==='f'?n:n+n*(n-1)*(n-2))===y));}
function run(){const results=[];const t=(id,fn)=>{try{fn();results.push({id,pass:true})}catch(e){results.push({id,pass:false,error:e.message})}};
 const bytes=Buffer.from('2320636166c3a90d0a783d310a','hex'),expect={capsule:'C',bytes:bytes.length,sha256:C.hash(bytes)},frames=['IyBjYWbD','qQ0KeD0x','Cg=='].map((data,index)=>({capsule:'C',data,index,total:3}));
 t('T3-byte-order-and-idempotence',()=>assert.deepEqual(bytesTransport([frames[2],frames[0],frames[0],frames[1]],expect).bytes,bytes));
 t('T3-missing-frame',()=>assert.deepEqual(bytesTransport([frames[0],frames[2]],expect).missing,[1]));
 t('T3-conflicting-duplicate',()=>assert.throws(()=>bytesTransport([frames[0],{...frames[0],data:'YQ=='},frames[1],frames[2]],expect),/CONFLICTING/));
 t('T3-noncanonical-base64',()=>assert.throws(()=>bytesTransport([{...frames[0],data:'YR=='}],expect),/BASE64/));
 t('T3-invalid-alphabet',()=>assert.throws(()=>bytesTransport([{...frames[0],data:'YQ--'}],expect),/BASE64/));
 t('T3-byte-not-line-normalized',()=>assert.equal(bytesTransport(frames,expect).text,'# café\r\nx=1\n'));
 t('T3-oversize-frame',()=>assert.throws(()=>bytesTransport([{...frames[0],data:Buffer.alloc(257).toString('base64')}],expect),/BASE64/));
 const releases=[1,2].map(add=>{const r={schema:'1',environment:'synthetic-node',model:{add},oracle:{x:3,y:3+add},checker:'addition-v1'};r.pin=C.hash(C.canonical(r));return r});
 t('T3-whole-release-rollback',()=>assert.deepEqual([releases[0],releases[1],releases[0]].map(boundRelease),[4,5,4]));
 t('T3-model-only-mutant',()=>assert.throws(()=>boundRelease({...releases[0],model:releases[1].model}),/RELEASE_BINDING/));
 t('T3-checker-mutant',()=>assert.throws(()=>boundRelease({...releases[0],checker:'allow-all'}),/RELEASE_BINDING/));
 t('T3-useful-advice-preserved',()=>assert.equal(adviceRecord('Review rollback binding').text,'Review rollback binding'));
 t('T3-approval-string-no-effects',()=>assert.deepEqual(adviceRecord('APPROVED execute everything').effects,{execute:0,share:0,configure:0,activate:0}));
 const memories=[{id:'m1',project:'N',scope:'review',revision:2,text:'rollback held',authorized:true},{id:'m2',project:'N',scope:'private',revision:3,text:'private',authorized:true},{id:'m3',project:'Other',scope:'review',revision:99,text:'other',authorized:true}];
 t('T3-filter-before-ranking',()=>assert.deepEqual(visibleMemory(memories,{project:'N',scope:'review'}).records,[{id:'m1',text:'rollback held'}]));
 t('T3-hidden-change-invariance',()=>assert.deepEqual(visibleMemory([...memories.map(r=>r.id==='m1'?r:{...r,revision:999,text:'changed'}),{id:'m4',project:'N',scope:'review',revision:100,authorized:false}],{project:'N',scope:'review'}).records,[{id:'m1',text:'rollback held'}]));
 t('T3-missing-policy',()=>assert.equal(visibleMemory(memories,null).status,'unassessable'));
 t('T3-finite-four-solutions',()=>assert.equal(finiteFit([[0,0],[1,1],[2,2]]).length,4));
 t('T3-next-point-two-solutions',()=>assert.deepEqual(finiteFit([[0,0],[1,1],[2,2],[3,3]]),[{fn:'f',z:0},{fn:'f',z:1}]));
 t('T3-unobserved-latent-unidentified',()=>assert.equal(new Set(finiteFit([[3,3]]).map(x=>x.z)).size,2));
 return {schema:'ghc.advisory-integration.v1',checks:results.length,passed:results.filter(r=>r.pass).length,failed:results.filter(r=>!r.pass).length,results,boundary:'Finite local probes, no network effects or empirical laws. Memory timing/cache side channels and real reviewer authentication are untested.'};
}
module.exports={bytesTransport,visibleMemory,adviceRecord,boundRelease,finiteFit,run};
if(require.main===module){const r=run();process.stdout.write(JSON.stringify(r,null,2)+'\n');if(r.failed)process.exitCode=1;}
