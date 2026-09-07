"""Join observed owner results into Method Flow and an addressable evidence deck."""
import collections,copy,hashlib,html,json,pathlib
from build_ghc_family_svg_x1 import ROOT,BASE,BANK,SOURCE,GATES,BOUNDARY,BASELINE,write,strict,sha
X1='974183bd5a670e42aac60223f76fa44f9a87313a'

def main():
 assert not (BASE/'x2/method-flow/ledger.json').exists(),'Existing Method Flow must not be regenerated or overwritten'
 assert not (BASE/'x2/deck').exists(),'Existing addressable deck must not be regenerated'
 ledger=strict((BASE/'x1/method-flow/ledger.json').read_bytes());ledger['x1_commit']=X1
 ps=strict((BASE/'x1/new-proposals.json').read_bytes())['proposals'];pm={p['proposal_id']:p for p in ps}
 def method(label,title):
  mid='OP6882-X2-M-'+label
  record={'method_id':mid,'title':title,'failure_signature':title,'trigger_preconditions':['Frozen SVG contract or interface state'],'privacy_class':'sanitized_public','approval_class':'safe_now','candidate_workaround':'Preserve the complete immutable definition and failed candidate; accept only the declared bounded result.','validation_witness_ids':[],'recurrence_guard':'Check exact types, complete keys, provenance and scope before interpreting a pass.','rollback':'Stop selecting the candidate; retain source, failed witnesses and narrow recoveries.','recommendation_state':'candidate','supersedes':[],'protected_gates':GATES,'retained_negative_ids':[],'scope_boundary':BOUNDARY,'execution_authority':'owner_self_scoped_delta','source_commit':SOURCE,'final_commit':None,'repository_scan':False,'module_scan':True,'cross_lane_scan':False,'unchanged_history_scan':False,'sibling_lane_mutation':False,'changed_file_allowlist':[],'module_allowlist':['scripts/orren_pike_v688_v2/ghc_family_svg_evidence_core.py'],'exact_pushed_head_required':True}
  ledger['methods'].append(record);return record
 def witness(m,label,result,expected,observed):
  wid=m['method_id']+'-'+label;negative='OP6882-NEG-'+label if result=='fail' else None
  if negative:m['retained_negative_ids'].append(negative)
  ledger['witnesses'].append({'witness_id':wid,'method_id':m['method_id'],'procedure':m['title'],'scope':'Orren Pike v688-v2 frozen SVG evidence only','expected':expected,'observed':observed,'result':result,'same_owner_only':True,'independent_reproduction':False,'retained_negative_ids':[negative] if negative else [],'boundary':BOUNDARY});m['validation_witness_ids'].append(wid)
 results=strict((BASE/'x2/contract-results.json').read_bytes())['rows'];mut=strict((BASE/'x2/mutation-results.json').read_bytes())['rows'];port=strict((BASE/'x2/portfolio-results.json').read_bytes())
 for op in dict.fromkeys(p['operation'] for p in ps):
  m=method(op,'Reject altered complete outputs for '+op)
  for r in results:
   if pm[r['proposal_id']]['operation']!=op:continue
   assert r['pass'];witness(m,r['proposal_id']+'-RESULT','pass',pm[r['proposal_id']]['expected_output'],r['actual_output'])
  for r in mut:
   if pm[r['proposal_id']]['operation']!=op:continue
   assert r['rejected'];witness(m,r['candidate_id']+'-CANDIDATE','fail','Complete frozen output',r['candidate_output']);witness(m,r['candidate_id']+'-REFUSAL','pass','Reject altered output',{'rejected':True,'original_candidate_credit':0})
  m=method('interface-'+op,'Refuse duplicate keys and nonfinite JSON for '+op)
  for r in port['safe']:
   if r['kind']!='json_interface' or pm[r['proposal_id']]['operation']!=op:continue
   assert r['pass']
   if r['refused']:witness(m,r['procedure_id']+'-INVALID','fail','A valid uniquely keyed finite JSON request',{'refusal':r['refusal_reason'],'input_serialization_sha256':r['input_serialization_sha256']})
   witness(m,r['procedure_id']+'-CHECK','pass','Declared interface acceptance or refusal',r)
 m=method('cfr','Normalize, recover, and explain frozen records without erasing failed candidates')
 for r in port['clean_fix_refine']:
  assert r['pass']
  if r['kind']=='FIX':witness(m,r['procedure_id']+'-BROKEN','fail','Complete value field retained',r['failed_candidate'])
  witness(m,r['procedure_id']+'-CHECK','pass',r['purpose'],r)
 for r in strict((BASE/'x2/skill-use.json').read_bytes())['rows']:
  m=method(r['name'],'Portable skill complete output and duplicate-key boundary')
  witness(m,r['name']+'-INVALID','fail','Uniquely keyed finite JSON',r['adverse'])
  witness(m,r['name']+'-LOCAL','pass','Frozen accepting output',r['positive'])
  witness(m,r['name']+'-REFUSAL','pass','Duplicate-key refusal',r['adverse'])
  witness(m,r['name']+'-GLOBAL','pass','Byte-equal global package accepts the same fixture',r['positive'])
 for r in strict((BASE/'x2/runner-use.json').read_bytes())['rows']:
  m=method(r['name'].replace('.py',''),'Four-operation runner preserves scope and refuses duplicate JSON')
  witness(m,r['name']+'-INVALID','fail','Uniquely keyed finite JSON',r['adverse']);witness(m,r['name']+'-REFUSAL','pass','Duplicate-key refusal',r['adverse'])
  for op in r['operations']:
   for where in ['LOCAL','GLOBAL']:witness(m,op['operation']+'-'+where,'pass','Complete frozen accepting output',op['actual_output'])
 package=strict((BASE/'x2/package-smokes.json').read_bytes())
 for name in package['versions']:
  m=method('package-'+name.replace('.','-'),'Pinned '+name+' synthetic behavior and adverse input')
  witness(m,name+'-INVALID','fail','Valid package-level grammar or attribute',package['adverse'][name]);witness(m,name+'-REFUSAL','pass','Refuse adverse package input',package['adverse'][name]);witness(m,name+'-POSITIVE','pass','Declared synthetic geometry or serialization',package['positive'][name])
 for m in ledger['methods'][14:]:
  assert m['retained_negative_ids'] and any(w['method_id']==m['method_id'] and w['result']=='pass' for w in ledger['witnesses'])
  m['recommendation_state']='preferred'
  for a,b in [('observed','candidate'),('candidate','validated'),('validated','preferred')]:ledger['state_events'].append({'method_id':m['method_id'],'from':a,'to':b,'note':'The passing witness is separate from the retained failed candidate.'})
 counts={'methods':len(ledger['methods']),'witnesses':len(ledger['witnesses']),'state_events':len(ledger['state_events']),'recommendations':len(ledger['recommendations']),'states':{x:sum(m['recommendation_state']==x for m in ledger['methods']) for x in ['observed','candidate','validated','preferred','superseded','deprecated']},'witness_results':dict(collections.Counter(w['result'] for w in ledger['witnesses']))};ledger['counts']=counts
 write('x2/method-flow/ledger.json',ledger)
 outcomes=dict(collections.Counter(r['outcome'] for r in results));effective={**BASELINE,'proposals':15830,'negatives':BASELINE['negatives']+counts['witness_results']['fail'],'methods':BASELINE['methods']+counts['methods'],'failed_witnesses':BASELINE['failed_witnesses']+counts['witness_results']['fail'],'passing_witnesses':BASELINE['passing_witnesses']+counts['witness_results']['pass'],'open_gaps':BASELINE['open_gaps']+outcomes.get('open_gap',0),'exact_gates':BASELINE['exact_gates']+outcomes.get('exact_gate',0)}
 write('x2/retained-negative-register.json',{'source':SOURCE,'activation_baseline':BASELINE,'effective_counts':effective,'failed_witness_refs':[w['witness_id'] for w in ledger['witnesses'] if w['result']=='fail'],'failures_erased':0,'failures_promoted':0,'count_boundary':'Rejected synthetic candidates have zero original success credit; successful refusals and recoveries are separate same-owner witnesses.'})
 for label in ['open_gap','exact_gate']:write('x2/'+label.replace('_','-')+'-register.json',{'inherited':BASELINE['open_gaps' if label=='open_gap' else 'exact_gates'],'added':outcomes.get(label,0),'refs':[r['proposal_id'] for r in results if r['outcome']==label],'closed_by_software':0,'boundary':BOUNDARY})
 truth={'owner':'Orren Pike','phase':'v688-v2','source':SOURCE,'x1':X1,'state':'X2_EVIDENCE_PREPARED','outcomes':outcomes,'effective_counts':effective,'owner_method_flow':counts,'canonical_invocations':0,'canonical_successes':0,'canonical_replays':0,'successor_contacts':0,'full_repository_suite':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'};write('x2/phase-truth.json',truth)
 identity=strict((BASE/'x1/identity.json').read_bytes());cards=[]
 def card(tier,title,parent,content,outcome='represented'):
  v={'schema':'ghc.family.flashcard.v1','tier':tier,'title':title,'parent_ids':[] if parent is None else [parent],'owner':'Orren Pike','phase':'v688-v2','content':content,'outcome':outcome,'stability':'stable' if tier<=2 else 'volatile','source_refs':[SOURCE,X1],'protected_gates':GATES,'boundary':BOUNDARY};v['card_id']='ghc-card-'+sha(v)[:24];cards.append(v);return v['card_id']
 root=card(1,'Orren Pike relational anchor',None,identity)
 pillars={name:card(2,name,root,{'evidence_class':'synthetic or symbolic only','empirical_or_authority_credit':False}) for name in ['GMUT Mind','THOS Body','Freed ID and CBR Heart']}
 practices={r['name']:card(3,r['name'],pillars[r['pillar']],{'qualification':False,'real_practice':False}) for r in identity['practices']}
 for p,r in zip(ps,results):card(4,p['title'],practices[p['practice']],{'proposal':p,'result':r},r['outcome'])
 for m in ledger['methods']:card(4,m['title'],next(iter(practices.values())),{'method':m,'witnesses':[w for w in ledger['witnesses'] if w['method_id']==m['method_id']],'state_events':[e for e in ledger['state_events'] if e['method_id']==m['method_id']]},'completed')
 ids={c['card_id']:c for c in cards};assert len(ids)==len(cards)
 for c in cards:
  if c['tier']>1:assert len(c['parent_ids'])==1 and ids[c['parent_ids'][0]]['tier']==c['tier']-1
  write('x2/deck/cards/'+c['card_id']+'.json',c)
 write('x2/deck/deck-index.json',{'schema':'ghc.family.deck-index.v1','source':SOURCE,'x1':X1,'cards':[c['card_id'] for c in cards],'counts':dict(collections.Counter(c['tier'] for c in cards)),'unresolved_parents':0,'cache_or_identity_benefit_claimed':False})
 write('x2/deck/stable-prefix.json',{'cards':[c['card_id'] for c in cards if c['tier']<=2]});write('x2/deck/volatile-index.json',{'cards':[c['card_id'] for c in cards if c['tier']>2],'implicit_completion':False})
 sections=['Identity and corrigibility','Current route and release','Immutable source and lifecycle','Frozen proposal contracts','Trinity evidence boundaries','Four synthetic practices','Concrete task and method cards','Method Flow retained failures','Open gaps and exact gates','Validation and manifests','Workload and accessibility','Successor ideas','Compact activation index']
 write('x2/deck/baton-index.json',{'sections':sections,'section_count':13,'live_delivery':False})
 page='<!doctype html><html lang="en"><meta charset="utf-8"><title>Orren Pike SVG evidence deck</title><body><a href="#main">Skip to table</a><main id="main"><h1>Bounded SVG contract evidence</h1><p>'+html.escape(BOUNDARY)+'</p><table><caption>Complete frozen contract outcomes</caption><thead><tr><th scope="col">Contract</th><th scope="col">Rule</th><th scope="col">Outcome</th></tr></thead><tbody>'
 for p,r in zip(ps,results):page+='<tr><th scope="row">'+p['proposal_id']+'</th><td>'+html.escape(p['title'])+'</td><td>'+r['outcome']+'</td></tr>'
 page+='</tbody></table><p>Manual keyboard, assistive-technology, cognitive, responsive, language and affected-user evaluation remain open. No complete accessibility claim.</p></main></body></html>\n';(BASE/'x2/deck/accessible-report.html').write_text(page,encoding='utf-8',newline='\n')
 (BASE/'x2/deck/compact-activation.md').write_text('Orren Pike v688-v2 remains PREPARED_NOT_SENT. Tamar Vey v688-v3 is prospective after exact final, one successful canonical and current guard reread. The final baton will bind exact immutable anchors.\n',encoding='utf-8',newline='\n')
 entries=[]
 for p in sorted((BASE/'x2/deck').rglob('*')):
  if p.is_file():raw=p.read_bytes();entries.append({'path':p.relative_to(BASE/'x2/deck').as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 write('x2/deck/card-manifest.json',{'entries':entries,'self_exclusion':'card-manifest.json','count':len(entries)})
 write('x2/complete-incomplete.json',{'completed_scope':['200 complete typed output checks','300 safe procedures','250 candidate rejections','300 CLEAN/FIX/REFINE procedures','10 local and global skills','5 local and global runners','3 pinned packages','four-tier deck'],'represented_scope':['SVG metadata and declarations','GMUT exact symbolic path-state proxy','THOS software workflow proxy','Freed ID relational records and CBR reservations'],'open_gaps':['Two unresolved synthetic local fragments','Independent and empirical evaluation','Full accessibility and privacy evaluation'],'exact_gates':['Three external-reference requests','50 exact packets','30 blocked packets','All protected competent and affected authority decisions'],'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
 overview=(BASE/'x1/integrated-overview.html').read_text().replace('planning overview','x2 evidence overview').replace('The complete planning contract','The bounded executed contract').replace('Execution and terminal conditions','Evidence and terminal conditions')
 overview=overview.replace('</main>','<p>'+html.escape(json.dumps(truth['outcomes']))+'; '+html.escape(json.dumps(effective))+'</p></main>');(BASE/'x2/integrated-overview.html').write_text(overview,encoding='utf-8',newline='\n')
 print(json.dumps({'method_flow':counts,'effective':effective,'cards':len(cards),'deck_manifest_entries':len(entries)}))
if __name__=='__main__':main()
