'use strict';
// Five logical checks, one optional PreToolUse handler. No subprocesses or writes.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const LIMIT=32768;
const CONFIG_KEYS=new Set(['tui.alternate_screen','tui.animations','hide_agent_reasoning']);
const HUB='D:/GHC-Archives/global-tools/ghc-nexus-hub/hub.mjs';
const notices={
 source_manifest:'Nexus source pin is unavailable or differs from the reviewed runtime. Reconcile the selected installation before executing; a source-tree change is not an installed update.',
 config_schema:'Nexus config proposal uses an unsupported key or value. Use the Config Menu allowlist and selected-layer hash/conflict review.',
 secret_export:'Nexus export contains a sensitive-looking literal or lacks a bounded selected-record list. Review selected nonsecret records; never export credentials or raw histories.',
 selected_route:'Nexus route is unknown, compound, missing an exact selection or missing --execute. Inspect one supported plan and preserve its host/provider/admission boundary.',
 budget_admission:'Nexus finite-job size is outside 1–200000 or malformed. Use a small admitted size. Paid work also needs the remaining aggregate USD50 budget; this check does not read billing.'
};
function tokenize(text){
 const out=[];let word='',quote=null;
 for(let i=0;i<text.length;i++){let c=text[i];if(quote){if(c===quote)quote=null;else word+=c;continue}
  if(c==='"'||c==="'"){quote=c;continue}
  if(/[;|<>`\r\n$]/.test(c))return null;
  if(/\s/.test(c)){if(word){out.push(word);word=''};continue}word+=c;
 }
 if(quote)return null;if(word)out.push(word);if(out[0]==='&')out.shift();
 if(out.some(t=>t==='&'||t==='&&'))return null;
 return out;
}
function option(args,name){const values=[];for(let i=0;i<args.length;i++){if(args[i]===name)values.push(args[i+1]);else if(args[i].startsWith(name+'='))values.push(args[i].slice(name.length+1))}return values.length===1?values[0]:null}
function sensitive(text){return /\bsk-[A-Za-z0-9_-]{16,}|\b(?:Bearer|authorization)\s*[:= ]\s*\S{12,}|\b(?:auth\.json|cookies\.sqlite|state_\d+\.sqlite)\b/i.test(text)}
function checkPins(root,pins){
 try{for(const pin of pins){if(!/^[a-z0-9-]+\.mjs$/.test(pin.path))return false;let p=path.join(root,pin.path),s=fs.lstatSync(p);if(!s.isFile()||s.isSymbolicLink()||s.nlink!==1||s.size>65536)return false;for(let d=path.dirname(p);;d=path.dirname(d)){if(fs.lstatSync(d).isSymbolicLink())return false;if(path.dirname(d)===d)break}let b=fs.readFileSync(p);if(b.length>65536||crypto.createHash('sha256').update(b).digest('hex')!==pin.sha256)return false}return true}catch{return false}
}
function evaluate(payload,{sourceCheck=()=>true,actions=[]}={}){
 if(!payload||payload.hook_event_name!=='PreToolUse'||!['Bash','exec_command'].includes(payload.tool_name))return [];
 const command=payload.tool_input?.command??payload.tool_input?.cmd;
 if(typeof command!=='string'||command.length>LIMIT||!/(?:ghc-nexus|ghc-nexus-hub[\\/]hub\.mjs|config_menu\.py)/i.test(command))return [];
 const findings=[],tokens=tokenize(command);
 const add=id=>{if(!findings.includes(id))findings.push(id)};
 if(sensitive(command))add('secret_export');
 if(!tokens){add('selected_route');return findings}
 const normalized=tokens.map(t=>t.replaceAll('\\','/'));
 const hubIndex=normalized.findIndex(t=>t.toLowerCase()===HUB.toLowerCase());
 const aliasIndex=normalized.findIndex(t=>/^(?:.*\/)?ghc-nexus(?:\.ps1|\.cmd)?$/i.test(t));
 const configIndex=normalized.findIndex(t=>/(?:^|\/)config_menu\.py$/.test(t));
 if(configIndex>=0){
  const args=tokens.slice(configIndex+1);
  if(args[0]==='propose'){
   const settings=[];for(let i=0;i<args.length;i++)if(args[i]==='--set')settings.push(args[++i]);else if(args[i].startsWith('--set='))settings.push(args[i].slice(6));
   if(!settings.length)add('config_schema');
   for(const s of settings){if(typeof s!=='string'||!s.includes('=')){add('config_schema');continue}const split=s.indexOf('='),k=s.slice(0,split);let v;try{v=JSON.parse(s.slice(split+1))}catch{add('config_schema');continue}if(!CONFIG_KEYS.has(k)||(k==='tui.alternate_screen'?!['auto','always','never'].includes(v):typeof v!=='boolean'))add('config_schema')}
  }
  return findings;
 }
 if(hubIndex<0&&aliasIndex<0)return findings;
 const args=tokens.slice((hubIndex>=0?hubIndex:aliasIndex)+1),[group,verb]=args;
 const mutating=group==='run'||(['chats','lab','memory','identity','remote','sentinel'].includes(group)&&['open','run','serve','export','add','certificate','configure','connect','save','import','snapshot','restore'].includes(verb))||(group==='messages'&&['draft','queue','claim','receipt'].includes(verb));
 if(mutating){if(hubIndex<0||!sourceCheck())add('source_manifest');if(!args.includes('--execute'))add('selected_route')}
 if(['plan','run'].includes(group)&&!actions.includes(verb))add('selected_route');
 if(group==='chats'&&['resolve','plan','open'].includes(verb)&&!option(args,'--id'))add('selected_route');
 if(group==='study'){
  if(verb!=='search'||!option(args,'--file')||!option(args,'--search')||!/^[0-9a-f]{64}$/.test(option(args,'--fingerprint')||'')||args.includes('--execute'))add('selected_route');
 }
 if(group==='messages'){
  if(!['list','show','plan','draft','queue','claim','receipt'].includes(verb))add('selected_route');
  if(['plan','draft','queue','receipt'].includes(verb)&&!option(args,'--file'))add('selected_route');
  if(['show','claim'].includes(verb)&&!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(option(args,'--id')||''))add('selected_route');
 }
 if(group==='memory'&&verb==='export'){const ids=option(args,'--id');if(!ids||!ids.split(',').every(x=>/^[a-z0-9][a-z0-9-]{0,79}$/.test(x))||ids.split(',').length>30||new Set(ids.split(',')).size!==ids.split(',').length)add('secret_export')}
 if(group==='lab'&&['run','plan'].includes(verb)){const raw=option(args,'--size');if(args.some(a=>a==='--size'||a.startsWith('--size='))&&(raw===null||!/^\d+$/.test(raw)||Number(raw)<1||Number(raw)>200000))add('budget_admission')}
 return findings;
}
function output(findings){return findings.length?{systemMessage:findings.map(f=>notices[f]).join('\n')}:{};}
function main(){
 let chunks=[],size=0,finished=false;
 const finish=value=>{if(finished)return;finished=true;clearTimeout(timer);process.stdin.destroy();process.stdout.write(JSON.stringify(value)+'\n')};
 const timer=setTimeout(()=>finish({systemMessage:'Nexus preflight input did not finish; no check result is available.'}),1000);
 process.stdin.on('data',chunk=>{size+=chunk.length;if(size>LIMIT){finish({systemMessage:'Nexus preflight input exceeded its bound; no check result is available.'});return}chunks.push(chunk)});
 process.stdin.on('error',()=>finish({}));
 process.stdin.on('end',()=>{try{const p=JSON.parse(Buffer.concat(chunks).toString('utf8'));const pinPath=path.join(__dirname,'../references/hub-source.json');const stat=fs.lstatSync(pinPath);if(!stat.isFile()||stat.isSymbolicLink()||stat.size>32768)throw Error('invalid pin file');const spec=JSON.parse(fs.readFileSync(pinPath,'utf8'));finish(output(evaluate(p,{actions:spec.actions,sourceCheck:()=>checkPins(spec.installedRoot,spec.files)})))}catch{finish({})}});
}
module.exports={evaluate,output,tokenize,checkPins,notices};
if(require.main===module)main();
