#!/usr/bin/env python3
"""Build Tavian Sol v652-v6 final-validation correction three."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from typing import Any

try:
    import build_ghc_family_v652_v6_final_validation_correction_2 as c2
except ModuleNotFoundError:
    from scripts import build_ghc_family_v652_v6_final_validation_correction_2 as c2


c1 = c2.c1
base = c2.base
REPO = c2.REPO
ROOT = c2.ROOT
SOURCE = c2.SOURCE
CORRECTION2 = "276839c87de60f44843df3f01fb1af7b411aa664"
EXPECTED_SCOPED_TESTS = 58
NEGATIVE = {
    "negative_id": "V6526-FINAL-N07",
    "category": "failed_exact_final_retry_2",
    "failed": (
        "The second corrected exact-head retry completed with 56 of 58 launch-scoped "
        "tests and 29 of 30 detailed checks, so it earned zero canonical credit."
    ),
    "recovery": (
        "Make the first correction test assert additive lower bounds and component "
        "parity instead of freezing intermediate negative and Method Flow totals."
    ),
    "passing": (
        "The corrected first-correction module passed seven of seven, correction-three "
        "tests passed five of five, and all 58 launch tests enumerated without another "
        "canonical invocation."
    ),
}
EFFECTIVE_NEGATIVES = c2.EFFECTIVE_NEGATIVES + 1
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
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-31.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-31-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-31-passing.json",
    f"{base.d.PHASE_ROOT}/truth/final-validation-retained-negative.json",
    f"{base.d.PHASE_ROOT}/validation/final-validation-failed-attempt-03.json",
    f"{base.d.PHASE_ROOT}/validation/final-validation-prepared-receipt.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-3-staged-privacy.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-3-staged-review.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-3-staged-manifest.json"
    ),
    f"{base.d.PHASE_ROOT}/validation/final-corrected-owner-manifest-v3.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-3-validation-receipt.json"
    ),
    "scripts/build_ghc_family_v652_v6_final_validation_correction_3.py",
    "scripts/ghc_family_v652_v6_final_validate.py",
    "tests/test_ghc_family_v652_v6_final_validation_correction.py",
    "tests/test_ghc_family_v652_v6_final_validation_correction_3.py",
}


def read_at_head(relative: str) -> Any:
    return json.loads(
        base.git("show", f"{CORRECTION2}:{base.d.PHASE_ROOT}/{relative}")
    )


def append_method_flow() -> dict[str, Any]:
    ledger = read_at_head("method-flow/final-method-flow-ledger.json")
    spec = importlib.util.spec_from_file_location(
        "ghc_family_method_flow_state_final_correction_3",
        base.METHOD_RUNNER,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the official Method Flow runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    method_id = "V6526-METHOD-31"
    method = {
        "method_id": method_id,
        "title": "Keep correction tests additive across later retained failures",
        "failure_signature": NEGATIVE["failed"],
        "trigger_preconditions": [NEGATIVE["category"]],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_local_final_validation_recovery",
        "candidate_workaround": NEGATIVE["recovery"],
        "validation_witness_ids": [],
        "recurrence_guard": (
            "Correction tests may freeze their own minimum baseline but must derive "
            "cumulative totals from the current retained registers."
        ),
        "rollback": (
            "Stop, retain the failed retry, and leave route, sibling, and external "
            "authority state unchanged."
        ),
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": base.d.PROTECTED_GATES,
        "retained_negative_ids": [NEGATIVE["negative_id"]],
        "scope_boundary": (
            "Owner-local test correction only; no canonical, full-repository, "
            "independent-reproduction, or route-send credit."
        ),
    }
    failed = {
        "witness_id": "V6526-WITNESS-31-F",
        "method_id": method_id,
        "procedure": "Retain the complete failed exact-head retry receipt.",
        "scope": NEGATIVE["category"],
        "expected": "All 58 launch-scoped tests and all detailed checks pass.",
        "observed": NEGATIVE["failed"],
        "result": "fail",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [NEGATIVE["negative_id"]],
        "boundary": "Zero canonical credit; external failed receipt retained.",
    }
    passing = {
        "witness_id": "V6526-WITNESS-31-P",
        "method_id": method_id,
        "procedure": NEGATIVE["recovery"],
        "scope": "additive_correction_test_contract",
        "expected": "The corrected targeted modules pass without a canonical invocation.",
        "observed": NEGATIVE["passing"],
        "result": "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [NEGATIVE["negative_id"]],
        "boundary": (
            "Same-owner bounded recovery only; canonical credit remains unclaimed."
        ),
    }
    base.write_json("method-flow/requests/method-31.json", method)
    base.write_json("method-flow/requests/witness-31-failed.json", failed)
    base.write_json("method-flow/requests/witness-31-passing.json", passing)
    ledger["methods"].append(method)
    runner.append_event(
        ledger,
        method_id,
        None,
        "candidate",
        "method recorded with retained failed-retry linkage",
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
        "bounded additive-test witness passed",
        passing["witness_id"],
    )
    method["recommendation_state"] = "preferred"
    runner.append_event(
        ledger,
        method_id,
        "validated",
        "preferred",
        "Promoted only after bounded recovery; failed retry retained.",
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
    return '''"""Third correction tests for Tavian Sol v652-v6 final validation."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6FinalValidationCorrection3(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_failed_retry_two_is_retained(self):
        row = self.load("validation/final-validation-failed-attempt-03.json")
        self.assertEqual(row["tests_run"], 58)
        self.assertEqual(row["tests_passed"], 56)
        self.assertEqual(row["canonical_success_credit"], 0)
        self.assertTrue(row["external_receipt_written"])

    def test_final_counts_are_additive(self):
        row = self.load("final/retained-negative-register.json")
        self.assertEqual(row["final_validation_operational"], 7)
        self.assertEqual(row["effective_count"], 8917)

    def test_method_flow_has_thirty_one_pairs(self):
        flow = self.load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(flow["counts"]["methods"], 31)
        self.assertEqual(flow["counts"]["witness_results"], {"fail":31,"pass":31})
        self.assertEqual(flow["counts"]["states"]["preferred"], 31)

    def test_six_commit_launch_contract_and_route(self):
        contract = self.load("final/final-validation-contract.json")
        route = self.load("route/final-route-state.json")
        self.assertEqual(contract["expected_phase_commits"], 6)
        self.assertEqual(contract["expected_scoped_tests"], 58)
        self.assertFalse(contract["full_repository_suite_required"])
        self.assertEqual(route["state"], "PREPARED_NOT_SENT")
        self.assertEqual(route["send_count"], 0)
        self.assertEqual(route["contact_count"], 0)

    def test_correction_three_review_and_privacy(self):
        review = self.load("validation/final-validation-correction-3-staged-review.json")
        privacy = self.load("validation/final-validation-correction-3-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()
'''


def build_manifests() -> tuple[dict[str, Any], dict[str, Any]]:
    manifest_path = (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-3-staged-manifest.json"
    )
    owner_path = (
        f"{base.d.PHASE_ROOT}/validation/final-corrected-owner-manifest-v3.json"
    )
    receipt_path = (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-3-validation-receipt.json"
    )
    manifest_exclusions = [manifest_path, owner_path, receipt_path]
    owner_exclusions = [owner_path, receipt_path]
    current = set(c1.status_paths())
    unexpected = sorted(current - CORRECTION_PATHS)
    privacy = c1.privacy_scan(sorted(current))
    base.write_json(
        "validation/final-validation-correction-3-staged-privacy.json",
        privacy,
    )
    base.write_json(
        "validation/final-validation-correction-3-staged-review.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-3-staged-review.v1"
            ),
            "correction_2_head": CORRECTION2,
            "head_before_correction_3_commit": base.git("rev-parse", "HEAD"),
            "unexpected_paths": unexpected,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "route_mutated": False,
            "x1_evidence_closeout_or_prior_correction_mutated": False,
            "valid": (
                base.git("rev-parse", "HEAD") == CORRECTION2
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
            "ghc.family.v652-v6.final-validation-correction-3-staged-manifest.v1"
        ),
        "hash_domain": "git_path_filtered_blob",
        "correction_2_head": CORRECTION2,
        "entry_count": len(correction_entries),
        "entries": correction_entries,
        "self_exclusions": manifest_exclusions,
        "coverage_boundary": (
            "All intended third-correction paths except this manifest, the final "
            "cumulative owner manifest, and the count-bearing validation receipt."
        ),
    }
    base.write_json(
        "validation/final-validation-correction-3-staged-manifest.json",
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
        "schema": "ghc.family.v652-v6.final-corrected-owner-manifest-v3.v1",
        "hash_domain": "git_path_filtered_blob",
        "source_head": SOURCE,
        "correction_2_head": CORRECTION2,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "self_exclusions": owner_exclusions,
        "coverage_boundary": (
            "All Tavian source-to-third-corrected-final paths except this manifest "
            "and the count-bearing third-correction receipt."
        ),
    }
    base.write_json("validation/final-corrected-owner-manifest-v3.json", owner)
    return manifest, owner


def build() -> None:
    if base.git("rev-parse", "HEAD") != CORRECTION2:
        raise RuntimeError("correction-three builder must begin at correction-two head")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    flow = append_method_flow()

    negatives = read_at_head("final/retained-negative-register.json")
    negatives["final_validation_operational"] = 7
    negatives["final_validation_rows"].append(
        {**NEGATIVE, "canonical_success_credit": 0}
    )
    negatives["effective_count"] = EFFECTIVE_NEGATIVES
    base.write_json("final/retained-negative-register.json", negatives)

    truth = read_at_head("final/final-phase-truth.json")
    truth["effective_negatives"] = EFFECTIVE_NEGATIVES
    base.write_json("final/final-phase-truth.json", truth)

    anchor = read_at_head("final/anchor-ledger.json")
    anchor["correction_2"] = CORRECTION2
    anchor["final"] = "resolve_as_containing_third_correction_commit_after_creation"
    anchor["five_phase_commits_required"] = False
    anchor["six_phase_commits_required"] = True
    anchor["retained_failed_exact_final_attempts"] = 3
    base.write_json("final/anchor-ledger.json", anchor)

    wellbeing = read_at_head("final/wellbeing-workload-receipt.json")
    wellbeing["planned_phase_commits"] = 6
    wellbeing["retained_failed_exact_final_attempts"] = 3
    wellbeing["successful_canonical_passes_before_retry"] = 0
    base.write_json("final/wellbeing-workload-receipt.json", wellbeing)

    contract = read_at_head("final/final-validation-contract.json")
    contract["expected_phase_commits"] = 6
    contract["retained_failed_exact_final_attempts"] = 3
    contract["successful_canonical_passes_before_retry"] = 0
    contract["retry_authorized_after_zero_success"] = True
    contract["checks"] = [
        "launch-scoped tests",
        "complete phase JSON",
        "five-class privacy scan",
        "ten manifest contracts",
        "stale labels",
        "document contracts",
        "source/x1/evidence/closeout/correction-1/correction-2 ancestry",
        "six phase commits",
        "zero merges",
        "one final parent",
        "three retained zero-credit failed exact-final attempts",
        "exact head",
        "clean before and after",
        "four-way live equality",
    ]
    base.write_json("final/final-validation-contract.json", contract)

    retained = read_at_head("truth/final-validation-retained-negative.json")
    retained["negative_ids"].append(NEGATIVE["negative_id"])
    retained["final_validation_operational"] = 7
    retained["effective_final"] = EFFECTIVE_NEGATIVES
    retained["failed_exact_final_attempts"] = 3
    retained["external_receipts_written"] = 2
    retained["no_failure_erased"] = True
    base.write_json("truth/final-validation-retained-negative.json", retained)

    external_path = (
        REPO.parents[1]
        / "validation"
        / f"tavian-v652-v6-{CORRECTION2}.json"
    )
    external_raw = external_path.read_bytes()
    external = json.loads(external_raw.decode("utf-8"))
    if (
        external["valid"]
        or external["exact_head"] != CORRECTION2
        or external["launch_scoped_tests"]["total"] != 58
        or external["launch_scoped_tests"]["passed"] != 56
        or external["passed"] != 29
        or external["total"] != 30
        or external["full_repository_suite_run"]
    ):
        raise RuntimeError("unexpected failed second-retry receipt")
    base.write_json(
        "validation/final-validation-failed-attempt-03.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-failed-attempt.v3",
            "recorded_at_utc": now,
            "attempted_head": CORRECTION2,
            "tests_run": 58,
            "tests_passed": 56,
            "detailed_passed": 29,
            "detailed_total": 30,
            "minimal_passed": 20,
            "minimal_total": 21,
            "json_parse_count": 285,
            "privacy_confirmed_hits": 0,
            "manifest_entry_total": 1326,
            "failed_checks": ["launch_scoped_tests"],
            "failed_test_ids": [
                (
                    "test_method_flow_retains_both_witnesses "
                    "(TestTavianV652V6FinalValidationCorrection)"
                ),
                (
                    "test_negative_is_additive "
                    "(TestTavianV652V6FinalValidationCorrection)"
                ),
            ],
            "external_receipt_name": external_path.name,
            "external_receipt_sha256": hashlib.sha256(external_raw).hexdigest(),
            "external_receipt_written": True,
            "full_repository_suite_run": False,
            "canonical_success_credit": 0,
            "successful_canonical_passes": 0,
            "retained_negative_id": NEGATIVE["negative_id"],
            "boundary": (
                "Failed launch-scoped retry with zero canonical credit; Eiren's "
                "full-repository suite was not rerun and route remained unsent."
            ),
        },
    )
    base.write_json(
        "validation/final-validation-prepared-receipt.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-prepared.v4",
            "state": "third_retry_prepared_after_three_failed_attempts",
            "failed_exact_final_attempt_count": 3,
            "successful_pass_count": 0,
            "replay_count": 0,
            "completed_retry_count": 2,
            "next_retry_authorized": True,
            "external_receipt_required": True,
            "phase_commit_cap": 6,
            "planned_phase_commits": 6,
            "reason": (
                "All prior exact-head attempts earned zero success credit. One next "
                "attempt is prepared only after this final allowed additive correction "
                "is pushed, clean, and four-way equal."
            ),
        },
    )

    base.write_repo(
        "tests/test_ghc_family_v652_v6_final_validation_correction_3.py",
        test_source(),
    )
    manifest, owner = build_manifests()

    correction_test_output = base.run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v6_final_validation_correction_3",
    )
    correction_1_test_output = base.run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v6_final_validation_correction",
    )
    spec = importlib.util.spec_from_file_location(
        "tavian_final_validator_preflight_3",
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
        ROOT / "validation/final-validation-correction-3-staged-review.json"
    )
    privacy = base.read_json(
        ROOT / "validation/final-validation-correction-3-staged-privacy.json"
    )
    valid = (
        review["valid"]
        and privacy["confirmed_hit_count"] == 0
        and flow["counts"]["methods"] == 31
        and selection["eligible_count"] == EXPECTED_SCOPED_TESTS
    )
    base.write_json(
        "validation/final-validation-correction-3-validation-receipt.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-3-validation.v1"
            ),
            "built_at_utc": now,
            "correction_3_tests_passed": 5,
            "correction_3_tests_total": 5,
            "corrected_correction_1_tests_passed": 7,
            "corrected_correction_1_tests_total": 7,
            "selection_enumerated": selection["eligible_count"],
            "selection_loader_errors": selection["loader_errors"],
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "correction_manifest_entries": manifest["entry_count"],
            "corrected_owner_manifest_entries": owner["entry_count"],
            "correction_test_stdout": correction_test_output,
            "corrected_correction_1_test_stdout": correction_1_test_output,
            "full_repository_suite_rerun": False,
            "canonical_retry_run": False,
            "valid": valid,
            "boundary": (
                "Precommit third-correction validation only; canonical credit "
                "remains reserved for the pushed exact head."
            ),
        },
    )
    if not valid:
        raise RuntimeError("third correction preflight invalid")
    print(
        json.dumps(
            {
                "effective_negatives": EFFECTIVE_NEGATIVES,
                "method_flow": flow["counts"],
                "correction_3_tests": "5/5",
                "corrected_correction_1_tests": "7/7",
                "selection_enumerated": selection["eligible_count"],
                "correction_manifest_entries": manifest["entry_count"],
                "corrected_owner_manifest_entries": owner["entry_count"],
                "canonical_retry_run": False,
                "status": "third_correction_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
