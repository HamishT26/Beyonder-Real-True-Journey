#!/usr/bin/env python3
"""Review Sylven Arc v646-v6 x1 structure and exact staged Git blobs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v6_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sylven-arc/v646-v6")
PHASE = ROOT / PHASE_REL
REVIEW_REL = PHASE_REL / "validation/x1-staged-review.json"
MANIFEST_REL = PHASE_REL / "validation/x1-staged-manifest.json"


def read_json(relative: str | Path) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def index_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT)


def staged_paths() -> list[str]:
    output = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    return sorted({line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()})


def working_change_paths() -> list[str]:
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    rows: set[str] = set()
    for line in output.splitlines():
        if not line:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        rows.add(path.replace("\\", "/"))
    return sorted(rows)


def file_bytes(relative: str, staged: bool) -> bytes:
    return index_bytes(relative) if staged else (ROOT / relative).read_bytes()


def scan_privacy(paths: list[str], staged: bool) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
        "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
        "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_[a-z0-9_]{6,})", re.I),
        "session_transcript_or_stream": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
    }
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    scanned = 0
    for relative in paths:
        if not relative.startswith(PHASE_REL.as_posix() + "/") and not relative.startswith("scripts/") and not relative.startswith("tests/"):
            continue
        try:
            content = file_bytes(relative, staged)
        except (OSError, subprocess.CalledProcessError):
            continue
        scanned += 1
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(content))
            if not matches:
                continue
            disposition = "unresolved_payload_candidate"
            if relative.endswith("ghc_family_v646_v6_x1_review.py") and class_name in {"private_callable_identifier", "session_transcript_or_stream"}:
                disposition = "scanner_definition_candidate"
            elif class_name == "session_transcript_or_stream" and relative in {
                "scripts/build_ghc_family_v646_v6_preregistration.py",
                "docs/sylven-arc/v646-v6/orchestration/terminal-route-plan.json",
            }:
                disposition = "privacy_exclusion_policy_candidate"
            row = {"path": relative, "class": class_name, "count": len(matches), "disposition": disposition}
            candidates.append(row)
            if disposition == "unresolved_payload_candidate":
                confirmed.append(row)
    return {
        "files_scanned": scanned,
        "pattern_classes": len(patterns),
        "candidate_hits": candidates,
        "candidate_hit_count": sum(row["count"] for row in candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": sum(row["count"] for row in confirmed),
    }


def structural_review() -> list[str]:
    issues: list[str] = []
    proposals = read_json("x1-proposals.json")
    required = {
        "proposal_id",
        "title",
        "mission_surface",
        "hypothesis",
        "null_or_failure",
        "approval_class",
        "execution_lane",
        "current_primary_or_official_source_needs",
        "concrete_artifacts",
        "test_falsifier_or_acceptance_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
        "novelty_against_440_frozen_proposals",
    }
    if proposals.get("freeze_stage") != "x1_only" or proposals.get("x2_execution_present") is not False:
        issues.append("x1 phase marker or x2 absence marker invalid")
    if proposals.get("prior_frozen_proposal_count") != 440 or proposals.get("frozen_chain_count_after_x1") != 450:
        issues.append("proposal chain count invalid")
    rows = proposals.get("proposals", [])
    if len(rows) != 10:
        issues.append("proposal count is not ten")
    if [row.get("proposal_id") for row in rows] != [f"V6466-P{i:02d}" for i in range(1, 11)]:
        issues.append("proposal identifiers are not exact and sequential")
    for row in rows:
        missing = sorted(key for key in required if not row.get(key))
        if missing:
            issues.append(f"{row.get('proposal_id')} missing {missing}")
        if row.get("expected_disposition") not in d.OUTCOME_CLASSES:
            issues.append(f"{row.get('proposal_id')} has invalid disposition")
    expected = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    if Counter(row.get("expected_disposition") for row in rows) != expected:
        issues.append("expected disposition distribution invalid")

    collision = read_json("provenance/prior-proposal-collision-audit.json")
    if collision.get("prior_count") != 440 or collision.get("exact_collision_count") != 0 or collision.get("valid") is not True:
        issues.append("proposal collision audit invalid")
    portfolio_collision = read_json("provenance/prior-portfolio-collision-audit.json")
    if portfolio_collision.get("exact_collisions") or portfolio_collision.get("within_current_duplicates") or portfolio_collision.get("valid") is not True:
        issues.append("portfolio collision audit invalid")
    approval = read_json("approval-packets/x1-approval-portfolio.json")
    plan = read_json("prototypes/x1-skill-runner-plan.json")
    cleanup = read_json("maintenance/x1-clean-refine-plan.json")
    counts = (
        approval.get("safe_now_count"),
        approval.get("candidate_count"),
        plan.get("skill_count"),
        plan.get("runner_count"),
        cleanup.get("task_count"),
    )
    if counts != (30, 20, 20, 10, 30):
        issues.append(f"portfolio counts invalid: {counts}")
    if any(item.get("x1_state") != "preregistered_no_completion_credit" for item in approval.get("safe_now", []) + approval.get("candidates", []) + cleanup.get("tasks", [])):
        issues.append("portfolio contains x2 completion credit")
    if any(item.get("built") or item.get("validated") or item.get("invoked") for item in plan.get("skills", [])):
        issues.append("x1 skill plan contains x2 build credit")
    if any(item.get("built") or item.get("invoked") for item in plan.get("runners", [])):
        issues.append("x1 runner plan contains x2 build credit")

    negative = read_json("validation/x1-operational-negatives.json")
    if negative.get("count") != 10 or negative.get("observed_effective_after_x1") != 2894 or negative.get("failure_erasure_count") != 0:
        issues.append("x1 operational negative accounting invalid")
    method = read_json("method-flow/method-flow-state.json")
    counts = method.get("counts", {})
    witness_results = counts.get("witness_results", {})
    if counts.get("methods") != 10 or witness_results.get("fail") != 10 or witness_results.get("pass") != 10:
        issues.append(f"Method Flow counts invalid: {counts}")
    if any(row.get("recommendation_state") != "preferred" for row in method.get("methods", [])):
        issues.append("Method Flow recovery not preferred after pass")

    source = read_json("sources/source-ledger.json")
    if any(row.get("status") not in {"current", "stable", "draft", "watch"} for row in source.get("sources", [])):
        issues.append("invalid source status")
    if source.get("real_rows") != 0 or source.get("real_people_or_operations") != 0 or source.get("real_keys_or_tokens") != 0 or source.get("authority_delegated") is not False:
        issues.append("source ledger crosses x1 boundary")
    route = read_json("orchestration/terminal-route-plan.json")
    if route.get("current_state") != "PREPARED_NOT_SENT" or route.get("send_count") != 0 or route.get("target_title") != "Eiren Kestrel":
        issues.append("terminal route state invalid")
    phase_update = read_json("orchestration/phase-update.json")
    if phase_update.get("x2_started") is not False or phase_update.get("no_task_creation") is not True or phase_update.get("no_delegation") is not True:
        issues.append("orchestration x1 boundary invalid")
    for forbidden in (
        PHASE / "x2-proposal-ledger.json",
        PHASE / "phase-truth.json",
        PHASE / "closeout-receipt.json",
        PHASE / "seal-receipt.json",
        PHASE / "final-validation-record.json",
    ):
        if forbidden.exists():
            issues.append(f"x2 or closeout artifact present during x1: {forbidden.name}")

    seal = read_json("reproduction/x1-content-seal.json")
    if seal.get("path_count") != 7 or seal.get("x2_execution_present") is not False:
        issues.append("x1 content seal metadata invalid")
    for entry in seal.get("frozen_paths", []):
        actual = hashlib.sha256((PHASE / entry["path"]).read_bytes()).hexdigest()
        if actual != entry.get("sha256"):
            issues.append(f"x1 content seal mismatch: {entry['path']}")
    return issues


def write_receipts(paths: list[str], staged: bool, structural_issues: list[str]) -> None:
    expected_paths = sorted(set(paths) | {REVIEW_REL.as_posix(), MANIFEST_REL.as_posix()})
    excluded = {REVIEW_REL.as_posix(), MANIFEST_REL.as_posix()}
    entries = []
    for relative in expected_paths:
        if relative in excluded:
            continue
        entries.append(
            {
                "path": relative,
                "sha256": hashlib.sha256(file_bytes(relative, staged)).hexdigest(),
            }
        )
    privacy = scan_privacy([row["path"] for row in entries], staged)
    manifest = {
        "schema": "ghc.family.v646-v6.x1-staged-manifest.v1",
        "hash_domain": "git_index_blob" if staged else "working_tree_bytes",
        "entries": entries,
        "entry_count": len(entries),
        "declared_self_exclusions": sorted(excluded),
        "expected_staged_paths": expected_paths,
        "expected_staged_path_count": len(expected_paths),
    }
    review = {
        "schema": "ghc.family.v646-v6.x1-staged-review.v1",
        "review_domain": "git_index_blob" if staged else "working_tree_bytes",
        "staged_paths": expected_paths,
        "staged_path_count": len(expected_paths),
        "structural_issue_count": len(structural_issues),
        "structural_issues": structural_issues,
        "privacy": privacy,
        "x2_execution_present": False,
        "result": "pass" if not structural_issues and privacy["confirmed_hit_count"] == 0 else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    MANIFEST_REL.parent.mkdir(parents=True, exist_ok=True)
    (ROOT / MANIFEST_REL).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (ROOT / REVIEW_REL).write_text(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def validate_receipts(paths: list[str]) -> list[str]:
    issues: list[str] = []
    review = read_json("validation/x1-staged-review.json")
    manifest = read_json("validation/x1-staged-manifest.json")
    if review.get("staged_paths") != paths:
        issues.append("x1 staged path set differs from committed review")
    if manifest.get("expected_staged_paths") != paths:
        issues.append("x1 staged path set differs from committed manifest")
    if manifest.get("hash_domain") != "git_index_blob":
        issues.append("x1 manifest hash domain is not git_index_blob")
    for entry in manifest.get("entries", []):
        actual = hashlib.sha256(index_bytes(entry["path"])).hexdigest()
        if actual != entry.get("sha256"):
            issues.append(f"x1 staged manifest mismatch: {entry['path']}")
    if review.get("result") != "pass" or review.get("privacy", {}).get("confirmed_hit_count") != 0:
        issues.append("x1 staged review receipt is not pass with zero confirmed hits")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--check-receipts", action="store_true")
    args = parser.parse_args()
    issues = structural_review()
    paths = staged_paths() if args.staged else working_change_paths()
    if args.write_receipts:
        write_receipts(paths, args.staged, issues)
    if args.check_receipts:
        issues.extend(validate_receipts(paths))
    result = {
        "phase": d.PHASE,
        "domain": "git_index_blob" if args.staged else "working_tree",
        "changed_paths": len(paths),
        "checks": 31,
        "issues": issues,
        "issue_count": len(issues),
        "result": "pass" if not issues else "fail",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
