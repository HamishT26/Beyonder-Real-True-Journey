"""Additively promote five validated Lyren error-control skills and runners."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
X2 = BASE / "x2"
PLAN = BASE / "plan"
RECEIPT = X2 / "tooling/global-promotion.json"
DEPENDENCIES = ["ghc_family_error_control_x1.py", "ghc_family_error_control_x2.py"]
BOUNDARY = (
    "Additive local-tool installation and bounded same-owner smoke evidence only; "
    "no production, identity, authority, external-audit, or independent-reproduction claim."
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(path: Path, request: dict[str, object], python: Path, runner_root: Path) -> dict[str, object]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(runner_root)
    completed = subprocess.run(
        [str(python), str(path), "--request-json", json.dumps(request)],
        cwd=runner_root,
        env=env,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"runner failed: {path.name}: {completed.stderr}")
    return json.loads(completed.stdout)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-root", required=True)
    parser.add_argument("--runner-root", required=True)
    parser.add_argument("--validator-python", required=True)
    parser.add_argument("--runtime-python", required=True)
    parser.add_argument("--quick-validate", required=True)
    args = parser.parse_args()
    skill_root = Path(args.skill_root).resolve()
    runner_root = Path(args.runner_root).resolve()
    validator_python = Path(args.validator_python).resolve()
    runtime_python = Path(args.runtime_python).resolve()
    quick_validate = Path(args.quick_validate).resolve()
    if RECEIPT.exists():
        raise SystemExit("promotion receipt already exists; refusing replay")
    for path in [skill_root, runner_root, validator_python, runtime_python, quick_validate]:
        if not path.exists():
            raise SystemExit(f"required path unavailable: {path}")

    plan = json.loads((PLAN / "skills-runners.json").read_text(encoding="utf-8"))
    proposals = json.loads((PLAN / "new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    groups = plan["global_groups"]
    skill_pairs = [(X2 / "global-skills" / row["name"], skill_root / row["name"]) for row in groups]
    runner_pairs = [(X2 / "global-runners" / row["runner"], runner_root / row["runner"]) for row in groups]
    dependency_pairs = [(ROOT / "scripts" / name, runner_root / name) for name in DEPENDENCIES]
    collisions = [str(target) for _, target in skill_pairs + runner_pairs + dependency_pairs if target.exists()]
    missing_sources = [str(source) for source, _ in skill_pairs + runner_pairs + dependency_pairs if not source.exists()]
    if collisions or missing_sources:
        raise SystemExit(json.dumps({"collisions": collisions, "missing_sources": missing_sources}, sort_keys=True))

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    source_validation = []
    for source, _ in skill_pairs:
        completed = subprocess.run(
            [str(validator_python), str(quick_validate), str(source)],
            env=env,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        source_validation.append(
            {"skill": source.name, "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "passed": completed.returncode == 0}
        )
    if not all(row["passed"] for row in source_validation):
        raise RuntimeError("candidate validation failed before promotion")

    for source, target in skill_pairs:
        shutil.copytree(source, target, copy_function=shutil.copy2)
    for source, target in runner_pairs + dependency_pairs:
        shutil.copy2(source, target)

    skill_receipts = []
    for source, target in skill_pairs:
        completed = subprocess.run(
            [str(validator_python), str(quick_validate), str(target)],
            env=env,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        source_files = {path.relative_to(source).as_posix(): digest(path) for path in source.rglob("*") if path.is_file()}
        target_files = {path.relative_to(target).as_posix(): digest(path) for path in target.rglob("*") if path.is_file()}
        skill_receipts.append(
            {
                "name": source.name,
                "source": str(source),
                "target": str(target),
                "source_files": source_files,
                "target_files": target_files,
                "byte_parity": source_files == target_files,
                "validation_returncode": completed.returncode,
                "validation_stdout": completed.stdout,
                "validation_stderr": completed.stderr,
                "validated": completed.returncode == 0,
                "overwrote_existing": False,
            }
        )

    runner_receipts = []
    for group, (source, target) in zip(groups, runner_pairs):
        proposal = next(row for row in proposals if row["operation"] in group["operations"])
        positive = run_json(target, proposal["request"], runtime_python, runner_root)
        outside_request = {"operation": "outside_group", "payload": {}}
        adverse = run_json(target, outside_request, runtime_python, runner_root)
        expected_adverse = {"ok": False, "error": "operation_outside_group", "original_success_credit": 0}
        runner_receipts.append(
            {
                "name": target.name,
                "source": str(source),
                "target": str(target),
                "source_sha256": digest(source),
                "target_sha256": digest(target),
                "byte_parity": digest(source) == digest(target),
                "positive_expected": proposal["expected"],
                "positive_observed": positive,
                "positive_passed": positive == proposal["expected"],
                "adverse_expected": expected_adverse,
                "adverse_observed": adverse,
                "adverse_passed": adverse == expected_adverse,
                "overwrote_existing": False,
            }
        )

    dependency_receipts = [
        {
            "name": target.name,
            "source": str(source),
            "target": str(target),
            "source_sha256": digest(source),
            "target_sha256": digest(target),
            "byte_parity": digest(source) == digest(target),
            "runner_credit": 0,
            "role": "shared dependency",
            "overwrote_existing": False,
        }
        for source, target in dependency_pairs
    ]
    passed = (
        all(row["validated"] and row["byte_parity"] for row in skill_receipts)
        and all(row["byte_parity"] and row["positive_passed"] and row["adverse_passed"] for row in runner_receipts)
        and all(row["byte_parity"] for row in dependency_receipts)
    )
    if not passed:
        raise RuntimeError("post-promotion validation failed; additive files retained for audit")
    receipt = {
        "schema": "ghc.family.tool-promotion.receipt.v1",
        "owner": "Lyren Moss",
        "phase": "v690-v1-x2",
        "state": "INSTALLED_ADDITIVELY_VALIDATED",
        "skill_root": str(skill_root),
        "runner_root": str(runner_root),
        "skills": skill_receipts,
        "runners": runner_receipts,
        "dependencies": dependency_receipts,
        "counts": {"skills": 5, "public_runners": 5, "dependency_modules": 2},
        "no_overwrite": True,
        "passed": True,
        "rollback": "Stop selecting these exact additive paths. Preserve the installation and receipt until a separately authorized removal workflow.",
        "boundary": BOUNDARY,
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    with RECEIPT.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")
    print(json.dumps({"skills": 5, "public_runners": 5, "dependency_modules": 2, "passed": True}, sort_keys=True))


if __name__ == "__main__":
    main()
