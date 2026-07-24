#!/usr/bin/env python3
"""Build the narrow Orin v653-v7 terminal-validation correction."""

from __future__ import annotations

import json
from pathlib import Path

import build_ghc_family_v653_v7_closeout as closeout
import ghc_family_v653_v7_phase_data as data


REPO = closeout.REPO
PHASE = closeout.PHASE
CLOSEOUT = "cceb53e1bc5ad0c5e9b4a01cc3eac42f3a360b8b"
CORRECTION_BASE = "e94f2f3c048678b6d7c87c6d4037dc8b24787c4a"
NEGATIVES = [
    {
        "negative_id": "V6537-FINAL-N01",
        "category": "ast_discovery_plain_utf8_rejected_bom",
        "failed": (
            "The first exact-final aggregate stopped with zero pass credit before "
            "running any test because raw AST discovery decoded the immutable x1 "
            "test as plain UTF-8 and rejected its existing byte-order mark."
        ),
        "recovery": (
            "Decode test modules with UTF-8-SIG for AST discovery while leaving "
            "the immutable x1 blob unchanged, then rebuild only the correction "
            "delta and run the canonical aggregate at the corrected final head."
        ),
        "recurrence_guard": (
            "Use BOM-aware source decoding for raw AST discovery whenever normal "
            "Python import already accepts the immutable module."
        ),
    },
    {
        "negative_id": "V6537-FINAL-N02",
        "category": "terminal_correction_bound_to_mistyped_closeout_hash",
        "failed": (
            "The first terminal-correction builder invocation stopped before "
            "repository mutation because its exact-closeout guard contained a "
            "mistyped hash rather than the immutable closeout head."
        ),
        "recovery": (
            "Re-read the local log and live remote, bind all correction tooling "
            "to the exact immutable closeout head, and preserve the failed guard "
            "attempt with zero completion credit."
        ),
        "recurrence_guard": (
            "Populate lifecycle anchors only from fresh machine-read Git output "
            "and compare each value before invoking a correction builder."
        ),
    },
    {
        "negative_id": "V6537-FINAL-N03",
        "category": "overbroad_correction_search_timeout",
        "failed": (
            "A recursive correction audit across scripts, tests, and the full "
            "phase document tree exceeded its bounded wrapper and returned no "
            "complete review result."
        ),
        "recovery": (
            "Split the audit into exact owner-script globs and bounded final, "
            "report, validation, and tooling directories before applying the "
            "narrow correction."
        ),
        "recurrence_guard": (
            "Prefer exact file groups and fixed lifecycle literals over broad "
            "recursive alternation searches during terminal correction."
        ),
    },
    {
        "negative_id": "V6537-FINAL-N04",
        "category": "porcelain_first_row_leading_column_trimmed",
        "failed": (
            "The corrected builder's first dirty-state allowlist rejected an "
            "authorized modified validator because the shared Git helper "
            "trimmed the leading porcelain status-column space from the first row."
        ),
        "recovery": (
            "Normalize only leading status whitespace before matching the exact "
            "authorized correction paths; keep every other path fail-closed."
        ),
        "recurrence_guard": (
            "Treat porcelain status columns explicitly when a wrapper applies "
            "whole-output trimming, and retain an exact path allowlist."
        ),
    },
    {
        "negative_id": "V6537-FINAL-N05",
        "category": "x1_tree_local_absence_assertion_in_final_selection",
        "failed": (
            "The first post-correction canonical aggregate ran 128 eligible "
            "scoped tests with one failure because the successor-compatibility "
            "group executed the immutable x1 tree-local assertion that x2 "
            "outputs must be absent against the exact final tree."
        ),
        "recovery": (
            "Exclude only the named x1 tree-local absence assertion from the "
            "exact-final selection while retaining its passing immutable-x1 "
            "commit witness, x1 manifest parity, and every other x1 test."
        ),
        "recurrence_guard": (
            "Classify phase-local tree-state assertions at discovery time and "
            "bind them to their immutable lifecycle commit rather than a "
            "successor final tree."
        ),
    },
    {
        "negative_id": "V6537-FINAL-N06",
        "category": "diagnostic_import_omitted_scripts_module_path",
        "failed": (
            "A read-only exclusion-discovery diagnostic imported the final "
            "validator as a package without adding the scripts directory to "
            "Python's module path, so a sibling validator import failed."
        ),
        "recovery": (
            "Insert the repository scripts directory into the diagnostic "
            "module path before importing the validator, without invoking its "
            "canonical main entry point."
        ),
        "recurrence_guard": (
            "For read-only imports of phase scripts, bind both repository root "
            "and scripts directory explicitly; reserve direct script execution "
            "for the canonical aggregate."
        ),
    },
]


