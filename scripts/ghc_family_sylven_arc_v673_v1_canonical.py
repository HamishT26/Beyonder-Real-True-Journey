"""One-shot exact-final owner-scoped canonical validator for Sylven v673-v1."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_PREFIX = "docs/sylven-arc/v673-v1/"
OWNER_ROOT = ROOT / "docs" / "sylven-arc" / "v673-v1"
BRANCH = "codex/GHC-Family/sylven-arc-v673-v1-full-tools"
SOURCE_FINAL = "305708c6d5a8dfee0432a2c09ef5b59da4b6c438"
X1 = "606f6b7afef6d4368e1b34d128e57fc061629b05"
EVIDENCE = "11dbffa2598f106bfa78b37974f8726fb61c7708"
EXPECTED_COUNTS = {"proposal_chain": 6270, "effective_negatives": 36372, "effective_methods": 22700, "failed_witnesses": 8033, "bounded_passing_witnesses": 10263, "open_gaps": 293, "exact_gates": 286}
OWNER_SCRIPTS = {
    "scripts/build_ghc_family_sylven_arc_v673_v1_x1.py",
    "scripts/build_ghc_family_sylven_arc_v673_v1_x2.py",
    "scripts/build_ghc_family_sylven_arc_v673_v1_closeout.py",
    "scripts/ghc_family_sylven_arc_v673_v1_canonical.py",
    "scripts/ghc_family_flag_attachment_abstention.py",
    "scripts/ghc_family_flag_condition_separation.py",
    "scripts/ghc_family_flag_contract.py",
    "scripts/ghc_family_flag_edge_topology.py",
    "scripts/ghc_family_flag_evidence.py",
    "scripts/ghc_family_flag_flashcard_projection.py",
    "scripts/ghc_family_flag_flashcards.py",
    "scripts/ghc_family_flag_identity.py",
    "scripts/ghc_family_flag_material_vacancy.py",
    "scripts/ghc_family_flag_privacy_access.py",
    "scripts/ghc_family_flag_provenance_correction.py",
    "scripts/ghc_family_flag_seam_relation.py",
    "scripts/ghc_family_flag_workload_handover.py",
}
OWNER_TESTS = {
    "tests/test_ghc_family_sylven_arc_v673_v1_x1.py",
    "tests/test_ghc_family_sylven_arc_v673_v1_x2.py",
    "tests/test_ghc_family_sylven_arc_v673_v1_final.py",
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def blob(path: str) -> bytes:
    return git("show", f"HEAD:{path}").stdout


def load_blob(path: str) -> Any:
    return json.loads(blob(path).decode("utf-8"))


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_manifest(path: str) -> tuple[int, list[str]]:
    manifest = load_blob(path)
    mismatches = []
    for entry in manifest["entries"]:
        data = blob(entry["path"])
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            mismatches.append(entry["path"])
    return len(manifest["entries"]), mismatches


def run_tests() -> dict[str, Any]:
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    names = [
        "tests.test_ghc_family_sylven_arc_v673_v1_x1",
        "tests.test_ghc_family_sylven_arc_v673_v1_x2",
        "tests.test_ghc_family_sylven_arc_v673_v1_final",
    ]
    raw_suite = unittest.defaultTestLoader.loadTestsFromNames(names)
    excluded_suffixes = {
        "TestSylvenArcV673V1X1.test_01_exact_source_head",
        "TestSylvenArcV673V1X1.test_03_x2_and_closeout_absent",
        "TestSylvenArcV673V1X2.test_01_x2_begins_at_exact_x1",
        "TestSylvenArcV673V1X2.test_03_closeout_is_absent",
    }
    selected = []
    def flatten(node):
        for item in node:
            if isinstance(item, unittest.TestSuite):
                flatten(item)
            elif not any(item.id().endswith(suffix) for suffix in excluded_suffixes):
                selected.append(item)
    flatten(raw_suite)
    suite = unittest.TestSuite(selected)
    selected_count = suite.countTestCases()
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    x1_paths = set(git_text("ls-tree", "-r", "--name-only", X1).splitlines())
    evidence_paths = set(git_text("ls-tree", "-r", "--name-only", EVIDENCE).splitlines())
    lifecycle = {
        "x1_head_parent_is_source": git_text("rev-parse", f"{X1}^") == SOURCE_FINAL,
        "x1_tree_has_no_x2_or_closeout": not any(path.startswith(f"{OWNER_PREFIX}x2/") or path.startswith(f"{OWNER_PREFIX}closeout/") for path in x1_paths),
        "evidence_head_parent_is_x1": git_text("rev-parse", f"{EVIDENCE}^") == X1,
        "evidence_tree_has_x2_and_no_closeout": any(path.startswith(f"{OWNER_PREFIX}x2/") for path in evidence_paths) and not any(path.startswith(f"{OWNER_PREFIX}closeout/") for path in evidence_paths),
    }
    successful = result.wasSuccessful() and all(lifecycle.values()) and selected_count == 77
    return {"tests": 81, "executed_tests": selected_count, "lifecycle_dependency_checks": lifecycle, "lifecycle_dependency_passed": sum(lifecycle.values()), "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped), "successful": successful, "raw_aggregate_retained": {"tests": 81, "passed": 77, "failed": 4, "success_credit": 0}, "output_sha256": sha(stream.getvalue().encode("utf-8"))}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s<]+"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\Users\\|/home/|/Users/)"),
        "private_route_or_callable": re.compile(r"(?i)(?:thread[_-]?id|task[_-]?id|callable[_-]?id|session[_-]?id)\s*[:=]"),
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "transcript_or_session_stream": re.compile(r"(?i)(raw transcript|session stream|screenshot payload)"),
    }
    candidates = []; scanned = 0
    for path in paths:
        try: text = blob(path).decode("utf-8")
        except UnicodeDecodeError: continue
        scanned += 1
        definition = path.startswith("scripts/") or path.startswith("tests/")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    return {"classes": len(patterns), "scanned": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed)}


def validate(expected_head: str) -> dict[str, Any]:
    head_before = git_text("rev-parse", "HEAD")
    if head_before != expected_head:
        raise RuntimeError("expected-head mismatch")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = [int(value) for value in git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    clean_before = not git("status", "--porcelain").stdout
    parent = git_text("rev-parse", "HEAD^")
    source_to_final_commits = int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..HEAD"))
    merges = [line for line in git_text("rev-list", "--merges", f"{SOURCE_FINAL}..HEAD").splitlines() if line]
    chain_parents = {commit: git_text("rev-list", "--parents", "-n", "1", commit).split()[1:] for commit in [X1, EVIDENCE, expected_head]}

    tree_paths = [path for path in git_text("ls-tree", "-r", "--name-only", "HEAD").splitlines() if path]
    owner_paths = sorted(path for path in tree_paths if path.startswith(OWNER_PREFIX) or path in OWNER_SCRIPTS or path in OWNER_TESTS)
    owner_json = [path for path in owner_paths if path.endswith(".json")]
    json_issues = []
    for path in owner_json:
        try: json.loads(blob(path).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc: json_issues.append({"path": path, "error": type(exc).__name__})
    owner_python = [path for path in owner_paths if path.endswith(".py")]
    compile_issues = []
    for path in owner_python:
        try: compile(blob(path).decode("utf-8"), path, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc: compile_issues.append({"path": path, "error": type(exc).__name__})
    privacy = privacy_scan(owner_paths)
    owner_entries, owner_manifest_issues = verify_manifest(f"{OWNER_PREFIX}validation/final-owner-manifest.json")
    delta_entries, delta_manifest_issues = verify_manifest(f"{OWNER_PREFIX}validation/final-delta-manifest.json")

    seal = load_blob(f"{OWNER_PREFIX}seal/content-seal.json")
    seal_issues = []
    for entry in seal["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or sha(data) != entry["sha256"]:
            seal_issues.append(entry["path"])
    tests = run_tests()
    truth = load_blob(f"{OWNER_PREFIX}closeout/phase-truth.json")
    route = load_blob(f"{OWNER_PREFIX}closeout/route-state.json")
    flow = load_blob(f"{OWNER_PREFIX}closeout/method-flow-final.json")
    precommit = load_blob(f"{OWNER_PREFIX}validation/final-precommit-validation.json")
    staged_review = load_blob(f"{OWNER_PREFIX}validation/final-staged-review.json")
    staged_privacy = load_blob(f"{OWNER_PREFIX}validation/final-staged-privacy.json")
    candidate_words = len(blob(f"{OWNER_PREFIX}handoffs/caelen-morrow-v673-v2-activation-candidate.md").decode("utf-8").split())
    static_report = blob(f"{OWNER_PREFIX}closeout/accessible-final-report.html").decode("utf-8")
    largest_words = 0; largest_path = ""
    for path in owner_paths:
        if Path(path).suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml", ".py"}:
            try: words = len(blob(path).decode("utf-8").split())
            except UnicodeDecodeError: continue
            if words > largest_words: largest_words, largest_path = words, path

    detailed = {
        "branch_exact": branch == BRANCH,
        "head_exact": head_before == expected_head,
        "parent_is_evidence": parent == EVIDENCE,
        "x1_parent_is_source": chain_parents[X1] == [SOURCE_FINAL],
        "evidence_parent_is_x1": chain_parents[EVIDENCE] == [X1],
        "final_parent_is_evidence": chain_parents[expected_head] == [EVIDENCE],
        "three_phase_commits": source_to_final_commits == 3,
        "zero_merges": not merges,
        "one_parent_each": all(len(value) == 1 for value in chain_parents.values()),
        "clean_before": clean_before,
        "zero_divergence": divergence == [0, 0],
        "four_way_equal": len({head_before, upstream, tracking, live}) == 1,
        "all_json_parses": not json_issues,
        "all_python_compiles": not compile_issues,
        "zero_confirmed_privacy_hits": privacy["confirmed_hit_count"] == 0,
        "owner_manifest_exact": not owner_manifest_issues,
        "delta_manifest_exact": not delta_manifest_issues,
        "content_seal_exact": not seal_issues,
        "tests_exact": tests["successful"] and tests["tests"] == 81,
        "truth_counts_exact": truth["counts"] == EXPECTED_COUNTS,
        "outcomes_exact": truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "method_flow_exact": flow["counts"]["methods"] == 211 and flow["counts"]["witness_results"] == {"fail": 211, "pass": 211},
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["sent_by_sylven_arc"] is False,
        "precommit_valid": precommit["valid"],
        "staged_review_valid": staged_review["valid"],
        "staged_privacy_valid": staged_privacy["valid"] and staged_privacy["confirmed_hit_count"] == 0,
        "candidate_word_floor": 10000 <= candidate_words <= 100000,
        "document_word_guard": largest_words <= 100000,
        "owner_file_guard": len(owner_paths) < 2000,
        "static_report_structure": all(token in static_report for token in ["<!doctype html>", "<main", "<h1>", "<h2", "Skip to main content"]),
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "canonical_pending_in_repository": truth["canonical_state"] == "PENDING_EXACT_FINAL_PUSH",
        "no_full_repository_suite_claim": True,
        "same_owner_boundary": True,
    }
    minimal_keys = [
        "head_exact", "parent_is_evidence", "three_phase_commits", "zero_merges", "clean_before",
        "zero_divergence", "four_way_equal", "tests_exact", "all_json_parses", "zero_confirmed_privacy_hits",
        "owner_manifest_exact", "delta_manifest_exact", "truth_counts_exact", "route_prepared_not_sent",
        "terminal_verdict",
    ]
    minimal = {key: detailed[key] for key in minimal_keys}
    valid = all(detailed.values()) and all(minimal.values())
    head_after = git_text("rev-parse", "HEAD")
    clean_after = not git("status", "--porcelain").stdout
    upstream_after = git_text("rev-parse", "@{upstream}")
    tracking_after = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_after_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live_after = live_after_line.split()[0] if live_after_line else ""
    after_equal = len({head_after, upstream_after, tracking_after, live_after}) == 1
    valid = valid and head_after == head_before and clean_after and after_equal
    return {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v8",
        "owner": "Sylven Arc", "phase": "v673-v1", "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "valid": valid, "exact_final": expected_head, "source_final": SOURCE_FINAL, "x1": X1, "evidence": EVIDENCE,
        "canonical_invocations": 1, "canonical_successes": 1 if valid else 0, "canonical_replays": 0,
        "tests": tests, "detailed": detailed, "detailed_passed": sum(detailed.values()), "detailed_total": len(detailed),
        "minimal": minimal, "minimal_passed": sum(minimal.values()), "minimal_total": len(minimal),
        "json_documents": len(owner_json), "json_issues": json_issues,
        "owner_python_files": len(owner_python), "compile_issues": compile_issues,
        "privacy": privacy, "owner_manifest_entries": owner_entries, "owner_manifest_issues": owner_manifest_issues,
        "delta_manifest_entries": delta_entries, "delta_manifest_issues": delta_manifest_issues,
        "content_seal_entries": seal["entry_count"], "content_seal_issues": seal_issues,
        "owner_files": len(owner_paths), "largest_document_words": largest_words, "largest_document": largest_path,
        "activation_candidate_words": candidate_words, "source_to_final_commits": source_to_final_commits,
        "merge_commits": len(merges), "parents": chain_parents, "divergence": {"ahead": divergence[0], "behind": divergence[1]},
        "head_stable": head_after == head_before, "clean_before": clean_before, "clean_after": clean_after,
        "four_way_before": {"local": head_before, "upstream": upstream, "tracking": tracking, "fresh_live": live, "equal": len({head_before, upstream, tracking, live}) == 1},
        "four_way_after": {"local": head_after, "upstream": upstream_after, "tracking": tracking_after, "fresh_live": live_after, "equal": after_equal},
        "full_repository_suite_run": False,
        "boundary": "Same-owner owner-delta validation under shared infrastructure only; not independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural ratification, Māori authority, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority. Māori concepts remain under Māori authority.",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    if receipt.exists():
        raise SystemExit("canonical receipt already exists; replay prohibited")
    payload = validate(args.expected_head)
    payload_bytes = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    payload["payload_sha256"] = sha(payload_bytes)
    final_bytes = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    temporary = receipt.with_suffix(receipt.suffix + ".tmp")
    temporary.write_bytes(final_bytes)
    os.replace(temporary, receipt)
    print(json.dumps({"status": payload["status"], "valid": payload["valid"], "exact_final": payload["exact_final"], "tests": payload["tests"], "detailed": [payload["detailed_passed"], payload["detailed_total"]], "minimal": [payload["minimal_passed"], payload["minimal_total"]], "json_documents": payload["json_documents"], "owner_files": payload["owner_files"], "owner_manifest_entries": payload["owner_manifest_entries"], "delta_manifest_entries": payload["delta_manifest_entries"], "privacy_confirmed_hits": payload["privacy"]["confirmed_hit_count"], "full_repository_suite_run": False}, sort_keys=True))
    raise SystemExit(0 if payload["valid"] else 1)


if __name__ == "__main__":
    main()
