#!/usr/bin/env python3
"""Review Eiren v647-v5 x1 structure and exact staged Git blobs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/eiren-kestrel/v647-v5")
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
        cwd=ROOT, text=True, encoding="utf-8",
    )
    return sorted({line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()})


def working_paths() -> list[str]:
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT, text=True, encoding="utf-8",
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


def content(relative: str, staged: bool) -> bytes:
    return index_bytes(relative) if staged else (ROOT / relative).read_bytes()


def privacy_scan(paths: list[str], staged: bool) -> dict[str, Any]:
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
        if not (relative.startswith(PHASE_REL.as_posix() + "/") or relative.startswith("scripts/") or relative.startswith("tests/")):
            continue
        try:
            raw = content(relative, staged)
        except (OSError, subprocess.CalledProcessError):
            continue
        scanned += 1
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(raw))
            if not matches:
                continue
            disposition = "unresolved_payload_candidate"
            if relative.endswith("ghc_family_v647_v5_x1_review.py") and class_name in {"private_callable_identifier", "session_transcript_or_stream"}:
                disposition = "scanner_definition_candidate"
            elif class_name == "session_transcript_or_stream" and relative.endswith("ghc_family_v647_v5_definitions.py"):
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


def structural_review(staged: bool) -> list[str]:
    issues: list[str] = []
    proposals = read_json("x1-proposals.json")
    required = {
        "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure",
        "approval_class", "execution_lane", "current_primary_or_official_source_needs",
        "concrete_artifacts", "test_falsifier_or_acceptance_gate", "rollback_or_recovery",
        "protected_gates", "expected_disposition", "novelty_against_510_frozen_proposals",
    }
    if proposals.get("freeze_stage") != "x1_only" or proposals.get("x2_execution_present") is not False:
        issues.append("x1 phase or x2 absence marker invalid")
    if (proposals.get("prior_frozen_proposal_count"), proposals.get("new_frozen_proposal_count"), proposals.get("frozen_chain_count_after_x1")) != (510, 10, 520):
        issues.append("proposal chain count invalid")
    rows = proposals.get("proposals", [])
    if [row.get("proposal_id") for row in rows] != [f"V6475-P{i:02d}" for i in range(1, 11)]:
        issues.append("proposal identifiers invalid")
    for row in rows:
        missing = sorted(key for key in required if not row.get(key))
        if missing:
            issues.append(f"{row.get('proposal_id')} missing {missing}")
    expected = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    if Counter(row.get("expected_disposition") for row in rows) != expected:
        issues.append("expected outcome distribution invalid")

    index = read_json("provenance/frozen-chain-proposal-index.json")
    if index.get("count") != 510 or len(index.get("prior_proposals", [])) != 510:
        issues.append("prior proposal index invalid")
    collision = read_json("provenance/prior-proposal-collision-audit.json")
    if collision.get("prior_count") != 510 or collision.get("exact_collision_count") != 0 or collision.get("valid") is not True:
        issues.append("proposal collision audit invalid")
    portfolio_collision = read_json("provenance/prior-portfolio-collision-audit.json")
    if portfolio_collision.get("exact_collision_count") != 0 or portfolio_collision.get("within_current_duplicates") or portfolio_collision.get("valid") is not True:
        issues.append("portfolio collision audit invalid")

    approval = read_json("approval-packets/x1-approval-portfolio.json")
    plan = read_json("prototypes/x1-skill-runner-plan.json")
    cleanup = read_json("maintenance/x1-clean-refine-plan.json")
    counts = (approval.get("safe_now_count"), approval.get("candidate_count"), plan.get("skill_count"), plan.get("runner_count"), cleanup.get("task_count"))
    if counts != (30, 20, 20, 10, 30):
        issues.append(f"portfolio counts invalid: {counts}")
    if (approval.get("exact_approval_count"), approval.get("blocked_count")) != (10, 5):
        issues.append("exact or blocked portfolio count invalid")
    portfolio_items = approval.get("safe_now", []) + approval.get("candidates", []) + approval.get("exact_approval", []) + approval.get("blocked", []) + cleanup.get("tasks", [])
    if any(item.get("x1_state") != "preregistered_no_completion_credit" or item.get("x2_completion_credit") is not False for item in portfolio_items):
        issues.append("portfolio contains x2 completion credit")
    if any(item.get("built") or item.get("validated") or item.get("invoked") for item in plan.get("skills", []) + plan.get("runners", [])):
        issues.append("skill or runner plan contains x2 build credit")

    negatives = read_json("validation/x1-operational-negatives.json")
    expected_negatives = len(d.X1_OPERATIONAL_NEGATIVES)
    if negatives.get("count") != expected_negatives or negatives.get("observed_effective_after_x1") != 3493 + expected_negatives or negatives.get("failure_erasure_count") != 0:
        issues.append("x1 operational negative accounting invalid")
    method = read_json("method-flow/method-flow-state.json")
    method_counts = method.get("counts", {})
    witness = method_counts.get("witness_results", {})
    if method_counts.get("methods") != expected_negatives or witness != {"fail": expected_negatives, "pass": expected_negatives}:
        issues.append("Method Flow count or witness parity invalid")
    if any(row.get("recommendation_state") != "preferred" for row in method.get("methods", [])):
        issues.append("Method Flow method is not preferred after bounded pass")

    source = read_json("sources/source-ledger.json")
    if source.get("source_count") != 20 or any(row.get("status") not in {"current", "stable", "draft", "watch"} for row in source.get("sources", [])):
        issues.append("source ledger invalid")
    if source.get("real_rows") != 0 or source.get("real_people_or_operations") != 0 or source.get("real_keys_or_tokens") != 0 or source.get("authority_delegated") is not False:
        issues.append("source ledger crosses x1 boundary")
    route = read_json("orchestration/terminal-route-plan.json")
    if route.get("current_state") != "PREPARED_NOT_SENT" or route.get("send_count") != 0 or route.get("target_title") != "Ilyra Fen":
        issues.append("terminal route state invalid")
    update = read_json("orchestration/phase-update.json")
    if update.get("x2_started") is not False or update.get("no_task_creation") is not True or update.get("no_delegation") is not True:
        issues.append("orchestration x1 boundary invalid")
    for relative in ("x2-proposal-ledger.json", "phase-truth.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"):
        if (PHASE / relative).exists():
            issues.append(f"x2 or closeout artifact present during x1: {relative}")

    seal = read_json("reproduction/x1-content-seal.json")
    if seal.get("path_count") != 7 or seal.get("x2_execution_present") is not False:
        issues.append("x1 content seal metadata invalid")
    for entry in seal.get("frozen_paths", []):
        relative = (PHASE_REL / entry["path"]).as_posix()
        actual = hashlib.sha256(content(relative, staged)).hexdigest()
        if actual != entry.get("sha256"):
            issues.append(f"x1 content seal mismatch: {entry['path']}")
    return issues


def write_receipts(paths: list[str], staged: bool, issues: list[str]) -> None:
    expected = sorted(set(paths) | {REVIEW_REL.as_posix(), MANIFEST_REL.as_posix()})
    excluded = {REVIEW_REL.as_posix(), MANIFEST_REL.as_posix()}
    entries = [
        {"path": relative, "sha256": hashlib.sha256(content(relative, staged)).hexdigest()}
        for relative in expected if relative not in excluded
    ]
    privacy = privacy_scan([row["path"] for row in entries], staged)
    manifest = {
        "schema": "ghc.family.v647-v5.x1-staged-manifest.v1",
        "hash_domain": "git_index_blob" if staged else "working_tree_bytes",
        "entries": entries, "entry_count": len(entries),
        "declared_self_exclusions": sorted(excluded),
        "expected_staged_paths": expected, "expected_staged_path_count": len(expected),
    }
    review = {
        "schema": "ghc.family.v647-v5.x1-staged-review.v1",
        "review_domain": "git_index_blob" if staged else "working_tree_bytes",
        "staged_paths": expected, "staged_path_count": len(expected),
        "structural_issue_count": len(issues), "structural_issues": issues,
        "privacy": privacy, "x2_execution_present": False,
        "result": "pass" if not issues and privacy["confirmed_hit_count"] == 0 else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    (ROOT / MANIFEST_REL).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / MANIFEST_REL).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (ROOT / REVIEW_REL).write_text(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def validate_receipts(paths: list[str]) -> list[str]:
    issues: list[str] = []
    review = read_json("validation/x1-staged-review.json")
    manifest = read_json("validation/x1-staged-manifest.json")
    if review.get("staged_paths") != paths or manifest.get("expected_staged_paths") != paths:
        issues.append("staged path set differs from committed receipt")
    if manifest.get("hash_domain") != "git_index_blob":
        issues.append("manifest hash domain is not git_index_blob")
    for entry in manifest.get("entries", []):
        if hashlib.sha256(index_bytes(entry["path"])).hexdigest() != entry.get("sha256"):
            issues.append(f"staged manifest mismatch: {entry['path']}")
    if review.get("result") != "pass" or review.get("privacy", {}).get("confirmed_hit_count") != 0:
        issues.append("staged review is not a zero-confirmed-hit pass")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--check-receipts", action="store_true")
    args = parser.parse_args()
    issues = structural_review(args.staged)
    paths = staged_paths() if args.staged else working_paths()
    if args.write_receipts:
        write_receipts(paths, args.staged, issues)
    if args.check_receipts:
        issues.extend(validate_receipts(paths))
    result = {
        "phase": d.PHASE, "domain": "git_index_blob" if args.staged else "working_tree",
        "changed_paths": len(paths), "checks": 36, "issues": issues, "issue_count": len(issues),
        "result": "pass" if not issues else "fail",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
