import crypto from 'node:crypto';
import {clean} from './core.mjs';
import {containsCredential} from './content-checks.mjs';
import {nexusHome,slug,readPrivate,writePrivate,listPrivate} from './private-store.mjs';

export function memoryRecord(raw){
  if(!raw||!slug(raw.id)||!['private','shareable'].includes(raw.classification)||typeof raw.body!=='string'||Buffer.byteLength(raw.body)>65536)throw new Error('Invalid memory record');
  if(containsCredential(raw))throw new Error('Credentials do not belong in the memory bank');
  return {schema:'ghc.nexus.memory.v1',id:raw.id,title:clean(raw.title||raw.id).slice(0,180),classification:raw.classification,body:raw.body,source:clean(raw.source||'user-provided').slice(0,240),createdAt:new Date().toISOString(),sha256:crypto.createHash('sha256').update(raw.body).digest('hex'),autoSync:false};
}
export function saveMemory(c,raw){const value=memoryRecord(raw);return writePrivate(nexusHome(c),'memory/'+value.id+'.json',value);}
export function validateMemoryRecord(r){
  const keys=['schema','id','title','classification','body','source','createdAt','sha256','autoSync'];
  if(!r||typeof r!=='object'||Array.isArray(r)||Object.keys(r).some(k=>!keys.includes(k))||r.schema!=='ghc.nexus.memory.v1'||!slug(r.id)||!['private','shareable'].includes(r.classification)||typeof r.body!=='string'||Buffer.byteLength(r.body)>65536||typeof r.title!=='string'||r.title.length>180||typeof r.source!=='string'||r.source.length>240||typeof r.createdAt!=='string'||!Number.isFinite(Date.parse(r.createdAt))||r.autoSync!==false||!(/^[0-9a-f]{64}$/).test(r.sha256)||containsCredential(r))throw new Error('Invalid memory record');
  if(crypto.createHash('sha256').update(r.body).digest('hex')!==r.sha256)throw new Error('Memory integrity mismatch');
  return r;
}
export function listMemory(c){const root=nexusHome(c);return listPrivate(root,'memory').map(n=>{const r=readMemory(c,n.slice(0,-5));return {id:r.id,title:clean(r.title),classification:r.classification,sha256:r.sha256,createdAt:r.createdAt};});}
export function readMemory(c,id){if(!slug(id))throw new Error('Invalid memory ID');const r=readPrivate(nexusHome(c),'memory/'+id+'.json');if(!r)throw new Error('Memory record not found');validateMemoryRecord(r);if(r.id!==id)throw new Error('Memory selection mismatch');return r;}
export function exportMemory(c,ids){
  if(!Array.isArray(ids)||ids.length<1||ids.length>30||new Set(ids).size!==ids.length)throw new Error('Invalid memory selection');
  const selected=ids.map(id=>readMemory(c,id));if(selected.some(r=>r.classification!=='shareable'))throw new Error('Private records cannot be exported');
  const payload={schema:'ghc.nexus.selected-memory.v1',createdAt:new Date().toISOString(),automaticUpload:false,records:selected};
  return writePrivate(nexusHome(c),'exports/memory-'+crypto.randomUUID()+'.json',payload);
}
