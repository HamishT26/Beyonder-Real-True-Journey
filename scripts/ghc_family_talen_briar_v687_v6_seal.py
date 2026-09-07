"""At most one attributable exact-final owner-scoped canonical invocation."""
import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import ghc_family_talen_briar_v687_v6_validation as v

X1 = '1fd150a6de48f02d847b2c949e388345ee5d3f2f'
EVIDENCE = '42d003be1a62858084c8b38bdccfba629fae23ad'


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def write_new(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as out:
        out.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n')


def run_tests(anchor, pattern, expected_count, scratch):
    paths = v.git('diff', '--name-only', v.SOURCE, anchor).decode().splitlines()
    assert all(v.owned(p) for p in paths)
    refs = [anchor+':'+p for p in paths]
    blobs = v.git_blobs(refs)
    destination = pathlib.Path(tempfile.mkdtemp(prefix='talen-'+pattern.split('_')[-1].split('.')[0]+'-', dir=scratch))
    for name, ref in zip(paths, refs):
        target = destination/name
        assert target.resolve().is_relative_to(destination.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blobs[ref])
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', pattern], cwd=destination,
        capture_output=True, text=True, timeout=60, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1'))
    match = re.search(r'Ran ([0-9]+) tests?', result.stderr)
    assert result.returncode == 0 and match and int(match[1]) == expected_count, 'Immutable owner test selection failed'
    return dict(anchor=anchor, pattern=pattern, selected=expected_count, passed=expected_count, materialized_owner_files=len(paths), independent_reproduction=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--canonical', action='store_true', required=True)
    parser.add_argument('--expected-final', required=True)
    parser.add_argument('--receipt-dir', required=True)
    parser.add_argument('--scratch', required=True)
    parser.add_argument('--skill-root', required=True)
    parser.add_argument('--shared-root', required=True)
    args = parser.parse_args()
    expected = args.expected_final
    assert re.fullmatch(r'[0-9a-f]{40}', expected)
    receipts = pathlib.Path(args.receipt_dir).resolve()
    scratch = pathlib.Path(args.scratch).resolve()
    assert not receipts.is_relative_to(v.REPO) and not scratch.is_relative_to(v.REPO)
    receipts.mkdir(parents=True, exist_ok=True)
    scratch.mkdir(parents=True, exist_ok=True)
    marker = receipts/'canonical-latch.json'
    receipt = receipts/'exact-final-canonical.json'
    assert not marker.exists() and not receipt.exists(), 'Canonical invocation already exists; replay refused'
    remote_before = v.remote(expected)
    started = utc()
    write_new(marker, dict(owner='Talen Briar', phase='v687-v6', expected_head=expected, invocation=1, started_at=started))
    try:
        ancestry = [line.split() for line in v.git('rev-list', '--parents', '--reverse', v.SOURCE+'..'+expected).decode().splitlines()]
        assert ancestry == [[X1,v.SOURCE],[EVIDENCE,X1],[expected,EVIDENCE]], 'Exact direct-parent lifecycle mismatch'
        assert int(v.git('rev-list','--count','--merges',v.SOURCE+'..'+expected)) == 0
        changed = v.git('diff','--name-status',v.SOURCE,expected).decode().splitlines()
        assert all(row.startswith('A\t') and v.owned(row[2:]) for row in changed)
        owner_paths = [row[2:] for row in changed]
        assert len(owner_paths) < 2000
        refs = [expected+':'+p for p in owner_paths]
        blobs = v.git_blobs(refs)
        items = {p:v.norm(blobs[ref]) for p,ref in zip(owner_paths,refs)}
        strict = 0
        for path, raw in items.items():
            assert len(raw.decode('utf-8').split()) <= 100000
            if path.endswith('.json'):
                v.parse(raw)
                strict += 1
        manifests = []
        for anchor, name in [(X1,'x1-manifest.json'),(EVIDENCE,'x2-manifest.json'),(expected,'final-delta-manifest.json'),(expected,'final-owner-manifest.json')]:
            manifests.append(v.replay(anchor,v.ROOT+'validation/'+name))
        x1_paths = v.git('diff','--name-only',v.SOURCE,X1).decode().splitlines()
        evidence_paths = v.git('diff','--name-only',v.SOURCE,EVIDENCE).decode().splitlines()
        assert not v.git('diff',X1,expected,'--',*x1_paths).strip()
        assert not v.git('diff',EVIDENCE,expected,'--',*evidence_paths).strip()
        privacy = v.scan(items)
        security = v.security(items)
        assert privacy['confirmed'] == 0, 'Confirmed privacy payload'
        assert not security['findings'], 'Bounded changed-code security finding'
        index = v.parse(items[v.ROOT+'handoffs/baton-index.json'])
        baton = items[index['path']]
        assert v.sha(baton)==index['sha256'] and len(baton.split())==index['words']
        assert 10000 <= index['words'] <= 100000 and index['modules']==13
        assert baton.decode().rstrip().endswith(index['eof'])
        tests = [run_tests(X1,'test_ghc_family_talen_briar_v687_v6_x1.py',11,scratch),
                 run_tests(EVIDENCE,'test_ghc_family_talen_briar_v687_v6_x2.py',16,scratch),
                 run_tests(expected,'test_ghc_family_talen_briar_v687_v6_final.py',11,scratch)]
        promotion = v.parse(items[v.ROOT+'x2/promotion-receipt.json'])
        for entry in promotion['members']:
            destination = pathlib.Path(args.skill_root)/entry['skill']/entry['relative'] if entry['kind']=='skill' else pathlib.Path(args.shared_root)/entry['relative']
            assert destination.read_bytes()==items[entry['source']]
            assert v.sha(destination.read_bytes())==entry['sha256']
        remote_after = v.remote(expected)
        result = dict(status='VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL',owner='Talen Briar',phase='v687-v6',source=v.SOURCE,x1=X1,evidence=EVIDENCE,expected_head=expected,started_at=started,completed_at=utc(),canonical_invocation_count=1,canonical_success_count=1,canonical_replay_count=0,owner_files=len(owner_paths),strict_json_documents=strict,manifests=manifests,manifest_bindings=sum(m['entries'] for m in manifests),manifest_self_exclusions=sum(len(m['self_exclusions']) for m in manifests),tests=tests,selected_tests=sum(t['selected'] for t in tests),privacy=privacy,security=security,global_parity_files=len(promotion['members']),baton=index,lifecycle=dict(phase_commits=3,phase_merges=0,final_parents=[EVIDENCE]),remote=remote_after,remote_before=remote_before,method_flow='13 additive compatible projections and one repair ledger; original x1/x2 format failures retained',same_owner_only=True,independent_reproduction=False,full_repository_suite=False,terminal_verdict='NOT_READY_FOR_STAGE_20')
        write_new(receipt,result)
        print(json.dumps(dict(status=result['status'],owner_files=len(owner_paths),strict_json_documents=strict,manifest_bindings=result['manifest_bindings'],selected_tests=result['selected_tests'],privacy_confirmed=privacy['confirmed'],security_findings=len(security['findings']),receipt_sha256=v.sha(receipt.read_bytes()))))
    except Exception as error:
        failure = receipts/'canonical-failure.json'
        write_new(failure,dict(status='FAILED_RETAINED_ZERO_SUCCESS_CREDIT',expected_head=expected,started_at=started,failed_at=utc(),error_class=type(error).__name__,replay=False))
        raise


if __name__ == '__main__':
    main()
