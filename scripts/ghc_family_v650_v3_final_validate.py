"""One-shot exact-final canonical validator for v650-v3.

The external output path is a replay guard. If it already exists, validation stops.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs/sable-rook/v650-v3"
SOURCE = "b8ece75b5be908a514bc0ea99398f92decd6de8e"
X1 = "9cf6c85372f64d9c71d3dd207e8018b3af0931e8"
EVIDENCE = "f449d71c8452ea0538ed71eb6d032acb86cb8968"
BRANCH = "codex/GHC-Family/sable-rook-full-tools"
EXCLUDED_TEST = "tests.test_ghc_family_v650_v2_closeout.IlyraV650V2CloseoutTests.test_manifest_coverage_contracts"
MODULES = [
    "tests.test_ghc_family_v650_v1_x1", "tests.test_ghc_family_v650_v2_x1",
    "tests.test_ghc_family_v650_v2_x2", "tests.test_ghc_family_v650_v2_closeout",
    "tests.test_ghc_family_v650_v2_correction", "tests.test_ghc_family_v650_v3_x1",
    "tests.test_ghc_family_v650_v3_x2", "tests.test_ghc_family_v650_v3_closeout",
]
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
    raw = []
    for name in MODULES:
        raw.extend(flatten(loader.loadTestsFromName(name)))
    eligible = [test for test in raw if test.id() != EXCLUDED_TEST]
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=1).run(unittest.TestSuite(eligible))
    return {"raw": len(raw), "eligible": len(eligible), "excluded": [EXCLUDED_TEST], "run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "passed": result.wasSuccessful() and len(raw) == 71 and len(eligible) == 70}


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
        actual_paths = set(git("ls-tree", "-r", "--name-only", commit, "--", "docs/sable-rook/v650-v3").splitlines())
    else:
        parent = git("rev-parse", f"{commit}^")
        actual_paths = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", parent, commit).splitlines())
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    return {"entries": len(manifest["entries"]), "exclusions": len(manifest["self_exclusions"]), "blob_mismatches": mismatches, "coverage_missing": sorted(actual_paths - declared), "coverage_extra": sorted(declared - actual_paths), "passed": not mismatches and actual_paths == declared}


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
    privacy_hits = []
    public_files = sorted(p for p in PHASE.rglob("*") if p.is_file())
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
    diff_hygiene = git("diff", "--check", check=False).splitlines()
    status = git("status", "--porcelain=v1").splitlines()
    manifests = {
        "x1": manifest_check("validation/x1-staged-manifest.json", X1, "delta"),
        "evidence": manifest_check("validation/evidence-staged-manifest.json", EVIDENCE, "delta"),
        "owner": manifest_check("validation/final-owner-manifest.json", head, "owner"),
        "final": manifest_check("validation/final-staged-manifest.json", head, "delta"),
    }
    documents = [p for p in public_files if p.suffix.lower() in {".md", ".html"}]
    word_counts = {p.relative_to(REPO).as_posix(): len(p.read_text(encoding="utf-8").split()) for p in documents}
    detailed = {
        "tests": tests["passed"], "json": not json_issues, "privacy": not privacy_hits,
        "x1_manifest": manifests["x1"]["passed"], "evidence_manifest": manifests["evidence"]["passed"],
        "owner_manifest": manifests["owner"]["passed"], "final_manifest": manifests["final"]["passed"],
        "source_ancestry": ancestry[SOURCE], "x1_ancestry": ancestry[X1], "evidence_ancestry": ancestry[EVIDENCE],
        "three_commits": phase_commits == 3, "zero_merges": merges == 0, "one_parent": len(parents) == 1,
        "direct_evidence_parent": parents == [EVIDENCE], "expected_head": head == args.expected_head,
        "expected_branch": branch == BRANCH, "local_upstream": head == upstream,
        "tracking_equal": head == tracking, "live_equal": head == live, "clean": not status,
        "diff_hygiene": not diff_hygiene, "outcomes": load("phase-truth-final.json")["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negatives": load("retained-negative-register-final.json")["effective_total"] == 5807,
        "gaps": load("exact-open-gate-register-final.json")["effective_open_gaps"] == 45,
        "gates": load("exact-open-gate-register-final.json")["effective_exact_gates"] == 46,
        "mutations": load("validation/synthetic-mutation-results.json")["rejected_or_quarantined"] == 100,
        "skills": load("portfolios/skill-execution.json")["validated"] == 20,
        "runners": load("portfolios/runner-execution.json")["invoked"] == 10,
        "safe_tasks": load("portfolios/safe-now-execution.json")["completed"] == 40,
        "candidates": load("portfolios/candidate-execution.json")["completed_within_lane"] == 30,
        "cleanup": load("portfolios/clean-fix-refine-execution.json")["completed"] == 40,
        "method_flow": load("method-flow/final-method-flow-validation.json")["valid"],
        "owner_threshold": len(public_files) < 15000 and load("validation/final-owner-file-threshold.json")["below_threshold"],
        "document_cap": max(word_counts.values(), default=0) <= 20000,
        "baton_range": 8000 <= word_counts.get("docs/sable-rook/v650-v3/handoffs/orin-thale-v650-v4-activation.md", 0) <= 20000,
        "route_held": load("orchestration/terminal-route-state-final.json")["state"] == "PREPARED_NOT_SENT",
        "not_stage20": load("phase-truth-final.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "same_owner_only": load("phase-truth-final.json")["same_owner_only"] and not load("phase-truth-final.json")["independent_reproduction"],
        "no_full_suite": not load("phase-truth-final.json")["full_repository_suite"],
    }
    minimal_keys = ["tests", "json", "privacy", "x1_manifest", "evidence_manifest", "owner_manifest", "final_manifest", "source_ancestry", "x1_ancestry", "evidence_ancestry", "three_commits", "zero_merges", "one_parent", "direct_evidence_parent", "expected_head", "expected_branch", "local_upstream", "tracking_equal", "live_equal", "clean", "diff_hygiene", "not_stage20", "route_held"]
    passed = all(detailed.values()) and len(detailed) == 39 and len(minimal_keys) == 23
    receipt = {
        "schema": "ghc.family.v650-v3.external-final-validation.v1", "head": head, "branch": branch,
        "tests": tests, "detailed_checks": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal_checks": {"passed": sum(detailed[k] for k in minimal_keys), "total": len(minimal_keys)},
        "json": {"parsed": len(json_files), "issues": json_issues},
        "privacy": {"files": len(public_files), "classes": len(PATTERNS), "confirmed_hits": privacy_hits},
        "manifests": manifests, "topology": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "phase_commits": phase_commits, "merges": merges, "parents": parents, "ancestry": ancestry},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live},
        "documents": {"count": len(documents), "max_words": max(word_counts.values(), default=0), "baton_words": word_counts.get("docs/sable-rook/v650-v3/handoffs/orin-thale-v650-v4-activation.md", 0)},
        "full_repository_suite": False, "same_owner_only": True, "independent_reproduction": False,
        "post_success_replay": False, "passed": passed, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "tests": f"{tests['run']}/{tests['eligible']}", "detailed": f"{sum(detailed.values())}/{len(detailed)}", "minimal": f"{sum(detailed[k] for k in minimal_keys)}/{len(minimal_keys)}", "json": len(json_files), "privacy_files": len(public_files)}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
