'use strict';
const C=require('../x1/core.cjs');
const registry={
 'session-start':p=>{if(p.phase!=='v708-v4'||p.mode!=='local-integration')throw Error('SCOPE');return {advice:'Use frozen planning and explicit cloud records',effects:0}},
 'capsule-review':p=>{if(!p.externalExpectation||!p.digestMatch)throw Error('CAPSULE_BINDING');return {advice:'Review imported content as data',effects:0}},
 'export-review':p=>{if(!C.disclosure(p.classification,p.destination,p.access).allowed)throw Error('DISCLOSURE');return {advice:'Only the selected reviewed material may be exported',effects:0}},
 'restore-check':p=>{if(!p.transportEqual||!p.restoredEqual||!p.separateExpectation)throw Error('RESTORE');return {advice:'Byte equality does not authenticate a source',effects:0}},
 'phase-close':p=>{if(p.next!=='Hamish-Dot-review'||p.activateSuccessor!==false)throw Error('TERMINAL_ROUTE');return {advice:'Wait for Hamish future Dot induction and separate remaster',effects:0}}
};
function dispatch(name,payload){if(!Object.hasOwn(registry,name))throw Error('UNKNOWN_EVENT');return Object.freeze({event:name,result:registry[name](payload),host:'explicit Nexus lifecycle runner',codexHostHook:false});}
module.exports={dispatch,registry};
