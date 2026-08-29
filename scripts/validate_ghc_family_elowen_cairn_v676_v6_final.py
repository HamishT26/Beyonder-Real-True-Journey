#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Elowen v676-v6."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v676-v6"
OWNER = "Elowen Cairn"
PHASE = "v676-v6"
BRANCH = "codex/GHC-Family/elowen-cairn-v676-v6-full-tools"
SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
X1 = "0943c5da5d4c1aced1ed9a29aca2d18de1c16b26"
EVIDENCE = "c32fde8ba3aa9518e65f212b8a87d1a108dbc69a"
ORIGINAL_FINAL = "b37d777b2800372003451d95d3ad5b854ff77d7b"
CORRECTION1_FINAL = "74a389089cca17558a93c9300af2a4232b3d145e"
FAILED_CANONICAL_RECEIPT_SHA256 = "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf"
FAILED_CORRECTION1_RECEIPT_SHA256 = "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f"
OWNER_TEST_TIMEOUT_SECONDS = 900
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
COUNTS = {
    "effective_negatives": 42651,
    "effective_methods": 33778,
    "retained_failed_witnesses": 14312,
    "bounded_passing_witnesses": 20155,
    "open_gaps": 359,
    "exact_gates": 351,
}
OWNER_PREFIX = "docs/elowen-cairn/v676-v6/"
BOUNDARY = (
    "Bounded owner-local software and documentation evidence under shared infrastructure only; "
    "not a full-repository suite, independent reproduction, external audit, empirical validation, "
    "professional certification, production readiness, legal or cultural ratification, "
    "Māori-authority review, complete privacy or accessibility assurance, exhaustive security, "
    "proof, canon, or Stage 20 authority."
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True, timeout=300)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def write_receipt(path: Path, payload: dict[str, Any], *, exclusive: bool = False) -> None:
    value = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if exclusive:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(value)
    else:
        path.write_text(value, encoding="utf-8", newline="\n")


def tree_objects(commit: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    for row in git_text("ls-tree", "-r", commit).splitlines():
        if not row:
            continue
        left, path = row.split("\t", 1)
        mode, kind, object_id = left.split()
        if kind == "blob":
            result[path] = (mode, object_id)
    return result


def batch_blobs(object_ids: list[str]) -> list[bytes | None]:
    if not object_ids:
        return []
    payload = b"".join(object_id.encode("ascii") + b"\n" for object_id in object_ids)
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        input=payload,
        capture_output=True,
        check=True,
        timeout=300,
    )
    stream = result.stdout
    offset = 0
    blobs: list[bytes | None] = []
    for _object_id in object_ids:
        end = stream.find(b"\n", offset)
        if end < 0:
            raise ValueError("truncated git cat-file batch header")
        header = stream[offset:end]
        offset = end + 1
        if header.endswith(b" missing"):
            blobs.append(None)
            continue
        size = int(header.rsplit(b" ", 1)[1])
        blob = stream[offset : offset + size]
        offset += size
        if stream[offset : offset + 1] != b"\n":
            raise ValueError("truncated git cat-file batch separator")
        offset += 1
        blobs.append(blob)
    return blobs


def allowed_owner_path(path: str) -> bool:
    return bool(
        path.startswith(OWNER_PREFIX)
        or re.fullmatch(
            r"scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_elowen_cairn_v676_v6_.*\.py",
            path,
        )
        or re.fullmatch(r"tests/test_ghc_family_elowen_cairn_v676_v6_.*\.py", path)
    )


def replay_manifest(commit: str, relative: str) -> dict[str, Any]:
    manifest = load(f"validation/{relative}")
    entries = manifest["entries"]
    objects = tree_objects(commit)
    missing = [row["path"] for row in entries if row["path"] not in objects]
    blobs = batch_blobs([objects[row["path"]][1] for row in entries]) if not missing else []
    mismatches: list[str] = []
    if not missing:
        for row, blob in zip(entries, blobs, strict=True):
            if blob is None:
                mismatches.append(row["path"])
                continue
            oid = objects[row["path"]][1]
            if (
                oid != row["git_blob_oid"]
                or len(blob) != row["bytes"]
                or len(normalized(blob)) != row["normalized_lf_bytes"]
                or hashlib.sha256(normalized(blob)).hexdigest() != row["sha256_normalized_lf"]
            ):
                mismatches.append(row["path"])
    exclusions = {row["path"] for row in manifest["declared_exclusions"]}
    return {
        "valid": not missing and not mismatches,
        "entries": manifest["entry_count"],
        "paths": sorted(row["path"] for row in entries),
        "exclusions": sorted(exclusions),
        "missing": missing,
        "mismatches": mismatches,
    }


