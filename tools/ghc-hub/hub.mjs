#!/usr/bin/env node
import {parseArgs} from 'node:util';
import {createInterface} from 'node:readline/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {ACTIONS,VERSION,MIN_NODE,clean,context,plan,runPlan,doctor,journal,safeJson} from './core.mjs';

export function publicError(error){
 const fixed=['Unknown action','Unknown command','Unexpected positional argument','Use --execute to run the displayed action, or use plan','An exact existing session UUID is required','Invalid environment ID','This action requires the Windows host','Reviewed Windows launcher is unavailable','Required executable is unavailable on this host','This action requires an interactive terminal; use plan or machine commands in an agent tool','Interactive actions require a terminal without --json; use plan --json to inspect them','Menu requires a terminal without --json. Agents can use doctor, actions, plan and run --json','Node 20 or later is required'];
 if(fixed.includes(error?.message))return {status:'error',code:'invalid_action',message:error.message};
 if(error?.code?.startsWith('ERR_PARSE_ARGS'))return {status:'error',code:'invalid_arguments',message:'Unknown or invalid arguments; use --help for the supported interface'};
 return {status:'error',code:'operation_unavailable',message:'Operation unavailable; check the selected host and required tools. No raw exception or credential data is displayed.'};
}

export async function main(argv=process.argv.slice(2)) {
  if(Number(process.versions.node.split('.')[0])<MIN_NODE)throw new Error('Node 20 or later is required');
  const {values,positionals}=parseArgs({args:argv,allowPositionals:true,strict:true,options:{json:{type:'boolean'},execute:{type:'boolean'},session:{type:'string'},env:{type:'string'},help:{type:'boolean'},version:{type:'boolean'}}});
  const output=value=>console.log(safeJson(value,values.json?undefined:2));
  if(values.version){output({name:'GHC Nexus Hub',version:VERSION});return;}
  if(values.help||positionals[0]==='help') { const help='GHC Nexus Hub\n\nnode hub.mjs [menu]\nnode hub.mjs doctor --json\nnode hub.mjs actions --json\nnode hub.mjs plan ACTION [--session UUID] [--env ID] --json\nnode hub.mjs run ACTION --execute [--session UUID] [--env ID] --json\n\nActions: '+ACTIONS.join(', ')+'\n\nPlans do not execute. Interactive shell/sign-in/Codex actions need a real terminal.\nThe hub never copies tokens, starts a daemon or upgrades a managed app-server.'; if(values.json)output({help,actions:ACTIONS});else console.log(help);return; }
  const cmd=positionals[0]||'menu';
  if(positionals.length>(['run','plan'].includes(cmd)?2:1))throw new Error('Unexpected positional argument');
  if(cmd==='actions'){output({actions:ACTIONS});return;}
  const c=context();
  if(cmd==='doctor'){output(await doctor(c));return;}
  if(cmd==='plan'||cmd==='run') {
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
  const entries=[['Inspect this host',null],['PowerShell here','powershell'],['Administrator PowerShell (Windows)','powershell-admin'],[c.platform==='win32'?'Linux primary — cloud task picker':'Linux shell in this executor',c.platform==='win32'?'cloud':'linux'],['Administrator Linux shell','linux-admin'],['Codex CLI — Astra Max, Fast, Full access','codex'],['Resume an existing CLI session','codex-resume'],['Launch ChatGPT/Codex app (Windows)','app'],['Check app launcher without opening app','app-check'],['List cloud tasks','cloud-list'],['Check Codex sign-in','auth-status'],['Sign in through official browser flow','auth-login'],['Sign in with official device code','auth-device'],['Google account in browser','google-account'],['ChatGPT account in browser','chatgpt-account']];
  while(true){
    console.log('\n╭────────────────────────────────────────────────────╮\n│  GHC NEXUS HUB  ·  Local authority / Cloud compute  │\n╰────────────────────────────────────────────────────╯');
    console.log('Host: '+clean(c.platform)+'    Workspace: '+clean(c.cwd));
    console.log('PowerShell • Linux • Codex App & CLI\nObserved access belongs to this host. Cloud is a separate executor.\n');
    entries.forEach(([label],i)=>console.log(String(i+1).padStart(2)+'. '+label));console.log(' C. Cloud Linux tasks — official Codex Cloud picker');if(c.platform==='win32')console.log(' U. Local Ubuntu — optional; normal startup unresolved');console.log(' 0. Exit');
    const rl=createInterface({input:process.stdin,output:process.stdout});let answer;
    try{answer=(await rl.question('\nChoose an action: ')).trim();}catch{rl.close();return;}
    if(answer==='0'||answer.toLowerCase()==='q'){rl.close();return;}
    if(answer.toLowerCase()==='c'||(answer.toLowerCase()==='u'&&c.platform==='win32')){try{const chosen=answer.toLowerCase()==='c'?'cloud':'linux';const p=plan(chosen,{},c);console.log(p.note);const yes=(await rl.question('Open this route? [y/N] ')).trim().toLowerCase();rl.close();if(yes==='y')console.log(safeJson(await runPlan(p,c),2));}catch(e){rl.close();console.error('Hub: '+publicError(e).message);}continue;}
    if(!/^\d+$/.test(answer)||Number(answer)<1||Number(answer)>entries.length){rl.close();console.log('Choose a listed number.');continue;}
    const action=entries[Number(answer)-1][1];
    try {
      if(!action){rl.close();console.log(safeJson(await doctor(c),2));continue;}
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
