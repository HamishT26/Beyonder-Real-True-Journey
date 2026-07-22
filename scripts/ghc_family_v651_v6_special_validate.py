#!/usr/bin/env python3
"""Run the one-shot exact-head scoped validation for Elaren v651-v6 special."""

from __future__ import annotations

import argparse
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/elaren-kestrel/v651-v6"
PHASE = ROOT / "docs/elaren-kestrel/v651-v6-special-cli-prep"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
BASE_FINAL = "7911fc2ff2f95d2e8723dbd396272f4a78d46a9f"
SPECIAL_PREP_COMMIT = "f40d1e0f1a5158a8747ed57cc04a513979f5ebe7"
BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
TEST_MODULES = [
    "tests.test_ghc_family_v651_v6_x1",
    "tests.test_ghc_family_v651_v6_x2",
    "tests.test_ghc_family_v651_v6_special_cli_prep",
]
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".py", ".yaml", ".yml", ".tex", ".mjs", ".cjs", ".js"}
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_uri": re.compile(r"(?i)\b(?:thread|task|session|codex)://\S+"),
    "absolute_local_path": re.compile(r"(?i)(?:^|[\s\"'])(?:[a-z]:[\\/]|\\\\)[^\s\"']+"),
    "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)\s*[:=]\s*\S+"),
    "delegation_markup": re.compile(r"(?i)<\/?codex_delegation\b"),
}


def command(*args: str, timeout: int = 60, check: bool = True) -> str:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    if check and result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(args[:3])}")
    return result.stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run_tests() -> dict[str, Any]:
    if str(ROOT) in sys.path:
        sys.path.remove(str(ROOT))
    sys.path.insert(0, str(ROOT))
    loader = unittest.TestLoader()
    suite = unittest.TestSuite(loader.loadTestsFromName(name) for name in TEST_MODULES)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "modules": TEST_MODULES,
        "tests_run": result.testsRun,
        "failures": [case.id() for case, _ in result.failures],
        "errors": [case.id() for case, _ in result.errors],
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
    }


