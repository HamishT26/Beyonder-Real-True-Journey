#!/usr/bin/env python3
"""Exact Git-index review for Eiren v647-v5 evidence and closeout surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v647_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/eiren-kestrel/v647-v5")
PHASE = ROOT / PHASE_REL
X1_COMMIT = "d69257c1922407637db3bb4933d426d70a27e4bd"
X1_FROZEN = {
    "docs/eiren-kestrel/v647-v5/x1-proposals.json",
    "docs/eiren-kestrel/v647-v5/approval-packets/x1-approval-portfolio.json",
    "docs/eiren-kestrel/v647-v5/prototypes/x1-skill-runner-plan.json",
    "docs/eiren-kestrel/v647-v5/maintenance/x1-clean-refine-plan.json",
    "docs/eiren-kestrel/v647-v5/sources/source-ledger.json",
    "docs/eiren-kestrel/v647-v5/provenance/prior-proposal-collision-audit.json",
    "docs/eiren-kestrel/v647-v5/provenance/prior-portfolio-collision-audit.json",
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
    exact = {
        "scripts/build_ghc_family_v647_v5_evidence.py",
        "scripts/build_ghc_family_v647_v5_closeout.py",
        "scripts/ghc_family_v647_v5_runtime.py",
        "scripts/ghc_family_v647_v5_skill_runner.py",
        "scripts/ghc_family_v647_v5_portfolio_runner.py",
        "scripts/ghc_family_v647_v5_validation_runner.py",
        "scripts/ghc_family_v647_v5_staged_review.py",
        "scripts/ghc_family_v647_v5_exact_head_audit.py",
        "scripts/ghc_family_v647_v5_definitions.py",
        "scripts/ghc_family_priority_backpressure_tribunal.py",
        "scripts/ghc_family_adm_constraint_obligations.py",
        "scripts/ghc_family_pantheon_plus_zero_row.py",
        "scripts/ghc_family_library_digital_handover.py",
        "scripts/ghc_family_oauth_par_profile.py",
        "scripts/ghc_family_git_protocol_v2_tribunal.py",
        "scripts/ghc_family_sortable_table_audit.py",
        "scripts/ghc_family_helmholtz_domain.py",
        "scripts/ghc_family_conformal_prediction_board.py",
        "tests/test_ghc_family_v647_v5.py",
        "tests/test_ghc_family_v647_v5_x1.py",
        "tests/test_ghc_family_v647_v5_closeout.py",
    }
    return relative in exact


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Documents|AppData)[\\/]", re.I),
        "credential_material": re.compile(rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer\s+[A-Za-z0-9._~-]{16,})", re.I),
        "private_callable_identifier": re.compile(rb"\b(?:mcp__|codex_app__|browser_[a-z0-9_]{6,})", re.I),
        "session_transcript_or_stream": re.compile(rb"(?:sessions[\\/][0-9]{4}[\\/]|rollout-[0-9]{4}|session[_ -]?stream|raw transcript)", re.I),
    }
    candidates = []
    confirmed = []
    for relative in paths:
        raw = index_bytes(relative)
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(raw))
            if not matches:
                continue
            disposition = "unresolved_payload_candidate"
            if relative.endswith(("ghc_family_v647_v5_staged_review.py", "ghc_family_v647_v5_validation_runner.py", "ghc_family_v647_v5_exact_head_audit.py")) and class_name in {"private_callable_identifier", "session_transcript_or_stream"}:
                disposition = "scanner_definition_candidate"
            elif relative.endswith("ghc_family_v647_v5_definitions.py") and class_name == "session_transcript_or_stream":
                disposition = "privacy_exclusion_policy_candidate"
            row = {"path": relative, "class": class_name, "count": len(matches), "disposition": disposition}
            candidates.append(row)
            if disposition == "unresolved_payload_candidate":
                confirmed.append(row)
    return {
        "files_scanned": len(paths), "pattern_classes": len(patterns), "candidate_hits": candidates,
        "candidate_hit_count": sum(row["count"] for row in candidates),
        "confirmed_hits": confirmed, "confirmed_hit_count": sum(row["count"] for row in confirmed),
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
    seal = read_json("reproduction/x1-content-seal.json")
    for entry in seal.get("frozen_paths", []):
        relative = (PHASE_REL / entry["path"]).as_posix()
        actual = hashlib.sha256(commit_bytes(X1_COMMIT, relative)).hexdigest()
        if actual != entry.get("sha256"):
            issues.append(f"x1 commit seal mismatch: {relative}")
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
    if stage == "closeout":
        if read_json("closeout-receipt.json").get("exact_final_head_validation") != "required_after_commit":
            issues.append("closeout prematurely claims exact final validation")
        if read_json("final-validation-record.json").get("named_local_only_replay") != "required_after_commit":
            issues.append("final protocol prematurely claims named replay")
        full = read_json("validation/full-suite-validation.json")
        if full.get("result") != "pass" or full.get("tests", {}).get("unexpected_failure_events"):
            issues.append("full-suite eligible validation invalid")
        manifest = read_json("validation/final-owner-manifest.json")
        indexed = {
            line for line in subprocess.check_output(["git", "ls-files", PHASE_REL.as_posix() + "/"], cwd=ROOT, text=True, encoding="utf-8").splitlines() if line
        }
        exclusions = set(manifest.get("declared_self_exclusions", []))
        entry_paths = {row["path"] for row in manifest.get("entries", [])}
        if indexed - entry_paths != exclusions & indexed:
            issues.append(f"final owner manifest coverage mismatch: {sorted((indexed - entry_paths) ^ (exclusions & indexed))}")
        for entry in manifest.get("entries", []):
            if hashlib.sha256(index_bytes(entry["path"])).hexdigest() != entry.get("sha256"):
                issues.append(f"final owner manifest mismatch: {entry['path']}")
    return issues


def write_receipts(paths: list[str], stage: str, issues: list[str]) -> tuple[str, str]:
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
        "schema": f"ghc.family.v647-v5.{stage}-staged-manifest.v1", "hash_domain": "git_index_blob",
        "entries": entries, "entry_count": len(entries), "declared_self_exclusions": sorted({review_rel, manifest_rel}),
        "expected_staged_paths": expected, "expected_staged_path_count": len(expected),
    }
    review = {
        "schema": f"ghc.family.v647-v5.{stage}-staged-review.v1", "stage": stage,
        "staged_paths": expected, "staged_path_count": len(expected), "json_blobs_parsed": parsed,
        "json_issues": json_issues, "structural_issues": issues, "privacy": privacy,
        "x1_commit": X1_COMMIT, "x1_frozen_path_changes": sorted(X1_FROZEN & set(paths)),
        "result": "pass" if not issues and not json_issues and privacy["confirmed_hit_count"] == 0 else "fail",
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["evidence", "closeout"], required=True)
    parser.add_argument("--write-receipts", action="store_true")
    parser.add_argument("--check-receipts", action="store_true")
    args = parser.parse_args()
    paths = staged_paths()
    issues = structural(paths, args.stage)
    if args.write_receipts:
        write_receipts(paths, args.stage, issues)
    if args.check_receipts:
        issues.extend(check_receipts(paths, args.stage))
    print(json.dumps({"stage": args.stage, "staged_paths": len(paths), "issues": issues, "issue_count": len(issues), "result": "pass" if not issues else "fail"}, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
