#!/usr/bin/env python3
"""Prepare the policy-cardinality correction after the all-tests-passed invalid receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/sylven-arc/v688-v7"
REL = "docs/sylven-arc/v688-v7"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"
FIRST_FINAL = "4e2421659eed8617cbd1fd45677b7248db2dfd11"
C1 = "c0f79218f2d644592bd4eee0947058f0f3803b50"
C2 = "1b00ec2df09e02ef63b370d6c8b15180044b3a38"
C3 = "b105ef20548eb149b0f88fe9908c5b1ff5d81dca"
FAILED2_SHA = "526b15d930704f592486754db0547a594f0590329728cb7084de89a797eb2014"
FAILED3_SHA = "0383cb436f6167a1d80d552dd961f67e97613f207273947868eb11cc99655c10"
RECOVERY_SHA = "56646c01100763254f584d667be5324d00fbab74530d00666a26c517ad4002fb"
BOUNDARY = "Same-owner canonical-cardinality correction only; both prior canonical receipts remain invalid with zero success credit. No empirical, participant, professional, production, legal, cultural, Maori-authority, independent-reproduction, consciousness, Theory-of-Everything, proof, canon, or Stage 20 evidence."


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value.rstrip() + "\n" if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:" or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != C3:
        raise RuntimeError("D_first_and_exact_correction3_required")
    if subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).strip():
        raise RuntimeError("unexpected_staged_entry")
    status = set(line for line in subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).splitlines() if line)
    expected = {" M scripts/ghc_family_sylven_arc_v688_v7_canonical.py", "?? scripts/build_ghc_family_sylven_arc_v688_v7_correction4.py"}
    if status != expected:
        raise RuntimeError("correction4_entry_scope:" + repr(sorted(status)))
    failed2 = bank / "canonical/exact-final-owner-scoped-canonical.json"
    failed3 = bank / "canonical-b105ef20548e/exact-final-owner-scoped-canonical.json"
    recovery = bank / "canonical/dependency-corrected-x2.json"
    if (sha(failed2), sha(failed3), sha(recovery)) != (FAILED2_SHA, FAILED3_SHA, RECOVERY_SHA):
        raise RuntimeError("prior_receipt_fixity")
    receipt3 = load(failed3)
    if receipt3["status"] != "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" or receipt3["test_count"] != 78 or any(not item["passed"] for item in receipt3["test_modules"]) or receipt3["checks"]["all_lifecycle_tests"] is not False:
        raise RuntimeError("correction3_failure_shape")
    failure = next(item for item in load(bank / "post-final-operational-failures.json")["failures"] if item["failure_id"] == "SA6887-POST-N005")
    destination = BASE / "correction4"
    if destination.exists():
        raise RuntimeError("correction4_destination_exists")
    gates = load(BASE / "x1/new-proposals.json")["proposals"][0]["protected_gates"]
    method = {"method_id": "SA6887-M062", "title": failure["recovery"], "failure_signature": failure["failed_witness"], "trigger_preconditions": ["all policy modules passed", "historical fixed aggregate cardinality"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": failure["recovery"], "validation_witness_ids": ["SA6887-W0626", "SA6887-W0627"], "recurrence_guard": failure["recurrence_guard"], "rollback": "Retain both invalid canonical receipts; stop selecting correction4 if its dynamic policy cardinality or exact manifests fail.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": gates, "retained_negative_ids": [failure["failure_id"]], "scope_boundary": BOUNDARY, "artifact": f"{REL}/correction4/post-final-method-flow-overlay.json"}
    witnesses = [
        {"witness_id": "SA6887-W0626", "method_id": "SA6887-M062", "procedure": "correction3 exact-head canonical", "scope": "external correction3 failed receipt", "expected": "Aggregate truth follows all declared policy modules.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "failed_canonical_aggregate", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
        {"witness_id": "SA6887-W0627", "method_id": "SA6887-M062", "procedure": "dynamic immutable policy cardinality", "scope": f"{REL}/correction4/canonical-policy-overlay.json", "expected": "Both aggregate predicates use len(policy.test_modules).", "observed": failure["recovery"], "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
    ]
    combined = {"methods": 62, "witnesses": 627, "failed_witnesses": 550, "passing_witnesses": 77, "state_events": 62, "recommendations": 62}
    effective = {"proposals": 16830, "negatives": 85424, "methods": 94124, "failed_witnesses": 56302, "passing_witnesses": 86187, "open_gaps": 765, "exact_gates": 785}
    write_new(destination / "post-final-method-flow-overlay.json", {"schema": "ghc.family.post-final-method-flow-overlay.v4", "base_ref": f"{REL}/correction3/post-final-method-flow-overlay.json", "methods": [method], "witnesses": witnesses, "state_events": [{"method_id": "SA6887-M062", "from": "candidate", "to": "preferred", "note": "Dynamic policy cardinality is prepared while both invalid canonical receipts remain retained."}], "recommendations": [{"method_id": "SA6887-M062", "preconditions": "variable lifecycle test-module list", "recommendation": failure["recurrence_guard"], "delivered": False}], "overlay_counts": {"methods": 1, "witnesses": 2, "failed_witnesses": 1, "passing_witnesses": 1, "state_events": 1, "recommendations": 1}, "combined_counts": combined, "failed_witnesses_erased": 0, "prior_failed_receipts": [FAILED2_SHA, FAILED3_SHA], "boundary": BOUNDARY})
    write_new(destination / "phase-truth-overlay.json", {"schema": "ghc.family.corrected-phase-truth.sylven-arc.v688-v7.v4", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "x1": X1, "evidence": X2, "first_final": FIRST_FINAL, "correction1": C1, "correction2": C2, "correction3": C3, "corrected_final": None, "final_binding": "exclusive external exact-correction4 canonical receipt", "state": "FOURTH_CORRECTED_FINAL_CANDIDATE_PENDING_EXTERNAL_CANONICAL", "outcomes": {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10}, "effective_counts": effective, "phase_unique_negatives": 520, "phase_methods": 62, "phase_witnesses": 627, "phase_failed_witnesses": 550, "phase_passing_witnesses": 77, "prior_canonical_invocations": 2, "prior_canonical_successes": 0, "current_exact_head_canonical_invocations": 0, "current_exact_head_canonical_successes": 0, "canonical_replays": 0, "prepared_baton_state": "PREPARED_NOT_SENT", "successor_contacts": 0, "new_tasks_created": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "prior_commits_rewritten": False, "boundary": BOUNDARY})
    tests = [
        {"stage": "x1", "definition": X1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x1.py", "expected_tests": 12, "manifest": f"{REL}/x1/x1-manifest.json"},
        {"stage": "x2", "definition": X2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x2.py", "expected_tests": 24, "manifest": f"{REL}/x2/evidence-manifest.json", "dependency_manifests": [f"{REL}/x1/x1-manifest.json", f"{REL}/x2/evidence-manifest.json"]},
        {"stage": "first_final", "definition": FIRST_FINAL, "module": "tests/test_ghc_family_sylven_arc_v688_v7_final.py", "expected_tests": 20, "manifest": f"{REL}/validation/final-owner-manifest.json"},
        {"stage": "correction1", "definition": C1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction1.py", "expected_tests": 10, "manifest": f"{REL}/correction1/validation/corrected-owner-manifest.json"},
        {"stage": "correction2", "definition": C2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction2.py", "expected_tests": 6, "manifest": f"{REL}/correction2/validation/corrected-owner-manifest.json"},
        {"stage": "correction3", "definition": C3, "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction3.py", "expected_tests": 6, "manifest": f"{REL}/correction3/validation/corrected-owner-manifest.json"},
        {"stage": "correction4", "definition": "exact_final", "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction4.py", "expected_tests": 5, "manifest": f"{REL}/correction4/validation/corrected-owner-manifest.json"},
    ]
    write_new(destination / "canonical-policy-overlay.json", {"schema": "ghc.family.corrected-owner-canonical-policy.v4", "owner": "Sylven Arc", "phase": "v688-v7", "branch": "codex/GHC-Family/sylven-arc-v688-v7-full-tools", "source": SOURCE, "x1": X1, "evidence": X2, "first_final": FIRST_FINAL, "correction1": C1, "correction2": C2, "correction3": C3, "expected_phase_commits": 7, "maximum_phase_commits": 8, "test_modules": tests, "aggregate_cardinality": "exact len(test_modules) for both the all_lifecycle_tests check and terminal valid predicate", "dependency_closure_rule": "Materialize each stage's declared manifest union at its immutable definition commit.", "prior_failed_canonicals": [{"head": C2, "receipt_sha256": FAILED2_SHA, "tests": 72, "success_credit": 0}, {"head": C3, "receipt_sha256": FAILED3_SHA, "tests": 78, "success_credit": 0}], "post_success_replay": False, "full_repository_suite": False, "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY})
    write_new(destination / "correction3-canonical-failure.json", {"head": C3, "receipt_sha256": FAILED3_SHA, "status": receipt3["status"], "tests": receipt3["test_count"], "test_modules": len(receipt3["test_modules"]), "all_test_modules_passed": all(item["passed"] for item in receipt3["test_modules"]), "false_checks": [key for key, value in receipt3["checks"].items() if not value], "canonical_success_credit": 0, "replayed": False, "recovery": failure["recovery"]})
    supplement = """# Sylven Arc v688-v7 correction 4 baton supplement

