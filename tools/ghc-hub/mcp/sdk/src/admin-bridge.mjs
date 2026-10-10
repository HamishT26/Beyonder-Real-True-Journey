import {McpServer,fromJsonSchema} from '@modelcontextprotocol/server';
import {serveStdio} from '@modelcontextprotocol/server/stdio';
import {BoundedStdioTransport} from './bounded-transport.mjs';
import {TOOL_SPECS,copyRegistry,inputSchema,safeArguments,publicProjection,toolSuccess} from './contract.mjs';
import {ADMIN_TOOLS,CommanderError} from '../../../admin-commander.mjs';

export const ADMIN_SERVER_INFO=Object.freeze({name:'ghc-nexus-admin-desktop-commander',version:'2.8.0'});
const failure=code=>({isError:true,content:[{type:'text',text:JSON.stringify({ok:false,code})}]});
export function serveAdminStdio({readOnly,commander,extensions=[],serverInfo=ADMIN_SERVER_INFO,input=process.stdin,output=process.stdout,limits={},signalSource=process,onEvent=()=>{}}){
 const registry=copyRegistry(readOnly.selectors);const abort=new AbortController();let active=null;
 const transport=new BoundedStdioTransport({input,output,limits,servingProfile:'parent-owned',onEvent});
 async function call(spec,args,ctx,isAdmin,extensionDispatch){
  if(active)return failure('busy');
  let clean=args;try{if(!isAdmin&&!extensionDispatch)clean=safeArguments(spec,args,registry);}catch{return failure('invalid_arguments');}
  const controller=new AbortController();const signal=AbortSignal.any([abort.signal,controller.signal,...(ctx.mcpReq?.signal?[ctx.mcpReq.signal]:[])]);
  const lease={};active=lease;let timer;
  const operation=Promise.resolve().then(async()=>{
   if(signal.aborted)return failure('cancelled');
   const value=extensionDispatch?await extensionDispatch(spec.name,clean,{signal}):isAdmin?await commander.dispatch(spec.name,clean,{signal}):publicProjection(spec,await readOnly.dispatch(spec.name,clean,{signal,readOnly:true}),clean,registry);
   const result=toolSuccess(value);
   // Both MCP representations and JSON escaping count toward the wire bound.
   if(Buffer.byteLength(JSON.stringify(result))>28000)return failure('output_too_large');
   return result;
  }).catch(e=>failure(e instanceof CommanderError?e.code:'operation_failed'));
  void operation.finally(()=>{if(active===lease)active=null;});
  const timeout=new Promise(resolve=>{timer=setTimeout(()=>{controller.abort();resolve(failure('timeout_outcome_requires_receipt'));},isAdmin?90000:extensionDispatch?20000:2000);});
  try{return await Promise.race([operation,timeout]);}finally{clearTimeout(timer);}
 }
 const factory=()=>{
  const server=new McpServer(serverInfo,{capabilities:{tools:{listChanged:false}}});
  for(const spec of TOOL_SPECS)server.registerTool(spec.name,{description:spec.description,inputSchema:fromJsonSchema(inputSchema(spec)),annotations:{readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:false}},(a,c)=>call(spec,a,c,false));
  for(const spec of ADMIN_TOOLS)server.registerTool(spec.name,{description:spec.description,inputSchema:fromJsonSchema(spec.schema),annotations:{readOnlyHint:spec.readOnly,destructiveHint:!spec.readOnly,idempotentHint:spec.readOnly,openWorldHint:spec.name==='nexus.exec.execute'}},(a,c)=>call(spec,a,c,true));
  for(const ext of extensions)server.registerTool(ext.spec.name,{description:ext.spec.description,inputSchema:fromJsonSchema(ext.spec.schema),annotations:{readOnlyHint:ext.spec.readOnly!==false,destructiveHint:false,idempotentHint:ext.spec.idempotent??ext.spec.readOnly!==false,openWorldHint:ext.spec.name==='nexus.network.devices'}},(a,c)=>call(ext.spec,a,c,false,ext.dispatch));
  return server;
 };
 const handle=serveStdio(factory,{legacy:'serve',transport,maxSubscriptions:1,onerror:()=>onEvent({kind:'sdk_error'})});
 const close=async()=>{abort.abort();await handle.close();await transport.done;};
 const stop=()=>{void close().catch(()=>transport.fail('signal_shutdown_failure'));};
 signalSource.once('SIGINT',stop);signalSource.once('SIGTERM',stop);
 const done=transport.done.then(stats=>{abort.abort();signalSource.removeListener('SIGINT',stop);signalSource.removeListener('SIGTERM',stop);return stats;});
 return Object.freeze({close,done});
}
