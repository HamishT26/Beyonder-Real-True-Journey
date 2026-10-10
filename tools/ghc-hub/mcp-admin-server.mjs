import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {context} from './core.mjs';
import {createNexusBindings} from './mcp-server.mjs';
import {loadAdminPolicy,createAdminCommander} from './admin-commander.mjs';
import {serveAdminStdio} from './mcp/sdk/src/admin-bridge.mjs';

export async function main(policyFile=process.argv[2]){
 if(!policyFile)throw new Error('An explicit private policy is required');
 const policy=await loadAdminPolicy(policyFile);
 const server=serveAdminStdio({readOnly:createNexusBindings(context()),commander:createAdminCommander(policy)});
 await server.done;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(()=>{console.error('GHC Admin MCP unavailable; verify its explicit private policy and installation.');process.exitCode=1;});