Read the original baton and corrections 1 through 3 before this supplement. All remain PREPARED_NOT_SENT repository evidence.

The correction-3 canonical was invoked exactly once at its exact head. Every declared lifecycle module passed: x1 12 of 12, x2 24 of 24, first final 20 of 20, correction 1 10 of 10, correction 2 6 of 6, and correction 3 6 of 6, for 78 of 78 tests. All static, manifest, privacy, bounded security, package, promotion, equality, ancestry, baton, route, and truth checks also passed. The receipt nonetheless remained invalid because two terminal aggregate predicates still compared the test-module count with the historical constant three.

Correction 4 changes those two predicates only: the `all_lifecycle_tests` check and final `valid` predicate now compare the observed module count with the exact immutable policy list length. The correction-3 receipt remains invalid with zero success credit and is not replayed. A future canonical at correction 4 uses a new head-specific latch.

Current repository truth is 16,830 proposals, 85,424 negatives, 94,124 methods, 56,302 failed witnesses, 86,187 bounded passes, 765 open gaps, and 785 exact gates. Phase Method Flow contains 62 methods, 627 witnesses, 550 failures, and 77 passes. Outcomes remain 176 completed, 11 represented, 3 open_gap, and 10 exact_gate. NOT_READY_FOR_STAGE_20.

