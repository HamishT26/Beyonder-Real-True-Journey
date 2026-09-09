"""One attributable exact-final Rowan validation; no source or suite replay."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

SOURCE = 'd0707cbb99491bbd6b5d652d506dd811b612d587'
PLANNING = 'b1fd358f5197de51fffc6e917becca988ec35056'
X1 = '6ea658e580770c5aef05d7ecf09046f103253763'
X2 = '53f60df337974e46088b21197e720999096b4557'
BRANCH = 'codex/GHC-Family/rowan-ash-main'
PREFIX = 'docs/rowan-ash/v689-v5/'
SCRIPT_NAMES = {
    'ghc_family_geometry_x1.py', 'ghc_family_geometry_x2.py', 'ghc_family_geometry_cli.py',
    'ghc_family_simplicial_faces_orientation.py', 'ghc_family_simplicial_boundary_composition.py',
    'ghc_family_graph_components_cycles.py', 'ghc_family_simplicial_euler_betti.py',
    'ghc_family_simplicial_chain_membership.py', 'ghc_family_cochain_gradient_stokes.py',
    'ghc_family_cochain_adjoint_laplacian.py', 'ghc_family_cochain_dirichlet_energy.py',
    'ghc_family_cochain_gauge_harmonic.py', 'ghc_family_geometry_provenance_authority.py',
}
TEST_NAMES = {'test_ghc_family_geometry_x1.py', 'test_ghc_family_geometry_x2.py'}
OUTCOMES = {'completed': 180, 'represented': 10, 'open_gap': 5, 'exact_gate': 5}


def require(condition, code):
    if not condition:
        raise ValueError(code)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'E_DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def strict_json(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('E_NONFINITE_JSON')))


def check_paths(paths):
    require(bool(paths) and len(paths) == len(set(paths)), 'E_PATH_SET')
    for value in paths:
        path = PurePosixPath(value)
        require(not path.is_absolute() and '..' not in path.parts and '\\' not in value, 'E_PATH_ESCAPE')
        allowed = value.startswith(PREFIX)
        allowed |= len(path.parts) == 2 and path.parts[0] == 'scripts' and path.name in SCRIPT_NAMES
        allowed |= len(path.parts) == 2 and path.parts[0] == 'tests' and path.name in TEST_NAMES
        require(allowed and '__pycache__' not in path.parts and path.suffix != '.pyc', 'E_OWNER_SCOPE')
    return len(paths)


def check_anchors(observed, final):
    expected = [[final, X2], [X2, X1], [X1, PLANNING], [PLANNING, SOURCE]]
    require(observed == expected, 'E_OWNER_ANCESTRY')
    return {'owner_commits': 4, 'merges': 0, 'source': SOURCE}


def check_safe_receipt(row, proposal):
    require(row['proposal_id'] == proposal['proposal_id'], 'E_RECEIPT_ID')
    require(row['passed'] is True and row['input_unchanged'] is True, 'E_RECEIPT_PASS')
    require(row['request_sha256'] == digest(proposal['request']), 'E_REQUEST_BINDING')
    require(row['expected_sha256'] == proposal['expected_sha256'] == digest(proposal['expected']), 'E_ORACLE_BINDING')
    require(digest(row['observed']) == proposal['expected_sha256'], 'E_OBSERVED_BINDING')
    require(row['outcome'] == proposal['expected_disposition'], 'E_OUTCOME')
    return True


def check_card_graph(cards):
    by_id = {card['card_id']: card for card in cards}
    require(len(by_id) == len(cards) == 288, 'E_CARD_COUNT')
    require(Counter(card['tier'] for card in cards) == {1: 1, 2: 3, 3: 4, 4: 280}, 'E_TIERS')
    for card in cards:
        value = dict(card)
        identifier = value.pop('card_id')
        require(identifier == 'ghc-card-' + digest(value)[:24], 'E_CARD_DIGEST')
        require(type(card['tier']) is int and card['outcome'] in OUTCOMES, 'E_CARD_TYPE')
        parents = card['parent_ids']
        if card['tier'] == 1:
            require(parents == [], 'E_ROOT_PARENT')
        else:
            require(len(parents) == 1 and parents[0] in by_id, 'E_CARD_PARENT')
            require(by_id[parents[0]]['tier'] == card['tier'] - 1, 'E_TIER_SKIP')
        require(card['owner'] == 'Rowan Ash' and card['phase'] == 'v689-v5', 'E_CARD_OWNER')
    return {'cards': len(cards), 'roots': 1, 'cycles': 0}


def git(repo, *args):
    executable = shutil.which('git')
    require(executable is not None, 'E_GIT_UNAVAILABLE')
    result = subprocess.run([executable, '-C', str(repo), *args], capture_output=True, timeout=180)
    require(result.returncode == 0, 'E_GIT_' + args[0])
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--expected-final', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, final = args.repo.resolve(), args.expected_final
    require(re.fullmatch('[0-9a-f]{40}', final) is not None, 'E_FINAL_HASH')
    bank = repo.parents[1] / 'phase-banks' / 'rowan-ash-v689-v5' / 'canonical'
    require(args.output.resolve() == (bank / 'exact-final.json').resolve(), 'E_CANONICAL_OUTPUT_SCOPE')
    bank.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    latch = {'owner': 'Rowan Ash', 'phase': 'v689-v5', 'expected_final': final,
             'started_at_utc': started, 'invocations': 1, 'replay_permitted': False}
    with (bank / 'invocation-latch.json').open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(latch, stream, indent=2)
        stream.write('\n')
    checks, raw_cache = [], {}

    def record(name, details):
        checks.append({'name': name, 'passed': True, 'details': details})
        print(json.dumps({'check': name, 'passed': True}), flush=True)

    def raw(relative):
        if relative not in raw_cache:
            path = (repo / relative).resolve()
            require(path.is_relative_to(repo), 'E_PATH_ESCAPE')
            raw_cache[relative] = path.read_bytes()
        return raw_cache[relative]

    def read(relative):
        return strict_json(raw(relative))

    try:
        head = git(repo, 'rev-parse', 'HEAD').decode().strip()
        upstream = git(repo, 'rev-parse', '@{u}').decode().strip()
        tracking = git(repo, 'rev-parse', 'refs/remotes/origin/' + BRANCH).decode().strip()
        branch = git(repo, 'branch', '--show-current').decode().strip()
        remote = git(repo, 'remote', 'get-url', 'origin').decode().strip()
        require(remote == 'https://github.com/HamishT26/Beyonder-Real-True-Journey.git', 'E_REMOTE')
        live_rows = git(repo, 'ls-remote', 'origin', 'refs/heads/' + BRANCH).decode().splitlines()
        require(len(live_rows) == 1, 'E_LIVE_REFERENCE')
        live = live_rows[0].split()[0]
        divergence = list(map(int, git(repo, 'rev-list', '--left-right', '--count', 'HEAD...@{u}').decode().split()))
        require(head == upstream == tracking == live == final and branch == BRANCH, 'E_FINAL_EQUALITY')
        require(divergence == [0, 0] and not git(repo, 'status', '--porcelain=v1').strip(), 'E_CLEAN_STATE')
        record('exact_final_git_state', {'head': head, 'upstream': upstream, 'tracking': tracking, 'fresh_live': live, 'divergence': divergence, 'clean': True})

        ancestry = [line.split() for line in git(repo, 'rev-list', '--parents', SOURCE + '..' + final).decode().splitlines()]
        record('direct_owner_lifecycle', check_anchors(ancestry, final))
        delta = git(repo, 'diff', '--name-status', SOURCE, final).decode().splitlines()
        require(all(line.startswith('A\t') for line in delta), 'E_NONADDITIVE_DELTA')
        paths = [line.split('\t', 1)[1] for line in delta]
        record('owner_delta_scope', {'paths': check_paths(paths), 'all_additive': True, 'sibling_mutations': 0})
        tracked = len(git(repo, 'ls-files', '-z').split(b'\0')) - 1
        materialized = 0
        for folder, directories, files in os.walk(repo):
            directories[:] = [name for name in directories if name != '.git']
            materialized += len(files)
        require(tracked < 2000 and materialized < 2000, 'E_FILE_CAPACITY')
        record('owner_file_capacity', {'tracked': tracked, 'materialized': materialized, 'ceiling': 2000, 'shallow_boundary': SOURCE})

        seal_path = PREFIX + 'final/content-seal.json'
        seal = read(seal_path)
        require(set(paths) == set(seal['entries']) | {seal_path}, 'E_SEAL_SCOPE')
        tree = {}
        for entry in git(repo, 'ls-tree', '-r', '-z', final).split(b'\0'):
            if not entry:
                continue
            metadata, name = entry.split(b'\t', 1)
            tree[name.decode()] = metadata.decode().split()[2]
        for path, item in seal['entries'].items():
            value = raw(path)
            require(len(value) == item['bytes'] and sha(value) == item['sha256'], 'E_FILE_FIXITY')
            oid = hashlib.sha1(('blob ' + str(len(value)) + '\0').encode() + value).hexdigest()
            require(tree.get(path) == oid == item['git_blob_sha1'], 'E_GIT_BYTE_DOMAIN')
        record('exact_owner_content_seal', {'entries': len(seal['entries']), 'self_exclusion': seal_path, 'checkout_git_blob_parity': True})

        definitions = read(PREFIX + 'plan/new-proposals.json')['proposals']
        require(len(definitions) == len({p['proposal_id'] for p in definitions}) == 200, 'E_PROPOSAL_COUNT')
        require(len({digest(p['request']) for p in definitions}) == 200, 'E_REQUEST_UNIQUENESS')
        require(all(digest(p['expected']) == p['expected_sha256'] and p['outcomes_observed'] is False for p in definitions), 'E_FROZEN_ORACLES')
        by_id = {p['proposal_id']: p for p in definitions}
        inherited = read(PREFIX + 'plan/inherited-selections.json')['selections']
        require(len(inherited) == 200 and all(p['new_execution_credit'] == p['new_novelty_credit'] == 0 for p in inherited), 'E_INHERITED_CREDIT')
        record('frozen_proposal_definitions', {'new': 200, 'inherited': 200, 'universal_novelty_claimed': False})

        admitted = []
        for session in ['x1', 'x2']:
            result = read(PREFIX + session + '/results.json')
            require(len(result['safe']) == len(result['candidate']) == 100, 'E_PORTFOLIO_COUNT')
            for row in result['safe']:
                check_safe_receipt(row, by_id[row['proposal_id']])
                admitted.append(row)
            for row in result['candidate']:
                p = by_id[row['proposal_id']]
                require(row['passed'] is True and row['input_unchanged'] is True and row['subject_success_credit'] == 0, 'E_CANDIDATE_CREDIT')
                require(digest(row['observed']) == digest(p['candidate_expected']) and row['request_sha256'] == digest(p['candidate_request']), 'E_CANDIDATE_BINDING')
        require(Counter(row['outcome'] for row in admitted) == OUTCOMES, 'E_CORE_OUTCOMES')
        record('portfolio_receipt_bindings', {'safe': 200, 'candidate_refusal_predicates': 200, 'candidate_subject_successes': 0, 'outcomes': OUTCOMES, 'calculations_reexecuted': 0})

        selected = {p['selection_id']: p for p in inherited}
        for session in ['x1', 'x2']:
            projection = read(PREFIX + session + '/source-projections.json')['projections']
            clean = read(PREFIX + session + '/cleanup-receipt.json')
            require(len(projection) == len(clean['rows']) == clean['passed'] == 100, 'E_CLEANUP_COUNT')
            for row in projection:
                require(len(row['keys']) == len(set(row['keys'])) == len(row['values']), 'E_PROJECTION_SHAPE')
                restored = dict(zip(row['keys'], row['values']))
                require(digest(restored) == selected[row['selection_id']]['source_record_sha256'], 'E_PROJECTION_BINDING')
            require(all(r['passed'] is True and r['source_execution_credit'] == 0 and r['host_cleanup_claimed'] is False for r in clean['rows']), 'E_CLEANUP_CREDIT')
        record('source_record_projection_bindings', {'refinements': 200, 'source_execution_credit': 0, 'host_cleanup_claimed': False})

        for session in ['x1', 'x2']:
            receipt = read(PREFIX + session + '/test-receipt.json')
            lines = receipt['output'].splitlines()
            test_names = [line.split(' ', 1)[0] for line in lines if line.startswith('test_') and line.endswith(' ... ok')]
            require(receipt['returncode'] == 0 and len(test_names) == len(set(test_names)) == 18, 'E_TEST_RECEIPT')
            require(sha(receipt['output'].encode()) == receipt['stderr_sha256'], 'E_TEST_TRANSCRIPT')
        record('invariant_test_receipt_bindings', {'x1': 18, 'x2': 18, 'tests_reexecuted': 0, 'independent_reproduction': False})

        for session in ['x1', 'x2']:
            validations = read(PREFIX + session + '/skill-validation.json')['skills']
            smokes = read(PREFIX + session + '/runner-smokes.json')['smokes']
            require(len(validations) == 10 and all(r['passed'] and r['example_safe_passed'] for r in validations), 'E_SKILL_VALIDATION')
            for row in validations:
                require(sha(raw(PREFIX + 'skills/' + row['name'] + '/SKILL.md')) == row['sha256'], 'E_SKILL_FIXITY')
            require(len(smokes) == 20 and all(r['passed'] for r in smokes), 'E_RUNNER_SMOKES')
        scope = read(PREFIX + 'x2/runner-scope-receipt.json')
        require(scope['passed'] == 10 and all(r['observed']['error'] == 'E_RUNNER_SCOPE' and r['returncode'] == 2 for r in scope['checks']), 'E_RUNNER_SCOPE')
        catalogue = read(PREFIX + 'final/meta-tool-catalogue.json')['cards']
        require(len(catalogue) == 33 and sum(r['kind'] == 'skill' for r in catalogue) == 20, 'E_CATALOGUE')
        require(sum(r.get('paired_interface', False) for r in catalogue) == 10, 'E_PAIRED_RUNNERS')
        require(all(sha(raw(r['source_path'])) == r['sha256'] for r in catalogue), 'E_CATALOGUE_FIXITY')
        record('skills_runners_and_catalogue', {'skills': 20, 'paired_runners': 10, 'shared_modules': 3, 'smokes': 40, 'new_scope_probes': 10, 'global_promotions': 0})

        package_plan = read(PREFIX + 'plan/package-plan.json')
        installation = read(PREFIX + 'x1/package-install-receipt.json')
        smokes = read(PREFIX + 'x1/package-smoke-receipt.json')
        versions = {p['name']: p['version'] for p in package_plan['closure']}
        require(len(versions) == 4 and package_plan['direct_additions'] == installation['direct_additions'] == 3, 'E_PACKAGE_COUNTS')
        require(smokes['versions'] == versions and smokes['passed'] == 6 and smokes['numexpr_threads'] == 2, 'E_PACKAGE_SMOKES')
        require([(p['name'], p['sha256']) for p in package_plan['closure']] == [(p['name'], p['sha256']) for p in installation['closure']], 'E_PACKAGE_HASH_BINDING')
        osv = read(PREFIX + 'x1/package-osv-review.json')
        require(osv['known_advisories'] == 0, 'E_PACKAGE_ADVISORY_REVIEW')
        record('package_receipt_bindings', {'direct_additions': 3, 'closure': versions, 'positive_smokes': 3, 'adverse_smokes': 3, 'known_advisories_at_review': 0, 'packages_reinstalled_or_smoked_again': False})

        interpretation = read(PREFIX + 'x2/interpretation-receipt.json')
        require(len(interpretation['symbolic_derivative_checks']) == 5 and all(r['passed'] and all(v == '0' for v in r['residuals']) for r in interpretation['symbolic_derivative_checks']), 'E_SYMBOLIC_RECEIPT')
        require(len(interpretation['array_energy_comparisons']) == 10 and all(r['passed'] and r['opt_einsum'] == r['numexpr'] == r['frozen_expected'] for r in interpretation['array_energy_comparisons']), 'E_ARRAY_RECEIPT')
        require(interpretation['negative_weight_counterexample']['energy'] == '-1/2' and interpretation['explicit_euler_steps'][-1]['energy_after'] == '2', 'E_COUNTEREXAMPLE')
        require(interpretation['disconnected_counterexample']['energy'] == '0' and interpretation['disconnected_counterexample']['globally_constant'] is False, 'E_CONNECTIVITY')
        record('interpretation_receipt_bindings', {'symbolic_checks': 5, 'library_comparisons': 20, 'assumption_counterexamples': 3, 'physical_law_credit': 0})

        ledger = read(PREFIX + 'final/method-flow-final.json')
        methods = {m['method_id']: m for m in ledger['methods']}
        witnesses = {w['witness_id']: w for w in ledger['witnesses']}
        require(len(methods) == len(ledger['methods']) and len(witnesses) == len(ledger['witnesses']), 'E_LEDGER_UNIQUENESS')
        require(all(w['method_id'] in methods and w['same_owner_only'] is True and w['independent_reproduction'] is False for w in witnesses.values()), 'E_WITNESS_SCOPE')
        require(all(witnesses[i]['method_id'] == m['method_id'] for m in methods.values() for i in m['validation_witness_ids']), 'E_LEDGER_BACKLINK')
        require(ledger['counts']['methods'] == len(methods) and ledger['counts']['witnesses'] == len(witnesses), 'E_LEDGER_COUNT')
        require(ledger['counts']['failed_witnesses'] == sum(w['result'] == 'fail' for w in witnesses.values()) and ledger['counts']['passing_witnesses'] == sum(w['result'] == 'pass' for w in witnesses.values()), 'E_WITNESS_COUNT')
        record('method_flow_bindings', ledger['counts'])

        deck_index = read(PREFIX + 'deck/deck-index.json')
        cards = [read(PREFIX + 'deck/cards/' + identifier + '.json') for identifier in deck_index['card_ids']]
        record('four_tier_deck', check_card_graph(cards))
        deck_manifest = read(PREFIX + 'deck/card-manifest.json')
        require(deck_manifest['self_excluded'] == ['card-manifest.json'], 'E_DECK_SELF_EXCLUSION')
        for name, item in deck_manifest['entries'].items():
            value = raw(PREFIX + 'deck/' + name)
            require(sha(value) == item['sha256'] and len(value) == item['bytes'], 'E_DECK_MANIFEST')
        record('deck_manifest', {'entries': len(deck_manifest['entries']), 'stable_cards': 8, 'volatile_cards': 280})

        baton = raw(PREFIX + 'final/hand-off-baton.md')
        index = read(PREFIX + 'final/baton-module-index.json')
        require(10000 <= len(baton.decode().split()) <= 100000 and len(index['modules']) == 13, 'E_BATON_SIZE')
        require(sha(baton) == index['baton_sha256'] and baton.decode().rstrip().endswith('EOF ROWAN ASH v689-v5 BATON.'), 'E_BATON_BINDING')
        require(all(sha(raw(row['path'])) == row['sha256'] for row in index['modules']), 'E_MODULE_FIXITY')
        record('modular_handoff', {'words': len(baton.decode().split()), 'modules': 13, 'eof_present': True})
        qa = read(PREFIX + 'final/overview-qa.json')
        require(qa['pages'] >= 3 and qa['visual_inspection'] == 'passed_all_three_rendered_pages', 'E_OVERVIEW_REVIEW')
        require(sha(raw(PREFIX + 'final/overview.pdf')) == qa['pdf_sha256'] and all(n > 500 for n in qa['page_text_lengths']), 'E_PDF_BINDING')
        record('rendered_overview', {'pages': qa['pages'], 'visual_inspection': qa['visual_inspection'], 'manual_accessibility_reserved': True})

        exact = read(PREFIX + 'final/exact-packet-state.json')
        blocked = read(PREFIX + 'plan/blocked-packets.json')['packets']
        require(len(exact['packets']) == 50 and exact['completed_at_repository_seal'] == 45 and exact['remaining'] == 5, 'E_EXACT_PACKET_STATE')
        require(len(blocked) == 30 and all(p['executed'] is False for p in blocked), 'E_BLOCKED_EXECUTION')
        route = read(PREFIX + 'final/terminal-route-candidate.json')
        require(route['state'] == 'PREPARED_NOT_SENT' and route['successor_exact_title'] == 'Neris Solane' and route['successor_phase'] == 'v689-v6' and route['native_messages_sent'] == 0, 'E_ROUTE_CANDIDATE')
        record('approval_and_route_state', {'exact_packets': 50, 'precommit_completed': 45, 'blocked_unexecuted': 30, 'route': 'PREPARED_NOT_SENT'})

        for session in ['plan', 'x1', 'x2']:
            manifest = read(PREFIX + session + '/manifest.json')
            for name, expected in manifest['entries'].items():
                path = PREFIX + name if session == 'plan' else name
                require(sha(raw(path)) == expected, 'E_FROZEN_SESSION_BYTES')
        record('frozen_lifecycle_manifests', {'planning': PLANNING, 'x1': X1, 'x2': X2, 'source_replays': 0})

        patterns = {'private_task_identifier': r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
                    'private_user_path': r'C:[/\\]Users[/\\]',
                    'private_protocol': r'(?:codex|session|thread)://',
                    'credential_assignment': r'(?i)(?:api_key|access_token|password)\s*[:=]\s*[\"\'][^\"\']{12,}[\"\']'}
        candidates = []
        for path in paths:
            if Path(path).suffix in ['.png', '.pdf']:
                continue
            text = raw(path).decode('utf-8')
            for name, pattern in patterns.items():
                if re.search(pattern, text):
                    candidates.append({'path': path, 'class': name})
        require(not candidates, 'E_PRIVACY_CANDIDATE')
        record('scoped_privacy', {'new_owner_files': len(paths), 'pattern_classes': list(patterns), 'candidates': candidates, 'complete_privacy_claimed': False})

        truth = read(PREFIX + 'final/phase-truth.json')
        require(truth['outcomes'] == OUTCOMES and truth['independent_reproduction'] is False and truth['real_measurements'] == 0 and truth['terminal_verdict'] == 'NOT_READY_FOR_STAGE_20', 'E_CLAIM_BOUNDARY')
        source = read(PREFIX + 'final/source-and-lifecycle.json')
        require(source['source_canonical_credit'] == 0 and source['source_canonical_status'] == 'INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL', 'E_SOURCE_CREDIT')
        record('scientific_and_source_boundaries', {'source_canonical_credit': 0, 'empirical_measurements': 0, 'independent_reproduction': False, 'terminal_verdict': 'NOT_READY_FOR_STAGE_20'})
        require(git(repo, 'rev-parse', 'HEAD').decode().strip() == final and not git(repo, 'status', '--porcelain=v1').strip(), 'E_POST_VALIDATION_STATE')
        record('post_validation_readback', {'head_unchanged': True, 'clean': True, 'source_canonical_replays': 0})
        status = 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL'
        error = None
    except Exception as exception:
        status = 'INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL'
        error = {'type': type(exception).__name__, 'message': str(exception)}
        checks.append({'name': 'stopped_component', 'passed': False, 'details': error})
    receipt = {'schema': 'ghc.family.exact-final-owner-canonical.v1', 'owner': 'Rowan Ash', 'phase': 'v689-v5',
               'final_commit': final, 'source': SOURCE, 'planning': PLANNING, 'x1': X1, 'x2': X2,
               'status': status, 'canonical_invocations': 1, 'canonical_successes': int(error is None),
               'canonical_replays': 0, 'source_canonical_replays': 0, 'checks': checks,
               'checks_passed': sum(c['passed'] for c in checks), 'check_count': len(checks),
               'error': error, 'started_at_utc': started, 'finished_at_utc': datetime.now(timezone.utc).isoformat(),
               'entrypoint_sha256': sha(Path(__file__).read_bytes()), 'independent_reproduction': False,
               'scope': 'Exact owner delta and bound earlier execution receipts; no source validator or passed calculation replay.',
               'terminal_verdict': 'NOT_READY_FOR_STAGE_20'}
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'status': status, 'checks_passed': receipt['checks_passed'], 'check_count': receipt['check_count'], 'receipt': str(args.output)}), flush=True)
    return 0 if error is None else 1


if __name__ == '__main__':
    raise SystemExit(main())