def tracked_surface() -> list[tuple[str, str]]:
    specs = [
        "docs/elaren-kestrel/v651-v6-special-cli-prep",
        "scripts/build_ghc_family_v651_v6_special_cli_prep.py",
        "scripts/ghc_family_v651_v6_special_validate.py",
        "tests/test_ghc_family_v651_v6_special_cli_prep.py",
    ]
    output = command("git", "ls-tree", "-r", "HEAD", "--", *specs)
    rows = []
    for line in output.splitlines():
        left, path = line.split("\t", 1)
        _mode, kind, blob = left.split()
        if kind == "blob":
            rows.append((path, blob))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--canonical-pass", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    issues: list[str] = []

    def check(name: str, passed: bool, observed: Any, expected: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})
        if not passed:
            issues.append(name)

    clean_before_rows = command("git", "status", "--porcelain=v1").splitlines()
    head = command("git", "rev-parse", "HEAD")
    upstream = command("git", "rev-parse", "@{upstream}")
    tracking = command("git", "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = command("git", "ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split("\t", 1)[0] if live_line else None
    check("canonical_flag", args.canonical_pass, args.canonical_pass, "true")
    check("exact_head", head == args.expected_head, head, args.expected_head)
    check("clean_before", not clean_before_rows, clean_before_rows, "clean")
    check("four_way_equality", len({head, upstream, tracking, live}) == 1, {"local": head, "upstream": upstream, "tracking": tracking, "live": live}, "all equal")
    for label, anchor in (("source_ancestry", SOURCE), ("base_ancestry", BASE_FINAL)):
        rc = subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=ROOT).returncode
        check(label, rc == 0, rc, "0")
    phase_commits = int(command("git", "rev-list", "--count", f"{SOURCE}..{head}"))
    special_commits = int(command("git", "rev-list", "--count", f"{BASE_FINAL}..{head}"))
    merges = int(command("git", "rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parents = command("git", "show", "-s", "--format=%P", head).split()
    check("special_commit_budget", phase_commits <= 12 and special_commits == 2, {"source_to_head": phase_commits, "base_to_head": special_commits}, "at most twelve from source and exactly two additive special commits including correction")
    check("zero_merges", merges == 0, merges, "0")
    check("single_parent_correction", parents == [SPECIAL_PREP_COMMIT], parents, f"[{SPECIAL_PREP_COMMIT}]")

    tests = run_tests()
    check("scoped_tests", tests["successful"], tests, "all selected modules pass")
    check("no_test_skips", tests["skipped"] == 0, tests["skipped"], "0")

    json_paths = sorted(PHASE.rglob("*.json"))
    json_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            json_failures.append(path.relative_to(ROOT).as_posix())
    check("json_parse", not json_failures, {"count": len(json_paths), "failures": json_failures}, "all parse")

    privacy_paths = [p for p in PHASE.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES]
    privacy_paths.extend([ROOT / "scripts/build_ghc_family_v651_v6_special_cli_prep.py", ROOT / "scripts/ghc_family_v651_v6_special_validate.py", ROOT / "tests/test_ghc_family_v651_v6_special_cli_prep.py"])
    privacy_hits = []
    for path in sorted(set(privacy_paths)):
        content = path.read_text(encoding="utf-8")
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                privacy_hits.append({"path": path.relative_to(ROOT).as_posix(), "class": label})
    check("privacy_scan", not privacy_hits, {"files": len(set(privacy_paths)), "pattern_classes": len(PATTERNS), "hits": privacy_hits}, "zero concrete hits")

    manifest_rows = []
    manifest_mismatches = []
    for path, blob in tracked_surface():
        working_blob = command("git", "hash-object", f"--path={path}", path)
        row = {"path": path, "blob": blob, "working_blob": working_blob, "match": blob == working_blob}
        manifest_rows.append(row)
        if not row["match"]:
            manifest_mismatches.append(path)
    check("committed_manifest", not manifest_mismatches and len(manifest_rows) >= 40, {"entries": len(manifest_rows), "mismatches": manifest_mismatches}, "at least forty entries and zero mismatches")

    truth = load("truth/phase-truth.json")
    proposals = load("proposals/special-prep-proposal-ledger.json")
    seats = load("cli/future-seat-register.json")
    raw_route = load("workflow/raw-audit/workflow-plan-refinement.json")
    normalized_route = load("workflow/normalized-audit/workflow-plan-refinement.json")
    methods = load("method-flow/method-flow-summary.json")
    method_validation = load("method-flow/method-flow-validation.json")
    reflection = load("reflection-remaster/special-review.json")
    meta = load("tooling/meta-tool-box-refresh.json")
    check("truth_distribution", truth.get("outcomes") == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, truth.get("outcomes"), "23/5/1/1")
    check("negative_retention", truth.get("effective_negatives") == 7338, truth.get("effective_negatives"), "7338")
    check("gate_retention", (truth.get("effective_open_gaps"), truth.get("effective_exact_gates")) == (58, 59), [truth.get("effective_open_gaps"), truth.get("effective_exact_gates")], "58 open and 59 exact")
    check("terminal_verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20", truth.get("terminal_verdict"), "NOT_READY_FOR_STAGE_20")
    check("proposal_count", proposals.get("proposal_count") == 30 and proposals.get("all_authorized_items_resolved_for_phase") is True, proposals.get("proposal_count"), "30 and resolved")
    check("future_seats", seats.get("seat_count") == 8 and seats.get("all_unnamed") is True and seats.get("all_unlaunched") is True, {k: seats.get(k) for k in ("seat_count", "all_unnamed", "all_unlaunched")}, "8 unnamed and unlaunched")
    check("route_dual_truth", raw_route.get("valid") is False and raw_route.get("requires_user_confirmation") is True and normalized_route.get("valid") is True, {"raw": raw_route.get("valid"), "confirmation": raw_route.get("requires_user_confirmation"), "candidate": normalized_route.get("valid")}, "raw fails, candidate structurally passes, confirmation required")
    check("method_flow", method_validation.get("valid") is True and methods.get("counts", {}).get("witness_results") == {"fail": 6, "pass": 6} and methods.get("counts", {}).get("states", {}).get("preferred") == 6, methods.get("counts"), "six preferred methods with six fail/pass pairs")
    check("reflection_review", reflection.get("candidate_count") == 27 and reflection.get("all_candidates_resolved_for_phase") is True and reflection.get("destructive_changes") == 0, reflection, "27 compatibility-held and zero destructive changes")
    check("meta_tool_box", meta.get("validation_valid") is True and meta.get("card_count") == 10, meta, "ten valid cards")

    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".html"}:
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": len(path.read_text(encoding="utf-8").split())})
    max_words = max(row["words"] for row in documents)
    baton_words = next(row["words"] for row in documents if row["path"] == "handoffs/vesper-arlen-v651-v7-special-activation.md")
    overview_words = next(row["words"] for row in documents if row["path"] == "overview/special-integrated-overview.md")
    check("document_cap", max_words <= 100000, {"documents": len(documents), "maximum": max_words}, "maximum <= 100000")
    check("baton_word_range", 10000 <= baton_words <= 100000, baton_words, "10000..100000")
    check("overview_three_page_equivalent", overview_words >= 1000, overview_words, ">= 1000")

    all_tracked = command("git", "ls-tree", "-r", "--name-only", "HEAD").splitlines()
    owner_paths = [p for p in all_tracked if p.startswith("docs/elaren-kestrel/") or "ghc_family_v651_v6" in p or "build_ghc_family_v651_v6" in p]
    check("owner_generated_file_threshold", len(owner_paths) < 2000, len(owner_paths), "< 2000 owner-scoped tracked files; inherited repository baseline excluded")
    cli_version = command("cmd.exe", "/d", "/c", "codex", "--version")
    check("cli_version", cli_version.endswith("0.145.0"), cli_version, "codex-cli 0.145.0")

    clean_after_rows = command("git", "status", "--porcelain=v1").splitlines()
    check("clean_after", not clean_after_rows, clean_after_rows, "clean")
    passed = sum(1 for row in checks if row["passed"])
    minimal_names = [
        "exact_head", "clean_before", "four_way_equality", "source_ancestry", "base_ancestry", "special_commit_budget", "zero_merges", "single_parent_correction", "scoped_tests", "json_parse", "privacy_scan", "committed_manifest", "terminal_verdict", "clean_after"
    ]
    minimal = [row for row in checks if row["name"] in minimal_names]
    receipt = {
        "schema": "ghc.family.v651-v6-special.exact-head-validation.v1",
        "valid": passed == len(checks),
        "successful_pass_count": 1 if passed == len(checks) else 0,
        "post_success_replay": False,
        "full_repository_suite_run": False,
        "head": head,
        "branch": BRANCH,
        "tests": tests,
        "detailed_check_count": len(checks),
        "detailed_checks_passed": passed,
        "checks": checks,
        "minimal_check_count": len(minimal),
        "minimal_checks_passed": sum(1 for row in minimal if row["passed"]),
        "json_parse_count": len(json_paths),
        "privacy_file_count": len(set(privacy_paths)),
        "privacy_pattern_class_count": len(PATTERNS),
        "privacy_hits": privacy_hits,
        "manifest_entry_count": len(manifest_rows),
        "manifest_mismatches": manifest_mismatches,
        "manifest": manifest_rows,
        "document_count": len(documents),
        "maximum_document_words": max_words,
        "baton_words": baton_words,
        "overview_words": overview_words,
        "issue_count": len(issues),
        "issues": issues,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One exact-head scoped canonical pass only; not a full repository suite, redundant replay, scientific confirmation, CLI launch, identity evidence, authority, production readiness, or Stage 20 readiness.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": receipt["valid"], "tests": tests["tests_run"], "detailed": f"{passed}/{len(checks)}", "minimal": f"{receipt['minimal_checks_passed']}/{len(minimal)}", "json": len(json_paths), "privacy_files": len(set(privacy_paths)), "privacy_hits": len(privacy_hits), "manifest": len(manifest_rows)}))
    return 0 if receipt["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
