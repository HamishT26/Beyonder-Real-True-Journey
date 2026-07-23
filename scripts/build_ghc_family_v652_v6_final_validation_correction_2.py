#!/usr/bin/env python3
"""Build Tavian Sol v652-v6 final-validation correction two."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import build_ghc_family_v652_v6_final_validation_correction as c1
except ModuleNotFoundError:
    from scripts import build_ghc_family_v652_v6_final_validation_correction as c1


base = c1.base
REPO = c1.REPO
ROOT = c1.ROOT
SOURCE = c1.SOURCE
CORRECTION1 = "6c6e491e5f1163979879865ce820ea718ed94084"
EXPECTED_SCOPED_TESTS = 58
NEW_NEGATIVES = [
    {
        "negative_id": "V6526-FINAL-N05",
        "category": "failed_exact_final_retry",
        "failed": (
            "The corrected exact-head retry completed with 57 of 58 launch-scoped "
            "tests and 27 of 29 detailed checks, so it earned zero canonical credit."
        ),
        "recovery": (
            "Make the inherited closeout test include additive final-validation "
            "negatives and compare the sealed closeout selection to 51 while the "
            "corrected launch selection remains 58."
        ),
        "passing": (
            "The corrected closeout module passed eight of eight, correction-two "
            "tests passed six of six, and all 58 launch tests enumerated without "
            "executing another canonical attempt."
        ),
    },
    {
        "negative_id": "V6526-FINAL-N06",
        "category": "stale_context_minimal_check_patch",
        "failed": (
            "The first minimal-check patch used stale context for the phase-commit "
            "label and did not apply."
        ),
        "recovery": (
            "Read the exact current literal lines, replace four-phase with five-phase, "
            "and add the retained retry check at that bounded location."
        ),
        "passing": (
            "The exact-context patch applied and the correction-two test confirmed "
            "the five-commit contract and retained retry fields."
        ),
    },
]
EFFECTIVE_NEGATIVES = c1.EFFECTIVE_NEGATIVES + len(NEW_NEGATIVES)
CORRECTION_PATHS = {
    f"{base.d.PHASE_ROOT}/final/anchor-ledger.json",
    f"{base.d.PHASE_ROOT}/final/final-phase-truth.json",
    f"{base.d.PHASE_ROOT}/final/final-validation-contract.json",
    f"{base.d.PHASE_ROOT}/final/retained-negative-register.json",
    f"{base.d.PHASE_ROOT}/final/wellbeing-workload-receipt.json",
    f"{base.d.PHASE_ROOT}/method-flow/final-method-flow-ledger.json",
    f"{base.d.PHASE_ROOT}/method-flow/final-method-flow-summary.json",
    f"{base.d.PHASE_ROOT}/method-flow/final-method-flow-summary.md",
    f"{base.d.PHASE_ROOT}/method-flow/final-method-flow-validation.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-29.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-30.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-29-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-29-passing.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-30-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-30-passing.json",
    f"{base.d.PHASE_ROOT}/truth/final-validation-retained-negative.json",
    f"{base.d.PHASE_ROOT}/validation/final-validation-failed-attempt-02.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-patch-failed-attempt-01.json"
    ),
    f"{base.d.PHASE_ROOT}/validation/final-validation-prepared-receipt.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-2-staged-privacy.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-2-staged-review.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-2-staged-manifest.json"
    ),
    f"{base.d.PHASE_ROOT}/validation/final-corrected-owner-manifest-v2.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-2-validation-receipt.json"
    ),
    "scripts/build_ghc_family_v652_v6_final_validation_correction_2.py",
    "scripts/ghc_family_v652_v6_final_validate.py",
    "tests/test_ghc_family_v652_v6_closeout.py",
    "tests/test_ghc_family_v652_v6_final_validation_correction_2.py",
}


def read_at_head(relative: str) -> Any:
    return json.loads(
        base.git("show", f"{CORRECTION1}:{base.d.PHASE_ROOT}/{relative}")
    )


def append_method_flow() -> dict[str, Any]:
    ledger = read_at_head("method-flow/final-method-flow-ledger.json")
    spec = importlib.util.spec_from_file_location(
        "ghc_family_method_flow_state_final_correction_2",
        base.METHOD_RUNNER,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the official Method Flow runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    for number, negative in enumerate(NEW_NEGATIVES, start=29):
        method_id = f"V6526-METHOD-{number:02d}"
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['category']}",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [negative["category"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_final_validation_recovery",
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": (
                "Retain the exact failure and validate only the corrected bounded "
                "surface before another pushed exact-head attempt."
            ),
            "rollback": (
                "Stop, retain the failed witness, and leave route, sibling, and "
                "external authority state unchanged."
            ),
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": base.d.PROTECTED_GATES,
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": (
                "Owner-local correction only; no canonical, full-repository, "
                "independent-reproduction, or route-send credit."
            ),
        }
        failed = {
            "witness_id": f"V6526-WITNESS-{number:02d}-F",
            "method_id": method_id,
            "procedure": "Retain the exact failed attempt.",
            "scope": negative["category"],
            "expected": "The bounded postcondition would pass.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero validation credit; failed witness retained.",
        }
        passing = {
            "witness_id": f"V6526-WITNESS-{number:02d}-P",
            "method_id": method_id,
            "procedure": negative["recovery"],
            "scope": negative["category"],
            "expected": "The isolated recovery establishes only its bounded postcondition.",
            "observed": negative["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": (
                "Same-owner bounded recovery only; canonical retry remains unrun."
            ),
        }
        base.write_json(f"method-flow/requests/method-{number:02d}.json", method)
        base.write_json(
            f"method-flow/requests/witness-{number:02d}-failed.json",
            failed,
        )
        base.write_json(
            f"method-flow/requests/witness-{number:02d}-passing.json",
            passing,
        )
        ledger["methods"].append(method)
        runner.append_event(
            ledger,
            method_id,
            None,
            "candidate",
            "method recorded with retained negative linkage",
        )
        ledger["witnesses"].append(failed)
        method["validation_witness_ids"].append(failed["witness_id"])
        ledger["witnesses"].append(passing)
        method["validation_witness_ids"].append(passing["witness_id"])
        method["recommendation_state"] = "validated"
        runner.append_event(
            ledger,
            method_id,
            "candidate",
            "validated",
            "bounded correction-two witness passed",
            passing["witness_id"],
        )
        method["recommendation_state"] = "preferred"
        runner.append_event(
            ledger,
            method_id,
            "validated",
            "preferred",
            "Promoted only after bounded recovery; failed witness retained.",
        )
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": method_id,
                "preconditions": method["trigger_preconditions"],
                "method": method["candidate_workaround"],
                "witness_ids": method["validation_witness_ids"],
                "recurrence_guard": method["recurrence_guard"],
                "rollback": method["rollback"],
                "scope_boundary": method["scope_boundary"],
            }
        )
    runner.refresh_counts(ledger)
    validation = runner.validate_ledger(ledger)
    if not validation["valid"]:
        raise RuntimeError("; ".join(validation["issues"]))
    summary = {
        "schema": "ghc.family.method-flow-state.summary.v1",
        "phase": ledger["phase"],
        "owner": ledger["owner"],
        "counts": ledger["counts"],
        "preferred_methods": [
            {
                "method_id": row["method_id"],
                "title": row["title"],
                "trigger_preconditions": row["trigger_preconditions"],
                "candidate_workaround": row["candidate_workaround"],
                "validation_witness_ids": row["validation_witness_ids"],
                "recurrence_guard": row["recurrence_guard"],
                "rollback": row["rollback"],
                "scope_boundary": row["scope_boundary"],
            }
            for row in ledger["methods"]
            if row["recommendation_state"] == "preferred"
        ],
        "retained_failed_witnesses": [
            row["witness_id"]
            for row in ledger["witnesses"]
            if row["result"] == "fail"
        ],
        "valid": True,
        "boundary": ledger["boundary"],
    }
    base.write_json("method-flow/final-method-flow-ledger.json", ledger)
    base.write_json("method-flow/final-method-flow-validation.json", validation)
    base.write_json("method-flow/final-method-flow-summary.json", summary)
    base.write_text(
        "method-flow/final-method-flow-summary.md",
        runner.render_markdown(ledger),
    )
    return ledger


def test_source() -> str:
    return '''"""Second correction tests for Tavian Sol v652-v6 final validation."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6FinalValidationCorrection2(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_failed_retry_is_retained(self):
        row = self.load("validation/final-validation-failed-attempt-02.json")
        self.assertEqual(row["tests_run"], 58)
        self.assertEqual(row["tests_passed"], 57)
        self.assertEqual(row["canonical_success_credit"], 0)
        self.assertTrue(row["external_receipt_written"])

    def test_all_negatives_are_additive(self):
        row = self.load("final/retained-negative-register.json")
        self.assertEqual(row["final_validation_operational"], 6)
        self.assertEqual(row["effective_count"], 8916)
        self.assertTrue(row["no_failure_erased"])

    def test_method_flow_contains_thirty_pairs(self):
        flow = self.load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(flow["counts"]["methods"], 30)
        self.assertEqual(flow["counts"]["witness_results"], {"fail":30,"pass":30})
        self.assertEqual(flow["counts"]["states"]["preferred"], 30)

    def test_five_commit_launch_contract(self):
        row = self.load("final/final-validation-contract.json")
        self.assertEqual(row["expected_scoped_tests"], 58)
        self.assertEqual(row["expected_phase_commits"], 5)
        self.assertFalse(row["full_repository_suite_required"])
        self.assertEqual(row["full_repository_suite_owner"], "Eiren Kestrel")

    def test_route_is_still_prepared_only(self):
        row = self.load("route/final-route-state.json")
        self.assertEqual(row["state"], "PREPARED_NOT_SENT")
        self.assertEqual(row["send_count"], 0)
        self.assertEqual(row["contact_count"], 0)

    def test_correction_two_review_and_privacy(self):
        review = self.load("validation/final-validation-correction-2-staged-review.json")
        privacy = self.load("validation/final-validation-correction-2-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()
'''


def build_manifests() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_path = (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-2-staged-manifest.json"
    )
    owner_path = (
        f"{base.d.PHASE_ROOT}/validation/final-corrected-owner-manifest-v2.json"
    )
    receipt_path = (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-2-validation-receipt.json"
    )
    manifest_exclusions = [manifest_path, owner_path, receipt_path]
    owner_exclusions = [owner_path, receipt_path]
    current = set(c1.status_paths())
    unexpected = sorted(current - CORRECTION_PATHS)
    privacy = c1.privacy_scan(sorted(current))
    base.write_json(
        "validation/final-validation-correction-2-staged-privacy.json",
        privacy,
    )
    base.write_json(
        "validation/final-validation-correction-2-staged-review.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-2-staged-review.v1"
            ),
            "correction_1_head": CORRECTION1,
            "head_before_correction_2_commit": base.git("rev-parse", "HEAD"),
            "unexpected_paths": unexpected,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "route_mutated": False,
            "x1_evidence_or_closeout_mutated": False,
            "valid": (
                base.git("rev-parse", "HEAD") == CORRECTION1
                and not unexpected
                and privacy["confirmed_hit_count"] == 0
            ),
        },
    )
    current = set(c1.status_paths())
    correction_paths = sorted(
        path
        for path in current
        if path not in manifest_exclusions
        and (REPO / path).is_file()
        and "__pycache__" not in path
    )
    correction_entries = [c1.hash_entry(path) for path in correction_paths]
    manifest = {
        "schema": (
            "ghc.family.v652-v6.final-validation-correction-2-staged-manifest.v1"
        ),
        "hash_domain": "git_path_filtered_blob",
        "correction_1_head": CORRECTION1,
        "entry_count": len(correction_entries),
        "entries": correction_entries,
        "self_exclusions": manifest_exclusions,
        "coverage_boundary": (
            "All intended second-correction paths except this manifest, the final "
            "cumulative owner manifest, and the count-bearing validation receipt."
        ),
    }
    base.write_json(
        "validation/final-validation-correction-2-staged-manifest.json",
        manifest,
    )
    committed = set(
        filter(
            None,
            base.git("diff", "--name-only", SOURCE, "HEAD").splitlines(),
        )
    )
    current = set(c1.status_paths())
    owner_paths = sorted(
        path
        for path in committed | current
        if path not in owner_exclusions
        and (REPO / path).is_file()
        and "__pycache__" not in path
    )
    owner_entries = [c1.hash_entry(path) for path in owner_paths]
    owner = {
        "schema": "ghc.family.v652-v6.final-corrected-owner-manifest-v2.v1",
        "hash_domain": "git_path_filtered_blob",
        "source_head": SOURCE,
        "correction_1_head": CORRECTION1,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "self_exclusions": owner_exclusions,
        "coverage_boundary": (
            "All Tavian source-to-second-corrected-final paths except this manifest "
            "and the count-bearing second-correction receipt."
        ),
    }
    base.write_json("validation/final-corrected-owner-manifest-v2.json", owner)
    return manifest, owner


def build() -> None:
    if base.git("rev-parse", "HEAD") != CORRECTION1:
        raise RuntimeError("correction-two builder must begin at correction-one head")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    flow = append_method_flow()

    negatives = read_at_head("final/retained-negative-register.json")
    negatives["final_validation_operational"] = 6
    negatives["final_validation_rows"].extend(
        {**row, "canonical_success_credit": 0}
        for row in NEW_NEGATIVES
    )
    negatives["effective_count"] = EFFECTIVE_NEGATIVES
    base.write_json("final/retained-negative-register.json", negatives)

    truth = read_at_head("final/final-phase-truth.json")
    truth["effective_negatives"] = EFFECTIVE_NEGATIVES
    base.write_json("final/final-phase-truth.json", truth)

    anchor = read_at_head("final/anchor-ledger.json")
    anchor["correction_1"] = CORRECTION1
    anchor["final"] = "resolve_as_containing_second_correction_commit_after_creation"
    anchor["four_phase_commits_required"] = False
    anchor["five_phase_commits_required"] = True
    anchor["retained_failed_exact_final_attempts"] = 2
    base.write_json("final/anchor-ledger.json", anchor)

    wellbeing = read_at_head("final/wellbeing-workload-receipt.json")
    wellbeing["planned_phase_commits"] = 5
    wellbeing["retained_failed_exact_final_attempts"] = 2
    wellbeing["successful_canonical_passes_before_retry"] = 0
    base.write_json("final/wellbeing-workload-receipt.json", wellbeing)

    contract = read_at_head("final/final-validation-contract.json")
    contract["expected_phase_commits"] = 5
    contract["retained_failed_exact_final_attempts"] = 2
    contract["retained_patch_failures"] = 1
    contract["successful_canonical_passes_before_retry"] = 0
    contract["retry_authorized_after_zero_success"] = True
    contract["checks"] = [
        "launch-scoped tests",
        "complete phase JSON",
        "five-class privacy scan",
        "eight manifest contracts",
        "stale labels",
        "document contracts",
        "source/x1/evidence/closeout/correction-1 ancestry",
        "five phase commits",
        "zero merges",
        "one final parent",
        "two retained zero-credit failed exact-final attempts",
        "exact head",
        "clean before and after",
        "four-way live equality",
    ]
    base.write_json("final/final-validation-contract.json", contract)

    retained = read_at_head("truth/final-validation-retained-negative.json")
    retained["negative_ids"].extend(
        row["negative_id"] for row in NEW_NEGATIVES
    )
    retained["final_validation_operational"] = 6
    retained["effective_final"] = EFFECTIVE_NEGATIVES
    retained["failed_exact_final_attempts"] = 2
    retained["failed_patch_attempts"] = 1
    retained["external_receipts_written"] = 1
    retained["no_failure_erased"] = True
    base.write_json("truth/final-validation-retained-negative.json", retained)

    external_path = (
        REPO.parents[1]
        / "validation"
        / f"tavian-v652-v6-{CORRECTION1}.json"
    )
    external_raw = external_path.read_bytes()
    external = json.loads(external_raw.decode("utf-8"))
    if (
        external["valid"]
        or external["exact_head"] != CORRECTION1
        or external["launch_scoped_tests"]["total"] != 58
        or external["launch_scoped_tests"]["passed"] != 57
        or external["passed"] != 27
        or external["total"] != 29
        or external["full_repository_suite_run"]
    ):
        raise RuntimeError("unexpected failed retry receipt")
    base.write_json(
        "validation/final-validation-failed-attempt-02.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-failed-attempt.v2",
            "recorded_at_utc": now,
            "attempted_head": CORRECTION1,
            "tests_run": 58,
            "tests_passed": 57,
            "detailed_passed": 27,
            "detailed_total": 29,
            "minimal_passed": 19,
            "minimal_total": 20,
            "json_parse_count": 272,
            "privacy_confirmed_hits": 0,
            "manifest_entry_total": 957,
            "failed_checks": [
                "launch_scoped_tests",
                "closeout_receipts",
            ],
            "failed_test_ids": [
                (
                    "test_negatives_and_gates "
                    "(TestTavianV652V6Closeout)"
                )
            ],
            "external_receipt_name": external_path.name,
            "external_receipt_sha256": hashlib.sha256(external_raw).hexdigest(),
            "external_receipt_written": True,
            "full_repository_suite_run": False,
            "canonical_success_credit": 0,
            "successful_canonical_passes": 0,
            "retained_negative_id": "V6526-FINAL-N05",
            "boundary": (
                "Failed launch-scoped retry with zero canonical credit; Eiren's "
                "full-repository suite was not rerun and route remained unsent."
            ),
        },
    )
    base.write_json(
        "validation/final-validation-patch-failed-attempt-01.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-patch-failure.v1",
            "failure_stage": "minimal_check_set_patch",
            "failure": "stale patch context did not apply",
            "recovery": "exact literal-line replacement applied",
            "canonical_success_credit": 0,
            "retained_negative_id": "V6526-FINAL-N06",
        },
    )
    base.write_json(
        "validation/final-validation-prepared-receipt.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-prepared.v3",
            "state": "second_retry_prepared_after_two_failed_attempts",
            "failed_exact_final_attempt_count": 2,
            "failed_correction_or_probe_count": 4,
            "successful_pass_count": 0,
            "replay_count": 0,
            "completed_retry_count": 1,
            "next_retry_authorized": True,
            "external_receipt_required": True,
            "reason": (
                "Both prior exact-head attempts earned zero success credit. One next "
                "attempt is prepared only after this additive correction is pushed, "
                "clean, and four-way equal."
            ),
        },
    )

    base.write_repo(
        "tests/test_ghc_family_v652_v6_final_validation_correction_2.py",
        test_source(),
    )
    manifest, owner = build_manifests()

    correction_test_output = base.run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v6_final_validation_correction_2",
    )
    closeout_test_output = base.run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v6_closeout",
    )
    spec = importlib.util.spec_from_file_location(
        "tavian_final_validator_preflight_2",
        REPO / "scripts/ghc_family_v652_v6_final_validate.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load corrected final validator")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    _suite, selection = validator.selected_tests()
    if (
        selection["eligible_count"] != EXPECTED_SCOPED_TESTS
        or selection["loader_errors"]
    ):
        raise RuntimeError(f"corrected selection invalid: {selection}")

    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        base.read_json(path)
    review = base.read_json(
        ROOT / "validation/final-validation-correction-2-staged-review.json"
    )
    privacy = base.read_json(
        ROOT / "validation/final-validation-correction-2-staged-privacy.json"
    )
    valid = (
        review["valid"]
        and privacy["confirmed_hit_count"] == 0
        and flow["counts"]["methods"] == 30
        and selection["eligible_count"] == EXPECTED_SCOPED_TESTS
    )
    base.write_json(
        "validation/final-validation-correction-2-validation-receipt.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-2-validation.v1"
            ),
            "built_at_utc": now,
            "correction_2_tests_passed": 6,
            "correction_2_tests_total": 6,
            "corrected_closeout_tests_passed": 8,
            "corrected_closeout_tests_total": 8,
            "selection_enumerated": selection["eligible_count"],
            "selection_loader_errors": selection["loader_errors"],
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "correction_manifest_entries": manifest["entry_count"],
            "corrected_owner_manifest_entries": owner["entry_count"],
            "correction_test_stdout": correction_test_output,
            "closeout_test_stdout": closeout_test_output,
            "full_repository_suite_rerun": False,
            "canonical_retry_run": False,
            "valid": valid,
            "boundary": (
                "Precommit second-correction validation only; canonical credit "
                "remains reserved for the pushed exact head."
            ),
        },
    )
    if not valid:
        raise RuntimeError("second correction preflight invalid")
    print(
        json.dumps(
            {
                "effective_negatives": EFFECTIVE_NEGATIVES,
                "method_flow": flow["counts"],
                "correction_2_tests": "6/6",
                "corrected_closeout_tests": "8/8",
                "selection_enumerated": selection["eligible_count"],
                "correction_manifest_entries": manifest["entry_count"],
                "corrected_owner_manifest_entries": owner["entry_count"],
                "canonical_retry_run": False,
                "status": "second_correction_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
