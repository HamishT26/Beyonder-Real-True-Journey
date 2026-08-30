#!/usr/bin/env python3
"""Run the one attributable Sylven Arc v676-v7 exact-final owner canonical."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sylven Arc"
PHASE = "v676-v7"
BRANCH = "codex/GHC-Family/sylven-arc-v676-v7-full-tools"
SOURCE = "b8e8b258876b5af3b3e3247f42ac58dde9a7e6a4"
X1 = "b9861f8aaed6f98606e5370ad0f11918865b3433"
EVIDENCE = "dee3fe5b0909b14ca3b807d702e36f6ced478ff0"
OWNER_PREFIX = "docs/sylven-arc/v676-v7/"
SCRIPT_RE = re.compile(r"^scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_sylven_arc_v676_v7_.*\.py$")
TEST_RE = re.compile(r"^tests/test_ghc_family_sylven_arc_v676_v7_.*\.py$")
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
    "credential_assignment": re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_stream": re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
}


def run(repo: Path, *args: str, check: bool = True, binary: bool = False) -> str | bytes:
    result = subprocess.run([*args], cwd=repo, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    return run(repo, "git", *args, binary=binary)


def load(repo: Path, relative: str) -> dict[str, Any]:
    return json.loads((repo / relative).read_text(encoding="utf-8"))


def owner_path(path: str) -> bool:
    return path.startswith(OWNER_PREFIX) or bool(SCRIPT_RE.fullmatch(path)) or bool(TEST_RE.fullmatch(path))


def manifest_replay(repo: Path, relative: str) -> tuple[int, list[str]]:
    manifest = load(repo, relative)
    failures = []
    for row in manifest["entries"]:
        raw = git(repo, "cat-file", "-p", row["git_blob_oid"], binary=True)
        normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if hashlib.sha256(normalized).hexdigest() != row["sha256_normalized_lf"]:
            failures.append(row["path"])
    return manifest["entry_count"], failures


def atomic_receipt(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt = args.receipt.resolve()
    if receipt.exists():
        raise SystemExit("exclusive canonical receipt already exists; replay refused")

    head = str(git(repo, "rev-parse", "HEAD"))
    branch = str(git(repo, "branch", "--show-current"))
    upstream = str(git(repo, "rev-parse", "@{upstream}"))
    tracking = str(git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}"))
    live_line = str(git(repo, "ls-remote", "origin", f"refs/heads/{BRANCH}"))
    live = live_line.split("\t", 1)[0]
    divergence = str(git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}"))
    porcelain_before = str(git(repo, "status", "--porcelain=v1"))
    prerequisites = {
        "expected_final": head == args.expected_final,
        "branch": branch == BRANCH,
        "direct_parent": str(git(repo, "rev-parse", "HEAD^")) == EVIDENCE,
        "evidence_parent": str(git(repo, "rev-parse", f"{EVIDENCE}^")) == X1,
        "x1_parent": str(git(repo, "rev-parse", f"{X1}^")) == SOURCE,
        "three_phase_commits": str(git(repo, "rev-list", "--count", f"{SOURCE}..HEAD")) == "3",
        "zero_merges": str(git(repo, "rev-list", "--merges", "--count", f"{SOURCE}..HEAD")) == "0",
        "one_final_parent": len(str(git(repo, "rev-list", "--parents", "-n", "1", "HEAD")).split()) == 2,
        "clean_before": porcelain_before == "",
        "zero_divergence_before": divergence.replace("\t", " ").split() == ["0", "0"],
        "four_way_before": len({head, upstream, tracking, live}) == 1,
    }
    if not all(prerequisites.values()):
        raise SystemExit("canonical prerequisites failed: " + repr(prerequisites))

    tests = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "pytest", "-q", "tests/test_ghc_family_sylven_arc_v676_v7_final.py"],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if tests.returncode != 0:
        raise SystemExit("owner final tests failed:\n" + tests.stdout + "\n" + tests.stderr)
    match = re.search(r"(\d+) passed", tests.stdout)
    test_count = int(match.group(1)) if match else 0

    delta_count, delta_failures = manifest_replay(repo, OWNER_PREFIX + "validation/final-delta-manifest.json")
    owner_count, owner_failures = manifest_replay(repo, OWNER_PREFIX + "validation/final-owner-manifest.json")
    x1_count, x1_failures = manifest_replay(repo, OWNER_PREFIX + "validation/x1-manifest.json")
    evidence_count, evidence_failures = manifest_replay(repo, OWNER_PREFIX + "validation/evidence-manifest.json")
    manifest_failures = x1_failures + evidence_failures + delta_failures + owner_failures

    committed_owner_paths = [
        row
        for row in str(git(repo, "ls-tree", "-r", "--name-only", "HEAD", "--", OWNER_PREFIX, "scripts", "tests")).splitlines()
        if owner_path(row)
    ]
    json_paths = [path for path in committed_owner_paths if path.endswith(".json")]
    json_failures = []
    for path in json_paths:
        try:
            json.loads(bytes(git(repo, "show", f"HEAD:{path}", binary=True)).decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            json_failures.append(f"{path}:{type(exc).__name__}")

    text_paths = [path for path in committed_owner_paths if path.endswith((".py", ".json", ".md", ".html", ".txt", ".yaml", ".yml"))]
    privacy_candidates = []
    confirmed_hits = []
    for path in text_paths:
        value = bytes(git(repo, "show", f"HEAD:{path}", binary=True)).decode("utf-8")
        for category, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(value):
                scanner_metadata = path.startswith(OWNER_PREFIX + "validation/") and path.endswith(("manifest.json", "staged-review.json"))
                row = {
                    "path": path,
                    "category": category,
                    "adjudication": "scanner_definition_or_adjudication_metadata" if path.endswith(".py") or scanner_metadata else "confirmed_payload_hit",
                }
                privacy_candidates.append(row)
                if row["adjudication"] == "confirmed_payload_hit":
                    confirmed_hits.append(row)

    python_paths = [path for path in committed_owner_paths if path.endswith(".py")]
    python_failures = []
    banned_calls = {"eval", "exec"}
    for path in python_paths:
        value = bytes(git(repo, "show", f"HEAD:{path}", binary=True)).decode("utf-8")
        try:
            tree = ast.parse(value, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in banned_calls:
                    python_failures.append(path + ":banned_dynamic_execution")
        except SyntaxError:
            python_failures.append(path + ":syntax_error")

    docs = [path for path in committed_owner_paths if path.endswith((".md", ".html"))]
    word_counts = {}
    for path in docs:
        value = bytes(git(repo, "show", f"HEAD:{path}", binary=True)).decode("utf-8")
        word_counts[path] = len(value.split())
    max_words = max(word_counts.values(), default=0)

    seal = load(repo, OWNER_PREFIX + "seal/content-seal.json")
    seal_failures = []
    for row in seal["entries"]:
        raw = bytes(git(repo, "show", f"HEAD:{row['path']}", binary=True)).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if hashlib.sha256(raw).hexdigest() != row["sha256_normalized_lf"]:
            seal_failures.append(row["path"])

    phase_truth = load(repo, OWNER_PREFIX + "final/phase-truth.json")
    staged_review = load(repo, OWNER_PREFIX + "validation/final-staged-review.json")
    detailed = {
        "owner_tests_exact": test_count >= 18,
        "x1_manifest": x1_count == 21 and not x1_failures,
        "evidence_manifest": evidence_count == 541 and not evidence_failures,
        "final_delta_manifest": delta_count >= 20 and not delta_failures,
        "final_owner_manifest": owner_count >= 580 and not owner_failures,
        "manifest_union_clean": not manifest_failures,
        "json_parses": not json_failures,
        "json_count": len(json_paths) >= 500,
        "privacy_no_confirmed_hits": not confirmed_hits,
        "privacy_five_classes": set(PRIVACY_PATTERNS) == {"private_absolute_path", "raw_task_route", "credential_assignment", "raw_uuid", "session_stream"},
        "python_ast": not python_failures,
        "python_count": len(python_paths) >= 18,
        "owner_file_stop": len(committed_owner_paths) < 2000,
        "document_word_stop": max_words <= 100000,
        "content_seal": not seal_failures,
        "content_seal_count": seal["entry_count"] == len(seal["entries"]) >= 20,
        "staged_review_status": staged_review["status"] == "VALID_EXACT_FINAL_STAGED_REVIEW",
        "staged_review_zero_hits": staged_review["confirmed_privacy_or_raw_identifier_hits"] == 0,
        "outcome_vocabulary": set(phase_truth["outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "outcome_counts": phase_truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "negatives": phase_truth["effective_negatives"] == 42883,
        "methods": phase_truth["effective_methods"] == 34482,
        "failed_witnesses": phase_truth["retained_failed_witnesses"] == 14544,
        "passing_witnesses": phase_truth["bounded_passing_witnesses"] == 20627,
        "open_gaps": phase_truth["open_gaps"] == 361,
        "exact_gates": phase_truth["exact_gates"] == 353,
        "terminal_verdict": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "zero_real_rows": phase_truth["real_world_rows"] == 0,
        "zero_measurements": phase_truth["observed_measurements"] == 0,
        "zero_external_actions": phase_truth["external_actions"] == 0,
        "proposal_chain": phase_truth["declared_proposal_chain_after"] == 7670,
        "mutations": phase_truth["preregistered_mutations_executed"] == phase_truth["preregistered_mutations_rejected"] == 160,
        "skills": phase_truth["phase_local_skills"] == 20,
        "runners": phase_truth["family_current_runners"] == 10,
        "source_ancestry": bool(prerequisites["x1_parent"] and prerequisites["evidence_parent"] and prerequisites["direct_parent"]),
        "zero_merges": prerequisites["zero_merges"],
    }
    minimal = {
        "exact_head": head == args.expected_final,
        "clean": porcelain_before == "",
        "zero_divergence": prerequisites["zero_divergence_before"],
        "four_way_equal": prerequisites["four_way_before"],
        "direct_parent": prerequisites["direct_parent"],
        "three_commits": prerequisites["three_phase_commits"],
        "zero_merges": prerequisites["zero_merges"],
        "one_parent": prerequisites["one_final_parent"],
        "tests": test_count >= 18,
        "manifests": not manifest_failures,
        "json": not json_failures,
        "privacy": not confirmed_hits,
        "security": not python_failures,
        "caps": len(committed_owner_paths) < 2000 and max_words <= 100000,
        "verdict": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    if not all(detailed.values()) or not all(minimal.values()):
        raise SystemExit("canonical detail failure: " + repr({"detailed": detailed, "minimal": minimal}))

    porcelain_after = str(git(repo, "status", "--porcelain=v1"))
    upstream_after = str(git(repo, "rev-parse", "@{upstream}"))
    tracking_after = str(git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}"))
    live_after = str(git(repo, "ls-remote", "origin", f"refs/heads/{BRANCH}")).split("\t", 1)[0]
    divergence_after = str(git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}"))
    post = {
        "exact_head": str(git(repo, "rev-parse", "HEAD")) == head,
        "clean": porcelain_after == "",
        "zero_divergence": divergence_after.replace("\t", " ").split() == ["0", "0"],
        "four_way_equal": len({head, upstream_after, tracking_after, live_after}) == 1,
    }
    if not all(post.values()):
        raise SystemExit("post-canonical repository state failed: " + repr(post))

    payload: dict[str, Any] = {
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": OWNER,
        "phase": PHASE,
        "exact_final": head,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "canonical_invocation_count": 1,
        "canonical_success_count": 1,
        "canonical_replay_count": 0,
        "owner_tests_passed": test_count,
        "owner_tests_total": test_count,
        "detailed_checks_passed": sum(detailed.values()),
        "detailed_checks_total": len(detailed),
        "minimal_checks_passed": sum(minimal.values()),
        "minimal_checks_total": len(minimal),
        "strict_owner_json_parses": len(json_paths),
        "owner_files": len(committed_owner_paths),
        "privacy_classes": len(PRIVACY_PATTERNS),
        "privacy_candidates": privacy_candidates,
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed_hits),
        "changed_owner_python_files": len(python_paths),
        "bounded_security_findings": len(python_failures),
        "x1_manifest_entries": x1_count,
        "evidence_manifest_entries": evidence_count,
        "final_delta_manifest_entries": delta_count,
        "final_owner_manifest_entries": owner_count,
        "manifest_failures": manifest_failures,
        "maximum_document_words": max_words,
        "three_direct_single_parent_commits": True,
        "zero_merges": True,
        "one_final_parent": True,
        "clean_before_and_after": True,
        "typed_zero_divergence_before_and_after": True,
        "fresh_live_four_way_equal_before_and_after": True,
        "full_repository_suite_run": False,
        "same_owner_evidence_only": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "prerequisites": prerequisites,
        "detailed": detailed,
        "minimal": minimal,
        "post": post,
        "pytest_output": tests.stdout.strip(),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    atomic_receipt(receipt, payload)
    print(json.dumps({"status": payload["status"], "receipt": str(receipt), "payload_sha256": payload["canonical_payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
