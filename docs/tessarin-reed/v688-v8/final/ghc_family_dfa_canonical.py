"""Exact-head owner-scoped seal with immutable lifecycle definition views."""
import argparse
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

SOURCE = 'f7f7868561b86f4f0db6423413f626355b57639e'
X1 = '74794341a77eaa2206a7ef198fbd663b689be21f'
X2 = '892a8b67f5f28750740c8483fd924f0122ecd35f'
REL = 'docs/tessarin-reed/v688-v8'
BRANCH = 'codex/GHC-Family/tessarin-reed-v688-v8-full-tools'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def strict(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        json.dump(obj, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write('\n')

def privacy_candidates(path, text, patterns):
    spans = []
    if path.endswith('/final/ghc_family_dfa_canonical.py'):
        lines = text.splitlines(keepends=True)
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'patterns' for t in node.targets) and isinstance(node.value, ast.List):
                for value in node.value.elts:
                    if isinstance(value, ast.Constant) and isinstance(value.value, str) and value.value in patterns:
                        start = sum(len(line) for line in lines[:value.lineno - 1]) + value.col_offset
                        end = sum(len(line) for line in lines[:value.end_lineno - 1]) + value.end_col_offset
                        spans.append((start, end))
    hits, definitions = [], []
    for index, pattern in enumerate(patterns):
        for match in re.finditer(pattern, text):
            row = {'path': path, 'pattern_class_index': index, 'line': text.count('\n', 0, match.start()) + 1}
            if any(start <= match.start() and match.end() <= end for start, end in spans):
                definitions.append(dict(row, classification='scanner_definition'))
            else:
                hits.append(row)
    return hits, definitions

class Seal:
    def __init__(self, args):
        self.args = args
        self.repo = args.repo.resolve()
        self.checks = {}
        self.manifests = []

    def git(self, *args, input=None):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], input=input, timeout=90)

    def check(self, name, value):
        self.checks[name] = bool(value)
        if not value:
            raise ValueError(name)

    def batch(self, revision, paths):
        data = self.git('cat-file', '--batch', input=''.join(revision + ':' + p + '\n' for p in paths).encode())
        result = {}
        offset = 0
        for path in paths:
            end = data.index(b'\n', offset)
            fields = data[offset:end].split()
            if len(fields) != 3 or fields[1] != b'blob':
                raise ValueError('missing or nonblob owner dependency')
            size = int(fields[2])
            result[path] = data[end + 1:end + 1 + size]
            offset = end + size + 2
        self.check('complete_batch_framing', offset == len(data))
        return result

    def equality(self):
        local = self.git('rev-parse', 'HEAD').decode().strip()
        upstream = self.git('rev-parse', '@{upstream}').decode().strip()
        tracking = self.git('rev-parse', 'refs/remotes/origin/' + BRANCH).decode().strip()
        lines = self.git('ls-remote', 'origin', 'refs/heads/' + BRANCH).decode().splitlines()
        live = lines[0].split()[0] if len(lines) == 1 else None
        divergence = [int(n) for n in self.git('rev-list', '--left-right', '--count', 'HEAD...@{upstream}').decode().split()]
        clean = not self.git('status', '--porcelain=v1', '--untracked-files=all').strip()
        return {'local': local, 'upstream': upstream, 'tracking': tracking,
                'fresh_live': live, 'divergence': divergence, 'clean': clean,
                'all_equal': local == upstream == tracking == live == self.args.head}

    def manifest(self, revision, path):
        manifest = strict(self.git('show', revision + ':' + path))
        paths = [r['path'] for r in manifest['entries']]
        self.check('unique_manifest_paths_' + path.split('/')[-2], len(paths) == len(set(paths)))
        blobs = self.batch(revision, paths)
        self.check('manifest_fixity_' + path.split('/')[-2], all(len(blobs[r['path']]) == r['bytes'] and sha(blobs[r['path']]) == r['sha256'] for r in manifest['entries']))
        self.manifests.append({'path': path, 'revision': revision, 'entries': len(paths), 'valid': True})
        return sorted(set(paths + manifest['self_exclusions']))

    def static(self):
        self.check('branch_exact', self.git('branch', '--show-current').decode().strip() == BRANCH)
        before = self.equality()
        self.check('fresh_four_way_equal', before['all_equal'])
        self.check('clean', before['clean'])
        self.check('zero_divergence', before['divergence'] == [0, 0])
        self.check('exact_direct_parent_chain', self.git('show', '-s', '--format=%P', X1).decode().strip() == SOURCE and self.git('show', '-s', '--format=%P', X2).decode().strip() == X1 and self.git('show', '-s', '--format=%P', self.args.head).decode().strip() == X2)
        self.check('three_phase_commits', self.git('rev-list', '--count', SOURCE + '..' + self.args.head).decode().strip() == '3')
        self.check('zero_merges', self.git('rev-list', '--count', '--merges', SOURCE + '..' + self.args.head).decode().strip() == '0')
        changes = [line.split('\t') for line in self.git('diff', '--name-status', SOURCE, self.args.head).decode().splitlines()]
        paths = [row[1] for row in changes]
        self.check('additive_owner_scope', all(row[0] == 'A' and row[1].startswith(REL + '/') and '..' not in PurePosixPath(row[1]).parts for row in changes))
        self.check('owner_file_ceiling', 0 < len(paths) < 2000)
        blobs = self.batch(self.args.head, paths)
        parsed = 0
        python = 0
        privacy = []
        scanner_definitions = []
        security = []
        patterns = [r'(?i)[CD]:[\\/]', r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', r'sk-[a-zA-Z0-9]{20,}', r'BEGIN (?:RSA |EC )?PRIVATE KEY', r'<codex_delegation>']
        maximum = ('', 0)
        for path, data in blobs.items():
            text = data.decode('utf-8')
            words = len(text.split())
            if words > maximum[1]:
                maximum = (path, words)
            if path.endswith('.json'):
                strict(data)
                parsed += 1
            if path.endswith('.py'):
                tree = ast.parse(text)
                python += 1
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ['eval', 'exec']:
                        security.append(path)
                    if isinstance(node, ast.Call) and any(k.arg == 'shell' and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords):
                        security.append(path)
            hits, definitions = privacy_candidates(path, text, patterns)
            privacy.extend(hits)
            scanner_definitions.extend(definitions)
        self.check('document_ceiling', maximum[1] <= 100000)
        self.check('configured_privacy_classes', not privacy)
        self.check('bounded_ast_security', not security)
        scopes = {}
        for stage, revision in [('x1', X1), ('x2', X2), ('final', self.args.head)]:
            scopes[stage] = self.manifest(revision, REL + '/' + stage + '/manifest.json')
        owner = strict(blobs[REL + '/final/owner-manifest.json'])
        self.check('owner_manifest_complete', set(paths) == {r['path'] for r in owner['entries']} | set(owner['self_exclusions']))
        self.check('owner_manifest_fixity', all(len(blobs[r['path']]) == r['bytes'] and sha(blobs[r['path']]) == r['sha256'] for r in owner['entries']))
        self.check('content_seal', strict(blobs[REL + '/final/content-seal.json'])['owner_manifest_sha256'] == sha(blobs[REL + '/final/owner-manifest.json']))
        self.check('stage_scope_complete', set(scopes['x1']) | set(scopes['x2']) | set(scopes['final']) == set(paths))
        def read(name):
            return strict(blobs[REL + '/' + name])
        truth = read('final/phase-truth.json')
        self.check('outcomes', truth['outcomes'] == {'completed': 170, 'represented': 17, 'open_gap': 3, 'exact_gate': 10})
        self.check('retained_method_counts', truth['phase_methods'] == 50 and truth['phase_witnesses'] == 590 and truth['phase_unique_negatives'] == 380 and truth['phase_failed_witnesses'] == 475 and truth['phase_passing_witnesses'] == 115)
        self.check('effective_counts', truth['effective_counts'] == {'proposals': 17030, 'negatives': 85805, 'methods': 94175, 'failed_witnesses': 56778, 'passing_witnesses': 86303, 'open_gaps': 768, 'exact_gates': 795})
        self.check('not_ready_for_stage20', truth['terminal_verdict'] == 'NOT_READY_FOR_STAGE_20')
        self.check('prepared_not_sent', read('final/terminal-route.json')['state'] == 'PREPARED_NOT_SENT' and truth['successor_contacts'] == 0)
        self.check('portfolio_complete', read('x2/portfolio-results.json')['predicate_passes'] == 850 and all(r['predicate_pass'] is True for r in read('x2/portfolio-results.json')['records'] if r['action_executed']))
        self.check('exact_and_blocked_unexecuted', all(not r['action_executed'] for r in read('x2/portfolio-results.json')['records'] if r['group'] in ['exact_packets', 'blocked_packets']))
        self.check('contracts_complete', read('x2/contract-summary.json') == {'contracts': 200, 'passed': 200, 'failed': 0, 'failure_ids': []})
        self.check('method_validation', read('x2/method-flow-validation-v2.json')['valid'] and read('final/method-flow-validation.json')['valid'])
        deck = read('x2/deck/card-manifest.json')
        self.check('deck_manifest_fixity', all(len(blobs[e['path']]) == e['bytes'] and sha(blobs[e['path']]) == e['sha256'] for e in deck['entries']))
        self.check('deck_card_count', read('x2/deck/deck-index.json')['card_count'] == 257)
        self.check('failure_nonerasure', not read('x2/manifest-probe-v1.json')['valid'] and read('x2/manifest-probe-v2.json')['valid'] and not read('x1/method-flow-validation.json')['valid'] and read('x1/method-flow-validation-v2.json')['valid'])
        lock = read('x1/tool-plan.json')['packages']['packages']
        self.check('package_artifacts', all((self.args.package_bank / 'artifacts' / p['filename']).stat().st_size == p['bytes'] and sha((self.args.package_bank / 'artifacts' / p['filename']).read_bytes()) == p['sha256'] for p in lock))
        self.check('package_smokes', read('x2/package-smokes.json')['comparisons'] == 420 and read('x2/package-smokes.json')['all_pass'])
        self.check('advisory_snapshot', len(read('x2/package-transaction.json')['osv_results']['results']) == 7)
        promotion = read('x2/tool-promotion.json')
        self.check('tool_smokes', len(promotion['smokes']) == 190 and all(r['predicate_pass'] for r in promotion['smokes']))
        for row in promotion['parity']:
            if row['tool'].startswith('ghc-family-'):
                target = self.args.skill_root / row['tool'] / row['relative_path']
                source = REL + '/x2/skills/' + row['tool'] + '/' + row['relative_path']
            else:
                target = self.args.runner_root / row['relative_path']
                source = REL + '/x2/code/' + row['relative_path']
            raw = target.read_bytes()
            self.check('promotion_raw_and_git_parity_' + str(len(self.checks)), len(raw) == row['bytes'] and sha(raw) == row['sha256'] and raw.replace(b'\r\n', b'\n') == blobs[source])
        original = read('x1/phase-truth.json')
        source_files = [('canonical-f7f7868561b8/exact-final-owner-scoped-canonical.json', original['source_canonical_sha256']), ('canonical/exact-final-owner-scoped-canonical.json', original['retained_invalid_canonicals'][0]), ('canonical-b105ef20548e/exact-final-owner-scoped-canonical.json', original['retained_invalid_canonicals'][1]), ('canonical/dependency-corrected-x2.json', original['retained_focused_recovery'])]
        self.check('source_receipts_read_only_fixity', all(sha((self.args.source_bank / path).read_bytes()) == digest for path, digest in source_files))
        baton = blobs[REL + '/handoffs/caelen-morrow-v689-v1-activation-baton.md'].decode()
        self.check('baton_budget_and_eof', 10000 <= len(baton.split()) <= 100000 and len(re.findall(r'^## Module ', baton, re.M)) == 13 and baton.rstrip().endswith('EOF TESSARIN REED v688-v8 BATON.'))
        self.check('baton_hash', read('final/baton-index.json')['sha256'] == sha(baton.encode()))
        policy = read('final/canonical-policy.json')
        self.check('canonical_policy', policy['source'] == SOURCE and policy['x1'] == X1 and policy['x2'] == X2 and len(policy['test_modules']) == 4 and policy['expected_total_tests'] == sum(row['expected_tests'] for row in policy['test_modules']))
        return {'before': before, 'paths': paths, 'blobs': blobs, 'scopes': scopes, 'policy': policy, 'scan': {'strict_json': parsed, 'python_ast': python, 'maximum_document': {'path': maximum[0], 'words': maximum[1]}, 'confirmed_privacy_hits': len(privacy), 'adjudicated_scanner_definitions': scanner_definitions, 'bounded_security_findings': security}}

    def run_tests(self, static, output):
        results = []
        definitions = {'x1': X1, 'x2': X2, 'final': self.args.head}
        materialized = {}
        for row in static['policy']['test_modules']:
            stage = row['stage']
            root = output / 'definitions' / stage
            if stage not in materialized:
                paths = static['scopes']['x1'] if stage == 'x1' else sorted(set(static['scopes']['x1'] + static['scopes']['x2'])) if stage == 'x2' else static['paths']
                blobs = self.batch(definitions[stage], paths)
                root.mkdir(parents=True, exist_ok=False)
                for path, data in blobs.items():
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open('xb') as handle:
                        handle.write(data)
                materialized[stage] = len(paths)
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
            cp = subprocess.run([sys.executable, '-X', 'utf8', str(root / row['path'])], cwd=root, env=env, capture_output=True, text=True, timeout=60)
            output_name = row['label'] + '-tests'
            (output / (output_name + '.stdout.txt')).write_text(cp.stdout, encoding='utf-8')
            (output / (output_name + '.stderr.txt')).write_text(cp.stderr, encoding='utf-8')
            match = re.search(r'Ran (\d+) tests?', cp.stdout + cp.stderr)
            count = int(match.group(1)) if match else 0
            results.append({'stage': stage, 'module': row['path'], 'definition': definitions[stage], 'definition_sha256': sha((root / row['path']).read_bytes()), 'materialized_files': materialized[stage], 'tests': count, 'expected_tests': row['expected_tests'], 'returncode': cp.returncode, 'passed': cp.returncode == 0 and count == row['expected_tests']})
        self.checks['all_lifecycle_tests'] = len(results) == len(static['policy']['test_modules']) and all(row['passed'] for row in results)
        return results

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['repo', 'package-bank', 'source-bank', 'skill-root', 'runner-root', 'receipt-root']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--head', required=True)
    parser.add_argument('--mode', choices=['preflight', 'canonical'], required=True)
    args = parser.parse_args()
    if not re.fullmatch('[a-f0-9]{40}', args.head):
        raise ValueError('exact full head required')
    output = args.receipt_root / ('canonical-' + args.head[:12])
    marker = output / 'invocation.json'
    receipt = output / 'exact-final-owner-scoped-canonical.json'
    if marker.exists() or receipt.exists():
        raise ValueError('canonical replay refused')
    seal = Seal(args)
    static = seal.static()
    if args.mode == 'preflight':
        write(output / 'preflight.json', {'schema': 'ghc.family.dfa.canonical-preflight.v1', 'head': args.head, 'checks': seal.checks, 'valid': all(seal.checks.values()), 'test_modules_planned': static['policy']['test_modules'], 'canonical_invocations': 0})
        print(json.dumps({'mode': 'preflight', 'valid': True, 'checks': len(seal.checks), 'owner_files': len(static['paths'])}))
        return 0
    preflight = strict((output / 'preflight.json').read_bytes())
    seal.check('preflight_exact', preflight['head'] == args.head and preflight['valid'])
    write(marker, {'head': args.head, 'invocation_count': 1, 'success_count': 0, 'replay_count': 0})
    tests = []
    error = None
    try:
        tests = seal.run_tests(static, output)
        after = seal.equality()
        seal.check('fresh_four_way_equal_after', after['all_equal'])
        seal.check('clean_after', after['clean'])
        seal.check('zero_divergence_after', after['divergence'] == [0, 0])
    except Exception as exc:
        after = None
        error = {'type': type(exc).__name__, 'message': str(exc).replace(str(args.repo), '<owned-repo>').replace(str(args.receipt_root), '<receipt-bank>')}
    valid = error is None and all(seal.checks.values()) and len(tests) == len(static['policy']['test_modules'])
    result = {'schema': 'ghc.family.dfa.exact-final-owner-scoped-canonical.v1', 'owner': 'Tessarin Reed', 'phase': 'v688-v8', 'source': SOURCE, 'x1': X1, 'evidence': X2, 'head': args.head, 'branch': BRANCH, 'status': 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL' if valid else 'INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL', 'checks': seal.checks, 'check_count': len(seal.checks), 'passed_check_count': sum(seal.checks.values()), 'test_modules': tests, 'test_count': sum(row['tests'] for row in tests), 'canonical_invocation_count': 1, 'canonical_success_count': int(valid), 'canonical_replay_count': 0, 'owner_files': len(static['paths']), 'scan': static['scan'], 'manifests': seal.manifests, 'equality_before': static['before'], 'equality_after': after, 'full_repository_suite_run': False, 'independent_reproduction': False, 'same_owner_shared_infrastructure': True, 'successor_contacts': 0, 'terminal_verdict': 'NOT_READY_FOR_STAGE_20', 'error': error, 'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write(receipt, result)
    print(json.dumps({'status': result['status'], 'checks': len(seal.checks), 'passed': sum(seal.checks.values()), 'tests': result['test_count'], 'receipt_sha256': sha(receipt.read_bytes()), 'error': error}))
    return 0 if valid else 1

if __name__ == '__main__':
    raise SystemExit(main())
