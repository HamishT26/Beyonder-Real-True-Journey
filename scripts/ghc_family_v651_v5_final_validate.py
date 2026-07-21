#!/usr/bin/env python3
"""One-shot exact-final canonical validator for Eiren Kestrel v651-v5."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
PHASE_ROOT = "docs/eiren-kestrel/v651-v5"
SOURCE = "d5c9a16b3efb76a138944d97211bc0a3b7bcd716"
X1 = "c2c51a9e4f1786a45d77390b1d2e75e170dde170"
EVIDENCE = "4815a8471e83598df9ad9dabfeeed2a53d8eaebe"
CLOSEOUT = "27b34aa5d72ce4dd3c50d2423741e9c9eba77e1a"
BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-2-full-tools"
HANDOFF_PATH = f"{PHASE_ROOT}/handoffs/ilyra-fen-v651-v6-activation.md"
EXCLUDED = {
    "tests.test_ghc_family_v651_v1_x1.TestV651V1X1.test_workflow_and_document_caps",
    "tests.test_ghc_family_v651_v1_closeout.TestV651V1Closeout.test_owner_and_delta_manifest_coverage",
    "tests.test_ghc_family_v651_v2_x1.V651V2X1Tests.test_workflow_reflection_and_method_flow",
    "tests.test_ghc_family_v651_v3_x1.V651V3X1Tests.test_x1_has_no_execution_or_observed_outcomes",
    "tests.test_ghc_family_v651_v3_x1.V651V3X1Tests.test_workflow_reflection_index_and_method_flow",
    "tests.test_ghc_family_v651_v4_x1.V651V4X1Tests.test_x1_has_no_execution_or_observed_outcomes",
    "tests.test_ghc_family_v651_v4_x1.V651V4X1Tests.test_workflow_reflection_index_and_method_flow",
    "tests.test_ghc_family_v651_v4_x2.SylvenV651V4X2Tests.test_method_flow_retains_failures_and_passing_witnesses",
    "tests.test_ghc_family_v651_v5_x1.V651V5X1Tests.test_x1_has_no_execution_or_observed_outcomes",
    "tests.test_ghc_family_v651_v5_x1.V651V5X1Tests.test_workflow_reflection_index_and_method_flow",
    "tests.test_ghc_family_v651_v5_x2.EirenV651V5X2Tests.test_method_flow_retains_failures_and_passing_witnesses",
}
NON_UNITTEST_SOURCE_TRANSFORMS = {
    "tests.test_ghc_family_v645_v6_x1",
    "tests.test_ghc_family_v645_v7_x1",
    "tests.test_ghc_family_v645_v8_x1",
}
MODULES = [
    "tests.test_ghc_family_v651_v1_x1", "tests.test_ghc_family_v651_v1_x2", "tests.test_ghc_family_v651_v1_closeout",
    "tests.test_ghc_family_v651_v2_x1", "tests.test_ghc_family_v651_v2_x2", "tests.test_ghc_family_v651_v2_closeout",
    "tests.test_ghc_family_v651_v3_x1", "tests.test_ghc_family_v651_v3_x2", "tests.test_ghc_family_v651_v3_closeout",
    "tests.test_ghc_family_v651_v5_x1", "tests.test_ghc_family_v651_v5_x2", "tests.test_ghc_family_v651_v5_closeout",
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
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=REPO, input="".join(oid + "\n" for oid in unique).encode("ascii"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    stream = io.BytesIO(proc.stdout)
    result = {}
    for expected in unique:
        header = stream.readline().rstrip(b"\n").decode("ascii").split()
        if len(header) != 3 or header[0] != expected or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header: {header}")
        size = int(header[2])
        result[expected] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("missing batch frame terminator")
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
        if record:
            meta, path = record.split(b"\t", 1)
            _mode, kind, oid = meta.decode("ascii").split()
            if kind == "blob":
                result[path.decode("utf-8")] = oid
    return result


def load_at(commit: str, path: str):
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


def full_suite_plan(exclusions: set[str]) -> tuple[list[dict[str, object]], list[str]]:
    rows: list[dict[str, object]] = []
    discovered: list[str] = []
    for path in sorted((REPO / "tests").glob("test*.py")):
        module_name = f"tests.{path.stem}"
        if module_name in NON_UNITTEST_SOURCE_TRANSFORMS:
            rows.append({"module": module_name, "test_ids": [], "classification": "historical_source_transform_no_unittest_credit"})
            continue
        importlib.invalidate_caches()
        tests = list(flatten(unittest.defaultTestLoader.loadTestsFromModule(importlib.import_module(module_name))))
        failed_loads = [test.id() for test in tests if test.__class__.__name__ == "_FailedTest"]
        if failed_loads:
            raise RuntimeError(f"test discovery failed for {module_name}: {failed_loads}")
        ids = sorted(test.id() for test in tests)
        discovered.extend(ids)
        eligible = [test_id for test_id in ids if test_id not in exclusions]
        rows.append({"module": module_name, "test_ids": eligible, "discovered_count": len(ids), "eligible_count": len(eligible)})
    missing = sorted(exclusions - set(discovered))
    if missing:
        raise RuntimeError(f"declared exact exclusions were not discovered: {missing}")
    return rows, discovered


def run_full_suite(exclusions: set[str]) -> tuple[dict, dict]:
    rows, discovered = full_suite_plan(exclusions)
    module_results = []
    total_run = total_failures = total_errors = total_skipped = 0
    environment = {**os.environ, "PYTHONUTF8": "1"}
    for row in rows:
        module_name = str(row["module"])
        ids = list(row.get("test_ids", []))
        if not ids:
            module_results.append({"module": module_name, "tests_run": 0, "failures": 0, "errors": 0, "skipped": 0, "successful": True, "classification": row.get("classification", "zero_discovered_tests")})
            continue
        proc = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", *ids], cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace", env=environment)
        output = proc.stdout + proc.stderr
        ran = re.search(r"Ran\s+(\d+)\s+tests?", output)
        count = int(ran.group(1)) if ran else 0
        failed = re.search(r"FAILED\s*\(([^)]*)\)", output)
        fields = dict((name, int(value)) for name, value in re.findall(r"(failures|errors|skipped)=(\d+)", failed.group(1))) if failed else {}
        failures = fields.get("failures", 0)
        errors = fields.get("errors", 0)
        skipped_match = re.search(r"OK\s*\(skipped=(\d+)\)", output)
        skipped = fields.get("skipped", int(skipped_match.group(1)) if skipped_match else 0)
        if proc.returncode and failures + errors == 0:
            errors = 1
        total_run += count
        total_failures += failures
        total_errors += errors
        total_skipped += skipped
        module_results.append({"module": module_name, "tests_run": count, "failures": failures, "errors": errors, "skipped": skipped, "successful": proc.returncode == 0, "output_tail": output[-1200:] if proc.returncode else ""})
    expected_run = len(discovered) - len(exclusions)
    successful = total_run == expected_run and total_failures == 0 and total_errors == 0 and total_skipped == 0 and all(row["successful"] for row in module_results)
    selection = {
        "mode": "one_coherent_module_isolated_pass",
        "tests_discovered": len(discovered),
        "exact_exclusions": sorted(exclusions),
        "tests_excluded": len(exclusions),
        "tests_run": total_run,
        "expected_tests_run": expected_run,
        "failures": total_failures,
        "errors": total_errors,
        "skipped": total_skipped,
        "failed_modules": [row for row in module_results if not row["successful"]],
        "canonical_successful_passes": 1 if successful else 0,
        "failed_incomplete_validator_attempts_retained": 1,
        "post_success_replay": False,
    }
    tests = {"passed": total_run - total_failures - total_errors, "total": total_run, "failures": total_failures, "errors": total_errors, "skipped": total_skipped}
    return selection, tests


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
    branch = git("branch", "--show-current")
    clean_before = not bool(git("status", "--porcelain=v1"))
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""

    prior_recovery = load_at(head, "docs/eiren-kestrel/v650-v7/validation/full-repository-suite-recovery.json")
    allowed_lifecycle = set(prior_recovery["exact_excluded_test_ids"]) | EXCLUDED
    selection, test_summary = run_full_suite(allowed_lifecycle)
    test_valid = selection["canonical_successful_passes"] == 1
    if not test_valid:
        issues.append("full_repository_suite")

    source_to_x1 = set(filter(None, git("diff", "--name-only", f"{SOURCE}..{X1}").splitlines()))
    x1_to_evidence = set(filter(None, git("diff", "--name-only", f"{X1}..{EVIDENCE}").splitlines()))
    evidence_to_final = set(filter(None, git("diff", "--name-only", f"{EVIDENCE}..{head}").splitlines()))
    owner_tree = set(tree_map(head, PHASE_ROOT))
    manifests = [
        manifest_check(X1, f"{PHASE_ROOT}/validation/x1-staged-manifest.json", source_to_x1),
        manifest_check(EVIDENCE, f"{PHASE_ROOT}/validation/evidence-staged-manifest.json", x1_to_evidence),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-delta-manifest.json", evidence_to_final),
        manifest_check(head, f"{PHASE_ROOT}/validation/final-owner-manifest.json", owner_tree),
    ]
    if not all(row["valid"] for row in manifests):
        issues.append("manifest_parity")

    owner_map = tree_map(head, PHASE_ROOT)
    owner_blobs = batch_blobs(list(owner_map.values()))
    json_count, json_issues, privacy_hits, word_issues = 0, [], [], []
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
        if path.endswith((".md", ".html")) and path != HANDOFF_PATH:
            count = len(re.findall(r"\b[\w'-]+\b", data.decode("utf-8")))
            if count > 6000:
                word_issues.append({"path": path, "words": count})
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
    portfolio = load_at(head, f"{PHASE_ROOT}/portfolios/expanded-portfolio-execution.json")
    environment = load_at(head, f"{PHASE_ROOT}/final/environment-receipt.json")
    staged_review = load_at(head, f"{PHASE_ROOT}/validation/final-staged-review.json")
    stale = load_at(head, f"{PHASE_ROOT}/validation/final-stale-label-review.json")
    selection_policy = load_at(head, f"{PHASE_ROOT}/validation/final-selection-policy.json")
    validation_plan = load_at(head, f"{PHASE_ROOT}/validation/final-validation-plan.json")
    cap_receipt = load_at(head, f"{PHASE_ROOT}/validation/final-document-cap-receipt.json")
    threshold = load_at(head, f"{PHASE_ROOT}/validation/final-owner-file-threshold.json")
    report = owner_blobs[owner_map[f"{PHASE_ROOT}/reports/final-static-report.html"]].decode("utf-8").casefold()
    overview = owner_blobs[owner_map[f"{PHASE_ROOT}/overview/final-integrated-overview.md"]].decode("utf-8")
    handoff = owner_blobs[owner_map[HANDOFF_PATH]].decode("utf-8")
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview))
    handoff_words = len(re.findall(r"\b[\w'-]+\b", handoff))
    phase_commits = int(git("rev-list", "--count", f"{SOURCE}..{head}"))
    merges = int(git("rev-list", "--count", "--merges", f"{SOURCE}..{head}"))
    parents = git("rev-list", "--parents", "-n", "1", head).split()
    parent_count = len(parents) - 1
    diff_hygiene = subprocess.run(["git", "diff", "--check", f"{EVIDENCE}..{head}"], cwd=REPO).returncode == 0

    detailed = {
        "expected_branch": branch == BRANCH,
        "local_equals_upstream": head == upstream,
        "local_equals_tracking": head == tracking,
        "local_equals_live": head == live,
        "clean_before": clean_before,
        "source_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE, head], cwd=REPO).returncode == 0,
        "x1_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", X1, head], cwd=REPO).returncode == 0,
        "evidence_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE, head], cwd=REPO).returncode == 0,
        "closeout_ancestral": subprocess.run(["git", "merge-base", "--is-ancestor", CLOSEOUT, head], cwd=REPO).returncode == 0,
        "four_phase_commits": phase_commits == 4,
        "zero_merges": merges == 0,
        "one_final_parent": parent_count == 1,
        "final_direct_child_of_closeout": parent_count == 1 and parents[1] == CLOSEOUT,
        "outcome_distribution": truth["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negative_retention": negatives["effective"] == 7086 and negatives["no_failure_erased"] and negatives["closeout_operational"] == 13,
        "open_gap_retention": gates["effective_open_gaps"] == 55 and gates["silently_closed"] == 0,
        "exact_gate_retention": gates["effective_exact_gates"] == 56 and gates["silently_closed"] == 0,
        "method_count": methods["counts"]["methods"] == 38,
        "method_states": methods["counts"]["states"]["preferred"] == 38,
        "failed_witness_count": methods["counts"]["witness_results"]["fail"] == 38,
        "passing_witness_count": methods["counts"]["witness_results"]["pass"] == 38,
        "x1_manifest": manifests[0]["valid"],
        "evidence_manifest": manifests[1]["valid"],
        "final_delta_manifest": manifests[2]["valid"],
        "final_owner_manifest": manifests[3]["valid"],
        "complete_json_parse": not json_issues and json_count > 0,
        "five_class_privacy_scan": not privacy_hits,
        "document_caps": not word_issues and cap_receipt["passed"],
        "overview_three_page_equivalent": 1500 <= overview_words <= 6000,
        "baton_word_contract": 8000 <= handoff_words <= 20000,
        "owner_files_below_rotation": len(owner_map) < 15000 and threshold["passed"],
        "route_prepared_not_sent": route["terminal_route"] == "PREPARED_NOT_SENT" and route["target_exact_title"] == "Ilyra Fen" and route["target_phase"] == "v651-v6",
        "send_count_zero": route["send_count"] == 0,
        "no_task_creation_or_fork": not route["task_created"] and not route["task_forked"],
        "no_cross_platform_or_subagent": not route["cross_platform_substitute"] and not route["collaboration_subagent"],
        "full_suite_external_binding": test_valid and selection["tests_run"] == selection["expected_tests_run"],
        "named_or_detached_replay_not_run": not truth["named_or_detached_replay_run"],
        "post_success_replay_not_run": not truth["post_success_replay_run"],
        "independent_reproduction_not_claimed": not truth["independent_reproduction_claimed"],
        "terminal_abstention": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "twenty_skills": skills["official_quick_validated"] == 20 and skills["smoke_used"] == 20,
        "ten_runners": runners["count"] == 10 and runners["passed"] == 10,
        "hundred_mutations": mutations["executed"] == 100 and mutations["rejected_or_quarantined"] == 100 and mutations["accepted"] == 0,
        "portfolio_floors": portfolio["completed_counts"] == {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40},
        "static_report_structural": all(phrase in report for phrase in ("skip to content", "assistive-technology", "affected-user evaluation remain reserved", "not complete accessibility conformance")),
        "exact_exclusion_set": set(selection["exact_exclusions"]) == allowed_lifecycle,
        "full_repository_suite": test_valid,
        "stale_label_review": stale["passed"] and not stale["stale_current_owner_or_route_labels"],
        "staged_review": staged_review["passed"] and not staged_review["forbidden_paths"],
        "selection_policy": selection_policy["full_repository_suite"] and set(selection_policy["exact_lifecycle_exclusions"]) == allowed_lifecycle and selection_policy["broad_exclusions_forbidden"],
        "validation_plan": validation_plan["credited_successful_aggregate_limit"] == 1 and not validation_plan["post_success_replay"] and validation_plan["complete_repository_suite"],
        "stale_route_state": "PREPARED_NOT_SENT" in handoff and route["terminal_route"] == "PREPARED_NOT_SENT",
        "diff_hygiene": diff_hygiene,
        "versions_observed_only": environment["versions_verified_only"] and not environment["desktop_updated"],
    }
    failed_detailed = [name for name, passed in detailed.items() if not passed]
    if failed_detailed:
        issues.extend("detailed:" + name for name in failed_detailed)
    minimal_names = ["expected_branch", "local_equals_upstream", "local_equals_tracking", "local_equals_live", "clean_before", "source_ancestral", "x1_ancestral", "evidence_ancestral", "closeout_ancestral", "four_phase_commits", "zero_merges", "one_final_parent", "final_direct_child_of_closeout", "outcome_distribution", "negative_retention", "open_gap_retention", "exact_gate_retention", "final_delta_manifest", "final_owner_manifest", "complete_json_parse", "five_class_privacy_scan", "full_repository_suite", "terminal_abstention"]
    minimal = {name: detailed[name] for name in minimal_names}
    clean_after = not bool(git("status", "--porcelain=v1"))
    if not clean_after:
        issues.append("clean_after")
    valid = not issues
    receipt = {
        "schema": "ghc.family.v651-v5.exact-final-validation.v1", "phase": "v651-v5", "owner": "Eiren Kestrel", "exact_head": head, "branch": branch,
        "selection": selection,
        "tests": test_summary,
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json": {"parsed": json_count, "issues": json_issues},
        "privacy": {"files_scanned": len(owner_map), "pattern_classes": sorted(PATTERNS), "confirmed_hits": privacy_hits, "zero_confirmed_hits": not privacy_hits, "boundary": "Five-class scanning is not privacy-complete assurance."},
        "manifests": manifests,
        "documents": {"overview_words": overview_words, "handoff_words": handoff_words, "issues": word_issues},
        "history": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "closeout": CLOSEOUT, "phase_commits": phase_commits, "merge_commits": merges, "final_parent_count": parent_count},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "live": live, "all_equal": head == upstream == tracking == live},
        "clean_before": clean_before, "clean_after": clean_after, "full_repository_suite_run": True, "named_or_detached_replay_run": False, "post_success_replay_run": False, "same_owner_only": True, "independent_reproduction": False,
        "issues": issues, "valid": valid, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": "One Eiren-owned exact-final module-isolated complete-repository aggregate with exact lifecycle exclusions only; the earlier zero-test validator attempt remains retained and no replay follows the first success. This is not independent reproduction or external audit.",
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"head": head, "tests": f"{receipt['tests']['passed']}/{receipt['tests']['total']}", "detailed": f"{receipt['detailed']['passed']}/{receipt['detailed']['total']}", "minimal": f"{receipt['minimal']['passed']}/{receipt['minimal']['total']}", "json": json_count, "privacy_files": len(owner_map), "manifest_entries": sum(row["entries"] for row in manifests), "clean_before": clean_before, "clean_after": clean_after, "all_equal": receipt["equality"]["all_equal"], "valid": valid}))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
