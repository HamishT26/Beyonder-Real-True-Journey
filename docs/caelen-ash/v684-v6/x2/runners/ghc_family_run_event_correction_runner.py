#!/usr/bin/env python3
"""Family-current runner for run-event correction quarantine and nonerasure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_caelen_ash_v684_v6_contracts import validate_fixture

PROPOSAL_IDS = ['CA6846-N026', 'CA6846-N027', 'CA6846-N028', 'CA6846-N029', 'CA6846-N030', 'CA6846-N031', 'CA6846-N032', 'CA6846-N033']
BOUNDARY = 'run-event correction quarantine and nonerasure'


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output")
    args = parser.parse_args()
    controls_path = ROOT / "docs" / "caelen-ash" / "v684-v6" / "x2" / "positive-controls.json"
    controls = json.loads(controls_path.read_text(encoding="utf-8"))["entries"]
    selected = [row for row in controls if row["proposal_id"] in PROPOSAL_IDS]
    checks = []
    for row in selected:
        passed, errors = validate_fixture(row["fixture"])
        checks.append({"proposal_id": row["proposal_id"], "passed": passed, "errors": errors})
    result = {
        "schema": "ghc.family.runner-receipt.v2",
        "runner": 'ghc_family_run_event_correction_runner.py',
        "boundary": BOUNDARY,
        "selected": len(selected),
        "checks": checks,
        "passed": len(selected) == len(PROPOSAL_IDS) and all(item["passed"] for item in checks),
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True)
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(payload)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
