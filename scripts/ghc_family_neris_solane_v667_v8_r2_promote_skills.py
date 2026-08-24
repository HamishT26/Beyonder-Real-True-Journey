#!/usr/bin/env python3
"""Additively promote the ten validated Neris v667-v8-r2 skills."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r2"
SOURCE_ROOT = PHASE_ROOT / "skills"
GLOBAL_ROOT = Path.home() / ".codex" / "skills"
VALIDATOR = GLOBAL_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
EXPECTED = (
    "ghc-family-api-surface-check",
    "ghc-family-artifact-integrity-ledger",
    "ghc-family-codex-prefix-guard",
    "ghc-family-import-contract",
    "ghc-family-lockfile-origin-policy",
    "ghc-family-package-metadata-boundary",
    "ghc-family-spdx-structure-validator",
    "ghc-family-test-timeout-discipline",
    "ghc-family-toolchain-transaction-guard",
    "ghc-family-wheel-content-audit",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(path: Path) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    return {
        "returncode": result.returncode,
        "passed": result.returncode == 0 and "Skill is valid!" in result.stdout,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main() -> int:
    if not VALIDATOR.is_file():
        raise RuntimeError("quick_validate helper is unavailable")
    actual = tuple(sorted(path.name for path in SOURCE_ROOT.iterdir() if path.is_dir()))
    if actual != EXPECTED:
        raise RuntimeError(f"phase-local skill set drift: {actual}")

    preflight: list[dict[str, object]] = []
    for name in EXPECTED:
        source = SOURCE_ROOT / name
        source_skill = source / "SKILL.md"
        if not source_skill.is_file():
            raise RuntimeError(f"missing phase-local SKILL.md: {name}")
        source_validation = validate(source)
        if not source_validation["passed"]:
            raise RuntimeError(f"phase-local validation failed: {name}: {source_validation}")
        destination = GLOBAL_ROOT / name
        if destination.exists():
            destination_skill = destination / "SKILL.md"
            if not destination_skill.is_file() or sha256(destination_skill) != sha256(source_skill):
                raise RuntimeError(f"refusing to overwrite non-identical global skill: {name}")
            state = "ALREADY_PRESENT_IDENTICAL"
        else:
            state = "ABSENT_READY_FOR_ADDITIVE_INSTALL"
        preflight.append({
            "skill": name,
            "state": state,
            "source_skill_sha256": sha256(source_skill),
            "source_validation": source_validation,
        })

    installed_now = 0
    for row in preflight:
        name = str(row["skill"])
        source = SOURCE_ROOT / name
        destination = GLOBAL_ROOT / name
        if not destination.exists():
            shutil.copytree(source, destination)
            installed_now += 1
        destination_validation = validate(destination)
        if not destination_validation["passed"]:
            raise RuntimeError(f"global validation failed: {name}: {destination_validation}")
        if sha256(destination / "SKILL.md") != row["source_skill_sha256"]:
            raise RuntimeError(f"global SKILL.md hash mismatch: {name}")
        row["destination"] = f"<CODEX_SKILL_ROOT>/{name}"
        row["destination_validation"] = destination_validation
        row["installed"] = True

    receipt = {
        "schema": "ghc-family-global-skill-promotion-receipt-v1",
        "owner": "Neris Solane",
        "phase": "v667-v8-r2",
        "generated_at_utc": "2026-08-24T03:10:00.000Z",
        "mode": "additive_exact_absence_or_identical_resume",
        "global_root_alias": "<CODEX_SKILL_ROOT>",
        "skill_count": len(preflight),
        "installed_now": installed_now,
        "validated_count": sum(bool(row["destination_validation"]["passed"]) for row in preflight),
        "overwritten_count": 0,
        "deleted_count": 0,
        "status": "PASS",
        "skills": preflight,
        "boundary": "local Codex skill discovery only; no production, credential, authority, identity, legal, cultural, Maori, scientific, or Stage 20 claim",
    }
    receipt_path = PHASE_ROOT / "x2" / "global-skill-promotion-receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    summary_path = PHASE_ROOT / "x2" / "skills-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["global_install_count"] = len(preflight)
    summary["promotion_state"] = "PASS_ADDITIVE_GLOBAL_PROMOTION"
    summary["promotion_receipt"] = "docs/neris-solane/v667-v8-r2/x2/global-skill-promotion-receipt.json"
    for row in summary["skills"]:
        row["global_install_count"] = 1
        row["global_promotion_state"] = "PASS"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "skills": len(preflight), "installed_now": installed_now}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
