#!/usr/bin/env python3
"""Exact x1 contract checks for Vesper v689-v7-r2."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    sys.path.insert(0, str(root / "scripts"))
    from ghc_family_source_ledger_x1 import evaluate

    proposals = json.loads((root / "docs/vesper-arlen/v689-v7-r2/plan/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    selected = [row for row in proposals if row["session"] == "x1"]
    assert len(selected) == 100
    safe = candidate = immutable = 0
    for row in selected:
        request = copy.deepcopy(row["request"])
        if evaluate(request) != row["expected"]:
            raise AssertionError(row["proposal_id"])
        safe += 1
        if request != row["request"]:
            raise AssertionError(f"mutated {row['proposal_id']}")
        immutable += 1
        if evaluate(copy.deepcopy(row["candidate_request"])) != row["candidate_expected"]:
            raise AssertionError(f"candidate {row['proposal_id']}")
        candidate += 1
    assert evaluate({"op": "not-real", "payload": {}, "synthetic": True})["error"] == "E_OPERATION"
    assert evaluate({"op": "source_record_shape", "payload": {}, "synthetic": False})["error"] == "E_SYNTHETIC"
    print(json.dumps({"status": "VALID_X1_CONTRACTS", "safe": safe, "candidate_refusals": candidate, "immutable_inputs": immutable, "extra_invariants": 2}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
