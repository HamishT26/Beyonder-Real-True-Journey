'use strict';
const {hash,canonical,safeRelative}=require('./operations.js');
function ingest({source,blob,manifest,contractId,labVersion},state,allowlist){
 if(!source||!/^[a-f0-9]{40}$/.test(source.commit)||!safeRelative(source.path))throw Error('invalid source');
 if(!allowlist.some(a=>a.commit===source.commit&&a.path===source.path))throw Error('out-of-scope source');
 if(!Buffer.isBuffer(blob))throw Error('missing evidence');
 if(blob.length>4*1024*1024)throw Error('evidence too large');
 const binding=manifest?.entries?.find(r=>r.path===source.path);
 if(!binding||binding.bytes!==blob.length||binding.sha256!==hash(blob))throw Error('source checksum mismatch');
 const data=JSON.parse(blob.toString('utf8'));
 const contract=data.contracts?.find(r=>r.contract_id===contractId);
 if(!contract||!['completed','represented','open_gap','exact_gate'].includes(contract.outcome)||hash(canonical(contract.actual))!==contract.result_sha256)throw Error('invalid original result');
 if(typeof labVersion!=='string'||!/^[a-f0-9]{64}$/.test(labVersion))throw Error('lab version required');
 const key=hash(canonical({source,contractId}));
 if(state.has(key))throw Error('duplicate receipt');
 const card={schema:'ghc.lab.evidence-card.v1',receipt_id:key,owner:data.owner,phase:data.phase,source:{...source,bytes:blob.length,sha256:hash(blob),manifest_path:'docs/avelin-reed/v707-v6/manifest.json',json_pointer:'/contracts/'+data.contracts.indexOf(contract)},inputs:contract.request,result:contract.actual,original_outcome:contract.outcome,original_result_sha256:contract.result_sha256,original_negative_ids:contract.mutations.map(x=>x.negative_id),checks:['exact source allowlist','source blob bytes and SHA-256 match source manifest','nested original result digest','original outcome preserved','duplicate receipt absent'],limitations:['Imported finite/synthetic evidence; not independently reproduced.','Zero new domain-completion credit.','Open gaps and authority limitations remain open.'],new_domain_completion_credit:0,source_execution_replayed:false,lab_version_sha256:labVersion,superseded_record_links:[]};
 state.add(key);return card;
}
module.exports={ingest};
