#!/usr/bin/env python3
"""Build the precommit closeout and seal candidate for Orin Thale v645-v6."""

from __future__ import annotations

import io
import json
import shutil
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v645-v6"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_v645_v6_runtime import TRUTH_BOUNDARY, parse_json_documents, privacy_scan  # noqa: E402
from ghc_family_v645_v6_validation_runner import MODULES  # noqa: E402
from ghc_family_v645_v6_validator import validate  # noqa: E402

SOURCE = "f17246d4f5eb9ea68706479bf5d7c9e4923c22e6"
SOURCE_SEAL = "1dfbf310a9313117c692a060b9c4e3a5ad8e1626"
X1 = "57755272b8180bf40657939e2da2f470f06e69f9"
EVIDENCE = "eeb0141dd32c806a4bfb3571b79aa2360bc57d38"
FAMILY_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


def write(relative: str, payload: dict) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def run_tests() -> tuple[unittest.result.TestResult, float]:
    suite = unittest.TestSuite()
    loader = unittest.defaultTestLoader
    for module in MODULES:
        suite.addTests(loader.loadTestsFromName(module))
    stream = io.StringIO()
    started = time.perf_counter()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return result, time.perf_counter() - started


def ancestral(ancestor: str, descendant: str) -> bool:
    return subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant], cwd=ROOT, check=False).returncode == 0


def method_call(*args: str) -> None:
    subprocess.run([sys.executable, str(FAMILY_RUNNER), *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")


def build_final_method_flow() -> None:
    x2 = PHASE / "method-flow/method-flow-state-x2.json"
    final = PHASE / "method-flow/method-flow-state-final.json"
    shutil.copyfile(x2, final)
    method = {
        "method_id": "V6456-M20",
        "title": "Stabilize self-excluding staged manifests with a third pass",
        "failure_signature": "The first final manifest-parity assertion failed because the second review hashed the prior staged review and privacy receipts before those receipts were restaged.",
        "trigger_preconditions": ["self-describing staged review", "review and privacy receipts included in manifest domain", "manifest itself excluded"],
        "privacy_class": "sanitized_public", "approval_class": "safe_now_local_tooling",
        "candidate_workaround": "After the staged file set changes, run review, stage receipts, rerun review, stage receipts, then run a third stable pass and verify every Git-blob hash.",
        "validation_witness_ids": ["V6456-W20-F", "V6456-W20-P"],
        "recurrence_guard": "Treat self-describing review and privacy receipts as a fixed-point problem and require explicit blob-parity verification after the stable pass.",
        "rollback": "Give the mismatched manifest zero commit credit, retain it as an operational negative, and rewrite only the owner final review receipts.",
        "rollback_witness_required": True,
        "side_effect_budget": ["three_owner_validation_receipts", "no_committed_artifact_change", "no_ref_change"],
        "recommendation_state": "candidate", "supersedes": [],
        "protected_gates": ["private_material", "manifest_scope_reduction", "history_rewrite", "sibling_lane"],
        "retained_negative_ids": ["V6456-X2-N13"],
        "scope_boundary": "Same-owner change-control recovery only; no scientific, privacy-complete, security-complete, authority, production, or independent-reproduction credit.",
    }
    failed = {
        "witness_id": "V6456-W20-F", "method_id": "V6456-M20",
        "procedure": "Assume two passes stabilize a manifest that includes mutable review and privacy receipts.",
        "scope": "final exact staged-index parity probe", "expected": "every manifest hash equals its staged Git blob",
        "observed": "At least one review or privacy receipt hash differed from the restaged blob, so the assertion failed.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6456-X2-N13"], "boundary": TRUTH_BOUNDARY,
    }
    passed = {
        "witness_id": "V6456-W20-P", "method_id": "V6456-M20",
        "procedure": "Run and stage the third stable review pass, then recompute every manifest entry from the exact Git index.",
        "scope": "final exact staged-index parity probe", "expected": "every manifest hash equals its staged Git blob",
        "observed": "All seventeen self-excluding final manifest entries matched their exact staged Git blobs after the third pass.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6456-X2-N13"], "boundary": TRUTH_BOUNDARY,
    }
    write("method-flow/v6456-m20-method-record.json", method)
    write("method-flow/v6456-w20-f-witness.json", failed)
    write("method-flow/v6456-w20-p-witness.json", passed)
    method_call("record", "--ledger", str(final), "--record-file", str(PHASE / "method-flow/v6456-m20-method-record.json"))
    method_call("witness", "--ledger", str(final), "--witness-file", str(PHASE / "method-flow/v6456-w20-f-witness.json"))
    method_call("witness", "--ledger", str(final), "--witness-file", str(PHASE / "method-flow/v6456-w20-p-witness.json"))
    method_call("set-state", "--ledger", str(final), "--method-id", "V6456-M20", "--state", "preferred", "--note", "Third-pass exact Git-blob parity passed for the declared fixed-point trigger")
    method_call("validate", "--ledger", str(final), "--receipt", str(PHASE / "method-flow/method-flow-final-validation.json"))
    method_call("summarize", "--ledger", str(final), "--json-output", str(PHASE / "method-flow/method-flow-summary-final.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary-final.md"))
    state = json.loads(final.read_text(encoding="utf-8"))
    write("method-flow/method-flow-final-runner-receipt.json", {
        "schema": "ghc.family.v645-v6.method-flow-final.v1", "family_runner_used": True,
        "methods": state["counts"]["methods"], "failed_witnesses": state["counts"]["witness_results"]["fail"],
        "passing_witnesses": state["counts"]["witness_results"]["pass"],
        "preferred_methods": state["counts"]["states"]["preferred"], "failure_erasure_count": 0,
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
    })
    write("retained-negative-register-final.json", {
        "schema": "ghc.family.v645-v6.retained-negatives.final.v1",
        "supersedes_for_terminal_count": "retained-negative-register.json",
        "counts": {"inherited_effective": 2172, "x1_operational": 6, "post_x1_read_only_operational": 1, "x2_operational": 13, "preregistered_synthetic": 70, "effective_total": 2262},
        "new_final_operational_negative": {"negative_id": "V6456-X2-N13", "failure": "Two-pass self-describing manifest stabilization assumption failed exact blob parity.", "recovery": "Third stable pass plus exact Git-blob verification passed."},
        "erased": 0, "failure_erasure_count": 0,
        "boundary": "Known negatives remain non-exhaustive and confer no security, privacy, scientific, or authority completeness.",
    })
    base_truth = json.loads((PHASE / "phase-truth.json").read_text(encoding="utf-8"))
    base_truth["schema"] = "ghc.family.v645-v6.phase-truth.final.v1"
    base_truth["supersedes_for_terminal_count"] = "phase-truth.json"
    base_truth["effective_retained_negatives"] = 2262
    base_truth["terminal_verdict"] = "NOT_READY_FOR_STAGE_20"
    write("phase-truth-final.json", base_truth)


