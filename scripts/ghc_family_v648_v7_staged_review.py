#!/usr/bin/env python3
"""Exact Git-index review for v648-v7 evidence and closeout packets."""

import argparse, json, re, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def git(*a,binary=False):
    r=subprocess.run(['git',*a],cwd=ROOT,check=True,capture_output=True)
    return r.stdout if binary else r.stdout.decode('utf-8').strip()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--manifest',type=Path,required=True); ap.add_argument('--receipt',type=Path,required=True); ap.add_argument('--stage',required=True); args=ap.parse_args()
    manifest_path=args.manifest if args.manifest.is_absolute() else ROOT/args.manifest
    receipt_path=args.receipt if args.receipt.is_absolute() else ROOT/args.receipt
    manifest=json.loads(manifest_path.read_text(encoding='utf-8')); entries={r['path']:r for r in manifest['entries']}; expected=set(entries)|set(manifest['self_exclusions'])
    staged=set(filter(None,git('diff','--cached','--name-only','--diff-filter=ACMR').splitlines()))
    if staged != expected: raise RuntimeError(f"staged path mismatch missing={sorted(expected-staged)} unexpected={sorted(staged-expected)}")
    patterns={
        'raw_task_or_thread_identifier':re.compile(r'(?i)(source_thread_id|thread_id)\s*[:=]'),
        'private_absolute_local_path':re.compile(r'(?i)[A-Z]:\\Users\\[^\s\"\']+'),
        'credential_or_secret':re.compile(r'(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})'),
        'private_route_or_callable':re.compile(r'(?i)(private_route|callable_identifier|browser_send_submitted_response_active)'),
        'transcript_or_session_stream':re.compile(r'(?i)(session_stream|raw_transcript|conversation_export)'),
    }
    strict=re.compile(r'(?i)(?:api[_-]?key|client_secret|private_key)\s*[:=]\s*[\"\'][^\"\']{6,}[\"\']|bearer\s+[A-Za-z0-9._-]{12,}')
    candidates=[]; confirmed=[]; parsed=0; blob_bad=[]; bytes_bad=[]
    for rel in sorted(staged):
        blob=git('show',f':{rel}',binary=True)
        if rel in entries:
            if git('rev-parse',f':{rel}') != entries[rel]['git_blob']: blob_bad.append(rel)
            p=ROOT/rel
            if not p.is_file() or p.stat().st_size != entries[rel]['bytes']: bytes_bad.append(rel)
        try: text=blob.decode('utf-8')
        except UnicodeDecodeError: continue
        if rel.endswith('.json'): json.loads(text); parsed+=1
        for cls,pat in patterns.items():
            if not pat.search(text): continue
            defined=(rel.startswith('scripts/') and 'v648_v7' in rel) or rel.endswith('-privacy.json') or rel.endswith('canonical-validation.json') or rel.endswith('privacy-scan.json') or (rel.startswith('docs/tamar-vey/v648-v7/method-flow/') and cls=='credential_or_secret' and not strict.search(text))
            row={'path':rel,'pattern_class':cls,'disposition':'definition' if defined else 'confirmed_payload_hit'}; candidates.append(row)
            if not defined: confirmed.append(row)
    subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
    if confirmed or blob_bad or bytes_bad: raise RuntimeError('staged privacy, blob, or checkout-byte mismatch')
    payload=json.loads(receipt_path.read_text(encoding='utf-8')); payload.update({'stage':args.stage,'actual_staged_review':True,'actual_staged_path_count':len(staged),'actual_staged_json_parse_count':parsed,'actual_manifest_entry_count':len(entries),'actual_self_exclusion_count':len(manifest['self_exclusions']),'actual_privacy_pattern_class_count':5,'actual_privacy_candidate_count':len(candidates),'actual_privacy_confirmed_hit_count':0,'actual_blob_mismatch_count':0,'actual_checkout_byte_mismatch_count':0,'actual_diff_hygiene_passed':True,'actual_path_parity_passed':True,'boundary':'Exact Git-index blobs plus current checkout bytes; zero confirmed hits is not complete privacy assurance.'})
    receipt_path.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n'); print(json.dumps({'stage':args.stage,'paths':len(staged),'json':parsed,'privacy_confirmed':0,'blob_mismatches':0},sort_keys=True))
if __name__=='__main__': main()
