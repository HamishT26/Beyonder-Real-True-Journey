#!/usr/bin/env node
import {parseArgs} from 'node:util';
import {createInterface} from 'node:readline/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {ACTIONS,VERSION,MIN_NODE,clean,context,plan,runPlan,doctor,journal,safeJson} from './core.mjs';
import {NEXUS_COMMANDS,NEXUS_HELP,nexusCommand,chatMenu,workbenchMenu} from './nexus.mjs';
import {terminalOptions} from './core.mjs';
import {renderMenu} from './terminal-presentation.mjs';

export function publicError(error){
 const fixed=["An exact chat ID or unique title is required; use --id","Chat not found","Ambiguous chat selection","Chat limit must be 1 to 100","Unknown laboratory model","Laboratory size must be 1 to 200000","Existing chat settings must be inherited","Unsupported option for this command; use --help"].concat(['Unknown action','Unknown command','Unexpected positional argument','Use --execute to run the displayed action, or use plan','An exact existing session UUID is required','Invalid environment ID','This action requires the Windows host','Reviewed Windows launcher is unavailable','Required executable is unavailable on this host','This action requires an interactive terminal; use plan or machine commands in an agent tool','Interactive actions require a terminal without --json; use plan --json to inspect them','Menu requires a terminal without --json. Agents can use doctor, actions, plan and run --json','Node 20 or later is required']);
 if(fixed.includes(error?.message))return {status:'error',code:'invalid_action',message:error.message};
 if(error?.code?.startsWith('ERR_PARSE_ARGS'))return {status:'error',code:'invalid_arguments',message:'Unknown or invalid arguments; use --help for the supported interface'};
 return {status:'error',code:'operation_unavailable',message:'Operation unavailable; check the selected host and required tools. No raw exception or credential data is displayed.'};
}

export function validateCommandOptions(cmd,verb,values){
 const matrix={
 chats:{list:['refresh','limit','search'],recovery:['id'],import:['file','execute'],resolve:['id'],plan:['id','override'],open:['id','execute']},
 messages:{list:[],show:['id'],plan:['file'],draft:['file','execute'],queue:['file','execute'],claim:['id','execute'],receipt:['file','execute']},
 identity:{list:[],show:['id'],add:['file','execute'],certificate:['id','execute'],verify:['id','fingerprint']},
 memory:{list:[],show:['id'],add:['file','execute'],export:['id','execute'],snapshot:['id','execute'],'snapshot-verify':['id','fingerprint'],restore:['id','fingerprint','execute']},
 lab:{catalogue:[],plan:['id','size'],run:['id','size','execute'],serve:['execute']},
 sentinel:{template:['id'],list:[],show:['id'],validate:['id','file'],plan:['id','file'],save:['id','file','execute'],'api-providers':[],'api-validate':['file'],'api-plan':['file','quote']},
 remote:{plan:['file'],connect:['file','execute'],configure:['file','execute']}
 };
 let specific=matrix[cmd]?.[verb]||[];
 if(cmd==='run'||cmd==='plan')specific=[...(cmd==='run'?['execute']:[]),...(verb==='codex-resume'?['session']:[]),...(verb==='cloud-list'?['env']:[])];
 const allowed=new Set(['json',...specific]);
 if(Object.keys(values).some(k=>!allowed.has(k)))throw new Error('Unsupported option for this command; use --help');
}

