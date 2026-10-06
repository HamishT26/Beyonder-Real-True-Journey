import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {saveMemory,readMemory} from './memory-bank.mjs';
import {writePrivate,readPrivate} from './private-store.mjs';
import {snapshotMemory,verifyMemorySnapshot,restoreMemorySnapshot} from './memory-snapshot.mjs';
import {nexusCommand} from './nexus.mjs';
import {validateCommandOptions} from './hub.mjs';

const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
function fixture(t){
 const base=path.resolve(process.env.GHC_HUB_TEST_TMP||(process.platform==='win32'?'D:/GHC-Archives/phase-banks/ghc-nexus-tests':os.tmpdir()));
 fs.mkdirSync(base,{recursive:true});const root=fs.mkdtempSync(path.join(base,'memory-snapshot-'));
 t.after(()=>{const rel=path.relative(base,path.resolve(root));if(!rel||rel.startsWith('..')||path.isAbsolute(rel))throw new Error('Cleanup scope mismatch');fs.rmSync(root,{recursive:true,force:true});});
 return {nexusHome:root,platform:process.platform,cwd:root,state:root};
}
const note=(id,classification='private')=>({id,classification,title:id,body:'Selected '+id,source:'synthetic fixture'});
function mutateSnapshot(c,saved,change){const b=JSON.parse(fs.readFileSync(saved.path,'utf8'));change(b);fs.writeFileSync(saved.path,JSON.stringify(b,null,2)+'\n');return sha(fs.readFileSync(saved.path));}

