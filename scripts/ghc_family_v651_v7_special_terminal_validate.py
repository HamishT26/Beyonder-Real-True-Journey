#!/usr/bin/env python3
"""Run the single exact-head terminal validation for Vesper v651-v7 special."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PHASE_REL = "docs/vesper-arlen/v651-v7-special-cli-prep"
BASE = "96684c6fd22b33254aa37de2db7990f2e28bd88e"
X1 = "07785aa97b0aa46a4fbf0c60109a8ee8e678aacf"
EVIDENCE = "4dda60a276f4401d5dc52eaddf6c4ff14fadc4c0"
BRANCH = "codex/GHC-Family/vesper-arlen-v651-v7-special-cli-prep"
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".yaml", ".yml", ".py"}
OWNER_GLOBALS = {
    "scripts/build_ghc_family_v651_v7_special_preregistration.py",
    "scripts/build_ghc_family_v651_v7_special_execution.py",
    "scripts/build_ghc_family_v651_v7_special_closeout.py",
    "scripts/ghc_family_baton_pointer_guard.py",
    "scripts/ghc_family_cli_capability_contract.py",
    "scripts/ghc_family_cli_route_coverage.py",
    "scripts/ghc_family_sparse_lane_guard.py",
    "scripts/ghc_family_v651_v7_special_cli_batch.py",
    "scripts/ghc_family_v651_v7_special_evidence_validate.py",
    "scripts/ghc_family_v651_v7_special_manifest.py",
    "scripts/ghc_family_v651_v7_special_x1_validate.py",
    "scripts/ghc_family_v651_v7_special_final_stage_validate.py",
    "scripts/ghc_family_v651_v7_special_terminal_validate.py",
    "tests/test_ghc_family_v651_v7_special_x1.py",
    "tests/test_ghc_family_v651_v7_special_x2.py",
    "tests/test_ghc_family_v651_v7_special_closeout.py",
}
SCANNER_DEFINITIONS = {
    "scripts/ghc_family_v651_v7_special_evidence_validate.py",
    "scripts/ghc_family_v651_v7_special_final_stage_validate.py",
    "scripts/ghc_family_v651_v7_special_terminal_validate.py",
}
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file|vscode)://"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret)\s*[:=]\s*[^\s,}\]]+"),
    "delegation_markup": re.compile(r"(?i)<\s*codex_delegation\b"),
}


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, capture_output=True, text=True,
        encoding="utf-8", check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def blob(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout


def load_at(commit: str, relative: str) -> dict[str, Any]:
    return json.loads(blob(commit, f"{PHASE_REL}/{relative}").decode("utf-8"))


def tree_map(commit: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in git("ls-tree", "-r", commit).splitlines():
        meta, path = row.split("\t", 1)
        result[path] = meta.split()[2]
    return result


def run_tests() -> dict[str, Any]:
    suite = unittest.defaultTestLoader.loadTestsFromNames(
        [
            "tests.test_ghc_family_v651_v7_special_x1",
            "tests.test_ghc_family_v651_v7_special_x2",
            "tests.test_ghc_family_v651_v7_special_closeout",
        ]
    )
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "output": stream.getvalue()[-2000:],
    }


def verify_manifest(commit: str, tree: dict[str, str]) -> dict[str, Any]:
    relative = f"{PHASE_REL}/validation/final-owner-manifest.json"
    payload = json.loads(blob(commit, relative).decode("utf-8"))
    phase_paths = {path for path in tree if path.startswith(PHASE_REL + "/")}
    exclusions = set(payload["self_exclusions"])
    listed = {row["path"] for row in payload["entries"]}
    mismatches = []
    for row in payload["entries"]:
        data = blob(commit, row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    missing_exclusions = sorted(path for path in exclusions if path not in tree)
    return {
        "valid": payload.get("domain") == "index" and listed == phase_paths - exclusions and not mismatches and not missing_exclusions,
        "entries": payload["entry_count"],
        "domain_equal": listed == phase_paths - exclusions,
        "mismatches": mismatches,
        "missing_exclusions": missing_exclusions,
        "exclusions": sorted(exclusions),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})

    status_before = git("status", "--porcelain=v1").splitlines()
    run("git", "fetch", "origin", BRANCH, "--quiet")
    head = git("rev-parse", "HEAD")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_rows = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_rows[0].split()[0] if live_rows else ""
    divergence = git("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    branch = git("branch", "--show-current")
    check("clean_before", not status_before, status_before, [])
    check("exact_head", head == args.expected_head, head, args.expected_head)
    check("exact_branch", branch == BRANCH, branch, BRANCH)
    check("four_way_equality", len({head, upstream, tracking, live}) == 1, {"local": head, "upstream": upstream, "tracking": tracking, "live": live}, "all exact head")
    check("zero_divergence", divergence == ["0", "0"], divergence, ["0", "0"])

    commits = [row for row in git("rev-list", "--reverse", f"{BASE}..{head}").splitlines() if row]
    merges = [row for row in git("rev-list", "--merges", f"{BASE}..{head}").splitlines() if row]
    parent_counts = {commit: len(git("rev-list", "--parents", "-n", "1", commit).split()) - 1 for commit in commits}
    check("special_commit_count", len(commits) == 3, commits, "three special commits")
    check("zero_merges", not merges, merges, [])
    check("single_parent_history", all(value == 1 for value in parent_counts.values()), parent_counts, "one parent each")
    check("final_direct_child_of_evidence", git("rev-parse", f"{head}^") == EVIDENCE, git("rev-parse", f"{head}^"), EVIDENCE)
    ancestry = {anchor: run("git", "merge-base", "--is-ancestor", anchor, head, check=False).returncode == 0 for anchor in (BASE, X1, EVIDENCE)}
    check("anchor_ancestry", all(ancestry.values()), ancestry, "all ancestral")

    tests = run_tests()
    check("scoped_tests", tests["successful"] and tests["tests_run"] == 26, tests, "26 passing tests")
    check("no_test_skips", tests["skipped"] == 0, tests["skipped"], 0)

    tree = tree_map(head)
    phase_paths = sorted(path for path in tree if path.startswith(PHASE_REL + "/"))
    changed = sorted(path for path in git("diff", "--name-only", BASE, head).splitlines() if path)
    out_of_scope = [path for path in changed if not path.startswith(PHASE_REL + "/") and path not in OWNER_GLOBALS]
    absent_globals = sorted(path for path in OWNER_GLOBALS if path not in tree)
    check("owner_scope", not out_of_scope and not absent_globals, {"out_of_scope": out_of_scope, "absent_globals": absent_globals}, "exact owner scope")

    json_failures = []
    json_paths = [path for path in phase_paths if path.endswith(".json")]
    for path in json_paths:
        try:
            json.loads(blob(head, path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_failures.append({"path": path, "error": type(exc).__name__})
    check("phase_json_parse", not json_failures, {"parsed": len(json_paths) - len(json_failures), "total": len(json_paths), "issues": json_failures}, "all parse")

    scan_paths = sorted(set(phase_paths) | OWNER_GLOBALS)
    privacy_candidates: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    scanned = 0
    for path in scan_paths:
        if Path(path).suffix.lower() not in TEXT_SUFFIXES:
            continue
        scanned += 1
        text = blob(head, path).decode("utf-8", errors="replace")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                row = {"path": path, "class": label}
                if path in SCANNER_DEFINITIONS:
                    privacy_candidates.append(row)
                else:
                    privacy_hits.append(row)
    check("privacy_scan", not privacy_hits, {"files": scanned, "classes": len(PATTERNS), "candidates": privacy_candidates, "confirmed": privacy_hits}, "zero confirmed hits")

    manifest = verify_manifest(head, tree)
    check("owner_manifest", manifest["valid"], manifest, "exact HEAD phase manifest")
    stage_review = load_at(head, "validation/final-staged-review.json")
    check("staged_review", stage_review["valid"] and stage_review["tests"]["tests_run"] == 26, {"valid": stage_review["valid"], "tests": stage_review["tests"]["tests_run"], "checks": f"{stage_review['checks_passed']}/{stage_review['check_count']}"}, "passing staged review")

    truth = load_at(head, "truth/phase-truth.json")
    negative = load_at(head, "truth/retained-negative-register.json")
    method = load_at(head, "method-flow/method-flow-summary.json")
    closeout = load_at(head, "closeout/closeout-receipt.json")
    seal = load_at(head, "seal/seal-receipt.json")
    final = load_at(head, "final/final-record.json")
    plan = load_at(head, "validation/terminal-validation-plan.json")
    batch = load_at(head, "cli/cli-batch-receipt.json")
    environment = load_at(head, "environment/environment-version-receipt.json")
    baton_guard = load_at(head, "validation/baton-pointer-guard.json")
    check("outcomes", truth["outcomes"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, truth["outcomes"], "23/5/1/1")
    check("negative_arithmetic", truth["effective_negatives"] == negative["effective_total"] == 7570 and negative["failures_erased"] == 0, {"truth": truth["effective_negatives"], "register": negative["effective_total"], "erased": negative["failures_erased"]}, "7570 and zero erased")
    check("gate_arithmetic", (truth["effective_open_gaps"], truth["effective_exact_gates"]) == (59, 60), [truth["effective_open_gaps"], truth["effective_exact_gates"]], [59, 60])
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
    check("method_flow", method["valid"] and method["counts"]["states"]["preferred"] == 10 and method["counts"]["witness_results"] == {"fail": 12, "pass": 11}, method["counts"], "10 preferred, 12 fail, 11 pass")
    check("future_seats", batch["prepare_passes"] == 8 and batch["launch_refusals"] == 8 and batch["all_unnamed"] and batch["all_unlaunched"] and environment["future_cli_processes_launched"] == 0, {"prepared": batch["prepare_passes"], "refused": batch["launch_refusals"], "unnamed": batch["all_unnamed"], "unlaunched": batch["all_unlaunched"], "processes": environment["future_cli_processes_launched"]}, "8 prepared, zero named or launched")
    check("immediate_route", truth["immediate_successor"] == "Ilyra Fen" and truth["immediate_successor_phase"] == "v651-v8", [truth["immediate_successor"], truth["immediate_successor_phase"]], ["Ilyra Fen", "v651-v8"])
    check("delivery_pre_send", truth["terminal_delivery_state"] == "PREPARED_NOT_SENT" and final["delivery_state"] == "PREPARED_NOT_SENT", [truth["terminal_delivery_state"], final["delivery_state"]], ["PREPARED_NOT_SENT", "PREPARED_NOT_SENT"])
    check("closeout_seal", closeout["complete"] and seal["state"] == "READY_FOR_FINAL_COMMIT" and seal["future_cli_created"] == 0, {"closeout": closeout["complete"], "seal": seal["state"], "future_cli_created": seal["future_cli_created"]}, "sealed candidate with zero future CLI creation")
    check("single_pass_policy", plan["single_canonical_pass"] and not plan["replay_after_success"] and not plan["full_repository_suite"]["run"] and plan["full_repository_suite"]["owner"] == "Eiren Kestrel", plan, "one Vesper pass, no replay, full suite Eiren-only")
    check("baton_pointer", baton_guard["valid"] and 10000 <= baton_guard["baton_words"] <= 100000 and baton_guard["privacy_hits"] == [], baton_guard, "valid file-backed baton and compact pointer")
    check("nonclaim", final["same_owner_only"] and not final["independent_reproduction"], {"same_owner": final["same_owner_only"], "independent": final["independent_reproduction"]}, "same-owner only")

    oversized = []
    stale = []
    for path in phase_paths:
        if Path(path).suffix.lower() not in {".md", ".txt", ".html"}:
            continue
        text = blob(head, path).decode("utf-8", errors="replace")
        words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", text))
        if words > 100000:
            oversized.append({"path": path, "words": words})
        if ("Vesper " + "Arien") in text or ("v651-v7 " + "(SPECIAL)") in text:
            stale.append(path)
    check("document_word_cap", not oversized, oversized, "all at or below 100000")
    check("stale_label_review", not stale, stale, [])
    diff_check = run("git", "diff", "--check", BASE, head, check=False)
    check("diff_hygiene", diff_check.returncode == 0, diff_check.stdout + diff_check.stderr, "clean")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and path.name != ".git")
    check("materialized_limit", materialized < 2000, materialized, "below 2000")

    status_after = git("status", "--porcelain=v1").splitlines()
    check("clean_after", not status_after, status_after, [])
    minimal_names = {
        "clean_before", "exact_head", "four_way_equality", "zero_divergence",
        "special_commit_count", "zero_merges", "anchor_ancestry", "scoped_tests",
        "phase_json_parse", "privacy_scan", "owner_manifest", "outcomes",
        "terminal_verdict", "clean_after",
    }
    passed = sum(row["passed"] for row in checks)
    minimal_passed = sum(row["passed"] for row in checks if row["name"] in minimal_names)
    payload = {
        "schema": "ghc.family.v651-v7-special.terminal-validation.v1",
        "valid": passed == len(checks),
        "exact_head": head,
        "checks_passed": passed,
        "check_count": len(checks),
        "minimal_checks_passed": minimal_passed,
        "minimal_check_count": len(minimal_names),
        "checks": checks,
        "tests": tests,
        "json_files": len(json_paths),
        "privacy_files": scanned,
        "privacy_pattern_classes": len(PATTERNS),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": privacy_hits,
        "manifest_entries": manifest["entries"],
        "phase_files": len(phase_paths),
        "special_commits": len(commits),
        "merge_commits": len(merges),
        "four_way_equal": len({head, upstream, tracking, live}) == 1,
        "same_owner_only": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "full_repository_suite_owner": "Eiren Kestrel",
        "canonical_terminal_pass_number": 1,
        "replay_after_success": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One exact-head same-owner terminal validation only; not independent reproduction, external audit, production certification, scientific confirmation, authority, or Stage 20 evidence.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": payload["valid"], "head": head, "tests": tests["tests_run"], "detailed": f"{passed}/{len(checks)}", "minimal": f"{minimal_passed}/{len(minimal_names)}", "json": len(json_paths), "privacy_files": scanned, "manifest": manifest["entries"], "commits": len(commits), "merges": len(merges), "four_way_equal": payload["four_way_equal"]}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
