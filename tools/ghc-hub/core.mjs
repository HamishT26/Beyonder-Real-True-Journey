import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import { spawn } from 'node:child_process';

export const VERSION = '1.0.0';
export const MIN_NODE = 20;
export const clean = value => String(value).replace(/[\x00-\x1f\x7f-\x9f\u202a-\u202e\u2066-\u2069]/g, ' ').slice(0, 2048);
export const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
export const uuid = value => /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value || '');
const winRoot = 'D:/GHC-Archives/global-tools';
export function findExecutable(name, platform = process.platform, env = process.env) {
  const ext = platform === 'win32' ? '.exe' : '';
  for (const dir of (env.PATH || '').split(platform === 'win32' ? ';' : ':')) {
    if (!dir || !path.isAbsolute(dir)) continue;
    const file = path.join(dir, name + ext);
    try { if (fs.statSync(file).isFile()) { fs.accessSync(file, platform === 'win32' ? fs.constants.F_OK : fs.constants.X_OK); return file; } } catch {}
  }
  return null;
}
export function context(env = process.env) {
  const windows = process.platform === 'win32';
  const defaultCodex = windows ? winRoot + '/npm/node_modules/@openai/codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe' : findExecutable('codex');
  const choose = (override, fallback) => {
    const p = override || fallback;
    if (!p) return null;
    if (!path.isAbsolute(p) || /[\x00-\x1f]/.test(p)) throw new Error('Executable override must be an absolute local path');
    if (windows && !p.toLowerCase().endsWith('.exe')) throw new Error('Windows executable overrides must name an .exe, not a shell shim');
    return fs.existsSync(p) ? path.resolve(p) : null;
  };
  const cwd = path.resolve(env.GHC_HUB_WORKSPACE || (windows ? 'D:/GHC-Family-Laboratory' : process.cwd()));
  if (!fs.statSync(cwd).isDirectory()) throw new Error('Workspace must be an existing directory');
  return {
    platform: process.platform, cwd,
    state: path.resolve(env.GHC_HUB_HOME || (windows ? 'D:/GHC-Archives/phase-banks/ghc-hub' : path.join(os.homedir(), '.local/state/ghc-hub'))),
    codex: choose(env.GHC_HUB_CODEX, defaultCodex),
    pwsh: choose(env.GHC_HUB_PWSH, windows ? winRoot + '/powershell/7.6.6/pwsh.exe' : findExecutable('pwsh')),
    bash: windows ? null : findExecutable('bash'),
    sudo: windows ? null : findExecutable('sudo'),
    wsl: windows ? findExecutable('wsl') : null,
    adminLauncher: windows ? winRoot + '/ghc-config-launchers/Start-GhcAdmin.ps1' : null,
    node: process.execPath,
    uid: typeof process.getuid === 'function' ? process.getuid() : null,
  };
}
export function bounded(command, args, { cwd, timeoutMs = 15000, maxBytes = 65536, spawnFn = spawn } = {}) {
  if (!Number.isInteger(timeoutMs) || timeoutMs < 100 || timeoutMs > 60000) throw new Error('Timeout must be 100–60000 milliseconds');
  return new Promise(resolve => {
    const started = performance.now(); let output = [], bytes = 0, reason = null, settled = false;
    let child, hardStop, reapDeadline;
    const finish = result => { if (settled) return; settled = true; clearTimeout(timer); clearTimeout(hardStop); clearTimeout(reapDeadline); resolve({ ...result, elapsedMs: performance.now() - started, output: Buffer.concat(output).toString('utf8') }); };
    let timer;
    const stopOwnedChild = () => {
      if (settled || hardStop) return;
      child.kill();
      hardStop = setTimeout(() => { if (!settled && child.exitCode === null && !child.signalCode) child.kill('SIGKILL'); }, 250);
      reapDeadline = setTimeout(() => {
        if (settled) return;
        child.stdout.destroy(); child.stderr.destroy(); child.unref();
        finish({status:reason||'timeout',exitCode:child.exitCode,childCloseObserved:false,cleanup:'unconfirmed; no descendant containment claimed'});
      }, 1500);
    };
    try { child = spawnFn(command, args, { cwd, shell: false, windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] }); }
    catch { finish({ status: 'spawn_error', exitCode: null }); return; }
    const collect = chunk => {
      bytes += chunk.length;
      if (bytes > maxBytes) { reason = 'output_limit'; stopOwnedChild(); return; }
      output.push(chunk);
    };
    child.stdout.on('data', collect);
    child.stderr.on('data', collect);
    child.once('error', () => finish({ status: 'spawn_error', exitCode: null }));
    child.once('close', (code, signal) => finish({ status: reason || (code === 0 ? 'ok' : 'failed'), exitCode: code, signal: signal || null, childCloseObserved:true }));
    timer = setTimeout(() => { reason ||= 'timeout'; stopOwnedChild(); }, timeoutMs);
  });
}
const disabledMcp = ['circleci','e2b','oci','notion','neon','openai','github','docker','render','expo','kimicode','node_repl'];
export function codexOptions(c) {
  const args = ['--no-daemon', '--no-alt-screen', '--ask-for-approval', 'never', '--sandbox', 'danger-full-access', '--model', 'gpt-6-astra', '-c', 'model_reasoning_effort="max"', '-c', 'service_tier="fast"', '-c', 'model_context_window=872000', '-c', 'model_auto_compact_token_limit=600000', '-c', 'features.apps=false', '-c', 'features.multi_agent=false', '--cd', c.cwd];
  for (const name of disabledMcp) args.push('-c', `mcp_servers.${name}.enabled=false`);
  return args;
}
export const ACTIONS = ['powershell','powershell-admin','linux','linux-admin','codex','codex-resume','app','app-check','cloud-list','auth-status','auth-login','auth-device','google-account','chatgpt-account'];
export function plan(action, opts, c) {
  if (!ACTIONS.includes(action)) throw new Error('Unknown action');
  let command, args = [], interactive = false, note = '';
  switch (action) {
    case 'powershell': command = c.pwsh; args = ['-NoLogo','-NoProfile']; interactive = true; break;
    case 'powershell-admin': case 'app': case 'app-check':
      if (c.platform !== 'win32') throw new Error('This action requires the Windows host');
      if (!fs.existsSync(c.adminLauncher)) throw new Error('Reviewed Windows launcher is unavailable');
      command = c.pwsh; args = ['-NoLogo','-NoProfile','-File',c.adminLauncher,'-Target', action === 'powershell-admin' ? 'PowerShell' : 'Codex'];
      if (action === 'app-check') args.push('-Check');
      note = 'Uses the existing signed-app/UAC launcher. Existing app instances are not replaced.'; break;
    case 'linux': case 'linux-admin':
      interactive = true;
      if (c.platform === 'win32') { command = c.wsl; args = ['--distribution','Ubuntu','--cd','/mnt/d/GHC-Family-Laboratory']; if (action === 'linux-admin') args.push('--user','root'); note = 'Explicit local WSL start; normal Ubuntu startup is historically unresolved. This uses laptop RAM.'; }
      else if (action === 'linux-admin' && c.uid !== 0) { command = c.sudo; args = ['-i']; note = 'Normal sudo policy applies; no cloud role or sandbox is changed.'; }
      else { command = c.bash; args = ['--noprofile','--norc']; }
      break;
    case 'codex': case 'codex-resume':
      command = c.codex; args = codexOptions(c); interactive = true;
      if (action === 'codex-resume') { if (!uuid(opts.session)) throw new Error('An exact existing session UUID is required'); args.push('resume',opts.session); }
      note = 'Requests Astra/Max/Fast and Full access for this invocation; OS privilege and provider limits are separate. Unrelated MCP services disabled only here.'; break;
    case 'cloud-list': command = c.codex; args = ['cloud','list','--json','--limit','5']; if (opts.env) { if (!/^[A-Za-z0-9_-]{1,160}$/.test(opts.env)) throw new Error('Invalid environment ID'); args.push('--env',opts.env); } note = 'Experimental Codex Cloud CLI route; it may differ from existing managed app workers.'; break;
    case 'auth-status': command = c.codex; args = ['login','status']; break;
    case 'auth-login': case 'auth-device': command = c.codex; args = ['login', ...(action === 'auth-device' ? ['--device-auth'] : [])]; interactive = true; note = 'Official sign-in; credentials and one-time codes are never captured by the hub.'; break;
    case 'google-account': case 'chatgpt-account': {
      const url = action === 'google-account' ? 'https://myaccount.google.com/' : 'https://chatgpt.com/';
      if (c.platform === 'win32') { command = c.pwsh; args = ['-NoProfile','-NonInteractive','-Command',`Start-Process -FilePath '${url}'`]; }
      else { command = findExecutable('xdg-open'); args = [url]; }
      note = `Open official account page: ${url}. This does not grant new scopes.`; break;
    }
  }
  if (!command) throw new Error('Required executable is unavailable on this host');
  return { schema: 'ghc.hub.plan.v1', action, command, args, cwd: c.cwd, platform: c.platform, interactive, shell: false, note };
}
export function journal(c, record) {
  try {
    fs.mkdirSync(path.join(c.state,'events'), {recursive:true,mode:0o700});
    const id = crypto.randomUUID();
    const safe = {schema:'ghc.hub.event.v1',id,utc:new Date().toISOString(),version:VERSION,action:record.action,status:record.status,exitCode:record.exitCode ?? null,elapsedMs:record.elapsedMs ?? null};
    fs.writeFileSync(path.join(c.state,'events',id+'.json'),JSON.stringify(safe)+'\n',{flag:'wx',mode:0o600});
    return {saved:true,id};
  } catch { return {saved:false,warning:'Timing record unavailable; execution outcome is separate'}; }
}
export async function doctor(c) {
  const versions = {};
  for (const [name, executable] of Object.entries({codex:c.codex,powershell:c.pwsh})) {
    if (!executable) { versions[name] = {available:false}; continue; }
    const r = await bounded(executable,['--version'],{cwd:c.cwd});
    versions[name] = {available:true,path:executable,status:r.status,version:r.status==='ok' ? r.output.match(/\d+\.\d+\.\d+(?:[-+][\w.-]+)?/)?.[0] || null : null,elapsedMs:r.elapsedMs};
  }
  let administrator = c.platform !== 'win32' ? c.uid === 0 : null;
  if (c.platform === 'win32' && c.pwsh) {
    const r=await bounded(c.pwsh,['-NoProfile','-NonInteractive','-Command','([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)'],{cwd:c.cwd});
    if(r.status==='ok' && /^(True|False)\s*$/.test(r.output)) administrator=r.output.trim()==='True';
  }
  const result={schema:'ghc.hub.doctor.v1',version:VERSION,utc:new Date().toISOString(),platform:c.platform,node:process.version,workspace:c.cwd,versions,administrator,uid:c.uid,localMemoryBytes:os.totalmem(),freeMemoryBytes:os.freemem(),linuxRoute:c.platform==='win32'?'WSL explicit-only; not started':'current Linux executor',cloudRoute:'official CLI adapter; connectivity separately checked',credentialContentsRead:false,backgroundServicesStarted:false};
  result.journal=journal(c,{action:'doctor',status:'observed'});return result;
}
export async function runPlan(p,c,{interactive=Boolean(process.stdin.isTTY&&process.stdout.isTTY),spawnFn=spawn}={}) {
  if(p.interactive && !interactive) throw new Error('This action requires an interactive terminal; use plan or machine commands in an agent tool');
  const started=performance.now();
  if(p.interactive) {
    const result=await new Promise(resolve=>{
      let child;try{child=spawnFn(p.command,p.args,{cwd:p.cwd,shell:false,stdio:'inherit'});}catch{resolve({status:'spawn_error',exitCode:null});return;}
      child.once('error',()=>resolve({status:'spawn_error',exitCode:null}));
      child.once('close',(code,signal)=>resolve({status:code===0?'completed':'failed',exitCode:code,signal:signal||null}));
    });
    result.elapsedMs=performance.now()-started;result.journal=journal(c,{action:p.action,...result});return result;
  }
  const r=await bounded(p.command,p.args,{cwd:p.cwd,timeoutMs:p.action==='app-check'?60000:30000,spawnFn});
  const result={status:r.status,exitCode:r.exitCode,elapsedMs:r.elapsedMs};
  if(p.action==='auth-status') {result.signedIn=r.status==='ok'?true:null;result.method=r.status==='ok' ? (/ChatGPT/i.test(r.output)?'ChatGPT':/API key/i.test(r.output)?'API key':'provider-reported') : 'unknown';}
  if(p.action==='cloud-list'&&r.status==='ok') {
    try {const data=JSON.parse(r.output);if(!Array.isArray(data.tasks))throw new Error();result.tasks=data.tasks.slice(0,5).map(t=>({id:clean(t.id),title:clean(t.title),status:typeof t.status==='string'?clean(t.status):'structured',environment_id:typeof t.environment_id==='string'?clean(t.environment_id):null}));}
    catch {result.status='invalid_provider_json';}
  }
  if(p.action==='app-check'&&r.status==='ok') {try{result.observation=JSON.parse(r.output);}catch{result.status='invalid_provider_json';}}
  result.journal=journal(c,{action:p.action,...result});return result;
}
