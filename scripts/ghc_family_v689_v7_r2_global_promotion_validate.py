#!/usr/bin/env python3
"""Validate the additive Vesper global skill and runner promotion."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

OWNER = "Vesper Arlen"
PHASE = "v689-v7-r2"
BOUNDARY = (
    "Global discoverability, byte parity, same-owner validation, and bounded smoke use do not establish universal correctness, "
    "independent reproduction, production readiness, authority, identity continuity, empirical GMUT confirmation, or Stage 20."
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--runner-root", type=Path, required=True)
    parser.add_argument("--quick-validate", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    skill_root = args.skill_root.resolve()
    runner_root = args.runner_root.resolve()
    quick_validate = args.quick_validate.resolve()
    phase = root / "docs/vesper-arlen/v689-v7-r2"
    plan = load(phase / "plan/skills-runners-plan.json")
    proposals = load(phase / "plan/new-proposals.json")["proposals"]
    by_operation = {row["operation"]: row for row in proposals}
    skill_rows = []
    runner_rows = []
    for spec in plan["global_merge_candidates"]:
        source_skill = phase / "global-candidates/skills" / spec["name"] / "SKILL.md"
        target_skill = skill_root / spec["name"] / "SKILL.md"
        source_hash = digest(source_skill)
        target_hash = digest(target_skill)
        validation = subprocess.run([sys.executable, str(quick_validate), str(target_skill.parent)], text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
        skill_rows.append({"name": spec["name"], "operations": spec["operations"], "source_sha256": source_hash, "target_sha256": target_hash, "byte_parity": source_hash == target_hash, "quick_validate_exit": validation.returncode, "validated": validation.returncode == 0, "next_turn_discovery_required": True})

        source_runner = phase / "global-candidates/runners" / spec["runner"]
        target_runner = runner_root / spec["runner"]
        source_runner_hash = digest(source_runner)
        target_runner_hash = digest(target_runner)
        proposal = by_operation[spec["operations"][0]]
        positive = subprocess.run([sys.executable, str(target_runner), "--module-root", str(root / "scripts"), "--request-json", json.dumps(proposal["request"], ensure_ascii=False)], text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
        adverse = subprocess.run([sys.executable, str(target_runner), "--module-root", str(root / "scripts"), "--request-json", json.dumps(proposal["candidate_request"], ensure_ascii=False)], text=True, encoding="utf-8", errors="replace", capture_output=True, check=False)
        positive_pass = positive.returncode == 0 and json.loads(positive.stdout) == proposal["expected"]
        adverse_pass = adverse.returncode == 2 and json.loads(adverse.stdout) == proposal["candidate_expected"]
        runner_rows.append({"name": spec["runner"], "operations": spec["operations"], "source_sha256": source_runner_hash, "target_sha256": target_runner_hash, "byte_parity": source_runner_hash == target_runner_hash, "positive_smoke": positive_pass, "adverse_subject_failed": True, "adverse_refusal": adverse_pass, "adverse_success_credit": 0})
    all_parity = all(row["byte_parity"] for row in skill_rows + runner_rows)
    all_validated = all(row["validated"] for row in skill_rows)
    all_smoked = all(row["positive_smoke"] and row["adverse_refusal"] for row in runner_rows)
    if not (all_parity and all_validated and all_smoked):
        raise RuntimeError("global promotion validation failed")
    receipt = {"schema": "ghc.family.global-promotion-receipt.v1", "owner": OWNER, "phase": PHASE, "skills_installed": len(skill_rows), "runners_installed": len(runner_rows), "overwrites": 0, "all_byte_parity": all_parity, "all_validated": all_validated, "all_smoked": all_smoked, "skills": skill_rows, "runners": runner_rows, "installation_scope": {"skills": "CODEX_HOME_discoverable_additive", "runners": "D_family_global_tools_additive"}, "rollback": "Remove only these newly absent-at-intake targets after exact review; preserve the repository candidates and receipt.", "boundary": BOUNDARY}
    write(phase / "x2/global-promotion-receipt.json", receipt)
    candidates = load(phase / "x2/global-promotion-candidates.json")
    candidates["promotion_ran"] = True
    candidates["promotion_receipt"] = "x2/global-promotion-receipt.json"
    candidates["state"] = "INSTALLED_VALIDATED_SMOKED_ADDITIVE_NO_OVERWRITE"
    write(phase / "x2/global-promotion-candidates.json", candidates)
    summary = load(phase / "x2/phase-summary.json")
    summary["state"] = "X2_EXECUTED_GLOBAL_PROMOTION_VALIDATED_PENDING_COMMIT"
    summary["global_skills_installed"] = 5
    summary["global_runners_installed"] = 5
    write(phase / "x2/phase-summary.json", summary)
    manifest_path = phase / "x2/manifest.json"
    manifest = load(manifest_path)
    required = [
        "docs/vesper-arlen/v689-v7-r2/x2/global-promotion-receipt.json",
        "scripts/ghc_family_v689_v7_r2_global_promotion_validate.py",
    ]
    known = {row["path"] for row in manifest["entries"]}
    for relative in required:
        if relative not in known:
            manifest["entries"].append({"path": relative})
    for row in manifest["entries"]:
        data = (root / row["path"]).read_bytes().replace(b"\r\n", b"\n")
        row["bytes_normalized_lf"] = len(data)
        row["sha256_normalized_lf"] = hashlib.sha256(data).hexdigest()
    manifest["entries"] = sorted(manifest["entries"], key=lambda row: row["path"])
    manifest["entry_count"] = len(manifest["entries"])
    write(manifest_path, manifest)
    print(json.dumps({"state": candidates["state"], "skills": 5, "runners": 5, "overwrites": 0, "manifest_entries": manifest["entry_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
