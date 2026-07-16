#!/usr/bin/env python3
"""Validate the frozen v646-v4 expanded portfolio execution receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    specifications = (
        ("safe_now", "approval-packets/x2-safe-now-execution.json", 30),
        ("candidate", "prototypes/x2-candidate-execution.json", 20),
        ("cleanup", "maintenance/x2-clean-refine-ledger.json", 30),
    )
    checks = []
    for name, relative, expected in specifications:
        payload = load(relative)
        tasks = payload.get("tasks", [])
        artifacts = [(PHASE / row.get("artifact", "missing")).is_file() for row in tasks]
        checks.append({
            "portfolio": name,
            "expected": expected,
            "count": len(tasks),
            "completed": payload.get("completed"),
            "artifact_count": sum(artifacts),
            "destructive_actions": payload.get("destructive_actions", 0),
            "passed": len(tasks) == expected and payload.get("completed") == expected and all(artifacts) and payload.get("destructive_actions", 0) == 0,
        })
    protected = load("approval-packets/x2-protected-packet-register.json")
    protected_passed = (
        protected.get("inherited_exact_count") == 10
        and protected.get("inherited_blocked_count") == 5
        and protected.get("executed") == 0
        and protected.get("relabelled_safe_now") == 0
    )
    valid = all(row["passed"] for row in checks) and protected_passed
    result = {
        "schema": "ghc.family.v646-v4.portfolio-runner.v1", "checks": checks,
        "protected_packets_unexecuted": protected_passed, "total_tasks": 80,
        "same_owner_only": True, "independent_reproduction": False, "passed": valid, "valid": valid,
        "boundary": "Portfolio completion is bounded to declared owner-scoped software and synthetic gates; it confers no external authority or production credit.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    else:
        print(rendered, end="")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
