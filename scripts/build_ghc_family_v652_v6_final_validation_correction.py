#!/usr/bin/env python3
"""Build the additive Tavian Sol v652-v6 final-validation correction."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import build_ghc_family_v652_v6_closeout as base
except ModuleNotFoundError:
    from scripts import build_ghc_family_v652_v6_closeout as base


REPO = base.REPO
ROOT = base.ROOT
SOURCE = base.SOURCE
CLOSEOUT = "bdb02fbe63e189700b915e18c45bc00b80e5aaeb"
NEGATIVE_ID = "V6526-FINAL-N01"
FINAL_NEGATIVES = [
    {
        "negative_id": NEGATIVE_ID,
        "category": "missing_repository_root_for_dynamic_test_import",
        "failed": (
            "The first exact-final invocation stopped before tests ran because the "
            "direct script entrypoint could not import the scripts package."
        ),
        "recovery": (
            "Bind the resolved repository root before importing scoped modules, then "
            "enumerate the corrected committed selection."
        ),
        "passing": (
            "The corrected importer loaded all seven modules and enumerated 58 tests "
            "with no loader errors; canonical credit remained unclaimed."
        ),
    },
    {
        "negative_id": "V6526-FINAL-N02",
        "category": "correction_builder_preflight_review_failure",
        "failed": (
            "The first correction build reached its targeted suite but failed one of "
            "seven tests because its staged review contained a truncated first path "
            "and was invalid."
        ),
        "recovery": (
            "Read raw porcelain output without stripping its first leading status "
            "column, then rebuild the correction review and manifests from closeout."
        ),
        "passing": (
            "The rebuilt review preserved every complete path, reported no unexpected "
            "path, and the targeted correction suite passed seven of seven."
        ),
    },
    {
        "negative_id": "V6526-FINAL-N03",
        "category": "diagnostic_correction_suite_failure",
        "failed": (
            "The isolated verbose diagnostic suite reproduced the invalid-review "
            "assertion as one failure among seven tests and earned zero validation credit."
        ),
        "recovery": (
            "Use the reproduced truncated path to isolate the leading-column parser "
            "defect, correct it, and rerun only through the rebuilt correction preflight."
        ),
        "passing": (
            "The corrected raw-output parser retained the leading character and the "
            "rebuilt seven-test correction preflight passed completely."
        ),
    },
    {
        "negative_id": "V6526-FINAL-N04",
        "category": "malformed_regex_source_probe",
        "failed": (
            "A bounded source-location probe used an unbalanced regular expression "
            "for code punctuation and exited with a regex parse error."
        ),
        "recovery": (
            "Search the exact code token as a fixed string, then inspect only the "
            "bounded surrounding line range."
        ),
        "passing": (
            "The literal probe located the refresh boundary and the bounded line read "
            "exposed the exact insertion point without interpreting punctuation."
        ),
    },
]
EFFECTIVE_NEGATIVES = base.EFFECTIVE_NEGATIVES + len(FINAL_NEGATIVES)
EXPECTED_SCOPED_TESTS = 58
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
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-25.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-26.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-27.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/method-28.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-25-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-25-passing.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-26-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-26-passing.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-27-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-27-passing.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-28-failed.json",
    f"{base.d.PHASE_ROOT}/method-flow/requests/witness-28-passing.json",
    f"{base.d.PHASE_ROOT}/truth/final-validation-retained-negative.json",
    f"{base.d.PHASE_ROOT}/validation/final-validation-failed-attempt-01.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-failed-attempt-01.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-diagnostic-failed-attempt-01.json"
    ),
    f"{base.d.PHASE_ROOT}/validation/final-validation-prepared-receipt.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-staged-privacy.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-staged-review.json"
    ),
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-staged-manifest.json"
    ),
    f"{base.d.PHASE_ROOT}/validation/final-corrected-owner-manifest.json",
    (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-validation-receipt.json"
    ),
    "scripts/build_ghc_family_v652_v6_final_validation_correction.py",
    "scripts/ghc_family_v652_v6_final_validate.py",
    "tests/test_ghc_family_v652_v6_final_validation_correction.py",
}


def status_paths() -> list[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    rows = proc.stdout.decode("utf-8").splitlines()
    return sorted(
        {
            row[3:].replace("\\", "/")
            for row in rows
            if len(row) > 3
        }
    )


def append_method_flow() -> dict[str, Any]:
    ledger = json.loads(
        base.git(
            "show",
            f"{CLOSEOUT}:{base.d.PHASE_ROOT}/method-flow/final-method-flow-ledger.json",
        )
    )
    spec = importlib.util.spec_from_file_location(
        "ghc_family_method_flow_state_final_correction", base.METHOD_RUNNER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load the official Method Flow runner")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    method_id = "V6526-METHOD-25"
    method = {
        "method_id": method_id,
        "title": "Restore repository-root import visibility before scoped loading",
        "failure_signature": (
            "The first exact-final attempt stopped during scoped test import because "
            "the validator omitted the repository root from sys.path."
        ),
        "trigger_preconditions": ["scoped_test_import_from_direct_script_entrypoint"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_local_final_validation_recovery",
        "candidate_workaround": (
            "Insert the resolved repository root at the front of sys.path before "
            "loading test modules, then enumerate the committed launch selection."
        ),
        "validation_witness_ids": [],
        "recurrence_guard": (
            "Every direct-entrypoint validator that imports repository packages must "
            "bind the repository root before dynamic module loading."
        ),
        "rollback": (
            "Stop, retain the failed attempt, remove no evidence, and leave route and "
            "external authority state unchanged."
        ),
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": base.d.PROTECTED_GATES,
        "retained_negative_ids": [NEGATIVE_ID],
        "scope_boundary": (
            "Import-path and selection-enumeration recovery only; no canonical, "
            "full-repository, independent-reproduction, or route-send credit."
        ),
    }
    failed = {
        "witness_id": "V6526-WITNESS-25-F",
        "method_id": method_id,
        "procedure": "Invoke the direct-entrypoint exact-final validator.",
        "scope": "selected_test_import",
        "expected": "All six committed launch-scoped modules import.",
        "observed": (
            "Import stopped before tests ran because the repository package root was "
            "not visible."
        ),
        "result": "fail",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [NEGATIVE_ID],
        "boundary": "Zero canonical or aggregate credit; no external receipt was written.",
    }
    passing = {
        "witness_id": "V6526-WITNESS-25-P",
        "method_id": method_id,
        "procedure": (
            "Bind the repository root before dynamic imports and enumerate the "
            "corrected seven-module launch selection without executing it."
        ),
        "scope": "import_path_and_selection_enumeration",
        "expected": "All modules import and exactly 58 tests are selected.",
        "observed": (
            "All seven modules imported with no loader errors and exactly 58 tests "
            "were enumerated; the canonical retry remained unrun."
        ),
        "result": "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": [NEGATIVE_ID],
        "boundary": (
            "Bounded same-owner recovery only; canonical credit remains reserved for "
            "the later pushed exact-head retry."
        ),
    }
    base.write_json("method-flow/requests/method-25.json", method)
    base.write_json("method-flow/requests/witness-25-failed.json", failed)
    base.write_json("method-flow/requests/witness-25-passing.json", passing)
    ledger["methods"].append(method)
    runner.append_event(
        ledger,
        method_id,
        None,
        "candidate",
        "method recorded with retained failed-attempt linkage",
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
        "bounded import and enumeration witness passed",
        passing["witness_id"],
    )
    method["recommendation_state"] = "preferred"
    runner.append_event(
        ledger,
        method_id,
        "validated",
        "preferred",
        "Promoted only after bounded recovery; failed attempt retained.",
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
    for number, negative in enumerate(FINAL_NEGATIVES[1:], start=26):
        extra_method_id = f"V6526-METHOD-{number:02d}"
        extra_method = {
            "method_id": extra_method_id,
            "title": f"Bounded recovery for {negative['category']}",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [negative["category"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_final_validation_recovery",
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": (
                "Retain the exact failed witness and use only the isolated bounded "
                "recovery before rebuilding correction artifacts."
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
                "Owner-local correction recovery only; no canonical, aggregate, "
                "independent-reproduction, or route-send credit."
            ),
        }
        extra_failed = {
            "witness_id": f"V6526-WITNESS-{number:02d}-F",
            "method_id": extra_method_id,
            "procedure": "Retain the exact failed correction attempt.",
            "scope": negative["category"],
            "expected": "The bounded correction postcondition would pass.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero validation credit; failed witness retained.",
        }
        extra_passing = {
            "witness_id": f"V6526-WITNESS-{number:02d}-P",
            "method_id": extra_method_id,
            "procedure": negative["recovery"],
            "scope": negative["category"],
            "expected": "The isolated recovery establishes only its stated postcondition.",
            "observed": negative["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": (
                "Same-owner bounded recovery only; the failed witness remains."
            ),
        }
        base.write_json(
            f"method-flow/requests/method-{number:02d}.json",
            extra_method,
        )
        base.write_json(
            f"method-flow/requests/witness-{number:02d}-failed.json",
            extra_failed,
        )
        base.write_json(
            f"method-flow/requests/witness-{number:02d}-passing.json",
            extra_passing,
        )
        ledger["methods"].append(extra_method)
        runner.append_event(
            ledger,
            extra_method_id,
            None,
            "candidate",
            "method recorded with retained negative linkage",
        )
        ledger["witnesses"].append(extra_failed)
        extra_method["validation_witness_ids"].append(extra_failed["witness_id"])
        ledger["witnesses"].append(extra_passing)
        extra_method["validation_witness_ids"].append(extra_passing["witness_id"])
        extra_method["recommendation_state"] = "validated"
        runner.append_event(
            ledger,
            extra_method_id,
            "candidate",
            "validated",
            "bounded correction witness passed",
            extra_passing["witness_id"],
        )
        extra_method["recommendation_state"] = "preferred"
        runner.append_event(
            ledger,
            extra_method_id,
            "validated",
            "preferred",
            "Promoted only after bounded recovery; failed witness retained.",
        )
        ledger["recommendations"].append(
            {
                "recommendation_index": len(ledger["recommendations"]) + 1,
                "method_id": extra_method_id,
                "preconditions": extra_method["trigger_preconditions"],
                "method": extra_method["candidate_workaround"],
                "witness_ids": extra_method["validation_witness_ids"],
                "recurrence_guard": extra_method["recurrence_guard"],
                "rollback": extra_method["rollback"],
                "scope_boundary": extra_method["scope_boundary"],
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
    return '''"""Correction tests for Tavian Sol v652-v6 final validation."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tavian-sol/v652-v6"


