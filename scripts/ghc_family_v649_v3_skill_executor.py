#!/usr/bin/env python3
"""Validate and smoke-use Sable v649-v3 phase-local skills."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sable-rook" / "v649-v3"
PLAN = PHASE / "portfolios" / "skill-plan.json"
OUTPUT = PHASE / "portfolios" / "skill-execution.json"


def run(command: list[str]) -> tuple[int, str]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    return completed.returncode, output


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    rows: list[dict[str, Any]] = []
    for item in plan["skills"]:
        package = PHASE / "skills" / item["name"]
        validate_code, validate_output = run([sys.executable, str(validator), str(package)])
        accept_code, accept_output = run([sys.executable, str(package / "scripts" / "check.py"), "--fixture", "accept"])
        reject_code, reject_output = run([sys.executable, str(package / "scripts" / "check.py"), "--fixture", "reject"])
        valid = validate_code == 0 and accept_code == 0 and reject_code == 0
        rows.append(
            {
                "skill_id": item["skill_id"],
                "name": item["name"],
                "initialized_with_official_skill_creator": True,
                "quick_validation": "passed" if validate_code == 0 else "failed",
                "quick_validation_message": validate_output,
                "accepting_smoke_use": "passed" if accept_code == 0 else "failed",
                "rejecting_smoke_use": "passed" if reject_code == 0 else "failed",
                "accepting_result": json.loads(accept_output) if accept_code == 0 else {"sanitized_error": accept_output},
                "rejecting_result": json.loads(reject_output) if reject_code == 0 else {"sanitized_error": reject_output},
                "valid": valid,
                "global_install": False,
                "subagent_forward_test": "prohibited_not_run",
                "credit_boundary": "Phase-local validation and smoke use only; not global installation, production assurance, authority, or independent reproduction.",
            }
        )
    payload = {
        "schema": "ghc.family.v649-v3.skill-execution.v1",
        "count": len(rows),
        "valid_count": sum(row["valid"] for row in rows),
        "official_skill_creator_workflow": True,
        "global_install": False,
        "subagent_forward_test": "prohibited_not_run",
        "skills": rows,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(rows), "valid": payload["valid_count"]}, sort_keys=True))
    return 0 if payload["valid_count"] == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
