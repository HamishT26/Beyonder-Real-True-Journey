#!/usr/bin/env python3
"""Exclusive exact-final owner-scoped canonical validator for Sable v687-v3."""

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
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
SOURCE = "71e94d1699eea013c82bef0b7a7e081ac6e43c8c"
X1 = "1a57a093dff78bcb217de33f9c5f282d3ee8bf17"
EVIDENCE = "f08302a468e819a0e89280333d980b8d4ac6a4f7"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"
SKILLS = [
    "ghc-family-jcs-canonical-profile", "ghc-family-confusable-nonidentity",
    "ghc-family-digest-migration-ledger", "ghc-family-receipt-expiry-conjunction",
    "ghc-family-event-branch-conflict", "ghc-family-checkpoint-parent-fixity",
    "ghc-family-artifact-budget-uncertainty", "ghc-family-accessible-codec-comparison",
    "ghc-family-gmut-claim-firewall", "ghc-family-authority-vacancy-matrix",
]
RUNNERS = [
    "ghc_family_sable_rook_v687_v3_jcs_canonical_profile.py",
    "ghc_family_sable_rook_v687_v3_confusable_nonidentity.py",
    "ghc_family_sable_rook_v687_v3_digest_migration_ledger.py",
    "ghc_family_sable_rook_v687_v3_receipt_expiry_conjunction.py",
    "ghc_family_sable_rook_v687_v3_event_branch_conflict.py",
    "ghc_family_sable_rook_v687_v3_contracts.py",
]


def git(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True,
    ).stdout.strip()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = json.loads(git("show", f"{commit}:{path}"))
    failures = []
    for entry in manifest["entries"]:
        data = subprocess.run(["git", "show", f"{commit}:{entry['path']}"], cwd=ROOT, check=True, capture_output=True).stdout
        data = normalized(data)
        actual = hashlib.sha256(data).hexdigest()
        if len(data) != entry["bytes_normalized_lf"] or actual != entry["sha256_normalized_lf"]:
            failures.append({"path": entry["path"], "actual": actual})
    return {"path": path, "entries": len(manifest["entries"]), "self_exclusions": len(manifest.get("self_exclusions", [])), "failures": failures, "passed": not failures}


def selected_tests(expected_head: str) -> dict[str, Any]:
    os.environ["SR6873_EXPECTED_FINAL"] = expected_head
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    suite = unittest.TestLoader().loadTestsFromName("tests.test_ghc_family_sable_rook_v687_v3_final")
    result = unittest.TestResult()
    suite.run(result)
    failures = [test.id() for test, _ in result.failures]
    errors = [test.id() for test, _ in result.errors]
    return {"selected": result.testsRun, "passed": result.testsRun - len(failures) - len(errors), "failures": failures, "errors": errors, "success": result.wasSuccessful()}


