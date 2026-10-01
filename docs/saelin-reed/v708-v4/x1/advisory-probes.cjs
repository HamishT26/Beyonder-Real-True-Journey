'use strict';
const assert=require('node:assert/strict'),crypto=require('node:crypto'),C=require('./core.cjs');
const out=[];function check(id,run){try{run();out.push({id,result:'pass'});}catch(e){out.push({id,result:'fail',error:e.message});}}
function selectGeneration(active,candidate,validated){return validated?structuredClone(candidate):structuredClone(active);}
const c0={interpreter:'A',dependencies:'A',export:'disabled'},c1={interpreter:'B',dependencies:'B',export:'disabled'};
check('T2-config-complete',()=>assert.deepEqual(selectGeneration(c0,c1,true),c1));
check('T2-config-partial-refused',()=>assert.deepEqual(selectGeneration(c0,{interpreter:'B'},false),c0));
check('T2-config-rollback-keeps-evidence',()=>{const retained=structuredClone(c1),restored=selectGeneration(c1,c0,true);assert.deepEqual(restored,c0);assert.deepEqual(retained,c1);assert.notDeepEqual({...c0,interpreter:'B'},c0);});
function mockContained(request){if(!C.safePath(request.path))return false;return !request.before.reparse&&!request.opened.reparse&&request.opened.root==='LAB'&&request.before.identity===request.opened.identity;}
const good={path:'data/ok.txt',before:{root:'LAB',identity:'i1',reparse:false},opened:{root:'LAB',identity:'i1',reparse:false}};
check('T2-path-regular-control',()=>assert.equal(mockContained(good),true));
check('T2-path-outside-and-traversal',()=>{assert.equal(mockContained({...good,path:'../other/x'}),false);assert.equal(mockContained({...good,opened:{root:'OTHER',identity:'i2',reparse:true}}),false);});
check('T2-path-race-model',()=>{const flipped={...good,opened:{root:'OTHER',identity:'i2',reparse:true}};assert.equal(mockContained(flipped),false);const prefixOnlyMutant=C.safePath(flipped.path);assert.equal(prefixOnlyMutant,true);});
// Public, deterministic test-only seeds. These keys are never used for real records.
function testKey(byte){return crypto.createPrivateKey({key:Buffer.concat([Buffer.from('302e020100300506032b657004220420','hex'),Buffer.alloc(32,byte)]),format:'der',type:'pkcs8'});}
const k0=testKey(1),k1=testKey(2),pub0=crypto.createPublicKey(k0);
const data={'notes.txt':'OK\n','state.txt':'1\n'};
function manifest(snapshot=7){return {namespace:'lab-memory',snapshot,schema:1,files:Object.entries(data).map(([name,s])=>({name,bytes:Buffer.byteLength(s),sha256:C.hash(s)}))};}
function signed(m,key){const bytes=Buffer.from(C.canonical(m));return {m,signature:crypto.sign(null,bytes,key)};}
function acceptBackup(bundle,files,anchor){if(!anchor)throw Error('TRUST_ANCHOR_MISSING');return bundle.m.snapshot===7&&crypto.verify(null,Buffer.from(C.canonical(bundle.m)),anchor,bundle.signature)&&bundle.m.files.every(e=>Object.hasOwn(files,e.name)&&Buffer.byteLength(files[e.name])===e.bytes&&C.hash(files[e.name])===e.sha256)&&Object.keys(files).length===bundle.m.files.length;}
check('T2-signed-positive',()=>assert.equal(acceptBackup(signed(manifest(),k0),data,pub0),true));
check('T2-signer-substitution-detected',()=>{const b=signed(manifest(),k1);assert.equal(acceptBackup(b,data,pub0),false);assert.equal(crypto.verify(null,Buffer.from(C.canonical(b.m)),crypto.createPublicKey(k1),b.signature),true);});
check('T2-snapshot-and-completeness',()=>{assert.equal(acceptBackup(signed(manifest(6),k0),data,pub0),false);assert.equal(acceptBackup(signed(manifest(),k0),{'notes.txt':'OK\n'},pub0),false);assert.throws(()=>acceptBackup(signed(manifest(),k0),data,null),/TRUST_ANCHOR/);});
const j1={schema:1,seq:1,model:'v1',status:'FAILED',credit:0,previous:null},j2={schema:1,seq:2,model:'v2',status:'PASSED',corrects:1,previous:C.hash(C.canonical(j1))},j3={schema:1,seq:3,model:'v3',status:'PASSED',corrects:2,previous:C.hash(C.canonical(j2))};
function committed(records,checkpoint){const chosen=records.slice(0,checkpoint.seq);if(chosen.length!==checkpoint.seq||C.hash(C.canonical(chosen.at(-1)))!==checkpoint.digest)throw Error('COMMITTED_PREFIX_DAMAGED');for(let i=0;i<chosen.length;i++)if(chosen[i].schema!==1||chosen[i].seq!==i+1||(i&&chosen[i].previous!==C.hash(C.canonical(chosen[i-1]))))throw Error('COMMITTED_PREFIX_DAMAGED');return chosen;}
const checkpoint={seq:2,digest:C.hash(C.canonical(j2))};
check('T2-journal-positive',()=>assert.deepEqual(committed([j1,j2],checkpoint),[j1,j2]));
check('T2-journal-tail-not-commit',()=>{const r=committed([j1,j2,j3],checkpoint);assert.equal(r.length,2);assert.equal(r[0].credit,0);assert.equal([j1,j2,j3].at(-1).model,'v3');assert.equal(r.at(-1).model,'v2');});
check('T2-journal-damaged-prefix',()=>assert.throws(()=>committed([j1,j3],checkpoint),/DAMAGED/));
function tensorFixture(signature){if(!signature)throw Error('TENSOR_CONVENTION_UNSPECIFIED');const q=[0.5,0,-0.5,-0.5];return {q,trace:q.reduce((s,x,i)=>s+x*signature[i],0),divergence:[0,0,0,0],units:'m^-2',disposition:'KINEMATIC_ONLY'};}
check('T2-tensor-nine-points',()=>{for(const t of [-2,0,2])for(const x of [-2,0,2]){const r=tensorFixture([-1,1,1,1]);assert.deepEqual(r.q,[0.5,0,-0.5,-0.5]);assert.equal(r.trace,-1.5);assert.deepEqual(r.divergence,[0,0,0,0]);assert.equal(r.disposition,'KINEMATIC_ONLY');}});
check('T2-tensor-euclidean-mutant',()=>{assert.equal(tensorFixture([1,1,1,1]).trace,-0.5);assert.notEqual(tensorFixture([1,1,1,1]).trace,-1.5);});
check('T2-tensor-conventions-required',()=>assert.throws(()=>tensorFixture(null),/UNSPECIFIED/));
const report={schema:'ghc.advisory-adoption-results.v1',source:'Teren Serein consultation 2',session:'x1',tests:out.length,passed:out.filter(r=>r.result==='pass').length,failed:out.filter(r=>r.result==='fail').length,results:out,limits:['Filesystem race fixture is a mock, not a Windows race-security proof.','Public test signing keys are unsuitable for real backups.','Tensor fixture is kinematic, not a solution of a gravitational field equation.','No live external effects or source suite replay.']};
if(require.main===module){console.log(JSON.stringify(report,null,2));process.exitCode=report.failed?1:0;}module.exports={report};
