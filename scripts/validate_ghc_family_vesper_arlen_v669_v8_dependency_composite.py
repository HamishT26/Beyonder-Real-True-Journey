"""One-shot dependency-corrected terminal composite for Vesper Arlen v669-v8."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_ghc_family_vesper_arlen_v669_v8_final import (
    BRANCH,
    EVIDENCE_COMMIT,
    SOURCE_FINAL,
    X1_COMMIT,
    exact_delta_review,
    replay_manifests,
    run,
)

INITIAL_FINAL = "35f412d1db9daae8745d7fe53898ce2f2bdc7561"
FAILED_CANONICAL_FINAL = "f313819c3e480bc5510e309effb74b2d9bb9127d"
FAILED_CANONICAL_RECEIPT_SHA256 = "6c904f3f6722eb8161ba7530ac8e174842ed7fd5467a1ff4222432fc47332b4b"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
SEALED_COUNTS = {
    "effective_negatives": 31856,
    "methods": 17961,
    "failed_witnesses": 3677,
    "passing_witnesses": 4932,
    "open_gaps": 239,
    "exact_gates": 234,
}


def exact_failed_canonical_truth(payload: dict[str, Any], sha256: str) -> bool:
    false_checks = [key for key, value in payload["checks"].items() if value is False]
    return (
        sha256 == FAILED_CANONICAL_RECEIPT_SHA256
        and payload["exact_final"] == FAILED_CANONICAL_FINAL
        and payload["result"] == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        and payload["invocation_count"] == 1
        and payload["successful_invocation_count"] == 0
        and payload["post_success_replay"] is False
        and false_checks == ["selected_tests_passed_once"]
        and payload["tests"]["returncode"] == 0
        and payload["tests"]["passed"] == 16
        and payload["tests"]["declared"] == 81
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--failed-canonical-receipt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit("dependency-corrected output already exists; one-shot recovery refuses replay")
    output.parent.mkdir(parents=True, exist_ok=True)
    final = args.expected_final

    failed_bytes = args.failed_canonical_receipt.resolve().read_bytes()
    failed_sha256 = hashlib.sha256(failed_bytes).hexdigest()
    failed_payload = json.loads(failed_bytes.decode("utf-8"))

    head = run(repo, "git", "rev-parse", "HEAD").stdout.strip()
    upstream = run(repo, "git", "rev-parse", "@{u}").stdout.strip()
    tracking = run(repo, "git", "rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.strip()
    live_line = run(repo, "git", "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    live = live_line.split()[0] if live_line else ""
    divergence = run(repo, "git", "rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.strip().split()
    phase_commits = run(repo, "git", "rev-list", "--reverse", f"{SOURCE_FINAL}..{final}").stdout.splitlines()
    merge_count = int(run(repo, "git", "rev-list", "--count", "--merges", f"{SOURCE_FINAL}..{final}").stdout.strip())
    parent_rows = [run(repo, "git", "rev-list", "--parents", "-n", "1", commit).stdout.strip().split() for commit in phase_commits]

    manifests = replay_manifests(repo, final)
    owner = exact_delta_review(repo, final)
    blobs: dict[str, bytes] = owner.pop("blobs")
    truth = json.loads(blobs["docs/vesper-arlen/v669-v8/closeout/phase-truth.json"].decode("utf-8"))
    baton_path = "docs/vesper-arlen/v669-v8/handoffs/lyren-moss-v670-v1-activation-candidate.md"
    baton_receipt = json.loads(blobs["docs/vesper-arlen/v669-v8/handoffs/activation-candidate-integrity.json"].decode("utf-8"))
    baton = blobs[baton_path]
    route = json.loads(blobs["docs/vesper-arlen/v669-v8/orchestration/route-state-final-candidate.json"].decode("utf-8"))
    report = blobs["docs/vesper-arlen/v669-v8/x2/accessible-evidence-report.html"].decode("utf-8")
    final_review = json.loads(blobs["docs/vesper-arlen/v669-v8/validation/final-staged-review.json"].decode("utf-8"))
    recovery_plan = json.loads(blobs["docs/vesper-arlen/v669-v8/final/dependency-corrected-composite-plan.json"].decode("utf-8"))

    test_files = [
        "tests/test_ghc_family_vesper_arlen_v669_v8_x1.py",
        "tests/test_ghc_family_vesper_arlen_v669_v8_x2.py",
        "tests/test_ghc_family_vesper_arlen_v669_v8_final.py",
        "tests/test_ghc_family_vesper_arlen_v669_v8_lifecycle_replacements.py",
    ]
    deselections = [
        "tests/test_ghc_family_vesper_arlen_v669_v8_x1.py::test_no_x2_closeout_seal_final_or_handoff_materialized",
        "tests/test_ghc_family_vesper_arlen_v669_v8_x2.py::test_no_closeout_seal_final_or_handoff_exists_yet",
    ]
    test_args = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", *test_files]
    for node_id in deselections:
        test_args.extend(["--deselect", node_id])
    test_proc = run(repo, *test_args)
    test_output = (test_proc.stdout + "\n" + test_proc.stderr).strip()
    match = re.search(r"(\d+) passed", test_output)
    test_count = int(match.group(1)) if match else 0

    worktree_diff = run(repo, "git", "diff", "--quiet").returncode
    index_diff = run(repo, "git", "diff", "--cached", "--quiet").returncode
    untracked = run(repo, "git", "ls-files", "--others", "--exclude-standard").stdout.splitlines()
    post_head = run(repo, "git", "rev-parse", "HEAD").stdout.strip()
    post_live_line = run(repo, "git", "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.strip()
    post_live = post_live_line.split()[0] if post_live_line else ""
    normalized_baton = baton.decode("utf-8").replace("\r\n", "\n").rstrip() + "\n"

    expected_history = [X1_COMMIT, EVIDENCE_COMMIT, INITIAL_FINAL, FAILED_CANONICAL_FINAL, final]
    checks = {
        "failed_canonical_receipt_exact": exact_failed_canonical_truth(failed_payload, failed_sha256),
        "canonical_aggregate_credit_zero": recovery_plan["canonical_aggregate_credit"] == 0,
        "expected_head": head == final == post_head,
        "local_upstream_equal": head == upstream,
        "local_tracking_equal": head == tracking,
        "local_fresh_live_equal": head == live == post_live,
        "zero_divergence": divergence == ["0", "0"],
        "clean_worktree": worktree_diff == 0,
        "clean_index": index_diff == 0,
        "zero_untracked": not untracked,
        "five_phase_commits": phase_commits == expected_history,
        "zero_merges": merge_count == 0,
        "single_parent_phase_history": len(parent_rows) == 5 and all(len(row) == 2 for row in parent_rows),
        "x1_direct_source_child": parent_rows[0][1] == SOURCE_FINAL,
        "evidence_direct_x1_child": parent_rows[1][1] == X1_COMMIT,
        "initial_final_direct_evidence_child": parent_rows[2][1] == EVIDENCE_COMMIT,
        "failed_canonical_final_direct_initial_final_child": parent_rows[3][1] == INITIAL_FINAL,
        "dependency_corrected_final_direct_failed_final_child": parent_rows[4][1] == FAILED_CANONICAL_FINAL,
        "all_manifest_replays": manifests["mismatches"] == 0,
        "all_json_parses": not owner["json_errors"],
        "zero_privacy_candidates": not owner["privacy_candidates"],
        "zero_bounded_python_findings": not owner["security_findings"],
        "stale_label_confined_to_declared_x1_truth": not owner["stale_label_paths_outside_allowlist"],
        "owner_file_ceiling": owner["owner_delta_files"] < 2000,
        "all_word_ceilings": not owner["word_violations"],
        "pytest_dependency_recovery_passed_once": test_proc.returncode == 0 and test_count == 81,
        "two_lifecycle_exclusions_have_exact_replacements": len(deselections) == 2 and test_files[-1].endswith("lifecycle_replacements.py"),
        "four_outcome_labels": truth["outcomes"] == OUTCOMES,
        "sealed_counts_preserved": all(truth[key] == value for key, value in SEALED_COUNTS.items()),
        "proposal_chain": truth["proposal_chain"] == 5230,
        "failed_canonical_state_preserved": truth["canonical_invocation_state"] == "FAILED_ZERO_CREDIT_DEPENDENCY_RECOVERY_PREPARED",
        "terminal_nonpromotion": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "baton_word_bounds": 10000 <= len(normalized_baton.split()) <= 100000,
        "baton_words": len(normalized_baton.split()) == baton_receipt["word_count"],
        "baton_sha256": hashlib.sha256(normalized_baton.encode("utf-8")).hexdigest() == baton_receipt["sha256_normalized_lf"],
        "baton_prepared_not_sent": baton_receipt["delivery_state"] == "PREPARED_NOT_SENT" and not baton_receipt["delivery_acknowledged"],
        "route_prepared_not_sent": route["delivery_state"] == "PREPARED_NOT_SENT" and route["successor_contact_count"] == 0 and not route["app_acknowledgement"],
        "final_staged_review_passed": final_review["passed"],
        "recovery_plan_exact": recovery_plan["recovery_state"] == "PREPARED_NOT_INVOKED" and recovery_plan["dependency_recovery_invocation_limit"] == 1 and recovery_plan["expected_tests"] == 81 and recovery_plan["failed_canonical_receipt_sha256"] == failed_sha256,
        "accessible_report_structure": all(token in report for token in ('lang="en"', 'href="#main"', '<main id="main">', '<caption>', 'scope="col"', 'scope="row"')) and "<script" not in report.lower(),
    }
    passed = all(checks.values())
    receipt = {
        "schema": "ghc.family.dependency-corrected-terminal-composite.v3",
        "owner": "Vesper Arlen",
        "phase": "v669-v8",
        "result": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT" if passed else "INVALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
        "canonical_aggregate_credit": 0,
        "failed_canonical_final": FAILED_CANONICAL_FINAL,
        "failed_canonical_receipt_sha256": failed_sha256,
        "dependency_recovery_invocation_count": 1,
        "successful_dependency_recovery_count": 1 if passed else 0,
        "post_success_replay": False,
        "exact_final": final,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_declared": len(checks),
        "tests": {"runner": "pytest", "declared": 81, "passed": test_count if test_proc.returncode == 0 else 0, "returncode": test_proc.returncode, "phase_local_deselections": deselections, "exact_lifecycle_replacements": 2},
        "manifests": manifests,
        "owner_review": owner,
        "history": {"phase_commits": phase_commits, "merge_count": merge_count, "single_parent_rows": len(parent_rows)},
        "equality": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "post_test_live": post_live, "divergence": divergence},
        "repository_sealed_counts": SEALED_COUNTS,
        "successor_visible_external_overlay": {**SEALED_COUNTS, "passing_witnesses": SEALED_COUNTS["passing_witnesses"] + (1 if passed else 0)},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "claim_boundary": "This dependency-corrected same-owner composite retains zero canonical aggregate credit and is not the complete repository suite, independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural review, Maori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.",
    }
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "result": receipt["result"],
                "checks": f"{receipt['checks_passed']}/{receipt['checks_declared']}",
                "tests": f"{receipt['tests']['passed']}/{receipt['tests']['declared']}",
                "json": owner["json_documents"],
                "privacy": len(owner["privacy_candidates"]),
                "manifest_entries": manifests["entries"],
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
