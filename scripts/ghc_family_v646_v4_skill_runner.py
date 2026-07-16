#!/usr/bin/env python3
"""Verify the twenty phase-local v646-v4 skills were validated and smoke-used."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v646-v4"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = json.loads((PHASE / "prototypes/skill-build-receipt.json").read_text(encoding="utf-8"))
    rows = receipt.get("skills", [])
    checks = []
    for row in rows:
        package = PHASE / "prototypes/skills" / row.get("name", "missing")
        passed = (
            package.joinpath("SKILL.md").is_file()
            and package.joinpath("agents/openai.yaml").is_file()
            and row.get("quick_validate_returncode") == 0
            and row.get("bounded_smoke_use", {}).get("passed") is True
            and row.get("global_skill_bank_mutated") is False
        )
        checks.append({"name": row.get("name"), "passed": passed})
    valid = receipt.get("valid") is True and len(rows) == 20 and all(row["passed"] for row in checks)
    result = {
        "schema": "ghc.family.v646-v4.skill-runner.v1", "skill_count": len(rows),
        "validated_count": receipt.get("validated_count"), "smoke_use_pass_count": receipt.get("smoke_use_pass_count"),
        "checks": checks, "subagents_used": 0, "global_skill_bank_mutated": False,
        "same_owner_only": True, "independent_reproduction": False, "passed": valid, "valid": valid,
        "boundary": "Phase-local packaging and smoke use are not global installation, future availability, professional competence, authority, or independent reproduction.",
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
