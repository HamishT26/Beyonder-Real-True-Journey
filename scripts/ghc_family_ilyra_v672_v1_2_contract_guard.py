from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED = {
    "proposal_id", "title", "hypothesis", "null_or_failure", "approval_class",
    "execution_lane", "current_official_or_primary_source_needs", "concrete_artifacts",
    "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "external_actions",
}


def run_contract_file() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"passed": False, "reason": "one local fixture path is required"}))
        return 2
    try:
        row = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        missing = sorted(REQUIRED - row.keys())
        if missing:
            raise ValueError(f"missing proposal fields: {missing}")
        if row["expected_disposition"] not in ALLOWED_OUTCOMES:
            raise ValueError("unapproved outcome label")
        if row["external_actions"] != 0 or not row["protected_gates"]:
            raise ValueError("protected zero-external-action boundary failed")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"passed": False, "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"passed": True, "proposal_id": row["proposal_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(run_contract_file())
