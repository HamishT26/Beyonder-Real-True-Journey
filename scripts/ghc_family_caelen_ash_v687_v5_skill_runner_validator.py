#!/usr/bin/env python3
"""Validate, smoke-use, and collision-safely promote Caelen v687-v5 skills and runners."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from build_ghc_family_caelen_ash_v687_v5_x1 import BASE, OPS
from ghc_family_caelen_ash_v687_v5_core import strict_equal, strict_load


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / BASE


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def write(relative: str, value) -> None:
    path = PHASE / "x2" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(encoded(value))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_members(root: Path) -> list[Path]:
    return sorted((path for path in root.rglob("*") if path.is_file()), key=lambda path: path.relative_to(root).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-evidence", type=Path, required=True)
    parser.add_argument("--global-skills", type=Path, required=True)
    parser.add_argument("--global-scripts", type=Path, required=True)
    parser.add_argument("--quick-validate", type=Path, required=True)
    parser.add_argument("--host-python", type=Path, required=True)
    args = parser.parse_args()

    runtime = args.runtime_evidence.resolve()
    runtime.mkdir(parents=True, exist_ok=False)
    proposals = strict_load(PHASE / "x1" / "new-proposals.json")["proposals"]
    by_operation = {operation: next(row for row in proposals if row["operation"] == operation) for operation, *_ in OPS}

    validation = []
    for operation, slug, *_ in OPS:
        skill_name = "ghc-family-" + slug
        skill = PHASE / "skills" / skill_name
        wrapper = ROOT / "scripts" / f"ghc_family_caelen_ash_v687_v5_{operation}.py"
        proposal = by_operation[operation]
        input_path = runtime / f"{operation}-input.json"
        output_path = runtime / f"{operation}-output.json"
        invalid_path = runtime / f"{operation}-duplicate-input.json"
        invalid_output = runtime / f"{operation}-invalid-output.json"
        input_path.write_bytes(encoded(proposal["input"]))
        invalid_path.write_text('{"duplicate":1,"duplicate":2}\n', encoding="utf-8", newline="\n")

        useful = subprocess.run(
            [sys.executable, str(wrapper), "--input", str(input_path), "--output", str(output_path)],
            cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True,
        )
        observed = strict_load(output_path) if output_path.exists() else None
        invalid = subprocess.run(
            [sys.executable, str(wrapper), "--input", str(invalid_path), "--output", str(invalid_output)],
            cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True,
        )
        quick = subprocess.run(
            [str(args.host_python), str(args.quick_validate), str(skill)],
            cwd=ROOT, text=True, encoding="utf-8", errors="strict", capture_output=True,
        )
        manifest = strict_load(skill / "manifest.json")
        manifest_pass = all(file_hash(skill / member["path"]) == member["sha256"] for member in manifest["entries"])
        row = {
            "operation": operation,
            "proposal": proposal["id"],
            "skill": skill_name,
            "source_files": len(relative_members(skill)),
            "quick_validate_passed": quick.returncode == 0,
            "frontmatter_validated": quick.returncode == 0,
            "manifest_validated": manifest_pass,
            "cli_exit_code": useful.returncode,
            "cli_result_matches": useful.returncode == 0 and strict_equal(observed, proposal["expected_output"]),
            "invalid_cli_exit_nonzero": invalid.returncode != 0,
            "invalid_output_absent": not invalid_output.exists(),
            "invalid_candidate_original_success_credit": 0,
            "same_owner_only": True,
        }
        validation.append(row)
    if not all(
        row["quick_validate_passed"] and row["manifest_validated"] and row["cli_result_matches"]
        and row["invalid_cli_exit_nonzero"] and row["invalid_output_absent"]
        for row in validation
    ):
        raise SystemExit("skill or runner validation failed")
    write("skill-runner-validation.json", validation)

    skill_sources = [PHASE / "skills" / ("ghc-family-" + slug) for _, slug, *_ in OPS]
    skill_targets = [args.global_skills / source.name for source in skill_sources]
    shared_operations = [operation for operation, *_ in OPS[:5]]
    runner_sources = [ROOT / "scripts" / f"ghc_family_caelen_ash_v687_v5_{operation}.py" for operation in shared_operations]
    runner_sources.append(ROOT / "scripts" / "ghc_family_caelen_ash_v687_v5_core.py")
    runner_targets = [args.global_scripts / source.name for source in runner_sources]

    collisions = [str(target.name) for target in skill_targets + runner_targets if target.exists()]
    if collisions:
        raise SystemExit("promotion collision: " + ",".join(collisions))
    if not all(source.exists() for source in skill_sources + runner_sources):
        raise SystemExit("promotion source missing")

    for source, target in zip(skill_sources, skill_targets):
        shutil.copytree(source, target)
    args.global_scripts.mkdir(parents=True, exist_ok=True)
    for source, target in zip(runner_sources, runner_targets):
        shutil.copy2(source, target)

    members = []
    parity = True
    for source, target in zip(skill_sources, skill_targets):
        source_members = relative_members(source)
        target_members = relative_members(target)
        parity = parity and [path.relative_to(source).as_posix() for path in source_members] == [path.relative_to(target).as_posix() for path in target_members]
        for member in source_members:
            relative = member.relative_to(source)
            source_digest = file_hash(member)
            target_digest = file_hash(target / relative)
            parity = parity and source_digest == target_digest
            members.append({"skill": source.name, "path": relative.as_posix(), "sha256": source_digest})
    for source, target in zip(runner_sources, runner_targets):
        parity = parity and file_hash(source) == file_hash(target)
    if not parity:
        raise SystemExit("post-copy byte parity failure")

    receipt = {
        "skills": len(skill_sources),
        "skill_files": len(members),
        "shared_runners": len(shared_operations),
        "dependency_files": 1,
        "shared_names": [source.name for source in runner_sources],
        "collision_free": True,
        "source_global_byte_parity": True,
        "same_owner_only": True,
        "members": members,
    }
    write("promotion-receipt.json", receipt)
    write(
        "global-install-validation.json",
        {
            "global_skills_validated": len(skill_sources),
            "shared_interfaces_smoked": len(shared_operations),
            "exact_parity_verified": True,
            "new_independent_witness_credit": 0,
        },
    )
    print(json.dumps({"skills_validated": len(validation), "skills_promoted": len(skill_sources), "skill_files": len(members), "shared_runners": len(shared_operations), "dependency_files": 1, "parity": parity}))


if __name__ == "__main__":
    main()
