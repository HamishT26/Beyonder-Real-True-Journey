#!/usr/bin/env python3
"""Family-current bounded source-ledger runner."""
import argparse
import json

from ghc_family_source_ledger_x1 import evaluate

ALLOWED = ['claim_grade', 'citation_scope']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json", required=True)
    args = parser.parse_args()
    request = json.loads(args.request_json)
    if request.get("op") not in ALLOWED:
        print(json.dumps({"error":"E_RUNNER_SCOPE","ok":False,"value":None}, sort_keys=True))
        return 2
    result = evaluate(request)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0 if result.get("ok") else 2

if __name__ == "__main__":
    raise SystemExit(main())
