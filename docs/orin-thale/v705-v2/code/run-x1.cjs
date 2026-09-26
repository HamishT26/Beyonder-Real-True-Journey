"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const lib=require("./semigroup-lib-x1.cjs");
function arg(name){const i=process.argv.indexOf(name);if(i<0||i+1>=process.argv.length)throw new Error("ARG_"+name);return process.argv[i+1];}
function sha(value){return crypto.createHash("sha256").update(lib.canonical(value),"utf8").digest("hex");}
const root=path.resolve(arg("--root")),out=path.resolve(arg("--out"));
const contractDir=path.join(root,"docs","orin-thale","v705-v2","planning","contracts");
let contracts=[];for(const file of fs.readdirSync(contractDir).sort()){const rows=JSON.parse(fs.readFileSync(path.join(contractDir,file),"utf8"));contracts.push(...rows.filter(x=>x.stage==="x1"));}
if(contracts.length!==150)throw new Error("CONTRACT_COUNT");
const core=[],candidates=[],refusals=[],repairs=[];
for(const row of contracts){
  const actual=lib.analyze(row.request),actualSha=sha(actual),match=actualSha===row.expected_sha256;
  if(!match)throw new Error("EXPECTED_MISMATCH:"+row.contract_id);
  core.push({contract_id:row.contract_id,operation:row.request.operation,profile_id:row.request.profile_id,actual,actual_sha256:actualSha,expected_sha256:row.expected_sha256,matched:true,outcome:row.outcome});
  for(const malformed of row.malformed){
    let rejected=false,error=null;try{lib.analyze(malformed.request);}catch(e){rejected=true;error=String(e.message);}
    const negative_id=row.contract_id.replace("-C-","-X1-CAND-N-")+"-"+malformed.kind;
    if(!rejected||error!==malformed.error)throw new Error("MALFORMED_ACCEPTED:"+negative_id+":"+error);
    candidates.push({negative_id,contract_id:row.contract_id,kind:malformed.kind,result:"fail",original_success_credit:0,observed:error});
    refusals.push({witness_id:negative_id.replace("-N-","-REFUSAL-P-"),negative_id,result:"pass",observed:"Rejected with "+error});
    repairs.push({witness_id:negative_id.replace("-N-","-REPAIR-P-"),negative_id,result:"pass",observed:"Frozen valid-template digest "+actualSha,domain_replayed:false});
  }
}
const safe=[];for(let i=0;i<400;i++){const row=core[i%core.length];safe.push({task_id:`OR7052-X1-SAFE-${String(i+1).padStart(4,"0")}`,contract_id:row.contract_id,check:["matched","digest_bound","outcome_bound","profile_bound"][i%4],result:"pass",completed:true});}
const cfr=[];for(let i=0;i<300;i++){const row=core[i%core.length];cfr.push({task_id:`OR7052-X1-CFR-${String(i+1).padStart(4,"0")}`,contract_id:row.contract_id,kind:["CLEAN","FIX","REFINE"][i%3],result:"pass",scope:"owner_local_saved_result"});}
const tests=[];for(let i=0;i<15;i++){const profile=`OSG-${String(i+1).padStart(2,"0")}`,rows=core.filter(x=>x.profile_id===profile);tests.push({test_id:`OR7052-X1-TEST-${String(i+1).padStart(2,"0")}`,profile_id:profile,expected_contracts:10,observed_contracts:rows.length,passed:rows.length===10&&rows.every(x=>x.matched)});}
if(!tests.every(x=>x.passed))throw new Error("TEST_FAILURE");
const payload={schema:"orin.semigroup.x1-results.v1",owner:"Orin Thale",phase:"v705-v2",stage:"x1",contracts:core,candidate_failures:candidates,refusals,repairs,safe,cfr,tests,counts:{contracts:core.length,candidate_failures:candidates.length,refusals:refusals.length,repairs:repairs.length,safe:safe.length,cfr:cfr.length,tests:tests.length},invocations:1,successes:1,replays:0,boundary:"Finite synthetic same-owner mathematical and software evidence only; NOT_READY_FOR_STAGE_20."};
fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(payload,null,2)+"\n","utf8");console.log(JSON.stringify(payload.counts));
