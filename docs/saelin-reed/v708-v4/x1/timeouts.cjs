'use strict';
const {doubleTimeout}=require('./core.cjs');
function patchTimeouts(text){
 const lines=text.split(/\r?\n/),out=[],changes=[];let table=null,block=[];
 function flush(){if(!block.length)return;const server=/^\[mcp_servers\.([^.[\]]+)\]$/.exec(table||'');if(server){const values={};for(let i=1;i<block.length;i++){const m=/^(\s*)(startup_timeout_sec|startup_timeout_ms|tool_timeout_sec)(\s*=\s*)(\d+(?:\.\d+)?)(.*)$/.exec(block[i]);if(m){if(values[m[2]]!==undefined)throw Error('DUPLICATE_TIMEOUT');values[m[2]]=Number(m[4]);const scale=m[2].endsWith('_ms')?1000:1,next=doubleTimeout(Number(m[4])/scale)*scale;if(next!==Number(m[4])){changes.push({server:server[1],key:m[2],before:Number(m[4]),after:next,source:'explicit'});block[i]=m[1]+m[2]+m[3]+next+m[5];}}}
 if(values.startup_timeout_sec!==undefined&&values.startup_timeout_ms!==undefined)throw Error('AMBIGUOUS_STARTUP_ALIAS');
 const added=[];if(values.startup_timeout_sec===undefined&&values.startup_timeout_ms===undefined){added.push('startup_timeout_sec = 20');changes.push({server:server[1],key:'startup_timeout_sec',before:10,after:20,source:'documented_default'});}if(values.tool_timeout_sec===undefined){added.push('tool_timeout_sec = 120');changes.push({server:server[1],key:'tool_timeout_sec',before:60,after:120,source:'documented_default'});}block.splice(1,0,...added);}
 out.push(...block);block=[];}
 for(let line of lines){if(/^\s*\[/.test(line)){flush();table=line.trim();}const m=/^(\s*NODE_REPL_NATIVE_PIPE_CONNECT_TIMEOUT_MS\s*=\s*")(\d+)(".*)$/.exec(line);if(m){const before=Number(m[2]),after=doubleTimeout(before/1000)*1000;if(before!==after){changes.push({server:'node_repl.env',key:'NODE_REPL_NATIVE_PIPE_CONNECT_TIMEOUT_MS',before,after,source:'explicit_env'});line=m[1]+after+m[3];}}block.push(line);}flush();return {text:out.join('\n'),changes};
}
module.exports={patchTimeouts};
