#!/usr/bin/env python3
"""Validate an integrated GHC phase bundle and its truth boundaries."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from scripts.ghc_family_empirical_adapters import validate_adapter_manifest
    from scripts.ghc_family_freed_id_conformance import run_vectors
except ModuleNotFoundError:  # direct `python scripts/...` execution
    from ghc_family_empirical_adapters import validate_adapter_manifest
    from ghc_family_freed_id_conformance import run_vectors


ALLOWED_DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
LOCAL_PATH = re.compile(r"(?i)(?:[a-z]:\\|[a-z]:/users/|/home/[^/]+/)")
PRIVATE_PATTERNS = {
    "openai_style_secret": re.compile(r"\bsk-[A-Za-z0-9_-]{12,}"),
    "github_token": re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]{12,}"),
    "raw_thread_field": re.compile(r'(?i)"(?:threadId|clientThreadId|thread_id)"\s*:'),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_phase(phase_dir: Path, repo_root: Path, *, final: bool) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    def issue(path: str, code: str, message: str) -> None:
        issues.append({"path": path, "code": code, "message": message})

    required = [
        "80-work-unit-ledger.json",
        "80-work-unit-ledger.md",
        "mission-matrix.md",
        "sources/source-ledger.json",
        "empirical/adapter-manifest.json",
        "empirical/adapter-validation.json",
        "physics/gmut-kernel-v641-demo.json",
        "thos/benchmark-protocol.json",
        "thos/synthetic-scorer-calibration-output.json",
        "freed-id/minimum-profile.json",
        "freed-id/conformance-vectors.json",
        "freed-id/conformance-report.json",
        "cbr/model-charter.md",
        "cbr/crosswalk.json",
        "security/red-team.json",
        "security/threat-model.md",
        "reproduction/manifest.json",
        "research/thermo-psyche-hypotheses.json",
        "research/unsolved-problems.json",
        "stage20/evidence-board.json",
        "next-ten-proposals.json",
        "phase-truth.json",
        "complete-incomplete-checklist.json",
        "v641-v1-integrated-overview.md",
        "wellbeing-check.md",
        "tooling/ghc-family-index.json",
    ]
    if final:
        required += [
            "deliverables/v641-v1-evidence-board.html",
            "deliverables/v641-v1-evidence-board.pdf",
            "deliverables/portable-overflow-diagnostic.json",
        ]
    for rel in required:
        if not (phase_dir / rel).is_file():
            issue(rel, "missing_required_file", "required phase artifact is absent")

    for path in phase_dir.rglob("*.json"):
        try:
            load_json(path)
        except Exception as exc:  # pragma: no cover - precise parser text is platform dependent
            issue(path.relative_to(phase_dir).as_posix(), "invalid_json", str(exc))

    ledger_path = phase_dir / "80-work-unit-ledger.json"
    if ledger_path.is_file():
        ledger = load_json(ledger_path)
        units = ledger.get("work_units", [])
        if len(units) != 80:
            issue("80-work-unit-ledger.json", "wrong_unit_count", str(len(units)))
        ids = [row.get("work_unit_id") for row in units]
        if len(set(ids)) != len(ids):
            issue("80-work-unit-ledger.json", "duplicate_work_unit_id", "IDs must be unique")
        slots = [row.get("origin_plan_slot") for row in units]
        if len(set(slots)) != 80:
            issue("80-work-unit-ledger.json", "origin_slot_coverage", "expected 80 unique origin slots")
        dispositions = Counter(row.get("x2", {}).get("disposition") for row in units)
        unexpected = set(dispositions) - ALLOWED_DISPOSITIONS
        if unexpected:
            issue("80-work-unit-ledger.json", "invalid_disposition", str(sorted(unexpected)))
        for index, row in enumerate(units):
            if row.get("x1", {}).get("status") != "completed":
                issue(f"work_units[{index}]", "x1_not_preregistered", "x1 status must be completed")
            if row.get("x2", {}).get("execution_receipt") != "assessed_and_outcome_recorded":
                issue(f"work_units[{index}]", "missing_x2_receipt", "unit lacks outcome receipt")
            artifact = row.get("x2", {}).get("artifact")
            if not artifact or not (repo_root / artifact).is_file():
                issue(f"work_units[{index}]", "missing_referenced_artifact", str(artifact))

    adapter_path = phase_dir / "empirical" / "adapter-manifest.json"
    if adapter_path.is_file():
        payload = load_json(adapter_path)
        for adapter_issue in validate_adapter_manifest(payload.get("adapters", [])):
            issue("empirical/adapter-manifest.json", adapter_issue.code, adapter_issue.message)
        if payload.get("fit_status") != "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION":
            issue("empirical/adapter-manifest.json", "fit_boundary_missing", "empirical boundary changed")

    profile_path = phase_dir / "freed-id" / "minimum-profile.json"
    vectors_path = phase_dir / "freed-id" / "conformance-vectors.json"
    if profile_path.is_file() and vectors_path.is_file():
        report = run_vectors(load_json(profile_path), load_json(vectors_path)["vectors"])
        if not report["profile_valid"] or not report["all_matched"]:
            issue("freed-id", "conformance_failure", json.dumps(report["profile_issues"]))

    board_path = phase_dir / "stage20" / "evidence-board.json"
    if board_path.is_file():
        board = load_json(board_path)
        required_claim = {"claim_id", "claim", "grade", "state", "evidence", "owner", "review_date", "rejection_or_promotion_condition"}
        for index, claim in enumerate(board.get("claims", [])):
            missing = required_claim - claim.keys()
            if missing:
                issue(f"stage20.claims[{index}]", "incomplete_evidence_claim", str(sorted(missing)))
        if any(claim.get("grade") == "E4" and "GMUT" in claim.get("claim", "") for claim in board.get("claims", [])):
            issue("stage20/evidence-board.json", "unsupported_e4_gmut", "no unique GMUT claim has independent reproduction")

    proposals_path = phase_dir / "next-ten-proposals.json"
    if proposals_path.is_file() and len(load_json(proposals_path).get("proposals", [])) != 10:
        issue("next-ten-proposals.json", "proposal_count", "expected ten proposals")

    overview_path = phase_dir / "v641-v1-integrated-overview.md"
    if overview_path.is_file() and len(overview_path.read_text(encoding="utf-8").split()) < 1800:
        issue("v641-v1-integrated-overview.md", "overview_too_short", "overview must exceed 1800 words")

    for path in phase_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".docx"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(phase_dir).as_posix()
        if LOCAL_PATH.search(text):
            issue(rel, "local_absolute_path", "portable artifact contains a local absolute path")
        for name, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                issue(rel, name, "private or raw task material pattern detected")

    if final:
        checklist_path = phase_dir / "complete-incomplete-checklist.json"
        if checklist_path.is_file() and load_json(checklist_path).get("state") != "LOCAL_CLOSE_COMPLETE_EXTERNAL_GAPS_OPEN":
            issue("complete-incomplete-checklist.json", "final_state_missing", "checklist is not locally closed")

    return {
        "schema": "ghc.family.phase-validation-report.v1",
        "phase": phase_dir.name,
        "mode": "final" if final else "core",
        "valid": not issues,
        "issue_count": len(issues),
        "issues": issues,
        "boundary": "local_artifact_validation_not_external_scientific_legal_or_security_certification",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase_dir", type=Path)
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase_dir = args.phase_dir.resolve()
    repo_root = args.repo_root.resolve() if args.repo_root else phase_dir.parents[2]
    report = validate_phase(phase_dir, repo_root, final=args.final)
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
