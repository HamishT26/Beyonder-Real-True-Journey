#!/usr/bin/env python3
"""Promote ten validated skills and five runner interfaces without overwriting."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
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


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")


def smoke(script: Path, operations: list[str], proposals: list[dict], fixture_root: Path, env: dict[str, str]) -> list[dict]:
    fixture_root.mkdir()
    rows = []
    for operation in operations:
        proposal = next(item for item in proposals if item["operation"] == operation and item["expected_acceptance"])
        accepted_path = fixture_root / f"{operation}-accepted.json"
        adverse_path = fixture_root / f"{operation}-adverse.json"
        write_new(accepted_path, proposal["input"])
        write_new(adverse_path, {**proposal["input"], "undeclared_extension": True})
        accepted = run([sys.executable, "-B", "-X", "utf8", str(script), str(accepted_path)], env)
        adverse = run([sys.executable, "-B", "-X", "utf8", str(script), str(adverse_path)], env)
        try:
            accepted_json = json.loads(accepted.stdout)
            adverse_json = json.loads(adverse.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"promotion_smoke_json:{operation}") from exc
        if accepted.returncode != 0 or not core.matches_contract(proposal, accepted_json):
            raise RuntimeError(f"promotion_accepting_smoke:{operation}")
        if adverse.returncode != 2 or adverse_json.get("accepted") is not False or adverse_json.get("error") != "field_set":
            raise RuntimeError(f"promotion_adverse_smoke:{operation}")
        rows.append({
            "operation": operation,
            "accepting_complete_envelope_pass": True,
            "accepting_sha256": hashlib.sha256(canonical(accepted_json)).hexdigest(),
            "adverse_rejected": True,
            "adverse_sha256": hashlib.sha256(canonical(adverse_json)).hexdigest(),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--skills", type=Path, required=True)
    parser.add_argument("--runners", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    skill_root = args.skills.resolve()
    runner_root = args.runners.resolve()
    if bank.drive.upper() != "D:" or runner_root.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_and_runner_root_required")
    plan = json.loads((BASE / "x1/tool-package-plan.json").read_text(encoding="utf-8"))
    proposals = json.loads((BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    local = json.loads((BASE / "x2/local-tool-validation.json").read_text(encoding="utf-8"))
    if local["state"] != "VALID_LOCAL_OWNER_TOOLS" or local["skill_count"] != 10 or local["runner_count"] != 5:
        raise RuntimeError("local_validation_gate")
    if any((skill_root / item["name"]).exists() for item in plan["skills"]):
        raise RuntimeError("global_skill_collision")
    if runner_root.exists():
        raise RuntimeError("runner_bank_collision")
    marker = bank / "promotion-invoked.json"
    write_new(marker, {"state": "STARTED", "skills": 10, "runner_interfaces": 5, "overwrite": False})
    fixture_root = bank / "promotion-fixtures"
    fixture_root.mkdir(exist_ok=False)
    parity = []
    skill_receipts = []
    runner_receipts = []
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1", "GHC_CHESS_RUNNER_ROOT": str(runner_root)}
    validator = skill_root / ".system/skill-creator/scripts/quick_validate.py"
    try:
        # Validate every source before the first external copy.
        for item in plan["skills"]:
            source = BASE / "skills" / item["name"]
            if any(path.is_symlink() for path in source.rglob("*")):
                raise RuntimeError(f"source_symlink:{item['name']}")
            result = run([sys.executable, "-B", "-X", "utf8", str(validator), str(source)], env)
            if result.returncode:
                raise RuntimeError(f"source_quick_validate:{item['name']}")
        runner_root.mkdir(parents=True, exist_ok=False)
        runner_names = [item["name"] for item in plan["runners"]] + ["ghc_family_chess_records_core.py"]
        for name in runner_names:
            source = ROOT / "scripts" / name
            target = runner_root / name
            with target.open("xb") as stream:
                stream.write(source.read_bytes())
            if target.read_bytes() != source.read_bytes():
                raise RuntimeError(f"runner_byte_parity:{name}")
            parity.append({
                "source": f"scripts/{name}",
                "target_class": "D-first shared runner bank",
                "target_name": name,
                "bytes": len(source.read_bytes()),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "byte_equal": True,
            })
        for index, item in enumerate(plan["skills"], 1):
            source = BASE / "skills" / item["name"]
            target = skill_root / item["name"]
            shutil.copytree(source, target, dirs_exist_ok=False)
            for path in sorted(candidate for candidate in source.rglob("*") if candidate.is_file()):
                copied = target / path.relative_to(source)
                if copied.read_bytes() != path.read_bytes():
                    raise RuntimeError(f"skill_byte_parity:{item['name']}")
                parity.append({
                    "source": path.relative_to(ROOT).as_posix(),
                    "target_class": "global Codex skill root",
                    "target_name": item["name"] + "/" + path.relative_to(source).as_posix(),
                    "bytes": len(path.read_bytes()),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "byte_equal": True,
                })
            validation = run([sys.executable, "-B", "-X", "utf8", str(validator), str(target)], env)
            if validation.returncode:
                raise RuntimeError(f"installed_quick_validate:{item['name']}")
            skill_receipts.append({
                "name": item["name"],
                "quick_validate_pass": True,
                "smokes": smoke(target / "scripts/ghc_family_chess_record_skill.py", item["operation_pair"], proposals, fixture_root / f"skill-{index:02d}", env),
            })
            print(json.dumps({"promoted_skill": item["name"], "count": index}), flush=True)
        for index, item in enumerate(plan["runners"], 1):
            runner_receipts.append({
                "name": item["name"],
                "smokes": smoke(runner_root / item["name"], item["operation_group"], proposals, fixture_root / f"runner-{index:02d}", env),
            })
        receipt = {
            "schema": "ghc.family.chess-tool-promotion.v1",
            "owner": "Sylven Arc",
            "phase": "v688-v7",
            "state": "PROMOTED_VALIDATED_BYTE_EQUAL",
            "skill_count": len(skill_receipts),
            "runner_interface_count": len(runner_receipts),
            "shared_core_count": 1,
            "overwrites": 0,
            "older_compatibility_files_changed": 0,
            "skills": skill_receipts,
            "runners": runner_receipts,
            "parity": parity,
            "accepting_smokes": sum(len(item["smokes"]) for item in skill_receipts + runner_receipts),
            "adverse_smokes": sum(len(item["smokes"]) for item in skill_receipts + runner_receipts),
            "rollback": "Select the retained prior package or runner bank; do not erase either historical package.",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "boundary": core.BOUNDARY,
        }
        write_new(bank / "promotion-receipt.json", receipt)
        write_new(BASE / "x2/promotion-receipt.json", receipt)
        print(json.dumps({"state": receipt["state"], "skills": 10, "runners": 5, "accepting_smokes": receipt["accepting_smokes"], "adverse_smokes": receipt["adverse_smokes"]}, sort_keys=True))
    except Exception as exc:
        write_new(bank / "promotion-failure.json", {
            "state": "FAILED_RETAINED",
            "error_class": type(exc).__name__,
            "signature": str(exc),
            "skills_completed": [item["name"] for item in skill_receipts],
            "runners_completed": [item["name"] for item in runner_receipts],
            "parity_records": parity,
            "success_credit": 0,
            "recovery": "Inspect each persisted target and recover only the failed dependency; never overwrite or duplicate.",
        })
        raise


if __name__ == "__main__":
    main()
