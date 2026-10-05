import {clean} from './core.mjs';
import {containsCredential} from './content-checks.mjs';
import {nexusHome,slug,writePrivate,readPrivate,listPrivate} from './private-store.mjs';

export function sentinelTemplate(id='sentinel-1'){
  if(!slug(id))throw new Error('Invalid agent ID');
  return {schema:'ghc.sentinel.spec.v1',id,title:'GHC Sentinel-1',stage:'design',implementation:'agent-orchestration',model:{provider:'openai',id:null,weightsAvailable:false},modalities:['text'],tools:['nexus.chats.list','nexus.lab.catalogue','nexus.identity.summary','nexus.sentinel.validate'],memory:{classification:'private',credentialStorage:'provider-native',automaticExport:false},authority:{local:'operating-system-user',cloud:'provider-role',escalation:'explicit supported flow'},budget:{maxUsd:50,maxTurns:20,maxOutputTokens:4096},evaluation:{required:['route-integrity','privacy-canaries','tool-boundary','source-citation','recovery','budget-stop'],minimumPassRate:1},research:{gmut:'hypothesis programme',millennium:'six open problems; Poincare solved',worldModel:'future research architecture, not an implemented model'},deployment:{enabled:false,requiresReview:true}};
}
export function validateSentinel(value){
  const errors=[];if(value?.schema!=='ghc.sentinel.spec.v1'||!slug(value?.id))errors.push('invalid_schema_or_id');
  if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).some(k=>!['schema','id','title','stage','implementation','model','modalities','tools','memory','authority','budget','evaluation','research','deployment'].includes(k)))errors.push('unknown_fields');
  if(value?.stage!=='design')errors.push('unsupported_stage');
  if(typeof value?.title!=='string'||value.title.length>160)errors.push('invalid_title');
  if(containsCredential(value))errors.push('credential_material');
  const shapes={model:['provider','id','weightsAvailable'],memory:['classification','credentialStorage','automaticExport'],authority:['local','cloud','escalation'],budget:['maxUsd','maxTurns','maxOutputTokens'],evaluation:['required','minimumPassRate'],research:['gmut','millennium','worldModel'],deployment:['enabled','requiresReview']};
  for(const [field,keys] of Object.entries(shapes)){const part=value?.[field];if(!part||typeof part!=='object'||Array.isArray(part)||Object.keys(part).some(k=>!keys.includes(k)))errors.push('unsupported_'+field+'_fields');}
  if(value?.implementation!=='agent-orchestration')errors.push('unimplemented_model_architecture');
  if(!Array.isArray(value?.modalities)||value.modalities.some(x=>!['text','image','audio','video'].includes(x)))errors.push('invalid_modalities');
  if(!Number.isFinite(value?.budget?.maxUsd)||value.budget.maxUsd<0||value.budget.maxUsd>50)errors.push('budget_out_of_range');
  if(!Number.isInteger(value?.budget?.maxTurns)||value.budget.maxTurns<1||value.budget.maxTurns>100)errors.push('turn_limit_out_of_range');
  if(!Number.isInteger(value?.budget?.maxOutputTokens)||value.budget.maxOutputTokens<1||value.budget.maxOutputTokens>32768)errors.push('output_limit_out_of_range');
  if(value?.memory?.automaticExport!==false)errors.push('automatic_memory_export_not_supported');
  if(!Array.isArray(value?.tools)||value.tools.some(x=>!['nexus.chats.list','nexus.lab.catalogue','nexus.identity.summary','nexus.sentinel.validate','nexus.remote.plan'].includes(x)))errors.push('unknown_tool');
  if(value?.deployment?.enabled!==false)errors.push('live_deployment_not_implemented');
  return {schema:'ghc.sentinel.validation.v1',valid:errors.length===0,errors,modelTrained:false,modelEntitlementVerified:false,superintelligenceEstablished:false,networkCalls:0};
}
export function saveSentinel(c,raw){const result=validateSentinel(raw);if(!result.valid)throw new Error('Invalid Sentinel specification');return writePrivate(nexusHome(c),'sentinel/'+raw.id+'.json',raw);}
export function listSentinel(c){const root=nexusHome(c);return listPrivate(root,'sentinel').map(n=>{const r=readPrivate(root,'sentinel/'+n);return {id:r.id,title:clean(r.title),validation:validateSentinel(r)};});}
export function readSentinel(c,id){if(!slug(id))throw new Error('Invalid agent ID');const r=readPrivate(nexusHome(c),'sentinel/'+id+'.json');if(!r)throw new Error('Agent specification not found');if(!validateSentinel(r).valid)throw new Error('Invalid Sentinel specification');return r;}
export function sentinelPlan(spec){const validation=validateSentinel(spec);return {schema:'ghc.sentinel.plan.v1',id:spec?.id,validation,steps:['Choose an available supported provider model','Run the six required offline evaluations','Configure a provider-supported private credential store','Review model/tool price and an enforceable spending limit','Review the exact live deployment separately'],liveActions:0,reason:'The builder creates and validates agent specifications; it does not train new model weights or deploy an autonomous agent'};}
