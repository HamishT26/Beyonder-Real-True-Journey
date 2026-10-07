import fs from 'node:fs';
import path from 'node:path';
import {randomUUID} from 'node:crypto';
import {createInterface} from 'node:readline/promises';
import {clean,safeJson,runPlan,terminalOptions} from './core.mjs';
import {renderChatPanel} from './terminal-presentation.mjs';
import {listChats,readRegistry,resolveChat,chatPlan,admitChat,saveRegistry,normalizeEntry,recoveryCatalogue,localResumePickerPlan} from './chats.mjs';
import {listProfiles,readProfile,saveProfile,issueCertificate,verifyCertificate} from './identity.mjs';
import {listMemory,readMemory,saveMemory,exportMemory} from './memory-bank.mjs';
import {snapshotMemory,verifyMemorySnapshot,restoreMemorySnapshot} from './memory-snapshot.mjs';
import {sentinelTemplate,validateSentinel,saveSentinel,listSentinel,readSentinel,sentinelPlan} from './sentinel.mjs';
import {prepareRequest as prepareSentinelRequest,offlinePlan as sentinelApiPlan,providers as sentinelProviders} from './sentinel-runtime/src/contract.mjs';
import {FileLedger as SentinelLedger} from './sentinel-runtime/src/ledger.mjs';
import {labCatalogue,labPlan,runLab,existingLabPlan} from './laboratory.mjs';
import {remotePlan,saveRemote} from './remote.mjs';
import {nexusHome,readPrivate} from './private-store.mjs';
import {messagePlan,queueMessage,messageStatus,listMessages,claimMessage,recordMessageReceipt} from './messages.mjs';