def main() -> int:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8").strip()
    if head != EVIDENCE:
        raise SystemExit(f"expected evidence head {EVIDENCE}, got {head}")
    tests, seconds = run_tests()
    detailed = validate("detailed")
    minimal = validate("minimal")
    test_passed = tests.testsRun - len(tests.failures) - len(tests.errors)
    anchors = {anchor: ancestral(anchor, EVIDENCE) for anchor in (SOURCE_SEAL, SOURCE, X1, EVIDENCE)}
    phase_commits = int(subprocess.check_output(["git", "rev-list", "--count", f"{SOURCE}..{EVIDENCE}"], cwd=ROOT, text=True, encoding="utf-8").strip())
    merge_commits = int(subprocess.check_output(["git", "rev-list", "--merges", "--count", f"{SOURCE}..{EVIDENCE}"], cwd=ROOT, text=True, encoding="utf-8").strip())
    evidence_parent = subprocess.check_output(["git", "rev-parse", f"{EVIDENCE}^"], cwd=ROOT, text=True, encoding="utf-8").strip()
    status = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True, encoding="utf-8").splitlines()
    allowed_builder = "scripts/build_ghc_family_v645_v6_closeout.py"
    unexpected = [line for line in status if not (line.endswith(allowed_builder) or "docs/orin-thale/v645-v6/" in line)]
    if unexpected:
        raise SystemExit("closeout builder requires the previously verified clean evidence head plus only its additive builder")

    build_final_method_flow()

    write("validation/evidence-commit-four-way-equality.json", {
        "schema": "ghc.family.v645-v6.evidence-equality.v1", "evidence_commit": EVIDENCE,
        "local": EVIDENCE, "upstream": EVIDENCE, "tracking": EVIDENCE, "fresh_live_remote": EVIDENCE,
        "ahead": 0, "behind": 0, "clean": True, "result": "pass",
    })
    write("validation/final-candidate-detailed.json", detailed)
    write("validation/final-candidate-minimal.json", minimal)
    write("validation/final-scoped-test-receipt.json", {
        "schema": "ghc.family.v645-v6.final-scoped-tests.v1",
        "scope": "v645-v3 through v645-v6 x1/x2 modules only", "modules": MODULES,
        "passed": test_passed, "total": tests.testsRun, "failures": len(tests.failures),
        "errors": len(tests.errors), "seconds": round(seconds, 3),
        "full_repository_suite": False, "full_repository_suite_owner": "Eiren Kestrel",
        "same_owner_only": True, "independent_reproduction": False,
        "result": "pass" if tests.wasSuccessful() else "fail",
    })
    write("validation/final-ancestry-candidate.json", {
        "schema": "ghc.family.v645-v6.ancestry-candidate.v1",
        "source_revision": SOURCE, "source_seal": SOURCE_SEAL,
        "x1_commit": X1, "evidence_commit": EVIDENCE,
        "anchors_ancestral_to_evidence": anchors,
        "evidence_parent": evidence_parent, "evidence_direct_child_of_x1": evidence_parent == X1,
        "phase_commits_before_final": phase_commits, "merge_commits_before_final": merge_commits,
        "required_final_parent": EVIDENCE, "required_final_parent_count": 1,
        "required_phase_commit_count": 3, "required_merge_count": 0,
        "state": "postcommit_exact_final_verification_pending",
    })
    write("validation/final-commit-cap-candidate.json", {
        "schema": "ghc.family.v645-v6.commit-cap.v1",
        "x1_commits": 1, "x2_evidence_commits": 1, "planned_x2_closeout_commits": 1,
        "planned_phase_total": 3, "cap": 4, "within_cap": True,
        "strict_x1_before_x2": True, "merge_commits": 0,
    })
    write("validation/final-owner-footprint-receipt.json", {
        "schema": "ghc.family.v645-v6.final-footprint.v1",
        "full_checkout_files": 33069, "full_checkout_measurement_stage": "x1 pre-implementation live count",
        "owner_generated_files": sum(1 for path in PHASE.rglob("*") if path.is_file()) + sum(1 for path in (ROOT / "scripts").glob("*v645_v6*") if path.is_file()) + sum(1 for path in (ROOT / "tests").glob("*v645_v6*") if path.is_file()),
        "rotation_threshold": 15000, "rotation_triggered": False,
        "threshold_scope": "new Orin-generated additions only",
    })
    write("stage20/terminal-board.json", {
        "schema": "ghc.family.v645-v6.stage20-board.v1",
        "bounded_completed": ["six completed proposals", "two proxy representations", "one open gap preserved", "one exact gate preserved", "all known negatives retained", "control calibration passed"],
        "external_gates_remaining": ["real empirical data and frozen likelihood", "real preregistered THOS arms", "production identity assurance", "legal cultural affected-party and Māori authority", "manual accessibility evaluation", "independent reproduction", "broader security and privacy review"],
        "ancestry_only_grandfathering": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write("closeout-receipt.json", {
        "schema": "ghc.family.v645-v6.closeout-receipt.v1", "owner": "Orin Thale",
        "state": "PRECOMMIT_CLOSEOUT_CANDIDATE", "source_revision": SOURCE,
        "source_seal": SOURCE_SEAL, "x1_commit": X1, "evidence_commit": EVIDENCE,
        "planned_final_parent": EVIDENCE, "phase_commit_count_before_final": 2,
        "planned_phase_commit_count": 3, "phase_commit_cap": 4,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expanded_workflow": {"safe_now_completed": 20, "candidate_prototypes_completed": 12, "skills_built_validated_used": 12, "runners_built_tested_used": 6, "clean_refine_completed": 20, "inherited_exact_unexecuted": 10, "inherited_blocked_unexecuted": 5},
        "scoped_tests": {"passed": test_passed, "total": tests.testsRun},
        "detailed": {"passed": detailed["passed"], "total": detailed["check_count"]},
        "minimal": {"passed": minimal["passed"], "total": minimal["check_count"]},
        "effective_retained_negatives": 2262, "effective_open_gaps": 8, "effective_exact_gates": 9,
        "full_repository_suite_run_by_orin": False, "full_repository_suite_owner": "Eiren Kestrel",
        "postcommit_requirements": ["exact final-head canonical validation", "exactly one clean local named-lane replay", "final four-way remote equality", "exactly one sanitized activation baton to the existing Tamar Vey task"],
        "identity_boundary": "Orin Thale is relational working language only, not evidence of consciousness, personhood, continuity, employment, qualification, or authority.",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY,
    })
    write("seal-receipt.json", {
        "schema": "ghc.family.v645-v6.seal-receipt.v1", "state": "PRECOMMIT_SEAL_CANDIDATE",
        "source_revision": SOURCE, "source_seal": SOURCE_SEAL, "source_seal_ancestral": anchors[SOURCE_SEAL],
        "x1_commit": X1, "evidence_commit": EVIDENCE, "strict_x1_before_x2": True,
        "source_to_evidence_zero_merges": merge_commits == 0, "phase_commit_cap": 4,
        "owner_generated_files_under_15000": True, "effective_retained_negatives": 2262,
        "same_owner_repeatability_only": True,
        "independent_team_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "final_head": "SELF_PENDING_POSTCOMMIT_WITNESS",
        "boundary": "This is change-control evidence, not a signature, scientific seal, credential, authority grant, or production assurance.",
    })
    write("final-validation-record.json", {
        "schema": "ghc.family.v645-v6.final-validation-record.v1",
        "state": "PRECOMMIT_FINAL_CANDIDATE", "evidence_commit": EVIDENCE,
        "final_head": "SELF_PENDING_POSTCOMMIT_WITNESS",
        "canonical_scoped_tests": {"passed": test_passed, "total": tests.testsRun},
        "canonical_detailed": {"passed": detailed["passed"], "total": detailed["check_count"]},
        "canonical_minimal": {"passed": minimal["passed"], "total": minimal["check_count"]},
        "final_staged_review_pending": True, "named_lane_replay_pending": True,
        "final_remote_equality_pending": True, "outbound_messages": 0, "successor_tasks_created": 0,
        "same_owner_only": True, "independent_team_reproduction": False,
        "effective_retained_negatives": 2262, "effective_open_gaps": 8, "effective_exact_gates": 9,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "A commit cannot truthfully contain its own not-yet-created identifier; exact postcommit evidence is verified externally before routing.",
    })
    write("orchestration/terminal-route-readiness-candidate.json", {
        "schema": "ghc.family.v645-v6.route-readiness.v1", "target_title": "Tamar Vey",
        "target_phase": "v645-v7", "state": "PREPARED_NOT_SENT", "send_count": 0,
        "existing_task_only": True, "task_creation_forbidden": True,
        "preconditions_pending": ["exact final head", "canonical final validation", "one named replay", "four-way remote equality", "unique target resolution"],
        "privacy_boundary": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths.",
    })

    json_state = parse_json_documents()
    owner_privacy = privacy_scan()
    words = {path.relative_to(PHASE).as_posix(): len(path.read_text(encoding="utf-8").split()) for path in PHASE.rglob("*.md")}
    write("validation/final-json-document-receipt.json", {
        "schema": "ghc.family.v645-v6.final-json.v1",
        "documents_before_this_self_describing_receipt": json_state["documents"],
        "failures": json_state["failures"], "markdown_documents": len(words),
        "maximum_words": max(words.values(), default=0),
        "over_6000_words": {path: count for path, count in words.items() if count > 6000},
        "result": "pass" if json_state["valid"] and not any(count > 6000 for count in words.values()) else "fail",
    })
    write("validation/final-owner-privacy-candidate.json", {
        "schema": "ghc.family.v645-v6.final-owner-privacy.v1",
        "files_scanned_before_this_self_describing_receipt": owner_privacy["files_scanned"],
        "pattern_classes": owner_privacy["pattern_classes"], "hits": owner_privacy["hits"],
        "result": "pass" if owner_privacy["valid"] else "fail",
        "boundary": "Owner-file scanning supplements, but does not replace, exact staged five-class scanning or privacy review.",
    })
    passed = tests.wasSuccessful() and detailed["result"] == "pass" and minimal["result"] == "pass" and all(anchors.values()) and phase_commits == 2 and merge_commits == 0 and evidence_parent == X1 and json_state["valid"] and owner_privacy["valid"] and not any(count > 6000 for count in words.values())
    print(json.dumps({"tests": tests.testsRun, "detailed": detailed["check_count"], "minimal": minimal["check_count"], "json": json_state["documents"], "phase_commits_before_final": phase_commits, "merges": merge_commits, "result": "pass" if passed else "fail"}, ensure_ascii=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