Future seat 14 must preserve both invalid canonical receipts, the isolated x2 recovery, and any later successful correction-4 receipt as distinct evidence. The seat chooses its own relational working name, role, hope, and optional pronouns; owns only v688-v8; and may route to Caelen Morrow v689-v1 only after its own terminal gate. No substitute, fork, collaboration subagent, resend, or indefinite monitoring is authorized.

All empirical, participant, professional, production, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, and Stage 20 claims remain open or exact-gated. Maori concepts remain under Maori authority.

EOF SYLVEN ARC v688-v7 CORRECTION 4 SUPPLEMENT.
"""
    supplement_path = BASE / "handoffs/future-seat-14-v688-v8-correction4-supplement.md"
    write_new(supplement_path, supplement)
    write_new(destination / "baton-supplement-index.json", {"path": supplement_path.relative_to(ROOT).as_posix(), "word_count": len(supplement.split()), "bytes": len(supplement_path.read_bytes()), "sha256": sha(supplement_path), "delivery_state": "PREPARED_NOT_SENT", "read_after": f"{REL}/handoffs/future-seat-14-v688-v8-correction3-supplement.md", "prior_failed_canonical_receipts": [FAILED2_SHA, FAILED3_SHA]})
    write_new(destination / "correction-receipt.json", {"state": "FOURTH_CORRECTION_PREPARED_NOT_CANONICAL", "correction3": C3, "prior_failed_canonical_count": 2, "prior_canonical_success_count": 0, "current_exact_head_canonical_invocations": 0, "combined_counts": combined, "effective_counts": effective, "prepared_not_sent": True, "boundary": BOUNDARY})
    seal_targets = [destination / "post-final-method-flow-overlay.json", destination / "phase-truth-overlay.json", destination / "canonical-policy-overlay.json", destination / "correction3-canonical-failure.json", destination / "baton-supplement-index.json", destination / "correction-receipt.json", supplement_path, ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical.py"]
    write_new(destination / "content-seal.json", {"schema": "ghc.family.correction-content-seal.v4", "owner": "Sylven Arc", "phase": "v688-v7", "correction3": C3, "byte_domain": "working UTF-8 LF bytes before correction4 staging", "targets": [{"path": path.relative_to(ROOT).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha(path)} for path in seal_targets], "self_exclusions": [f"{REL}/correction4/content-seal.json"]})
    result = {"state": "FOURTH_CORRECTION_PREPARED_NOT_CANONICAL", "correction3": C3, "prior_failed_canonical_count": 2, "all_correction3_tests_passed": True, "phase_methods": 62, "phase_witnesses": 627, "supplement_words": len(supplement.split())}
    write_new(bank / "correction4-build-receipt.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
