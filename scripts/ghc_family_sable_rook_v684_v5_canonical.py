#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical validator for Sable v684-v5."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v684-v5"
SOURCE = "73321b3ff077c3f33726562b8e9d5952608a060e"
X1 = "699e42fe27678cc0e12a55c2d60ba029c62998b4"
EVIDENCE = "35073d785c63ab2bbf47260d66ca54e6865b877d"
BRANCH = "codex/GHC-Family/sable-rook-v684-v5-full-tools"


def git(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True
    ).stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_sha(data: bytes) -> str:
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = json.loads(git("show", f"{commit}:{path}"))
    failures = []
    for entry in manifest["entries"]:
        data = subprocess.run(
            ["git", "show", f"{commit}:{entry['path']}"],
            cwd=ROOT, check=True, capture_output=True
        ).stdout
        actual = normalized_sha(data)
        if actual != entry["sha256_normalized_lf"]:
            failures.append({"path": entry["path"], "expected": entry["sha256_normalized_lf"], "actual": actual})
    return {
        "path": path,
        "entries": len(manifest["entries"]),
        "self_exclusions": len(manifest.get("self_exclusions", [])),
        "failures": failures,
        "passed": not failures,
    }


def selected_tests(expected_head: str) -> dict[str, Any]:
    os.environ["SR6845_EXPECTED_FINAL"] = expected_head
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName("tests.test_ghc_family_sable_rook_v684_v5_final")
    result = unittest.TestResult()
    suite.run(result)
    failures = [test.id() for test, _ in result.failures]
    errors = [test.id() for test, _ in result.errors]
    return {
        "selected": result.testsRun,
        "passed": result.testsRun - len(failures) - len(errors),
        "failures": failures,
        "errors": errors,
        "success": result.wasSuccessful(),
    }


