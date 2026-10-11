import fs from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';
import {TextDecoder} from 'node:util';
import {StringDecoder} from 'node:string_decoder';

export const ADMIN_VERSION = '2.9.0';
export const LIMITS = Object.freeze({file:8192, command:4096, output:8192, entries:64, requests:128, timeout:30000});
const digest = data => crypto.createHash('sha256').update(data).digest('hex');
const shaPattern = /^[a-f0-9]{64}$/;
const aliasPattern = /^[a-z][a-z0-9_-]{0,31}$/;
const idPattern = /^[a-f0-9-]{36}$/;
const blocked = /^(?:\.(?:git|codex|ssh|aws|azure|gnupg)|\.env(?:\..*)?|private|secrets?|credentials?|auth\.json|config\.toml|id_rsa|id_ed25519|.*\.(?:pem|p12|pfx|key))$/i;
const secret = /(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(?:Bearer\s+)[A-Za-z0-9._~+\/-]{12,})/g;
const decoder = new TextDecoder('utf-8',{fatal:true});
export class CommanderError extends Error {constructor(code){super(code);this.code=code;}}
function need(ok,code='invalid_arguments'){if(!ok)throw new CommanderError(code);}
function object(value){return value!==null&&typeof value==='object'&&!Array.isArray(value);}
function shape(args,keys){need(object(args)&&Object.keys(args).every(k=>keys.includes(k)));}
function contained(root,target){const rel=path.relative(root,target);return rel===''||(!path.isAbsolute(rel)&&rel!=='..'&&!rel.startsWith('..'+path.sep));}
function samePath(a,b){return process.platform==='win32'?path.resolve(a).toLowerCase()===path.resolve(b).toLowerCase():path.resolve(a)===path.resolve(b);}
function relative(value,empty=false){
 need(typeof value==='string'&&(empty||value.length>0)&&value.length<=512&&!/[\\:\x00-\x1f\x7f]/.test(value));
 if(value==='')return [];
 const parts=value.split('/');
 need(parts.every(p=>p!==''&&p!=='.'&&p!=='..'&&!/[. ]$/.test(p)&&!/[<>"|?*]/.test(p)&&!blocked.test(p)&&! /^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(p)),'path_refused');
 return parts;
}
function noSecret(text){secret.lastIndex=0;need(!secret.test(text),'sensitive_content_refused');}
export function redact(text){secret.lastIndex=0;return text.replace(secret,'[REDACTED]');}
async function hashFile(file){const h=crypto.createHash('sha256');for await(const bytes of createReadStream(file,{highWaterMark:1024*1024}))h.update(bytes);return h.digest('hex');}
async function boundedRead(file,max=LIMITS.file){const s=await fs.lstat(file);need(s.isFile()&&!s.isSymbolicLink()&&s.nlink===1&&s.size<=max,'file_refused');const h=await fs.open(file,'r');try{const now=await h.stat();need(now.dev===s.dev&&now.ino===s.ino&&now.nlink===1&&now.size<=max,'file_changed');const b=Buffer.alloc(max+1);const {bytesRead}=await h.read(b,0,b.length,0);need(bytesRead<=max,'file_too_large');return b.subarray(0,bytesRead);}finally{await h.close();}}
async function writeExclusive(file,data){const h=await fs.open(file,'wx',0o600);try{await h.writeFile(data);await h.sync();}finally{await h.close();}}
async function plainDirectory(dir){const stat=await fs.lstat(dir);need(stat.isDirectory()&&!stat.isSymbolicLink(),'directory_refused');const real=await fs.realpath(dir);need(samePath(real,dir),'reparse_refused');}

export async function loadAdminPolicy(file){
 const bytes=await boundedRead(file,32768);let policy;try{policy=JSON.parse(decoder.decode(bytes));}catch{throw new CommanderError('invalid_policy');}
 need(policy.schema==='ghc.admin.policy.v1'&&policy.enabled===true&&Array.isArray(policy.roots)&&policy.roots.length>0&&policy.roots.length<=8,'policy_disabled');
 need(typeof policy.stateDirectory==='string'&&path.isAbsolute(policy.stateDirectory),'invalid_policy');
 const roots=new Map();
 for(const r of policy.roots){need(object(r)&&aliasPattern.test(r.alias)&&!roots.has(r.alias)&&path.isAbsolute(r.path)&&typeof r.write==='boolean','invalid_policy');await plainDirectory(r.path);roots.set(r.alias,{path:path.resolve(r.path),write:r.write});}
 await plainDirectory(policy.stateDirectory);
 for(const r of roots.values())need(!contained(r.path,path.resolve(policy.stateDirectory))&&!contained(r.path,path.resolve(file)),'private_state_exposed');
 const shells=new Map();
 for(const [name,s] of Object.entries(policy.shells??{})){need(['cmd','powershell','node','linux'].includes(name)&&object(s)&&path.isAbsolute(s.path)&&shaPattern.test(s.sha256),'invalid_shell');shells.set(name,Object.freeze({...s}));}
 return Object.freeze({roots,shells,stateDirectory:path.resolve(policy.stateDirectory),sha256:digest(bytes),file:path.resolve(file)});
}

export function createAdminCommander(policy,{spawnImpl=spawn,now=()=>Date.now()}={}){
 let active=false;let held=false;
 async function currentPolicy(){need(digest(await boundedRead(policy.file,32768))===policy.sha256,'policy_changed');}
 async function target(alias,rel,{write=false,missing=false,directory=false}={}){
  need(aliasPattern.test(alias)&&policy.roots.has(alias),'unknown_root');const root=policy.roots.get(alias);need(!write||root.write,'read_only_root');const parts=relative(rel,directory);await plainDirectory(root.path);let value=root.path;
  for(let i=0;i<parts.length;i++){value=path.join(value,parts[i]);need(contained(root.path,value),'path_refused');let s;try{s=await fs.lstat(value);}catch(e){if(e.code==='ENOENT'&&missing&&i===parts.length-1)return value;throw new CommanderError('path_missing');}need(!s.isSymbolicLink(),'link_refused');if(i<parts.length-1||directory)need(s.isDirectory(),'directory_required');else need(s.isFile()&&s.nlink===1,'file_refused');const real=await fs.realpath(value);need(contained(root.path,real)&&samePath(real,value),'reparse_refused');}
  return value;
 }
 async function requestPath(id){need(idPattern.test(id),'invalid_request');await plainDirectory(policy.stateDirectory);const dir=path.join(policy.stateDirectory,id);await plainDirectory(dir);return dir;}
 async function readRequest(id){const dir=await requestPath(id);const bytes=await boundedRead(path.join(dir,'request.json'),16384);const value=JSON.parse(decoder.decode(bytes));need(value.id===id&&value.policySha256===policy.sha256,'request_changed');need(value.expiresAt>now(),'request_expired');return {dir,value,sha256:digest(bytes)};}
 async function status(){return {version:ADMIN_VERSION,platform:process.platform,roots:[...policy.roots].map(([alias,r])=>({alias,write:r.write})),shells:[...policy.shells.keys()],execution:'exact_local_approval_required',held,gui:'use_supported_computer_use_tool',policySha256:policy.sha256,adminToken:'not_measured_by_this_operation'};}
 async function list(args){shape(args,['root','path']);const dir=await target(args.root,args.path??'',{directory:true});const safe=[];let scanned=0;let truncated=false;for await(const e of await fs.opendir(dir)){if(++scanned>256||safe.length===LIMITS.entries){truncated=true;break;}if(!blocked.test(e.name)&&!e.isSymbolicLink())safe.push({name:e.name,type:e.isDirectory()?'directory':e.isFile()?'file':'other'});}safe.sort((a,b)=>a.name.localeCompare(b.name));return {root:args.root,path:args.path??'',entries:safe,truncated};}
 async function read(args){shape(args,['root','path']);const file=await target(args.root,args.path);const bytes=await boundedRead(file);let text;try{text=decoder.decode(bytes);}catch{throw new CommanderError('text_required');}noSecret(text);return {root:args.root,path:args.path,bytes:bytes.length,sha256:digest(bytes),text};}
 async function write(args,{signal}={}){
  shape(args,['root','path','text','expectedSha256']);need(typeof args.text==='string'&&Buffer.byteLength(args.text)<=LIMITS.file,'file_too_large');noSecret(args.text);need(args.expectedSha256===null||shaPattern.test(args.expectedSha256),'expected_hash_required');
  const file=await target(args.root,args.path,{write:true,missing:args.expectedSha256===null});const bytes=Buffer.from(args.text);let before;
  let backupId=null;need(!signal?.aborted,'cancelled');
  if(args.expectedSha256===null){await writeExclusive(file,bytes);}
  else{
   before=await boundedRead(file);need(digest(before)===args.expectedSha256,'stale_file');
   const backupDir=path.join(policy.stateDirectory,'file-backups');await fs.mkdir(backupDir,{recursive:true,mode:0o700});await plainDirectory(backupDir);backupId=crypto.randomUUID();await writeExclusive(path.join(backupDir,backupId+'.bin'),before);await writeExclusive(path.join(backupDir,backupId+'.json'),JSON.stringify({root:args.root,path:args.path,sha256:digest(before),at:now()})+'\n');
   const tmp=file+'.ghc-'+crypto.randomUUID()+'.tmp';
   await writeExclusive(tmp,bytes);
   try{await target(args.root,args.path,{write:true});need(digest(await boundedRead(file))===args.expectedSha256,'stale_file');need(!signal?.aborted,'cancelled');await fs.rename(tmp,file);}finally{await fs.unlink(tmp).catch(e=>{if(e.code!=='ENOENT')throw e;});}
  }
  const actual=await boundedRead(file);need(actual.equals(bytes),'write_unverified');return {root:args.root,path:args.path,bytes:actual.length,sha256:digest(actual),previousSha256:before?digest(before):null,backupId,written:true};
 }
 async function prepare(args){
  shape(args,['shell','command','root','directory','timeoutMs']);need(policy.shells.has(args.shell),'unsupported_shell');need(typeof args.command==='string'&&args.command.trim().length>0&&Buffer.byteLength(args.command)<=LIMITS.command&&!args.command.includes('\0'),'invalid_command');noSecret(args.command);
  const timeoutMs=args.timeoutMs??10000;need(Number.isInteger(timeoutMs)&&timeoutMs>=100&&timeoutMs<=LIMITS.timeout,'invalid_timeout');await target(args.root,args.directory??'',{directory:true});
  const dirs=await fs.readdir(policy.stateDirectory);need(dirs.filter(n=>idPattern.test(n)).length<LIMITS.requests,'request_capacity');const id=crypto.randomUUID();const dir=path.join(policy.stateDirectory,id);await fs.mkdir(dir,{mode:0o700});
  const value={schema:'ghc.admin.request.v1',id,policySha256:policy.sha256,shell:args.shell,command:args.command,root:args.root,directory:args.directory??'',timeoutMs,createdAt:now(),expiresAt:now()+15*60*1000};const bytes=Buffer.from(JSON.stringify(value,null,2)+'\n');await writeExclusive(path.join(dir,'request.json'),bytes);
  return {id,sha256:digest(bytes),state:'awaiting_local_approval',expiresAt:value.expiresAt,review:{shell:value.shell,command:value.command,root:value.root,directory:value.directory,timeoutMs},warning:'An approved command uses the server OS token; file roots are not a command sandbox.'};
 }
 async function approve(id,expectedSha256){await currentPolicy();need(shaPattern.test(expectedSha256),'expected_hash_required');const r=await readRequest(id);need(r.sha256===expectedSha256,'request_changed');const bin=policy.shells.get(r.value.shell);need(bin&&await hashFile(bin.path)===bin.sha256,'executable_changed');need(r.value.expiresAt>now(),'request_expired');await writeExclusive(path.join(r.dir,'approval.json'),JSON.stringify({requestSha256:r.sha256,policySha256:policy.sha256,at:now()})+'\n');return {id,sha256:r.sha256,approved:true};}
 async function execute(args,{signal}={}){
  shape(args,['id','sha256']);need(shaPattern.test(args.sha256),'expected_hash_required');const r=await readRequest(args.id);need(r.sha256===args.sha256,'request_changed');let approval;try{approval=JSON.parse(decoder.decode(await boundedRead(path.join(r.dir,'approval.json'))));}catch{throw new CommanderError('local_approval_required');}
  need(approval.requestSha256===r.sha256&&approval.policySha256===policy.sha256,'approval_changed');const bin=policy.shells.get(r.value.shell);need(bin&&await hashFile(bin.path)===bin.sha256,'executable_changed');const cwd=await target(r.value.root,r.value.directory,{directory:true});need(!signal?.aborted,'cancelled');need(r.value.expiresAt>now(),'request_expired');await currentPolicy();
  try{await writeExclusive(path.join(r.dir,'claim.json'),JSON.stringify({at:now(),requestSha256:r.sha256})+'\n');}catch(e){if(e.code==='EEXIST')throw new CommanderError('already_claimed');throw e;}
  const shellArgs={cmd:['/d','/s','/c',r.value.command],powershell:['-NoLogo','-NoProfile','-NonInteractive','-Command',r.value.command],node:['-e',r.value.command],linux:['--noprofile','--norc','-c',r.value.command]}[r.value.shell];
  const env=Object.fromEntries(Object.entries(process.env).filter(([k])=>/^(SystemRoot|WINDIR|PATH|PATHEXT|COMSPEC|TEMP|TMP|USERPROFILE|HOME|LANG|LC_ALL)$/i.test(k)));
  const result=await new Promise(resolve=>{
   let child;let total=0;let out='';let err='';let reason=null;let settled=false;let timer;let killTimer;let killer;let fallbackTimer;const decOut=new StringDecoder('utf8');const decErr=new StringDecoder('utf8');
   const finish=(exit,signalName,closed=true)=>{if(settled)return;settled=true;clearTimeout(timer);clearTimeout(killTimer);clearTimeout(fallbackTimer);signal?.removeEventListener('abort',abort);resolve({id:args.id,requestSha256:r.sha256,exitCode:exit??null,signal:signalName??null,reason,stdout:redact(out+decOut.end()),stderr:redact(err+decErr.end()),outputBytesObserved:total,childClosed:closed,retry:'never_automatic',executed:!!child?.pid});};
   const fallback=()=>{try{child?.kill('SIGKILL');}catch{}};
   const stop=why=>{if(reason)return;reason=why;if(child?.pid&&child.exitCode===null){if(process.platform==='win32'){try{killer=spawnImpl(path.join(process.env.SystemRoot??'C:/Windows','System32/taskkill.exe'),['/PID',String(child.pid),'/T','/F'],{windowsHide:true,stdio:'ignore',env});killer.on('error',fallback);killer.on('exit',code=>{if(code!==0)fallback();});}catch{fallback();}}else{try{process.kill(-child.pid,'SIGKILL');}catch{fallback();}}fallbackTimer=setTimeout(fallback,3000);killTimer=setTimeout(()=>{held=true;try{killer?.kill();}catch{}child.stdout?.destroy();child.stderr?.destroy();child.unref();finish(null,null,false);},5000);}else finish(child?.exitCode,null);};
   const abort=()=>stop('cancelled');
   try{child=spawnImpl(bin.path,shellArgs,{cwd,env,windowsHide:true,stdio:['ignore','pipe','pipe'],detached:process.platform!=='win32'});child.stdout.on('data',b=>{total+=b.length;if(total<=LIMITS.output)out+=decOut.write(b);else stop('output_limit');});child.stderr.on('data',b=>{total+=b.length;if(total<=LIMITS.output)err+=decErr.write(b);else stop('output_limit');});child.on('error',()=>{reason='spawn_failed';finish(null,null);});child.on('close',finish);signal?.addEventListener('abort',abort,{once:true});timer=setTimeout(()=>stop('timeout'),r.value.timeoutMs);if(signal?.aborted)abort();}catch{reason='spawn_failed';finish(null,null);}
  });
  if(!result.childClosed)await writeExclusive(path.join(policy.stateDirectory,'HALTED.json'),JSON.stringify({reason:'child_close_unconfirmed',id:args.id,at:now()})+'\n');
  await writeExclusive(path.join(r.dir,'receipt.json'),JSON.stringify({...result,stdout:undefined,stderr:undefined,at:now()})+'\n');return result;
 }
 async function receipt(args){shape(args,['id']);const dir=await requestPath(args.id);try{return JSON.parse(decoder.decode(await boundedRead(path.join(dir,'receipt.json'))));}catch(e){if(e.code!=='ENOENT')throw e;let claimed=false;try{await fs.stat(path.join(dir,'claim.json'));claimed=true;}catch{}return {id:args.id,state:claimed?'claimed_outcome_unknown':'not_executed',retry:'never_automatic'};}}
 const operations={'nexus.admin.status':status,'nexus.files.list':list,'nexus.files.read':read,'nexus.files.write':write,'nexus.exec.prepare':prepare,'nexus.exec.execute':execute,'nexus.exec.receipt':receipt};
 async function dispatch(name,args,context={}){need(Object.hasOwn(operations,name),'unknown_tool');need(!active,'busy');active=true;try{need(!context.signal?.aborted,'cancelled');await currentPolicy();try{await fs.lstat(path.join(policy.stateDirectory,'HALTED.json'));held=true;}catch(e){if(e.code!=='ENOENT')throw e;}need(!held||name==='nexus.admin.status'||name==='nexus.exec.receipt','operator_reconciliation_required');return await operations[name](args,context);}finally{active=false;}}
 return Object.freeze({dispatch,approve,status});
}

const text={type:'string'};const alias={type:'string',pattern:aliasPattern.source};const rel={type:'string',maxLength:512};
const schema=(properties,required=[])=>({type:'object',properties,required,additionalProperties:false});
export const ADMIN_TOOLS=Object.freeze([
 {name:'nexus.admin.status',description:'Report reviewed roots, command approval mode and server capabilities.',schema:schema({}),readOnly:true},
 {name:'nexus.files.list',description:'List at most64 entries inside a reviewed root.',schema:schema({root:alias,path:rel},['root']),readOnly:true},
 {name:'nexus.files.read',description:'Read at most8192 bytes of ordinary UTF-8 text, excluding credential stores.',schema:schema({root:alias,path:rel},['root','path']),readOnly:true},
 {name:'nexus.files.write',description:'Write bounded UTF-8 text. Null expectedSha256 creates exclusively; replacements require the exact existing digest.',schema:schema({root:alias,path:rel,text:{...text,maxLength:8192},expectedSha256:{type:['string','null']}},['root','path','text','expectedSha256']),readOnly:false},
 {name:'nexus.exec.prepare',description:'Prepare an exact terminal request. Execution requires a separate local approval; this does not run a command.',schema:schema({shell:{type:'string',enum:['cmd','powershell','node','linux']},command:{...text,maxLength:4096},root:alias,directory:rel,timeoutMs:{type:'integer',minimum:100,maximum:30000}},['shell','command','root']),readOnly:false},
 {name:'nexus.exec.execute',description:'Execute a previously approved exact request once using the server OS token. No automatic retries.',schema:schema({id:text,sha256:text},['id','sha256']),readOnly:false},
 {name:'nexus.exec.receipt',description:'Read a command outcome without re-executing it; stdout and stderr are not persisted.',schema:schema({id:text},['id']),readOnly:true}
]);
