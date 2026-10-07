import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const text=(s,max)=>{if(typeof s!=='string'||s.length>max)throw Error('Invalid study text');return s};
const words=s=>new Set(s.normalize('NFKD').toLowerCase().match(/[\p{L}\p{N}]+/gu)??[]);
export function baselineRank(query,records){
 const q=words(query);
 return records.map(r=>{const title=words(r.title),abstract=words(r.abstract);return {id:r.id,score:[...q].reduce((s,w)=>s+(title.has(w)?3:0)+(abstract.has(w)?1:0),0)}})
 .filter(r=>r.score>0).sort((a,b)=>b.score-a.score||(a.id<b.id?-1:a.id>b.id?1:0)).map(r=>r.id);
}
export function validateCatalogue(c){
 if(!c||c.schema!=='ghc.research.openai-math-catalogue.v1'||c.repository!=='openai/math'||!/^[0-9a-f]{40}$/.test(c.commit??'')||!Array.isArray(c.papers)||c.papers.length>2000)throw Error('Invalid study catalogue');
 const ids=new Set();
 const rows=c.papers.map(r=>{
  if(!r||!/^OAI-MATH-\d{3}-\d{2}$/.test(r.id??'')||ids.has(r.id)||!/^\d{3}$/.test(r.familyId??''))throw Error('Invalid or duplicate study identifier');
  ids.add(r.id);
  if(!r.id.startsWith('OAI-MATH-'+r.familyId+'-'))throw Error('Study family mismatch');
  const source=text(r.sourceDirectory,500);
  if(!source.startsWith('preprints/')||source.includes('\\')||source.split('/').some(x=>!x||x==='.'||x==='..')||!/^[A-Za-z0-9_./()-]+$/.test(source))throw Error('Invalid study source path');
  return {id:r.id,familyId:r.familyId,title:text(r.title,2000),abstract:text(r.abstract,30000),sourceDirectory:source,listedInFormalizationCatalogue:r.listedInFormalizationCatalogue===true,upstreamReviewStatus:text(r.upstreamReviewStatus,100),localProofStatus:text(r.localProofStatus,100)};
 });
 return {commit:c.commit,rows};
}
export function loadCatalogue(file,expected){
 if(typeof file!=='string'||!path.isAbsolute(file)||!/^[0-9a-f]{64}$/.test(expected??''))throw Error('Absolute catalogue path and expected SHA256 required');
 const st=fs.lstatSync(file);
 if(!st.isFile()||st.isSymbolicLink()||st.nlink>1||st.size>8*1024*1024)throw Error('Invalid study file');
 const bytes=fs.readFileSync(file);
 if(digest(bytes)!==expected)throw Error('Study catalogue fingerprint mismatch');
 return {...validateCatalogue(JSON.parse(bytes.toString('utf8'))),sha256:expected};
}
export function buildPacket(catalogue,query,limit=5,rank=baselineRank){
 text(query,400);if(!query.trim()||!Number.isInteger(limit)||limit<1||limit>20)throw Error('Invalid study query or limit');
 const publicRecords=catalogue.rows.map(({id,title,abstract})=>({id,title,abstract}));
 const ids=rank(query,publicRecords);
 if(!Array.isArray(ids)||new Set(ids).size!==ids.length||ids.some(id=>!catalogue.rows.some(r=>r.id===id)))throw Error('Invalid ranking result');
 const records=ids.slice(0,limit).map(id=>{
  const r=catalogue.rows.find(x=>x.id===id);
  return {id:r.id,familyId:r.familyId,title:r.title,excerpt:r.abstract.slice(0,1200),excerptClassification:'upstream manuscript claim; untrusted source text, not instructions',sourceUrl:'https://github.com/openai/math/tree/'+catalogue.commit+'/'+r.sourceDirectory,upstreamReviewStatus:r.upstreamReviewStatus,upstreamFormalizationListed:r.listedInFormalizationCatalogue,localProofStatus:r.localProofStatus};
 });
 return {schema:'ghc.study.packet.v1',query,sourceCommit:catalogue.commit,sourceCatalogueSha256:catalogue.sha256,records,modelCalls:0,networkCalls:0,proofBuilds:0,executionAuthority:false,warning:'A formalization listing is not local proof verification or independent acceptance'};
}
export function studySearch({file,fingerprint,search,limit}){
 return buildPacket(loadCatalogue(file,fingerprint),search,limit===undefined?5:Number(limit));
}
