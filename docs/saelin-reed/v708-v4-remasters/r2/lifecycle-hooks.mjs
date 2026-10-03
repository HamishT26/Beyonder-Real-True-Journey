export function createLifecycleHooks(){
 const events={admission:0,beforeStep:0,modelComplete:0,evidenceReady:0,publicationReview:0};
 const states=new Map();let reviewReady=false;
 const requireState=(model,phase)=>{const s=states.get(model);if(!s||s.phase!==phase)throw Error('Lifecycle order violation');return s;};
 const hooks={
  admission({model,steps,duration}){
   if(!/^S\d{2}$/.test(model)||states.has(model)||!Number.isInteger(steps)||steps<1||steps>200000||!(duration>0))throw Error('Invalid or duplicate model admission');
   states.set(model,{phase:'admitted',steps,next:0});events.admission++;
  },
  beforeStep({model,step}){
   const s=requireState(model,'admitted');if(step!==s.next||step>=s.steps)throw Error('Step order violation');
   s.next++;events.beforeStep++;
  },
  modelComplete({model,checks}){
   const s=requireState(model,'admitted');
   if(s.next!==s.steps||!Array.isArray(checks)||checks.length===0||checks.some(c=>typeof c.pass!=='boolean'))throw Error('Incomplete model evidence');
   s.phase='complete';s.passed=checks.every(c=>c.pass);events.modelComplete++;
  },
  evidenceReady({model,passed}){
   const s=requireState(model,'complete');if(passed!==s.passed)throw Error('Result and check disposition disagree');
   s.phase='evidence';events.evidenceReady++;
  },
  publicationReview({allPassed}){
   if(states.size===0||[...states.values()].some(s=>s.phase!=='evidence'))throw Error('Missing evidence at review');
   const observed=[...states.values()].every(s=>s.passed);if(allPassed!==observed)throw Error('Aggregate disposition mismatch');
   reviewReady=observed;events.publicationReview++;
  }
 };
 return {hooks,events,summary:()=>({models:states.size,ready_for_human_review:reviewReady,external_publication_performed:false})};
}
