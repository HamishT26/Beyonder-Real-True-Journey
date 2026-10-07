import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {EventEmitter} from 'node:events';
import {baselineRank,validateCatalogue,loadCatalogue,buildPacket,studySearch} from './study.mjs';
import {bounded} from './core.mjs';
import {validateCommandOptions} from './hub.mjs';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const fixture=()=>({schema:'ghc.research.openai-math-catalogue.v1',repository:'openai/math',commit:'a'.repeat(40),papers:[
{id:'OAI-MATH-003-01',familyId:'003',title:'Quasi Riemann zero free region',abstract:'An upstream claim, not a local proof.',sourceDirectory:'preprints/Quasi-Riemann',listedInFormalizationCatalogue:true,upstreamReviewStatus:'unchecked',localProofStatus:'not-verified'},
{id:'OAI-MATH-102-01',familyId:'102',title:'Unique Games theorem',abstract:'Finite constraint optimization.',sourceDirectory:'preprints/Unique-Games',listedInFormalizationCatalogue:true,upstreamReviewStatus:'unchecked',localProofStatus:'not-verified'}]});
test('study retains source claim and local verification boundary',()=>{const c={...validateCatalogue(fixture()),sha256:'b'.repeat(64)},p=buildPacket(c,'Riemann',5);assert.equal(p.records[0].id,'OAI-MATH-003-01');assert.equal(p.records[0].localProofStatus,'not-verified');assert.equal(p.records[0].upstreamFormalizationListed,true);assert.equal(p.proofBuilds,0);assert.equal(p.modelCalls,0);assert.equal(p.executionAuthority,false);assert.ok(!p.records[0].sourceUrl.endsWith('.pdf'))});
test('no lexical match produces no misleading sources',()=>{assert.deepEqual(baselineRank('xyzzznomatch',fixture().papers),[])});
test('study duplicates are rejected',()=>{const f=fixture();f.papers.push(f.papers[0]);assert.throws(()=>validateCatalogue(f),/duplicate/)});
test('source traversal and foreign repositories are rejected',()=>{const f=fixture();f.papers[0].sourceDirectory='preprints/../private';assert.throws(()=>validateCatalogue(f),/source path/);assert.throws(()=>validateCatalogue({...fixture(),repository:'other/repo'}))});
test('family and id must agree',()=>{const f=fixture();f.papers[0].familyId='009';assert.throws(()=>validateCatalogue(f),/family/)});
test('query and result limits are enforced',()=>{const c=validateCatalogue(fixture());for(const n of [0,21,NaN,1.5])assert.throws(()=>buildPacket(c,'Riemann',n));for(const q of ['', ' ', 'x'.repeat(401)])assert.throws(()=>buildPacket(c,q,1))});
test('candidate output cannot invent or repeat sources',()=>{const c=validateCatalogue(fixture());assert.throws(()=>buildPacket(c,'x',1,()=>['fake']));assert.throws(()=>buildPacket(c,'x',2,()=>[c.rows[0].id,c.rows[0].id]))});
test('consumer-held fingerprint detects changed file bytes',()=>{const base=process.env.GHC_TEST_TMP||os.tmpdir();const dir=fs.mkdtempSync(path.join(base,'ghc-study-'));const file=path.join(dir,'catalogue.json');try{const data=Buffer.from(JSON.stringify(fixture()));fs.writeFileSync(file,data,{flag:'wx'});assert.equal(loadCatalogue(file,sha(data)).rows.length,2);fs.appendFileSync(file,' ');assert.throws(()=>loadCatalogue(file,sha(data)),/fingerprint/);}finally{assert.ok(path.resolve(file).startsWith(path.resolve(dir)+path.sep));fs.unlinkSync(file);fs.rmdirSync(dir)}});
test('read-only study CLI allowlist refuses execute and route options',()=>{assert.doesNotThrow(()=>validateCommandOptions('study','search',{file:'f',fingerprint:'x',search:'q',limit:'5',json:true}));for(const key of ['execute','session','override','env'])assert.throws(()=>validateCommandOptions('study','search',{[key]:true}))});
function fake({lateAfterStop=false,pipeError=false,earlyOutput=false}={}){
 const child=new EventEmitter();child.pid=123;child.exitCode=null;child.signalCode=null;child.stdout=new EventEmitter();child.stderr=new EventEmitter();child.stdout.destroy=()=>{};child.stderr.destroy=()=>{};child.unref=()=>{};
 child.kill=()=>{if(lateAfterStop)child.stdout.emit('data',Buffer.alloc(20));queueMicrotask(()=>{child.exitCode=1;child.emit('close',1,null)});return true;};
 queueMicrotask(()=>{child.emit('spawn');if(pipeError)child.stderr.emit('error',new Error('fixture'));if(earlyOutput)child.stdout.emit('data',Buffer.alloc(20));});
 return child;
}
test('runner keeps timeout when buffered output arrives while stopping',async()=>{const r=await bounded('fixture',[],{timeoutMs:100,maxBytes:10,spawnFn:()=>fake({lateAfterStop:true})});assert.equal(r.status,'timeout');assert.equal(r.childCloseObserved,true)});
test('runner keeps an earlier pipe error when late output exceeds limit',async()=>{const r=await bounded('fixture',[],{timeoutMs:100,maxBytes:10,spawnFn:()=>fake({lateAfterStop:true,pipeError:true})});assert.equal(r.status,'pipe_error')});
test('output-first failure still reports output limit',async()=>{const r=await bounded('fixture',[],{timeoutMs:100,maxBytes:10,spawnFn:()=>fake({earlyOutput:true})});assert.equal(r.status,'output_limit')});
