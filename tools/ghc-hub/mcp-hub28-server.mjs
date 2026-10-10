import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {context} from './core.mjs';
import {createNexusBindings} from './mcp-server.mjs';
import {loadAdminPolicy,createAdminCommander} from './admin-commander.mjs';
import {createFabricDispatcher,FABRIC_TOOLS} from './host-fabric.mjs';
import {createMessageRelay,MESSAGE_TOOLS} from './message-relay.mjs';
import {serveAdminStdio} from './mcp/sdk/src/admin-bridge.mjs';

export async function main(configFile=process.argv[2]){
 if(!configFile||!path.isAbsolute(configFile))throw Error('Explicit private config required');
 const stat=await fs.lstat(configFile);if(!stat.isFile()||stat.isSymbolicLink()||stat.nlink!==1||stat.size>16384)throw Error('Config refused');
 const config=JSON.parse(await fs.readFile(configFile,'utf8'));
 if(config.schema!=='ghc.hub28.config.v1'||config.enabled!==true||!path.isAbsolute(config.adminPolicy)||!path.isAbsolute(config.tailscaleKeyFile))throw Error('Config refused');
 const policy=await loadAdminPolicy(config.adminPolicy);
 const c=context();
 const dispatch=createFabricDispatcher({tailscaleKeyFile:config.tailscaleKeyFile});
 const relay=createMessageRelay(c);
 const extensions=[...FABRIC_TOOLS.map(spec=>({spec,dispatch})),...MESSAGE_TOOLS.map(spec=>({spec,dispatch:relay}))];
 const server=serveAdminStdio({readOnly:createNexusBindings(c),commander:createAdminCommander(policy),extensions,serverInfo:{name:'ghc-nexus-admin-desktop-commander',version:'2.8.0'}});
 await server.done;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(()=>{console.error('Nexus 2.8 candidate unavailable; review its explicit private config.');process.exitCode=1;});
