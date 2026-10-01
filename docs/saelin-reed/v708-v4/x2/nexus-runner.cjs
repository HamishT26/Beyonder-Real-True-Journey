'use strict';
const fs=require('node:fs'),path=require('node:path');
function admission(model,effort,role){if(role==='new-inductee')return {allowed:model==='gpt-6.1-sol'&&effort==='max',model,effort,scope:role};return {allowed:['gpt-5.6-sol','gpt-6-astra','gpt-6.1-sol'].includes(model)&&['low','medium','high','xhigh','max','ultra'].includes(effort),model,effort,scope:role};}
function route(phase){return {phase,execute:false,next:phase==='v708-v4'?'Hamish and future Dot review':null,reason:'Roster is a projection; current direct instruction and native controls govern activation.'};}
function catalogue(file,query){const c=JSON.parse(fs.readFileSync(file,'utf8'));const matches=c.entries.filter(e=>e.name.includes(query||''));return {total:c.entries.length,matched:matches.length,names:matches.slice(0,15).map(e=>e.name),inventory_not_validation:true};}
module.exports={admission,route,catalogue};
if(require.main===module){const [command,...args]=process.argv.slice(2);let result;if(command==='admission')result=admission(...args);else if(command==='route')result=route(args[0]);else if(command==='catalogue')result=catalogue(path.join(__dirname,'catalogue.json'),args[0]);else throw Error('Use admission, route or catalogue');console.log(JSON.stringify(result));if(result.allowed===false)process.exitCode=2;}
