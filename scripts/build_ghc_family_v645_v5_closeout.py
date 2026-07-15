#!/usr/bin/env python3
"""Build the bounded precommit closeout candidate for Sable Rook v645-v5."""

from __future__ import annotations

import io
import json
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/sable-rook/v645-v5"
PHASE = "v645-gmut-thos-v5-x1-x2"
SOURCE = "3e0f37ec230252776e89841f12aa31b18dc21808"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
X1 = "2e330ab76f03c05ff556c484c22851d682b0ac7b"
EVIDENCE = "658466909006bf4403e8a346d8b7320d956a42b1"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v645_v5_validator import validate  # noqa: E402

MODULES = [
    "tests.test_ghc_family_v645_v3_x1", "tests.test_ghc_family_v645_v3",
    "tests.test_ghc_family_v645_v4_x1", "tests.test_ghc_family_v645_v4",
    "tests.test_ghc_family_v645_v5_x1", "tests.test_ghc_family_v645_v5",
]


def write(relative: str, payload: dict) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def run_tests() -> tuple[unittest.result.TestResult, float]:
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in MODULES:
        suite.addTests(loader.loadTestsFromName(module))
    stream = io.StringIO()
    started = time.perf_counter()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return result, time.perf_counter() - started


def main() -> int:
    tests, seconds = run_tests()
    detailed = validate("detailed")
    minimal = validate("minimal")
    write("validation/final-candidate-detailed.json", detailed)
    write("validation/final-candidate-minimal.json", minimal)

    identity_boundary = (
        "Sable Rook, they/them, is relational working language for an evidence-and-"
        "reproducibility steward. It is not evidence of consciousness, sentience, legal "
        "personhood, identity continuity, employment, professional qualification, or independent authority."
    )
    claim_boundary = (
        "This bounded software and synthetic evidence makes no empirical GMUT or likelihood, "
        "THOS effectiveness, production identity, aviation competence, legal or cultural authority, "
        "complete accessibility, exhaustive security, independent reproduction, AGI or ASI, "
        "consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim."
    )
    write("closeout-receipt.json", {
        "schema": "ghc.family.v645-v5.closeout-receipt.v1", "phase": PHASE,
        "owner": "Sable Rook", "state": "PRECOMMIT_CLOSEOUT_CANDIDATE",
        "source_revision": SOURCE, "source_seal": SOURCE_SEAL,
        "x1_commit": X1, "evidence_commit": EVIDENCE,
        "phase_commit_count_before_final": 2, "phase_commit_cap": 4,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expanded_workflow": {"safe_now_completed": 20, "candidate_prototypes_completed": 12, "skills_built_validated_used": 12, "runners_built_tested_used": 6, "clean_refine_completed": 20, "predecessor_completion_credit": 0, "exact_unexecuted": 10, "blocked_unexecuted": 5},
        "scoped_repository_tests": {"passed": tests.testsRun - len(tests.failures) - len(tests.errors), "total": tests.testsRun},
        "full_repository_suite_run_by_sable": False, "full_repository_suite_owner": "Eiren Kestrel",
        "detailed_validation": {"passed": detailed["passed"], "total": detailed["check_count"]},
        "minimal_validation": {"passed": minimal["passed"], "total": minimal["check_count"]},
        "effective_retained_negatives": 2168, "open_gaps": 7, "exact_gates": 8,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "postcommit_requirements": ["exact final-head canonical validation", "exactly one clean local named-lane replay", "final four-way remote equality", "exactly one sanitized activation baton to the existing Orin Thale task"],
        "identity_boundary": identity_boundary, "boundary": claim_boundary,
    })
    write("seal-receipt.json", {
        "schema": "ghc.family.v645-v5.seal-receipt.v1", "phase": PHASE,
        "state": "PRECOMMIT_SEAL_CANDIDATE", "source_revision": SOURCE,
        "source_seal": SOURCE_SEAL, "source_seal_ancestral": True,
        "x1_commit": X1, "evidence_commit": EVIDENCE,
        "x1_and_evidence_four_way_equal_before_successor_stage": True,
        "strict_x1_before_x2": True, "source_to_evidence_zero_merges": True,
        "owner_generated_files_under_15000": True, "phase_commit_cap": 4,
        "same_owner_repeatability_only": True, "independent_team_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "final_head_pending": True,
        "boundary": "The final commit and one named replay must still validate this candidate. This is change-control evidence, not a signature, scientific seal, credential, or authority grant.",
    })
    write("final-validation-record.json", {
        "schema": "ghc.family.v645-v5.final-validation-record.v1", "phase": PHASE,
        "state": "PRECOMMIT_FINAL_CANDIDATE", "canonical_evidence_head": EVIDENCE,
        "final_head": "SELF_PENDING_POSTCOMMIT_WITNESS",
        "canonical_scoped_tests": {"passed": tests.testsRun - len(tests.failures) - len(tests.errors), "total": tests.testsRun},
        "canonical_detailed": {"passed": detailed["passed"], "total": detailed["check_count"]},
        "canonical_minimal": {"passed": minimal["passed"], "total": minimal["check_count"]},
        "effective_retained_negatives": 2168, "open_gap_count": 7, "exact_gate_count": 8,
        "final_staged_review_pending": True, "named_replay_pending": True,
        "final_remote_equality_pending": True, "outbound_message_count": 0,
        "successor_task_count": 0, "same_owner_only": True,
        "independent_team_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "A commit cannot truthfully contain its own not-yet-created identifier; exact postcommit evidence belongs in the sanitized terminal closeout and baton.",
    })
    write("validation/final-scoped-test-receipt.json", {
        "schema": "ghc.family.scoped-test-receipt.v2", "phase": PHASE,
        "scope": ["v645-v3 x1 and x2", "v645-v4 x1 and x2", "v645-v5 x1 and x2"],
        "modules": MODULES, "tests_run": tests.testsRun,
        "failures": len(tests.failures), "errors": len(tests.errors),
        "seconds": round(seconds, 3), "result": "pass" if tests.wasSuccessful() else "fail",
        "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True, "independent_reproduction": False,
    })
    write("validation/final-ancestry-candidate.json", {
        "schema": "ghc.family.ancestry-candidate.v1", "phase": PHASE,
        "source_revision": SOURCE, "source_seal": SOURCE_SEAL,
        "x1_commit": X1, "evidence_commit": EVIDENCE,
        "required_ancestry": [SOURCE_SEAL, SOURCE, X1, EVIDENCE],
        "required_final_parent": EVIDENCE, "required_source_to_final_merge_count": 0,
        "required_final_parent_count": 1, "required_phase_commit_count": 3,
        "state": "postcommit_verification_pending",
    })
    write("validation/named-lane-replay-plan.json", {
        "schema": "ghc.family.named-lane-replay-plan.v1", "phase": PHASE,
        "replay_count_required": 1, "named_branch_required": True,
        "detached_worktree_forbidden": True, "local_only": True, "push_forbidden": True,
        "scope": "six v645-v3 through v645-v5 scoped modules plus detailed and minimal validators, JSON, five-class owner-blob privacy, commit-local manifests, ancestry, exact head, and clean checks",
        "same_owner_only": True, "independent_reproduction": False,
        "state": "pending_exact_final_head",
    })
    write("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.terminal-route-plan.v2", "phase": PHASE,
        "successor": "Orin Thale", "successor_phase": "v645-gmut-thos-v6-x1-x2",
        "existing_task_only": True, "create_or_fork_task": False,
        "message_count_before_final_validation": 0,
        "message_count_authorized_after_final_validation": 1,
        "standby_siblings_messaged": False, "state": "PREPARED_NOT_SENT",
        "privacy_boundary": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths.",
    })
    write("validation/commit-cap-candidate.json", {
        "schema": "ghc.family.commit-cap-candidate.v1", "phase": PHASE,
        "source_to_x1_commits": 1, "x1_to_evidence_commits": 1,
        "planned_final_commits": 1, "planned_phase_total": 3, "cap": 4,
        "zero_merge_required": True, "final_single_parent_required": True,
    })

    json_files = list(PHASE_DIR.rglob("*.json"))
    json_errors = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            json_errors.append(path.relative_to(PHASE_DIR).as_posix())
    docs = list(PHASE_DIR.rglob("*.md"))
    word_counts = {path.relative_to(PHASE_DIR).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in docs}
    write("validation/final-json-document-receipt.json", {
        "schema": "ghc.family.json-document-receipt.v2", "phase": PHASE,
        "json_parses_before_this_self_describing_receipt": len(json_files),
        "json_errors": json_errors, "markdown_documents": len(docs),
        "maximum_words": max(word_counts.values(), default=0),
        "over_6000_words": {key: value for key, value in word_counts.items() if value > 6000},
        "overview_words": word_counts.get("v645-v5-integrated-overview.md", 0),
        "result": "pass" if not json_errors and not any(value > 6000 for value in word_counts.values()) else "fail",
    })
    passed = tests.wasSuccessful() and detailed["result"] == "pass" and minimal["result"] == "pass" and not json_errors and not any(value > 6000 for value in word_counts.values())
    print(json.dumps({"tests": tests.testsRun, "detailed": detailed["check_count"], "minimal": minimal["check_count"], "json_before_receipt": len(json_files), "documents": len(docs), "result": "pass" if passed else "fail"}))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