def bounded_privacy(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definition_files = {
        "scripts/build_ghc_family_sable_rook_v684_v5_x1.py",
        "scripts/build_ghc_family_sable_rook_v684_v5_x2.py",
        "scripts/build_ghc_family_sable_rook_v684_v5_final.py",
        "scripts/ghc_family_sable_rook_v684_v5_canonical.py",
    }
    candidates = []
    confirmed = []
    for rel in paths:
        path = ROOT / rel
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                item = {
                    "path": rel,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "class": label,
                    "disposition": "scanner_definition_not_payload" if rel in definition_files else "confirmed_payload_hit",
                }
                candidates.append(item)
                if rel not in definition_files:
                    confirmed.append(item)
    return {
        "pattern_classes": list(patterns),
        "files": len(paths),
        "candidates": candidates,
        "confirmed": confirmed,
        "passed": not confirmed,
    }


def bounded_ast(paths: list[str]) -> dict[str, Any]:
    findings = []
    python_paths = [path for path in paths if path.endswith(".py")]
    for rel in python_paths:
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append({"path": rel, "line": node.lineno, "finding": "eval"})
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                findings.append({"path": rel, "line": node.lineno, "finding": "system_call"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": rel, "line": node.lineno, "finding": "shell_true"})
    return {"python_files": len(python_paths), "findings": findings, "passed": not findings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    if args.receipt.exists():
        raise SystemExit("canonical receipt already exists; success replay refused")

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split("\t", 1)[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    clean_before = not git("status", "--porcelain=v1")

    owner_manifest = load(BASE / "validation" / "final-owner-manifest.json")
    owner_paths = [entry["path"] for entry in owner_manifest["entries"]]
    owner_paths.extend(owner_manifest["self_exclusions"])
    owner_paths = sorted(set(owner_paths))

    tests = selected_tests(args.expected_head)
    manifests = [
        replay_manifest(X1, "docs/sable-rook/v684-v5/validation/x1-index-manifest.json"),
        replay_manifest(EVIDENCE, "docs/sable-rook/v684-v5/validation/evidence-index-manifest.json"),
        replay_manifest(head, "docs/sable-rook/v684-v5/validation/final-delta-manifest.json"),
        replay_manifest(head, "docs/sable-rook/v684-v5/validation/final-owner-manifest.json"),
    ]
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    json_failures = []
    for rel in json_paths:
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except Exception as exc:  # bounded receipt, sanitized type only
            json_failures.append({"path": rel, "error": type(exc).__name__})
    privacy = bounded_privacy(owner_paths)
    security = bounded_ast(owner_paths)

    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_lines = git("rev-list", "--merges", f"{SOURCE}..{head}")
    merges = 0 if not merge_lines else len(merge_lines.splitlines())
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    single_parent_history = all(
        len(line.split()) == 2
        for line in git("rev-list", "--parents", f"{SOURCE}..{head}").splitlines()
        if line.strip()
    )
    ancestry = {
        "source": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=ROOT).returncode == 0,
        "x1": subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=ROOT).returncode == 0,
        "evidence": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=ROOT).returncode == 0,
    }

    detailed = {
        "exact_head": head == args.expected_head,
        "exact_branch": branch == BRANCH,
        "direct_evidence_parent": len(parents) == 2 and parents[1] == EVIDENCE,
        "source_ancestry": ancestry["source"],
        "x1_ancestry": ancestry["x1"],
        "evidence_ancestry": ancestry["evidence"],
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merges == 0,
        "single_parent_history": single_parent_history,
        "one_final_parent": len(parents) == 2,
        "clean_before": clean_before,
        "typed_zero_ahead": divergence == ["0", "0"],
        "local_upstream_equal": head == upstream,
        "local_tracking_equal": head == tracking,
        "local_live_equal": head == live,
        "selected_tests": tests["success"],
        "x1_manifest": manifests[0]["passed"],
        "evidence_manifest": manifests[1]["passed"],
        "final_delta_manifest": manifests[2]["passed"],
        "final_owner_manifest": manifests[3]["passed"],
        "strict_json": not json_failures,
        "privacy": privacy["passed"],
        "security": security["passed"],
        "owner_file_ceiling": len(owner_paths) < 2000,
        "handoff_word_range": load(BASE / "closeout" / "handoff-candidate-receipt.json")["within_range"],
        "terminal_verdict": load(BASE / "final" / "phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_held": load(BASE / "closeout" / "route-readiness.json")["state"] == "PREPARED_NOT_SENT",
        "route_send_count_zero": load(BASE / "closeout" / "route-readiness.json")["send_count"] == 0,
        "four_outcome_labels": set(load(BASE / "final" / "source-and-proposal-ledger.json")["allowed_labels"]) == {"completed", "represented", "open_gap", "exact_gate"},
        "outcome_counts": load(BASE / "final" / "final-summary.json")["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "positive_controls": load(BASE / "closeout" / "evidence-receipt.json")["positive_controls"]["passed"] == 60,
        "rejecting_mutations": load(BASE / "closeout" / "evidence-receipt.json")["rejecting_mutations"]["rejected"] == 300,
        "skills": load(BASE / "closeout" / "evidence-receipt.json")["skills"]["quick_validated"] == 20,
        "runners": load(BASE / "closeout" / "evidence-receipt.json")["runners"]["passed"] == 10,
        "negative_nonerasure": load(BASE / "closeout" / "retained-negative-register.json")["effective_negatives"] == 59408,
        "open_gaps": load(BASE / "closeout" / "gate-register.json")["open_gaps"] == 528,
        "exact_gates": load(BASE / "closeout" / "gate-register.json")["exact_gates"] == 518,
        "no_silent_gate_close": load(BASE / "closeout" / "gate-register.json")["silently_closed"] == 0,
        "canonical_budget_one": load(BASE / "closeout" / "final-validation-candidate.json")["canonical_invocation_budget"] == 1,
        "no_success_replay": load(BASE / "closeout" / "final-validation-candidate.json")["replay_after_success"] is False,
    }
    minimal_names = [
        "exact_head", "direct_evidence_parent", "three_phase_commits", "zero_merges",
        "single_parent_history", "clean_before", "typed_zero_ahead",
        "local_upstream_equal", "local_tracking_equal", "local_live_equal",
        "selected_tests", "final_owner_manifest", "strict_json", "privacy",
        "terminal_verdict",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    clean_after = not git("status", "--porcelain=v1")
    success = (
        all(detailed.values())
        and all(minimal.values())
        and clean_after
        and tests["success"]
        and all(item["passed"] for item in manifests)
        and not json_failures
        and privacy["passed"]
        and security["passed"]
    )
    payload = {
        "schema": "ghc.family.exact-final-canonical.v2",
        "phase": "v684-v5",
        "owner": "Sable Rook",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
        "canonical_invocations": 1,
        "canonical_successes": 1 if success else 0,
        "replay_after_success": False,
        "expected_head": args.expected_head,
        "observed_head": head,
        "branch": branch,
        "tests": tests,
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json": {"parsed": len(json_paths) - len(json_failures), "total": len(json_paths), "failures": json_failures},
        "manifests": manifests,
        "manifest_entries": sum(item["entries"] for item in manifests),
        "privacy": privacy,
        "security": security,
        "owner_files": len(owner_paths),
        "clean_before": clean_before,
        "clean_after": clean_after,
        "same_owner_only": True,
        "independent_reproduction": False,
        "full_repository_suite": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Bounded same-owner software and documentation evidence only; no empirical, professional, production, legal, cultural, Māori-authority, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness or personhood, Theory of Everything, proof, canon, or Stage 20 claim.",
    }
    hash_basis = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(hash_basis).hexdigest()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "status": payload["status"],
        "tests": f"{tests['passed']}/{tests['selected']}",
        "detailed": f"{payload['detailed']['passed']}/{payload['detailed']['total']}",
        "minimal": f"{payload['minimal']['passed']}/{payload['minimal']['total']}",
        "json": f"{payload['json']['parsed']}/{payload['json']['total']}",
        "manifest_entries": payload["manifest_entries"],
        "owner_files": payload["owner_files"],
        "privacy_confirmed": len(privacy["confirmed"]),
        "security_findings": len(security["findings"]),
    }))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
