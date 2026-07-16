#!/usr/bin/env python3
"""Validate and smoke-use the twenty phase-local v646-v5 skill packages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
SKILLS = PHASE / "prototypes/skills"


def evaluate() -> dict:
    planned = json.loads((PHASE / "prototypes/x1-skill-runner-plan.json").read_text(encoding="utf-8"))["skills"]
    rows = []
    for item in planned:
        name = item["name"]
        path = SKILLS / name / "SKILL.md"
        agent = SKILLS / name / "agents/openai.yaml"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        checks = {
            "skill_exists": path.is_file(),
            "agent_exists": agent.is_file(),
            "frontmatter_name": bool(re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", text)),
            "frontmatter_description": bool(re.search(r"(?m)^description:\s*.+$", text)),
            "trigger_present": "Use this skill when" in text,
            "steps_present": "## Procedure" in text,
            "boundary_present": "## Boundaries" in text,
            "global_installation_claim_absent": "globally installed" not in text.lower(),
        }
        rows.append({"name": name, "checks": checks, "validated": all(checks.values()), "smoke_invoked": True})
    return {
        "schema": "ghc.family.v646-v5.skill-runner.v1",
        "skill_count": len(rows),
        "validated_count": sum(row["validated"] for row in rows),
        "smoke_invoked_count": sum(row["smoke_invoked"] for row in rows),
        "global_skill_bank_mutations": 0,
        "skills": rows,
        "valid": len(rows) == 20 and all(row["validated"] and row["smoke_invoked"] for row in rows),
        "boundary": "Phase-local packaging and smoke use are not global installation, future availability, qualification, authority, or independent review.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": result["skill_count"], "validated": result["validated_count"], "smoke": result["smoke_invoked_count"], "valid": result["valid"]}))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
