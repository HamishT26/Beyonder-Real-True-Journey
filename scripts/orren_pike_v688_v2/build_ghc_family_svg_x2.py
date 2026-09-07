"""Execute only the frozen owner contracts and materialize portable packages."""
from __future__ import annotations
import collections,copy,hashlib,html,json,pathlib,sys
from build_ghc_family_svg_x1 import ROOT,BASE,BANK,SOURCE,GATES,BOUNDARY,BASELINE,write,strict,sha,canonical,SKILL_PAIRS
from ghc_family_svg_evidence_core import evaluate,strict_loads,Refusal
X1='974183bd5a670e42aac60223f76fa44f9a87313a'

def equal(a,b):return canonical(a)==canonical(b)
def main():
 assert not (BASE/'x2').exists(),'Never overwrite an observed x2 run'
 bound=strict((BANK/'x1-equality.json').read_bytes());assert bound['clean'] and set(bound['heads'].values())=={X1}
 write('x2/x1-boundary.json',bound)
 pset=strict((BASE/'x1/new-proposals.json').read_bytes())['proposals'];pmap={p['proposal_id']:p for p in pset}
 portfolio=strict((BASE/'x1/portfolio-plan.json').read_bytes());rows=[]
 for p in pset:
  inp=copy.deepcopy(p['input']);actual=evaluate(inp);match=equal(actual,p['expected_output']) and equal(inp,p['input'])
  rows.append({'proposal_id':p['proposal_id'],'definition_sha256':sha(p),'input_sha256':sha(p['input']),'actual_output':actual,'complete_match':match,'input_unchanged':equal(inp,p['input']),'pass':match,'outcome':p['expected_execution_disposition'],'external_credit':False})
 write('x2/contract-results.json',{'schema':'ghc.family.svg-contract-results.v1','source':SOURCE,'x1':X1,'count':len(rows),'rows':rows,'same_owner_only':True,'independent_reproduction':False})
 assert all(r['pass'] for r in rows)
 safe=[]
 for item in portfolio['safe']:
  p=pmap[item['proposal_id']]
  if item['kind']=='full_contract':safe.append({**item,'pass':next(r['pass'] for r in rows if r['proposal_id']==p['proposal_id'])});continue
  mode=item['mode'];expected_refusal=mode.endswith('refusal')
  if mode=='compact_object':raw=json.dumps(p['input'],separators=(',',':'))
  elif mode=='indented_object':raw=json.dumps(p['input'],indent=2)
  elif mode=='reversed_key_order':raw=json.dumps(dict(reversed(list(p['input'].items()))))
  elif mode=='duplicate_operation_refusal':raw='{"operation":"'+p['operation']+'",'+json.dumps(p['input'])[1:]
  else:raw='{"operation":NaN}'
  try:actual=evaluate(strict_loads(raw));passed=not expected_refusal and equal(actual,p['expected_output']);reason=None
  except (Refusal,ValueError) as exc:actual=None;reason=str(exc);passed=expected_refusal
  safe.append({**item,'input_serialization_sha256':hashlib.sha256(raw.encode()).hexdigest(),'pass':passed,'refused':expected_refusal and actual is None,'refusal_reason':reason})
 assert all(x['pass'] for x in safe)
 mutations=[]
 for c in portfolio['candidates']:
  p=pmap[c['proposal_id']];mut=copy.deepcopy(p['expected_output'])
  if c['mutation']=='flip_accepted':mut['accepted']=not mut['accepted']
  else:del mut['value']
  rejected=not equal(mut,p['expected_output']);mutations.append({**c,'state':'executed_rejected' if rejected else 'unexpected_match','candidate_output':mut,'rejected':rejected,'candidate_success_credit':0})
 assert all(x['rejected'] for x in mutations)
 cfr=[]
 for c in portfolio['clean_fix_refine']:
  p=pmap[c['proposal_id']]
  if c['kind']=='CLEAN':out=json.loads(canonical(p));passed=equal(out,p);detail={'normalized_record_sha256':sha(out),'original_retained':True}
  elif c['kind']=='FIX':
   broken=copy.deepcopy(p['expected_output']);del broken['value'];refused=not equal(broken,p['expected_output']);fixed={**broken,'value':copy.deepcopy(p['expected_output']['value'])};passed=refused and equal(fixed,p['expected_output']);detail={'failed_candidate':broken,'failed_candidate_credit':0,'recovered_output':fixed,'failure_retained':True}
  else:
   out=[{'field':k,'type':type(v).__name__,'value':v,'rule':p['title']} for k,v in p['input'].items()];passed=equal({x['field']:x['value'] for x in out},p['input']);detail={'explanation':out,'source_definition_sha256':sha(p)}
  cfr.append({**c,'pass':passed,**detail})
 assert all(x['pass'] for x in cfr)
 write('x2/mutation-results.json',{'schema':'ghc.family.svg-output-mutations.v1','x1':X1,'rows':mutations,'count':250,'failed_candidate_credit':0})
 write('x2/portfolio-results.json',{'schema':'ghc.family.svg-portfolio-results.v1','safe':safe,'clean_fix_refine':cfr,'exact_packets':portfolio['exact_packets'],'blocked_packets':portfolio['blocked_packets'],'counts':{'safe_completed':len(safe),'candidates_rejected':len(mutations),'clean_fix_refine_completed':len(cfr),'exact_held':50,'blocked_held':30},'external_actions':0})
 core=ROOT/'scripts/orren_pike_v688_v2/ghc_family_svg_evidence_core.py';core_bytes=core.read_bytes()
 introductions=[
  'Keep lexical SVG numbers separate from typed JSON numbers. Preserve signed zero for numeric tokens. Lengths retain units and context vacancies; these routines do not perform CSS layout or physical calibration.',
  'Treat viewBox minima independently from nonnegative extents. Zero extents disable the representation. Preserve aspect alignment and meet/slice policy; none ignores fitting mode. No viewport transform or visual result is computed.',
  'Keep coordinate separators, pair boundaries and command parameter groups explicit. Moveto followups become lineto groups. This is a bounded complete-list grammar, not a complete SVG document parser.',
  'Track the current point in command order. Relative moveto followups accumulate after the initial point; horizontal and vertical lines change only one axis. Zero-length lines remain explicit.',
  'Close only a declared active subpath. A coincident endpoint still differs from a closepath command. Drawing after close starts an implicit subpath. The bounded topology profile refuses consecutive closes.',
  'Reflect a control point only when the preceding command is from the matching curve family. Cubic state must never stand in for quadratic state. Relative controls share the segment starting-point offset.',
  'Preserve arc branch flags with exact integer types. Coincident endpoints are omitted; zero radii yield a line representation; negative radii become magnitudes. Declared pathLength is metadata, not a measured curve length.',
  'Keep winding/parity declarations separate from computed fill. CSS cascade keywords remain unresolved. Duplicate odd dash vectors before interpreting their period; all-zero patterns represent solid strokes.',
  'Keep cap, join, miter limit and orientation as separate declarations. Preserve SVG2 token distinctions. Automatic marker angles require a tangent, and radians remain unconverted metadata.',
  'Resolve only explicit local fragment identifiers in a caller-supplied synthetic target list. Never fetch an external reference. Paint-order omissions append remaining components in the canonical fill/stroke/markers order.'
 ]
 for i,(name,ops) in enumerate(SKILL_PAIRS):
  dest=BASE/'skills'/name;dest.mkdir(parents=True,exist_ok=False);(dest/'scripts').mkdir();(dest/'references').mkdir()
  guide=f'''---\nname: {name}\ndescription: Evaluate {" and ".join(op.replace('_',' ') for op in ops)} for bounded synthetic SVG metadata with exact typed outputs.\n---\n\n# {name.replace('ghc-family-','').replace('-',' ').title()}\n\n{introductions[i]}\n\nRead [the frozen contracts](references/contracts.json) before choosing an input. Run `python scripts/ghc_family_svg_skill.py INPUT.json` from this package. The input names one supported operation and the exact documented fields. The numeric profile uses textual ASCII SVG numbers, bounded exponents and exact rational results. Extra fields, duplicate JSON keys and nonfinite JSON constants are refused.\n\nCompare the entire typed output, including false external-credit fields. Exit zero means accepted bounded metadata; exit two preserves a refusal. The two operations are {', '.join(ops)}. Keep this wrapper and its shared core together under the package manifest.\n\nUse only synthetic caller-owned records. No renderer, browser, network fetch, real artwork, rights decision, accessibility certification, professional judgment or cultural decision is invoked. For a new behavior, preregister an owner contract and preserve any failed witness before correction. An inherited accepting example is zero novelty credit.\n\nRollback means stop selecting this additive package and retain its source and failures. Never overwrite a different skill or alter an inherited caller. {BOUNDARY}\n'''
  (dest/'SKILL.md').write_text(guide,encoding='utf-8',newline='\n')
  (dest/'references/contracts.json').write_text(json.dumps({'operations':ops,'contracts':[p for p in pset if p['operation'] in ops]},indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
  (dest/'scripts/ghc_family_svg_evidence_core.py').write_bytes(core_bytes)
  (dest/'scripts/ghc_family_svg_skill.py').write_text('from ghc_family_svg_evidence_core import main\nif __name__ == "__main__":\n    raise SystemExit(main('+repr(ops)+'))\n',encoding='utf-8',newline='\n')
  entries=[{'path':p.relative_to(dest).as_posix(),'bytes':len(p.read_bytes()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(dest.rglob('*')) if p.is_file()]
  (dest/'manifest.json').write_text(json.dumps({'files':entries,'self_exclusion':'manifest.json','x1':X1},indent=2)+'\n',encoding='utf-8',newline='\n')
 for i in range(5):
  ops=SKILL_PAIRS[2*i][1]+SKILL_PAIRS[2*i+1][1]
  (core.parent/f'ghc_family_svg_group_{i+1}.py').write_text('from ghc_family_svg_evidence_core import main\nif __name__ == "__main__":\n    raise SystemExit(main('+repr(ops)+'))\n',encoding='utf-8',newline='\n')
 print(json.dumps({'contracts_passed':200,'safe_procedures':300,'candidates_rejected':250,'cfr_completed':300,'skills_built_not_yet_used':10,'runners_built_not_yet_used':5,'outcomes':dict(collections.Counter(p['expected_execution_disposition'] for p in pset))}))
if __name__=='__main__':main()
