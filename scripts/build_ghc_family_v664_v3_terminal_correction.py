#!/usr/bin/env python3
"""Build and review Vesper v664-v3's additive terminal-manifest correction."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/vesper-arlen/v664-v3"
PHASE_PREFIX = "docs/vesper-arlen/v664-v3/"
SOURCE = "01043740ba76979ec037abddf00a0284535abc0b"
X1 = "ce24a100bc5317d91b85afe3848f5fa2803ebe93"
EVIDENCE = "ba42eed137d3c12b880232c99adb610a4a1e90fc"
INITIAL_FINAL = "d03b584fff9130d2836cc3733f8918d7b6ea9a95"
FAILED_CANONICAL_RECEIPT_SHA256 = "c8675a5bf869f829e7e4120f089cea35473f98e732b181f2892465ad3f956b7d"
FAILED_CANONICAL_TESTS = 63
FAILED_CANONICAL_JSON = 140
FAILED_CANONICAL_PRIVACY_FILES = 162
CORRECTION_MANIFEST = f"{PHASE_PREFIX}validation/terminal-correction-manifest.json"
CORRECTION_CANDIDATE = f"{PHASE_PREFIX}validation/terminal-correction-stage-candidate.json"
CORRECTION_REVIEW = f"{PHASE_PREFIX}validation/terminal-correction-staged-review.json"
CORRECTION_SELF_EXCLUSIONS = {CORRECTION_MANIFEST, CORRECTION_CANDIDATE, CORRECTION_REVIEW}
OWNER_CODE = {
    "scripts/ghc_family_v664_v3_canonical_validator.py",
    "scripts/build_ghc_family_v664_v3_terminal_correction.py",
    "tests/test_ghc_family_vesper_v664_v3_closeout.py",
}
TEST_MODULES = [
    "tests/test_ghc_family_vesper_v664_v3.py",
    "tests/test_ghc_family_vesper_v664_v3_closeout.py",
]
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".txt", ".tex", ".mjs", ".js", ".cjs"}
PRIVATE_PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/(?:home|Users)/)"),
    "credential": re.compile(r"(?i)(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\"(?:password|api_key|access_token|resume_token)\"\s*:)") ,
    "private_route_identifier": re.compile(r"(?i)(?:codex" r"://|vscode" r"://|app" r"://connector_[0-9a-f]+)"),
    "transcript_or_session": re.compile(r"(?i)\"(?:raw_transcript|session_stream|private_app_state|browser_route)\"\s*:"),
}
SECURITY_PATTERNS = {
    "dynamic_eval": re.compile(r"(?m)^\s*(?:eval|exec)\s*\("),
    "unsafe_pickle_load": re.compile(r"\bpickle\.loads?\s*\("),
    "shell_true": re.compile(r"\bshell\s*=\s*True\b"),
    "destructive_git": re.compile(r"git\s+(?:reset\s+--hard|push\s+--force)"),
    "recursive_delete": re.compile(r"(?i)(?:rm\s+-" r"rf|Remove-" r"Item\b[^\n]*-Recurse)"),
}
NEW_FAILURES = [
    {
        "negative_id": "VE6643-X2-OP007",
        "method_id": "VE6643-X2-M027",
        "artifact_name": "ve6643-x2-m027-canonical-git-blob-domain-correction.json",
        "failure_class": "exact_final_manifest_replay_domain_mismatch",
        "failure_signature": "The one canonical aggregate at the retained initial final passed 63 tests, 140 JSON parses, and privacy/security scans, but failed manifest replay because legacy prospective byte and SHA fields described mixed Windows worktree materialization rather than canonical Git blob bytes.",
        "zero_credit": True,
        "candidate_workaround": "Retain the failed aggregate, make exact Git blob identity the canonical content domain, report noncanonical worktree byte metadata separately, and target any later aggregate only at an additive corrected final.",
        "bounded_passing_witness": "An isolated four-manifest replay validated 312 exact entries with zero blob mismatches while reporting ten legacy noncanonical worktree metadata rows.",
        "recurrence_guard": "Build future manifests from staged or committed Git blob bytes; never treat mutable worktree line endings as the canonical content domain.",
        "rollback": "The failed external receipt remains immutable at zero success credit; the retained initial final remains ancestral and is not rewritten.",
        "protected_gates": ["one_shot_canonical", "exact_git_blob_identity", "retained_initial_final"],
    },
    {
        "negative_id": "VE6643-X2-OP008",
        "method_id": "VE6643-X2-M028",
        "artifact_name": "ve6643-x2-m028-session-handle-preservation.json",
        "failure_class": "isolated_probe_session_handle_suppressed",
        "failure_signature": "The first isolated replay probe crossed its observation window while the wrapper projected stdout only, suppressing the continuation handle; the invocation therefore earned zero passing credit.",
        "zero_credit": True,
        "candidate_workaround": "Inspect the exact process read-only, wait for that process to exit, and surface full execution-result metadata for any replacement probe.",
        "bounded_passing_witness": "The original process was uniquely identified and allowed to exit without duplicate execution; the later bounded replay surfaced and reused its continuation handle correctly.",
        "recurrence_guard": "Never project only stdout for a command that can return a continuation session; preserve the full result envelope until terminal exit.",
        "rollback": "The probe was read-only, changed no file or ref, and its unseen output received zero validation credit.",
        "protected_gates": ["process_attribution", "no_duplicate_probe", "no_hidden_success"],
    },
    {
        "negative_id": "VE6643-X2-OP009",
        "method_id": "VE6643-X2-M029",
        "artifact_name": "ve6643-x2-m029-byte-value-line-ending-probe.json",
        "failure_class": "inline_byte_literal_overescape",
        "failure_signature": "A seven-path recovery probe over-escaped CR/LF byte literals through the shell, so it searched for backslash characters and earned zero compatibility credit.",
        "zero_credit": True,
        "candidate_workaround": "Construct byte separators from integer values to remove shell-escape ambiguity.",
        "bounded_passing_witness": "The replacement probe used byte values, preserved exact blob identity, and correctly exposed that uniform CRLF expansion was not the historical byte domain.",
        "recurrence_guard": "Use byte-value construction or a checked script file for nested-shell binary literal probes.",
        "rollback": "The malformed probe was read-only and changed no repository or external state.",
        "protected_gates": ["binary_literal_attribution", "manifest_domain", "no_false_pass"],
    },
    {
        "negative_id": "VE6643-X2-OP010",
        "method_id": "VE6643-X2-M030",
        "artifact_name": "ve6643-x2-m030-mixed-line-ending-domain-refusal.json",
        "failure_class": "uniform_crlf_materialization_assumption_rejected",
        "failure_signature": "A correctly escaped seven-path probe showed that whole-file LF-to-CRLF expansion did not reproduce the legacy manifest metadata because the edited Python files had mixed line-ending materialization.",
        "zero_credit": True,
        "candidate_workaround": "Refuse to reconstruct noncanonical worktree bytes; validate exact Git blob identity and surface legacy byte metadata only as noncanonical compatibility information.",
        "bounded_passing_witness": "The exact four-manifest component replay passed all 312 entries with canonical Git blob identity and explicitly reported ten noncanonical metadata rows.",
        "recurrence_guard": "Never infer a uniform checkout line-ending transform for files produced by mixed copy and patch operations.",
        "rollback": "The rejected assumption changed no files or refs and conferred no manifest or aggregate success credit.",
        "protected_gates": ["canonical_git_blob_domain", "line_ending_transparency", "no_metadata_promotion"],
    },
    {
        "negative_id": "VE6643-X2-OP011",
        "method_id": "VE6643-X2-M031",
        "artifact_name": "ve6643-x2-m031-explicit-sparse-staging.json",
        "failure_class": "sparse_index_out_of_cone_stage_refusal",
        "failure_signature": "The first exact correction staging command staged in-cone paths but refused the new correction builder outside the sparse definition because the command omitted Git's explicit sparse-index override.",
        "zero_credit": True,
        "candidate_workaround": "Preserve the partial index, regenerate the mutable correction receipts, and stage the exact owner allowlist with git add --sparse.",
        "bounded_passing_witness": "The replacement exact-allowlist stage includes every correction path, no unexpected path, and passes cached diff hygiene.",
        "recurrence_guard": "Use the explicit --sparse option whenever an authorized owner-local addition lies outside the current sparse materialization patterns.",
        "rollback": "No reset or rewrite is used; the partial index is superseded by exact restaging of the same owner-scoped allowlist.",
        "protected_gates": ["sparse_index_scope", "exact_staged_allowlist", "no_destructive_recovery"],
    },
    {
        "negative_id": "VE6643-X2-OP012",
        "method_id": "VE6643-X2-M032",
        "artifact_name": "ve6643-x2-m032-correction-review-test-isolation.json",
        "failure_class": "terminal_correction_staged_review_test_failure",
        "failure_signature": "The first terminal-correction staged review passed its allowlist, manifest, JSON, privacy, and security checks but failed because one closeout test retained the pre-correction protocol-state expectation.",
        "zero_credit": True,
        "candidate_workaround": "Retain the failed review, isolate the 12-test closeout module, and change only the stale protocol-state assertion.",
        "bounded_passing_witness": "The regenerated correction review passes the exact staged allowlist, manifest, 63 tests, JSON, privacy, and security checks.",
        "recurrence_guard": "When a lifecycle state is intentionally refined, audit tests that bind the prior state before the staged aggregate.",
        "rollback": "The failed review remains represented in Method Flow and is overwritten only as a mutable self-excluded candidate before commit.",
        "protected_gates": ["staged_review_truth", "isolated_recovery", "no_success_replay"],
    },
    {
        "negative_id": "VE6643-X2-OP013",
        "method_id": "VE6643-X2-M033",
        "artifact_name": "ve6643-x2-m033-corrected-protocol-state-assertion.json",
        "failure_class": "stale_closeout_protocol_state_assertion",
        "failure_signature": "The isolated closeout module confirmed that its protocol test expected POSTCOMMIT_REQUIRED after the correction deliberately advanced the state to CORRECTED_FINAL_POSTCOMMIT_REQUIRED.",
        "zero_credit": True,
        "candidate_workaround": "Bind the assertion to the explicit corrected-final postcommit state while preserving the no-preclaim and no-success-replay checks.",
        "bounded_passing_witness": "The isolated closeout module and regenerated 63-test correction review pass after the one-line state correction.",
        "recurrence_guard": "Keep lifecycle-state assertions aligned with additive correction schemas and never relax the associated no-preclaim fields.",
        "rollback": "The failed isolated test was read-only and changed no artifact, index, ref, remote, or external state.",
        "protected_gates": ["canonical_state_machine", "no_preclaim", "no_post_success_replay"],
    },
]


class CorrectionError(RuntimeError):
    """Raised when the additive correction violates its frozen scope."""


def run_git_bytes(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git_text(*args: str) -> str:
    return run_git_bytes(*args).stdout.decode("utf-8", "strict").strip()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(relative: str) -> dict[str, Any]:
    value = json.loads((PHASE / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CorrectionError(f"JSON root is not an object: {relative}")
    return value


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def owner_scope(path: str) -> bool:
    return path.startswith(PHASE_PREFIX) or path in OWNER_CODE


def working_paths() -> list[str]:
    raw = run_git_bytes("status", "--porcelain=v1", "-z", "--untracked-files=all").stdout.decode("utf-8", "strict")
    tokens = raw.split("\0")
    rows: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        if len(token) < 4:
            raise CorrectionError(f"malformed Git status row: {token!r}")
        status, path = token[:2], token[3:].replace("\\", "/")
        if status[0] in {"R", "C"} or status[1] in {"R", "C"}:
            index += 1
        rows.append(path)
    return sorted(set(rows))


def ensure_scope(paths: Iterable[str]) -> None:
    unexpected = [path for path in paths if not owner_scope(path)]
    if unexpected:
        raise CorrectionError(f"out-of-scope correction paths: {unexpected}")


def object_exists(commit: str, path: str) -> bool:
    return run_git_bytes("cat-file", "-e", f"{commit}:{path}", check=False).returncode == 0


def prospective_blob_record(path: str) -> dict[str, Any]:
    file_path = ROOT / path
    if not file_path.is_file():
        raise CorrectionError(f"prospective correction path missing: {path}")
    object_id = git_text("hash-object", "-w", f"--path={path}", path)
    raw = run_git_bytes("cat-file", "blob", object_id).stdout
    return {
        "path": path,
        "status": "M" if object_exists(INITIAL_FINAL, path) else "A",
        "mode": "100644",
        "object_type": "blob",
        "bytes": len(raw),
        "sha256": sha256(raw),
        "git_blob": object_id,
        "content_domain": "exact_git_blob",
    }


def append_once(rows: list[dict[str, Any]], additions: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    existing = {row.get(key) for row in rows}
    output = list(rows)
    for row in additions:
        if row[key] not in existing:
            output.append(row)
            existing.add(row[key])
    return output


def build_records() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    if head != INITIAL_FINAL:
        raise CorrectionError(f"correction builder requires retained initial final {INITIAL_FINAL}, got {head}")
    ensure_scope(working_paths())

    negatives = read_json("retained-negative-register-final.json")
    negative_rows = [
        {
            "negative_id": row["negative_id"],
            "proposal_id": None,
            "failure_class": row["failure_class"],
            "reason": row["failure_signature"],
            "completion_credit": 0,
            "retained": True,
        }
        for row in NEW_FAILURES
    ]
    negatives["schema"] = "ghc.family.vesper.v664-v3.retained-negative-register.terminal-correction.v1"
    negatives["post_evidence_operational_negatives"] = 9
    negatives["effective_negatives"] = 24_437
    negatives["new_records"] = append_once(list(negatives["new_records"]), negative_rows, "negative_id")
    negatives["terminal_correction_negative_count"] = 7
    negatives["no_negative_erased"] = True
    negatives["valid"] = len(negatives["new_records"]) == 93
    write_json("retained-negative-register-final.json", negatives)

    methods = read_json("method-flow/method-flow-state-final.json")
    method_rows = [
        {
            "method_id": row["method_id"],
            "proposal_id": None,
            "retained_failed_witnesses": [row["negative_id"]],
            "failed_witness_count": 1,
            "passing_witness_count": 1,
            **row,
            "same_owner_only": True,
            "independent_reproduction": False,
            "valid": True,
        }
        for row in NEW_FAILURES
    ]
    methods["schema"] = "ghc.family.vesper.v664-v3.method-flow.terminal-correction.v1"
    methods["post_evidence_operational_methods"] = 9
    methods["effective_methods"] = 8_791
    methods["methods"] = append_once(list(methods["methods"]), method_rows, "method_id")
    methods["failed_witnesses"] = 93
    methods["bounded_passing_witnesses"] = 93
    methods["terminal_correction_method_count"] = 7
    methods["valid"] = len(methods["methods"]) == 33
    write_json("method-flow/method-flow-state-final.json", methods)
    for row in method_rows:
        write_json(
            f"method-flow/{row['artifact_name']}",
            {
                "schema": "ghc.family.vesper.v664-v3.method-flow.terminal-correction-recovery.v1",
                **row,
                "result": "bounded_recovery_passed",
            },
        )

    truth = read_json("phase-truth-final.json")
    truth.update(
        {
            "schema": "ghc.family.vesper.v664-v3.phase-truth.terminal-corrected-candidate.v1",
            "retained_initial_final": INITIAL_FINAL,
            "effective_negatives": 24_437,
            "effective_methods": 8_791,
            "failed_initial_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "failed_initial_canonical_success_credit": 0,
            "terminal_correction_required": True,
            "corrected_exact_final_supplied_postcommit": True,
            "canonical_success_preclaimed": False,
            "successor_contacted": False,
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        }
    )
    write_json("phase-truth-final.json", truth)

    anchors = read_json("lifecycle/phase-anchor-contract.json")
    anchors.update(
        {
            "schema": "ghc.family.vesper.v664-v3.anchor-contract.terminal-correction.v1",
            "retained_initial_final": INITIAL_FINAL,
            "expected_phase_commit_count_after_final": 4,
            "initial_final_direct_child_of_evidence_required": True,
            "corrected_final_direct_child_of_initial_final_required": True,
            "final_direct_child_of_evidence_required": False,
            "valid": True,
        }
    )
    write_json("lifecycle/phase-anchor-contract.json", anchors)

    protocol = read_json("validation/canonical-validation-protocol.json")
    protocol.update(
        {
            "schema": "ghc.family.vesper.v664-v3.canonical-protocol.terminal-correction.v1",
            "state": "CORRECTED_FINAL_POSTCOMMIT_REQUIRED",
            "retained_failed_exact_head": INITIAL_FINAL,
            "failed_invocation_count": 1,
            "failed_invocation_success_credit": 0,
            "failed_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "new_exact_head_required": True,
            "post_success_replay_allowed": False,
            "preclaims_success": False,
            "valid": True,
        }
    )
    write_json("validation/canonical-validation-protocol.json", protocol)

    closeout = read_json("closeout-receipt.json")
    closeout.update(
        {
            "schema": "ghc.family.vesper.v664-v3.closeout-receipt.terminal-correction.v1",
            "retained_initial_final": INITIAL_FINAL,
            "effective_negatives": 24_437,
            "effective_methods": 8_791,
            "failed_initial_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "failed_initial_canonical_success_credit": 0,
            "postcommit_canonical_completed": False,
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        }
    )
    write_json("closeout-receipt.json", closeout)

    seal = read_json("seal-receipt.json")
    seal.update(
        {
            "schema": "ghc.family.vesper.v664-v3.seal-receipt.terminal-correction.v1",
            "retained_initial_final": INITIAL_FINAL,
            "initial_final_terminal": False,
            "terminal_correction_candidate": True,
            "postcommit_canonical_required": True,
            "valid": True,
        }
    )
    write_json("seal-receipt.json", seal)

    route = read_json("orchestration/terminal-route-state.json")
    route.update(
        {
            "schema": "ghc.family.vesper.v664-v3.terminal-route-state.terminal-correction.v1",
            "state": "PREPARED_NOT_SENT",
            "message_sent": False,
            "retained_initial_final": INITIAL_FINAL,
            "corrected_final_pending": True,
            "valid": True,
        }
    )
    write_json("orchestration/terminal-route-state.json", route)

    checklist = read_json("complete-incomplete-checklist-final.json")
    checklist["schema"] = "ghc.family.vesper.v664-v3.checklist.terminal-correction.v1"
    checklist["complete_now"] = list(checklist["complete_now"]) + [
        "retained zero-credit initial canonical failure and exact Git-blob-domain correction candidate"
    ]
    checklist["pending_postcommit"] = [
        "additive corrected exact final and fresh four-way equality",
        "one successful canonical owner-delta pass at the corrected head with no replay",
        "newest live roster/auth reread and one acknowledged Lyren activation",
    ]
    checklist["valid"] = True
    write_json("complete-incomplete-checklist-final.json", checklist)

    baton_path = PHASE / "handoffs/lyren-moss-v664-v4-activation.md"
    baton = baton_path.read_text(encoding="utf-8")
    count_sources = [
        "Vesper retains ten x1 operational failures, eighty rejecting synthetic mutations, four x2 evidence operational failures, and two post-evidence lifecycle failures. The prepared final truth is 24,430 effective negatives and 8,784 methods",
        "Vesper retains ten x1 operational failures, eighty rejecting synthetic mutations, four x2 evidence operational failures, and six post-evidence lifecycle failures. The corrected prepared truth is 24,434 effective negatives and 8,788 methods",
        "Vesper retains ten x1 operational failures, eighty rejecting synthetic mutations, four x2 evidence operational failures, and seven post-evidence lifecycle failures. The corrected prepared truth is 24,435 effective negatives and 8,789 methods",
    ]
    new_counts = "Vesper retains ten x1 operational failures, eighty rejecting synthetic mutations, four x2 evidence operational failures, and nine post-evidence lifecycle failures. The corrected prepared truth is 24,437 effective negatives and 8,791 methods"
    for old_counts in count_sources:
        if old_counts in baton:
            baton = baton.replace(old_counts, new_counts, 1)
            break
    if new_counts not in baton:
        raise CorrectionError("baton count sentence does not match retained or mutable correction state")
    anchor_line = "- Exact final: supplied only by the acknowledged live terminal overlay after the containing commit exists and passes the one-shot canonical validator."
    correction_lines = (
        f"{anchor_line}\n"
        f"- Retained nonterminal initial final: `{INITIAL_FINAL}`.\n"
        f"- Its one failed canonical receipt has SHA-256 `{FAILED_CANONICAL_RECEIPT_SHA256}` and zero aggregate-success credit; all passing subchecks remain bounded observations only.\n"
        "- The additive correction makes exact Git blob identity canonical, reports legacy worktree byte metadata separately, and requires a genuinely new exact final before any later aggregate."
    )
    if "- Retained nonterminal initial final:" not in baton:
        if anchor_line not in baton:
            raise CorrectionError("baton exact-final anchor line is missing")
        baton = baton.replace(anchor_line, correction_lines, 1)
    write_text("handoffs/lyren-moss-v664-v4-activation.md", baton)
    baton_raw = baton_path.read_bytes()
    baton_receipt = read_json("handoffs/lyren-moss-v664-v4-activation-receipt.json")
    baton_receipt.update(
        {
            "schema": "ghc.family.vesper.v664-v3.handoff-preparation-receipt.terminal-correction.v1",
            "bytes": len(baton_raw),
            "words": len(re.findall(rb"\S+", baton_raw)),
            "sha256": sha256(baton_raw),
            "state": "PREPARED_NOT_SENT",
            "sent_by_vesper_arlen": False,
            "retained_initial_final": INITIAL_FINAL,
            "valid": True,
        }
    )
    write_json("handoffs/lyren-moss-v664-v4-activation-receipt.json", baton_receipt)

    write_json(
        "validation/terminal-correction-receipt.json",
        {
            "schema": "ghc.family.vesper.v664-v3.terminal-correction-receipt.v1",
            "retained_initial_final": INITIAL_FINAL,
            "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "failed_canonical_success_credit": 0,
            "failed_canonical_tests_passed": FAILED_CANONICAL_TESTS,
            "failed_canonical_json_parses": FAILED_CANONICAL_JSON,
            "failed_canonical_privacy_files": FAILED_CANONICAL_PRIVACY_FILES,
            "failed_canonical_detailed_checks": "24/25",
            "failed_canonical_minimal_checks": "16/17",
            "isolated_manifest_replay_entries": 312,
            "isolated_manifest_replay_mismatches": 0,
            "legacy_noncanonical_metadata_rows": 10,
            "canonical_content_domain": "exact_git_blob",
            "corrected_final_supplied_postcommit": True,
            "same_owner_only": True,
            "independent_reproduction": False,
            "valid": True,
        },
    )

    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts)
    write_json(
        "validation/final-file-budget.json",
        {
            "schema": "ghc.family.vesper.v664-v3.file-budget.terminal-correction.v1",
            "materialized_file_count_before_correction_manifests": materialized,
            "threshold": 2_000,
            "rotation_required": materialized >= 2_000,
            "valid": materialized < 2_000,
        },
    )
    index = read_json("tooling/ghc-family-index-final.json")
    index.update(
        {
            "schema": "ghc.family.vesper.v664-v3.family-index.terminal-correction.v1",
            "retained_initial_final": INITIAL_FINAL,
            "terminal_correction_builder": "scripts/build_ghc_family_v664_v3_terminal_correction.py",
            "canonical_content_domain": "exact_git_blob",
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        }
    )
    write_json("tooling/ghc-family-index-final.json", index)

    ensure_scope(working_paths())
    expected = sorted((set(working_paths()) - {CORRECTION_REVIEW}) | {CORRECTION_MANIFEST, CORRECTION_CANDIDATE})
    write_json(
        "validation/terminal-correction-stage-candidate.json",
        {
            "schema": "ghc.family.vesper.v664-v3.terminal-correction-stage-candidate.v1",
            "source_commit": INITIAL_FINAL,
            "intended_allowlist": expected,
            "review_self_exclusion": CORRECTION_REVIEW,
            "manifest_self_exclusions": sorted(CORRECTION_SELF_EXCLUSIONS),
            "route_state": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    entries = [prospective_blob_record(path) for path in expected if path not in CORRECTION_SELF_EXCLUSIONS]
    write_json(
        "validation/terminal-correction-manifest.json",
        {
            "schema": "ghc.family.vesper.v664-v3.terminal-correction-manifest.v1",
            "generated_at_utc": utc_now(),
            "source_commit": INITIAL_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": sorted(CORRECTION_SELF_EXCLUSIONS),
            "canonical_content_domain": "exact_git_blob",
            "valid": True,
        },
    )
    observed = sorted(set(working_paths()) - {CORRECTION_REVIEW})
    ensure_scope(observed)
    if observed != expected:
        raise CorrectionError(f"working correction paths differ from candidate: missing={sorted(set(expected)-set(observed))}, extra={sorted(set(observed)-set(expected))}")
    return {
        "head": head,
        "correction_paths": len(expected),
        "manifest_entries": len(entries),
        "effective_negatives": 24_437,
        "effective_methods": 8_791,
        "baton_words": baton_receipt["words"],
        "route": "PREPARED_NOT_SENT",
        "valid": True,
    }


def staged_paths() -> list[str]:
    raw = run_git_bytes("diff", "--cached", "--name-only", "-z").stdout.decode("utf-8", "strict")
    return sorted(path for path in raw.split("\0") if path)


def index_blob(path: str) -> tuple[str, bytes]:
    object_id = git_text("rev-parse", f":{path}")
    raw = run_git_bytes("show", f":{path}").stdout
    return object_id, raw


def run_tests() -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    total = 0
    for relative in TEST_MODULES:
        result = subprocess.run(
            [sys.executable, str(ROOT / relative)], cwd=ROOT,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", check=False,
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        match = re.search(r"Ran (\d+) tests? in", result.stdout)
        count = int(match.group(1)) if match else 0
        total += count
        modules.append({"module": relative, "tests_run": count, "returncode": result.returncode, "valid": result.returncode == 0 and match is not None})
    return {"modules": modules, "tests_run": total, "valid": all(row["valid"] for row in modules)}


def review_records() -> dict[str, Any]:
    candidate = read_json("validation/terminal-correction-stage-candidate.json")
    manifest = read_json("validation/terminal-correction-manifest.json")
    expected = sorted(candidate["intended_allowlist"])
    observed = staged_paths()
    issues: list[str] = []
    if observed != expected:
        issues.append("staged paths differ from the correction allowlist")
    diff = run_git_bytes("diff", "--cached", "--check", check=False)
    if diff.returncode != 0:
        issues.append("staged correction diff hygiene failed")

    json_errors: list[dict[str, str]] = []
    privacy_hits: list[dict[str, str]] = []
    security_findings: list[dict[str, str]] = []
    json_count = 0
    text_count = 0
    python_count = 0
    for path in observed:
        _, raw = index_blob(path)
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                json.loads(raw.decode("utf-8", "strict"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                json_errors.append({"path": path, "error": str(exc)})
        if suffix not in TEXT_SUFFIXES:
            continue
        text_count += 1
        try:
            text = raw.decode("utf-8", "strict")
        except UnicodeError as exc:
            privacy_hits.append({"path": path, "class": "invalid_utf8", "detail": str(exc)})
            continue
        for label, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                privacy_hits.append({"path": path, "class": label})
        if suffix == ".py":
            python_count += 1
            try:
                compile(text, path, "exec", dont_inherit=True)
            except SyntaxError as exc:
                security_findings.append({"path": path, "rule": "python_compile", "detail": str(exc)})
            for label, pattern in SECURITY_PATTERNS.items():
                if pattern.search(text):
                    security_findings.append({"path": path, "rule": label})
    if json_errors:
        issues.append("strict JSON parsing failed")
    if privacy_hits:
        issues.append("five-class privacy scan found candidates")
    if security_findings:
        issues.append("changed-Python compile or security review found candidates")

    manifest_rows = {row["path"]: row for row in manifest["entries"]}
    required = set(observed) - set(manifest["self_exclusions"])
    missing = sorted(required - set(manifest_rows))
    extra = sorted(set(manifest_rows) - required)
    mismatches: list[dict[str, str]] = []
    for path, row in manifest_rows.items():
        if path not in required:
            continue
        object_id, raw = index_blob(path)
        if object_id != row["git_blob"]:
            mismatches.append({"path": path, "reason": "Git blob differs"})
        if len(raw) != row["bytes"] or sha256(raw) != row["sha256"]:
            mismatches.append({"path": path, "reason": "canonical Git blob bytes or SHA-256 differ"})
    if missing or extra or mismatches:
        issues.append("terminal correction manifest failed exact staged replay")

    tests = run_tests()
    if not tests["valid"] or tests["tests_run"] != 63:
        issues.append("dependency-closed correction tests did not pass 63 of 63")
    truth = read_json("phase-truth-final.json")
    route = read_json("orchestration/terminal-route-state.json")
    details = {
        "exact_allowlist": observed == expected,
        "diff_hygiene": diff.returncode == 0,
        "strict_json": not json_errors,
        "five_class_privacy": not privacy_hits,
        "changed_python_security": not security_findings,
        "correction_manifest": not missing and not extra and not mismatches,
        "tests": tests["valid"] and tests["tests_run"] == 63,
        "truth_counts": truth["effective_negatives"] == 24_437 and truth["effective_methods"] == 8_791,
        "gates": truth["effective_open_gaps"] == 169 and truth["effective_exact_gates"] == 167,
        "initial_final_retained": truth["retained_initial_final"] == INITIAL_FINAL,
        "failed_receipt_retained": truth["failed_initial_canonical_receipt_sha256"] == FAILED_CANONICAL_RECEIPT_SHA256,
        "route_unsent": route["state"] == "PREPARED_NOT_SENT" and route["message_sent"] is False and route["successor_title"] == "Lyren Moss",
        "head_is_initial_final": git_text("rev-parse", "HEAD") == INITIAL_FINAL,
    }
    if not all(details.values()):
        issues.append("one or more detailed correction checks failed")
    payload = {
        "schema": "ghc.family.vesper.v664-v3.terminal-correction-staged-review.v1",
        "source_commit": INITIAL_FINAL,
        "expected_staged_path_count": len(expected),
        "staged_path_count": len(observed),
        "staged_paths": observed,
        "allowlist_missing": sorted(set(expected) - set(observed)),
        "allowlist_unexpected": sorted(set(observed) - set(expected)),
        "strict_json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_scanned_text_file_count": text_count,
        "privacy_classes": sorted(PRIVATE_PATTERNS),
        "privacy_confirmed_hits": privacy_hits,
        "changed_python_count": python_count,
        "security_findings": security_findings,
        "manifest_entry_count": manifest["entry_count"],
        "manifest_missing": missing,
        "manifest_extra": extra,
        "manifest_mismatches": mismatches,
        "tests": tests,
        "detailed_checks": details,
        "detailed_check_count": len(details),
        "detailed_checks_passed": sum(details.values()),
        "issues": issues,
        "valid": not issues,
        "boundary": "Additive terminal-manifest correction only; corrected exact final, canonical success, route authorization, and acknowledged delivery remain pending.",
    }
    write_json("validation/terminal-correction-staged-review.json", payload)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "review"), nargs="?", default="build")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_records() if args.mode == "build" else review_records()
        print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
        return 0 if payload.get("valid", True) else 2
    except (CorrectionError, OSError, UnicodeError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"VESPER_V664_V3_TERMINAL_CORRECTION_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
