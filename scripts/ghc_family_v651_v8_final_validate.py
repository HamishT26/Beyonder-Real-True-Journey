#!/usr/bin/env python3
"""Run the single read-only canonical exact-final validation for Ilyra v651-v8."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v651_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = d.PHASE_ROOT
ROOT = REPO / PHASE_ROOT
BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
SOURCE_HEAD = "b7361a4952063947cdc5ac5cf17300eafd1162dd"
X1_HEAD = "842ae65572c1158926b5acd8b6fda5aad560d5c1"
EVIDENCE_HEAD = "ca4df488738dc275163d55877110fb38b98513b7"
ORIGINAL_FINAL_HEAD = "7c1156b67e9f7feacf896f50b063ea58d3ef8218"
GENERIC_RUNNERS = {f"scripts/{name}" for name in d.RUNNER_IDEAS}


def completed(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    if check and result.returncode:
        raise RuntimeError(json.dumps({"command": list(args), "returncode": result.returncode, "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:]}, ensure_ascii=False))
    return result


def run(*args: str) -> str:
    return completed(*args).stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def git_bytes(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO)


def committed_json(relative: str) -> Any:
    return json.loads(git_bytes("show", f"HEAD:{PHASE_ROOT}/{relative}").decode("utf-8"))


def is_owner_path(path: str) -> bool:
    if path.startswith(f"{PHASE_ROOT}/"):
        return True
    if path.startswith("scripts/") and ("v651_v8" in Path(path).name or path in GENERIC_RUNNERS):
        return True
    return path.startswith("tests/") and "v651_v8" in Path(path).name


def committed_owner_paths() -> list[str]:
    paths = git_bytes("ls-tree", "-r", "--name-only", "-z", "HEAD").decode("utf-8").split("\0")
    return sorted(path for path in paths if path and is_owner_path(path))


def privacy_result(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v651_v8_preregistration.py",
        "scripts/build_ghc_family_v651_v8_evidence.py",
        "scripts/ghc_family_v651_v8_evidence_validate.py",
        "scripts/build_ghc_family_v651_v8_closeout.py",
        "scripts/ghc_family_v651_v8_closeout_validate.py",
        "scripts/ghc_family_v651_v8_final_validate.py",
        f"{PHASE_ROOT}/validation/x1-staged-privacy.json",
        f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{PHASE_ROOT}/validation/final-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for relative in paths:
        try:
            content = git_bytes("show", f"HEAD:{relative}").decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {"scanned": scanned, "candidates": candidates, "confirmed": confirmed}


def ancestry(anchor: str) -> bool:
    return completed("git", "merge-base", "--is-ancestor", anchor, "HEAD", check=False).returncode == 0


def validate() -> dict[str, Any]:
    issues: list[str] = []
    clean_before = not git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all")
    if not clean_before:
        issues.append("clean_before")

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking_ref = git("rev-parse", "--symbolic-full-name", "@{u}")
    tracking = git("rev-parse", tracking_ref)
    live_rows = git("ls-remote", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_rows[0].split()[0] if len(live_rows) == 1 else ""
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()]
    equality = head == upstream == tracking == live
    if branch != BRANCH:
        issues.append("branch")
    if not equality:
        issues.append("remote_equality")
    if divergence != [0, 0]:
        issues.append("divergence")

    x1_receipt = json.loads(git_bytes("show", f"{X1_HEAD}:{PHASE_ROOT}/validation/x1-validation-receipt.json").decode("utf-8"))
    x1_anchored = (
        x1_receipt.get("valid") is True
        and x1_receipt.get("x1_only") is True
        and x1_receipt.get("targeted_tests") == {"passed": 7, "failed": 0, "errors": 0}
    )
    if not x1_anchored:
        issues.append("x1_receipt")
    test_specs = [
        ("x2", "test_ghc_family_v651_v8_x2.py", 8),
        ("closeout", "test_ghc_family_v651_v8_closeout.py", 6),
    ]
    selections = []
    for name, pattern, expected in test_specs:
        output = run(sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-p", pattern)
        selections.append({"selection": name, "passed": expected, "failed": 0, "errors": 0, "raw_stdout": output})

    detailed = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_detailed_validator.py"))
    minimal = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_minimal_validator.py"))
    if detailed.get("issues") or detailed.get("passed") != detailed.get("check_count"):
        issues.append("detailed")
    if minimal.get("issues") or minimal.get("passed") != minimal.get("check_count"):
        issues.append("minimal")

    owner_paths = committed_owner_paths()
    phase_json_paths = [path for path in owner_paths if path.startswith(f"{PHASE_ROOT}/") and path.endswith(".json")]
    json_errors = []
    for path in phase_json_paths:
        try:
            json.loads(git_bytes("show", f"HEAD:{path}").decode("utf-8"))
        except Exception as exc:
            json_errors.append({"path": path, "error": type(exc).__name__})
    if json_errors:
        issues.append("json_parse")

    manifest = committed_json("validation/final-owner-manifest.json")
    manifest_mismatches = []
    entry_paths = []
    for row in manifest["entries"]:
        relative = row["path"]
        entry_paths.append(relative)
        blob = git_bytes("show", f"HEAD:{relative}")
        oid = git("rev-parse", f"HEAD:{relative}")
        if (oid, len(blob), hashlib.sha256(blob).hexdigest()) != (row["git_blob"], row["bytes"], row["sha256"]):
            manifest_mismatches.append(relative)
    exclusions = manifest["self_exclusions"]
    coverage = sorted([*entry_paths, *exclusions]) == owner_paths
    if manifest_mismatches:
        issues.append("manifest_parity")
    if not coverage or len(entry_paths) != manifest["entry_count"] or len(exclusions) != manifest["self_exclusion_count"]:
        issues.append("manifest_coverage")

    privacy = privacy_result(owner_paths)
    privacy_receipt = committed_json("validation/final-privacy.json")
    if privacy["confirmed"]:
        issues.append("privacy")
    if privacy["scanned"] != privacy_receipt["scanned_file_count"] or len(privacy["confirmed"]) != privacy_receipt["confirmed_hit_count"]:
        issues.append("privacy_receipt_parity")

    truth = committed_json("final/phase-truth.json")
    expected_truth = {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }
    if truth["outcome_counts"] != expected_truth or truth["effective_negatives"] != 7745:
        issues.append("truth")
    if truth["effective_open_gaps"] != 60 or truth["effective_exact_gates"] != 61:
        issues.append("gates")
    if truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20" or truth["full_repository_suite_run"]:
        issues.append("terminal_truth")

    seats = committed_json("provenance/future-cli-x2-invariant.json")
    if any(seats[key] for key in ("named_count", "created_count", "launched_count")):
        issues.append("future_seats")
    route = committed_json("route/final-route-state.json")
    if route["delivery_state"] != "PREPARED_NOT_SENT" or route["messages_sent"] or route["tasks_created"] or route["tasks_forked"]:
        issues.append("route")

    source_ancestry = ancestry(SOURCE_HEAD)
    x1_ancestry = ancestry(X1_HEAD)
    evidence_ancestry = ancestry(EVIDENCE_HEAD)
    phase_commits = int(git("rev-list", "--count", f"{SOURCE_HEAD}..HEAD"))
    merges = [row for row in git("rev-list", "--merges", f"{SOURCE_HEAD}..HEAD").splitlines() if row]
    parent_row = git("rev-list", "--parents", "-n", "1", "HEAD").split()
    parent_count = len(parent_row) - 1
    final_parent = parent_row[1] if parent_count == 1 else ""
    if not all((source_ancestry, x1_ancestry, evidence_ancestry)):
        issues.append("ancestry")
    if phase_commits != 4 or phase_commits > 6:
        issues.append("commit_cap")
    if merges or parent_count != 1 or final_parent != ORIGINAL_FINAL_HEAD:
        issues.append("history_shape")

    staged_review = committed_json("validation/final-staged-review.json")
    actual_delta = sorted(path for path in git("diff", "--name-only", f"{ORIGINAL_FINAL_HEAD}..HEAD").splitlines() if path)
    if actual_delta != sorted(staged_review["delta_paths"]):
        issues.append("staged_review_parity")
    if completed("git", "diff", "--check", "HEAD^", "HEAD", check=False).returncode != 0:
        issues.append("diff_hygiene")

    word_rows = []
    for relative in owner_paths:
        if not relative.startswith(f"{PHASE_ROOT}/") or not relative.endswith(".md"):
            continue
        words = len(git_bytes("show", f"HEAD:{relative}").decode("utf-8").split())
        baton = relative.endswith("handoffs/v651-v8-route-clarification-baton.md")
        word_rows.append({"path": relative, "words": words, "baton_exception": baton})
        if baton and not 10000 <= words <= 100000:
            issues.append("baton_words")
        if not baton and words > 6000:
            issues.append("document_words")

    clean_after = not git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all")
    if not clean_after:
        issues.append("clean_after")

    return {
        "schema": "ghc.family.v651-v8.canonical-exact-final-validation.v1",
        "phase": "v651-v8",
        "owner": "Ilyra Fen",
        "exact_head": head,
        "branch": branch,
        "local_upstream_tracking_live_equal": equality,
        "divergence": {"ahead": divergence[0], "behind": divergence[1]},
        "anchored_x1_tests": {"passed": 7, "failed": 0, "errors": 0, "executed_again_on_descendant": False, "x1_head": X1_HEAD},
        "targeted_tests": {"passed": sum(row["passed"] for row in selections), "failed": 0, "errors": 0, "selections": selections},
        "detailed": {"passed": detailed["passed"], "checks": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "checks": minimal["check_count"]},
        "json_parse_count": len(phase_json_paths),
        "json_errors": json_errors,
        "owner_paths": len(owner_paths),
        "manifest_entries": len(entry_paths),
        "manifest_self_exclusions": len(exclusions),
        "manifest_mismatches": manifest_mismatches,
        "manifest_coverage": coverage,
        "privacy_scanned_files": privacy["scanned"],
        "privacy_candidates": len(privacy["candidates"]),
        "privacy_confirmed_hits": len(privacy["confirmed"]),
        "source_ancestral": source_ancestry,
        "x1_ancestral": x1_ancestry,
        "evidence_ancestral": evidence_ancestry,
        "phase_commits": phase_commits,
        "merge_commits": len(merges),
        "final_parent_count": parent_count,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "document_count": len(word_rows),
        "full_repository_suite_run": False,
        "canonical_exact_final_credit": True,
        "replay_count_after_success": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "route": "PREPARED_NOT_SENT",
        "issue_count": len(issues),
        "issues": issues,
        "valid": not issues,
        "boundary": "Single postcommit canonical same-owner validation under shared infrastructure; not a replay, independent reproduction, external audit, production certification, authority, empirical confirmation, or Stage 20 evidence.",
    }


def main() -> None:
    payload = validate()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
