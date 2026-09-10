#!/usr/bin/env python3
"""Merged source-faithful runner requiring an explicit module root."""
import argparse
import json
import sys
from pathlib import Path

ALLOWED = ['route_projection', 'rights_reservation', 'accessible_source_summary', 'gmut_obligation']
X1 = ['source_record_shape', 'digest_envelope', 'encoding_observation', 'version_token', 'authority_tier', 'instruction_quarantine', 'claim_grade', 'citation_scope', 'lineage_nonidentity', 'excerpt_window']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--module-root", type=Path, required=True)
    parser.add_argument("--request-json", required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.module_root.resolve()))
    request = json.loads(args.request_json)
    if request.get("op") not in ALLOWED:
        print(json.dumps({"error":"E_RUNNER_SCOPE","ok":False,"value":None}, sort_keys=True))
        return 2
    if request["op"] in X1:
        from ghc_family_source_ledger_x1 import evaluate
    else:
        from ghc_family_source_ledger_x2 import evaluate
    result = evaluate(request)
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result.get("ok") else 2

if __name__ == "__main__":
    raise SystemExit(main())
