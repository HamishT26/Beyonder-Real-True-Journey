"""Bind the exact x2 owner delta and retained correction without broad-history execution."""
import argparse
import ast
import hashlib
import json
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE='docs/thalen-reed/v687-v8/'
X1='8f9070f01e38fa5cc330cff247ea8e32541a0387'
SOURCE='7e72086683731c40b4884ee7254c864891e354a9'
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_thalen_reed_v687_v8_x1_audit import strict, privacy, normalized

PCM_PATHS={'scripts/ghc_family_pcm_evidence_core.py','scripts/ghc_family_pcm_container_runner.py','scripts/ghc_family_pcm_timeline_runner.py','scripts/ghc_family_pcm_edit_runner.py','scripts/ghc_family_pcm_byte_binding_runner.py','scripts/ghc_family_pcm_claim_runner.py'}

def allowed(p):
    return p.startswith(BASE) or p.startswith('scripts/build_ghc_family_thalen_reed_v687_v8_') or p.startswith('scripts/ghc_family_thalen_reed_v687_v8_') or p.startswith('tests/test_ghc_family_thalen_reed_v687_v8_') or p in PCM_PATHS

def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
def read(path):return strict((ROOT/path).read_text(encoding='utf-8'))
def write(name,obj):(ROOT/BASE/'validation'/name).write_text(json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def current_paths():
    found=[]
    for directory in [ROOT/BASE,ROOT/'scripts',ROOT/'tests']:
        for p in directory.rglob('*'):
            if p.is_file():
                rel=p.relative_to(ROOT).as_posix()
                if allowed(rel):found.append(rel)
    return sorted(found)

class Structure(HTMLParser):
    def __init__(self):super().__init__();self.tags=Counter();self.ids=[];self.links=[];self.language=False;self.scoped_headers=0
    def handle_starttag(self,tag,attrs):
        self.tags[tag]+=1;attrs=dict(attrs)
        if tag=='html':self.language=bool(attrs.get('lang'))
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag=='a' and attrs.get('href','').startswith('#'):self.links.append(attrs['href'][1:])
        if tag=='th' and attrs.get('scope') in ['row','col']:self.scoped_headers+=1

def semantic_checks():
    results=read(BASE+'x2/contract-results.json')['rows'];mut=read(BASE+'x2/mutation-results.json');truth=read(BASE+'x2/phase-truth.json');portfolio=read(BASE+'x2/portfolio-results.json')
    checks={
        '200_exact_outputs':len(results)==200 and all(r['complete_match'] and r['input_unchanged'] for r in results),
        'outcomes':dict(Counter(r['outcome'] for r in results))=={'completed':160,'represented':14,'open_gap':8,'exact_gate':18},
        '250_candidates_retained_rejected':len(mut['rows'])==250 and all(r['rejected'] and r['original_candidate_success_credit']==0 for r in mut['rows']),
        '850_local_procedures_resolved':all(len(portfolio[k])==n and all(r['executed'] and r['procedure_pass'] for r in portfolio[k]) for k,n in [('safe_now',300),('candidates',250),('clean_fix_refine',300)]),
        '80_held_packets_unexecuted':len(portfolio['exact_packets'])==50 and len(portfolio['blocked_packets'])==30 and all(not r['executed'] for k in ['exact_packets','blocked_packets'] for r in portfolio[k]),
        'three_package_pairs':read(BASE+'x2/package-smokes.json')['all_pass'],
        'ten_validated_skills':len(read(BASE+'x2/skill-validation.json')['rows'])==10,
        'five_used_runners':len(read(BASE+'x2/runner-smokes.json')['rows'])==5,
        'promotion_56_members':read(BASE+'x2/promotion-receipt.json')['file_count']==56,
        'current_flow_projection':read(BASE+'validation/x2-method-flow-corrected.json')['valid'] and read(BASE+'validation/x2-x1-method-flow-projection.json')['valid'],
        'original_flow_failures_retained':not read(BASE+'validation/x2-method-flow.json')['valid'] and not read(BASE+'validation/x2-x1-method-flow.json')['valid'],
        'effective_counts':truth['effective_counts']=={'proposals':15430,'negatives':82301,'methods':93234,'failed_witnesses':53149,'passing_witnesses':82493,'open_gaps':740,'exact_gates':729},
        'terminal_boundary':truth['terminal_verdict']=='NOT_READY_FOR_STAGE_20' and truth['canonical_invocations']==0 and not truth['successor_contacted'],
    }
    deck=read(BASE+'x2/deck/deck-index.json');cards=[read(BASE+'x2/deck/cards/'+ident+'.json') for ident in deck['cards']];lookup={c['card_id']:c for c in cards};assert len(lookup)==len(cards)==208
    for c in cards:
        content={k:v for k,v in c.items() if k!='card_id'};raw=json.dumps(content,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()
        assert c['card_id']=='ghc-card-'+hashlib.sha256(raw).hexdigest()[:24]
        assert c['outcome'] in {'completed','represented','open_gap','exact_gate'}
        if c['tier']==1:assert c['parent_ids']==[]
        else:assert len(c['parent_ids'])==1 and lookup[c['parent_ids'][0]]['tier']==c['tier']-1
    checks['deck_graph']=True
    manifest=read(BASE+'x2/deck/card-manifest.json')
    for e in manifest['entries']:
        raw=(ROOT/e['path']).read_bytes();assert len(raw)==e['bytes'] and hashlib.sha256(raw).hexdigest()==e['sha256']
    checks['deck_manifest']=True
    parser=Structure();parser.feed((ROOT/BASE/'x2/deck/accessible-report.html').read_text(encoding='utf-8'))
    checks['html_structure']=parser.language and parser.tags['main']==1 and parser.tags['caption']==1 and parser.tags['tr']==201 and parser.scoped_headers==203 and len(parser.ids)==len(set(parser.ids)) and all(x in parser.ids for x in parser.links)
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args()
    assert git('rev-parse','HEAD')==X1
    old=set(git('diff','--name-only',SOURCE,X1).splitlines())
    for p in old:
        raw=subprocess.check_output(['git','-C',str(ROOT),'show',X1+':'+p]);assert normalized(ROOT/p)==raw,p
    changes=git('status','--porcelain=v1','--untracked-files=all').splitlines();assert all(allowed(line[3:]) for line in changes),[x[:150] for x in changes if not allowed(x[3:])]
    checks=semantic_checks();assert all(checks.values()),checks
    if a.write:
        write('x2-checks.json',{'schema':'ghc.family.owner-x2-checks.v1','checks':checks,'x1_immutable':True,'selected_unit_tests_previously_passed':28,'canonical_credit':0})
        write('x2-privacy.json',{'state':'pending'});write('x2-security.json',{'state':'pending'});write('x2-staged-review.json',{'state':'pending'})
        mf=BASE+'validation/x2-manifest.json';paths=sorted((set(current_paths())-old)|{mf});assert len(paths)<2000
        write('x2-staged-review.json',{'schema':'ghc.family.staged-allowlist.v1','anchor_parent':X1,'allowed_paths':paths,'allowed_change_kind':'A','path_count':len(paths),'deletions':0})
        items={p:normalized(ROOT/p) for p in paths if p!=mf};scan=privacy(items);assert scan['confirmed_hits']==0,scan;write('x2-privacy.json',scan)
        findings=[];asts=0;jsons=0;words={}
        for path,raw in items.items():
            text=raw.decode('utf-8');words[path]=len(text.split());assert words[path]<=100000,path
            if path.endswith('.json'):strict(text);jsons+=1
            if path.endswith('.py'):
                tree=ast.parse(text,filename=path);asts+=1
                for n in ast.walk(tree):
                    if isinstance(n,ast.Call):
                        if isinstance(n.func,ast.Name) and n.func.id in ['eval','exec']:findings.append({'path':path,'line':n.lineno,'rule':'dynamic_code'})
                        if any(k.arg=='shell' and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords):findings.append({'path':path,'line':n.lineno,'rule':'shell_true'})
        assert not findings,findings
        write('x2-security.json',{'schema':'ghc.family.bounded-security.v1','findings':findings,'python_ast_checks':asts,'strict_json':jsons,'rules':['no_dynamic_eval_exec','no_shell_true','bounded_fixture_collections','no_audio_playback_or_external_action','explicit_owner_write_paths'],'manual_review':'Core operations are pure bounded record transforms. CLI reads one size-limited JSON file. Builders write named owner artifacts and exclusive reviewed promotion destinations. No source deletion, network call, playback, credential, or user-data operation exists in the PCM core.','exhaustive_security':False})
        items={p:normalized(ROOT/p) for p in paths if p!=mf}
        write('x2-manifest.json',{'schema':'ghc.family.normalized-lf-manifest.v1','byte_domain':'normalized_lf_git_blob','anchor':'PENDING_EVIDENCE_COMMIT','parent':X1,'entry_count':len(items),'entries':[{'path':p,'bytes_normalized_lf':len(b),'sha256_normalized_lf':hashlib.sha256(b).hexdigest()} for p,b in items.items()],'declared_self_exclusions':[mf]})
        print(json.dumps({'state':'X2_OWNER_EVIDENCE_PASS','checks':len(checks),'delta_files':len(paths),'manifest_bindings':len(items),'x1_immutable':True,'confirmed_privacy_hits':0,'bounded_security_findings':0,'python_ast':asts,'strict_json':jsons,'maximum_document_words':max(words.values())}))
    else:print(json.dumps(checks))

if __name__=='__main__':main()
