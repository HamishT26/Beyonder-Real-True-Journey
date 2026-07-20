#!/usr/bin/env python3
"""One-shot exact-final canonical validator for Orin Thale v651-v2."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
PHASE_ROOT = "docs/orin-thale/v651-v2"
SOURCE = "ad2b530c2449656b54ac0fee1a1284208c2a6a75"
X1 = "06c5545a79e992537b6307eb6a68e6d01204144d"
EVIDENCE = "8b3c1bb68852acc52c4554c34f1b6689a7c49efd"
BRANCH = "codex/GHC-Family/orin-thale-v642-v6-full-tools"
EXCLUDED = "tests.test_ghc_family_v651_v1_closeout.TestV651V1Closeout.test_owner_and_delta_manifest_coverage"
MODULES = [
    "tests.test_ghc_family_v651_v1_x1",
    "tests.test_ghc_family_v651_v1_x2",
    "tests.test_ghc_family_v651_v1_closeout",
    "tests.test_ghc_family_v651_v2_x1",
    "tests.test_ghc_family_v651_v2_x2",
    "tests.test_ghc_family_v651_v2_closeout",
]
PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def git(*args: str, binary: bool = False, check: bool = True) -> str | bytes:
    proc = subprocess.run(["git", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    unique = list(dict.fromkeys(oids))
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode().split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
        result[expected] = data
    if stream.read():
        raise RuntimeError("unexpected trailing batch output")
    return result


def tree_map(commit: str, prefix: str | None = None) -> dict[str, str]:
    args = ["ls-tree", "-r", "-z", commit]
    if prefix:
        args.extend(["--", prefix])
    raw = git(*args, binary=True)
    result = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        _mode, kind, oid = meta.decode().split()
        if kind == "blob":
            result[path.decode("utf-8")] = oid
    return result


def load_at(commit: str, path: str) -> object:
    return json.loads(git("show", f"{commit}:{path}"))


def manifest_check(commit: str, path: str, expected_paths: set[str]) -> dict:
    manifest = load_at(commit, path)
    declared = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    tree = tree_map(commit)
    blobs = batch_blobs([row["git_blob"] for row in manifest["entries"]])
    issues = []
    if declared != expected_paths:
        issues.append("path_set")
    for row in manifest["entries"]:
        data = blobs[row["git_blob"]]
        if tree.get(row["path"]) != row["git_blob"]:
            issues.append("blob:" + row["path"])
        if len(data) != row["bytes"]:
            issues.append("bytes:" + row["path"])
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            issues.append("sha256:" + row["path"])
    return {"manifest": path, "commit": commit, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "issues": issues, "valid": not issues}


def flatten(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def selected_tests() -> tuple[unittest.TestSuite, dict]:
    loader = unittest.defaultTestLoader
    selected = []
    raw_source = 0
    source_eligible = 0
    current = 0
    excluded = []
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        tests = list(flatten(loader.loadTestsFromModule(module)))
        is_source = "v651_v1" in module_name
        if is_source:
            raw_source += len(tests)
        for test in tests:
            if test.id() == EXCLUDED:
                excluded.append(test.id())
                continue
            selected.append(test)
            if is_source:
                source_eligible += 1
            else:
                current += 1
    return unittest.TestSuite(selected), {"raw_source": raw_source, "source_eligible": source_eligible, "current": current, "eligible": len(selected), "excluded": excluded}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output.exists():
        raise SystemExit("refusing to overwrite an existing validation attempt")
    try:
        output.relative_to(REPO.resolve())
        raise SystemExit("validation output must remain outside the repository")
    except ValueError:
        pass
    output.parent.mkdir(parents=True, exist_ok=True)

    issues = []
    head = git("rev-parse", "HEAD")
    clean_before = not bool(git("status", "--porcelain=v1"))
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""

    suite, selection = selected_tests()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    test_valid = result.testsRun == 59 and not result.failures and not result.errors and selection == {"raw_source": 24, "source_eligible": 23, "current": 36, "eligible": 59, "excluded": [EXCLUDED]}
    if not test_valid:
        issues.append("selected_tests")

    source_to_x1 = set(filter(None, git("diff", "--name-only", f"{SOURCE}..{X1}").splitlines()))
    x1_to_evidence = set(filter(None, git("diff", "--name-only", f"{X1}..{EVIDENCE}").splitlines()))
    evidence_to_final = set(filter(None, git("diff", "--name-only", f"{EVIDENCE}..{head}").splitlines()))
    owner_tree = set(tree_map(head, PHASE_ROOT))
    manifest_results = [
        manifest_check(X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json", source_to_x1),
        manifest_check(EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json", x1_to_evidence),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-delta-manifest.json", evidence_to_final),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-owner-manifest.json", owner_tree),
    ]
    if not all(row["valid"] for row in manifest_results):
        issues.append("manifest_parity")

    owner_map = tree_map(head, PHASE_ROOT)
    owner_blobs = batch_blobs(list(owner_map.values()))
    json_count = 0
    json_issues = []
    privacy_hits = []
    word_issues = []
    for path, oid in owner_map.items():
        data = owner_blobs[oid]
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
                json_count += 1
            except Exception as exc:
                json_issues.append(f"{path}:{type(exc).__name__}")
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                privacy_hits.append({"path": path, "class": class_name, "offset": match.start()})
        if path.endswith(".md"):
            words = len(re.findall(r"\b\w+\b", data.decode("utf-8"), flags=re.UNICODE))
            if path.endswith("handoffs/tamar-vey-v651-v3-activation.md"):
                if not 8000 <= words <= 20000:
                    word_issues.append({"path": path, "words": words})
            elif words > 6000:
                word_issues.append({"path": path, "words": words})
    if json_issues:
        issues.append("json_parse")
    if privacy_hits:
        issues.append("privacy_scan")
    if word_issues:
        issues.append("document_caps")

    truth = load_at(head, f"{PHASE_ROOT}/final/phase-truth.json")
    negatives = load_at(head, f"{PHASE_ROOT}/final/retained-negative-register.json")
    gates = load_at(head, f"{PHASE_ROOT}/final/gate-register.json")
    methods = load_at(head, f"{PHASE_ROOT}/method-flow/method-flow-summary.json")
    route = load_at(head, f"{PHASE_ROOT}/route/final-phase-state.json")
    skills = load_at(head, f"{PHASE_ROOT}/tooling/skill-validation-summary.json")
    runners = load_at(head, f"{PHASE_ROOT}/tooling/runner-inventory.json")
    mutations = load_at(head, f"{PHASE_ROOT}/validation/mutation-execution-summary.json")
    safe = load_at(head, f"{PHASE_ROOT}/portfolios/safe-now-execution.json")
    candidates = load_at(head, f"{PHASE_ROOT}/portfolios/candidate-execution.json")
    cleanup = load_at(head, f"{PHASE_ROOT}/portfolios/clean-fix-refine-execution.json")
    report = owner_blobs[owner_map[f"{PHASE_ROOT}/reports/final-static-report.html"]].decode("utf-8").casefold()
    baton = owner_blobs[owner_map[f"{PHASE_ROOT}/handoffs/tamar-vey-v651-v3-activation.md"]].decode("utf-8")
    overview = owner_blobs[owner_map[f"{PHASE_ROOT}/overview/final-integrated-overview.md"]].decode("utf-8")
    baton_words = len(re.findall(r"\b\w+\b", baton, flags=re.UNICODE))
    overview_words = len(re.findall(r"\b\w+\b", overview, flags=re.UNICODE))
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    parent_count = len(parents) - 1
    diff_hygiene = subprocess.run(["git", "diff", "--check", f"{EVIDENCE}..{head}"], cwd=REPO).returncode == 0
    stale_ready = re.search(r"(?<!NOT_)READY_FOR_STAGE_20", "\n".join(data.decode("utf-8", errors="ignore") for data in owner_blobs.values())) is None
    stale_sent = '"terminal_route": "SENT"' not in "\n".join(data.decode("utf-8", errors="ignore") for data in owner_blobs.values())

    detailed = {
        "expected_branch": branch == BRANCH,
        "upstream_configured": bool(upstream),
        "local_equals_upstream": head == upstream,
        "local_equals_tracking": head == tracking,
        "local_equals_live": head == live,
        "clean_before": clean_before,
        "source_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=REPO).returncode == 0,
        "x1_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=REPO).returncode == 0,
        "evidence_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=REPO).returncode == 0,
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merges == 0,
        "one_final_parent": parent_count == 1,
        "final_direct_child_of_evidence": parent_count == 1 and parents[1] == EVIDENCE,
        "outcome_distribution": truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negative_retention": negatives["effective"] == 6685 and negatives["no_failure_erased"],
        "open_gap_retention": gates["effective_open_gaps"] == 52 and gates["silently_closed"] == 0,
        "exact_gate_retention": gates["effective_exact_gates"] == 53 and gates["silently_closed"] == 0,
        "method_count": methods["counts"]["methods"] == 19,
        "failed_witness_count": methods["counts"]["witness_results"]["fail"] == 19,
        "passing_witness_count": methods["counts"]["witness_results"]["pass"] == 19,
        "x1_manifest": manifest_results[0]["valid"],
        "evidence_manifest": manifest_results[1]["valid"],
        "final_delta_manifest": manifest_results[2]["valid"],
        "final_owner_manifest": manifest_results[3]["valid"],
        "complete_json_parse": not json_issues and json_count > 0,
        "five_class_privacy_scan": not privacy_hits,
        "document_caps": not word_issues,
        "baton_word_contract": 8000 <= baton_words <= 20000,
        "overview_three_page_equivalent": 1500 <= overview_words <= 6000,
        "owner_files_below_rotation": len(owner_map) < 15000,
        "route_prepared_not_sent": route["terminal_route"] == "PREPARED_NOT_SENT",
        "send_count_zero": route["send_count"] == 0,
        "no_task_creation_or_fork": not route["task_created"] and not route["task_forked"],
        "no_cross_platform_or_subagent": not route["cross_platform_substitute"] and not route["collaboration_subagent"],
        "full_suite_not_run": not truth["full_repository_suite_run"],
        "named_or_detached_replay_not_run": not truth["named_or_detached_replay_run"],
        "independent_reproduction_not_claimed": not truth["independent_reproduction_claimed"],
        "terminal_abstention": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "twenty_skills": skills["official_quick_validated"] == 20 and skills["smoke_used"] == 20,
        "ten_runners": runners["count"] == 10 and runners["passed"] == 10,
        "hundred_mutations": mutations["executed"] == 100 and mutations["rejected_or_quarantined"] == 100 and mutations["accepted"] == 0,
        "forty_safe_now": safe["completed"] == 40,
        "thirty_candidates": candidates["completed"] == 30,
        "forty_cleanup": cleanup["completed"] == 40 and not cleanup["deleted_user_material"] and not cleanup["sibling_mutation"],
        "static_report_structural": all(phrase in report for phrase in ("skip to content", "manual keyboard", "assistive-technology", "affected-user evaluation remain reserved")),
        "exact_exclusion_set": selection["excluded"] == [EXCLUDED],
        "selected_tests": test_valid,
        "semantic_stale_ready_review": stale_ready,
        "semantic_stale_sent_review": stale_sent,
        "diff_hygiene": diff_hygiene,
        "owner_path_set": manifest_results[3]["valid"],
        "delta_path_set": manifest_results[2]["valid"],
    }
    failed_detailed = [name for name, passed in detailed.items() if not passed]
    if failed_detailed:
        issues.extend("detailed:" + name for name in failed_detailed)
    minimal_names = [
        "expected_branch", "local_equals_upstream", "local_equals_tracking", "local_equals_live", "clean_before",
        "source_ancestral", "x1_ancestral", "evidence_ancestral", "three_phase_commits", "zero_merges",
        "one_final_parent", "final_direct_child_of_evidence", "outcome_distribution", "negative_retention", "open_gap_retention",
        "exact_gate_retention", "final_delta_manifest", "final_owner_manifest", "complete_json_parse", "five_class_privacy_scan",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    clean_after = not bool(git("status", "--porcelain=v1"))
    if not clean_after:
        issues.append("clean_after")
    valid = not issues
    receipt = {
        "schema": "ghc.family.v651-v2.exact-final-validation.v1",
        "phase": "v651-v2",
        "owner": "Orin Thale",
        "exact_head": head,
        "branch": branch,
        "selection": selection,
        "tests": {"passed": result.testsRun - len(result.failures) - len(result.errors), "total": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "log": stream.getvalue().splitlines()},
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json": {"parsed": json_count, "issues": json_issues},
        "privacy": {"files_scanned": len(owner_map), "pattern_classes": sorted(PATTERNS), "confirmed_hits": privacy_hits, "zero_confirmed_hits": not privacy_hits, "boundary": "Five-class scanning is not privacy-complete assurance."},
        "manifests": manifest_results,
        "documents": {"baton_words": baton_words, "overview_words": overview_words, "issues": word_issues},
        "history": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "phase_commits": phase_commits, "merge_commits": merges, "final_parent_count": parent_count},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live, "all_equal": head == upstream == tracking == live},
        "clean_before": clean_before,
        "clean_after": clean_after,
        "full_repository_suite_run": False,
        "named_or_detached_replay_run": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "issues": issues,
        "valid": valid,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "One exact-final non-Eiren canonical pass only; no replay after success and no complete-suite or independent-reproduction credit.",
    }
    output.write_text(json.dumps(receipt, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"head": head, "tests": f"{receipt['tests']['passed']}/{receipt['tests']['total']}", "detailed": f"{receipt['detailed']['passed']}/{receipt['detailed']['total']}", "minimal": f"{receipt['minimal']['passed']}/{receipt['minimal']['total']}", "json": json_count, "privacy_files": len(owner_map), "manifest_entries": sum(row["entries"] for row in manifest_results), "clean_before": clean_before, "clean_after": clean_after, "all_equal": receipt["equality"]["all_equal"], "valid": valid}))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
