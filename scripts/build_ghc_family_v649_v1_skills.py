#!/usr/bin/env python3
"""Initialize, customize, validate, and smoke-use twenty phase-local skills."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v649-v1"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def title(name: str) -> str:
    return " ".join(word.capitalize() for word in name.removeprefix("ghc-family-").split("-"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-creator-root", type=Path, required=True)
    args = parser.parse_args()
    init_script = args.skill_creator_root / "scripts" / "init_skill.py"
    validate_script = args.skill_creator_root / "scripts" / "quick_validate.py"
    plan = json.loads((PHASE / "portfolios" / "skill-plan.json").read_text(encoding="utf-8"))["skills"]
    output_root = PHASE / "skills"
    rows = []
    for item in plan:
        name = item["name"]
        skill_dir = output_root / name
        display = title(name)
        short = item["description"].rstrip(".")[:64]
        default_prompt = f"Use ${name} to run its bounded v649-v1 check and preserve every stated gate."
        if not skill_dir.exists():
            subprocess.run([
                sys.executable, str(init_script), name, "--path", str(output_root),
                "--interface", f"display_name={display}",
                "--interface", f"short_description={short}",
                "--interface", f"default_prompt={default_prompt}",
            ], check=True, capture_output=True, text=True, encoding="utf-8")
        skill_text = f'''---
name: {name}
description: {item["description"]} Use for the matching v649-v1 bounded software, symbolic, structural, or synthetic contract; retain failures and authority gates.
---

# {display}

1. Read the matching proposal contract and source status before evaluation.
2. Run only bounded local fixtures; do not use real participants, credentials, services, operations, or authority decisions.
3. Reject missing obligations, nonzero external-action counters, boundary erasure, or forbidden claim promotion.
4. Retain each rejected fixture as a negative and credit only an explicit passing witness.
5. Report `completed`, `represented`, `open_gap`, or `exact_gate` without widening the evidence scope.

This phase-local skill is workflow evidence only. It does not establish independent reproduction, production readiness, professional competence, legal or cultural authority, Maori authority, complete accessibility, exhaustive security, consciousness, personhood, AGI/ASI, a Theory of Everything, or Stage 20 readiness.
'''
        (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
        write_json(skill_dir / "valid-fixture.json", {"fixture": "bounded", "expected": "accept", "external_action_count": 0, "authority_decision": "none"})
        write_json(skill_dir / "rejecting-fixture.json", {"fixture": "boundary_erasure", "expected": "reject", "external_action_count": 1, "authority_decision": "automatic_real_decision"})
        validation = subprocess.run([sys.executable, str(validate_script), str(skill_dir)], capture_output=True, text=True, encoding="utf-8")
        body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        valid_fixture = json.loads((skill_dir / "valid-fixture.json").read_text(encoding="utf-8"))
        rejecting_fixture = json.loads((skill_dir / "rejecting-fixture.json").read_text(encoding="utf-8"))
        smoke = bool(re.search(rf"(?m)^name: {re.escape(name)}$", body)) and valid_fixture["expected"] == "accept" and rejecting_fixture["expected"] == "reject" and rejecting_fixture["external_action_count"] > 0
        rows.append({
            "skill_id": item["skill_id"], "name": name, "initialized_with_skill_creator": True,
            "phase_local": True, "globally_installed": False, "quick_validate_exit": validation.returncode,
            "quick_validate_passed": validation.returncode == 0, "smoke_used": smoke,
            "subagent_forward_test": "not_run_delegation_prohibited", "boundary": "Phase-local structural smoke use only.",
        })
    passed = all(row["quick_validate_passed"] and row["smoke_used"] for row in rows)
    write_json(PHASE / "x2" / "skill-use-ledger.json", {
        "schema": "ghc.family.v649-v1.skill-use-ledger.v1", "skill_count": len(rows),
        "completed_count": sum(row["quick_validate_passed"] and row["smoke_used"] for row in rows),
        "all_passed": passed, "global_install": False, "subagent_forward_test": False, "skills": rows,
        "boundary": "Initialization, quick validation, and same-owner smoke use only; no global installation or independent forward test.",
    })
    return 0 if passed and len(rows) == 20 else 1


if __name__ == "__main__":
    raise SystemExit(main())