class TestTavianV652V6FinalValidationCorrection(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_failed_attempt_is_zero_credit(self):
        row = self.load("validation/final-validation-failed-attempt-01.json")
        self.assertEqual(row["tests_run"], 0)
        self.assertEqual(row["canonical_success_credit"], 0)
        self.assertFalse(row["external_receipt_written"])

    def test_negative_is_additive(self):
        row = self.load("final/retained-negative-register.json")
        self.assertEqual(row["final_validation_operational"], 4)
        self.assertEqual(row["effective_count"], 8914)
        self.assertTrue(row["no_failure_erased"])

    def test_method_flow_retains_both_witnesses(self):
        flow = self.load("method-flow/final-method-flow-ledger.json")
        self.assertEqual(flow["counts"]["methods"], 28)
        self.assertEqual(flow["counts"]["witness_results"], {"fail":28,"pass":28})
        self.assertEqual(flow["counts"]["states"]["preferred"], 28)

    def test_launch_contract_not_full_repository(self):
        row = self.load("final/final-validation-contract.json")
        self.assertEqual(row["validation_scope"], "launch_scoped")
        self.assertEqual(row["expected_scoped_tests"], 58)
        self.assertFalse(row["full_repository_suite_required"])
        self.assertEqual(row["full_repository_suite_owner"], "Eiren Kestrel")

    def test_route_remains_unsent(self):
        row = self.load("route/final-route-state.json")
        self.assertEqual(row["state"], "PREPARED_NOT_SENT")
        self.assertEqual(row["send_count"], 0)
        self.assertEqual(row["contact_count"], 0)

    def test_validator_binds_repository_root(self):
        text = (REPO / "scripts/ghc_family_v652_v6_final_validate.py").read_text(encoding="utf-8")
        self.assertIn("sys.path.insert(0, str(REPO))", text)
        self.assertIn("test_ghc_family_v652_v6_final_validation_correction.py", text)

    def test_correction_preflight_review(self):
        review = self.load("validation/final-validation-correction-staged-review.json")
        privacy = self.load("validation/final-validation-correction-staged-privacy.json")
        self.assertTrue(review["valid"])
        self.assertEqual(review["unexpected_paths"], [])
        self.assertEqual(privacy["confirmed_hit_count"], 0)


if __name__ == "__main__":
    unittest.main()
'''


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(
            r"(?i)(?:[A-Z]:\\[^\s\"']+|[A-Z]:\\\\[^\s\"']+|"
            r"/Users/[^\s\"']+|/home/[^\s\"']+)"
        ),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|"
            r"bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|"
            r"browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v6_final_validation_correction.py",
        "scripts/ghc_family_v652_v6_final_validate.py",
        (
            f"{base.d.PHASE_ROOT}/validation/"
            "final-validation-correction-staged-privacy.json"
        ),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = (
                    "scanner_definition"
                    if relative in definitions
                    else "confirmed_payload_hit"
                )
                row = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": disposition,
                }
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v652-v6.final-validation-correction-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": (
            "Five structural classes with scanner-definition quarantine; zero "
            "confirmed hits is not complete privacy assurance."
        ),
    }


def hash_entry(relative: str) -> dict[str, Any]:
    oid = base.git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def build_manifests() -> tuple[dict[str, Any], dict[str, Any]]:
    correction_manifest_path = (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-staged-manifest.json"
    )
    owner_manifest_path = (
        f"{base.d.PHASE_ROOT}/validation/final-corrected-owner-manifest.json"
    )
    validation_receipt_path = (
        f"{base.d.PHASE_ROOT}/validation/"
        "final-validation-correction-validation-receipt.json"
    )
    correction_exclusions = [
        correction_manifest_path,
        owner_manifest_path,
        validation_receipt_path,
    ]
    owner_exclusions = [owner_manifest_path, validation_receipt_path]
    current = set(status_paths())
    unexpected = sorted(current - CORRECTION_PATHS)
    privacy = privacy_scan(sorted(current))
    base.write_json(
        "validation/final-validation-correction-staged-privacy.json",
        privacy,
    )
    base.write_json(
        "validation/final-validation-correction-staged-review.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-staged-review.v1"
            ),
            "closeout_head": CLOSEOUT,
            "head_before_correction_commit": base.git("rev-parse", "HEAD"),
            "unexpected_paths": unexpected,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "route_mutated": False,
            "x1_or_evidence_mutated": False,
            "valid": (
                base.git("rev-parse", "HEAD") == CLOSEOUT
                and not unexpected
                and privacy["confirmed_hit_count"] == 0
            ),
        },
    )
    current = set(status_paths())
    correction_paths = sorted(
        path
        for path in current
        if path not in correction_exclusions
        and (REPO / path).is_file()
        and "__pycache__" not in path
    )
    correction_entries = [hash_entry(path) for path in correction_paths]
    correction_manifest = {
        "schema": (
            "ghc.family.v652-v6.final-validation-correction-staged-manifest.v1"
        ),
        "hash_domain": "git_path_filtered_blob",
        "closeout_head": CLOSEOUT,
        "entry_count": len(correction_entries),
        "entries": correction_entries,
        "self_exclusions": correction_exclusions,
        "coverage_boundary": (
            "All intended final-validation correction paths except the correction "
            "manifest, cumulative corrected owner manifest, and count-bearing "
            "correction validation receipt."
        ),
    }
    base.write_json(
        "validation/final-validation-correction-staged-manifest.json",
        correction_manifest,
    )
    committed = set(
        filter(
            None,
            base.git("diff", "--name-only", SOURCE, "HEAD").splitlines(),
        )
    )
    current = set(status_paths())
    owner_paths = sorted(
        path
        for path in committed | current
        if path not in owner_exclusions
        and (REPO / path).is_file()
        and "__pycache__" not in path
    )
    owner_entries = [hash_entry(path) for path in owner_paths]
    owner_manifest = {
        "schema": "ghc.family.v652-v6.final-corrected-owner-manifest.v1",
        "hash_domain": "git_path_filtered_blob",
        "source_head": SOURCE,
        "closeout_head": CLOSEOUT,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "self_exclusions": owner_exclusions,
        "coverage_boundary": (
            "All Tavian source-to-corrected-final owner paths except this cumulative "
            "manifest and the count-bearing correction validation receipt."
        ),
    }
    base.write_json(
        "validation/final-corrected-owner-manifest.json",
        owner_manifest,
    )
    return correction_manifest, owner_manifest


def build() -> None:
    if base.git("rev-parse", "HEAD") != CLOSEOUT:
        raise RuntimeError("correction builder must begin at the sealed closeout head")
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    flow = append_method_flow()

    negatives = json.loads(
        base.git(
            "show",
            f"{CLOSEOUT}:{base.d.PHASE_ROOT}/final/retained-negative-register.json",
        )
    )
    negatives["final_validation_operational"] = len(FINAL_NEGATIVES)
    negatives["final_validation_rows"] = [
        {**row, "canonical_success_credit": 0}
        for row in FINAL_NEGATIVES
    ]
    negatives["effective_count"] = EFFECTIVE_NEGATIVES
    base.write_json("final/retained-negative-register.json", negatives)

    truth = json.loads(
        base.git(
            "show",
            f"{CLOSEOUT}:{base.d.PHASE_ROOT}/final/final-phase-truth.json",
        )
    )
    truth["effective_negatives"] = EFFECTIVE_NEGATIVES
    base.write_json("final/final-phase-truth.json", truth)

    anchor = json.loads(
        base.git(
            "show",
            f"{CLOSEOUT}:{base.d.PHASE_ROOT}/final/anchor-ledger.json",
        )
    )
    anchor["closeout"] = CLOSEOUT
    anchor["final"] = "resolve_as_containing_correction_commit_after_creation"
    anchor["three_phase_commits_required"] = False
    anchor["four_phase_commits_required"] = True
    anchor["retained_failed_exact_final_attempts"] = 1
    base.write_json("final/anchor-ledger.json", anchor)

    wellbeing = json.loads(
        base.git(
            "show",
            (
                f"{CLOSEOUT}:{base.d.PHASE_ROOT}/final/"
                "wellbeing-workload-receipt.json"
            ),
        )
    )
    wellbeing["planned_phase_commits"] = 4
    wellbeing["retained_failed_exact_final_attempts"] = 1
    wellbeing["successful_canonical_passes_before_retry"] = 0
    base.write_json("final/wellbeing-workload-receipt.json", wellbeing)

    contract = json.loads(
        base.git(
            "show",
            (
                f"{CLOSEOUT}:{base.d.PHASE_ROOT}/final/"
                "final-validation-contract.json"
            ),
        )
    )
    contract["expected_scoped_tests"] = EXPECTED_SCOPED_TESTS
    contract["patterns"] = [
        "test_ghc_family_v652_v5_closeout.py",
        "test_ghc_family_v652_v5_route_correction.py",
        "test_ghc_family_v652_v5_final_validation_correction.py",
        "test_ghc_family_v652_v6_x1.py",
        "test_ghc_family_v652_v6_core.py",
        "test_ghc_family_v652_v6_closeout.py",
        "test_ghc_family_v652_v6_final_validation_correction.py",
    ]
    contract["retained_failed_exact_final_attempts"] = 1
    contract["retained_correction_preflight_failures"] = 2
    contract["retained_correction_probe_failures"] = 1
    contract["successful_canonical_passes_before_retry"] = 0
    contract["retry_authorized_after_zero_success"] = True
    contract["checks"] = [
        "launch-scoped tests",
        "complete phase JSON",
        "five-class privacy scan",
        "six manifest contracts",
        "stale labels",
        "document contracts",
        "source/x1/evidence/closeout ancestry",
        "four phase commits",
        "zero merges",
        "one final parent",
        "one retained zero-credit failed exact-final attempt",
        "exact head",
        "clean before and after",
        "four-way live equality",
    ]
    base.write_json("final/final-validation-contract.json", contract)

    base.write_json(
        "truth/final-validation-retained-negative.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-negative.v1",
            "negative_ids": [
                row["negative_id"] for row in FINAL_NEGATIVES
            ],
            "sealed_closeout_effective": base.EFFECTIVE_NEGATIVES,
            "final_validation_operational": len(FINAL_NEGATIVES),
            "effective_final": EFFECTIVE_NEGATIVES,
            "failed_exact_final_attempts": 1,
            "failed_correction_preflights": 2,
            "failed_source_probes": 1,
            "canonical_tests_run": 0,
            "external_receipt_written": False,
            "failed_attempt_received_credit": False,
            "no_failure_erased": True,
        },
    )
    base.write_json(
        "validation/final-validation-failed-attempt-01.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-failed-attempt.v1",
            "recorded_at_utc": now,
            "attempted_head": CLOSEOUT,
            "failure_stage": "selected_test_import",
            "error_class": "ModuleNotFoundError",
            "sanitized_error": (
                "The scripts package was unavailable while importing the current "
                "core test module from the direct validator entrypoint."
            ),
            "tests_run": 0,
            "external_receipt_written": False,
            "canonical_success_credit": 0,
            "successful_canonical_passes": 0,
            "retained_negative_id": NEGATIVE_ID,
            "boundary": (
                "Incomplete failed attempt with zero aggregate credit; no route, "
                "full-repository, or exact-final success claim."
            ),
        },
    )
    base.write_json(
        "validation/final-validation-correction-failed-attempt-01.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-failed-attempt.v1"
            ),
            "attempted_head": CLOSEOUT,
            "failure_stage": "targeted_correction_preflight",
            "tests_run": 7,
            "passed": 6,
            "failures": 1,
            "failed_assertion": "correction staged review valid",
            "root_cause": "leading_porcelain_status_column_was_stripped",
            "canonical_success_credit": 0,
            "retained_negative_id": "V6526-FINAL-N02",
            "boundary": (
                "Failed precommit correction build only; no canonical retry or "
                "full-repository suite ran."
            ),
        },
    )
    base.write_json(
        "validation/final-validation-diagnostic-failed-attempt-01.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-diagnostic-failed-attempt.v1"
            ),
            "attempted_head": CLOSEOUT,
            "failure_stage": "isolated_verbose_correction_test",
            "tests_run": 7,
            "passed": 6,
            "failures": 1,
            "failed_assertion": "correction staged review valid",
            "canonical_success_credit": 0,
            "retained_negative_id": "V6526-FINAL-N03",
            "boundary": (
                "Diagnostic reproduction only; zero validation credit and no "
                "canonical retry."
            ),
        },
    )
    base.write_json(
        "validation/final-validation-prepared-receipt.json",
        {
            "schema": "ghc.family.v652-v6.final-validation-prepared.v2",
            "state": "retry_prepared_after_failed_attempt",
            "failed_attempt_count": 1,
            "failed_correction_preflight_count": 2,
            "failed_source_probe_count": 1,
            "successful_pass_count": 0,
            "replay_count": 0,
            "retry_count": 0,
            "retry_authorized": True,
            "external_receipt_required": True,
            "reason": (
                "The first attempt stopped before tests and earned zero credit. One "
                "retry is prepared only after the additive correction is pushed, clean, "
                "and four-way equal."
            ),
        },
    )

    base.write_repo(
        "tests/test_ghc_family_v652_v6_final_validation_correction.py",
        test_source(),
    )
    correction_manifest, owner_manifest = build_manifests()

    test_output = base.run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v6_final_validation_correction",
    )
    spec = importlib.util.spec_from_file_location(
        "tavian_final_validator_preflight",
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
        ROOT / "validation/final-validation-correction-staged-review.json"
    )
    privacy = base.read_json(
        ROOT / "validation/final-validation-correction-staged-privacy.json"
    )
    valid = (
        review["valid"]
        and privacy["confirmed_hit_count"] == 0
        and flow["counts"]["methods"] == 28
        and selection["eligible_count"] == EXPECTED_SCOPED_TESTS
    )
    base.write_json(
        "validation/final-validation-correction-validation-receipt.json",
        {
            "schema": (
                "ghc.family.v652-v6.final-validation-correction-validation.v1"
            ),
            "built_at_utc": now,
            "correction_tests_passed": 7,
            "correction_tests_total": 7,
            "selection_enumerated": selection["eligible_count"],
            "selection_loader_errors": selection["loader_errors"],
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "correction_manifest_entries": correction_manifest["entry_count"],
            "corrected_owner_manifest_entries": owner_manifest["entry_count"],
            "test_stdout": test_output,
            "full_repository_suite_rerun": False,
            "canonical_retry_run": False,
            "valid": valid,
            "boundary": (
                "Precommit correction validation only; canonical retry credit remains "
                "reserved for the pushed corrected exact head."
            ),
        },
    )
    if not valid:
        raise RuntimeError("final-validation correction preflight invalid")
    print(
        json.dumps(
            {
                "effective_negatives": EFFECTIVE_NEGATIVES,
                "method_flow": flow["counts"],
                "correction_tests": "7/7",
                "selection_enumerated": selection["eligible_count"],
                "correction_manifest_entries": correction_manifest["entry_count"],
                "corrected_owner_manifest_entries": owner_manifest["entry_count"],
                "canonical_retry_run": False,
                "status": "correction_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
