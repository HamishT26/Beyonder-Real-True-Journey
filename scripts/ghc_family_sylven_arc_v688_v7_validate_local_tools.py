#!/usr/bin/env python3
"""Quick-validate and accepting/adverse smoke all owner-local chess tools."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_chess_records_core as core


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"},
    )


def smoke(script: Path, operations: list[str], proposals: list[dict], fixture_root: Path, scope_name: str) -> list[dict]:
    fixture_root = fixture_root / scope_name
    fixture_root.mkdir()
    rows = []
    for operation in operations:
        proposal = next(item for item in proposals if item["operation"] == operation and item["expected_acceptance"])
        accepted_path = fixture_root / f"{operation}-accepted.json"
        adverse_path = fixture_root / f"{operation}-adverse.json"
        write_new(accepted_path, proposal["input"])
        write_new(adverse_path, {**proposal["input"], "undeclared_extension": True})
        accepted = run([sys.executable, "-B", "-X", "utf8", str(script), str(accepted_path)])
        adverse = run([sys.executable, "-B", "-X", "utf8", str(script), str(adverse_path)])
        try:
            accepted_json = json.loads(accepted.stdout)
            adverse_json = json.loads(adverse.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"non_json_smoke:{script.name}:{operation}") from exc
        if accepted.returncode != 0 or not core.matches_contract(proposal, accepted_json):
            raise RuntimeError(f"accepting_smoke:{script.name}:{operation}")
        if adverse.returncode != 2 or adverse_json.get("accepted") is not False or adverse_json.get("error") != "field_set":
            raise RuntimeError(f"adverse_smoke:{script.name}:{operation}")
        rows.append({
            "operation": operation,
            "accepting_complete_envelope_pass": True,
            "accepting_output_sha256": hashlib.sha256(canonical(accepted_json)).hexdigest(),
            "adverse_rejected": True,
            "adverse_error": "field_set",
            "adverse_output_sha256": hashlib.sha256(canonical(adverse_json)).hexdigest(),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    fixture_root = bank / "local-tool-fixtures"
    fixture_root.mkdir(exist_ok=False)
    plan = json.loads((BASE / "x1/tool-package-plan.json").read_text(encoding="utf-8"))
    proposals = json.loads((BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    validator = args.skill_root.resolve() / ".system/skill-creator/scripts/quick_validate.py"
    if not validator.is_file():
        raise RuntimeError("skill_quick_validator_missing")
    skills = []
    runners = []
    try:
        for item in plan["skills"]:
            folder = BASE / "skills" / item["name"]
            validation = run([sys.executable, "-B", "-X", "utf8", str(validator), str(folder)])
            if validation.returncode != 0:
                raise RuntimeError(f"quick_validate:{item['name']}")
            script = folder / "scripts/ghc_family_chess_record_skill.py"
            skills.append({
                "name": item["name"],
                "quick_validate_pass": True,
                "file_count": sum(path.is_file() for path in folder.rglob("*")),
                "smokes": smoke(script, item["operation_pair"], proposals, fixture_root, "skill-" + item["name"]),
            })
        for item in plan["runners"]:
            script = ROOT / "scripts" / item["name"]
            runners.append({
                "name": item["name"],
                "smokes": smoke(script, item["operation_group"], proposals, fixture_root, "runner-" + script.stem),
            })
        receipt = {
            "schema": "ghc.family.chess-local-tool-validation.v1",
            "owner": "Sylven Arc",
            "phase": "v688-v7",
            "skill_count": len(skills),
            "runner_count": len(runners),
            "operation_count": sum(len(item["smokes"]) for item in skills),
            "skills": skills,
            "runners": runners,
            "accepting_smoke_count": sum(len(item["smokes"]) for item in skills + runners),
            "adverse_rejection_count": sum(len(item["smokes"]) for item in skills + runners),
            "failures": [],
            "state": "VALID_LOCAL_OWNER_TOOLS",
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": core.BOUNDARY,
        }
        write_new(bank / "local-tool-validation.json", receipt)
        write_new(BASE / "x2/local-tool-validation.json", receipt)
        print(json.dumps({"state": receipt["state"], "skills": len(skills), "runners": len(runners), "accepting_smokes": receipt["accepting_smoke_count"], "adverse_smokes": receipt["adverse_rejection_count"]}, sort_keys=True))
    except Exception as exc:
        write_new(bank / "local-tool-validation-failure.json", {
            "state": "FAILED_RETAINED",
            "error_class": type(exc).__name__,
            "signature": str(exc),
            "success_credit": 0,
            "recovery": "Inspect the named local skill or runner and rerun only its failed dependency.",
        })
        raise


if __name__ == "__main__":
    main()