export async function main(argv=process.argv.slice(2)) {
  if(Number(process.versions.node.split('.')[0])<MIN_NODE)throw new Error('Node 20 or later is required');
  const {values,positionals}=parseArgs({args:argv,allowPositionals:true,strict:true,options:{json:{type:'boolean'},execute:{type:'boolean'},session:{type:'string'},env:{type:'string'},help:{type:'boolean'},version:{type:'boolean'},id:{type:'string'},file:{type:'string'},limit:{type:'string'},search:{type:'string'},refresh:{type:'boolean'},size:{type:'string'},override:{type:'boolean'},fingerprint:{type:'string'},quote:{type:'string'}}});
  const output=value=>console.log(safeJson(value,values.json?undefined:2));
  if(values.version){output({name:'GHC Nexus Hub',version:VERSION});return;}
  if(values.help||positionals[0]==='help') { const help='GHC Nexus Hub\n\nnode hub.mjs [menu]\nnode hub.mjs doctor --json\nnode hub.mjs actions --json\nnode hub.mjs plan ACTION [--session UUID (codex-resume only)] [--env ID (cloud-list only)] --json\nnode hub.mjs run ACTION --execute [--session UUID (codex-resume only)] [--env ID (cloud-list only)] --json\n\nActions: '+ACTIONS.join(', ')+'\n\nPlans do not execute. Interactive shell/sign-in/Codex actions need a real terminal.\nThe hub never copies tokens or upgrades a managed app-server.'+NEXUS_HELP; if(values.json)output({help,actions:ACTIONS,commands:NEXUS_COMMANDS});else console.log(help);return; }
  const cmd=positionals[0]||'menu';
  validateCommandOptions(cmd,positionals[1],values);
  if(NEXUS_COMMANDS.includes(cmd)){if(positionals.length!==2)throw new Error('Unknown Nexus command');const result=await nexusCommand(cmd,positionals[1],values,context());output(result);if(result?.valid===false||result?.validation?.valid===false||result?.signatureValid===false||result?.passed===false||['error','failed','unavailable'].includes(result?.status)||(values.execute&&result?.status&&!['ok','completed','saved'].includes(result.status)))process.exitCode=1;return;}
  if(positionals.length>(['run','plan'].includes(cmd)?2:1))throw new Error('Unexpected positional argument');
  if(cmd==='actions'){output({actions:ACTIONS});return;}
  const c=context();
  if(cmd==='doctor'){output(await doctor(c));return;}
  if(cmd==='plan'||cmd==='run') {
    if(positionals[1]==='codex-resume'){
      const result=await nexusCommand('chats',cmd==='plan'?'plan':'open',{...values,id:values.session},c);output(result);
      if(cmd==='run'&&!['ok','completed'].includes(result.status))process.exitCode=1;return;
    }
    const p=plan(positionals[1],values,c);
    if(cmd==='plan'){output(p);return;}
    if(!values.execute)throw new Error('Use --execute to run the displayed action, or use plan');
    if(values.json && p.interactive)throw new Error('Interactive actions require a terminal without --json; use plan --json to inspect them');
    const result=await runPlan(p,c);output({action:p.action,...result});
    if(!['ok','completed'].includes(result.status))process.exitCode=1;
    return;
  }
  if(cmd!=='menu')throw new Error('Unknown command');
  if(values.json||!process.stdin.isTTY||!process.stdout.isTTY)throw new Error('Menu requires a terminal without --json. Agents can use doctor, actions, plan and run --json');
  const startRecord=journal(c,{action:'menu',status:'opened'});
  if(!startRecord.saved)console.error(startRecord.warning);
  await menu(c);
}
async function menu(c) {
  const entries=[['Inspect this host',null],['PowerShell here','powershell'],['Administrator PowerShell (Windows)','powershell-admin'],[c.platform==='win32'?'Linux primary — cloud task picker':'Linux shell in this executor',c.platform==='win32'?'cloud':'linux'],[c.platform==='win32'?'Local Ubuntu as root (optional WSL)':'Administrator shell in this Linux executor','linux-admin'],['New Codex CLI — Astra Max, Fast, Full access','codex'],['GHC-Family chat panel menu','chats'],['Launch ChatGPT/Codex app (Windows)','app'],['Check app launcher without opening app','app-check'],['GHC-Family Laboratory','lab'],['GHC-Family Freed ID certificates','identity'],['GHC-Family Spaces / Filesystem Memory bank','memory'],['GHC-Family Sentinel-1 Agent builder','sentinel'],['GHC-Family persistent remote terminal','remote'],['Check Codex sign-in','auth-status'],['Sign in through official browser flow','auth-login'],['Sign in with official device code','auth-device'],['Google account in browser','google-account'],['ChatGPT account in browser','chatgpt-account']];
  while(true){
    const display=terminalOptions();
    const menuItems=entries.map(([label],i)=>({key:String(i+1),label:i===5?'New Codex CLI - needs your explicit new-helper approval':label}));
    menuItems.push({key:'C',label:'Cloud Linux tasks - official Codex Cloud picker'});
    if(c.platform==='win32')menuItems.push({key:'U',label:'Local Ubuntu - optional; normal startup unresolved'},{key:'A',label:'Direct Administrator App - action 8 is the updater route'},{key:'D',label:'CMD Hub with this Windows token'},{key:'E',label:'Administrator CMD Hub'});
    menuItems.push({key:'0',label:'Exit'});
    console.log(renderMenu({title:'GHC NEXUS HUB',subtitle:'Host: '+clean(c.platform)+' | Workspace: '+clean(c.cwd),items:menuItems,footer:['PowerShell / CMD / Node / Linux / App & CLI','Windows token and Cloud permissions belong to their own hosts.']},display));
    const rl=createInterface({input:process.stdin,output:process.stdout});let answer;
    try{answer=(await rl.question('\nChoose an action: ')).trim();}catch{rl.close();return;}
    if(answer==='0'||answer.toLowerCase()==='q'){rl.close();return;}
    if(display.columns<24){rl.close();console.log('Widen the terminal before selecting an action.');continue;}
    if(['a','d','e'].includes(answer.toLowerCase())&&c.platform==='win32'){try{const action={a:'app-admin',d:'cmd',e:'cmd-admin'}[answer.toLowerCase()];const p=plan(action,{},c);console.log(p.note);const yes=(await rl.question('Open this selected Windows route? [y/N] ')).trim().toLowerCase();rl.close();if(yes==='y')console.log(safeJson(await runPlan(p,c),2));}catch(e){rl.close();console.error('Hub: '+publicError(e).message);}continue;}
    if(answer.toLowerCase()==='c'||(answer.toLowerCase()==='u'&&c.platform==='win32')){try{const chosen=answer.toLowerCase()==='c'?'cloud':'linux';const p=plan(chosen,{},c);console.log(p.note);const yes=(await rl.question('Open this route? [y/N] ')).trim().toLowerCase();rl.close();if(yes==='y')console.log(safeJson(await runPlan(p,c),2));}catch(e){rl.close();console.error('Hub: '+publicError(e).message);}continue;}
    if(!/^\d+$/.test(answer)||Number(answer)<1||Number(answer)>entries.length){rl.close();console.log('Choose a listed number.');continue;}
    const action=entries[Number(answer)-1][1];
    try {
      if(!action){rl.close();console.log(safeJson(await doctor(c),2));continue;}
      if(action==='chats'){rl.close();await chatMenu(c);continue;}
      if(['lab','identity','memory','sentinel','remote'].includes(action)){rl.close();await workbenchMenu(action,c);continue;}
      const opts={};if(action==='codex-resume')opts.session=(await rl.question('Exact existing session UUID: ')).trim();
      const p=plan(action,opts,c);console.log('\n'+clean(p.command)+'\n'+p.args.map(a=>JSON.stringify(clean(a))).join(' '));if(p.note)console.log(p.note);
      const yes=(await rl.question('Run this action on this host? [y/N] ')).trim().toLowerCase();rl.close();if(yes!=='y')continue;
      console.log(safeJson(await runPlan(p,c),2));
    }catch(e){rl.close();console.error('Hub: '+publicError(e).message);}
  }
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  main().catch(e=>{const error=publicError(e);console.error(process.argv.includes('--json')?safeJson(error):'Hub: '+error.message);process.exitCode=1;});
}
