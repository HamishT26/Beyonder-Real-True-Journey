#!/usr/bin/env python3
"""Exact x2 contract checks for Vesper v689-v7-r2."""

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
    from ghc_family_source_ledger_x2 import evaluate

    proposals = json.loads((root / "docs/vesper-arlen/v689-v7-r2/plan/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    selected = [row for row in proposals if row["session"] == "x2"]
    assert len(selected) == 100
    for row in selected:
        request = copy.deepcopy(row["request"])
        assert evaluate(request) == row["expected"], row["proposal_id"]
        assert request == row["request"]
        candidate = copy.deepcopy(row["candidate_request"])
        assert evaluate(candidate) == row["candidate_expected"]
        assert candidate == row["candidate_request"]
    print(json.dumps({"safe": 100, "candidate_refusals": 100, "status": "PASS"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
