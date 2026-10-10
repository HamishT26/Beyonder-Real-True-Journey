import fs from 'node:fs/promises';
import os from 'node:os';
import {CommanderError} from './admin-commander.mjs';

const need=(ok,code)=>{if(!ok)throw new CommanderError(code);};
const cleanText=value=>typeof value==='string'?value.replace(/[\x00-\x1f\x7f]/g,'').slice(0,128):null;
const object=value=>value!==null&&typeof value==='object'&&!Array.isArray(value);
const noArgs={type:'object',properties:{},additionalProperties:false};
export const FABRIC_TOOLS=Object.freeze([
 {name:'nexus.host.resources',description:'Measure this executor CPU and memory. Does not grant or infer Administrator, Cloud, GPU or GUI access.',schema:noArgs},
 {name:'nexus.network.devices',description:'Read a bounded device inventory from the official Tailscale API. Network authorization is not remote shell or administrator authority.',schema:noArgs},
 {name:'nexus.desktop.status',description:'Report measured desktop backend readiness. A staged package is not a working GUI connection.',schema:noArgs},
 {name:'nexus.workload.plan',description:'Plan one local or cloud workload against measured capabilities and reserved memory. Does not start a process or provision a machine.',schema:{type:'object',properties:{kind:{type:'string',enum:['windows-cli','linux-cli','node','desktop-gui']},memoryMiB:{type:'integer',minimum:16,maximum:65536}},required:['kind'],additionalProperties:false}}
]);

export function measureResources(){return {observedAt:new Date().toISOString(),platform:process.platform,architecture:process.arch,logicalCpus:os.availableParallelism(),totalMemoryMiB:Math.floor(os.totalmem()/1048576),freeMemoryMiB:Math.floor(os.freemem()/1048576),localConcurrencyLimit:1,reserveMemoryMiB:256,administrator:'not_measured_by_this_operation',gpu:'not_measured_by_this_operation'};}

export function deviceProjection(raw,now=Date.now()){
 need(object(raw)&&Array.isArray(raw.devices),'invalid_network_response');
 return {observedAt:new Date(now).toISOString(),source:'tailscale-api',operation:'GET devices',readOnly:true,truncated:raw.devices.length>128,devices:raw.devices.slice(0,128).map(d=>({hostname:cleanText(d.hostname),os:cleanText(d.os),authorized:d.authorized===true,clientVersion:cleanText(d.clientVersion),expires:cleanText(d.expires),lastSeen:cleanText(d.lastSeen),ephemeral:typeof d.ephemeral==='boolean'?d.ephemeral:null})),executionAuthority:'not_attested_by_network_membership'};
}

export async function readTailscaleDevices(keyFile,{fetchImpl=fetch,signal,now=Date.now}={}){
 const stat=await fs.lstat(keyFile);
 need(stat.isFile()&&!stat.isSymbolicLink()&&stat.nlink===1&&stat.size>0&&stat.size<=4096,'credential_file_refused');
 let credential=(await fs.readFile(keyFile,'utf8')).trim();
 need(/^tskey-api-[A-Za-z0-9_-]+$/.test(credential),'credential_format_refused');
 const combined=AbortSignal.any([AbortSignal.timeout(15000),...(signal?[signal]:[])]);
 let response;
 try {response=await fetchImpl('https://api.tailscale.com/api/v2/tailnet/-/devices',{method:'GET',headers:{Authorization:'Bearer '+credential,Accept:'application/json'},redirect:'error',signal:combined});}
 catch {throw new CommanderError('network_unavailable');}
 finally {credential='';}
 need(response.status===200,'network_request_refused');
 const chunks=[];let size=0;
 try {
  for await(const chunk of response.body){size+=chunk.length;need(size<=1048576,'network_response_too_large');chunks.push(chunk);}
  return deviceProjection(JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(Buffer.concat(chunks))),now());
 }catch(e){if(e instanceof CommanderError)throw e;throw new CommanderError('invalid_network_response');}
}

export function planWorkload(args,local,remote=[],gui={state:'unavailable'},now=Date.now()){
 need(object(args)&&Object.keys(args).every(k=>['kind','memoryMiB'].includes(k)),'invalid_arguments');
 need(['windows-cli','linux-cli','node','desktop-gui'].includes(args.kind),'invalid_arguments');
 const memoryMiB=args.memoryMiB??128;
 need(Number.isSafeInteger(memoryMiB)&&memoryMiB>=16&&memoryMiB<=65536,'invalid_arguments');
 const age=now-Date.parse(local.observedAt);
 need(Number.isFinite(age)&&age>=0&&age<=60000,'stale_resource_observation');
 const base={kind:args.kind,memoryMiB,executes:false,provisions:false,privilege:'executor-specific; never inherited from network membership',localConcurrencyLimit:1};
 const windows=local.platform==='win32';
 const localCompatible=args.kind==='node'||(args.kind==='windows-cli'&&windows)||(args.kind==='linux-cli'&&local.platform==='linux')||(args.kind==='desktop-gui'&&windows&&gui.state==='verified');
 const available=Math.max(0,local.freeMemoryMiB-(local.reserveMemoryMiB??256));
 if(localCompatible&&Number.isFinite(available)&&available>=memoryMiB)return {...base,state:'local-candidate',host:'local',availableMemoryMiB:available,requires:'normal tool approval and current target validation'};
 const candidate=remote.find(r=>{
  const elapsed=now-Date.parse(r.observedAt);
  return r.executionVerified===true&&typeof r.evidenceSha256==='string'&&/^[a-f0-9]{64}$/.test(r.evidenceSha256)&&Number.isFinite(elapsed)&&elapsed>=0&&elapsed<=900000&&Array.isArray(r.kinds)&&r.kinds.includes(args.kind)&&Number.isFinite(r.availableMemoryMiB)&&r.availableMemoryMiB>=memoryMiB;
 });
 if(candidate)return {...base,state:'remote-candidate',host:cleanText(candidate.host),evidenceSha256:candidate.evidenceSha256,requires:'fresh authenticated remote executor; local files must be explicitly transferred'};
 return {...base,state:'held',reason:localCompatible?'insufficient_measured_capacity':'no_verified_compatible_executor',localAvailableMemoryMiB:available,wslStart:'never_automatic',cloudCpuPooling:false};
}

export function createFabricDispatcher({tailscaleKeyFile,resources=measureResources,network=readTailscaleDevices,guiStatus=()=>({state:'unavailable',reason:'no_verified_gui_backend'}),remoteExecutors=[]}){
 return async(name,args={},options={})=>{
  if(name!=='nexus.workload.plan')need(object(args)&&Object.keys(args).length===0,'invalid_arguments');
  switch(name){
   case 'nexus.host.resources':return resources();
   case 'nexus.network.devices':need(typeof tailscaleKeyFile==='string','network_not_configured');return network(tailscaleKeyFile,options);
   case 'nexus.desktop.status':return guiStatus();
   case 'nexus.workload.plan':return planWorkload(args,resources(),remoteExecutors,await guiStatus());
   default:throw new CommanderError('unknown_tool');
  }
 };
}
