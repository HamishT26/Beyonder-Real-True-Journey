#!/usr/bin/env python3
"""Family-current bounded source-ledger x2 runner."""
import argparse
import json

from ghc_family_source_ledger_x2 import evaluate

ALLOWED = ['accessible_source_summary', 'gmut_obligation']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json", required=True)
    args = parser.parse_args()
    request = json.loads(args.request_json)
    if request.get("op") not in ALLOWED:
        print(json.dumps({"error":"E_RUNNER_SCOPE","ok":False,"value":None}, sort_keys=True))
        return 2
    result = evaluate(request)
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if result.get("ok") else 2

if __name__ == "__main__":
    raise SystemExit(main())
