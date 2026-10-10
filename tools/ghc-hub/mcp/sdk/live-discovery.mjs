import fs from 'node:fs/promises';
import path from 'node:path';
import {Client} from '@modelcontextprotocol/client';
import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';
const evidence=process.argv[2];if(!evidence||!path.isAbsolute(evidence))throw Error('Evidence directory required');
const client=new Client({name:'ghc-installed-discovery',version:'2.7.0'},{versionNegotiation:{mode:{pin:'2026-07-28'}}});
const transport=new StdioClientTransport({command:process.execPath,args:['--max-old-space-size=128','D:/GHC-Archives/global-tools/ghc-nexus-hub/mcp-admin-server.mjs','D:/GHC-Archives/private/ghc-nexus/admin/policy.json'],cwd:evidence,stderr:'pipe',maxBufferSize:32768});
let stderrBytes=0;transport.stderr.on('data',b=>stderrBytes+=b.length);
const report={at:new Date().toISOString(),realInstalledRuntime:true,mutations:0,modelCalls:0,connected:false};
try{const start=performance.now();await client.connect(transport,{timeout:30000});report.connected=true;report.discoveryMs=Math.round(performance.now()-start);const r=await client.listTools({}, {timeout:10000});report.toolNames=r.tools.map(t=>t.name);report.toolCount=r.tools.length;const s=await client.callTool({name:'nexus.admin.status',arguments:{}},{timeout:15000});report.adminStatus=s.structuredContent;report.statusSuccess=s.isError!==true;}catch(e){report.error=String(e.message).slice(0,300);}finally{await client.close();report.transportClosed=true;report.stderrBytes=stderrBytes;}
await fs.writeFile(path.join(evidence,'installed-discovery.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));process.exitCode=report.connected&&report.toolCount===16&&report.statusSuccess?0:1;