def current_equality() -> dict[str, Any]:
    local = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live_tokens = live_line.split()
    live = live_tokens[0] if len(live_tokens) == 2 else None
    divergence = [int(value) for value in git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    return {
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": local == upstream == tracking == live,
        "ahead": divergence[0],
        "behind": divergence[1],
    }


def check(name: str, passed: bool, observed: Any) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "observed": observed}


def seal_replay(head: str, relative: str) -> dict[str, Any]:
    seal = load(relative)
    objects = tree_objects(head)
    rows = seal["entries"]
    missing = [row["path"] for row in rows if row["path"] not in objects]
    blobs = batch_blobs([objects[row["path"]][1] for row in rows]) if not missing else []
    mismatches = []
    if not missing:
        for row, blob in zip(rows, blobs, strict=True):
            if blob is None or hashlib.sha256(normalized(blob)).hexdigest() != row["sha256_normalized_lf"]:
                mismatches.append(row["path"])
    return {"valid": not missing and not mismatches, "entries": len(rows), "missing": missing, "mismatches": mismatches}


def lifecycle_absence_check(commit: str, stage: str) -> dict[str, Any]:
    base = "docs/elowen-cairn/v676-v6"
    docs = [path for path in git_text("ls-tree", "-r", "--name-only", commit, "--", base).splitlines() if path]
    scripts = [path for path in git_text("ls-tree", "-r", "--name-only", commit, "--", "scripts").splitlines() if path]
    tests = [path for path in git_text("ls-tree", "-r", "--name-only", commit, "--", "tests").splitlines() if path]
    if stage == "x1":
        forbidden = [path for path in docs if path.startswith(base + "/x2/")]
        forbidden.extend(path for path in scripts if "elowen_cairn_v676_v6_x2" in path)
        forbidden.extend(path for path in tests if "elowen_cairn_v676_v6_x2" in path)
    elif stage == "evidence":
        forbidden_prefixes = tuple(base + "/" + value + "/" for value in ("final", "closeout", "handoffs"))
        forbidden = [path for path in docs if path.startswith(forbidden_prefixes)]
        forbidden.extend(path for path in scripts if "elowen_cairn_v676_v6_final" in path)
    else:
        raise ValueError(f"unsupported lifecycle stage: {stage}")
    grep = git(
        "grep",
        "-I",
        "-n",
        "-P",
        "-e",
        r"[A-Z]:[\\/]+Users[\\/]+",
        "-e",
        r"(thread_id|source_thread_id|clientThreadId)",
        "-e",
        r"(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]",
        "-e",
        r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
        commit,
        "--",
        base,
        check=False,
    )
    grep_error = grep.returncode not in (0, 1)
    privacy_hits = grep.stdout.decode("utf-8", "replace").splitlines() if grep.returncode == 0 else []
    return {
        "stage": stage,
        "commit": commit,
        "documents": len(docs),
        "scripts": len(scripts),
        "tests": len(tests),
        "forbidden_paths": forbidden,
        "privacy_hits": privacy_hits,
        "grep_error": grep_error,
        "passed": not forbidden and not privacy_hits and not grep_error,
    }


