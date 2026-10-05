import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {nexusHome,checkPath,writePrivate} from './private-store.mjs';
import {bounded} from './core.mjs';

const directory=path.dirname(fileURLToPath(import.meta.url));
export const LAB_MODELS=[
  {id:'diffusion',pillar:'GMUT comparison',title:'Finite conservative diffusion',meaning:'A standard finite-difference comparator; no empirical GMUT validation'},
  {id:'queue',pillar:'THOS',title:'Bounded single-server queue',meaning:'Synthetic scheduling and resource accounting'},
  {id:'consent',pillar:'Freed ID / CBR',title:'Consent expiry and revocation',meaning:'A finite policy model; no legal or moral certification'}
];
export function labCatalogue(c){
  let existing={status:'unavailable'};
  if(c.platform==='win32')try{
    const pointer=JSON.parse(fs.readFileSync('D:/GHC-Family-Laboratory/current.json','utf8'));
    const release=path.resolve(pointer.release),base=path.resolve('D:/GHC-Family-Laboratory/releases');
    if(!release.startsWith(base+path.sep)||typeof pointer.entrypoint!=='string')throw new Error();
    const entry=checkPath(release,pointer.entrypoint),manifest=checkPath(release,'release-manifest.json');
    const manifestBytes=fs.readFileSync(manifest),digest=crypto.createHash('sha256').update(manifestBytes).digest('hex');
    if(digest!==pointer.manifest_sha256)throw new Error();
    const bindings=JSON.parse(manifestBytes).entries?.filter(r=>r.path===pointer.entrypoint.replaceAll('\\','/'));
    const entryBytes=fs.readFileSync(entry),entrySha256=crypto.createHash('sha256').update(entryBytes).digest('hex');
    if(bindings?.length!==1||bindings[0].bytes!==entryBytes.length||bindings[0].sha256!==entrySha256)throw new Error();
    existing={status:'pointer_manifest_verified',release,entry,port:pointer.port,entrySha256,note:'Pointer, manifest digest and exact entrypoint bytes agree; opening the existing server is separate'};
  }catch{existing={status:'unavailable',reason:'pointer_or_manifest_not_verified'};}
  return {schema:'ghc.nexus.lab-catalogue.v1',models:LAB_MODELS,existing,executor:c.platform,security:'Laboratory jobs inherit this executor. These numerical examples are bounded, but this is not an OS sandbox or universal administrator role.'};
}
export function labPlan(c,id,{size=1000}={}){
  if(!LAB_MODELS.some(m=>m.id===id))throw new Error('Unknown laboratory model');
  if(!Number.isInteger(size)||size<1||size>200000)throw new Error('Laboratory size must be 1 to 200000');
  return {schema:'ghc.nexus.lab-plan.v1',status:'ready',action:'lab-'+id,executor:{platform:c.platform,hostId:c.hostId||'current',location:'current executor'},command:c.node,args:[path.join(directory,'lab-worker.mjs'),id,String(size)],cwd:c.cwd,interactive:false,shell:false,timeoutMs:30000,maxOutputBytes:65536,requestedIterations:size,writes:'one private result receipt after completion',modelClass:'synthetic finite experiment'};
}
export async function runLab(c,id,opts={}){
  const plan=labPlan(c,id,opts),r=await bounded(plan.command,plan.args,{cwd:plan.cwd,timeoutMs:plan.timeoutMs,maxBytes:plan.maxOutputBytes});
  let result=null;if(r.status==='ok'){try{result=JSON.parse(r.stdout);if(result.schema!=='ghc.nexus.lab-result.v1'||result.model!==id)throw new Error();}catch{result=null;}}
  const receipt={schema:'ghc.nexus.lab-receipt.v1',id:crypto.randomUUID(),utc:new Date().toISOString(),model:id,executor:c.platform,status:r.status==='ok'&&!result?'failed':r.status,reason:r.status==='ok'&&!result?'invalid_lab_output':null,exitCode:r.exitCode,signal:r.signal??null,spawnObserved:r.spawnObserved??false,elapsedMs:r.elapsedMs,childCloseObserved:r.childCloseObserved,cleanup:r.cleanup??null,signalErrors:r.signalErrors??0,result,passed:r.status==='ok'&&result?.passed===true};
  const saved=writePrivate(nexusHome(c),'lab-results/'+receipt.id+'.json',receipt);return {...receipt,saved};
}
export function existingLabPlan(c){const existing=labCatalogue(c).existing;if(existing.status!=='pointer_manifest_verified')throw new Error('Existing laboratory is unavailable');return {status:'ready',action:'lab-serve',command:c.node,args:[existing.entry],cwd:path.dirname(existing.entry),interactive:true,shell:false,note:'Runs the existing read-only laboratory on localhost:'+existing.port+'. Stop with Ctrl+C. It does not expose an administrator shell to the network.'};}
