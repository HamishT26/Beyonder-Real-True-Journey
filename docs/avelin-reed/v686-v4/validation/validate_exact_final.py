"""Exact-owner preflight and exclusive one-shot canonical validation."""
import argparse
import ast
from collections import Counter
import copy
import datetime
import hashlib
import importlib.metadata
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

sys.dont_write_bytecode = True
SOURCE = 'c5cdc995c99bca100f5a63a4f3f23e932d9433a5'
X1 = '5fbfddafacbfdae773777a7e7591b473797491a5'
PREFIX = 'docs/avelin-reed/v686-v4/'
BRANCH = 'codex/GHC-Family/avelin-reed-v686-v4-full-tools'
DOMAIN = 'normalized-LF Git blob bytes'


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(compact(value)).hexdigest()


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate_member')
        result[key] = value
    return result


def strict_json(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=strict_pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))


def git(repo, *args, binary=False, input_data=None):
    result = subprocess.check_output(['git', '-C', str(repo), *args], input=input_data)
    return result if binary else result.decode('utf-8').strip()


def blobs(repo, revision, paths):
    raw = git(repo, 'cat-file', '--batch', binary=True, input_data=('\n'.join(revision + ':' + path for path in paths) + '\n').encode())
    position = 0
    result = {}
    for path in paths:
        end = raw.index(b'\n', position)
        header = raw[position:end].split()
        if len(header) != 3 or header[1] != b'blob':
            raise ValueError('missing_blob:' + path)
        length = int(header[2])
        position = end + 1
        result[path] = raw[position:position + length]
        position += length + 1
    if position != len(raw):
        raise ValueError('batch_remainder')
    return result


def equality(repo):
    head = git(repo, 'rev-parse', 'HEAD')
    heads = [head, git(repo, 'rev-parse', '@{upstream}'), git(repo, 'rev-parse', 'refs/remotes/origin/' + BRANCH),
             git(repo, 'ls-remote', '--exit-code', 'origin', 'refs/heads/' + BRANCH).split()[0]]
    return {'local_upstream_tracking_fresh_live': heads, 'clean': git(repo, 'status', '--porcelain=v1') == '',
            'divergence': [int(x) for x in git(repo, 'rev-list', '--left-right', '--count', 'HEAD...@{upstream}').split()],
            'branch_matches': git(repo, 'branch', '--show-current') == BRANCH}


def collect_tests(repo):
    path = repo / PREFIX / 'tests/test_ghc_family_temporal_records.py'
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    def flatten(item):
        if isinstance(item, unittest.TestSuite):
            return [identifier for child in item for identifier in flatten(child)]
        return [item.id()]
    return suite, sorted(flatten(suite))


def manifest_check(manifest, available, expected):
    rows = manifest['entries']
    if manifest['domain'] != DOMAIN or manifest['entry_count'] != len(rows):
        return False
    if len({row['path'] for row in rows}) != len(rows) or {row['path'] for row in rows} != set(expected):
        return False
    return all(row['path'] in available and len(available[row['path']]) == row['bytes'] and hashlib.sha256(available[row['path']]).hexdigest() == row['sha256'] for row in rows)


