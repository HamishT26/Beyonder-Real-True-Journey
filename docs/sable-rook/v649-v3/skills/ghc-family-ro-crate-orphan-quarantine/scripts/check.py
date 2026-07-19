#!/usr/bin/env python3
"""Accepting and rejecting smoke use for a v649-v3 phase-local skill."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_v649_v3_runtime import accepting_fixture, evaluate, mutation_fixtures
parser = argparse.ArgumentParser()
parser.add_argument("--fixture", choices=("accept", "reject"), required=True)
args = parser.parse_args()
payload = accepting_fixture("V6493-P01") if args.fixture == "accept" else mutation_fixtures("V6493-P01")[0][1]
result = evaluate("V6493-P01", payload)
observed = result["passed"] if args.fixture == "accept" else not result["passed"]
print(json.dumps({"fixture": args.fixture, "expected_guard_observed": observed, "issue_count": result["issue_count"], "boundary": result["boundary"]}, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if observed else 1)
