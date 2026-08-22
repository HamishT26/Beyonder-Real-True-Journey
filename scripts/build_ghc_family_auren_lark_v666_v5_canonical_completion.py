#!/usr/bin/env python3
"""One-shot exact-final canonical aggregate for Auren Lark v666-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import py_compile
import re
import subprocess
import sys
from tempfile import NamedTemporaryFile
from typing import Any

from ghc_family_auren_lark_v666_v5_runtime import (
    PHASE_ROOT,
    ROOT,
    X1_SHA,
    git_tree_map,
    read_exact,
    replay_manifest,
)


SOURCE_SHA = "e4548a5447996f09087644a4a03e77dea8045ee4"
EVIDENCE_SHA = "7b116c152a78d0c62c7185aac707f3292d6570f1"
BRANCH = "codex/GHC-Family/auren-lark-v666-v5-full-tools"
OWNER_DOC_PREFIX = "docs/auren-lark/v666-v5/"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )


def git(*args: str) -> str:
    completed = run(["git", *args])
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed.stdout.strip()


def owner_path(path: str) -> bool:
    return (
        path.startswith(OWNER_DOC_PREFIX)
        or bool(re.fullmatch(r"scripts/(?:build_)?ghc_family_auren_lark_v666_v5_[a-z0-9_]+\.py", path))
        or bool(re.fullmatch(r"tests/test_ghc_family_auren_lark_v666_v5_[a-z0-9_]+\.py", path))
    )


def exact_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    tree = git_tree_map(commit)
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result: dict[str, bytes] = {}
    try:
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("git cat-file pipes unavailable")
        for path in paths:
            if path not in tree:
                raise RuntimeError(f"missing exact-final path: {path}")
            oid = tree[path][1]
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[0] != oid or header[1] != "blob":
                raise RuntimeError(f"invalid exact-final batch header: {path}")
            result[path] = read_exact(process.stdout, int(header[2]))
            if read_exact(process.stdout, 1) != b"\n":
                raise RuntimeError(f"missing exact-final batch terminator: {path}")
    finally:
        if process.stdin is not None:
            process.stdin.close()
        return_code = process.wait(timeout=30)
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        if process.stdout is not None:
            process.stdout.close()
        if process.stderr is not None:
            process.stderr.close()
        if return_code:
            raise RuntimeError(stderr[:240])
    return result


def test_targets(label: str, targets: list[str], expected: int) -> dict[str, Any]:
    completed = run([sys.executable, "-X", "utf8", "-m", "unittest", "-q", *targets])
    combined = completed.stdout + "\n" + completed.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
    count = int(match.group(1)) if match else 0
    return {
        "label": label,
        "targets": targets,
        "expected": expected,
        "observed": count,
        "returncode": completed.returncode,
        "valid": completed.returncode == 0 and count == expected,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    expected_final = args.expected_final.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", expected_final):
        raise SystemExit("expected-final must be a lowercase 40-hex commit")
    receipt_path = Path(args.receipt).resolve()
    if receipt_path.exists():
        prior = json.loads(receipt_path.read_text(encoding="utf-8"))
        if prior.get("status") == "SUCCESS":
            raise SystemExit("successful canonical receipt already exists; replay forbidden")
        raise SystemExit("canonical receipt path already exists; inspect retained failure before any recovery")
    head = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()]
    status = git("status", "--porcelain")
    parent = git("rev-parse", "HEAD^")
    commit_count = int(git("rev-list", "--count", f"{SOURCE_SHA}..{head}"))
    merge_count = int(git("rev-list", "--merges", "--count", f"{SOURCE_SHA}..{head}"))
    history_checks = {
        "head_matches_expected": head == expected_final,
        "final_direct_child_of_evidence": parent == EVIDENCE_SHA,
        "source_to_final_commit_count_3": commit_count == 3,
        "source_to_final_merge_count_0": merge_count == 0,
        "clean": status == "",
        "ahead_0": divergence[0] == 0,
        "behind_0": divergence[1] == 0,
        "four_way_equal": len({head, upstream, tracking, live}) == 1,
    }
    manifests = {
        "x1": replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA),
        "evidence": replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", EVIDENCE_SHA),
        "final_delta": replay_manifest(PHASE_ROOT / "validation" / "final-delta-manifest.json", head),
        "final_owner": replay_manifest(PHASE_ROOT / "validation" / "final-owner-manifest.json", head),
    }
    tests = [
        test_targets("x2", ["tests.test_ghc_family_auren_lark_v666_v5_x2"], 66),
        test_targets(
            "evidence_final_lifecycle_compatible",
            [
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_evidence_summary_exact",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_x2_test_receipt_is_attributable_and_noncanonical",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_failed_mixed_lifecycle_invocation_is_retained",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_privacy_and_security_receipts_are_bounded",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_x1_manifest_replays_exactly",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_evidence_seal_binds_core_ledgers_without_terminal_claim",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_toolbox_and_deck_receipts_are_bounded",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_authority_gaps_and_terminal_verdict_remain",
                "tests.test_ghc_family_auren_lark_v666_v5_evidence.AurenLarkV666V5EvidenceTests.test_all_evidence_json_parses",
            ],
            9,
        ),
        test_targets("closeout", ["tests.test_ghc_family_auren_lark_v666_v5_closeout"], 12),
    ]
    tree = git_tree_map(head)
    owner_paths = sorted(path for path in tree if owner_path(path))
    blobs = exact_blobs(head, owner_paths)
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    json_count = 0
    markdown_count = 0
    html_count = 0
    privacy_candidates = []
    security_findings = []
    python_count = 0
    compile_failures = []
    maximum_words = 0
    maximum_path = ""
    for path in owner_paths:
        raw = blobs[path]
        value = raw.decode("utf-8")
        if "\r" in value:
            raise RuntimeError(f"non-LF exact-final text: {path}")
        words = len(re.findall(r"\S+", value))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(value)
            json_count += 1
        if path.endswith(".md"):
            markdown_count += 1
        if path.endswith(".html"):
            html_count += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(value):
                privacy_candidates.append({"path": path, "class": class_name})
        if path.endswith(".py"):
            python_count += 1
            tree_ast = ast.parse(value, filename=path)
            for node in ast.walk(tree_ast):
                if not isinstance(node, ast.Call):
                    continue
                name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
                if name in {"eval", "exec"}:
                    security_findings.append({"path": path, "line": node.lineno, "class": f"dynamic_{name}"})
                if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security_findings.append({"path": path, "line": node.lineno, "class": "shell_true"})
            try:
                compile(value, path, "exec")
            except SyntaxError as exc:
                compile_failures.append({"path": path, "error": str(exc)})
    truth = json.loads(blobs["docs/auren-lark/v666-v5/closeout/phase-truth.json"])
    review = json.loads(blobs["docs/auren-lark/v666-v5/validation/final-staged-review.json"])
    final_owner = json.loads(blobs["docs/auren-lark/v666-v5/validation/final-owner-manifest.json"])
    content_checks = {
        "owner_file_count_matches": len(owner_paths) == final_owner["exact_final_owner_count_including_self"] == review["exact_final_owner_count"],
        "owner_file_ceiling": len(owner_paths) <= 2000,
        "all_json_parse": json_count > 0,
        "markdown_present": markdown_count > 0,
        "html_present": html_count > 0,
        "document_word_cap": maximum_words <= 100000,
        "five_class_privacy_zero": not privacy_candidates,
        "bounded_python_security_zero": not security_findings,
        "python_compile_zero": not compile_failures,
        "outcomes_14_4_1_1": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_counts": truth["effective_negatives"] == 26640 and truth["effective_methods"] == 11412,
        "gaps_and_gates": truth["open_gaps"] == 187 and truth["exact_gates"] == 185,
        "terminal_not_ready": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "successor_prepared_not_sent": json.loads(blobs["docs/auren-lark/v666-v5/orchestration/route-state-final-candidate.json"])["route"] == "PREPARED_NOT_SENT",
    }
    valid = (
        all(history_checks.values())
        and all(result["valid"] for result in manifests.values())
        and all(result["valid"] for result in tests)
        and all(content_checks.values())
    )
    receipt = {
        "schema": "ghc.family.auren-lark.v666-v5.external-canonical-receipt.v1",
        "status": "SUCCESS" if valid else "FAILURE",
        "expected_final": expected_final,
        "head": head,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "evidence_sha": EVIDENCE_SHA,
        "branch": BRANCH,
        "history": {"checks": history_checks, "upstream": upstream, "tracking": tracking, "fresh_live": live, "ahead": divergence[0], "behind": divergence[1], "source_to_final_commits": commit_count, "source_to_final_merges": merge_count},
        "manifests": manifests,
        "tests": tests,
        "test_total": sum(row["observed"] for row in tests),
        "test_expected_total": sum(row["expected"] for row in tests),
        "declared_lifecycle_exclusions": [
            "the frozen x1 current-filesystem absence assertion is not run against the final worktree; exact x1 manifest replay and zero-later-path Git-tree checks cover the immutable x1 boundary",
            "the immutable evidence no-closeout-materialized assertion is not run against the final worktree; exact evidence manifest replay and zero-closeout-path evidence Git-tree checks cover the immutable evidence boundary",
        ],
        "owner_file_count": len(owner_paths),
        "json_parse_count": json_count,
        "markdown_count": markdown_count,
        "html_count": html_count,
        "python_compile_count": python_count,
        "python_compile_failures": compile_failures,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": privacy_candidates,
        "security_findings": security_findings,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "content_checks": content_checks,
        "proposal_chain_total": 4270,
        "outcomes": truth["outcomes"],
        "effective_negatives": truth["effective_negatives"],
        "effective_methods": truth["effective_methods"],
        "open_gaps": truth["open_gaps"],
        "exact_gates": truth["exact_gates"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "full_repository_suite_run": False,
        "same_owner_validation_is_independent_reproduction": False,
        "post_success_replay_forbidden": True,
        "claim_boundary": "one attributable exact-final owner-scoped same-owner aggregate; not independent reproduction, professional or legal validation, cultural or Māori authority, or Stage 20 authority",
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", newline="\n", delete=False, dir=receipt_path.parent, prefix="canonical-", suffix=".tmp") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, receipt_path)
    payload = {
        "status": receipt["status"],
        "expected_final": expected_final,
        "test_total": receipt["test_total"],
        "manifest_entries": {name: row["entry_count"] for name, row in manifests.items()},
        "owner_files": len(owner_paths),
        "json": json_count,
        "markdown": markdown_count,
        "html": html_count,
        "python": python_count,
        "privacy_candidates": len(privacy_candidates),
        "security_findings": len(security_findings),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