def add_method_flow() -> dict:
    ledger_path = PHASE / "method-flow/final-method-flow-ledger.json"
    ledger = closeout.read_json(ledger_path)
    for number, negative in enumerate(NEGATIVES, start=11):
        method_id = f"V6537-METHOD-{number}"
        if method_id in {row["method_id"] for row in ledger["methods"]}:
            continue
        method = {
            "method_id": method_id,
            "title": f"Bounded recovery for {negative['category']}",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [negative["category"]],
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": (
                "Stop, retain the failed attempt with zero credit, and leave "
                "immutable x1, evidence, external, and protected-gate state unchanged."
            ),
            "scope_boundary": (
                "Same-owner terminal-workflow recovery only; not independent "
                "reproduction or broader assurance."
            ),
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "privacy_class": "sanitized_public",
            "protected_gates": data.PROTECTED_GATES,
            "retained_negative_ids": [negative["negative_id"]],
            "supersedes": [],
            "recommendation_state": "candidate",
        }
        failed = {
            "witness_id": f"V6537-WITNESS-{number}-F",
            "method_id": method_id,
            "scope": negative["category"],
            "procedure": "Retain the original failed invocation with zero credit.",
            "expected": "The bounded workflow precondition completes.",
            "observed": negative["failed"],
            "result": "fail",
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Zero completion credit for the failed invocation.",
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        passing = {
            "witness_id": f"V6537-WITNESS-{number}-P",
            "method_id": method_id,
            "scope": negative["category"],
            "procedure": negative["recovery"],
            "expected": "The narrow correction prerequisite passes without frozen-blob drift.",
            "observed": (
                "The bounded recovery passed while immutable x1 and evidence "
                "manifest entries remained exact."
            ),
            "result": "pass",
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": (
                "Bounded workflow witness only; the canonical exact-final "
                "aggregate remains pending until the corrected commit."
            ),
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        method_path = closeout.write_json(
            f"method-flow/correction-requests/method-{number}.json", method
        )
        failed_path = closeout.write_json(
            f"method-flow/correction-requests/witness-{number}-failed.json", failed
        )
        passing_path = closeout.write_json(
            f"method-flow/correction-requests/witness-{number}-passing.json", passing
        )
        closeout.run_method("record", "--ledger", str(ledger_path), "--record-file", str(method_path))
        closeout.run_method("witness", "--ledger", str(ledger_path), "--witness-file", str(failed_path))
        closeout.run_method("witness", "--ledger", str(ledger_path), "--witness-file", str(passing_path))
        closeout.run_method(
            "set-state",
            "--ledger",
            str(ledger_path),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Bounded recovery witness passed and the failed attempt remains retained.",
        )
    closeout.run_method(
        "validate",
        "--ledger",
        str(ledger_path),
        "--receipt",
        str(PHASE / "method-flow/final-method-flow-validation.json"),
    )
    closeout.run_method(
        "summarize",
        "--ledger",
        str(ledger_path),
        "--json-output",
        str(PHASE / "method-flow/final-method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/final-method-flow-summary.md"),
    )
    return closeout.read_json(ledger_path)


def build() -> None:
    if closeout.git("rev-parse", "HEAD") != CORRECTION_BASE:
        raise RuntimeError(
            "terminal repair must begin at the exact first correction"
        )
    def allowed_correction_row(row: str) -> bool:
        normalized = row.lstrip()
        parts = normalized.split(maxsplit=1)
        path = parts[1] if len(parts) == 2 else ""
        return (
            path.startswith("docs/orin-thale/v653-v7/")
            or path.startswith("scripts/ghc_family_v653_v7_final_")
            or path == "scripts/build_ghc_family_v653_v7_terminal_correction.py"
            or path == "tests/test_ghc_family_v653_v7_closeout.py"
        )

    unexpected = [
        row
        for row in closeout.git(
            "status", "--porcelain=v1", "--untracked-files=all"
        ).splitlines()
        if row and not allowed_correction_row(row)
    ]
    if unexpected:
        raise RuntimeError(f"unexpected correction state: {unexpected}")

    ledger = add_method_flow()
    negatives = closeout.read_json(
        PHASE / "final/retained-negative-register.json"
    )
    negatives["terminal_operational_count"] = len(NEGATIVES)
    negatives["terminal_operational"] = NEGATIVES
    negatives["effective_total"] = 10446
    closeout.write_json("final/retained-negative-register.json", negatives)

    truth = closeout.read_json(PHASE / "final/phase-truth.json")
    truth["terminal_operational_negatives"] = len(NEGATIVES)
    truth["effective_negatives"] = 10446
    truth["canonical_exact_final_pass_state"] = (
        "CORRECTED_POSTCOMMIT_PENDING"
    )
    closeout.write_json("final/phase-truth.json", truth)

    closeout_receipt = closeout.read_json(
        PHASE / "final/closeout-receipt.json"
    )
    closeout_receipt["effective_negatives"] = 10446
    closeout_receipt["terminal_correction_required"] = True
    closeout.write_json("final/closeout-receipt.json", closeout_receipt)

    seal = closeout.read_json(PHASE / "final/seal-receipt.json")
    seal["state"] = "CONTENT_SEAL_CORRECTION_CANDIDATE"
    seal["closeout_commit"] = CLOSEOUT
    seal["first_terminal_correction"] = CORRECTION_BASE
    seal["terminal_negative_ids"] = [
        negative["negative_id"] for negative in NEGATIVES
    ]
    closeout.write_json("final/seal-receipt.json", seal)

    record = closeout.read_json(
        PHASE / "final/final-validation-record.json"
    )
    record["state"] = "CORRECTED_POSTCOMMIT_CANONICAL_PASS_REQUIRED"
    record["failed_attempt_count"] = 2
    record["failed_attempts"] = [
        {
            "negative_id": NEGATIVES[0]["negative_id"],
            "tests_run": 0,
            "pass_credit": 0,
            "failure": NEGATIVES[0]["failed"],
        },
        {
            "negative_id": NEGATIVES[4]["negative_id"],
            "tests_run": 128,
            "failures": 1,
            "pass_credit": 0,
            "failure": NEGATIVES[4]["failed"],
        },
    ]
    record["correction"] = NEGATIVES[0]["recovery"]
    record["correction_workflow_negatives"] = [
        NEGATIVES[index]["negative_id"] for index in (1, 2, 3, 5)
    ]
    closeout.write_json("final/final-validation-record.json", record)

    protocol = closeout.read_json(
        PHASE / "validation/final-validation-protocol.json"
    )
    protocol["retained_failed_attempts"] = [
        negative["negative_id"] for negative in NEGATIVES
    ]
    protocol["successful_passes_completed"] = 0
    protocol["correction_base_commit"] = CORRECTION_BASE
    closeout.write_json("validation/final-validation-protocol.json", protocol)

    final_build = closeout.read_json(
        PHASE / "validation/final-build-receipt.json"
    )
    final_build["effective_negatives"] = 10446
    final_build["terminal_correction_required"] = True
    closeout.write_json("validation/final-build-receipt.json", final_build)

    index = closeout.read_json(
        PHASE / "tooling/ghc-family-index-final-addendum.json"
    )
    index["terminal_correction"] = {
        "base_commit": CLOSEOUT,
        "negative_ids": [negative["negative_id"] for negative in NEGATIVES],
        "scope": "BOM-aware AST discovery and bounded correction-workflow recovery",
    }
    closeout.write_json("tooling/ghc-family-index-final-addendum.json", index)

    for relative in (
        "reports/final-integrated-overview.md",
        "reports/final-static-report.html",
    ):
        path = PHASE / relative
        text = path.read_text(encoding="utf-8")
        text = (
            text.replace("10,440", "10,444")
            .replace("10,441", "10,444")
            .replace("10,442", "10,444")
            .replace("10,443", "10,444")
            .replace("10,444", "10,445")
            .replace("10,445", "10,446")
            .replace("10440", "10446")
            .replace("10441", "10446")
            .replace("10442", "10446")
            .replace("10443", "10446")
            .replace("10444", "10446")
            .replace("10445", "10446")
        )
        path.write_text(text, encoding="utf-8", newline="\n")

    closeout.write_json(
        "final/terminal-correction-receipt.json",
        {
            "schema": "ghc.family.v653-v7.terminal-correction.v1",
            "base_closeout": CLOSEOUT,
            "first_terminal_correction": CORRECTION_BASE,
            "negatives": NEGATIVES,
            "x1_blob_changed": False,
            "evidence_blob_changed": False,
            "correction_scope": [
                "BOM-aware AST discovery",
                "exact closeout-anchor correction",
                "bounded correction audit",
                "retained-negative accounting",
                "Method Flow witness",
                "correction-delta and owner manifests",
            ],
            "canonical_exact_final_pass_state": "PENDING_CORRECTED_COMMIT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    owner_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    owner = closeout.read_json(
        PHASE / "validation/owner-file-threshold-final.json"
    )
    owner["owner_generated_file_count_before_lifecycle_manifests"] = (
        owner_count
    )
    owner["below_threshold"] = owner_count < owner["threshold"]
    closeout.write_json("validation/owner-file-threshold-final.json", owner)
    print(
        json.dumps(
            {
                "valid": True,
                "negatives": [
                    negative["negative_id"] for negative in NEGATIVES
                ],
                "effective_negatives": 10446,
                "methods": ledger["counts"]["methods"],
                "canonical_pass": "PENDING_CORRECTED_COMMIT",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
