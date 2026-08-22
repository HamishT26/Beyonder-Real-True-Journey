#!/usr/bin/env python3
"""One-shot exact-final owner-delta validator for Tamar Vey v665-v3."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "docs/tamar-vey/v665-v3/"
BRANCH = "codex/GHC-Family/tamar-vey-v665-v3-full-tools"
SOURCE = "a559ab2dfe46cace97fd03c09f1018477fdc09f4"
X1 = "2198fa869c26c9672af02d2a2edde7ba8f14c1e3"
EVIDENCE = "015f9a618d71df1d5e4eb6c517e21ecf9d8556e9"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
OWNER_MANIFEST = f"{PREFIX}validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{PREFIX}validation/final-delta-manifest.json"
X1_MANIFEST = f"{PREFIX}x1/x1-content-manifest.json"
EVIDENCE_MANIFEST = f"{PREFIX}x2/validation/evidence-content-manifest.json"
TEST = "tests/test_ghc_family_tamar_v665_v3_closeout.py"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def blob(revision: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True
    ).stdout


def parse_json(revision: str, path: str) -> Any:
    return json.loads(blob(revision, path).decode("utf-8"))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def scan_candidates(path: str, raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8", errors="replace")
    patterns = {
        "windows_private_absolute_path": re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\"),
        "unix_private_absolute_path": re.compile(r"(?i)/(?:home|users)/[^\s'\"]+"),
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_callable_or_session_stream": re.compile(r"(?i)(?:mcp__[a-z0-9_]{6,}|session_stream\s*[:=]|resume_value\s*[:=])"),
    }
    return [
        {"path": path, "class": name}
        for name, pattern in patterns.items()
        if pattern.search(text)
    ]


def replay_manifest(revision: str, path: str) -> dict[str, Any]:
    manifest = parse_json(revision, path)
    mismatches = []
    for entry in manifest["entries"]:
        raw = blob(revision, entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    return {
        "path": path,
        "entry_count": len(manifest["entries"]),
        "declared_self_exclusions": len(manifest.get("declared_self_exclusions", [])),
        "mismatches": mismatches,
        "valid": not mismatches and manifest.get("coverage_valid") is True,
    }


def changed_python_security(head: str, paths: list[str]) -> dict[str, Any]:
    findings = []
    compiled = 0
    for path in paths:
        if not path.endswith(".py"):
            continue
        source = blob(head, path).decode("utf-8")
        compile(source, path, "exec")
        compiled += 1
        tree = ast.parse(source, filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    prefix = node.func.value.id if isinstance(node.func.value, ast.Name) else ""
                    name = f"{prefix}.{node.func.attr}" if prefix else node.func.attr
                if name in {"eval", "exec", "os.system", "pickle.loads", "marshal.loads"}:
                    findings.append({"path": path, "line": node.lineno, "call": name})
                if name in {"subprocess.run", "subprocess.Popen", "run"} and any(
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                    for keyword in node.keywords
                ):
                    findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    return {"compiled_python_files": compiled, "findings": findings, "valid": not findings}


def validate() -> dict[str, Any]:
    head_before = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    clean_before = git("status", "--porcelain=v1") == ""
    run("git", "fetch", "origin", BRANCH)
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else "ABSENT"
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}")
    final_parent = git("rev-parse", "HEAD^")
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..HEAD"))
    merges_raw = git("rev-list", "--merges", f"{SOURCE}..HEAD")
    merge_count = len(merges_raw.splitlines()) if merges_raw else 0
    owner_paths_raw = git("diff", "--name-only", "--diff-filter=ACMR", f"{SOURCE}..HEAD")
    owner_paths = sorted(line for line in owner_paths_raw.splitlines() if line)
    deletion_raw = git("diff", "--name-only", "--diff-filter=D", f"{SOURCE}..HEAD")
    deletion_paths = deletion_raw.splitlines() if deletion_raw else []

    manifests = [
        replay_manifest(X1, X1_MANIFEST),
        replay_manifest(EVIDENCE, EVIDENCE_MANIFEST),
        replay_manifest(head_before, DELTA_MANIFEST),
        replay_manifest(head_before, OWNER_MANIFEST),
    ]
    owner_manifest = parse_json(head_before, OWNER_MANIFEST)
    expected_owner_paths = sorted(
        [entry["path"] for entry in owner_manifest["entries"]]
        + owner_manifest["declared_self_exclusions"]
    )

    phase_paths_raw = git("ls-tree", "-r", "--name-only", head_before, PREFIX.rstrip("/"))
    phase_paths = sorted(line for line in phase_paths_raw.splitlines() if line)
    json_paths = [path for path in phase_paths if path.endswith(".json")]
    json_failures = []
    for path in json_paths:
        try:
            parse_json(head_before, path)
        except Exception as exc:
            json_failures.append({"path": path, "error": type(exc).__name__})

    markdown_paths = [
        f"{PREFIX}x1/x1-overview.md",
        f"{PREFIX}x2/x2-overview.md",
        f"{PREFIX}reports/final-integrated-overview.md",
        f"{PREFIX}handoffs/next-owner-activation-prepared.md",
    ]
    markdown_issues = []
    for path in markdown_paths:
        text = blob(head_before, path).decode("utf-8")
        if not text.startswith("# ") or "\n## " not in text:
            markdown_issues.append(path)
    overview_words = len(
        blob(head_before, f"{PREFIX}reports/final-integrated-overview.md")
        .decode("utf-8")
        .split()
    )
    report = blob(head_before, f"{PREFIX}reports/static-report.html").decode("utf-8")
    report_checks = {
        "doctype": report.casefold().startswith("<!doctype html>"),
        "lang": '<html lang="en">' in report,
        "skip_link": 'href="#main"' in report,
        "main_landmark": '<main id="main">' in report,
        "caption": "<caption>" in report,
        "visible_focus": ":focus" in report,
        "no_script": "<script" not in report.casefold(),
        "manual_reservation": "Manual keyboard" in report,
    }

    privacy_candidates = []
    owner_words = 0
    for path in owner_paths:
        raw = blob(head_before, path)
        privacy_candidates.extend(scan_candidates(path, raw))
        if path.endswith((".json", ".md", ".py", ".html")):
            owner_words += len(raw.decode("utf-8").split())
    security = changed_python_security(head_before, owner_paths)

    tests = run(sys.executable, TEST, "-v", check=False)
    test_text = tests.stdout + "\n" + tests.stderr
    test_count = len(re.findall(r"(?m)^test_\d+.*\.\.\. ok\s*$", test_text))

    truth = parse_json(head_before, f"{PREFIX}closeout/phase-truth.json")
    negatives = parse_json(head_before, f"{PREFIX}closeout/retained-negative-register.json")
    methods = parse_json(head_before, f"{PREFIX}closeout/method-flow-final.json")
    gates = parse_json(head_before, f"{PREFIX}closeout/exact-open-gate-register.json")
    delivery = parse_json(head_before, f"{PREFIX}closeout/delivery-state.json")
    canonical_contract = parse_json(head_before, f"{PREFIX}validation/final-canonical-contract.json")
    diff_check = run("git", "diff", "HEAD^", "HEAD", "--check", check=False)

    detailed = [
        ("branch_exact", branch == BRANCH),
        ("head_non_source", head_before not in {SOURCE, X1, EVIDENCE}),
        ("x1_parent_source", git("rev-parse", f"{X1}^") == SOURCE),
        ("evidence_parent_x1", git("rev-parse", f"{EVIDENCE}^") == X1),
        ("final_parent_evidence", final_parent == EVIDENCE),
        ("phase_commits_three", phase_commits == 3),
        ("zero_merges", merge_count == 0),
        ("clean_before", clean_before),
        ("upstream_equal", head_before == upstream),
        ("tracking_equal", head_before == tracking),
        ("fresh_live_equal", head_before == live),
        ("zero_divergence", divergence.replace("\t", " ").split() == ["0", "0"]),
        ("owner_path_parity", owner_paths == expected_owner_paths),
        ("zero_deletions", not deletion_paths),
        ("under_file_ceiling", len(owner_paths) < 2_000),
        ("under_word_ceiling", owner_words < 100_000),
        ("overview_three_page", overview_words >= 1_500),
        ("json_valid", not json_failures),
        ("markdown_valid", not markdown_issues),
        ("static_report_valid", all(report_checks.values())),
        ("privacy_zero", not privacy_candidates),
        ("security_zero", security["valid"]),
        ("tests_pass", tests.returncode == 0 and test_count > 0),
        ("all_manifests_valid", all(row["valid"] for row in manifests)),
        ("outcome_truth", truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}),
        ("negative_truth", negatives["effective_total"] == 25_425 and negatives["failure_erasure_count"] == 0),
        ("method_truth", methods["effective_total"] == 9_287 and methods["failure_erasure_count"] == 0),
        ("gate_truth", gates["open_gap_total"] == 177 and gates["exact_gate_total"] == 175 and gates["silently_closed_count"] == 0),
        ("zero_real_rows", truth["real_rows"] == 0),
        ("zero_authority_events", truth["authority_events"] == 0),
        ("same_owner_only", truth["same_owner_validation_only"] is True and truth["independent_reproduction"] is False),
        ("full_suite_not_run", truth["full_repository_suite_run"] is False),
        ("terminal_not_ready", truth["terminal_verdict"] == TERMINAL_VERDICT),
        ("delivery_unsent", delivery["successor_state"] == "PREPARED_NOT_SENT" and delivery["send_count"] == 0),
        ("canonical_contract_valid", canonical_contract["valid"] is True and canonical_contract["invocation_limit"] == 1),
        ("diff_hygiene", diff_check.returncode == 0),
    ]
    minimal_names = {
        "branch_exact",
        "final_parent_evidence",
        "phase_commits_three",
        "zero_merges",
        "clean_before",
        "fresh_live_equal",
        "owner_path_parity",
        "zero_deletions",
        "privacy_zero",
        "tests_pass",
        "all_manifests_valid",
        "negative_truth",
        "gate_truth",
        "terminal_not_ready",
        "delivery_unsent",
    }
    minimal = [(name, valid) for name, valid in detailed if name in minimal_names]
    valid = all(value for _, value in detailed) and all(value for _, value in minimal)
    head_after = git("rev-parse", "HEAD")
    clean_after = git("status", "--porcelain=v1") == ""
    valid = valid and head_before == head_after and clean_after
    return {
        "schema": "ghc.family.tamar.v665-v3.exact-final-canonical-receipt.v1",
        "scope": "exact source-to-final Tamar owner delta only",
        "head": head_before,
        "branch": branch,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "final_parent": final_parent,
        "phase_commits": phase_commits,
        "merge_commits": merge_count,
        "divergence": divergence,
        "four_way_equal": head_before == upstream == tracking == live,
        "clean_before": clean_before,
        "clean_after": clean_after,
        "head_stable": head_before == head_after,
        "tests": {"passed": test_count, "return_code": tests.returncode, "full_repository_suite": False},
        "detailed": {"passed": sum(value for _, value in detailed), "total": len(detailed), "checks": [{"name": name, "valid": value} for name, value in detailed]},
        "minimal": {"passed": sum(value for _, value in minimal), "total": len(minimal), "checks": [{"name": name, "valid": value} for name, value in minimal]},
        "json": {"parsed": len(json_paths), "failures": json_failures},
        "markdown": {"checked": len(markdown_paths), "issues": markdown_issues, "overview_words": overview_words},
        "static_report_checks": report_checks,
        "privacy": {"files_scanned": len(owner_paths), "classes": 5, "candidates": privacy_candidates, "confirmed_hits": 0 if not privacy_candidates else len(privacy_candidates)},
        "security": security,
        "manifests": manifests,
        "owner_paths": len(owner_paths),
        "owner_words": owner_words,
        "deletion_paths": deletion_paths,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": valid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.receipt.exists():
        print(json.dumps({"valid": False, "error": "exclusive_receipt_already_exists"}, sort_keys=True))
        return 2
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    try:
        payload = validate()
    except Exception as exc:
        payload = {
            "schema": "ghc.family.tamar.v665-v3.exact-final-canonical-receipt.v1",
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
            "terminal_verdict": TERMINAL_VERDICT,
        }
    payload["payload_sha256"] = sha256(canonical_bytes(payload))
    with args.receipt.open("xb") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")
    print(
        json.dumps(
            {
                "valid": payload.get("valid") is True,
                "head": payload.get("head"),
                "tests": payload.get("tests"),
                "detailed": payload.get("detailed", {}).get("passed"),
                "minimal": payload.get("minimal", {}).get("passed"),
                "json": payload.get("json", {}).get("parsed"),
                "privacy_hits": payload.get("privacy", {}).get("confirmed_hits"),
                "payload_sha256": payload["payload_sha256"],
            },
            sort_keys=True,
        )
    )
    return 0 if payload.get("valid") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
