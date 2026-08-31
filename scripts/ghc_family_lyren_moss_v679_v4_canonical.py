#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Lyren v679-v4."""

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


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
VALIDATION = PHASE / "validation"
SOURCE = "e1c3ef6d2ff0bc2f1e38f5d702e008149842659f"
X1_HEAD = "1fe28fafc308298e1043a9e2afbecf59c24c9866"
EVIDENCE_HEAD = "b204dcbfbcb3d016ab18f4bebc5ef9dc56d9dee6"
BRANCH = "codex/GHC-Family/lyren-moss-v679-v4-full-tools"
RECEIPT_BANK = Path("D:/GHC-Archives/phase-scratch/lyren-v679-v4")
TEXT_SUFFIXES = {".json", ".md", ".html", ".yaml", ".yml", ".py"}
PRIVACY_PATTERNS = {
    "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/]+" + "Users" + r"[\\/]+"),
    "raw_task_route": re.compile(r"(?i)(" + "source" + r"[_-]?thread[_-]?id|" + "client" + r"ThreadId)"),
    "credential_assignment": re.compile(r"(?i)(" + "api" + r"[_-]?key|" + "private" + r"[_-]?key|" + "pass" + r"word|" + "bear" + r"er)\s*[:=]"),
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "session_or_capture": re.compile(r"(?i)(" + "terminal trans" + r"cript|" + "screen" + r"shot payload|" + "session" + r"[_ -]?stream)"),
}


def command(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check)