def validate(args):
    repo = args.repo.resolve()
    head = git(repo, 'rev-parse', args.head)
    checks = []
    def check(name, condition, detail=None):
        row = {'check': name, 'pass': bool(condition)}
        if detail is not None:
            row['detail'] = detail
        checks.append(row)
        if not condition:
            raise ValueError('check_failed:' + name)
    diff = git(repo, 'diff', '--name-status', SOURCE, head).splitlines()
    paths = [line.split('\t')[-1] for line in diff]
    check('additive_exact_owner_delta', bool(paths) and all(line.startswith('A\t' + PREFIX) for line in diff) and len(paths) < 2000)
    available = blobs(repo, head, paths)
    parsed = {}
    def data(relative):
        path = PREFIX + relative
        if path not in parsed:
            parsed[path] = strict_json(available[path])
        return parsed[path]
    check('materialized_owner_file_ceiling', len([p for p in (repo / PREFIX).rglob('*') if p.is_file()]) < 2000)
    check('checkout_matches_exact_git_blobs', all((repo / p).read_bytes().replace(b'\r\n', b'\n') == b if not p.endswith('.pdf') else (repo / p).read_bytes() == b for p, b in available.items()))
    policy = data('final/validation-policy.json')
    malformed = set(policy['intentionally_malformed_json_fixtures'])
    ordinary_json = [p for p in paths if p.endswith('.json') and p not in malformed]
    for p in ordinary_json:
        parsed[p] = strict_json(available[p])
    check('all_declared_ordinary_json_strictly_parses', True, len(ordinary_json))
    rejected = 0
    for p in malformed:
        try:
            strict_json(available[p])
        except ValueError as exc:
            if str(exc) == 'duplicate_member':
                rejected += 1
    check('all_declared_duplicate_member_fixtures_refused', rejected == len(malformed) == 15)
    python_paths = [p for p in paths if p.endswith('.py')]
    for p in python_paths:
        ast.parse(available[p].decode('utf-8'), filename=p)
    check('all_changed_python_ast_parses', True, len(python_paths))
    check('x1_direct_source_parent', git(repo, 'rev-parse', X1 + '^') == SOURCE)
    x1_paths = git(repo, 'diff', '--name-only', SOURCE, X1).splitlines()
    x1_blobs = blobs(repo, X1, x1_paths)
    check('immutable_x1', all(available[p] == b for p, b in x1_blobs.items()))
    x1_manifest = data('x1/manifest.json')
    check('x1_manifest_replay', manifest_check(x1_manifest, available, set(x1_paths) - {PREFIX + 'x1/manifest.json'}))
    eq = data('x2/x1-equality.json')
    check('preimplementation_x1_four_way_equality', eq['clean'] is True and eq['divergence'] == [0, 0] and eq['local_upstream_tracking_fresh_live'] == [X1] * 4 and eq['implementation_started_before_check'] is False)
    evidence = policy['evidence_commit']
    check('three_direct_single_parent_commits', git(repo, 'rev-parse', evidence + '^') == X1 and git(repo, 'rev-parse', head + '^') == evidence and git(repo, 'rev-list', '--count', SOURCE + '..' + head) == '3' and git(repo, 'rev-list', '--merges', SOURCE + '..' + head) == '')
    evidence_paths = git(repo, 'diff', '--name-only', SOURCE, evidence).splitlines()
    evidence_blobs = blobs(repo, evidence, evidence_paths)
    check('immutable_evidence_layer', all(available[p] == b for p, b in evidence_blobs.items()))
    ev_manifest_path = PREFIX + 'validation/evidence-manifest.json'
    check('evidence_manifest_replay', manifest_check(data('validation/evidence-manifest.json'), available, set(evidence_paths) - {ev_manifest_path}))
    seal_path = PREFIX + 'final/content-seal.json'
    final_manifest_path = PREFIX + 'final/final-manifest.json'
    check('final_content_seal_replay', manifest_check(data('final/content-seal.json'), available, set(paths) - {seal_path, final_manifest_path}))
    check('final_manifest_replay', manifest_check(data('final/final-manifest.json'), available, set(paths) - {final_manifest_path}))

    proposals = data('x1/new-proposals.json')['proposals']
    selection = data('x1/inherited-selection.json')
    check('proposal_count_and_inherited_zero_credit', len(proposals) == 200 and len(selection['selections']) == 200 and all(row['novelty_credit'] == row['execution_credit'] == 0 for row in selection['selections']))
    check('frozen_contract_definition_hashes', all(digest({k: v for k, v in p.items() if k != 'definition_sha256'}) == p['definition_sha256'] for p in proposals))
    novelty = data('x1/novelty-audit.json')
    check('source_bounded_novelty_and_unique_cases', novelty['comparison_pairs'] == 40000 and novelty['quarantine_count'] == 0 and len({(p['family'], digest(p['input'])) for p in proposals}) == 200)
    sys.path.insert(0, str(repo / PREFIX / 'x2'))
    import execute_contracts as lab
    observed = data('x2/contract-results.json')['rows']
    def recompute(proposal, row):
        original = copy.deepcopy(proposal['input'])
        actual = lab.MODULES[proposal['runner']].run(proposal['family'], original)
        return (lab.canonical(original) == lab.canonical(proposal['input'])
                and lab.canonical(actual) == lab.canonical(proposal['expected_result']) == lab.canonical(row['actual']) == lab.canonical(row['expected'])
                and row['input_unchanged'] is True and row['oracle_matched'] is True and row['report_valid'] is True
                and lab.validate_report(proposal, row['report']))
    check('frozen_oracle_and_observed_report_recomputation', len(observed) == 200 and all(recompute(p, r) for p, r in zip(proposals, observed)))
    outcomes = Counter(r['outcome'] for r in observed)
    check('exact_four_outcome_distribution', outcomes == {'completed': 170, 'represented': 10, 'open_gap': 10, 'exact_gate': 10})
    by_id = {p['proposal_id']: p for p in proposals}
    adverse = data('x2/retained-adverse-records.json')['rows']
    check('all_1550_retained_adverse_contracts_reject', len(adverse) == 1550 and len({r['negative_id'] for r in adverse}) == 1550 and all(r['invalid_accepted'] is False and r['bounded_recovery_passed'] is True and not lab.validate_report(by_id[r['proposal_id']], r['invalid_report']) for r in adverse))
    mutation = data('x2/registered-mutations.json')
    check('all_registered_mutation_slots_retained', mutation['count'] == 1000 and Counter((r['proposal_id'], r['kind']) for r in mutation['rows']) == Counter((p['proposal_id'], kind) for p in proposals for kind in p['preregistered_mutations']))
    portfolio = data('x2/portfolio-results.json')
    check('released_portfolio_executions_and_unexecuted_packets', len(portfolio['safe_tasks']) == 300 and all(r['pass'] for r in portfolio['safe_tasks']) and len(portfolio['candidate_tasks']) == 250 and all(r['pass'] for r in portfolio['candidate_tasks']) and len(portfolio['clean_fix_refine']) == 300 and all(r['initial_pass'] is False and r['corrected_pass'] is True for r in portfolio['clean_fix_refine']) and len(portfolio['exact_packets']) == 50 and len(portfolio['blocked_packets']) == 30 and all(r['executed'] is False for r in portfolio['exact_packets'] + portfolio['blocked_packets']))
    method = data('x2/method-flow.json')
    check('method_flow_retention_and_recovery_pairs', method['counts']['methods'] == 1580 and len(method['methods']) == 1580 and Counter(w['result'] for w in method['witnesses']) == {'fail': 1580, 'pass': 1580} and all(w['same_owner_only'] is True and w['independent_reproduction'] is False for w in method['witnesses']) and data('x2/method-flow-validation.json')['valid'] is True)
    counts = data('x2/effective-counts.json')
    check('effective_count_arithmetic', all(counts['effective'][key] == counts['baseline'][key] + 1580 for key in ['effective_negatives','effective_methods','failed_witnesses','bounded_passing_witnesses']) and counts['effective']['open_gaps'] == 632 and counts['effective']['exact_gates'] == 619 and counts['effective']['declared_proposal_chain'] == 13030)
    address = data('x2/evidence-address-index.json')
    def resolve_pointer(record, pointer):
        for part in pointer.removeprefix('/').split('/') if pointer else []:
            token = part.replace('~1', '/').replace('~0', '~')
            record = record[int(token)] if isinstance(record, list) else record[token]
        return record
    def address_matches(row):
        target = resolve_pointer(parsed[row['path']], row['pointer'])
        return target.get('negative_id', target.get('id')) == row['negative_id']
    check('every_negative_has_an_exact_resolvable_address', len(address['entries']) == 1580 and all(address_matches(row) for row in address['entries']))

    deck = data('x2/flashcards/deck-index.json')
    card_paths = [p for p in paths if p.startswith(PREFIX + 'x2/flashcards/cards/') and p.endswith('.json')]
    cards = [strict_json(available[p]) for p in card_paths]
    card_map = {c['card_id']: c for c in cards}
    check('card_content_ids_and_exact_tier_graph', len(cards) == len(card_map) == deck['card_count'] == 240 and all(c['card_id'] == 'ghc-card-' + digest({k: v for k, v in c.items() if k != 'card_id'}) for c in cards) and all((c['parent_ids'] == []) if c['tier'] == 1 else len(c['parent_ids']) == 1 and c['parent_ids'][0] in card_map and card_map[c['parent_ids'][0]]['tier'] == c['tier'] - 1 for c in cards))
    deck_paths = {p for p in paths if p.startswith(PREFIX + 'x2/flashcards/')}
    check('card_manifest_complete_replay', manifest_check(data('x2/flashcards/card-manifest.json'), available, deck_paths - {PREFIX + 'x2/flashcards/card-manifest.json'}))
    html_text = available[PREFIX + 'x2/flashcards/accessible-report.html'].decode('utf-8')
    check('html_landmarks_headers_and_review_reservation', all(s in html_text for s in ['lang="en-NZ"','<main id="main">','<caption>','scope="col"','scope="row"','Manual browser','Māori-language']) and '<script' not in html_text)
    pdf_blob = available[PREFIX + 'x2/integrated-overview.pdf']
    pdf_sha = hashlib.sha256(pdf_blob).hexdigest()
    visual = data('x2/overview-visual-review.json')
    structure = data('x2/overview-structure.json')
    check('four_page_render_and_visual_review_binding', structure['pages'] == 4 and structure['pdf_sha256'] == visual['pdf_sha256'] == pdf_sha and visual['pages_reviewed'] == [1,2,3,4] and visual['legible'] is True and visual['clipped_content'] is False and visual['rendered_page_hashes'] == [p['sha256'] for p in structure['rendered_pages']])
    pdf_probe = 'import json,sys;from pypdf import PdfReader;p=PdfReader(sys.argv[1]);t="\\n".join(x.extract_text() or "" for x in p.pages);print(json.dumps({"pages":len(p.pages),"macron":"Māori" in t,"replacement":"\\ufffd" in t}))'
    pdf_result = json.loads(subprocess.check_output([str(args.document_python), '-X', 'utf8', '-c', pdf_probe, str(repo / PREFIX / 'x2/integrated-overview.pdf')]))
    check('pdf_text_structure', pdf_result == {'pages': 4, 'macron': True, 'replacement': False})
    baton = available[PREFIX + 'final/lyren-moss-v686-v5-baton.md']
    integrity = data('final/baton-integrity.json')
    check('complete_modular_baton_integrity', 10000 <= len(baton.decode('utf-8').split()) <= 100000 and hashlib.sha256(baton).hexdigest() == integrity['sha256'] and integrity['sections'] == 13 and len(re.findall(r'(?m)^# \d{2} ', baton.decode('utf-8'))) == 13 and all(p['proposal_id'] in baton.decode('utf-8') for p in proposals))

    app_plan = data('x1/package-plan.json')
    expected = sorted((r['name'], r['version']) for r in app_plan['packages']) + [('pip','26.2.1')]
    inventory = sorted((d.metadata['Name'], d.version) for d in importlib.metadata.distributions())
    check('exact_corrected_distribution_inventory', inventory == sorted(expected))
    check('three_direct_packages_and_bounded_smokes', sum(r['direct_addition'] for r in app_plan['packages']) == 3 and len(app_plan['packages']) == 4 and all(r['positive_pass'] and r['adverse_refused'] for r in data('x2/toolchain/package-smokes.json')['rows']) and data('x2/toolchain/advisory-audit-r2.json')['known_advisory_records'] == 0 and data('x2/toolchain/advisory-audit-r1.json')['known_advisory_count'] == 12)
    for row in app_plan['packages'] + [data('x2/toolchain/bootstrap-correction-plan.json')]:
        check('wheel_hash_' + row['name'], hashlib.sha256((args.wheelhouse / row['wheel']).read_bytes()).hexdigest() == row['sha256'])
    promotion = data('tooling/global-promotion.json')
    parity = True
    for skill in promotion['skills']:
        global_root = args.skill_root / skill['skill']
        local_root = repo / PREFIX / 'skills' / skill['skill']
        actual = {p.relative_to(global_root).as_posix() for p in global_root.rglob('*') if p.is_file()}
        parity = parity and actual == {r['relative_path'] for r in skill['bindings']}
        for row in skill['bindings']:
            content = (global_root / row['relative_path']).read_bytes()
            parity = parity and content == (local_root / row['relative_path']).read_bytes() and hashlib.sha256(content).hexdigest() == row['sha256']
            parity = parity and content.replace(b'\r\n', b'\n') == available[PREFIX + 'skills/' + skill['skill'] + '/' + row['relative_path']]
    check('ten_additive_global_skills_exact_byte_parity', parity and promotion['skill_count'] == 10 and promotion['total_copied_files'] == 90)
    runner_smokes = data('tooling/runner-smoke-summary.json')
    check('five_unique_portable_runner_sources', len(runner_smokes) == 5 and all(r['positive_pass'] and r['adverse_refused'] and r['source_sha256'] == hashlib.sha256(available[PREFIX + 'runners/' + r['runner']]).hexdigest() for r in runner_smokes) and all(r['positive_pass'] and r['adverse_refused'] for r in data('tooling/skill-smoke-summary.json')) and all(available[PREFIX + 'skills/' + skill['skill'] + '/scripts/' + row['runner']] == available[PREFIX + 'runners/' + row['runner']] for skill in promotion['skills'] for row in runner_smokes))
    check('catalogue_scope_and_retained_post_promotion_timing', data('tooling/meta-tool-box/validation.json')['valid'] is True and data('tooling/meta-tool-box/catalogue.json')['card_count'] == 15 and data('tooling/meta-tool-box/runner-query.json')['result_count'] == 5 and data('tooling/meta-tool-box/promotion-post-audit.json')['prepromotion_meta_command_claimed'] is False and data('tooling/meta-tool-box/overlap-review.json')['family_sets_are_disjoint_between_skills'] is True)

    patterns = {
        'raw_identifiers': r'(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b',
        'private_local_paths': r'(?<![A-Za-z])\b[A-Za-z]:[\\/][A-Za-z0-9]|/(?:Users|home)/[A-Za-z0-9]',
        'credentials': r'\b(?:sk-[A-Za-z0-9]{24,}|ghp_[A-Za-z0-9]{24,})\b',
        'private_transcripts': r'(?m)^\s*(?:<codex_delegation>|"session_meta"\s*:)',
        'private_app_state': r'"(?:clientThreadId|providerTabId|private_callable_id)"\s*:',
    }
    findings = []
    for path, content in available.items():
        if path.endswith('.pdf'):
            continue
        text = content.decode('utf-8')
        for kind, pattern in patterns.items():
            if re.search(pattern, text):
                findings.append({'path': path, 'class': kind})
    check('bounded_five_class_privacy', not findings, findings)
    forbidden = {'eval','exec','compile','__import__'}
    unsafe_imports = {'subprocess','socket','urllib','requests','os','shutil'}
    security = []
    for path in paths:
        if not path.startswith(PREFIX + 'runners/') or not path.endswith('.py'):
            continue
        for node in ast.walk(ast.parse(available[path].decode('utf-8'))):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden:
                security.append(path + ':dynamic_execution')
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [x.name.split('.')[0] for x in node.names] if isinstance(node, ast.Import) else [(node.module or '').split('.')[0]]
                if unsafe_imports.intersection(names):
                    security.append(path + ':external_or_process_surface')
    check('bounded_runner_execution_security', not security, security)
    helper_review = data('validation/helper-security-review.json')
    helper_paths = {p for p in python_paths if '/skills/' not in p and '/runners/' not in p and '/tests/' not in p}
    check('helper_security_review_binding', helper_review['reviewed_owner_helpers_only'] is True and helper_review['unresolved_findings'] == 0 and {r['path'] for r in helper_review['files']} == helper_paths and all(hashlib.sha256(available[row['path']]).hexdigest() == row['sha256'] for row in helper_review['files']))
    suite, identifiers = collect_tests(repo)
    definition = data('validation/test-definition-manifest.json')
    module_path = PREFIX + 'tests/test_ghc_family_temporal_records.py'
    check('exact_selected_test_inventory', identifiers == definition['test_identifiers'] and len(identifiers) == 51 and hashlib.sha256(available[module_path]).hexdigest() == definition['module_sha256'])
    check('test_definition_hash_binding', digest({'module_sha256': definition['module_sha256'], 'test_identifiers': identifiers, 'proposal_definition_hashes': [p['definition_sha256'] for p in proposals]}) == definition['definition_sha256'])
    test_result = {'tests_run': 0, 'execution_deferred_to_canonical': args.mode == 'preflight'}
    if args.mode == 'canonical':
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
        test_result = {'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'test_identifiers': identifiers}
        check('selected_owner_tests', result.wasSuccessful() and result.testsRun == 51)
    check('protected_boundary_and_unsent_repository_state', data('final/phase-truth.json')['terminal_verdict'] == 'NOT_READY_FOR_STAGE_20' and data('final/delivery-state.json')['state'] == 'PREPARED_NOT_SENT' and data('final/delivery-state.json')['send_count'] == 0)
    return {'schema': 'ghc.family.avelin-exact-final.v686.v4', 'owner': 'Avelin Reed', 'phase': 'v686-v4', 'source': SOURCE,
            'x1': X1, 'evidence': evidence, 'head': head, 'checks': checks, 'tests': test_result,
            'counts': {'owner_files': len(paths), 'strict_json_documents': len(ordinary_json), 'intentional_malformed_json_fixtures': len(malformed),
                       'changed_python_ast': len(python_paths), 'detailed_checks': len(checks), 'passed_checks': sum(c['pass'] for c in checks),
                       'manifest_bindings': len(x1_manifest['entries']) + len(data('validation/evidence-manifest.json')['entries']) + len(data('final/content-seal.json')['entries']) + len(data('final/final-manifest.json')['entries']) + len(data('x2/flashcards/card-manifest.json')['entries']),
                       'cards': len(cards), 'baton_words': len(baton.decode('utf-8').split()), 'pdf_pages': 4, 'confirmed_privacy_hits': len(findings), 'bounded_runner_security_findings': len(security)},
            'same_owner_only': True, 'independent_reproduction': False, 'complete_repository_suite': False,
            'terminal_verdict': 'NOT_READY_FOR_STAGE_20'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--head', required=True)
    parser.add_argument('--mode', choices=['preflight','canonical'], required=True)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--skill-root', required=True, type=Path)
    parser.add_argument('--wheelhouse', required=True, type=Path)
    parser.add_argument('--document-python', required=True, type=Path)
    args = parser.parse_args()
    if args.output.resolve().is_relative_to(args.repo.resolve()):
        raise SystemExit('Receipt must remain outside the sealed worktree')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise SystemExit('Existing output blocks duplicate invocation')
    before = equality(args.repo)
    if not before['clean'] or before['divergence'] != [0, 0] or not before['branch_matches'] or before['local_upstream_tracking_fresh_live'] != [args.head] * 4:
        raise SystemExit('Exact pushed clean four-way-equal head required')
    if args.mode == 'canonical':
        marker = args.output.parent / 'avelin-reed-v686-v4-canonical.invoked'
        with marker.open('x', encoding='utf-8') as file:
            file.write(json.dumps({'owner': 'Avelin Reed', 'phase': 'v686-v4', 'head': args.head, 'invocations': 1}))
    try:
        result = validate(args)
        after = equality(args.repo)
        if before != after:
            raise ValueError('Post-validation equality changed')
        result.update({'status': 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' if args.mode == 'canonical' else 'VALID_EXACT_FINAL_PREFLIGHT_ONLY',
                       'before': before, 'after': after, 'canonical_invocation_count': int(args.mode == 'canonical'),
                       'canonical_success_count': int(args.mode == 'canonical'), 'canonical_replay_count': 0,
                       'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    except Exception as exc:
        result = {'schema': 'ghc.family.avelin-exact-final.v686.v4', 'status': 'FAILED_' + args.mode.upper(), 'head': args.head,
                  'exception_type': type(exc).__name__, 'failure': str(exc) if isinstance(exc, ValueError) else 'Inspect the attributable failing dependency',
                  'canonical_invocation_count': int(args.mode == 'canonical'), 'canonical_success_count': 0,
                  'canonical_replay_count': 0, 'same_owner_only': True}
    result['payload_sha256'] = digest(result)
    with args.output.open('x', encoding='utf-8', newline='\n') as output:
        json.dump(result, output, ensure_ascii=False, indent=2, sort_keys=True)
        output.write('\n')
    print(json.dumps({key: result[key] for key in ['status','head','payload_sha256']} | {'counts': result.get('counts'), 'failure': result.get('failure')}))
    return 0 if result['status'].startswith('VALID_') else 1


if __name__ == '__main__':
    raise SystemExit(main())
