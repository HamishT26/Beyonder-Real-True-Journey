#!/usr/bin/env python3
"""Bounded family-current v649-v7 runner: authority_reservation_matrix."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args=parser.parse_args()
    payload=json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    mutation=bool(payload.get("mutation"))
    valid=payload.get("valid") is True and payload.get("bounded") is True and bool(payload.get("protected_gates"))
    accepted=valid and not mutation
    result={"purpose":"authority_reservation_matrix","accepted":accepted,"mutation_rejected":mutation and not accepted,"bounded":True,"external_side_effects":False,"authority_credit":False,"stage20":False}
    print(json.dumps(result,sort_keys=True))
    return 0 if accepted or result["mutation_rejected"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