def privacy(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definitions = {
        "build_ghc_family_sable_rook_v687_v3_x1.py", "build_ghc_family_sable_rook_v687_v3_x2.py",
        "build_ghc_family_sable_rook_v687_v3_final.py", "ghc_family_sable_rook_v687_v3_canonical.py",
    }
    candidates = []
    confirmed = []
    for rel in paths:
        path = ROOT / rel
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt", ".lock"}:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition_not_payload" if path.name in definitions else "confirmed_payload_hit"
                row = {"path": rel, "line": text.count("\n", 0, match.start()) + 1, "class": label, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {"pattern_classes": list(patterns), "files": len(paths), "candidates": candidates, "confirmed": confirmed, "passed": not confirmed}


def security(paths: list[str]) -> dict[str, Any]:
    findings = []
    python_paths = [rel for rel in paths if rel.endswith(".py")]
    for rel in python_paths:
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append({"path": rel, "line": node.lineno, "finding": "eval"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": rel, "line": node.lineno, "finding": "shell_true"})
    return {"python_files": len(python_paths), "findings": findings, "passed": not findings, "exhaustive_security": False}


def promotion_parity(global_skill_root: Path, global_script_root: Path) -> dict[str, Any]:
    failures = []
    skill_files = 0
    for name in SKILLS:
        source = BASE / "skills" / name
        target = global_skill_root / name
        for path in [p for p in source.rglob("*") if p.is_file()]:
            skill_files += 1
            other = target / path.relative_to(source)
            if not other.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != hashlib.sha256(other.read_bytes()).hexdigest():
                failures.append(f"{name}/{path.relative_to(source).as_posix()}")
    for name in RUNNERS:
        source = ROOT / "scripts" / name
        target = global_script_root / name
        if not target.exists() or hashlib.sha256(source.read_bytes()).hexdigest() != hashlib.sha256(target.read_bytes()).hexdigest():
            failures.append(name)
    return {"skills": len(SKILLS), "skill_files": skill_files, "shared_runners": 5, "dependency_files": 1, "failures": failures, "passed": not failures}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--global-skill-root", required=True, type=Path)
    parser.add_argument("--global-script-root", required=True, type=Path)
    args = parser.parse_args()
    if args.receipt.exists():
        raise SystemExit("exclusive canonical receipt already exists; replay refused")

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{branch}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    live = live_line.split("\t", 1)[0] if live_line else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    clean_before = not git("status", "--porcelain=v1")

    owner_manifest = load(BASE / "validation" / "final-owner-manifest.json")
    owner_paths = sorted({entry["path"] for entry in owner_manifest["entries"]} | set(owner_manifest["self_exclusions"]))
    tests = selected_tests(args.expected_head)
    manifests = [
        replay_manifest(X1, "docs/sable-rook/v687-v3/validation/x1-manifest.json"),
        replay_manifest(EVIDENCE, "docs/sable-rook/v687-v3/validation/x2-manifest.json"),
        replay_manifest(head, "docs/sable-rook/v687-v3/validation/final-delta-manifest.json"),
        replay_manifest(head, "docs/sable-rook/v687-v3/validation/final-owner-manifest.json"),
    ]
    json_paths = [rel for rel in owner_paths if rel.endswith(".json")]
    json_failures = []
    for rel in json_paths:
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except Exception as exc:
            json_failures.append({"path": rel, "error_class": type(exc).__name__})
    privacy_result = privacy(owner_paths)
    security_result = security(owner_paths)
    promotions = promotion_parity(args.global_skill_root, args.global_script_root)

    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merge_lines = git("rev-list", "--merges", f"{SOURCE}..{head}")
    merges = 0 if not merge_lines else len(merge_lines.splitlines())
    parent_tokens = git("rev-list", "--parents", "-n", "1", head).split()
    history = [line for line in git("rev-list", "--parents", f"{SOURCE}..{head}").splitlines() if line]
    all_single_parent = all(len(line.split()) == 2 for line in history)
    baton = load(BASE / "handoffs" / "baton-index.json")
    seal = load(BASE / "closeout" / "content-seal.json")
    seal_failures = []
    for entry in seal["targets"]:
        data = normalized((ROOT / entry["path"]).read_bytes())
        if hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            seal_failures.append(entry["path"])
    counts = load(BASE / "final" / "phase-truth.json")["effective_counts"]
    detailed = {
        "exact_head": head == args.expected_head,
        "exact_branch": branch == BRANCH,
        "direct_evidence_parent": len(parent_tokens) == 2 and parent_tokens[1] == EVIDENCE,
        "source_ancestry": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=ROOT).returncode == 0,
        "x1_ancestry": subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=ROOT).returncode == 0,
        "evidence_ancestry": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=ROOT).returncode == 0,
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merges == 0,
        "all_single_parent": all_single_parent,
        "one_final_parent": len(parent_tokens) == 2,
        "clean_before": clean_before,
        "typed_zero_divergence": divergence == ["0", "0"],
        "local_upstream_equal": head == upstream,
        "local_tracking_equal": head == tracking,
        "local_fresh_live_equal": head == live,
        "final_tests": tests["success"],
        "x1_manifest": manifests[0]["passed"],
        "x2_manifest": manifests[1]["passed"],
        "final_delta_manifest": manifests[2]["passed"],
        "final_owner_manifest": manifests[3]["passed"],
        "strict_json": not json_failures,
        "five_class_privacy": privacy_result["passed"],
        "bounded_ast_security": security_result["passed"],
        "promotion_parity": promotions["passed"],
        "content_seal": not seal_failures,
        "owner_file_ceiling": len(owner_paths) < 2000,
        "baton_word_range": 10000 <= baton["words"] <= 100000,
        "baton_modules": len(baton["modules"]) == 13,
        "baton_eof": (BASE / "handoffs" / "future-seat-08-v687-v4-activation-candidate.md").read_text(encoding="utf-8").rstrip().endswith(baton["eof"]),
        "outcome_counts": load(BASE / "final" / "phase-truth.json")["outcomes"] == {"completed": 160, "represented": 20, "open_gap": 10, "exact_gate": 10},
        "negative_nonerasure": counts["effective_negatives"] == 77893,
        "open_gaps": counts["open_gaps"] == 674,
        "exact_gates": counts["exact_gates"] == 659,
        "route_held": load(BASE / "closeout" / "route-readiness.json")["state"] == "PREPARED_NOT_CREATED",
        "creation_count_zero": load(BASE / "closeout" / "route-readiness.json")["creation_count"] == 0,
        "caelen_not_contacted": load(BASE / "closeout" / "route-readiness.json")["caelen_contacted"] is False,
        "canonical_budget_one": load(BASE / "closeout" / "final-validation-candidate.json")["canonical_invocation_budget"] == 1,
        "no_success_replay": load(BASE / "closeout" / "final-validation-candidate.json")["replay_after_success"] is False,
        "full_repository_suite_false": load(BASE / "closeout" / "final-validation-candidate.json")["full_repository_suite"] is False,
        "terminal_verdict": load(BASE / "final" / "phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    minimal_names = [
        "exact_head", "direct_evidence_parent", "three_phase_commits", "zero_merges",
        "all_single_parent", "clean_before", "typed_zero_divergence",
        "local_upstream_equal", "local_tracking_equal", "local_fresh_live_equal",
        "final_tests", "final_owner_manifest", "strict_json", "five_class_privacy",
        "terminal_verdict",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    clean_after = not git("status", "--porcelain=v1")
    success = all(detailed.values()) and all(minimal.values()) and clean_after
    payload = {
        "schema": "ghc.family.sable-exact-final.v687.v3", "phase": "v687-v3", "owner": "Sable Rook",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
        "canonical_invocation_count": 1, "canonical_success_count": 1 if success else 0,
        "canonical_replay_count": 0, "canonical_replayed": False,
        "expected_head": args.expected_head, "head": head, "branch": branch,
        "tests": tests, "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "manifests": manifests, "manifest_bindings": sum(row["entries"] for row in manifests),
        "json": {"parsed": len(json_paths) - len(json_failures), "total": len(json_paths), "failures": json_failures},
        "privacy": privacy_result, "security": security_result, "promotions": promotions,
        "content_seal": {"targets": len(seal["targets"]), "failures": seal_failures},
        "owner_files": len(owner_paths), "clean_before": clean_before, "clean_after": clean_after,
        "complete_repository_suite": False, "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "Bounded same-owner synthetic software and documentation evidence only; no empirical, participant, professional, production, legal, cultural, Māori-authority, complete privacy/accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim.",
    }
    basis = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(basis).hexdigest()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": payload["status"], "tests": f"{tests['passed']}/{tests['selected']}", "detailed": f"{payload['detailed']['passed']}/{payload['detailed']['total']}", "minimal": f"{payload['minimal']['passed']}/{payload['minimal']['total']}", "json": f"{payload['json']['parsed']}/{payload['json']['total']}", "manifest_bindings": payload["manifest_bindings"], "owner_files": payload["owner_files"], "privacy_confirmed": len(privacy_result["confirmed"]), "security_findings": len(security_result["findings"]), "promotion_failures": len(promotions["failures"])}))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
