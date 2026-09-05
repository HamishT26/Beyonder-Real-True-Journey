"""Exact runner smokes, direct package witnesses, and catalogue checks."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parents[2]
sys.path.insert(0, str(ROOT / 'runners'))
sys.path.insert(0, str(ROOT / 'x2'))
import execute_contracts as lab


def write(relative, obj):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as output:
        output.write(obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--meta-script', required=True, type=Path)
    args = parser.parse_args()
    proposals = lab.read('x1/new-proposals.json')['proposals']
    runner_rows = []
    for ordinal, name in enumerate(lab.MODULES, 1):
        proposal = next(p for p in proposals if p['runner'] == name)
        script = 'ghc_family_temporal_' + name + '.py'
        root = ROOT / 'tooling/runner-smokes' / script.removesuffix('.py')
        root.mkdir(parents=True)
        write(root.relative_to(ROOT) / 'positive-input.json', {'family': proposal['family'], 'input': proposal['input']})
        write(root.relative_to(ROOT) / 'duplicate-member-input.json', '{"family":"a","family":"b","input":{}}\n')
        for kind, filename in [('positive', 'positive-input.json'), ('adverse', 'duplicate-member-input.json')]:
            call = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'runners' / script), '--input', str(root / filename), '--output', str(root / (kind + '-output.json'))], capture_output=True, text=True, encoding='utf-8')
            assert call.returncode == 0
        good = json.loads((root / 'positive-output.json').read_text(encoding='utf-8'))
        bad = json.loads((root / 'adverse-output.json').read_text(encoding='utf-8'))
        assert lab.canonical(good) == lab.canonical(proposal['expected_result'])
        assert bad == {'error': 'duplicate_member'}
        receipt = {'schema': 'ghc.family.runner-smoke.v686.v4', 'runner': script, 'positive_pass': True, 'adverse_refused': True,
                   'negative_id': f'AR6864-RUNNER-{ordinal:02}', 'source_proposal': proposal['proposal_id'], 'same_owner_only': True,
                   'initial_adverse_credit': 0, 'source_sha256': hashlib.sha256((ROOT / 'runners' / script).read_bytes()).hexdigest()}
        write(root.relative_to(ROOT) / 'smoke-receipt.json', receipt)
        runner_rows.append(receipt)
    write('tooling/runner-smoke-summary.json', runner_rows)

    import portion as P
    from intervaltree import IntervalTree
    from pyrsistent import freeze, thaw
    union = [list(r) for r in P.to_data(P.closedopen(0, 2) | P.closed(2, 4))]
    positive = union == [[True, 0, 4, True]]
    adverse = union != [[True, 0, 4, False]]
    package_rows = [{'package': 'portion', 'positive_pass': positive, 'adverse_refused': adverse, 'negative_id': 'AR6864-PACKAGE-01', 'actual': union, 'refused_fixture': [[True, 0, 4, False]]}]
    tree = IntervalTree.from_tuples([(0, 4, 'a'), (2, 6, 'b')])
    point = sorted(r.data for r in tree.at(2))
    rejected = False
    try:
        tree.addi(2, 2, 'empty')
    except ValueError:
        rejected = True
    package_rows.append({'package': 'intervaltree', 'positive_pass': point == ['a', 'b'], 'adverse_refused': rejected, 'negative_id': 'AR6864-PACKAGE-02', 'actual': point, 'refused_fixture': 'empty half-open interval'})
    prior = freeze([{'a': 1}])
    later = prior.append(freeze({'b': 2}))
    rejected = False
    try:
        prior[0]['a'] = 5
    except TypeError:
        rejected = True
    package_rows.append({'package': 'pyrsistent', 'positive_pass': thaw(prior) == [{'a': 1}] and thaw(later) == [{'a': 1}, {'b': 2}], 'adverse_refused': rejected, 'negative_id': 'AR6864-PACKAGE-03', 'actual': thaw(later), 'refused_fixture': 'direct persistent-map mutation'})
    assert all(r['positive_pass'] and r['adverse_refused'] for r in package_rows)
    write('x2/toolchain/package-smokes.json', {'schema': 'ghc.family.package-smokes.v686.v4', 'rows': package_rows, 'checks': 6, 'same_owner_only': True, 'independent_reproduction': False})

    spec = importlib.util.spec_from_file_location('bounded_meta', args.meta_script)
    meta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(meta)
    catalogue = meta.build(LANE, ROOT)
    # The compatibility builder assumes root-level scripts. Explicit owner paths
    # adapt that layout without moving files or scanning another lane.
    for receipt in runner_rows:
        script = receipt['runner']
        path = ROOT / 'runners' / script
        catalogue['cards'].append({'card_id': 'runner:' + script, 'name': script, 'kind': 'runner',
                                   'source_path': path.relative_to(LANE).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                   'status': 'current', 'evidence_state': 'validated', 'owner_scope': 'Avelin Reed v686-v4 phase-local',
                                   'triggers': meta.tokens(script), 'caller_paths': [(ROOT / 'tooling/runner-smokes' / script.removesuffix('.py') / 'smoke-receipt.json').relative_to(LANE).as_posix()],
                                   'rollback': 'Select the previous validated source and retain this exact runner and its witnesses.',
                                   'protected_gates': meta.PROTECTED, **meta.route_fields(script)})
    catalogue['cards'].sort(key=lambda row: row['card_id'])
    for card in catalogue['cards']:
        card.update({'execution_authority': 'owner_self_scoped_delta', 'repository_scan': False, 'module_scan': False,
                     'cross_lane_scan': False, 'unchanged_history_scan': False, 'sibling_lane_mutation': False,
                     'source_commit': lab.SOURCE, 'scope_role': 'owner-local capability catalogue; not a canonical validator'})
    catalogue['card_count'] = len(catalogue['cards'])
    validation = meta.validate(catalogue)
    assert validation['valid'] and len(catalogue['cards']) == 15
    collisions = meta.collisions(catalogue)
    query = meta.query(catalogue, argparse.Namespace(kind='runner', status='current', evidence_state='validated', owner_scope=None, trigger=None, endpoint_kind=None))
    assert query['result_count'] == 5
    promotion = [meta.promotion(catalogue, 'skill:' + s['name']) for s in lab.read('x1/skill-runner-plan.json')['skills']]
    assert all(p['state'] == 'ready' for p in promotion)
    write('tooling/meta-tool-box/catalogue.json', catalogue)
    write('tooling/meta-tool-box/validation.json', validation)
    write('tooling/meta-tool-box/collisions.json', collisions)
    write('tooling/meta-tool-box/runner-query.json', query)
    write('tooling/meta-tool-box/promotion-post-audit.json', {'schema': 'ghc.family.promotion-post-audit.v686.v4', 'timing': 'after completed byte-preserving promotions', 'prepromotion_meta_command_claimed': False, 'rows': promotion})
    review = {'schema': 'ghc.family.trigger-overlap-review.v686.v4', 'finding_count': collisions['finding_count'],
              'findings_retained': True, 'selection_rule': 'Choose the exact family listed in the frozen skill contract, then its explicit runner; a lexical overlap never selects a winner.',
              'family_sets_are_disjoint_between_skills': len({f for s in lab.read('x1/skill-runner-plan.json')['skills'] for f in s['families']}) == 20,
              'context_only': True, 'scope': 'Reviewed lexical overlap is not an external behavior or authority claim.'}
    write('tooling/meta-tool-box/overlap-review.json', review)
    write('x2/promotion-procedure-event.json', {'id': 'AR6864-OP012', 'failure': 'Local metadata, accepting/adverse CLI use, collision-free directories, and byte parity were checked before copying, but the separate Meta Tool Box promotion command was omitted before global copying.',
                                            'recovery': 'Retain the procedural lapse and run an explicit post-promotion catalogue, collision, query, and promotion audit. Do not claim the post-audit preceded the copied files; require the Meta Tool Box check before future copies.',
                                            'initial_success_credit': 0, 'lifecycle': 'x2_promotion', 'host_mutation': 'ten authorized new skill directories only', 'recovery_passed': True})
    print(json.dumps({'runner_pairs': 5, 'package_checks': 6, 'catalogue_cards': 15, 'catalogue_valid': True,
                      'lexical_collisions_retained': collisions['finding_count'], 'promotion_post_audit_ready': 10}))


if __name__ == '__main__':
    main()
