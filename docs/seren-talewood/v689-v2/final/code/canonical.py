"""One-shot owner exact-final canonical. The invocation marker is never replayed."""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REL = 'docs/seren-talewood/v689-v2'
SOURCE = 'ac9f049a165005776a2aec4c451e654c3d08013b'
X1 = '5ed797b5674205dc6f9928a804f77d44decc149d'
X2 = 'cbf66513c04b297ed0f3c4a89c4817f9f9122818'
BRANCH = 'codex/GHC-Family/seren-talewood-v689-v2-full-tools'
PATTERNS = {
    'private_absolute_path': re.compile(r'\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b', re.I),
    'raw_uuid': re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', re.I),
    'credential_or_token': re.compile(r'\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"\'][^\"\']+[\"\']', re.I),
    'private_key': re.compile(r'-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----'),
    'private_route_markup': re.compile(r'<(?:codex_delegation|source_thread_id)>|\b(?:app|plugin)://', re.I),
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def constant(_):
        raise ValueError('non-finite JSON constant')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def write_once(path, value):
    with path.open('xb') as handle:
        handle.write(json_bytes(value))


def git(repo, *args, data=None):
    return subprocess.run(['git', '-C', str(repo), *args], input=data, capture_output=True, check=True, timeout=180).stdout


def scalar(repo, *args):
    return git(repo, *args).decode('utf-8').strip()


def exact_state(repo, expected):
    local = scalar(repo, 'rev-parse', 'HEAD')
    upstream = scalar(repo, 'rev-parse', '@{upstream}')
    tracking = scalar(repo, 'rev-parse', 'refs/remotes/origin/' + BRANCH)
    lines = scalar(repo, 'ls-remote', '--exit-code', '--heads', 'origin', 'refs/heads/' + BRANCH).splitlines()
    assert len(lines) == 1
    live, ref = lines[0].split()
    divergence = [int(v) for v in scalar(repo, 'rev-list', '--left-right', '--count', 'HEAD...@{upstream}').split()]
    assert ref == 'refs/heads/' + BRANCH and local == upstream == tracking == live == expected
    assert divergence == [0, 0]
    assert scalar(repo, 'branch', '--show-current') == BRANCH
    assert not scalar(repo, 'status', '--porcelain=v1', '--untracked-files=all')
    return {'local': local, 'upstream': upstream, 'tracking': tracking, 'fresh_live': live,
            'divergence': divergence, 'clean': True, 'all_equal': True, 'recorded_at_utc': datetime.now(timezone.utc).isoformat()}


def owner_blobs(repo, commit):
    rows = git(repo, 'ls-tree', '-r', '-z', commit, '--', REL).split(b'\0')
    index = {}
    for row in rows:
        if not row:
            continue
        left, path = row.decode('utf-8').split('\t', 1)
        mode, kind, oid = left.split()
        assert mode == '100644' and kind == 'blob' and path.startswith(REL + '/')
        index[path] = oid
    names = sorted(index)
    raw = git(repo, 'cat-file', '--batch', data=('\n'.join(index[name] for name in names) + '\n').encode('ascii'))
    offset, output = 0, {}
    for name in names:
        end = raw.index(b'\n', offset)
        oid, kind, length = raw[offset:end].decode('ascii').split()
        offset = end + 1
        length = int(length)
        blob = raw[offset:offset+length]
        offset += length + 1
        assert kind == 'blob' and oid == index[name]
        output[name] = {'oid': oid, 'raw': blob}
    assert offset == len(raw)
    return output


def materialize(directory, blobs):
    directory.mkdir(exist_ok=False)
    for name, blob in blobs.items():
        relative = Path(name).relative_to(REL)
        path = directory / relative
        assert path.resolve().is_relative_to(directory.resolve())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(blob['raw'])


def verify_manifest(manifest, blobs, expected_names):
    entries = manifest['entries']
    assert len(entries) == len({row['path'] for row in entries})
    assert {row['path'] for row in entries} | set(manifest['self_exclusions']) == expected_names
    for row in entries:
        blob = blobs[row['path']]
        assert sha(blob['raw']) == row['sha256'] and len(blob['raw']) == row['bytes'] and blob['oid'] == row['git_oid']


def run(args):
    # The caller performs final pushed-head preflight before this sole invocation.
    # Even a failed invocation retains its marker and cannot be resumed or replayed.
    args.receipt_dir.mkdir(exist_ok=False)
    write_once(args.receipt_dir / 'invocation-marker.json', {'expected_final': args.expected_final,
        'source': SOURCE, 'x1': X1, 'x2': X2, 'invocation': 1, 'started_at_utc': datetime.now(timezone.utc).isoformat()})
    checks = []
    def checked(label, condition, details=None):
        checks.append({'check': label, 'passed': bool(condition), 'details': details})
        if not condition:
            raise AssertionError(label)
    try:
        before = exact_state(args.repo, args.expected_final)
        checked('fresh_pushed_exact_final_before', True, before)
        chain = scalar(args.repo, 'rev-list', '--reverse', SOURCE + '..' + args.expected_final).splitlines()
        checked('exact_three_commit_lifecycle', chain == [X1, X2, args.expected_final], chain)
        for commit, parent in [(X1, SOURCE), (X2, X1), (args.expected_final, X2)]:
            checked('direct_single_parent_' + commit[:12], scalar(args.repo, 'show', '-s', '--format=%P', commit) == parent)
        checked('zero_merge_commits', scalar(args.repo, 'rev-list', '--count', '--merges', SOURCE + '..' + args.expected_final) == '0')
        source_receipt = args.source_receipt.read_bytes()
        checked('source_canonical_receipt_hash', sha(source_receipt) == '2f0f18311c93d165643c2b86944ad9e26537a6d9709d364aa952bb8a787ad8b5')
        gates = [strict_json(args.x1_gate.read_bytes()), strict_json(args.x2_gate.read_bytes())]
        checked('earlier_freeze_gates', all(g['all_equal'] and g['clean'] and g['divergence'] == [0, 0] for g in gates))
        checked('earlier_gate_heads', gates[0]['local'] == X1 and gates[1]['local'] == X2)
        stages = {name: owner_blobs(args.repo, commit) for name, commit in [('x1', X1), ('x2', X2), ('final', args.expected_final)]}
        final = stages['final']
        checked('owner_file_ceiling', len(final) < 2000, len(final))
        delta = scalar(args.repo, 'diff', '--name-status', SOURCE, args.expected_final).splitlines()
        checked('entire_owner_delta_additive', len(delta) == len(final) and all(row.startswith('A\t' + REL + '/') for row in delta)
                and {row[2:] for row in delta} == set(final))
        for label, previous in [('x1', set()), ('x2', set(stages['x1'])), ('final', set(stages['x2']))]:
            blobs = stages[label]
            manifest = strict_json(blobs[REL + '/' + label + '/manifest.json']['raw'])
            verify_manifest(manifest, blobs, set(blobs) - previous)
            checked('complete_' + label + '_git_blob_manifest', True, len(manifest['entries']))
        for name, blob in stages['x1'].items():
            assert stages['x2'][name] == blob and final[name] == blob
        for name, blob in stages['x2'].items():
            assert final[name] == blob
        checked('x1_and_x2_immutable_in_final', True)
        seal = strict_json(final[REL + '/final/content-seal.json']['raw'])
        expected_seal_names = set(final) - {REL + '/final/' + name for name in ['content-seal.json', 'manifest.json', 'staged-review.json']}
        checked('content_seal_complete_paths', {row['path'] for row in seal['entries']} == expected_seal_names)
        checked('content_seal_exact_bytes', all(sha(final[row['path']]['raw']) == row['sha256'] and len(final[row['path']]['raw']) == row['bytes'] for row in seal['entries']))
        json_count = ast_count = 0
        candidates = []
        maximum = {'words': 0}
        for name, blob in final.items():
            path = args.repo / name
            checked_name = Path(name)
            assert path.is_file() and not path.is_symlink() and path.read_bytes() == blob['raw']
            text = blob['raw'].decode('utf-8')
            assert b'\r' not in blob['raw']
            words = len(text.split())
            assert words <= 100000
            if words > maximum['words']:
                maximum = {'path': name, 'words': words}
            if checked_name.suffix == '.json':
                strict_json(blob['raw'])
                json_count += 1
            if checked_name.suffix == '.py':
                ast.parse(text)
                ast_count += 1
            for label, pattern in PATTERNS.items():
                if pattern.search(text):
                    candidates.append({'path': name, 'class': label})
        checked('working_copy_equals_final_blobs', True)
        checked('all_owner_json_strict', True, json_count)
        checked('all_owner_python_ast', True, ast_count)
        checked('document_word_caps', True, maximum)
        checked('five_class_privacy_candidates', candidates == [], {'classes': sorted(PATTERNS), 'candidates': candidates, 'complete_privacy': False})
        policy = strict_json(final[REL + '/final/canonical-policy.json']['raw'])
        checked('canonical_policy_one_invocation', policy['canonical_invocations'] == 1 and not policy['replay_authorized'])
        test_receipts = []
        for stage, blobs in stages.items():
            target = args.receipt_dir / ('materialized-' + stage)
            materialize(target, blobs)
            definition = next(row for row in policy['test_stages'] if row['stage'] == stage)
            folder = target / stage
            for module in definition['modules']:
                path = target / module['relative_path']
                assert sha(path.read_bytes()) == module['sha256']
                names = sorted(n.name for n in ast.walk(ast.parse(path.read_text())) if isinstance(n, ast.FunctionDef) and n.name.startswith('test_'))
                assert names == module['test_names']
            env = os.environ.copy()
            env['PYTHONDONTWRITEBYTECODE'] = '1'
            scratch = args.receipt_dir / ('scratch-' + stage)
            scratch.mkdir(exist_ok=False)
            env.update(TMP=str(scratch.resolve()), TEMP=str(scratch.resolve()))
            test = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-m', 'unittest', 'discover', '-s', str(folder), '-p', 'test_*.py', '-v'],
                                  capture_output=True, text=True, encoding='utf-8', env=env, timeout=120)
            output = test.stdout + test.stderr
            (args.receipt_dir / ('tests-' + stage + '.log')).write_text(output, encoding='utf-8')
            found = re.search(r'Ran (\d+) tests? in ', output)
            count = int(found.group(1)) if found else -1
            checked('complete_' + stage + '_stage_tests', test.returncode == 0 and count == definition['test_count'],
                    {'tests': count, 'exit_code': test.returncode, 'immutable_stage': stage})
            test_receipts.append({'stage': stage, 'tests': count, 'exit_code': test.returncode})
        materialized = args.receipt_dir / 'materialized-final'
        package_review = strict_json(final[REL + '/x2/packages/review.json']['raw'])
        expected_packages = {p['name'].lower(): p['version'] for p in package_review['packages']}
        installed = {d.metadata['Name'].lower(): d.version for d in importlib.metadata.distributions(path=[str(args.package_site)])}
        checked('isolated_package_closure_exactly_three', installed == expected_packages and len(installed) == 3)
        wheel_files = 0
        for package in package_review['packages']:
            artifact = package['artifact']
            wheel = args.package_artifacts / artifact['filename']
            checked('wheel_hash_' + package['name'], sha(wheel.read_bytes()) == artifact['digests']['sha256'])
            with zipfile.ZipFile(wheel) as archive:
                for info in archive.infolist():
                    if info.is_dir():
                        continue
                    if info.filename.endswith('.dist-info/RECORD'):
                        # pip rewrites this installation index; the original remains
                        # bound by the wheel hash and the installed index is bound below.
                        continue
                    target = args.package_site / info.filename
                    assert target.resolve().is_relative_to(args.package_site.resolve())
                    assert target.is_file() and target.read_bytes() == archive.read(info.filename)
                    wheel_files += 1
        checked('installed_wheel_payload_parity', True, wheel_files)
        layout = strict_json(final[REL + '/final/package-installation-layout.json']['raw'])
        site_files = {path.relative_to(args.package_site).as_posix(): path for path in args.package_site.rglob('*') if path.is_file()}
        checked('complete_installed_package_file_set', set(site_files) == {row['path'] for row in layout['files']})
        checked('installed_metadata_and_launcher_hashes', all(not site_files[row['path']].is_symlink()
                and sha(site_files[row['path']].read_bytes()) == row['sha256']
                and site_files[row['path']].stat().st_size == row['bytes'] for row in layout['files']))
        result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(materialized / 'x2/code/package_smoke.py'),
                                '--site', str(args.package_site), '--out', str(args.receipt_dir / 'package-smoke.json')],
                               capture_output=True, text=True, encoding='utf-8', timeout=60)
        (args.receipt_dir / 'package-smoke.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        checked('package_smoke_fresh', result.returncode == 0)
        checked('package_smoke_frozen_equality', strict_json((args.receipt_dir / 'package-smoke.json').read_bytes()) == strict_json(final[REL + '/x2/packages/smoke.json']['raw']))
        promotion = strict_json(final[REL + '/x2/tool-promotion.json']['raw'])
        for entry in promotion['parity']:
            if entry['kind'] == 'skill':
                path = args.skills_root / entry['name'] / entry['relative_file']
            else:
                path = args.global_tools / entry['name']
            assert path.is_file() and sha(path.read_bytes()) == entry['sha256'] and path.stat().st_size == entry['bytes']
        checked('all_promoted_tool_bytes_equal', True, len(promotion['parity']))
        for tool in policy['support_tools']:
            path = args.skills_root / tool['relative_path']
            checked('support_definition_' + tool['label'], sha(path.read_bytes()) == tool['sha256'])
        phase = strict_json(final[REL + '/final/phase-truth.json']['raw'])
        checked('held_terminal_policy', phase['successor_contacts'] == 0 and not phase['successor_activation_authorized']
                and phase['terminal_after_valid_canonical'] == 'CLOSED_OWNER_SCOPE_HELD_FOR_HAMISH'
                and phase['terminal_verdict'] == 'NOT_READY_FOR_STAGE_20')
        checked('no_source_canonical_or_source_tests_executed', True, {'source_receipt_read_only': True, 'source_modules_executed': 0})
        after = exact_state(args.repo, args.expected_final)
        checked('fresh_pushed_exact_final_after', True, after)
        receipt = {'schema': 'ghc.family.exact-final-owner-scoped-canonical.v1', 'status': 'VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',
                   'owner': 'Seren Talewood', 'phase': 'v689-v2', 'source': SOURCE, 'x1': X1, 'x2': X2, 'final': args.expected_final,
                   'canonical_invocations': 1, 'canonical_successes': 1, 'replays': 0,
                   'source_canonical_replayed': False, 'checks': checks, 'check_count': len(checks),
                   'test_stages': test_receipts, 'tests_passed': sum(row['tests'] for row in test_receipts),
                   'owner_files': len(final), 'strict_json': json_count, 'python_ast': ast_count,
                   'count_reconciliation': strict_json(final[REL + '/final/count-reconciliation.json']['raw']),
                   'before': before, 'after': after, 'independent_reproduction': False,
                   'terminal_status': 'CLOSED_OWNER_SCOPE_HELD_FOR_HAMISH', 'successor_contacts': 0,
                   'terminal_verdict': 'NOT_READY_FOR_STAGE_20', 'completed_at_utc': datetime.now(timezone.utc).isoformat()}
        write_once(args.receipt_dir / 'exact-final-owner-scoped-canonical.json', receipt)
        write_once(args.receipt_dir / 'success-marker.json', {'final': args.expected_final, 'canonical_successes': 1, 'replay_authorized': False})
        print(json.dumps({key: receipt[key] for key in ['status', 'final', 'check_count', 'tests_passed', 'owner_files', 'strict_json', 'python_ast', 'terminal_status', 'successor_contacts']}))
    except Exception as error:
        failure = {'status': 'FAILED_CANONICAL_RETAINED', 'expected_final': args.expected_final,
                   'canonical_invocations': 1, 'canonical_successes': 0, 'replay_authorized': False,
                   'error_type': type(error).__name__, 'checks': checks, 'successor_contacts': 0}
        write_once(args.receipt_dir / 'failure-receipt.json', failure)
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for name in ['repo', 'receipt-dir', 'package-site', 'package-artifacts', 'skills-root', 'global-tools', 'source-receipt', 'x1-gate', 'x2-gate']:
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--expected-final', required=True)
    run(parser.parse_args())
