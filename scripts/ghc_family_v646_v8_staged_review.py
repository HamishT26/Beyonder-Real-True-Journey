#!/usr/bin/env python3
"""Exact Git-index review for Ilyra v646-v8 evidence and final surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v646_v8_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/ilyra-fen/v646-v8")
PHASE = ROOT / PHASE_REL
X1_COMMIT = "37c0e57d82fa8826d891a5b39f1fcb8ce0812a4a"
X1_FROZEN = {
    "docs/ilyra-fen/v646-v8/x1-proposals.json",
    "docs/ilyra-fen/v646-v8/approval-packets/x1-approval-portfolio.json",
    "docs/ilyra-fen/v646-v8/approval-packets/x1-protected-packet-register.json",
    "docs/ilyra-fen/v646-v8/prototypes/x1-candidate-plan.json",
    "docs/ilyra-fen/v646-v8/prototypes/x1-skill-runner-plan.json",
    "docs/ilyra-fen/v646-v8/maintenance/x1-clean-refine-plan.json",
    "docs/ilyra-fen/v646-v8/sources/source-ledger.json",
    "docs/ilyra-fen/v646-v8/provenance/proposal-collision-audit.json",
}
PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
    "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
    "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_[a-z0-9_]{6,})", re.I),
    "session_transcript_or_stream": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
}


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def staged_paths() -> list[str]:
    output = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], cwd=ROOT, text=True, encoding="utf-8")
    return sorted({line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()})


def index_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{relative}"], cwd=ROOT)


def commit_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)


def allowed(relative: str) -> bool:
    if relative.startswith(PHASE_REL.as_posix() + "/"):
        return True
    if relative in {f"scripts/{name}" for name in d.RUNNER_TITLES}:
        return True
    if relative.startswith("scripts/ghc_family_v646_v8") or relative.startswith("scripts/build_ghc_family_v646_v8"):
        return relative.endswith(".py")
    return relative in {"tests/test_ghc_family_v646_v8.py", "tests/test_ghc_family_v646_v8_closeout.py"}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    candidates = []
    confirmed = []
    for relative in paths:
        raw = index_bytes(relative)
        for class_name, pattern in PATTERNS.items():
            count = len(list(pattern.finditer(raw)))
            if not count:
                continue
            disposition = "unresolved_payload_candidate"
            if relative.endswith(("ghc_family_v646_v8_staged_review.py", "ghc_family_v646_v8_validation_runner.py")) and class_name in {"private_callable_identifier", "session_transcript_or_stream"}:
                disposition = "scanner_definition_candidate"
            elif class_name == "private_callable_identifier" and b"browser_diversity_evaluation" in raw and relative in {
                "docs/ilyra-fen/v646-v8/accessibility/carousel-motion-contract.json",
                "scripts/ghc_family_v646_v8_runtime.py",
            }:
                disposition = "semantic_accessibility_field_candidate"
            elif class_name == "private_callable_identifier" and b"browser_diversity_evaluation" in raw and relative in {
                "docs/ilyra-fen/v646-v8/method-flow/v6468-m11-method-record.json",
                "docs/ilyra-fen/v646-v8/method-flow/method-flow-state.json",
            }:
                disposition = "retained_scanner_incident_candidate"
            row = {"path": relative, "class": class_name, "count": count, "disposition": disposition}
            candidates.append(row)
            if disposition == "unresolved_payload_candidate":
                confirmed.append(row)
    return {
        "files_scanned": len(paths),
        "pattern_classes": len(PATTERNS),
        "candidate_hits": candidates,
        "candidate_hit_count": sum(row["count"] for row in candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": sum(row["count"] for row in confirmed),
    }


def structural(paths: list[str], stage: str) -> list[str]:
    issues = []
    if not paths:
        issues.append("no staged paths")
    outside = [path for path in paths if not allowed(path)]
    if outside:
        issues.append(f"out-of-scope staged paths: {outside}")
    frozen_changed = sorted(X1_FROZEN & set(paths))
    if frozen_changed:
        issues.append(f"x1 frozen paths changed: {frozen_changed}")
    for relative in X1_FROZEN:
        try:
            raw = commit_bytes(X1_COMMIT, relative)
            if not raw:
                issues.append(f"x1 frozen blob empty: {relative}")
        except subprocess.CalledProcessError:
            issues.append(f"x1 frozen blob missing: {relative}")
    if stage == "evidence":
        validation = read_json("validation/evidence-validation-runner-summary.json")
        if validation.get("result") != "pass":
            issues.append("current evidence validation is not pass")
        if read_json("prototypes/skill-build-use-receipt.json").get("result") != "pass":
            issues.append("skill receipt is not pass")
        if read_json("prototypes/runner-build-use-receipt.json").get("result") != "pass":
            issues.append("runner receipt is not pass")
        if read_json("phase-truth.json").get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
            issues.append("Stage 20 verdict invalid")
    if stage == "final":
        if read_json("closeout-receipt.json").get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
            issues.append("closeout verdict invalid")
        if read_json("orchestration/final-route-gate.json").get("state") != "HELD_UNTIL_POST_COMMIT_VALIDATION":
            issues.append("terminal route was not held for post-commit validation")
    return issues


def write_receipts(paths: list[str], stage: str, structural_issues: list[str]) -> tuple[str, str]:
    review_name = f"validation/{stage}-staged-review.json"
    manifest_name = f"validation/{stage}-staged-manifest.json"
    review_rel = (PHASE_REL / review_name).as_posix()
    manifest_rel = (PHASE_REL / manifest_name).as_posix()
    expected = sorted(set(paths) | {review_rel, manifest_rel})
    entries = [{"path": path, "sha256": hashlib.sha256(index_bytes(path)).hexdigest()} for path in expected if path not in {review_rel, manifest_rel}]
    json_issues = []
    parsed = 0
    for row in entries:
        if row["path"].endswith(".json"):
            try:
                json.loads(index_bytes(row["path"]).decode("utf-8"))
                parsed += 1
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": row["path"], "error": str(exc)})
    privacy = privacy_scan([row["path"] for row in entries])
    manifest = {
        "schema": f"ghc.family.v646-v8.{stage}-staged-manifest.v1",
        "hash_domain": "git_index_blob",
        "entries": entries,
        "entry_count": len(entries),
        "declared_self_exclusions": sorted({review_rel, manifest_rel}),
        "expected_staged_paths": expected,
        "expected_staged_path_count": len(expected),
    }
    review = {
        "schema": f"ghc.family.v646-v8.{stage}-staged-review.v1",
        "stage": stage,
        "staged_paths": expected,
        "staged_path_count": len(expected),
        "json_blobs_parsed": parsed,
        "json_issues": json_issues,
        "structural_issues": structural_issues,
        "privacy": privacy,
        "x1_commit": X1_COMMIT,
        "x1_frozen_path_changes": sorted(X1_FROZEN & set(paths)),
        "result": "pass" if not structural_issues and not json_issues and privacy["confirmed_hit_count"] == 0 else "fail",
        "boundary": d.TRUTH_BOUNDARY,
    }
    (PHASE / manifest_name).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (PHASE / review_name).write_text(json.dumps(review, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return review_rel, manifest_rel


def check_receipts(paths: list[str], stage: str) -> list[str]:
    issues = []
    review = read_json(f"validation/{stage}-staged-review.json")
    manifest = read_json(f"validation/{stage}-staged-manifest.json")
    if review.get("staged_paths") != paths or manifest.get("expected_staged_paths") != paths:
        issues.append("staged path set differs from receipt")
    for entry in manifest.get("entries", []):
        if hashlib.sha256(index_bytes(entry["path"])).hexdigest() != entry.get("sha256"):
            issues.append(f"staged manifest mismatch: {entry['path']}")
    if review.get("result") != "pass" or review.get("privacy", {}).get("confirmed_hit_count") != 0:
        issues.append("staged review is not a zero-confirmed-hit pass")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=["evidence", "final"], required=True)
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--check-receipts", action="store_true")
    args = parser.parse_args()
    paths = staged_paths()
    issues = structural(paths, args.stage)
    if args.write_receipts:
        write_receipts(paths, args.stage, issues)
        persisted = read_json(f"validation/{args.stage}-staged-review.json")
        if persisted.get("result") != "pass":
            issues.append("written staged review result is not pass")
    if args.check_receipts:
        issues.extend(check_receipts(paths, args.stage))
    print(json.dumps({"stage": args.stage, "staged_paths": len(paths), "issues": issues, "issue_count": len(issues), "result": "pass" if not issues else "fail"}, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
