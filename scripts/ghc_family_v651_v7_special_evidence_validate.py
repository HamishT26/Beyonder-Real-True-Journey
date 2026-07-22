#!/usr/bin/env python3
"""Validate the exact staged x2 evidence boundary for Vesper's special phase."""

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
PHASE = ROOT / "docs/vesper-arlen/v651-v7-special-cli-prep"
PHASE_REL = PHASE.relative_to(ROOT).as_posix()
X1 = "07785aa97b0aa46a4fbf0c60109a8ee8e678aacf"
BRANCH = "codex/GHC-Family/vesper-arlen-v651-v7-special-cli-prep"
TEXT_SUFFIXES = {".json", ".md", ".txt", ".html", ".yaml", ".yml", ".py"}
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|file|vscode)://"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret)\s*[:=]\s*[^\s,}\]]+"),
    "delegation_markup": re.compile(r"(?i)<\s*codex_delegation\b"),
}


def git_text(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=False)
    if check and result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed with {result.returncode}")
    return result.stdout.strip()


def git_bytes(spec: str) -> bytes:
    result = subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"git show failed for {spec}")
    return result.stdout


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run_tests() -> dict[str, Any]:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for name in ("tests.test_ghc_family_v651_v7_special_x1", "tests.test_ghc_family_v651_v7_special_x2"):
        suite.addTests(loader.loadTestsFromName(name))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, observed: Any, expected: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), "observed": observed, "expected": expected})

    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"origin/{BRANCH}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").splitlines()
    live = live_rows[0].split()[0] if live_rows else ""
    check("x1_exact_head", head == X1, head, X1)
    check("x1_four_way_equality", len({head, upstream, tracking, live}) == 1, {"local": head, "upstream": upstream, "tracking": tracking, "live": live}, "all x1")

    tests = run_tests()
    check("scoped_tests", tests["successful"] and tests["tests_run"] == 18, tests, "18 passing tests")
    check("no_test_skips", tests["skipped"] == 0, tests["skipped"], 0)

    json_paths = sorted(PHASE.rglob("*.json"))
    parsed = 0
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
            parsed += 1
        except Exception as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    check("phase_json_parse", not json_issues, {"parsed": parsed, "total": len(json_paths), "issues": json_issues}, "all parse")

    scan_paths = [path for path in PHASE.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and path != args.receipt]
    scan_paths.extend(
        ROOT / value
        for value in (
            "scripts/ghc_family_v651_v7_special_cli_batch.py",
            "scripts/ghc_family_cli_route_coverage.py",
            "scripts/ghc_family_cli_capability_contract.py",
            "scripts/ghc_family_sparse_lane_guard.py",
            "scripts/ghc_family_baton_pointer_guard.py",
            "scripts/build_ghc_family_v651_v7_special_execution.py",
            "scripts/ghc_family_v651_v7_special_manifest.py",
            "scripts/ghc_family_v651_v7_special_evidence_validate.py",
            "tests/test_ghc_family_v651_v7_special_x1.py",
            "tests/test_ghc_family_v651_v7_special_x2.py",
        )
    )
    privacy_hits = []
    for path in sorted(set(scan_paths)):
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(ROOT).as_posix(), "class": label})
    check("privacy_scan", not privacy_hits, {"files": len(set(scan_paths)), "classes": len(PATTERNS), "hits": privacy_hits}, "zero confirmed hits")

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    exclusions = set(manifest["self_exclusions"])
    index_paths = set(git_text("ls-files", "--cached", "--", PHASE_REL).splitlines())
    expected = index_paths - exclusions
    listed = {row["path"] for row in manifest["entries"]}
    mismatches = []
    for row in manifest["entries"]:
        data = git_bytes(f":{row['path']}")
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    check("index_manifest", manifest.get("domain") == "index" and expected == listed and not mismatches, {"entries": len(listed), "domain_equal": expected == listed, "mismatches": mismatches}, "exact index domain")

    staged = git_text("diff", "--cached", "--name-only", "HEAD").splitlines()
    permitted_nonphase = {
        "scripts/ghc_family_v651_v7_special_cli_batch.py",
        "scripts/ghc_family_cli_route_coverage.py",
        "scripts/ghc_family_cli_capability_contract.py",
        "scripts/ghc_family_sparse_lane_guard.py",
        "scripts/ghc_family_baton_pointer_guard.py",
        "scripts/build_ghc_family_v651_v7_special_execution.py",
        "scripts/ghc_family_v651_v7_special_manifest.py",
        "scripts/ghc_family_v651_v7_special_evidence_validate.py",
        "tests/test_ghc_family_v651_v7_special_x1.py",
        "tests/test_ghc_family_v651_v7_special_x2.py",
    }
    out_of_scope = [path for path in staged if not path.startswith(PHASE_REL + "/") and path not in permitted_nonphase]
    staged_json = 0
    staged_privacy_hits = []
    for path in staged:
        data = git_bytes(f":{path}")
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            staged_json += 1
        if Path(path).suffix.lower() in TEXT_SUFFIXES:
            text = data.decode("utf-8", errors="replace")
            for label, pattern in PATTERNS.items():
                if pattern.search(text):
                    staged_privacy_hits.append({"path": path, "class": label})
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    check("exact_staged_review", not out_of_scope and not staged_privacy_hits and diff_check.returncode == 0, {"paths": len(staged), "json": staged_json, "out_of_scope": out_of_scope, "privacy_hits": staged_privacy_hits, "diff_check": diff_check.returncode}, "owner-scoped zero-hit clean diff")

    truth = load("truth/phase-truth.json")
    check("outcome_distribution", truth["outcomes"] == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}, truth["outcomes"], "23/5/1/1")
    check("negative_arithmetic", truth["effective_negatives"] == 7569, truth["effective_negatives"], 7569)
    check("gate_arithmetic", (truth["effective_open_gaps"], truth["effective_exact_gates"]) == (59, 60), [truth["effective_open_gaps"], truth["effective_exact_gates"]], [59, 60])
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    batch = load("cli/cli-batch-receipt.json")
    check("cli_prepare_refusal", batch["prepare_passes"] == 8 and batch["launch_refusals"] == 8 and batch["all_unnamed"] and batch["all_unlaunched"], batch, "8 prepare, 8 refuse, zero identity/launch")
    check("mutation_tribunal", batch["synthetic_mutations_rejected"] == 100, batch["synthetic_mutations_rejected"], 100)
    method = load("method-flow/method-flow-summary.json")
    check("method_flow", method["valid"] and method["counts"]["states"]["preferred"] == 9 and method["counts"]["witness_results"] == {"fail": 11, "pass": 10}, method["counts"], "9 preferred, 11 fail, 10 pass")
    baton = load("validation/baton-pointer-guard.json")
    check("baton_pointer", baton["valid"] and 10000 <= baton["baton_words"] <= 100000 and baton["privacy_hits"] == [], baton, "valid bounded baton and pointer")
    sparse = load("tooling/sparse-lane-guard.json")
    check("materialized_limit", sparse["valid"] and sparse["materialized_files"] < 2000, sparse, "sparse and below 2000")
    check("no_closeout_contamination", not (PHASE / "closeout/closeout-receipt.json").exists() and not (PHASE / "seal/seal-receipt.json").exists(), "absent", "absent")

    oversized = []
    for path in PHASE.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".html"}:
            words = len(re.findall(r"\b\w+(?:[-']\w+)*\b", path.read_text(encoding="utf-8", errors="replace")))
            if words > 100000:
                oversized.append({"path": path.relative_to(ROOT).as_posix(), "words": words})
    check("document_word_cap", not oversized, oversized, "all at or below 100000")
    stale_hits = []
    for path in scan_paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if ("Vesper " + "Arien") in text or ("v651-v7 " + "(SPECIAL)") in text:
            stale_hits.append(path.relative_to(ROOT).as_posix())
    check("stale_label_review", not stale_hits, stale_hits, "zero stale labels")

    passed = sum(row["passed"] for row in checks)
    minimal_names = {"x1_exact_head", "x1_four_way_equality", "scoped_tests", "phase_json_parse", "privacy_scan", "index_manifest", "exact_staged_review", "outcome_distribution", "terminal_verdict", "cli_prepare_refusal", "no_closeout_contamination"}
    minimal_passed = sum(row["passed"] for row in checks if row["name"] in minimal_names)
    payload = {
        "schema": "ghc.family.v651-v7-special.evidence-validation.v1",
        "valid": passed == len(checks),
        "checks_passed": passed,
        "check_count": len(checks),
        "minimal_checks_passed": minimal_passed,
        "minimal_check_count": len(minimal_names),
        "checks": checks,
        "tests": tests,
        "json_files": len(json_paths),
        "privacy_files": len(set(scan_paths)),
        "privacy_pattern_classes": len(PATTERNS),
        "privacy_hits": privacy_hits,
        "manifest_entries": len(manifest["entries"]),
        "staged_paths": len(staged),
        "staged_json": staged_json,
        "boundary": "Exact staged same-owner evidence validation only; not terminal closeout, independent reproduction, production assurance, or Stage 20 evidence.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": payload["valid"], "tests": tests["tests_run"], "detailed": f"{passed}/{len(checks)}", "minimal": f"{minimal_passed}/{len(minimal_names)}", "json": len(json_paths), "privacy_files": len(set(scan_paths)), "manifest": len(manifest["entries"]), "staged": len(staged)}))
    return 0 if payload["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
