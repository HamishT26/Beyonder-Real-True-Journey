#!/usr/bin/env python3
"""Run Lyren Moss v673-v7's one exclusive exact-final canonical aggregate."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import rfc8785


ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/lyren-moss/v673-v7"
BRANCH = "codex/GHC-Family/lyren-moss-v673-v7-full-tools"
SOURCE_FINAL = "7fe824e31286b3348d42103812a85e0e3e02a4c6"
X1_COMMIT = "786654cf8f28bb8c7abed41fb8f8315ab65f7e83"
EVIDENCE_COMMIT = "ea787fa029afd2b0c41108c03fd986c253b1bfc4"
STATUS = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
MANIFESTS = [
    f"{BASE}/validation/x1-manifest.json",
    f"{BASE}/validation/x2-evidence-manifest.json",
    f"{BASE}/validation/final-delta-manifest.json",
    f"{BASE}/validation/final-owner-manifest.json",
    f"{BASE}/validation/final-content-seal.json",
]


def git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def git(*args: str) -> str:
    return git_bytes(*args).decode("utf-8").strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def json_blob(path: str) -> Any:
    return json.loads(git_bytes("show", f"HEAD:{path}").decode("utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_parent(child: str, parent: str) -> bool:
    return git("rev-parse", f"{child}^") == parent


def replay_manifest(path: str) -> dict[str, Any]:
    document = json_blob(path)
    failures = []
    for row in document["entries"]:
        data = normalized(git_bytes("show", f"HEAD:{row['path']}"))
        actual = sha256(data)
        if len(data) != row["bytes"] or actual != row["sha256_normalized_lf"]:
            failures.append(
                {
                    "path": row["path"],
                    "expected_bytes": row["bytes"],
                    "actual_bytes": len(data),
                    "expected_sha256": row["sha256_normalized_lf"],
                    "actual_sha256": actual,
                }
            )
    if failures:
        raise RuntimeError(f"manifest replay failed for {path}: {failures[:3]}")
    return {"path": path, "entries": document["entry_count"], "failures": 0}


def owner_paths() -> list[str]:
    paths = git("ls-tree", "-r", "--name-only", "HEAD").splitlines()
    return sorted(
        path for path in paths
        if path.startswith(f"{BASE}/")
        or path == "ghc-family-index/references/v673-v7-lyren-moss.md"
        or path.startswith("scripts/build_ghc_family_lyren_moss_v673_v7_")
        or path == "scripts/validate_ghc_family_lyren_moss_v673_v7_final.py"
        or path.startswith("tests/test_ghc_family_lyren_moss_v673_v7_")
    )


def parse_json_blobs(paths: list[str]) -> int:
    count = 0
    for path in paths:
        if not path.endswith(".json"):
            continue
        json.loads(git_bytes("show", f"HEAD:{path}").decode("utf-8"))
        count += 1
    return count


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_or_thread_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "credential_assignment": re.compile(r"(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]"),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "international_phone_like_number": re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)"),
    }
    findings = []
    scanned = 0
    for path in paths:
        if Path(path).suffix.casefold() not in {".json", ".md", ".html", ".py"}:
            continue
        text = git_bytes("show", f"HEAD:{path}").decode("utf-8", "replace")
        scanned += 1
        for category, pattern in patterns.items():
            if pattern.search(text):
                findings.append({"path": path, "class": category})
    if findings:
        raise RuntimeError(f"privacy scan confirmed hits: {findings[:5]}")
    return {"files_scanned": scanned, "classes": len(patterns), "confirmed_hits": 0, "complete_privacy_assurance": False}


def security_scan(paths: list[str]) -> dict[str, Any]:
    findings = []
    python_files = [path for path in paths if path.endswith(".py")]
    for path in python_files:
        tree = ast.parse(git_bytes("show", f"HEAD:{path}").decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
            if name in {"eval", "exec", "system"}:
                findings.append({"path": path, "line": node.lineno, "call": name})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    if findings:
        raise RuntimeError(f"bounded AST findings: {findings[:5]}")
    return {"python_files": len(python_files), "bounded_findings": 0, "exhaustive_security": False}


def run_test(path: str) -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, path, "-q"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        text=True,
        encoding="utf-8",
    )
    output = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode:
        raise RuntimeError(f"selected test failed: {path}\n{output}")
    match = re.search(r"Ran\s+(\d+)\s+tests?", output)
    if not match:
        raise RuntimeError(f"could not parse selected test count: {path}\n{output}")
    return {"path": path, "tests": int(match.group(1)), "returncode": result.returncode, "status": "passed"}


def materialized_file_count() -> int:
    return sum(1 for path in ROOT.rglob("*") if path.is_file())


def validate(expected_head: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def passed(name: str, evidence: Any) -> None:
        checks.append({"check": name, "passed": True, "evidence": evidence})

    head = git("rev-parse", "HEAD")
    if head != expected_head:
        raise RuntimeError(f"exact head mismatch: expected {expected_head}, got {head}")
    passed("exact_head", head)
    branch = git("branch", "--show-current")
    if branch != BRANCH:
        raise RuntimeError(f"branch mismatch: {branch}")
    passed("exact_branch", branch)
    status = git("status", "--porcelain=v1")
    if status:
        raise RuntimeError(f"worktree not clean: {status}")
    passed("clean_before", True)

    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    if not live_line:
        raise RuntimeError("fresh live remote branch missing")
    live = live_line.split()[0]
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    if not (head == upstream == tracking == live and divergence == "0\t0"):
        raise RuntimeError(f"four-way equality failed: {head}, {upstream}, {tracking}, {live}, {divergence}")
    passed("fresh_four_way_equality", {"local": head, "upstream": upstream, "tracking": tracking, "live": live, "divergence": divergence})

    if not check_parent(X1_COMMIT, SOURCE_FINAL):
        raise RuntimeError("x1 parent mismatch")
    if not check_parent(EVIDENCE_COMMIT, X1_COMMIT):
        raise RuntimeError("evidence parent mismatch")
    if not check_parent(head, EVIDENCE_COMMIT):
        raise RuntimeError("final parent mismatch")
    commits = int(git("rev-list", "--count", f"{SOURCE_FINAL}..{head}"))
    merges = git("rev-list", "--merges", f"{SOURCE_FINAL}..{head}").splitlines()
    if commits != 3 or merges:
        raise RuntimeError(f"history shape failed: commits={commits}, merges={merges}")
    for commit in [X1_COMMIT, EVIDENCE_COMMIT, head]:
        if len(git("rev-list", "--parents", "-n", "1", commit).split()) != 2:
            raise RuntimeError(f"commit is not single-parent: {commit}")
    passed("direct_single_parent_zero_merge_history", {"commits": commits, "merges": 0})
    if commits > 8:
        raise RuntimeError("commit ceiling exceeded")
    passed("commit_ceiling", {"actual": commits, "ceiling": 8})

    paths = owner_paths()
    materialized = materialized_file_count()
    if len(paths) >= 2000 or materialized >= 2000:
        raise RuntimeError(f"file ceiling exceeded: owner={len(paths)}, materialized={materialized}")
    passed("file_ceiling", {"owner_files": len(paths), "materialized_files": materialized, "ceiling": 2000})
    json_parses = parse_json_blobs(paths)
    passed("strict_utf8_json_parse", json_parses)

    manifest_rows = [replay_manifest(path) for path in MANIFESTS]
    manifest_total = sum(row["entries"] for row in manifest_rows)
    passed("exact_manifest_replays", {"manifests": manifest_rows, "entries": manifest_total})

    privacy = privacy_scan(paths)
    passed("five_class_privacy_scan", privacy)
    security = security_scan(paths)
    passed("bounded_python_ast_scan", security)

    selected = [
        run_test("tests/test_ghc_family_lyren_moss_v673_v7_x2.py"),
        run_test("tests/test_ghc_family_lyren_moss_v673_v7_final.py"),
    ]
    selected_total = sum(row["tests"] for row in selected)
    passed("selected_owner_tests", {"modules": selected, "tests": selected_total})

    results = json_blob(f"{BASE}/x2/proposal-results.json")
    mutations = json_blob(f"{BASE}/x2/mutation-register.json")
    tools = json_blob(f"{BASE}/x2/toolchain-receipt.json")
    tasks = json_blob(f"{BASE}/x2/task-execution-ledger.json")
    summary = json_blob(f"{BASE}/closeout/terminal-summary.json")
    route = json_blob(f"{BASE}/closeout/route-state.json")
    if results["outcome_counts"] != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise RuntimeError("outcome counts drifted")
    if mutations["executed_count"] != 160 or mutations["rejected_count"] != 160:
        raise RuntimeError("mutation register drifted")
    if tools["wheel_count"] != 8 or not all(row["verified"] for row in tools["wheels"]):
        raise RuntimeError("tool integrity receipt drifted")
    if tasks["safe_now_executed"] != 60 or tasks["candidate_executed"] != 30:
        raise RuntimeError("task portfolio drifted")
    if summary["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("terminal verdict drifted")
    if route["state"] != "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED" or route["send_attempts"] != 0 or route["sent_by_lyren_moss"]:
        raise RuntimeError("route state is not prepared-not-sent")
    passed("program_truth", {"outcomes": results["outcome_counts"], "mutations": 160, "wheels": 8, "safe": 60, "candidate": 30, "terminal_verdict": summary["terminal_verdict"]})
    passed("precontact_guard", {"state": route["state"], "send_attempts": route["send_attempts"]})

    baton_path = f"{BASE}/handoffs/ilyra-fen-v673-v8-activation-candidate.md"
    baton = git_bytes("show", f"HEAD:{baton_path}")
    baton_words = len(re.findall(rb"\S+", baton))
    if baton_words < 900:
        raise RuntimeError(f"activation candidate too short: {baton_words} words")
    passed("activation_candidate", {"path": baton_path, "bytes": len(baton), "words": baton_words, "sha256": sha256(baton), "prepared_not_sent": True})

    stale = []
    for path in paths:
        if path.startswith(f"{BASE}/") or "v673_v7" in path or path == "ghc-family-index/references/v673-v7-lyren-moss.md":
            continue
        stale.append(path)
    if stale:
        raise RuntimeError(f"owner scope path drift: {stale}")
    passed("owner_scope_and_stale_path_hygiene", {"unexpected": 0})

    status_after = git("status", "--porcelain=v1")
    if status_after:
        raise RuntimeError(f"worktree changed during canonical validation: {status_after}")
    passed("clean_after", True)
    return {
        "status": STATUS,
        "owner": "Lyren Moss",
        "phase": "v673-v7",
        "exact_head": head,
        "branch": BRANCH,
        "invocation_count": 1,
        "replayed": False,
        "checks_passed": len(checks),
        "checks": checks,
        "selected_tests": selected_total,
        "json_parses": json_parses,
        "manifest_entries_replayed": manifest_total,
        "privacy_files_scanned": privacy["files_scanned"],
        "privacy_confirmed_hits": 0,
        "python_files_scanned": security["python_files"],
        "bounded_security_findings": 0,
        "owner_files": len(paths),
        "materialized_files": materialized,
        "source_to_final_commits": commits,
        "source_to_final_merges": 0,
        "complete_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "complete_privacy_assurance": False,
        "complete_accessibility_assurance": False,
        "exhaustive_security": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.receipt_dir.exists():
        raise SystemExit("exclusive canonical receipt directory already exists; replay refused")
    args.receipt_dir.mkdir(parents=True, exist_ok=False)
    invocation = {
        "owner": "Lyren Moss",
        "phase": "v673-v7",
        "expected_head": args.expected_head,
        "invocation_count": 1,
        "state": "RUNNING",
        "replayed": False,
    }
    (args.receipt_dir / "invocation.json").write_text(json.dumps(invocation, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    try:
        payload = validate(args.expected_head)
    except Exception as exc:
        failure = {**invocation, "state": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "error_type": type(exc).__name__, "error": str(exc)}
        (args.receipt_dir / "canonical-failure.json").write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        raise
    payload_bytes = rfc8785.dumps(payload)
    payload_sha = sha256(payload_bytes)
    receipt = {
        "status": STATUS,
        "exact_head": args.expected_head,
        "invocation_count": 1,
        "replayed": False,
        "canonical_payload_sha256": payload_sha,
        "checks_passed": payload["checks_passed"],
        "selected_tests": payload["selected_tests"],
        "manifest_entries_replayed": payload["manifest_entries_replayed"],
        "terminal_verdict": payload["terminal_verdict"],
    }
    (args.receipt_dir / "canonical-payload.json").write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (args.receipt_dir / "canonical-receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    (args.receipt_dir / "invocation.json").write_text(json.dumps({**invocation, "state": "SUCCEEDED_NO_REPLAY"}, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
