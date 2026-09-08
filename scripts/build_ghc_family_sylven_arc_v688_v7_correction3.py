#!/usr/bin/env python3
"""Prepare the dependency-closed canonical correction after one invalid aggregate."""
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
CORRECTION1 = "c0f79218f2d644592bd4eee0947058f0f3803b50"
CORRECTION2 = "1b00ec2df09e02ef63b370d6c8b15180044b3a38"
FAILED_RECEIPT_SHA = "526b15d930704f592486754db0547a594f0590329728cb7084de89a797eb2014"
RECOVERY_RECEIPT_SHA = "56646c01100763254f584d667be5324d00fbab74530d00666a26c517ad4002fb"
BOUNDARY = "Same-owner dependency-corrected software evidence only; the prior canonical remains invalid with zero success credit. No empirical, participant, professional, production, legal, cultural, Maori-authority, independent-reproduction, consciousness, Theory-of-Everything, proof, canon, or Stage 20 evidence."


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
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != CORRECTION2:
        raise RuntimeError("exact_correction2_required")
    if subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).strip():
        raise RuntimeError("unexpected_staged_entry")
    status = set(line for line in subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).splitlines() if line)
    expected = {
        " M scripts/ghc_family_sylven_arc_v688_v7_canonical.py",
        "?? scripts/build_ghc_family_sylven_arc_v688_v7_correction3.py",
        "?? scripts/ghc_family_sylven_arc_v688_v7_canonical_x2_recovery.py",
    }
    if status != expected:
        raise RuntimeError("correction3_entry_scope:" + repr(sorted(status)))
    failed_receipt = bank / "canonical/exact-final-owner-scoped-canonical.json"
    recovery_receipt = bank / "canonical/dependency-corrected-x2.json"
    if sha(failed_receipt) != FAILED_RECEIPT_SHA or sha(recovery_receipt) != RECOVERY_RECEIPT_SHA:
        raise RuntimeError("external_receipt_fixity")
    failed = load(failed_receipt)
    recovery = load(recovery_receipt)
    if failed["status"] != "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" or failed["canonical_success_count"] != 0 or recovery["state"] != "VALID_ISOLATED_X2_DEPENDENCY_RECOVERY" or recovery["aggregate_replayed"]:
        raise RuntimeError("failed_canonical_or_recovery_state")
    failure = next(item for item in load(bank / "post-final-operational-failures.json")["failures"] if item["failure_id"] == "SA6887-POST-N004")
    destination = BASE / "correction3"
    if destination.exists():
        raise RuntimeError("correction3_destination_exists")
    gates = load(BASE / "x1/new-proposals.json")["proposals"][0]["protected_gates"]
    method = {"method_id": "SA6887-M061", "title": failure["recovery"], "failure_signature": failure["failed_witness"], "trigger_preconditions": ["one invalid canonical at correction2", "one isolated x2 dependency recovery"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": failure["recovery"], "validation_witness_ids": ["SA6887-W0624", "SA6887-W0625"], "recurrence_guard": failure["recurrence_guard"], "rollback": "Retain the invalid canonical and isolated recovery; stop selecting correction3 if dependency-closed manifests or its new exact-head canonical fail.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": gates, "retained_negative_ids": [failure["failure_id"]], "scope_boundary": BOUNDARY, "artifact": f"{REL}/correction3/post-final-method-flow-overlay.json"}
    witnesses = [
        {"witness_id": "SA6887-W0624", "method_id": "SA6887-M061", "procedure": "one exact-head canonical aggregate at correction2", "scope": "external failed canonical receipt", "expected": "Every lifecycle test view is dependency closed.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "failed_canonical_aggregate", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
        {"witness_id": "SA6887-W0625", "method_id": "SA6887-M061", "procedure": "isolated x2 dependency materialization and module rerun", "scope": "external dependency-corrected x2 receipt", "expected": "Add exact immutable x1 dependencies and rerun only x2.", "observed": "34 x1 dependency paths added; 24 of 24 x2 tests passed; zero successful modules or aggregate replayed.", "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
    ]
    combined = {"methods": 61, "witnesses": 625, "failed_witnesses": 549, "passing_witnesses": 76, "state_events": 61, "recommendations": 61}
    effective = {"proposals": 16830, "negatives": 85423, "methods": 94123, "failed_witnesses": 56301, "passing_witnesses": 86186, "open_gaps": 765, "exact_gates": 785}
    write_new(destination / "post-final-method-flow-overlay.json", {"schema": "ghc.family.post-final-method-flow-overlay.v3", "base_ref": f"{REL}/correction2/post-final-method-flow-overlay.json", "methods": [method], "witnesses": witnesses, "state_events": [{"method_id": "SA6887-M061", "from": "candidate", "to": "preferred", "note": "Dependency-closed policy is prepared while the invalid canonical remains zero-credit."}], "recommendations": [{"method_id": "SA6887-M061", "preconditions": "lifecycle test with prior-stage dependencies", "recommendation": failure["recurrence_guard"], "delivered": False}], "overlay_counts": {"methods": 1, "witnesses": 2, "failed_witnesses": 1, "passing_witnesses": 1, "state_events": 1, "recommendations": 1}, "combined_counts": combined, "failed_witnesses_erased": 0, "prior_failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA, "isolated_recovery_receipt_sha256": RECOVERY_RECEIPT_SHA, "boundary": BOUNDARY})
    write_new(destination / "phase-truth-overlay.json", {"schema": "ghc.family.corrected-phase-truth.sylven-arc.v688-v7.v3", "owner": "Sylven Arc", "phase": "v688-v7", "source": SOURCE, "x1": X1, "evidence": X2, "first_final": FIRST_FINAL, "correction1": CORRECTION1, "correction2": CORRECTION2, "corrected_final": None, "final_binding": "exclusive external exact-correction3 canonical receipt", "state": "THIRD_CORRECTED_FINAL_CANDIDATE_PENDING_EXTERNAL_CANONICAL", "outcomes": {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10}, "effective_counts": effective, "phase_unique_negatives": 519, "phase_methods": 61, "phase_witnesses": 625, "phase_failed_witnesses": 549, "phase_passing_witnesses": 76, "prior_canonical_invocations": 1, "prior_canonical_successes": 0, "current_exact_head_canonical_invocations": 0, "current_exact_head_canonical_successes": 0, "canonical_replays": 0, "prepared_baton_state": "PREPARED_NOT_SENT", "successor_contacts": 0, "new_tasks_created": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "prior_commits_rewritten": False, "boundary": BOUNDARY})
    tests = [
        {"stage": "x1", "definition": X1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x1.py", "expected_tests": 12, "manifest": f"{REL}/x1/x1-manifest.json"},
        {"stage": "x2", "definition": X2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x2.py", "expected_tests": 24, "manifest": f"{REL}/x2/evidence-manifest.json", "dependency_manifests": [f"{REL}/x1/x1-manifest.json", f"{REL}/x2/evidence-manifest.json"]},
        {"stage": "first_final", "definition": FIRST_FINAL, "module": "tests/test_ghc_family_sylven_arc_v688_v7_final.py", "expected_tests": 20, "manifest": f"{REL}/validation/final-owner-manifest.json"},
        {"stage": "correction1", "definition": CORRECTION1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction1.py", "expected_tests": 10, "manifest": f"{REL}/correction1/validation/corrected-owner-manifest.json"},
        {"stage": "correction2", "definition": CORRECTION2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction2.py", "expected_tests": 6, "manifest": f"{REL}/correction2/validation/corrected-owner-manifest.json"},
        {"stage": "correction3", "definition": "exact_final", "module": "tests/test_ghc_family_sylven_arc_v688_v7_correction3.py", "expected_tests": 6, "manifest": f"{REL}/correction3/validation/corrected-owner-manifest.json"},
    ]
    write_new(destination / "canonical-policy-overlay.json", {"schema": "ghc.family.corrected-owner-canonical-policy.v3", "owner": "Sylven Arc", "phase": "v688-v7", "branch": "codex/GHC-Family/sylven-arc-v688-v7-full-tools", "source": SOURCE, "x1": X1, "evidence": X2, "first_final": FIRST_FINAL, "correction1": CORRECTION1, "correction2": CORRECTION2, "expected_phase_commits": 6, "maximum_phase_commits": 8, "test_modules": tests, "dependency_closure_rule": "Materialize the ordered union of each test stage's declared dependency manifests at that exact definition commit.", "prior_failed_canonical": {"head": CORRECTION2, "receipt_sha256": FAILED_RECEIPT_SHA, "success_credit": 0, "replayed": False}, "isolated_recovery": {"receipt_sha256": RECOVERY_RECEIPT_SHA, "x2_tests": 24, "passed": 24, "aggregate_replayed": False}, "post_success_replay": False, "full_repository_suite": False, "same_owner_only": True, "independent_reproduction": False, "boundary": BOUNDARY})
    write_new(destination / "failed-canonical-and-isolated-recovery.json", {"failed_canonical": {"head": CORRECTION2, "receipt_sha256": FAILED_RECEIPT_SHA, "status": failed["status"], "checks_passed": failed["passed_check_count"], "checks_total": failed["check_count"], "test_modules_passed": 4, "test_modules_total": 5, "tests_observed": failed["test_count"], "canonical_success_credit": 0, "replayed": False}, "isolated_recovery": {"receipt_sha256": RECOVERY_RECEIPT_SHA, "state": recovery["state"], "dependencies_added": recovery["x1_dependencies_added"], "tests": recovery["test_count"], "passed": recovery["passed"], "successful_modules_replayed": recovery["successful_canonical_components_replayed"], "aggregate_replayed": recovery["aggregate_replayed"]}, "future_exact_head_invocations": 0, "erased": 0})
    supplement = """# Sylven Arc v688-v7 correction 3 baton supplement

Read the original thirteen-module baton, correction 1, correction 2, and then this supplement. All are immutable repository evidence. None is a live task action, and delivery remains PREPARED_NOT_SENT.

One canonical aggregate was invoked at correction 2. It is permanently invalid and receives zero canonical-success credit. X1 passed 12 of 12, the first-final module passed 20 of 20, correction 1 passed 10 of 10, and correction 2 passed 6 of 6. The x2 module enumerated all 24 tests but returned four file-not-found errors because its external definition view contained the x2 evidence delta and omitted immutable x1 proposal and package-plan dependencies.

Only the failed dependency was recovered. Thirty-four exact paths from the immutable x1 manifest were added to the existing external x2 definition view. The x2 module alone was rerun and passed 24 of 24. No successful lifecycle module and no aggregate was replayed. The failed canonical receipt and focused recovery receipt remain external, hash-bound, and distinct.

Correction 3 makes the future exact-head canonical dependency closed. The x2 policy explicitly names both the x1 and x2 manifests; materialization takes their ordered de-duplicated union at the immutable x2 commit. Other stages use complete owner manifests for their own definition commits. A new exact-head latch is distinct from the prior failed head and may be invoked once only after a successful fresh preflight.

Repository truth now records 16,830 proposals, 85,423 negatives, 94,123 methods, 56,301 failed witnesses, 86,186 bounded passing witnesses, 765 open gaps, and 785 exact gates. Phase Method Flow contains 61 methods and 625 witnesses: 549 retained failures and 76 bounded passes. Outcomes remain 176 completed, 11 represented, 3 open_gap, and 10 exact_gate. NOT_READY_FOR_STAGE_20.

Future seat 14 must preserve the invalid canonical, focused recovery, and any later successful exact-head receipt as separate evidence. It chooses its own relational working name, role, hope, and optional pronouns, owns only v688-v8, and later contacts Caelen Morrow for v689-v1 only after its own exact terminal gate. No substitute, fork, collaboration subagent, second send, or indefinite monitoring is authorized.

No software, symbolic, citation, package, task, canonical, or composite result establishes empirical confirmation, participant evidence, professional or production status, legal or cultural ratification, Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything proof, proof, canon, or Stage 20. Maori concepts remain under Maori authority.

EOF SYLVEN ARC v688-v7 CORRECTION 3 SUPPLEMENT.
"""
    supplement_path = BASE / "handoffs/future-seat-14-v688-v8-correction3-supplement.md"
    write_new(supplement_path, supplement)
    write_new(destination / "baton-supplement-index.json", {"path": supplement_path.relative_to(ROOT).as_posix(), "word_count": len(supplement.split()), "bytes": len(supplement_path.read_bytes()), "sha256": sha(supplement_path), "delivery_state": "PREPARED_NOT_SENT", "read_after": f"{REL}/handoffs/future-seat-14-v688-v8-correction2-supplement.md", "prior_failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA, "isolated_recovery_receipt_sha256": RECOVERY_RECEIPT_SHA})
    write_new(destination / "correction-receipt.json", {"state": "THIRD_CORRECTION_PREPARED_NOT_CANONICAL", "correction2": CORRECTION2, "prior_failed_canonical_success_credit": 0, "isolated_x2_recovery_passed": True, "current_exact_head_canonical_invocations": 0, "combined_counts": combined, "effective_counts": effective, "prepared_not_sent": True, "boundary": BOUNDARY})
    seal_targets = [destination / "post-final-method-flow-overlay.json", destination / "phase-truth-overlay.json", destination / "canonical-policy-overlay.json", destination / "failed-canonical-and-isolated-recovery.json", destination / "baton-supplement-index.json", destination / "correction-receipt.json", supplement_path, ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical.py", ROOT / "scripts/ghc_family_sylven_arc_v688_v7_canonical_x2_recovery.py"]
    write_new(destination / "content-seal.json", {"schema": "ghc.family.correction-content-seal.v3", "owner": "Sylven Arc", "phase": "v688-v7", "correction2": CORRECTION2, "byte_domain": "working UTF-8 LF bytes before correction3 staging", "targets": [{"path": path.relative_to(ROOT).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha(path)} for path in seal_targets], "self_exclusions": [f"{REL}/correction3/content-seal.json"]})
    result = {"state": "THIRD_CORRECTION_PREPARED_NOT_CANONICAL", "correction2": CORRECTION2, "prior_failed_canonical": True, "isolated_x2_recovery_passed": True, "phase_methods": 61, "phase_witnesses": 625, "supplement_words": len(supplement.split())}
    write_new(bank / "correction3-build-receipt.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