test('selected private snapshot restores exactly and never changes the live bank',t=>{
 const c=fixture(t);saveMemory(c,note('chosen'));saveMemory(c,note('unselected'));
 writePrivate(c.nexusHome,'contacts/operator.json',{hidden:'CONTACT-CANARY'});writePrivate(c.nexusHome,'credentials/key.json',{hidden:'CREDENTIAL-CANARY'});
 const before=fs.readFileSync(path.join(c.nexusHome,'memory/chosen.json'));
 const saved=snapshotMemory(c,['chosen']);assert.equal(saved.recordCount,1);const serialized=fs.readFileSync(saved.path,'utf8');assert.ok(!serialized.includes('unselected'));assert.ok(!serialized.includes('CANARY'));
 const verified=verifyMemorySnapshot(c,saved.snapshotId,{expectedDigest:saved.sha256});assert.equal(verified.sourceDigestPinned,true);
 const restored=restoreMemorySnapshot(c,saved.snapshotId,{expectedDigest:saved.sha256});const receipt=JSON.parse(fs.readFileSync(restored.receipt,'utf8'));
 assert.equal(receipt.status,'completed');assert.deepEqual(fs.readFileSync(receipt.restored[0].path),before);assert.deepEqual(fs.readFileSync(path.join(c.nexusHome,'memory/chosen.json')),before);assert.equal(restored.liveMemoryChanged,false);
});
test('whole-file pin catches changes even when inner manifest is self-consistent',t=>{const c=fixture(t);saveMemory(c,note('one'));const s=snapshotMemory(c,['one']);mutateSnapshot(c,s,b=>b.createdAt='2026-01-01T00:00:00Z');assert.throws(()=>verifyMemorySnapshot(c,s.snapshotId,{expectedDigest:s.sha256}),/fingerprint mismatch/);});
test('changed body cannot pass snapshot record and manifest validation',t=>{const c=fixture(t);saveMemory(c,note('one'));const s=snapshotMemory(c,['one']);mutateSnapshot(c,s,b=>b.records[0].body='tampered');assert.throws(()=>verifyMemorySnapshot(c,s.snapshotId),/integrity mismatch/);});
test('manifest cannot redirect restore into another private folder',t=>{const c=fixture(t);saveMemory(c,note('one'));const s=snapshotMemory(c,['one']);const pin=mutateSnapshot(c,s,b=>b.manifest[0].path='../credentials/key.json');assert.throws(()=>restoreMemorySnapshot(c,s.snapshotId,{expectedDigest:pin}),/manifest mismatch/);assert.equal(fs.existsSync(path.join(c.nexusHome,'restores')),false);});
test('duplicate selected IDs and snapshot duplicate records are refused',t=>{const c=fixture(t);saveMemory(c,note('one'));assert.throws(()=>snapshotMemory(c,['one','one']));const s=snapshotMemory(c,['one']);mutateSnapshot(c,s,b=>{b.records.push(b.records[0]);b.manifest.push(b.manifest[0]);});assert.throws(()=>verifyMemorySnapshot(c,s.snapshotId),/Duplicate/);});
test('selection is validated before creating any snapshot',t=>{const c=fixture(t);saveMemory(c,note('one'));for(const ids of [[],['../credentials/key'],['one','missing'],Array.from({length:31},(_,i)=>'r'+i)])assert.throws(()=>snapshotMemory(c,ids));assert.equal(fs.existsSync(path.join(c.nexusHome,'snapshots')),false);});
test('memory record rejects unrecognized fields and filename identity mismatch',t=>{const c=fixture(t);saveMemory(c,note('one'));const file=path.join(c.nexusHome,'memory/one.json');let r=JSON.parse(fs.readFileSync(file));r.id='two';fs.writeFileSync(file,JSON.stringify(r));assert.throws(()=>readMemory(c,'one'),/selection mismatch/);r.id='one';r.privateNotes='hidden';fs.writeFileSync(file,JSON.stringify(r));assert.throws(()=>snapshotMemory(c,['one']),/Invalid memory record/);});
test('credential material inserted into a saved memory record is refused',t=>{const c=fixture(t);saveMemory(c,note('one'));const file=path.join(c.nexusHome,'memory/one.json');const r=JSON.parse(fs.readFileSync(file));r.body='{"access_token":"fixture"}';r.sha256=sha(r.body);fs.writeFileSync(file,JSON.stringify(r));assert.throws(()=>snapshotMemory(c,['one']),/Invalid memory record/);});
test('linked snapshot source is refused',t=>{const c=fixture(t);saveMemory(c,note('one'));const s=snapshotMemory(c,['one']);fs.linkSync(s.path,path.join(c.nexusHome,'other.json'));assert.throws(()=>verifyMemorySnapshot(c,s.snapshotId),/Linked private file|Invalid private file/);});
test('restore requires a separately saved fingerprint',t=>{const c=fixture(t);saveMemory(c,note('one'));const s=snapshotMemory(c,['one']);assert.throws(()=>restoreMemorySnapshot(c,s.snapshotId),/fingerprint is required/);assert.equal(verifyMemorySnapshot(c,s.snapshotId).sourceDigestPinned,false);});
test('maximum thirty-record selection restores in isolation and the thirty-first is refused',t=>{const c=fixture(t);const ids=Array.from({length:30},(_,i)=>'record-'+i);for(const id of ids)saveMemory(c,note(id));const s=snapshotMemory(c,ids);assert.equal(verifyMemorySnapshot(c,s.snapshotId,{expectedDigest:s.sha256}).recordCount,30);const restored=restoreMemorySnapshot(c,s.snapshotId,{expectedDigest:s.sha256});const receipt=JSON.parse(fs.readFileSync(restored.receipt));assert.equal(receipt.restored.length,30);for(const r of receipt.restored)assert.deepEqual(fs.readFileSync(r.path),fs.readFileSync(path.join(c.nexusHome,'memory/'+r.id+'.json')));assert.throws(()=>snapshotMemory(c,[...ids,'record-30']));});
test('JSON escaping cannot silently exceed the snapshot output bound',t=>{const c=fixture(t);const ids=Array.from({length:6},(_,i)=>'large-'+i);for(const id of ids)saveMemory(c,{...note(id),body:'\u0000'.repeat(65536)});assert.throws(()=>snapshotMemory(c,ids),/too large/);const dir=path.join(c.nexusHome,'snapshots');assert.deepEqual(fs.existsSync(dir)?fs.readdirSync(dir):[],[]);});
test('CLI writes require execute and reject arbitrary path options',async t=>{const c=fixture(t);await assert.rejects(()=>nexusCommand('memory','snapshot',{id:'one'},c),/--execute/);await assert.rejects(()=>nexusCommand('memory','restore',{id:'one'},c),/--execute/);assert.throws(()=>validateCommandOptions('memory','restore',{file:'private',execute:true}),/Unsupported/);});
