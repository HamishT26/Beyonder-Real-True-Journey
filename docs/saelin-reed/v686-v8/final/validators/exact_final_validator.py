"""Read-only owner checks with one explicit external canonical invocation latch."""
import sys
sys.dont_write_bytecode = True
import argparse
import ast
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import zipfile
from xml.etree import ElementTree as ET

SOURCE = 'e85af4eea2aed7f98d2dfec936f26a8e175fba44'
X1 = '9012ca9b7d7ed583d09267ebfa0ef271b1087706'
EVIDENCE = '5d32faf68e907086c1d749110e9b0716fe1cfdb7'
PREFIX = 'docs/saelin-reed/v686-v8/'
BRANCH = 'codex/GHC-Family/saelin-reed-v686-v8-full-tools'
PRIVACY = {
    'credential': r'(?:sk-(?:proj-)?[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)',
    'raw_route_identifier': r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b',
    'private_absolute_path': r'(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|/(?:Users|home)/[A-Za-z0-9._-]+)',
    'raw_application_state': r'"(?:providerTabId|clientThreadId|targetThreadId)"\s*:',
    'private_transcript_or_reasoning': r'(?:<analysis>\s*\w|<response_item(?:\s|>)|"role"\s*:\s*"(?:system|assistant|user)"\s*,\s*"content")',
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump_exclusive(path, value):
    raw = (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as stream:
        stream.write(raw)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--final', required=True)
    parser.add_argument('--mode', choices=('preflight', 'canonical'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo, output = args.repo.resolve(), args.output.resolve()
    if output.is_relative_to(repo) or not re.fullmatch('[0-9a-f]{40}', args.final):
        raise ValueError('An exact final and an external receipt path are required')
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError('Receipt already exists; preserve it without replay')
    marker = output.parent / 'saelin-v686-v8-canonical-invocation.json'
    if args.mode == 'canonical':
        dump_exclusive(marker, {'owner': 'Saelin Reed', 'phase': 'v686-v8', 'head': args.final,
                                'invocation_count': 1, 'replay_allowed': False})
    sys.path.insert(0, str(repo / 'scripts'))
    import ghc_family_contract_oracle as C
    import ghc_family_witness_pairing as W
    checks = []
    totals = {}

    def git(*items):
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0')
        return subprocess.check_output(['git', '-C', str(repo), *items], env=env)

    def check(name, passed, detail=None):
        checks.append({'check': name, 'pass': bool(passed), 'detail': detail})
        if not passed:
            raise ValueError('Validation failed: ' + name)

    def equality():
        branch = git('branch', '--show-current').decode().strip()
        heads = [git('rev-parse', ref).decode().strip() for ref in
                 ('HEAD', '@{upstream}', 'refs/remotes/origin/' + BRANCH)]
        remote = git('ls-remote', '--heads', 'origin', 'refs/heads/' + BRANCH).decode().splitlines()
        live = remote[0].split()[0] if len(remote) == 1 else None
        divergence = [int(x) for x in git('rev-list', '--left-right', '--count', 'HEAD...@{upstream}').split()]
        clean = not git('status', '--porcelain=v1', '--untracked-files=all')
        return {'branch': branch, 'local': heads[0], 'upstream': heads[1], 'tracking': heads[2],
                'fresh_live': live, 'divergence': divergence, 'clean': clean,
                'four_way_equal': all(x == args.final for x in heads + [live])}

    result = {'schema': 'ghc.family.saelin-exact-final.v686.v8', 'owner': 'Saelin Reed',
              'phase': 'v686-v8', 'source': SOURCE, 'x1': X1, 'evidence': EVIDENCE,
              'head': args.final, 'mode': args.mode, 'same_owner_only': True,
              'complete_repository_suite': False, 'external_audit': False,
              'independent_reproduction': False, 'canonical_invocation_count': int(args.mode == 'canonical'),
              'canonical_success_count': 0, 'canonical_replay_count': 0,
              'terminal_verdict': 'NOT_READY_FOR_STAGE_20',
              'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        before = equality()
        result['before'] = before
        check('exact_clean_branch_and_fresh_four_way_equality_before', before['branch'] == BRANCH
              and before['clean'] and before['four_way_equal'] and before['divergence'] == [0, 0], before)
        history = [line.split() for line in git('rev-list', '--parents', '--reverse', SOURCE + '..' + args.final).decode().splitlines()]
        check('three_direct_single_parent_commits_zero_merges', history == [[X1, SOURCE], [EVIDENCE, X1], [args.final, EVIDENCE]], {'commits': len(history), 'merges': sum(len(x) > 2 for x in history)})
        delta = [line.split('\t') for line in git('diff', '--name-status', SOURCE, args.final).decode().splitlines()]
        check('all_owner_changes_are_additions', all(len(x) == 2 and x[0] == 'A' for x in delta), len(delta))
        paths = [x[1] for x in delta]
        batch = subprocess.check_output(['git', '-C', str(repo), 'cat-file', '--batch'], input=('\n'.join(args.final + ':' + p for p in paths) + '\n').encode())
        blobs, offset = {}, 0
        for p in paths:
            pos = batch.index(b'\n', offset)
            size = int(batch[offset:pos].split()[2])
            blobs[p] = batch[pos + 1:pos + 1 + size]
            offset = pos + size + 2
        def doc(p):
            return C.strict_loads(blobs[PREFIX + p])
        plan = doc('final/validation-plan.json')
        check('exact_owner_allowlist', all(p.startswith(PREFIX) or p in plan['root_allowlist'] for p in paths), len(paths))
        materialized = [p for p in repo.rglob('*') if p.is_file() and p.name != '.git']
        check('two_thousand_file_ceiling', len(paths) <= 2000 and len(materialized) <= 2000, {'owner': len(paths), 'materialized': len(materialized)})
        check('all_materialized_owner_bytes_equal_git_blobs', all((repo / p).read_bytes() == b for p, b in blobs.items()))
        json_count = 0
        for p, b in blobs.items():
            if p.endswith('.json'):
                C.strict_loads(b)
                json_count += 1
        check('strict_finite_owner_json', True, json_count)
        total_bindings = 0
        boundaries = [('x1/manifest.json', SOURCE, X1), ('x2/manifest.json', X1, EVIDENCE),
                      ('closeout/final-delta-manifest.json', EVIDENCE, args.final),
                      ('closeout/owner-manifest.json', SOURCE, args.final)]
        for name, start, end in boundaries:
            manifest = doc(name)
            entries = manifest['files']
            excludes = manifest['self_excluded']
            excludes = [excludes] if isinstance(excludes, str) else excludes
            wanted = set(git('diff', '--name-only', start, end).decode().splitlines())
            actual = [e['path'] for e in entries]
            check('manifest_path_coverage_' + name, len(actual) == len(set(actual)) and set(actual) | set(excludes) == wanted and not set(actual) & set(excludes))
            bad = [e['path'] for e in entries if e['path'] not in blobs or type(e['bytes']) is not int
                   or len(blobs[e['path']]) != e['bytes'] or sha(blobs[e['path']]) != e['sha256']]
            check('manifest_byte_bindings_' + name, not bad, {'bindings': len(entries), 'failures': bad})
            total_bindings += len(entries)
        for name in ('x2/content-seal.json', 'closeout/content-seal.json'):
            entries = doc(name)['targets']
            bad = [e['path'] for e in entries if e['path'] not in blobs or sha(blobs[e['path']]) != e['sha256'] or len(blobs[e['path']]) != e['bytes']]
            check('content_seal_' + name, not bad, {'targets': len(entries), 'failures': bad})
        check('x1_and_x2_evidence_are_unchanged', not git('diff', '--name-only', X1, args.final, '--', PREFIX + 'x1')
              and not git('diff', '--name-only', EVIDENCE, args.final, '--', PREFIX + 'x2', PREFIX + 'skills', *plan['root_allowlist']))
        definitions, reports = doc('x1/new-proposals.json')['proposals'], doc('x2/contract-results.json')['reports']
        check('two_hundred_exact_contract_reports', len(definitions) == len(reports) == 200
              and all(C.verify_report(d, r, SOURCE, X1) and r['expectation_met'] is True and r['disposition'] == 'completed' for d, r in zip(definitions, reports)))
        inherited = doc('x2/inherited-readback.json')['rows']
        check('two_hundred_inherited_records_zero_new_credit', len(inherited) == 200 and all(r['binding_matches'] is True and r['new_owner_novelty_credit'] == 0 and r['new_owner_execution_credit'] == 0 for r in inherited))
        portfolio = doc('x1/portfolio-plan.json')['rows']
        check('released_portfolio_shape', {k: len(v) for k, v in portfolio.items()} == {'safe': 300, 'candidate': 250, 'clean_fix_refine': 300, 'exact': 50, 'blocked': 30})
        candidates = doc('x2/candidate-results.json')['rows']
        check('candidate_substitutions_retained_at_zero_credit', len(candidates) == 250 and all(r['candidate_accepted'] is False and r['candidate_success_credit'] == 0 for r in candidates))
        cleanup = doc('x2/clean-fix-refine-results.json')['rows']
        check('bounded_integrity_reviews_and_no_source_mutation', len(cleanup) == 300 and all(r['original_unchanged'] is True and r['candidate_success_credit'] == 0 for r in cleanup))
        gates = doc('x2/gate-packets.json')
        check('exact_and_blocked_packets_unexecuted', len(gates['exact']) == 50 and len(gates['blocked']) == 30
              and all(r['executed'] is False for r in gates['exact'] + gates['blocked']))
        flow = doc('x2/method-flow.json')['rows']
        late = doc('final/late-method-flow.json')['rows']
        check('retained_method_flow_and_late_overlay', len(flow) == 551 and len(late) == 2
              and len({r['id'] for r in flow + late}) == 553
              and all(r['initial_success_credit'] == 0 for r in flow + late)
              and all(r['recovery_passed'] is True for r in flow))
        expected_counts = {'effective_negatives': 76295, 'effective_methods': 92777, 'failed_witnesses': 47143,
                           'bounded_passing_witnesses': 74836, 'open_gaps': 663, 'exact_gates': 649, 'declared_proposal_chain': 13830}
        truth = doc('final/phase-truth.json')
        check('evidence_layers_counts_and_protected_verdict', C.same(truth['effective_counts'], expected_counts)
              and C.same(doc('final/evidence-layers.json')['saelin_final'], expected_counts)
              and truth['terminal_verdict'] == 'NOT_READY_FOR_STAGE_20'
              and truth['retained_negative_classes'] == {'observed_owner_operational_failures': 3, 'intentionally_invalid_synthetic_candidates': 550})
        index = doc('handoffs/baton-index.json')
        baton = blobs[index['path']]
        text, lines = baton.decode('utf-8'), baton.decode('utf-8').splitlines()
        check('baton_exact_digest_length_and_eof', sha(baton) == index['sha256'] and len(baton) == index['bytes']
              and len(text.split()) == index['words'] and 10000 <= index['words'] <= 100000
              and len(lines) == index['lines'] and lines[-1] == index['eof'], {'words': index['words'], 'lines': index['lines']})
        check('thirteen_navigable_baton_modules', len(index['modules']) == 13 and all(lines[m['line'] - 1] == f"## {m['number']:02d} {m['title']}" for m in index['modules']))
        check('baton_covers_each_frozen_case', all(text.count('### ' + d['id'] + ' ') == 1 for d in definitions))
        cards = [C.strict_loads(b) for p, b in blobs.items() if p.startswith(PREFIX + 'x2/deck/cards/')]
        byid = {c['card_id']: c for c in cards}
        edges = []
        graph_ok = len(cards) == len(byid) == 208
        for c in cards:
            payload = dict(c)
            ident = payload.pop('card_id')
            graph_ok = graph_ok and ident == 'ghc-card-' + C.sha(payload)[:20] and type(c['tier']) is int
            if c['tier'] == 1:
                graph_ok = graph_ok and c['parent_ids'] == []
            else:
                graph_ok = graph_ok and len(c['parent_ids']) == 1 and c['parent_ids'][0] in byid and byid[c['parent_ids'][0]]['tier'] == c['tier'] - 1
                edges.extend([p, ident] for p in c['parent_ids'])
        check('four_tier_content_addressed_card_graph', graph_ok and len(edges) == 207
              and len(W.acyclic_order({'nodes': list(byid), 'edges': edges})) == 208)
        deck_manifest = doc('x2/deck/card-manifest.json')
        check('complete_deck_manifest', {e['path'] for e in deck_manifest['files']} | {deck_manifest['self_excluded']} == {p for p in paths if p.startswith(PREFIX + 'x2/deck/')}
              and all(sha(blobs[e['path']]) == e['sha256'] and len(blobs[e['path']]) == e['bytes'] for e in deck_manifest['files']))
        privacy_findings, security_findings, ast_count, structural_uuids = [], [], 0, 0
        for p, raw in blobs.items():
            if p.endswith('.pdf'):
                continue
            surfaces = []
            if p.endswith('.docx'):
                from io import BytesIO
                with zipfile.ZipFile(BytesIO(raw)) as z:
                    for member in z.namelist():
                        if member.endswith(('.bin', '.exe', '.dll')):
                            security_findings.append({'path': p, 'member': member, 'reason': 'executable_document_member'})
                        if not member.endswith(('.xml', '.rels')):
                            continue
                        xml = z.read(member).decode()
                        root = ET.fromstring(xml)
                        for element in root.iter():
                            for key, value in element.attrib.items():
                                if re.search(PRIVACY['raw_route_identifier'], value):
                                    permitted = member.startswith('customXml/itemProps') and key == '{http://schemas.openxmlformats.org/officeDocument/2006/customXml}itemID'
                                    check('ooxml_identifier_has_exact_structural_location', permitted)
                                    structural_uuids += 1
                                    xml = xml.replace(value, 'STRUCTURAL_OOXML_IDENTIFIER')
                        surfaces.append((member, xml))
                    metadata = ET.fromstring(z.read('docProps/core.xml'))
                    check('document_author_metadata_empty', all(not element.text for element in metadata if element.tag.endswith(('creator', 'lastModifiedBy'))))
            else:
                text = raw.decode('utf-8')
                surfaces.append((None, text))
                check_lf = b'\r' not in raw
                if not check_lf:
                    privacy_findings.append({'path': p, 'class': 'unexpected_non_LF_text_domain'})
                if p.endswith('.py'):
                    tree = ast.parse(text)
                    ast_count += 1
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ''
                            if name in ('eval', 'exec', 'system') or any(k.arg == 'shell' and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords):
                                security_findings.append({'path': p, 'call': name, 'line': node.lineno})
            for member, surface in surfaces:
                for cls, pattern in PRIVACY.items():
                    if re.search(pattern, surface):
                        privacy_findings.append({'path': p, 'member': member, 'class': cls})
        check('five_class_text_surface_privacy_review', not privacy_findings, privacy_findings)
        check('changed_python_ast_and_bounded_security', not security_findings, {'ast_parses': ast_count, 'findings': security_findings})
        review = doc('final/overview-review.json')
        pdf_review = doc('final/pdf-integrity-review.json')
        check('four_page_reviewed_docx_pdf_and_structural_accessibility', review['pages'] == 4 and review['pages_visually_reviewed'] == [1, 2, 3, 4]
              and review['structural_a11y'] == {'high': 0, 'medium': 0, 'low': 0}
              and sha(blobs[PREFIX + 'final/saelin-reed-v686-v8-evidence-overview.docx']) == review['docx_sha256']
              and sha(blobs[PREFIX + 'final/saelin-reed-v686-v8-evidence-overview.pdf']) == review['pdf_sha256'] == pdf_review['pdf_sha256']
              and pdf_review['pages'] == 4 and pdf_review['author_metadata_empty'] is True and not pdf_review['text_surface_five_class_findings'])
        promotion = doc('x2/skill-promotion-receipt.json')
        global_root = Path(os.environ['SAELIN_GLOBAL_SKILL_ROOT']).resolve()
        invalid_paths, parity_failures = [], []
        for entry in promotion['files']:
            rel = PurePosixPath(entry['path'])
            if rel.is_absolute() or '..' in rel.parts or '\\' in entry['path']:
                invalid_paths.append(entry['path'])
                continue
            path = PREFIX + 'skills/' + entry['skill'] + '/' + entry['path']
            check_value = sha(blobs[path]) == entry['sha256'] and len(blobs[path]) == entry['bytes'] and (global_root / entry['skill'] / entry['path']).read_bytes() == blobs[path]
            if not check_value:
                parity_failures.append(path)
        check('skill_manifest_paths_are_relative', not invalid_paths, invalid_paths)
        check('global_skill_byte_parity', not parity_failures, {'files': len(promotion['files']), 'failures': parity_failures})
        check('ten_promoted_skills_and_five_shared_runners', promotion['skills'] == 10 and promotion['unique_shared_runners'] == 5 and len(promotion['files']) == 120, 120)
        package = doc('x2/package-validation.json')
        check('three_direct_packages_and_eight_pinned_dependencies', package['direct_additions'] == 3 and package['dependency_closure'] == 8
              and all(importlib.metadata.version(p['name']) == p['version'] for p in package['installed_versions'])
              and all(p['positive'] and p['adverse'] for p in package['positive_and_adverse_smokes'])
              and len(package['advisory_audit']['dependencies']) == 8
              and not any(p.get('vulns') for p in package['advisory_audit']['dependencies']))
        check('prepared_route_and_protected_authority', truth['next_owner'] == 'Auren Lark' and truth['next_phase'] == 'v687-v1'
              and truth['delivery_state'] == 'PREPARED_NOT_SENT' and truth['successor_contacted'] is False
              and truth['canonical_invoked_in_repository_snapshot'] is False and len(truth['protected_gates']) == 19)
        if args.mode == 'canonical':
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', SAELIN_TEST_ARTIFACTS=str(output.parent / 'canonical-test-artifacts'))
            test = subprocess.run([sys.executable, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_ghc_family_saelin_v686_v8.py', '-q'], cwd=repo, env=env, capture_output=True, text=True)
            diagnostic = (test.stdout + test.stderr).replace(str(repo), '<owner-repo>').replace(str(output.parent), '<external-receipts>')
            result['tests'] = {'returncode': test.returncode, 'output': diagnostic, 'tests_run': 210, 'same_owner_only': True}
            check('exact_final_owner_tests', test.returncode == 0 and 'Ran 210 tests' in diagnostic and 'OK' in diagnostic, result['tests'])
        after = equality()
        result['after'] = after
        check('exact_clean_branch_and_fresh_four_way_equality_after', after['clean'] and after['branch'] == BRANCH and after['four_way_equal'] and after['divergence'] == [0, 0], after)
        totals = {'owner_files': len(paths), 'strict_json_documents': json_count, 'manifest_bindings': total_bindings,
                  'python_ast_parses': ast_count, 'global_parity_files': 120, 'overview_pages': 4,
                  'baton_words': index['words'], 'baton_lines': index['lines'], 'cards': 208,
                  'owner_tests': 210 if args.mode == 'canonical' else 0, 'structural_ooxml_identifiers': structural_uuids,
                  'confirmed_privacy_findings': 0, 'bounded_security_findings': 0}
        result['status'] = 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' if args.mode == 'canonical' else 'PASS_EXACT_FINAL_PREFLIGHT_NO_CANONICAL_INVOCATION'
        result['canonical_success_count'] = int(args.mode == 'canonical')
        result['effective_counts'] = expected_counts
    except Exception as exc:
        result['status'] = 'FAILED_OWNER_SCOPED_CANONICAL_ZERO_AGGREGATE_CREDIT' if args.mode == 'canonical' else 'FAILED_EXACT_FINAL_PREFLIGHT'
        result['failure_type'] = type(exc).__name__
        result['failure'] = str(exc).replace(str(repo), '<owner-repo>').replace(str(output.parent), '<external-receipts>')
    result['checks'] = checks
    result['counts'] = {**totals, 'checks': len(checks), 'passed': sum(x['pass'] for x in checks)}
    result['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result['validator_git_blob_sha256'] = sha(Path(__file__).read_bytes())
    dump_exclusive(output, result)
    print(json.dumps({'status': result['status'], 'head': args.final, 'counts': result['counts'],
                      'receipt_sha256': sha(output.read_bytes()), 'canonical_invocations': result['canonical_invocation_count'],
                      'canonical_successes': result['canonical_success_count'], 'failure': result.get('failure')}))
    return int(result['canonical_success_count'] != 1 if args.mode == 'canonical' else not result['status'].startswith('PASS_'))


if __name__ == '__main__':
    raise SystemExit(main())
