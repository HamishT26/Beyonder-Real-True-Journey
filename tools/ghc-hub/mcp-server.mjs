import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {serveNexusStdio} from './mcp/sdk/src/bridge.mjs';
import {context} from './core.mjs';
import {nexusHome,readPrivate} from './private-store.mjs';
import {readRegistry,chatPlan} from './chats.mjs';
import {LAB_MODELS,labPlan} from './laboratory.mjs';
import {readSentinel,validateSentinel,sentinelPlan} from './sentinel.mjs';
import {remotePlan} from './remote.mjs';

export function createNexusBindings(c){
 const registry=readPrivate(nexusHome(c),'mcp/selectors.json',{missing:{schema:'ghc.nexus.mcp-selectors.v1',chats:[]}});
 if(registry.schema!=='ghc.nexus.mcp-selectors.v1'||!Array.isArray(registry.chats)||registry.chats.length>128)throw new Error('Invalid MCP selector registry');
 const saved=readRegistry(c),chatMap=new Map();
 for(const entry of registry.chats){
   if(!/^[a-z][a-z0-9_-]{0,63}$/.test(entry.alias)||chatMap.has(entry.alias))throw new Error('Invalid MCP selector alias');
   const found=saved.filter(r=>r.id===entry.id&&r.kind===entry.kind);if(found.length!==1)throw new Error('MCP selector binding changed');chatMap.set(entry.alias,found[0]);
 }
 const selectors={chats:[...chatMap.keys()],labs:LAB_MODELS.map(m=>m.id),sentinels:['sentinel-1'],remotes:['primary']};
 const route=p=>p.status==='ready'?(p.action==='chat-browser'?'manual':p.action==='cloud'?'cloud':'local'):p.status==='native-route'||p.status==='manual'||p.status==='supported_command_prepared'?'manual':'unavailable';
 const publicPlan=p=>({available:p.status==='ready',route:route(p),steps:['select','validate','review','handoff']});
 // Alias identity stays fixed for this process; current status/holds are reread.
 const liveChat=(alias,rows)=>{const bound=chatMap.get(alias);const found=rows.filter(r=>r.id===bound?.id&&r.kind===bound?.kind&&r.hostId===bound?.hostId);return found.length===1?found[0]:null;};
 const currentPlan=r=>r?chatPlan(r,c):{status:'unavailable'};
 async function dispatch(name,args,{signal}={}){
  if(signal?.aborted)throw new Error('Cancelled');
  if(name==='nexus.chats.list'){const rows=readRegistry(c);return {items:[...chatMap.keys()].map(alias=>({alias,available:currentPlan(liveChat(alias,rows)).status==='ready'}))};}
  if(name==='nexus.chats.resolve'||name==='nexus.chats.plan'){const p=currentPlan(liveChat(args.alias,readRegistry(c)));return name.endsWith('.resolve')?{available:p.status==='ready',route:route(p)}:publicPlan(p);}
  if(name==='nexus.lab.catalogue')return {items:LAB_MODELS.map(m=>({alias:m.id,available:true}))};
  if(name==='nexus.lab.plan')return publicPlan(labPlan(c,args.alias));
  if(name==='nexus.identity.summary')return {platform:c.platform,capabilities:{chats:true,lab:true,sentinel:true,remote:remotePlan(c).status==='ready'}};
  if(name==='nexus.remote.plan')return publicPlan(remotePlan(c));
  if(name==='nexus.sentinel.validate'||name==='nexus.sentinel.plan'){
   let spec;try{spec=readSentinel(c,args.alias);}catch{return name.endsWith('.validate')?{valid:null,issues:['missing_input']}:{available:false,route:'unavailable',steps:['select','validate','review']};}
   if(name.endsWith('.validate')){const v=validateSentinel(spec);return {valid:v.valid,issues:v.valid?[]:['invalid_fields']};}
   const p=sentinelPlan(spec);return {available:p.validation.valid,route:'manual',steps:['select','validate','review']};
  }
  throw new Error('Unsupported read-only tool');
 }
 return {dispatch,selectors};
}
export async function main(){
 const c=context(),bindings=createNexusBindings(c);
 const server=serveNexusStdio({input:process.stdin,output:process.stdout,...bindings,servingProfile:'parent-owned'});
 await server.done;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(()=>{console.error('GHC Nexus MCP unavailable; verify its private selector registry and installation.');process.exitCode=1;});
