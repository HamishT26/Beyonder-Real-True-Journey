// Synthetic fixtures only. No hub, provider, auth or network imports.
export function fixtureBindings(overrides={}){
  const calls=[];
  const selectors={chats:['quay'],labs:['lab-01'],sentinels:['sentinel-1'],remotes:['cloud-worker']};
  const make=(name,result)=>(args,context)=>{calls.push({name,args,readOnly:context.readOnly,signal:context.signal});return typeof result==='function'?result(args,context):structuredClone(result);};
  const plan={available:true,route:'cloud',steps:['select','review','handoff']};
  const handlers={
    chatsList:make('chatsList',{items:[{alias:'quay',available:true,title:'PRIVATE_TITLE_FIXTURE',nativeId:'PRIVATE_NATIVE_ID_FIXTURE'}]}),
    chatsResolve:make('chatsResolve',{available:true,route:'cloud',nativeId:'PRIVATE_NATIVE_ID_FIXTURE'}),
    chatsPlan:make('chatsPlan',plan),
    labCatalogue:make('labCatalogue',{items:[{alias:'lab-01',available:true}]}),
    labPlan:make('labPlan',plan),
    identitySummary:make('identitySummary',{platform:'linux',capabilities:{chats:true,lab:true,sentinel:true,remote:true},human:{name:'PRIVATE_HUMAN_FIXTURE',email:'PRIVATE_EMAIL_FIXTURE'},token:'PRIVATE_TOKEN_FIXTURE'}),
    sentinelValidate:make('sentinelValidate',{valid:null,issues:['unverified_source']}),
    sentinelPlan:make('sentinelPlan',plan),
    remotePlan:make('remotePlan',plan),
    sendChat:()=>{throw new Error('Forbidden fixture capability invoked');},
    ...overrides
  };
  const names=new Map([
    ['nexus.chats.list','chatsList'],['nexus.chats.resolve','chatsResolve'],['nexus.chats.plan','chatsPlan'],
    ['nexus.lab.catalogue','labCatalogue'],['nexus.lab.plan','labPlan'],['nexus.identity.summary','identitySummary'],
    ['nexus.sentinel.validate','sentinelValidate'],['nexus.sentinel.plan','sentinelPlan'],['nexus.remote.plan','remotePlan']
  ]);
  const dispatch=(name,args,context)=>handlers[names.get(name)](args,context);
  return {dispatch,selectors,calls};
}
