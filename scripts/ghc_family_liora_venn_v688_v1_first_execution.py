"""Run the frozen Liora caption contracts once and write an external receipt."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X1 = "421abce86426674b67e0cbd5ce63ad463421fc9f"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_caption_evidence_core import evaluate, exact_type_equal


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    assert subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip() == X1
    proposals = json.loads(
        (ROOT / "docs/liora-venn/v688-v1/x1/new-proposals.json").read_text(encoding="utf-8")
    )["proposals"]
    rows = []
    for proposal in proposals:
        payload = copy.deepcopy(proposal["input"])
        before = copy.deepcopy(payload)
        observed = evaluate(payload)
        unchanged = exact_type_equal(payload, before)
        passed = exact_type_equal(observed, proposal["expected_output"]) and unchanged
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "definition_sha256": hashlib.sha256(canonical(proposal)).hexdigest(),
                "input_sha256": hashlib.sha256(canonical(proposal["input"])).hexdigest(),
                "actual_output": observed,
                "complete_match": exact_type_equal(observed, proposal["expected_output"]),
                "input_unchanged": unchanged,
                "pass": passed,
            }
        )
    assert all(row["pass"] for row in rows)
    receipt = {
        "schema": "ghc.family.owner-first-execution.v1",
        "owner": "Liora Venn",
        "phase": "v688-v1",
        "x1": X1,
        "core_sha256": hashlib.sha256((ROOT / "scripts/ghc_family_caption_evidence_core.py").read_bytes()).hexdigest(),
        "rows": rows,
        "passed": len(rows),
        "failed": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "real_rows": 0,
        "external_actions": 0,
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"state": "FIRST_EXECUTION_PASS", "passed": len(rows), "failed": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
