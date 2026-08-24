#!/usr/bin/env python3
"""One-shot owner-head canonical aggregate for Lyren Moss v668-v2."""

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
BRANCH = "codex/GHC-Family/lyren-moss-v668-v2-full-tools"
SOURCE_FINAL = "ea14c75a4f0c543ef1bb89858e35252302924aec"
X1_HEAD = "0683eb961987fd4c7283d278e3b217647aef73f0"
EVIDENCE_HEAD = "6bb6b96b08eb26646c362967f8ed30263d348c15"
OWNER_MANIFEST = "docs/lyren-moss/v668-v2/validation/final-owner-manifest.json"
TESTS = [
    "tests/test_ghc_family_lyren_moss_v668_v2_x1.py",
    "tests/test_ghc_family_lyren_moss_v668_v2_x2.py",
    "tests/test_ghc_family_lyren_moss_v668_v2_final.py",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_text(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
        check=True,
        capture_output=True,
    ).stdout


def read_git_json(commit: str, path: str) -> Any:
    return json.loads(git_bytes(commit, path).decode("utf-8"))


def replay_manifest(commit: str, path: str) -> dict[str, int]:
    manifest = read_git_json(commit, path)
    mismatches = 0
    for row in manifest["entries"]:
        data = git_bytes(commit, row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches += 1
    if mismatches:
        raise AssertionError(f"{path} has {mismatches} exact Git-blob mismatches")
    return {"entries": len(manifest["entries"]), "mismatches": 0}


def privacy_scan(texts: dict[str, str]) -> dict[str, int]:
    joined = "\n".join(texts.values())
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:\\(?:Users|GHC-Archives)\\", re.I),
        "secret_token": re.compile(r"(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)"),
        "raw_route_tag": re.compile(r"<(?:source_thread_id|thread_id|client_thread_id)>|" + "client" + "ThreadId", re.I),
        "personal_email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    }
    hits = {name: len(pattern.findall(joined)) for name, pattern in patterns.items()}
    if any(hits.values()):
        raise AssertionError(f"confirmed bounded privacy candidates: {hits}")
    return hits


def security_scan(python_texts: dict[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for path, text in python_texts.items():
        tree = ast.parse(text, filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path, "line": node.lineno, "call": node.func.id})
            if isinstance(node.func, ast.Attribute):
                parts: list[str] = []
                current: ast.AST = node.func
                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)
                    current = current.value
                if isinstance(current, ast.Name):
                    parts.append(current.id)
                name = ".".join(reversed(parts))
                if name in {"os.system", "pickle.loads", "marshal.loads", "yaml.load"}:
                    findings.append({"path": path, "line": node.lineno, "call": name})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    if findings:
        raise AssertionError(f"bounded changed-Python security findings: {findings}")
    return findings


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def run_checks(expected_head: str) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    head = git_text("rev-parse", "HEAD")
    checks["exact_head"] = head == expected_head
    checks["exact_branch"] = git_text("branch", "--show-current") == BRANCH
    checks["clean_before"] = git_text("status", "--porcelain") == ""
    checks["final_parent_is_evidence"] = git_text("rev-parse", "HEAD^") == EVIDENCE_HEAD
    checks["evidence_parent_is_x1"] = git_text("rev-parse", f"{EVIDENCE_HEAD}^") == X1_HEAD
    checks["x1_parent_is_source"] = git_text("rev-parse", f"{X1_HEAD}^") == SOURCE_FINAL
    commits = git_text("rev-list", "--reverse", f"{SOURCE_FINAL}..{head}").splitlines()
    merges = git_text("rev-list", "--merges", f"{SOURCE_FINAL}..{head}").splitlines()
    checks["three_phase_commits"] = len(commits) == 3
    checks["zero_merges"] = len(merges) == 0
    checks["eight_commit_ceiling"] = len(commits) <= 8
    parent_counts = [len(git_text("show", "-s", "--format=%P", commit).split()) for commit in commits]
    checks["all_phase_commits_single_parent"] = parent_counts == [1, 1, 1]
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}")
    checks["upstream_equal"] = upstream == head
    checks["tracking_equal"] = tracking == head
    checks["fresh_live_equal"] = live == head
    checks["zero_divergence"] = divergence == "0\t0"
    if not all(checks.values()):
        raise AssertionError(f"pre-test lifecycle checks failed: {checks}")

    test_result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if test_result.returncode != 0:
        raise AssertionError("owner-scoped test aggregate failed")
    match = re.search(r"(\d+) passed", test_result.stdout)
    if not match:
        raise AssertionError("pytest success count unavailable")
    test_count = int(match.group(1))

    manifests = {
        "x1": replay_manifest(X1_HEAD, "docs/lyren-moss/v668-v2/x1/manifest.json"),
        "evidence": replay_manifest(EVIDENCE_HEAD, "docs/lyren-moss/v668-v2/evidence/evidence-content-manifest.json"),
        "final_delta": replay_manifest(head, "docs/lyren-moss/v668-v2/validation/final-delta-manifest.json"),
        "final_owner": replay_manifest(head, OWNER_MANIFEST),
    }
    owner_manifest = read_git_json(head, OWNER_MANIFEST)
    texts: dict[str, str] = {}
    json_parses = 0
    markdown_checks = 0
    python_compiles = 0
    for row in owner_manifest["entries"]:
        path = row["path"]
        text = git_bytes(head, path).decode("utf-8")
        texts[path] = text
        if path.endswith(".json"):
            json.loads(text)
            json_parses += 1
        elif path.endswith(".md"):
            if not text.strip():
                raise AssertionError(f"empty Markdown: {path}")
            markdown_checks += 1
        elif path.endswith(".py"):
            compile(text, path, "exec")
            python_compiles += 1
    owner_manifest_text = git_bytes(head, OWNER_MANIFEST).decode("utf-8")
    json.loads(owner_manifest_text)
    texts[OWNER_MANIFEST] = owner_manifest_text
    json_parses += 1
    privacy = privacy_scan(texts)
    security = security_scan({path: text for path, text in texts.items() if path.endswith(".py")})
    truth = read_git_json(head, "docs/lyren-moss/v668-v2/final/phase-truth.json")
    route = read_git_json(head, "docs/lyren-moss/v668-v2/closeout/route-and-roster-record.json")
    counts = read_git_json(head, "docs/lyren-moss/v668-v2/closeout/retained-negative-register.json")
    checks["four_exact_truth_labels"] = set(truth["allowed_outcomes"]) == {
        "completed", "represented", "open_gap", "exact_gate"
    }
    checks["exact_outcome_counts"] = truth["outcome_counts"] == {
        "completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8
    }
    checks["terminal_not_ready"] = truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    checks["route_prepared_not_sent"] = route["state"] == "PREPARED_NOT_SENT"
    checks["successor_not_contacted"] = route["successor_contacted"] is False
    checks["one_send_maximum"] = route["single_send_maximum"] == 1
    checks["retained_negative_total"] = counts["effective_negatives_before_canonical"] == 29216
    checks["open_gap_total"] = counts["open_gaps"] == 211
    checks["exact_gate_total"] = counts["exact_gates"] == 206
    materialized_files = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    checks["materialization_below_2000"] = materialized_files < 2000
    checks["owner_manifest_below_2000"] = owner_manifest["entry_count"] < 2000
    checks["privacy_zero_confirmed_hits"] = not any(privacy.values())
    checks["bounded_security_zero_findings"] = len(security) == 0
    checks["clean_after"] = git_text("status", "--porcelain") == ""
    if not all(checks.values()):
        raise AssertionError(f"post-test terminal checks failed: {checks}")
    return {
        "status": "SUCCESSFUL_ONCE_NO_REPLAY",
        "canonical_invocation_count": 1,
        "canonical_success_count": 1,
        "post_success_replay": False,
        "owner": "Lyren Moss",
        "phase": "v668-v2",
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final": head,
        "tests_passed": test_count,
        "test_files": TESTS,
        "manifest_replays": manifests,
        "manifest_entries_total": sum(item["entries"] for item in manifests.values()),
        "json_parses": json_parses,
        "markdown_checks": markdown_checks,
        "python_compiles": python_compiles,
        "privacy_classes": privacy,
        "confirmed_privacy_hits": sum(privacy.values()),
        "bounded_security_findings": len(security),
        "materialized_files": materialized_files,
        "owner_manifest_entries": owner_manifest["entry_count"],
        "terminal_checks": checks,
        "terminal_check_count": len(checks),
        "repository_sealed_counts": {
            "effective_negatives": 29216,
            "methods": 15802,
            "failed_witnesses": 1517,
            "passing_witnesses": 2352,
            "open_gaps": 211,
            "exact_gates": 206,
        },
        "proposal_chain": 4670,
        "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "full_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "same_owner_shared_infrastructure": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "completed_at": utc_now(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.receipt.exists():
        print(json.dumps({"status": "REFUSED_EXISTING_RECEIPT_NO_REPLAY"}, sort_keys=True))
        return 3
    started_at = utc_now()
    try:
        result = run_checks(args.expected_head)
        result["started_at"] = started_at
        write_receipt(args.receipt, result)
        print(json.dumps({
            "status": result["status"],
            "tests_passed": result["tests_passed"],
            "manifest_entries_total": result["manifest_entries_total"],
            "json_parses": result["json_parses"],
            "terminal_check_count": result["terminal_check_count"],
        }, sort_keys=True))
        return 0
    except Exception as exc:  # one-shot aggregate must retain any failure externally
        failure = {
            "status": "FAILED_ONCE_ZERO_CANONICAL_SUCCESS_CREDIT",
            "canonical_invocation_count": 1,
            "canonical_success_count": 0,
            "post_failure_aggregate_replay_allowed": False,
            "owner": "Lyren Moss",
            "phase": "v668-v2",
            "branch": BRANCH,
            "expected_head": args.expected_head,
            "error_class": type(exc).__name__,
            "error_summary": str(exc)[:500],
            "started_at": started_at,
            "failed_at": utc_now(),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_receipt(args.receipt, failure)
        print(json.dumps({"status": failure["status"], "error_class": failure["error_class"]}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
