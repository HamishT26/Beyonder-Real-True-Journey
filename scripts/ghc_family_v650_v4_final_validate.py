"""One-shot exact-final canonical validator for Orin Thale v650-v4."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
PHASE = REPO / "docs/orin-thale/v650-v4"
SOURCE = "b3c9e5ea94f28432911810fa9374eff15fecabad"
X1 = "2aef76bbfc315857ff5bd134424a346fa70d1ec3"
EVIDENCE = "6a25ee7cefa63039a4b17b56c06462b6cf622ea9"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
MODULES = [
    "tests.test_ghc_family_v650_v3_x1",
    "tests.test_ghc_family_v650_v3_x2",
    "tests.test_ghc_family_v650_v3_closeout",
    "tests.test_ghc_family_v650_v4_x1",
    "tests.test_ghc_family_v650_v4_x2",
    "tests.test_ghc_family_v650_v4_closeout",
]
EXPECTED_TESTS = 57
PATTERNS = {
    "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(r"(?:[A-Z]:\\Users\\|/home/[^/\s]+/|/Users/[^/\s]+/)", re.I),
    "private_uri": re.compile(r"(?:codex|vscode|file)://", re.I),
    "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret)\s*[:=]\s*['\"][^'\"]+"),
    "delegation_markup": re.compile(r"<codex_delegation>|<source_thread_id>|<thread_id>", re.I),
}


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", *args], cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def load(relative: str) -> dict:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run_tests() -> dict:
    loader = unittest.TestLoader()
    tests = []
    for module in MODULES:
        tests.extend(flatten(loader.loadTestsFromName(module)))
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(unittest.TestSuite(tests))
    loader_errors = [test.id() for test in tests if test.__class__.__name__ == "_FailedTest"]
    passed = result.wasSuccessful() and result.testsRun == EXPECTED_TESTS and len(tests) == EXPECTED_TESTS and not loader_errors
    return {"raw": len(tests), "eligible": len(tests), "excluded": [], "run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "loader_errors": loader_errors, "passed": passed}


def manifest_check(relative: str, commit: str, mode: str) -> dict:
    manifest = load(relative)
    mismatches = []
    for row in manifest["entries"]:
        try:
            actual = git("rev-parse", f"{commit}:{row['path']}")
        except RuntimeError:
            actual = "missing"
        if actual != row["git_blob"]:
            mismatches.append(row["path"])
    if mode == "owner":
        actual_paths = set(git("ls-tree", "-r", "--name-only", commit, "--", "docs/orin-thale/v650-v4").splitlines())
    else:
        parent = git("rev-parse", f"{commit}^")
        actual_paths = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", parent, commit).splitlines())
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    return {
        "entries": len(manifest["entries"]),
        "exclusions": len(manifest["self_exclusions"]),
        "blob_mismatches": mismatches,
        "coverage_missing": sorted(actual_paths - declared),
        "coverage_extra": sorted(declared - actual_paths),
        "passed": not mismatches and actual_paths == declared,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--external-output", required=True)
    args = parser.parse_args()
    output = Path(args.external_output)
    if output.exists():
        print("external output already exists; replay refused", file=sys.stderr)
        return 3

    tests = run_tests()
    json_files = sorted(PHASE.rglob("*.json"))
    json_issues = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            json_issues.append({"path": path.relative_to(REPO).as_posix(), "error": type(exc).__name__})
    public_files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    privacy_hits = []
    for path in public_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path.relative_to(REPO).as_posix(), "class": name})

    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{upstream}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_rows = git("ls-remote", "origin", f"refs/heads/{BRANCH}").split()
    live = live_rows[0] if live_rows else "missing"
    ancestry = {}
    for anchor in (SOURCE, X1, EVIDENCE):
        proc = subprocess.run(["git", "merge-base", "--is-ancestor", anchor, head], cwd=REPO)
        ancestry[anchor] = proc.returncode == 0
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    parents = git("show", "-s", "--format=%P", head).split()
    status = git("status", "--porcelain=v1").splitlines()
    diff_hygiene = git("diff", "--check", check=False).splitlines()

    manifests = {
        "x1": manifest_check("validation/x1-staged-manifest.json", X1, "delta"),
        "evidence": manifest_check("validation/evidence-staged-manifest.json", EVIDENCE, "delta"),
        "final_owner": manifest_check("validation/final-owner-manifest.json", head, "owner"),
        "final_delta": manifest_check("validation/final-staged-manifest.json", head, "delta"),
    }
    documents = [path for path in public_files if path.suffix.lower() in {".md", ".html", ".txt"}]
    word_counts = {path.relative_to(REPO).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in documents}
    baton_path = "docs/orin-thale/v650-v4/handoffs/tamar-vey-v650-v5-activation.md"
    truth = load("phase-truth-final.json")
    negatives = load("retained-negative-register-final.json")
    gates = load("exact-open-gate-register-final.json")
    method = load("method-flow/method-flow-state.json")
    env = load("environment/final-environment-receipt.json")
    detailed = {
        "bounded_tests": tests["passed"],
        "json_parse": not json_issues,
        "privacy_scan": not privacy_hits,
        "x1_manifest": manifests["x1"]["passed"],
        "evidence_manifest": manifests["evidence"]["passed"],
        "final_owner_manifest": manifests["final_owner"]["passed"],
        "final_delta_manifest": manifests["final_delta"]["passed"],
        "source_ancestry": ancestry[SOURCE],
        "x1_ancestry": ancestry[X1],
        "evidence_ancestry": ancestry[EVIDENCE],
        "three_commits": phase_commits == 3,
        "zero_merges": merges == 0,
        "one_parent": len(parents) == 1,
        "direct_evidence_parent": parents == [EVIDENCE],
        "expected_head": head == args.expected_head,
        "expected_branch": branch == BRANCH,
        "local_upstream": head == upstream,
        "tracking_equal": head == tracking,
        "live_equal": head == live,
        "clean": not status,
        "diff_hygiene": not diff_hygiene,
        "outcomes": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negatives": negatives["effective_total"] == 5925 and negatives["erased"] == 0,
        "open_gaps": gates["effective_open_gaps"] == 46,
        "exact_gates": gates["effective_exact_gates"] == 47,
        "mutations": load("validation/x2-synthetic-mutation-results.json")["rejected_or_quarantined"] == 100,
        "skills": load("portfolios/skill-execution.json")["completed"] == 20,
        "runners": load("portfolios/runner-execution.json")["completed"] == 10,
        "safe_tasks": load("portfolios/safe-now-execution.json")["completed"] == 40,
        "candidates": load("portfolios/candidate-execution.json")["completed"] == 30,
        "cleanup": load("portfolios/clean-fix-refine-execution.json")["completed"] == 40,
        "method_flow": method["counts"]["methods"] == 14 and method["counts"]["witness_results"] == {"fail": 14, "pass": 14},
        "owner_threshold": len(public_files) < 15000 and load("validation/final-owner-file-threshold.json")["below_threshold"],
        "document_cap": max(word_counts.values(), default=0) <= 20000,
        "baton_range": 8000 <= word_counts.get(baton_path, 0) <= 20000,
        "route_held": load("orchestration/terminal-route-state-final.json")["state"] == "PREPARED_NOT_SENT",
        "not_stage20": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "same_owner_only": truth["same_owner_only"] and not truth["independent_reproduction"],
        "no_full_suite": not truth["full_repository_suite"],
        "x1_before_x2": load("closeout/closeout-receipt.json")["x1_before_x2"],
        "evidence_remote_equal_before_closeout": load("closeout/closeout-receipt.json")["evidence_remote_equal_before_closeout"],
        "staged_review": load("validation/final-staged-review.json")["passed"],
        "stale_labels": load("validation/stale-label-review.json")["passed"],
        "identity_boundary": load("identity-receipt.json")["relational_only"],
        "environment_boundary": env["versions_verified_only"] and not any(env[key] for key in ("desktop_updated", "sandbox_or_hyperv_launched", "elevation", "host_security_weakened", "windows_feature_changed", "unrelated_software_installed", "reboot")),
    }
    minimal_keys = [
        "bounded_tests", "json_parse", "privacy_scan", "x1_manifest", "evidence_manifest",
        "final_owner_manifest", "final_delta_manifest", "source_ancestry", "x1_ancestry",
        "evidence_ancestry", "three_commits", "zero_merges", "one_parent", "direct_evidence_parent",
        "expected_head", "expected_branch", "local_upstream", "tracking_equal", "live_equal", "clean",
        "diff_hygiene", "not_stage20", "route_held", "same_owner_only", "no_full_suite",
    ]
    passed = all(detailed.values()) and len(minimal_keys) == 25
    receipt = {
        "schema": "ghc.family.v650-v4.external-final-validation.v1",
        "head": head,
        "branch": branch,
        "tests": tests,
        "detailed_checks": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal_checks": {"passed": sum(detailed[key] for key in minimal_keys), "total": len(minimal_keys)},
        "json": {"parsed": len(json_files), "issues": json_issues},
        "privacy": {"files": len(public_files), "classes": len(PATTERNS), "confirmed_hits": privacy_hits},
        "manifests": manifests,
        "topology": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "phase_commits": phase_commits, "merges": merges, "parents": parents, "ancestry": ancestry},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live},
        "documents": {"count": len(documents), "max_words": max(word_counts.values(), default=0), "baton_words": word_counts.get(baton_path, 0)},
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "named_or_detached_replay": False,
        "post_success_replay": False,
        "passed": passed,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "tests": f"{tests['run']}/{tests['eligible']}", "detailed": f"{sum(detailed.values())}/{len(detailed)}", "minimal": f"{sum(detailed[key] for key in minimal_keys)}/{len(minimal_keys)}", "json": len(json_files), "privacy_files": len(public_files)}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
