from pathlib import Path
import copy,hashlib,importlib.util,json

R=Path('D:/GHC-Archives/worktrees/rowan-ash-main');B=R/'docs/rowan-ash/v689-v5';F=B/'final';BANK=Path(__file__).parent
path=F/'ghc_family_owner_canonical.py'
spec=importlib.util.spec_from_file_location('rowan_canonical_preflight',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(p):return json.loads(p.read_bytes())
cards=[read(p) for p in sorted((B/'deck/cards').glob('*.json'))]
p=read(B/'plan/new-proposals.json')['proposals'][0];r=read(B/'x1/results.json')['safe'][0]
synthetic_final='f'*40
anchors=[[synthetic_final,m.X2],[m.X2,m.X1],[m.X1,m.PLANNING],[m.PLANNING,m.SOURCE]]
actual_paths=[p.relative_to(R).as_posix() for p in B.rglob('*') if p.is_file()]+['scripts/'+name for name in sorted(m.SCRIPT_NAMES)]+['tests/'+name for name in sorted(m.TEST_NAMES)]
bad_anchors=copy.deepcopy(anchors);bad_anchors[0][1]=m.X1
bad_cards=copy.deepcopy(cards);leaf=next(c for c in bad_cards if c['tier']==4);leaf['parent_ids']=['ghc-card-missing-parent'];value=dict(leaf);value.pop('card_id');leaf['card_id']='ghc-card-'+m.digest(value)[:24]
bad_receipt=copy.deepcopy(r);bad_receipt['observed']['value']=None
definitions=[
 ('owner_ancestry',lambda:m.check_anchors(anchors,synthetic_final),lambda:m.check_anchors(bad_anchors,synthetic_final),'E_OWNER_ANCESTRY','Synthetic final label supplies no actual final-commit claim.'),
 ('owner_path_scope',lambda:m.check_paths(actual_paths),lambda:m.check_paths(actual_paths+['../sibling/private.txt']),'E_PATH_ESCAPE','The adverse path is data only and is never read or written.'),
 ('card_parent_graph',lambda:m.check_card_graph(cards),lambda:m.check_card_graph(bad_cards),'E_CARD_PARENT','The leaf digest is recomputed so this tests its missing parent, not a stale digest.'),
 ('observed_receipt_binding',lambda:m.check_safe_receipt(r,p),lambda:m.check_safe_receipt(bad_receipt,p),'E_OBSERVED_BINDING','A true passed flag cannot override a changed observed value.')]
rows=[]
for name,good,bad,expected,boundary in definitions:
 good();observed=None
 try:bad()
 except ValueError as error:observed=str(error)
 assert observed==expected,(name,observed,expected)
 rows.append({'name':name,'positive_passed':True,'adverse_subject_success_credit':0,'expected_refusal':expected,'observed_refusal':observed,'guard_passed':True,'boundary':boundary})
receipt={'schema':'ghc.family.canonical-component-preflight.v1','component_checks':rows,'positive_controls':4,'adverse_subjects':4,'refusal_guards_passed':4,'canonical_invocations':0,'source_or_phase_calculations_reexecuted':0,'canonical_entrypoint_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'scope':'Pure validator predicates only. The exact-final canonical has not been invoked.'}
(F/'canonical-preflight.json').write_bytes((json.dumps(receipt,indent=2,sort_keys=True)+'\n').encode());print(json.dumps(receipt),flush=True)