export const NEXUS_COMMANDS=['chats','messages','identity','memory','lab','sentinel','remote'];
export const NEXUS_HELP=`\nGHC Family extension commands:\n  chats list [--refresh] [--limit 100] [--search TEXT]\n  chats recovery [--id UUID]\n  chats resolve|plan|open --id UUID [--execute]\n  chats import --file FILE --execute\n  messages list\n  messages show --id UUID\n  messages plan --file REQUEST-JSON\n  messages draft --file REQUEST-JSON --execute\n  messages queue --file REQUEST-JSON --execute\n  messages claim --id UUID --execute\n  messages receipt --file RECEIPT-JSON --execute\nMessage outbox has no automatic sender. An authorized existing agent claims once, sends through the native tool once, and records the result. Unknown outcomes require reconciliation.\n  identity list|show|certificate|verify --id NAME [--execute]\n  identity add --file FILE --execute\n  memory list|show --id NAME\n  memory add --file FILE --execute\n  memory export --id NAME[,NAME] --execute\n  memory snapshot --id NAME[,NAME] --execute\n  memory snapshot-verify --id UUID [--fingerprint SHA256]\n  memory restore --id UUID --fingerprint SHA256 --execute\n  lab catalogue|plan|run --id diffusion|queue|consent [--size 1000] [--execute]\n  lab serve --execute\n  sentinel template|list|show|validate|plan|save [--id NAME] [--file FILE] [--execute]\n  sentinel api-providers\n  sentinel api-validate --file REQUEST-JSON\n  sentinel api-plan --file REQUEST-JSON [--quote QUOTE-JSON]\n  remote plan|connect|configure [--file FILE] [--execute]\nEvery command accepts --json. Read/plan commands do not start a chat or model.\nExisting chats inherit their settings; deliberate model changes use their provider UI.\nUse the original provider UI for ChatGPT and managed-cloud chats that do not have a compatible CLI resume route.\n`;
function inputFile(file){if(typeof file!=='string'||!path.isAbsolute(file))throw new Error('An absolute input file is required');const s=fs.lstatSync(file);if(!s.isFile()||s.isSymbolicLink()||s.nlink>1||s.size>2097152)throw new Error('Invalid input file');return JSON.parse(fs.readFileSync(file,'utf8'));}
function requireExecute(values){if(!values.execute)throw new Error('Use --execute for this write or launch');}
export async function nexusCommand(group,verb,values,c){
 if(group==='messages'){
   if(verb==='list')return listMessages(c);
   if(verb==='show')return messageStatus(c,values.id,{includeBody:true});
   if(verb==='plan')return messagePlan(c,inputFile(values.file));
   requireExecute(values);
   if(verb==='draft')return queueMessage(c,inputFile(values.file),{draft:true});
   if(verb==='queue')return queueMessage(c,inputFile(values.file));
   if(verb==='claim')return claimMessage(c,values.id);
   if(verb==='receipt')return recordMessageReceipt(c,inputFile(values.file));
 }
 if(group==='chats'){
   if(verb==='recovery')return recoveryCatalogue(c,values.id);
   if(verb==='list')return listChats(c,{refresh:values.refresh===true,limit:values.limit?Number(values.limit):100,search:values.search||''});
   if(verb==='import'){requireExecute(values);const raw=inputFile(values.file);if(!Array.isArray(raw.entries))throw new Error('Invalid chat catalogue');const entries=raw.entries.map(r=>normalizeEntry(r,raw.source||r.source||'explicit import',raw.observedAt||r.observedAt||null));return saveRegistry(c,[...readRegistry(c),...entries]);}
   if(typeof values.id!=='string'||!values.id.trim())throw new Error('An exact chat ID or unique title is required; use --id');
   const selected=resolveChat(readRegistry(c),values.id);
   if(verb==='resolve')return selected;
   const p=chatPlan(selected,c,{override:values.override===true});if(verb==='plan')return p;
   if(verb==='open'){requireExecute(values);const admitted=await admitChat(c,selected);if(admitted.status!=='ready')return admitted;if(values.json&&admitted.interactive)throw new Error('Interactive actions require a real terminal');return runPlan(admitted,c);}
 }
 if(group==='identity'){
   if(verb==='list')return {profiles:listProfiles(c)};
   if(verb==='show')return readProfile(c,values.id);
   if(verb==='add'){requireExecute(values);return saveProfile(c,inputFile(values.file));}
   if(verb==='certificate'){requireExecute(values);return issueCertificate(c,values.id);}
   if(verb==='verify'){const cert=readPrivate(nexusHome(c),'certificates/'+safeId(values.id)+'.json');return verifyCertificate(cert,values.fingerprint);}
 }
 if(group==='memory'){
   if(verb==='list')return {records:listMemory(c),autoSync:false};
   if(verb==='show')return readMemory(c,values.id);
   if(verb==='add'){requireExecute(values);return saveMemory(c,inputFile(values.file));}
   if(verb==='export'){requireExecute(values);return exportMemory(c,String(values.id||'').split(','));}
   if(verb==='snapshot'){requireExecute(values);return snapshotMemory(c,String(values.id||'').split(','));}
   if(verb==='snapshot-verify')return verifyMemorySnapshot(c,values.id,{expectedDigest:values.fingerprint});
   if(verb==='restore'){requireExecute(values);return restoreMemorySnapshot(c,values.id,{expectedDigest:values.fingerprint});}
 }
 if(group==='lab'){
   if(verb==='catalogue')return labCatalogue(c);
   if(verb==='plan')return labPlan(c,values.id,{size:values.size?Number(values.size):1000});
   if(verb==='run'){requireExecute(values);return runLab(c,values.id,{size:values.size?Number(values.size):1000});}
   if(verb==='serve'){requireExecute(values);if(values.json)throw new Error('Interactive actions require a real terminal');return runPlan(existingLabPlan(c),c);}
 }
 if(group==='sentinel'){
   if(verb==='api-providers')return {providers:sentinelProviders(),networkCalls:0,liveModelStarted:false};
   if(verb==='api-validate'||verb==='api-plan'){
     const request=inputFile(values.file),prepared=prepareSentinelRequest(request);
     if(verb==='api-validate')return {valid:true,schema:'ghc.sentinel.request-validation.v1',provider:prepared.request.provider,model:prepared.request.model,requestSha256:prepared.requestSha256,networkCalls:0};
     let budget;try{budget=new SentinelLedger(path.join(nexusHome(c),'sentinel-runtime')).snapshot();}catch{budget={known:false};}
     return {...sentinelApiPlan(request,{quote:values.quote?inputFile(values.quote):null,budget}),liveModelStarted:false,helperApproval:'A request shown to Hamish and explicit approval are required before a new helper/model session'};
   }
   if(verb==='template')return sentinelTemplate(values.id||'sentinel-1');
   if(verb==='list')return {agents:listSentinel(c)};
   if(verb==='show')return readSentinel(c,values.id);
   const spec=values.file?inputFile(values.file):values.id?readSentinel(c,values.id):sentinelTemplate();
   if(verb==='validate')return validateSentinel(spec);
   if(verb==='plan')return sentinelPlan(spec);
   if(verb==='save'){requireExecute(values);return saveSentinel(c,spec);}
 }
 if(group==='remote'){
   if(verb==='configure'){requireExecute(values);return saveRemote(c,inputFile(values.file));}
   const p=remotePlan(c,values.file?inputFile(values.file):null);if(verb==='plan')return p;
   if(verb==='connect'){requireExecute(values);if(p.status!=='ready')return p;if(values.json)throw new Error('Interactive actions require a real terminal');return runPlan(p,c);}
 }
 throw new Error('Unknown Nexus command');
}
function safeId(value){if(typeof value!=='string'||!/^[a-z0-9][a-z0-9-]{0,79}$/.test(value))throw new Error('Invalid profile ID');return value;}
async function ask(prompt){const rl=createInterface({input:process.stdin,output:process.stdout});try{return (await rl.question(prompt)).trim();}finally{rl.close();}}
async function confirmPlan(p,c){console.log(safeJson(p,2));if(p.status!=='ready')return;if((await ask('Open this supported route? [y/N] ')).toLowerCase()==='y')console.log(safeJson(await runPlan(p,c),2));}
export async function chatMenu(c){
 let refresh=false,query='';
 while(true){
  const result=await listChats(c,{refresh,search:query});refresh=false;
  const display=terminalOptions();
  console.log(renderChatPanel(result,display));
  if(result.truncated)console.log('Showing '+result.entries.length+' of '+result.total+' records; filter or enter an exact ID.');
  if(result.cache?.status==='unavailable')console.log('The refreshed snapshot could not be saved; inspect the local private store before opening a newly found record.');
  console.log('\nM. Compose a private message draft (active agent relay required)\nO. Message outbox and delivery receipts\nR. Refresh local CLI/App and legacy cloud task metadata\nF. Filter titles or an exact ID\nI. Preserved chat IDs and recovery routes (offline)\nP. Official local CLI resume picker\nC. Official cloud task picker\n0. Back');
  const rawChoice=await ask('Select chat number, exact ID, or route: '),choice=rawChoice.toLowerCase();if(choice==='0'||choice==='q')return;
  if(display.columns<24){console.log('Widen the terminal before selecting a chat.');continue;}
  if(choice==='r'){refresh=true;continue;}
  if(choice==='o'){console.log(safeJson(listMessages(c),2));continue;}
  if(choice==='m'){
   const destination=await ask('Destination number or exact UUID: ');
   const matches=/^\d+$/.test(destination)?[result.entries[Number(destination)-1]].filter(Boolean):readRegistry(c).filter(e=>e.id.toLowerCase()===destination.toLowerCase());
   if(matches.length!==1){console.log('No unique exact destination.');continue;}
   const entry=matches[0],body=await ask('Message (one line; Enter cancels): ');if(!body)continue;
   console.log('To: '+clean(entry.title)+' | '+entry.id+' | '+clean(entry.hostId||'ChatGPT'));
   console.log('This saves a private draft for an active agent to relay. It does not send automatically.');
   if((await ask('Save this selected message to the outbox? [y/N] ')).toLowerCase()==='y')console.log(safeJson(queueMessage(c,{requestId:randomUUID(),toId:entry.id,body},{draft:true}),2));
   continue;
  }
  if(choice==='i'){console.log(safeJson(recoveryCatalogue(c),2));continue;}
  if(choice==='p'){await confirmPlan(localResumePickerPlan(c),c);continue;}
  if(choice==='f'){query=await ask('Title text or exact ID (empty clears filter): ');continue;}
  if(choice==='c'){await confirmPlan({status:'ready',action:'chat-picker',command:c.codex,args:['cloud'],cwd:c.cwd,interactive:true,shell:false,note:'Official provider picker for legacy cloud tasks; no existing local or held CLI session is selected by the hub.'},c);continue;}
  let selected;if(/^\d+$/.test(choice))selected=result.entries[Number(choice)-1];else try{selected=resolveChat(readRegistry(c),rawChoice);}catch{console.log('No unique matching saved chat; use its exact ID.');continue;}
  if(!selected)continue;console.log(safeJson({selection:{id:selected.id,title:selected.title,hostId:selected.hostId,kind:selected.kind},plan:chatPlan(selected,c)},2));if((await ask('Check the current provider state and open this existing route? [y/N] ')).toLowerCase()==='y'){const admitted=await admitChat(c,selected);if(admitted.status==='ready')console.log(safeJson(await runPlan(admitted,c),2));else console.log(safeJson(admitted,2));}
 }
}
export async function workbenchMenu(group,c){
 console.log('\n'+({lab:'GHC-Family Laboratory',identity:'GHC-Family Freed ID certificates',memory:'GHC-Family Spaces / Filesystem Memory bank',sentinel:'GHC-Family Sentinel-1 Agent builder',remote:'GHC-Family persistent remote terminal'}[group]));
 if(group==='lab'){
   console.log(safeJson(labCatalogue(c),2));const choice=await ask('Model ID to run, S for existing laboratory server, or Enter to return: ');if(!choice)return;
   if(choice.toLowerCase()==='s'){await confirmPlan(existingLabPlan(c),c);return;}
   const size=Number(await ask('Iterations (1–200000; 1000 is a light local check): '));const p=labPlan(c,choice,{size});console.log(safeJson(p,2));if((await ask('Run this finite experiment? [y/N] ')).toLowerCase()==='y')console.log(safeJson(await runLab(c,choice,{size}),2));return;
 }
 if(group==='identity'){const all=listProfiles(c);all.forEach(p=>console.log(p.id.padEnd(24)+' '+clean(p.name).slice(0,30)+' — '+clean(p.role||'Role not yet recorded').slice(0,65)));const id=await ask('Profile ID to view, or Enter to return: ');if(!id)return;console.log(safeJson(readProfile(c,id),2));if((await ask('Issue a local integrity certificate for this project profile? [y/N] ')).toLowerCase()==='y')console.log(safeJson(issueCertificate(c,id),2));return;}
 if(group==='memory'){console.log(safeJson({records:listMemory(c),home:nexusHome(c),note:'Personal contacts and signing keys are outside the exportable memory collection. Selected exports need an explicit command.'},2));return;}
 if(group==='sentinel'){console.log(safeJson({agents:listSentinel(c),template:sentinelTemplate(),plan:sentinelPlan(sentinelTemplate())},2));const id=await ask('New draft ID to save, or Enter to return: ');if(id)console.log(safeJson(saveSentinel(c,sentinelTemplate(id)),2));return;}
 if(group==='remote'){await confirmPlan(remotePlan(c),c);}
}
