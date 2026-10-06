import crypto from 'node:crypto';
import {nexusHome,slug,readPrivateBytes,writePrivate} from './private-store.mjs';
import {readMemory,validateMemoryRecord} from './memory-bank.mjs';

const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const encode=value=>Buffer.from(JSON.stringify(value,null,2)+'\n');
const uuid=value=>typeof value==='string'&&/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(value);
const digest=value=>typeof value==='string'&&/^[0-9a-f]{64}$/.test(value);
const exact=(value,keys)=>value&&typeof value==='object'&&!Array.isArray(value)&&Object.keys(value).length===keys.length&&Object.keys(value).every(k=>keys.includes(k));

export function snapshotMemory(c,ids){
  if(!Array.isArray(ids)||ids.length<1||ids.length>30||ids.some(id=>!slug(id))||new Set(ids).size!==ids.length)throw new Error('Select 1 to 30 unique memory IDs');
  // The only inputs are named memory records. No source path or credential folder is accepted.
  const records=ids.map(id=>readMemory(c,id));
  const manifest=records.map(record=>{const bytes=encode(record);return {id:record.id,path:'memory/'+record.id+'.json',bytes:bytes.length,sha256:hash(bytes)};});
  const id=crypto.randomUUID();
  const bundle={schema:'ghc.nexus.memory-snapshot.v1',id,createdAt:new Date().toISOString(),classification:'private',scope:'selected-memory-only',automaticUpload:false,manifest,records};
  const saved=writePrivate(nexusHome(c),'snapshots/'+id+'.json',bundle);
  return {...saved,snapshotId:id,recordCount:records.length,classification:'private',automaticUpload:false,sourceDigestPinned:true};
}

function readSnapshot(c,id,expectedDigest){
  if(!uuid(id))throw new Error('Invalid snapshot ID');
  if(expectedDigest!==undefined&&!digest(expectedDigest))throw new Error('Invalid snapshot fingerprint');
  const bytes=readPrivateBytes(nexusHome(c),'snapshots/'+id+'.json',{maxBytes:2097152});
  if(!bytes)throw new Error('Snapshot not found');
  const sha256=hash(bytes);
  if(expectedDigest!==undefined&&sha256!==expectedDigest)throw new Error('Snapshot fingerprint mismatch');
  const bundle=JSON.parse(bytes.toString('utf8'));
  if(!exact(bundle,['schema','id','createdAt','classification','scope','automaticUpload','manifest','records'])||bundle.schema!=='ghc.nexus.memory-snapshot.v1'||bundle.id!==id||bundle.classification!=='private'||bundle.scope!=='selected-memory-only'||bundle.automaticUpload!==false||typeof bundle.createdAt!=='string'||!Number.isFinite(Date.parse(bundle.createdAt))||!Array.isArray(bundle.records)||bundle.records.length<1||bundle.records.length>30||!Array.isArray(bundle.manifest)||bundle.manifest.length!==bundle.records.length)throw new Error('Invalid memory snapshot');
  const seen=new Set();
  bundle.records.forEach((r,i)=>{
    validateMemoryRecord(r);
    if(seen.has(r.id))throw new Error('Duplicate snapshot record');seen.add(r.id);
    const m=bundle.manifest[i],recordBytes=encode(r);
    if(!exact(m,['id','path','bytes','sha256'])||m.id!==r.id||m.path!=='memory/'+r.id+'.json'||m.bytes!==recordBytes.length||m.sha256!==hash(recordBytes))throw new Error('Snapshot manifest mismatch');
  });
  return {bundle,sha256,bytes:bytes.length};
}

export function verifyMemorySnapshot(c,id,{expectedDigest}={}){
  const {bundle,sha256,bytes}=readSnapshot(c,id,expectedDigest);
  return {status:'ok',schema:'ghc.nexus.memory-snapshot-verification.v1',snapshotId:id,sha256,bytes,recordCount:bundle.records.length,sourceDigestPinned:expectedDigest!==undefined,contentValid:true,authenticityEstablished:false,automaticUpload:false};
}

export function restoreMemorySnapshot(c,id,{expectedDigest}={}){
  if(!digest(expectedDigest))throw new Error('A saved snapshot fingerprint is required for restore');
  const {bundle,sha256}=readSnapshot(c,id,expectedDigest),root=nexusHome(c),restoreId=crypto.randomUUID();
  const base='restores/'+restoreId;
  // A interrupted restore has only an incomplete transaction and never modifies the live memory bank.
  writePrivate(root,base+'/transaction.json',{schema:'ghc.nexus.memory-restore-transaction.v1',restoreId,snapshotId:id,sha256,state:'incomplete',liveMemoryChanged:false});
  const restored=bundle.records.map((record,i)=>{
    const relative=base+'/'+bundle.manifest[i].path;
    const result=writePrivate(root,relative,record);
    const readback=readPrivateBytes(root,relative);
    if(!readback||readback.length!==bundle.manifest[i].bytes||hash(readback)!==bundle.manifest[i].sha256)throw new Error('Restored memory readback mismatch');
    return {id:record.id,path:result.path,bytes:readback.length,sha256:hash(readback)};
  });
  const receipt={schema:'ghc.nexus.memory-restore.v1',status:'completed',restoreId,snapshotId:id,sourceSha256:sha256,completedAt:new Date().toISOString(),recordCount:restored.length,restored,liveMemoryChanged:false,automaticUpload:false};
  const saved=writePrivate(root,base+'/receipt.json',receipt);
  return {status:'completed',restoreId,snapshotId:id,recordCount:restored.length,receipt:saved.path,liveMemoryChanged:false,automaticUpload:false};
}