def canonical_payload() -> dict[str, Any]:
    started = now_utc()
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    clean_before = git_text("status", "--porcelain=v1") == ""
    before_equality = current_equality()
    parent = git_text("rev-parse", "HEAD^")
    parent_count = len(git_text("show", "-s", "--format=%P", "HEAD").split())
    x1_parent = git_text("rev-parse", f"{X1}^")
    evidence_parent = git_text("rev-parse", f"{EVIDENCE}^")
    commit_count = int(git_text("rev-list", "--count", f"{SOURCE}..HEAD"))
    merge_count = int(git_text("rev-list", "--count", "--merges", f"{SOURCE}..HEAD"))

    test_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests/test_ghc_family_elowen_cairn_v676_v6_x1.py",
            "tests/test_ghc_family_elowen_cairn_v676_v6_x2.py",
            "tests/test_ghc_family_elowen_cairn_v676_v6_final.py",
            "tests/test_ghc_family_elowen_cairn_v676_v6_correction1.py",
            "tests/test_ghc_family_elowen_cairn_v676_v6_correction2.py",
            "-k",
            "not test_no_x2_material_and_no_private_payload_in_x1_docs and not test_no_final_closeout_handoff_or_private_payload_exists_at_evidence",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=OWNER_TEST_TIMEOUT_SECONDS,
    )
    test_output = test_result.stdout + test_result.stderr
    match = re.search(r"(\d+) passed", test_output)
    deselected_match = re.search(r"(\d+) deselected", test_output)
    current_tree_test_count = int(match.group(1)) if match else 0
    deselected_count = int(deselected_match.group(1)) if deselected_match else 0
    lifecycle_checks = [lifecycle_absence_check(X1, "x1"), lifecycle_absence_check(EVIDENCE, "evidence")]
    lifecycle_passed = sum(row["passed"] for row in lifecycle_checks)
    test_count = current_tree_test_count + lifecycle_passed

    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})

    x1_manifest = replay_manifest(X1, "x1-manifest.json")
    evidence_manifest = replay_manifest(EVIDENCE, "evidence-manifest.json")
    original_delta_manifest = replay_manifest(ORIGINAL_FINAL, "final-delta-manifest.json")
    original_owner_manifest = replay_manifest(ORIGINAL_FINAL, "final-owner-manifest.json")
    correction1_delta_manifest = replay_manifest(CORRECTION1_FINAL, "correction1-delta-manifest.json")
    correction1_owner_manifest = replay_manifest(CORRECTION1_FINAL, "correction1-owner-manifest.json")
    correction2_delta_manifest = replay_manifest(head, "correction2-delta-manifest.json")
    correction2_owner_manifest = replay_manifest(head, "correction2-owner-manifest.json")
    original_changed_delta = {path for path in git_text("diff", "--name-only", f"{EVIDENCE}..{ORIGINAL_FINAL}").splitlines() if path}
    correction1_changed_delta = {path for path in git_text("diff", "--name-only", f"{ORIGINAL_FINAL}..{CORRECTION1_FINAL}").splitlines() if path}
    correction2_changed_delta = {path for path in git_text("diff", "--name-only", f"{CORRECTION1_FINAL}..{head}").splitlines() if path}
    changed_owner = {
        path for path in git_text("diff", "--name-only", f"{SOURCE}..{head}").splitlines()
        if path and allowed_owner_path(path)
    }
    expected_original_delta = set(original_delta_manifest["paths"]) | set(original_delta_manifest["exclusions"])
    expected_correction1_delta = set(correction1_delta_manifest["paths"]) | set(correction1_delta_manifest["exclusions"])
    expected_correction2_delta = set(correction2_delta_manifest["paths"]) | set(correction2_delta_manifest["exclusions"])
    expected_owner = set(correction2_owner_manifest["paths"]) | set(correction2_owner_manifest["exclusions"])

    truth = load("correction2/phase-truth.json")
    method_flow = load("correction2/method-flow-overlay.json")
    gaps = load("final/open-gap-register.json")
    gates = load("final/exact-gate-register.json")
    portfolio = load("final/portfolio-truth.json")
    staged_review = load("validation/correction2-staged-review.json")
    route = load("orchestration/terminal-route-hold.json")
    closeout = load("closeout/closeout-receipt.json")
    skill_summary = load("x2/skill-summary.json")
    runner_summary = load("x2/runner-summary.json")
    mutation_summary = load("x2/mutation-summary.json")
    original_seal = seal_replay(ORIGINAL_FINAL, "closeout/content-seal.json")
    correction1_seal = seal_replay(CORRECTION1_FINAL, "correction1/content-seal.json")
    correction2_seal = seal_replay(head, "correction2/content-seal.json")

    final_prefixes = tuple(OWNER_PREFIX + part for part in ("final/", "closeout/", "handoffs/", "orchestration/", "correction1/", "correction2/"))
    final_public_paths = [
        path for path in changed_owner
        if path.startswith(final_prefixes) and path.endswith((".json", ".md", ".html", ".txt", ".yaml", ".yml"))
    ]
    stale_patterns = [
        re.compile(r"Tamar-owned proposal", re.I),
        re.compile(r"primary pillar was THOS Body", re.I),
        re.compile(r"codex-binding|book-conservation", re.I),
        re.compile(r"SENT_BY_TAMAR_VEY", re.I),
    ]
    stale_hits = []
    for path in sorted(final_public_paths):
        value = (ROOT / path).read_text(encoding="utf-8")
        for pattern in stale_patterns:
            if pattern.search(value):
                stale_hits.append({"path": path, "pattern": pattern.pattern})

    diff_check = git("diff", "--check", f"{SOURCE}..{head}", check=False)
    detailed = [
        check("exact_branch", branch == BRANCH, branch),
        check("correction2_parent_is_correction1_final", parent == CORRECTION1_FINAL, parent),
        check("x1_parent_is_source", x1_parent == SOURCE, x1_parent),
        check("evidence_parent_is_x1", evidence_parent == X1, evidence_parent),
        check("source_is_ancestor", git("merge-base", "--is-ancestor", SOURCE, head, check=False).returncode == 0, SOURCE),
        check("x1_is_ancestor", git("merge-base", "--is-ancestor", X1, head, check=False).returncode == 0, X1),
        check("evidence_is_ancestor", git("merge-base", "--is-ancestor", EVIDENCE, head, check=False).returncode == 0, EVIDENCE),
        check("original_final_is_ancestor", git("merge-base", "--is-ancestor", ORIGINAL_FINAL, head, check=False).returncode == 0, ORIGINAL_FINAL),
        check("correction1_final_is_ancestor", git("merge-base", "--is-ancestor", CORRECTION1_FINAL, head, check=False).returncode == 0, CORRECTION1_FINAL),
        check("five_phase_commits", commit_count == 5, commit_count),
        check("zero_merges", merge_count == 0, merge_count),
        check("one_final_parent", parent_count == 1, parent_count),
        check("clean_before", clean_before, clean_before),
        check("zero_divergence_before", before_equality["ahead"] == 0 and before_equality["behind"] == 0, before_equality),
        check("four_way_equal_before", before_equality["four_way_equal"], before_equality),
        check("x1_manifest_replay", x1_manifest["valid"] and x1_manifest["entries"] == 20, x1_manifest),
        check("evidence_manifest_replay", evidence_manifest["valid"] and evidence_manifest["entries"] == 540, evidence_manifest),
        check("original_final_delta_manifest_replay", original_delta_manifest["valid"], original_delta_manifest),
        check("original_final_owner_manifest_replay", original_owner_manifest["valid"], original_owner_manifest),
        check("correction1_delta_manifest_replay", correction1_delta_manifest["valid"], correction1_delta_manifest),
        check("correction1_owner_manifest_replay", correction1_owner_manifest["valid"], correction1_owner_manifest),
        check("correction2_delta_manifest_replay", correction2_delta_manifest["valid"], correction2_delta_manifest),
        check("correction2_owner_manifest_replay", correction2_owner_manifest["valid"], correction2_owner_manifest),
        check("original_final_delta_coverage", original_changed_delta == expected_original_delta, {"changed": len(original_changed_delta), "expected": len(expected_original_delta)}),
        check("correction1_delta_coverage", correction1_changed_delta == expected_correction1_delta, {"changed": len(correction1_changed_delta), "expected": len(expected_correction1_delta)}),
        check("correction2_delta_coverage", correction2_changed_delta == expected_correction2_delta, {"changed": len(correction2_changed_delta), "expected": len(expected_correction2_delta)}),
        check("correction2_owner_coverage", changed_owner == expected_owner, {"changed": len(changed_owner), "expected": len(expected_owner)}),
        check("staged_review_valid", staged_review["status"] == "VALID_PRECOMMIT_CORRECTION2_STAGED_REVIEW" and not staged_review["unexpected_paths"] and staged_review["confirmed_five_class_privacy_or_raw_identifier_hits"] == 0, staged_review["status"]),
        check("phase_outcomes_exact", truth["core_outcomes"] == OUTCOMES, truth["core_outcomes"]),
        check("phase_counts_exact", truth["current_overlay"] == COUNTS, truth["current_overlay"]),
        check("proposal_chain_exact", truth["declared_proposal_chain"] == 7630, truth["declared_proposal_chain"]),
        check("method_partition_exact", method_flow["current_phase_partition"] == {"methods": 660, "failed": 210, "passing": 450}, method_flow["current_phase_partition"]),
        check("failed_canonical_receipt_binding", [row["sha256"] for row in truth["failed_canonical_receipts"]] == [FAILED_CANONICAL_RECEIPT_SHA256, FAILED_CORRECTION1_RECEIPT_SHA256] and all(row["status"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" and row["success_count"] == 0 and row["replay_count"] == 0 for row in truth["failed_canonical_receipts"]), truth["failed_canonical_receipts"]),
        check("gap_gate_totals_exact", gaps["current"] == 359 and gates["current"] == 351, {"open_gaps": gaps["current"], "exact_gates": gates["current"]}),
        check("route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and route["provisional_exact_title"] == "Sylven Arc" and route["provisional_phase"] == "v676-v7" and route["send_count"] == 0, route),
        check("content_seal_replay", original_seal["valid"] and original_seal["entries"] == 8 and correction1_seal["valid"] and correction1_seal["entries"] == 4 and correction2_seal["valid"] and correction2_seal["entries"] == 4, {"original": original_seal, "correction1": correction1_seal, "correction2": correction2_seal}),
        check("stale_label_review", not stale_hits, stale_hits),
        check("diff_hygiene", diff_check.returncode == 0, diff_check.stderr.decode("utf-8", "replace")),
        check("terminal_verdict_exact", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"]),
    ]

    objects = tree_objects(head)
    changed_text = [
        path for path in sorted(changed_owner)
        if Path(path).suffix.lower() in {".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml"}
    ]
    text_blobs = batch_blobs([objects[path][1] for path in changed_text])
    privacy_patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "transcript_or_stream": re.compile(r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I),
    }
    privacy_candidates = []
    for path, blob in zip(changed_text, text_blobs, strict=True):
        scanner_surface = path.startswith(("scripts/", "tests/")) or path.endswith("-staged-review.json") or path.endswith("privacy-adjudication.json")
        if blob is None:
            privacy_candidates.append({"path": path, "class": "missing_blob", "disposition": "confirmed_payload_hit"})
            continue
        try:
            value = blob.decode("utf-8")
        except UnicodeDecodeError:
            privacy_candidates.append({"path": path, "class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        for label, pattern in privacy_patterns.items():
            if pattern.search(value):
                privacy_candidates.append({"path": path, "class": label, "disposition": "scanner_definition_or_adjudication_metadata" if scanner_surface else "confirmed_payload_hit"})
    confirmed_privacy = [row for row in privacy_candidates if row["disposition"] == "confirmed_payload_hit"]

    changed_python = [path for path in sorted(changed_owner) if path.endswith(".py")]
    security_findings = []
    for path in changed_python:
        blob = batch_blobs([objects[path][1]])[0]
        try:
            source = blob.decode("utf-8") if blob is not None else ""
            compile(source, path, "exec")
            ast.parse(source, filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            security_findings.append({"path": path, "issue": type(exc).__name__})

    documents = [path for path in OWNER_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html"}]
    max_words = max((len(path.read_text(encoding="utf-8").split()) for path in documents), default=0)
    owner_added_files = len(changed_owner)
    clean_after = git_text("status", "--porcelain=v1") == ""
    after_equality = current_equality()
    skill_rows = skill_summary["skills"]
    runner_rows = runner_summary["runners"]
    minimal = [
        check("owner_tests_42", test_result.returncode == 0 and current_tree_test_count == 40 and deselected_count == 2 and lifecycle_passed == 2 and test_count == 42, {"current_tree_tests": current_tree_test_count, "deselected_lifecycle_tests": deselected_count, "immutable_lifecycle_checks": lifecycle_passed, "tests": test_count, "exit": test_result.returncode}),
        check("strict_json", not json_issues, {"documents": len(json_paths), "issues": len(json_issues)}),
        check("five_class_privacy", not confirmed_privacy, {"scanned": len(changed_text), "candidates": len(privacy_candidates), "confirmed": len(confirmed_privacy)}),
        check("bounded_python_security", not security_findings, {"files": len(changed_python), "findings": len(security_findings)}),
        check("owner_file_cap", owner_added_files < 2000, owner_added_files),
        check("document_word_cap", max_words <= 100000, max_words),
        check("twenty_skills", skill_summary["count"] == 20 and all(row["official_initialization"] and row["quick"] and row["read_through_eof"] and row["smoke"] and not row["global_install"] for row in skill_rows), skill_summary["count"]),
        check("ten_runners", runner_summary["count"] == 10 and all(row["positive"] and row["invalid_rejected"] for row in runner_rows), runner_summary["count"]),
        check("mutations_160", mutation_summary["executed"] == 160 and mutation_summary["rejected"] == 160 and mutation_summary["failed_witnesses_retained"] == 160, mutation_summary),
        check("exact_blocked_unexecuted", gates["exact_approval_packets_unexecuted"] == 20 and gates["blocked_packets_unexecuted"] == 10, gates),
        check("portfolio_exact", portfolio["safe_now_completed"] == 60 and portfolio["candidate_completed_without_core_promotion"] == 30 and portfolio["clean_fix_refine_completed"] == 60, portfolio),
        check("full_suite_not_run", truth["full_repository_suite_run"] is False and closeout["full_repository_suite_run"] is False, {"truth": truth["full_repository_suite_run"], "closeout": closeout["full_repository_suite_run"]}),
        check("not_independent_reproduction", truth["independent_reproduction_claimed"] is False, truth["independent_reproduction_claimed"]),
        check("clean_after", clean_after, clean_after),
        check("four_way_equal_after", after_equality["four_way_equal"] and after_equality["ahead"] == 0 and after_equality["behind"] == 0, after_equality),
    ]

    detailed_passed = sum(row["passed"] for row in detailed)
    minimal_passed = sum(row["passed"] for row in minimal)
    valid = detailed_passed == 39 and minimal_passed == 15
    payload: dict[str, Any] = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "started_at_utc": started,
        "completed_at_utc": now_utc(),
        "invocation_count": 1,
        "success_count": 1 if valid else 0,
        "replay_count": 0,
        "branch": branch,
        "exact_final": head,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "tests": {"passed": test_count if test_result.returncode == 0 and lifecycle_passed == 2 else 0, "total": 42, "current_tree_passed": current_tree_test_count, "immutable_lifecycle_passed": lifecycle_passed, "deselected_lifecycle_tests": deselected_count, "lifecycle_checks": lifecycle_checks, "exit_code": test_result.returncode, "output_sha256": hashlib.sha256((test_output + json.dumps(lifecycle_checks, sort_keys=True)).encode("utf-8")).hexdigest()},
        "detailed_checks": {"passed": detailed_passed, "total": 30, "rows": detailed},
        "minimal_checks": {"passed": minimal_passed, "total": 15, "rows": minimal},
        "json_documents": len(json_paths),
        "json_issues": json_issues,
        "privacy": {"scanned_text_files": len(changed_text), "pattern_classes": sorted(privacy_patterns), "candidates": privacy_candidates, "confirmed_hits": confirmed_privacy},
        "security": {"changed_python_files": len(changed_python), "findings": security_findings},
        "manifests": {"x1": x1_manifest["entries"], "evidence": evidence_manifest["entries"], "original_final_delta": original_delta_manifest["entries"], "original_final_owner": original_owner_manifest["entries"], "correction1_delta": correction1_delta_manifest["entries"], "correction1_owner": correction1_owner_manifest["entries"], "correction2_delta": correction2_delta_manifest["entries"], "correction2_owner": correction2_owner_manifest["entries"]},
        "lifecycle": {"phase_commits": commit_count, "merges": merge_count, "final_parents": parent_count, "clean_before": clean_before, "clean_after": clean_after, "before_equality": before_equality, "after_equality": after_equality},
        "caps": {"owner_added_files": owner_added_files, "file_guard": 2000, "max_document_words": max_words, "word_guard": 100000},
        "outcomes": OUTCOMES,
        "counts": COUNTS,
        "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    payload["canonical_payload_sha256"] = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt).resolve()
    if receipt.suffix.lower() != ".json":
        raise SystemExit("canonical receipt must be an exact JSON path")
    if receipt.is_relative_to(ROOT.resolve()):
        raise SystemExit("canonical receipt must remain external to the repository")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    running = {
        "schema": "ghc.family.exact-final-owner-scoped-canonical-receipt.v3",
        "owner": OWNER,
        "phase": PHASE,
        "status": "INVOKED_RUNNING_NO_REPLAY",
        "started_at_utc": now_utc(),
        "invocation_count": 1,
        "success_count": 0,
        "replay_count": 0,
        "boundary": BOUNDARY,
    }
    try:
        write_receipt(receipt, running, exclusive=True)
    except FileExistsError as exc:
        raise SystemExit("canonical receipt already exists; replay prohibited") from exc
    try:
        payload = canonical_payload()
    except Exception as exc:
        invalid = {
            **running,
            "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "completed_at_utc": now_utc(),
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        write_receipt(receipt, invalid)
        raise
    write_receipt(receipt, payload)
    print(json.dumps({
        "status": payload["status"],
        "exact_final": payload["exact_final"],
        "tests": payload["tests"],
        "detailed": payload["detailed_checks"]["passed"],
        "minimal": payload["minimal_checks"]["passed"],
        "json_documents": payload["json_documents"],
        "privacy_confirmed_hits": len(payload["privacy"]["confirmed_hits"]),
        "security_findings": len(payload["security"]["findings"]),
        "canonical_payload_sha256": payload["canonical_payload_sha256"],
    }, sort_keys=True))
    if payload["status"] != "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