def git(*args: str) -> str:
    return command("git", *args).stdout.strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def replay_manifest(revision: str, entries: list[dict[str, Any]]) -> list[str]:
    mismatches: list[str] = []
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assert process.stdin is not None and process.stdout is not None
    try:
        for item in entries:
            process.stdin.write(f"{revision}:{item['path']}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                mismatches.append(item["path"])
                continue
            data = normalize(process.stdout.read(int(header[2])))
            process.stdout.read(1)
            if sha(data) != item["sha256"] or len(data) != item["normalized_lf_bytes"]:
                mismatches.append(item["path"])
    finally:
        process.stdin.close()
        process.wait(timeout=30)
    return mismatches


def changed_paths() -> list[str]:
    return [line for line in git("diff", "--name-only", f"{SOURCE}..HEAD").splitlines() if line]


def owner_paths() -> list[str]:
    paths = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(path for path in changed_paths() if path.endswith(".py"))
    return sorted(set(paths))


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    results = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        hits = sorted(name for name, pattern in PRIVACY_PATTERNS.items() if pattern.search(text))
        if hits:
            results.append({"path": relative, "classes": hits})
    return {"classes": len(PRIVACY_PATTERNS), "files_scanned": sum((ROOT / path).is_file() and (ROOT / path).suffix.lower() in TEXT_SUFFIXES for path in paths), "confirmed_candidates": len(results), "results": results}


def ast_security(paths: list[str]) -> dict[str, Any]:
    findings = []
    parsed = 0
    for relative in paths:
        path = ROOT / relative
        if not path.is_file() or path.suffix.lower() != ".py":
            continue
        parsed += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    findings.append({"path": relative, "line": node.lineno, "kind": node.func.id})
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": relative, "line": node.lineno, "kind": "subprocess_shell_true"})
    return {"python_files_parsed": parsed, "medium_or_high_findings": len(findings), "findings": findings, "exhaustive_security": False}


def json_parse(paths: list[str]) -> dict[str, Any]:
    failures = []
    count = 0
    for relative in paths:
        path = ROOT / relative
        if path.is_file() and path.suffix.lower() == ".json":
            count += 1
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # pragma: no cover - retained in receipt
                failures.append({"path": relative, "error": type(exc).__name__})
    return {"parsed": count, "failures": failures}


def collect_tests() -> int:
    result = command(
        sys.executable,
        "-m",
        "pytest",
        "--collect-only",
        "-q",
        "tests/test_ghc_family_lyren_moss_v679_v4_x2.py",
        "tests/test_ghc_family_lyren_moss_v679_v4_final.py",
    )
    match = re.search(r"(\d+) tests collected", result.stdout)
    if not match:
        raise RuntimeError("unable to parse collected test count")
    return int(match.group(1))


def run_tests_once() -> dict[str, Any]:
    result = command(
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/test_ghc_family_lyren_moss_v679_v4_x2.py",
        "tests/test_ghc_family_lyren_moss_v679_v4_final.py",
        check=False,
    )
    return {
        "exit_code": result.returncode,
        "stdout_tail": result.stdout[-4000:],
        "stderr_tail": result.stderr[-2000:],
    }


def verify(run_tests: bool) -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    local_branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", f"HEAD...{live}") if live else "missing"
    status = git("status", "--porcelain=v1")
    paths = changed_paths()
    owner = owner_paths()
    x1_manifest = read_json(VALIDATION / "x1-manifest.json")
    x2_manifest = read_json(VALIDATION / "x2-manifest.json")
    final_manifest = read_json(VALIDATION / "final-manifest.json")
    content_seal = read_json(VALIDATION / "final-content-seal.json")
    final_review = read_json(VALIDATION / "final-staged-review.json")
    terminal = read_json(PHASE / "final" / "terminal-truth.json")
    route = read_json(PHASE / "final" / "route-and-roster-overlay.json")
    handoff_meta = read_json(PHASE / "final" / "activation-candidate-metadata.json")
    handoff_path = ROOT / handoff_meta["path"]
    handoff_data = normalize(handoff_path.read_bytes())

    x1_replay = replay_manifest(head, x1_manifest["entries"])
    x2_replay = replay_manifest(head, x2_manifest["entries"])
    final_replay = replay_manifest(head, final_manifest["entries"])
    seal_replay = replay_manifest(head, content_seal["entries"])
    privacy = privacy_scan(owner)
    security = ast_security(paths)
    json_result = json_parse(owner)
    stale = []
    for relative in owner:
        path = ROOT / relative
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8")
            if ("Vesper " + "Rowan") in text or ("Rowan " + "Vesper") in text:
                stale.append(relative)

    parent = git("rev-parse", "HEAD^")
    evidence_parent = git("rev-parse", f"{EVIDENCE_HEAD}^")
    x1_parent = git("rev-parse", f"{X1_HEAD}^")
    commit_count = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    merges = [line for line in git("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines() if line]
    commits = [line for line in git("rev-list", "--reverse", f"{SOURCE}..HEAD").splitlines() if line]
    single_parent = all(len(git("rev-list", "--parents", "-n", "1", commit).split()) == 2 for commit in commits)
    collected = collect_tests()
    tests = run_tests_once() if run_tests else {"exit_code": None, "stdout_tail": "preflight_no_test_execution", "stderr_tail": ""}

    checks = {
        "exact_branch": local_branch == BRANCH,
        "clean_before_and_current": status == "",
        "upstream_equal": upstream == head,
        "tracking_equal": tracking == head,
        "fresh_live_equal": live == head,
        "zero_divergence": divergence.split() == ["0", "0"],
        "final_direct_child_of_evidence": parent == EVIDENCE_HEAD,
        "evidence_direct_child_of_x1": evidence_parent == X1_HEAD,
        "x1_direct_child_of_source": x1_parent == SOURCE,
        "three_new_commits": commit_count == 3,
        "zero_merges": len(merges) == 0,
        "all_new_commits_single_parent": single_parent,
        "commit_ceiling": commit_count <= 8,
        "owner_file_guard": len(paths) < 2000,
        "materialized_file_guard": sum(1 for path in ROOT.rglob("*") if path.is_file()) < 2000,
        "x1_manifest_exact": x1_manifest["entry_count"] == 20 and not x1_replay,
        "x2_manifest_exact": x2_manifest["entry_count"] == 331 and not x2_replay,
        "final_manifest_exact": final_manifest["entry_count"] >= 14 and not final_replay,
        "content_seal_exact": content_seal["entry_count"] == 12 and not seal_replay,
        "final_staged_review_passed": final_review["passed"] is True,
        "all_json_parses": not json_result["failures"],
        "privacy_scan_zero": privacy["confirmed_candidates"] == 0,
        "bounded_ast_security_zero": security["medium_or_high_findings"] == 0,
        "stale_label_zero": not stale,
        "outcome_labels_exact": terminal["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "terminal_verdict_preserved": terminal["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["route_state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and not route["precontact"],
        "handoff_digest_exact": sha(handoff_data) == handoff_meta["normalized_lf_sha256"] and len(handoff_data) == handoff_meta["normalized_lf_bytes"],
        "relational_boundary_preserved": read_json(PHASE / "final" / "wellbeing-and-boundaries.json")["names_roles_hopes_and_family_language_are_relational_only"] is True,
        "tests_collected": collected >= 40,
        "selected_tests_passed": (tests["exit_code"] == 0) if run_tests else True,
    }
    return {
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if run_tests and all(checks.values()) else ("VALID_EXACT_FINAL_PREFLIGHT" if not run_tests and all(checks.values()) else "FAILED"),
        "head": head,
        "branch": BRANCH,
        "checks": checks,
        "check_count": len(checks),
        "checks_passed": sum(checks.values()),
        "selected_test_methods_collected": collected,
        "tests": tests,
        "strict_json_parses": json_result["parsed"],
        "json_failures": json_result["failures"],
        "privacy": privacy,
        "security": security,
        "stale_labels": stale,
        "manifest_replays": {
            "x1": x1_manifest["entry_count"],
            "x2": x2_manifest["entry_count"],
            "final": final_manifest["entry_count"],
            "content_seal": content_seal["entry_count"],
            "total": x1_manifest["entry_count"] + x2_manifest["entry_count"] + final_manifest["entry_count"] + content_seal["entry_count"],
            "mismatches": x1_replay + x2_replay + final_replay + seal_replay,
        },
        "changed_owner_paths": len(paths),
        "materialized_files": sum(1 for path in ROOT.rglob("*") if path.is_file()),
        "same_owner_only": True,
        "full_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "complete_privacy_assurance": False,
        "complete_accessibility_assurance": False,
        "exhaustive_security": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def canonical() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    receipt_dir = RECEIPT_BANK / f"canonical-{head}"
    receipt_dir.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt_dir.mkdir(exist_ok=False)
    except FileExistsError as exc:
        raise RuntimeError("canonical receipt latch already exists; replay forbidden") from exc
    payload: dict[str, Any]
    try:
        payload = verify(run_tests=True)
    except Exception as exc:  # pragma: no cover - terminal retained failure path
        payload = {
            "state": "FAILED_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "head": head,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "canonical_success_credit": 0,
            "replay_forbidden_without_direct_child_correction": True,
        }
    payload["canonical_invocations"] = 1
    payload["canonical_successes"] = 1 if payload.get("state") == "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" else 0
    payload["canonical_replays"] = 0
    payload_raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt = {"payload_sha256": sha(payload_raw), "payload": payload}
    receipt_path = receipt_dir / f"canonical-{head}.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if payload.get("state") != "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL":
        raise RuntimeError(f"canonical failed; retained receipt at {receipt_path}")
    return {
        "state": payload["state"],
        "head": head,
        "checks": f"{payload['checks_passed']}/{payload['check_count']}",
        "selected_test_methods_collected": payload["selected_test_methods_collected"],
        "strict_json_parses": payload["strict_json_parses"],
        "privacy_files": payload["privacy"]["files_scanned"],
        "manifest_replays": payload["manifest_replays"]["total"],
        "payload_sha256": receipt["payload_sha256"],
        "receipt_path": str(receipt_path),
        "terminal_verdict": payload["terminal_verdict"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preflight", "canonical"))
    args = parser.parse_args()
    value = verify(run_tests=False) if args.mode == "preflight" else canonical()
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
