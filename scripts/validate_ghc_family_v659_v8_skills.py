#!/usr/bin/env python3
"""Validate and smoke-bind the ten Elowen Cairn v659-v8 skills."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import ghc_family_v659_v8_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
QUICK_VALIDATE = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    if not QUICK_VALIDATE.is_file():
        raise FileNotFoundError("skill-creator quick validator is unavailable")
    rows = []
    for (skill_name, purpose), (runner_name, surface) in zip(d.SELF_SKILL_SPECS, d.SELF_RUNNER_SPECS, strict=True):
        skill_dir = PHASE / "skills" / skill_name
        skill_file = skill_dir / "SKILL.md"
        yaml_file = skill_dir / "agents/openai.yaml"
        runner_file = ROOT / "scripts" / runner_name
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(QUICK_VALIDATE), str(skill_dir)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        skill_text = skill_file.read_text(encoding="utf-8") if skill_file.is_file() else ""
        yaml_text = yaml_file.read_text(encoding="utf-8") if yaml_file.is_file() else ""
        checks = {
            "quick_validate_passed": result.returncode == 0,
            "skill_file_present": skill_file.is_file(),
            "agents_yaml_present": yaml_file.is_file(),
            "runner_present": runner_file.is_file(),
            "no_todo_placeholder": "TODO" not in skill_text,
            "frontmatter_name_exact": f"name: {skill_name}" in skill_text,
            "default_prompt_names_skill": f"${skill_name}" in yaml_text,
            "family_runner_name": runner_name.startswith("ghc_family_") and runner_name.endswith(".py"),
        }
        row = {
            "skill_name": skill_name,
            "purpose": purpose,
            "runner": f"scripts/{runner_name}",
            "surface": surface,
            "checks": checks,
            "valid": all(checks.values()),
            "skill_sha256": sha256(skill_file) if skill_file.is_file() else None,
            "agents_yaml_sha256": sha256(yaml_file) if yaml_file.is_file() else None,
            "runner_sha256": sha256(runner_file) if runner_file.is_file() else None,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Packaging and local smoke-binding evidence only; not professional, production, authority, or Stage 20 evidence.",
        }
        rows.append(row)
        write_json(skill_dir / "smoke-receipt.json", {"schema": "ghc.family.skill-smoke-receipt.v1", **row})
    payload = {
        "schema": "ghc.family.v659-v8.skill-validation.v1",
        "skill_count": len(rows),
        "valid_skill_count": sum(row["valid"] for row in rows),
        "all_valid": all(row["valid"] for row in rows),
        "skills": rows,
        "subagent_forward_test_used": False,
        "subagent_forward_test_reason": "The user required solo work; deterministic valid and mutation fixtures provide the authorized bounded test surface.",
        "boundary": "Same-owner packaging validation only; no independent reproduction or protected-gate closure.",
    }
    write_json(PHASE / "tooling/skill-validation.json", payload)
    print(json.dumps({"skill_count": len(rows), "valid_skill_count": payload["valid_skill_count"], "all_valid": payload["all_valid"]}, sort_keys=True))
    if not payload["all_valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
