import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
const connectTimeoutMs=Number(process.argv[3]??30000);if(!Number.isInteger(connectTimeoutMs)||connectTimeoutMs<10000||connectTimeoutMs>120000)throw Error('Invalid preflight timeout');
const evidence=process.argv[2];if(!evidence||!path.isAbsolute(evidence))throw Error('Evidence directory required');
const cfg=path.join(evidence,'gui-preflight.toml');
await fs.writeFile(cfg,'[server]\ntransport="stdio"\nallow_insecure_remote=false\n');
const python='D:/GHC-Archives/global-tools/windows-mcp/0.8.8-stage/Scripts/python.exe';
const traced=process.argv[4]==='trace';
const pythonPrefix=traced?['-u','-c','import faulthandler,runpy; faulthandler.dump_traceback_later(45, exit=True); runpy.run_module("windows_mcp",run_name="__main__")']:['-m','windows_mcp'];
const client=new Client({name:'ghc-gui-preflight',version:'2.8.0-candidate'},{versionNegotiation:{mode:'legacy'}});
const transport=new StdioClientTransport({command:python,args:[...pythonPrefix,'serve','--config',cfg,'--transport','stdio','--tools','ControlStatus'],cwd:evidence,stderr:'pipe',maxBufferSize:65536,env:{SystemRoot:process.env.SystemRoot||'C:/Windows',PATH:path.dirname(python),USERPROFILE:process.env.USERPROFILE||'C:/Users/hamis',TEMP:evidence,TMP:evidence,PYTHONIOENCODING:'utf-8',PYTHONUTF8:'1',ANONYMIZED_TELEMETRY:'false',POSTHOG_API_KEY:'',WINDOWS_MCP_WATCHDOG:'off',NO_COLOR:'1'}});
let stderr='';transport.stderr.on('data',b=>{if(stderr.length<16000)stderr+=b.toString('utf8');});
const report={at:new Date().toISOString(),scope:'metadata and ControlStatus only',guiInputActions:0,screenshots:0,listener:false,exposedToTunnel:false,toolNames:[],connected:false,closed:false,connectTimeoutMs,startFreeMemoryMiB:Math.floor(os.freemem()/1048576),minimumFreeMemoryMiB:512,spawnAttempted:false};
try{
 if(report.startFreeMemoryMiB<report.minimumFreeMemoryMiB){report.heldForCapacity=true;throw Error('GUI probe held: less than512MiB free under the local operator guard');}
 report.spawnAttempted=true;
 const start=performance.now();await client.connect(transport,{timeout:connectTimeoutMs});report.connected=true;report.connectMs=Math.round(performance.now()-start);
 const listed=await client.listTools({}, {timeout:10000});report.toolNames=listed.tools.map(t=>t.name);
 if(report.toolNames.length!==1||report.toolNames[0]!=='ControlStatus')throw Error('Read-only preflight allowlist mismatch');
 const r=await client.callTool({name:'ControlStatus',arguments:{}},{timeout:10000});report.controlStatusSuccess=r.isError!==true;report.control=r.structuredContent??r.content.filter(c=>c.type==='text').map(c=>c.text);
}catch(e){report.error=String(e.message).slice(0,500);}finally{try{await client.close();report.closed=true;}catch{report.closed=false;}report.stderr=stderr.replace(/(?:sk-[\w-]+|tskey-[\w-]+|Bearer\s+\S+)/g,'[REDACTED]');}
await fs.writeFile(path.join(evidence,'gui-preflight.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));process.exitCode=report.heldForCapacity?2:report.connected&&report.controlStatusSuccess&&report.closed?0:1;
