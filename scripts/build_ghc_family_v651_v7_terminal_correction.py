#!/usr/bin/env python3
"""Build the additive Vesper v651-v7 terminal-validation correction."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"
SOURCE = "2500d063583194b30f01da429196522baaac7300"
X1 = "d55689f393292cea76f8d568d69da27c8f7b3bd6"
EVIDENCE = "78f4014c7d10d59d05f95e872ece4d52027a7a7b"
FAILED_SEAL = "12a767989aba8dc1a4c2f506561a95b1181d23a6"
NEGATIVES = 7458
OPEN_GAPS = 59
EXACT_GATES = 60
OWNER_GLOBALS = {
    "scripts/build_ghc_family_v651_v7_preregistration.py",
    "scripts/build_ghc_family_v651_v7_evidence.py",
    "scripts/build_ghc_family_v651_v7_tools.py",
    "scripts/build_ghc_family_v651_v7_closeout.py",
    "scripts/build_ghc_family_v651_v7_terminal_correction.py",
    "scripts/ghc_family_v651_v7_runtime.py",
    "scripts/ghc_family_v651_v7_detailed_validator.py",
    "scripts/ghc_family_v651_v7_minimal_validator.py",
    "scripts/ghc_family_v651_v7_final_validator.py",
    "scripts/ghc_family_concurrency_reclamation.py",
    "scripts/ghc_family_conditional_update.py",
    "scripts/ghc_family_identity_accessibility_proxy.py",
    "scripts/ghc_family_integrity_range.py",
    "scripts/ghc_family_numerical_boundary.py",
    "scripts/ghc_family_schema_cache_concurrency.py",
    "scripts/ghc_family_stage20_authority_refusal.py",
    "scripts/ghc_family_storage_reclamation.py",
    "scripts/ghc_family_time_rate_fairness.py",
    "scripts/ghc_family_transaction_checkpoint.py",
    "tests/test_ghc_family_v651_v7_x1.py",
    "tests/test_ghc_family_v651_v7_x2.py",
    "tests/test_ghc_family_v651_v7_closeout.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    ).strip()


def write_json(relative: str, payload: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def status_paths() -> list[str]:
    paths: list[str] = []
    output = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    )
    for row in output.splitlines():
        if not row:
            continue
        relative = row[3:]
        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1]
        paths.append(relative.replace("\\", "/"))
    return sorted(set(paths))


def filtered_blob(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    content = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def write_correction_documents() -> tuple[int, int]:
    baton_path = ROOT / "handoffs/authorized-successor-v651-v8-pending-confirmation.md"
    baton = baton_path.read_text(encoding="utf-8")
    baton = baton.replace(
        "effective negative baseline is 7454:",
        "effective negative baseline is 7458:",
    ).replace(
        "effective negative baseline is 7457:",
        "effective negative baseline is 7458:",
    ).replace(
        "two closeout operational failures",
        "six closeout operational failures",
    ).replace(
        "five closeout operational failures",
        "six closeout operational failures",
    ).replace(
        "Both failures receive zero credit.",
        "A correction-stage test then conflated the immutable two-method closeout ledger with the correction ledger and failed one of sixty-nine tests. All three later failures receive zero credit.",
    ).replace(
        "These three terminal failures raise the effective baseline to 7,457: 7,338 inherited, five x1 operational, nine x2 operational, five closeout or correction operational, and one hundred rejecting synthetic mutations.",
        "These four terminal failures raise the effective baseline to 7,458: 7,338 inherited, five x1 operational, nine x2 operational, six closeout or correction operational, and one hundred rejecting synthetic mutations.",
    )
    marker = "## Terminal-validation correction"
    if marker not in baton:
        baton += f"""

## Terminal-validation correction

The first canonical exact-head validation at {FAILED_SEAL} received zero credit. Its exact Git-blob manifests, 151 JSON parses, 203-file five-class privacy scan, 39 detailed checks, and 14 minimal checks passed, but its unit-test loader ran before the repository root was placed on the Python import path. It therefore executed three import-error placeholders rather than the expected phase tests. The correction moves repository-root insertion before test discovery and preserves the failed receipt externally and in a sanitized repository summary.

A later read-only diagnostic also failed before inspection because a PowerShell regular-expression argument was not transport-safe quoted. The first correction-builder invocation then failed closed because a trimmed porcelain-status helper removed the leading status-space from the first path and misclassified it as out of scope. A correction-stage test then conflated the immutable two-method closeout ledger with the correction ledger and failed one of sixty-nine tests. All three later failures receive zero credit. The recoveries use a simple quoted file read, exact line ranges, untrimmed positional parsing, and lifecycle-specific assertions. These four terminal failures raise the effective baseline to 7,458: 7,338 inherited, five x1 operational, nine x2 operational, six closeout or correction operational, and one hundred rejecting synthetic mutations.

The correction adds no scientific, empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 credit. The old seal remains immutable and ancestral. The corrected exact head must be a single-parent child of that failed seal, stay within the six-commit phase cap, be pushed and four-way equal, and pass one justified recovery validation. A successful recovery is terminal and must not be replayed.
"""
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"corrected baton words outside contract: {baton_words}")
    write_text("handoffs/authorized-successor-v651-v8-pending-confirmation.md", baton)
    overview_path = ROOT / "overview/final-integrated-overview.md"
    overview = overview_path.read_text(encoding="utf-8")
    overview = overview.replace(
        "A separate misquoted PowerShell diagnostic and one fail-closed porcelain-status parsing defect are also retained at zero credit.",
        "A separate misquoted PowerShell diagnostic, one fail-closed porcelain-status parsing defect, and one lifecycle-ledger assertion defect are also retained at zero credit.",
    ).replace(
        "effective negative baseline to 7,457",
        "effective negative baseline to 7,458",
    )
    overview_marker = "# Terminal-validation correction"
    if overview_marker not in overview:
        overview += f"""

# Terminal-validation correction

The first canonical exact-head validation at {FAILED_SEAL} is retained at zero credit because test discovery ran before the repository root entered the Python import path. All non-test canonical surfaces reported passing evidence, but three import-error placeholders are not the expected phase suite. A separate misquoted PowerShell diagnostic, one fail-closed porcelain-status parsing defect, and one lifecycle-ledger assertion defect are also retained at zero credit. The additive correction fixes only those workflow defects, raises the effective negative baseline to 7,458, preserves 59 open gaps and 60 exact gates, and keeps the route PREPARED_NOT_SENT. It adds no scientific result and does not launch or name any future CLI seat.
"""
    overview_words = len(overview.split())
    if not 3000 <= overview_words <= 100000:
        raise RuntimeError(f"corrected overview words outside contract: {overview_words}")
    write_text("overview/final-integrated-overview.md", overview)
    write_json(
        "truth/corrected-final-phase-truth.json",
        {
            "schema": "ghc.family.v651-v7.corrected-final-truth.v1",
            "owner": "Vesper Arlen",
            "phase": "v651-gmut-thos-v7-x1-x2",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "failed_seal": FAILED_SEAL,
            "outcomes": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
            "effective_negatives": NEGATIVES,
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "real_data_rows": 0,
            "participants": 0,
            "real_keys_or_tokens": 0,
            "authority_decisions": 0,
            "production_actions": 0,
            "future_cli_seats_named": 0,
            "future_cli_seats_launched": 0,
            "independent_reproduction": False,
            "same_owner_only": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "truth/corrected-final-negative-register.json",
        {
            "schema": "ghc.family.v651-v7.corrected-final-negative-register.v1",
            "inherited_effective": 7338,
            "x1_operational": 5,
            "x2_operational": 9,
            "closeout_operational": 6,
            "synthetic_rejecting_mutations": 100,
            "effective_total": NEGATIVES,
            "correction_failures": [
                {
                    "negative_id": "V6517-CORR-N01",
                    "failure": "The first canonical test loader ran before the repository root entered Python import search and executed three import-error placeholders.",
                    "recovery": "Insert the repository root before loading test modules and require the exact expected test count.",
                },
                {
                    "negative_id": "V6517-CORR-N02",
                    "failure": "A read-only PowerShell diagnostic used a misquoted regular-expression argument and failed before reading the validator.",
                    "recovery": "Use a transport-safe quoted file read and exact line ranges for the diagnostic.",
                },
                {
                    "negative_id": "V6517-CORR-N03",
                    "failure": "The first correction builder trimmed leading whitespace from porcelain status and misclassified the first owner path as out of scope.",
                    "recovery": "Read porcelain output without global trimming and preserve its two status columns before slicing the path.",
                },
                {
                    "negative_id": "V6517-CORR-N04",
                    "failure": "The first correction-stage test expected the expanded correction count from the immutable closeout ledger and the old correction count from the correction ledger.",
                    "recovery": "Bind the sealed closeout assertion to two methods and the expanded correction assertion to four methods.",
                },
            ],
            "failures_erased": 0,
            "valid": True,
        },
    )
    methods = [
        {
            "method_id": "V6517-M17",
            "title": "Establish repository import roots before unittest discovery",
            "state": "preferred",
            "failure_signature": "A script launched from the scripts directory asks unittest to import repository-root test modules before adding the repository root to sys.path.",
            "candidate_workaround": "Insert the repository root before test discovery and require the exact expected test count.",
            "recurrence_guard": "Canonical validators must establish import roots before loading any repository test module.",
            "rollback": "Retain the failed canonical receipt at zero credit and use one additive correction commit.",
            "scope_boundary": "Validation-loader recovery only; no scientific, production, independent-reproduction, or authority credit.",
        },
        {
            "method_id": "V6517-M18",
            "title": "Use transport-safe quoted diagnostic patterns",
            "state": "preferred",
            "failure_signature": "A PowerShell diagnostic embeds a double quote inside an already double-quoted regular expression.",
            "candidate_workaround": "Use a simple quoted path read or a single-quoted pattern with no transport ambiguity.",
            "recurrence_guard": "Preflight shell quoting before diagnostic execution and prefer exact line-range reads.",
            "rollback": "Retain the read-only failure at zero credit; no repository rollback is required.",
            "scope_boundary": "Read-only diagnostic recovery only; no scientific, production, independent-reproduction, or authority credit.",
        },
        {
            "method_id": "V6517-M19",
            "title": "Preserve porcelain status columns before path parsing",
            "state": "preferred",
            "failure_signature": "A helper globally strips Git porcelain output and removes the leading status-space from the first line.",
            "candidate_workaround": "Read raw porcelain lines without global trimming, then remove exactly the two status columns and separator.",
            "recurrence_guard": "Never apply strip to positional Git porcelain output before parsing.",
            "rollback": "Retain the fail-closed refusal at zero credit; no generated artifact was accepted.",
            "scope_boundary": "Owner-local status parsing recovery only; no scientific, production, independent-reproduction, or authority credit.",
        },
        {
            "method_id": "V6517-M20",
            "title": "Keep lifecycle-ledger assertions phase specific",
            "state": "preferred",
            "failure_signature": "A test applies the correction Method Flow count to the immutable closeout ledger and the stale correction count to the current correction ledger.",
            "candidate_workaround": "Assert each immutable lifecycle ledger against its own frozen count and update only the additive correction assertion.",
            "recurrence_guard": "Label every derived count with its exact lifecycle artifact before changing tests.",
            "rollback": "Retain the failed correction-stage test at zero credit and rebuild only additive correction artifacts.",
            "scope_boundary": "Lifecycle assertion recovery only; no scientific, production, independent-reproduction, or authority credit.",
        },
    ]
    witnesses = [
        {
            "witness_id": "V6517-M17-WFAIL",
            "method_id": "V6517-M17",
            "result": "fail",
            "observed": "Three test-module import errors at the first canonical head.",
            "credit": "zero",
        },
        {
            "witness_id": "V6517-M17-WPASS",
            "method_id": "V6517-M17",
            "result": "pass",
            "observed": "The corrected loader established the repository root before discovering all phase tests.",
            "credit": "bounded validation recovery only",
        },
        {
            "witness_id": "V6517-M18-WFAIL",
            "method_id": "V6517-M18",
            "result": "fail",
            "observed": "The misquoted diagnostic failed before file inspection.",
            "credit": "zero",
        },
        {
            "witness_id": "V6517-M18-WPASS",
            "method_id": "V6517-M18",
            "result": "pass",
            "observed": "The exact line-range read returned the intended validator sections without parsing ambiguity.",
            "credit": "bounded diagnostic recovery only",
        },
        {
            "witness_id": "V6517-M19-WFAIL",
            "method_id": "V6517-M19",
            "result": "fail",
            "observed": "The first modified scripts path lost its initial letter and triggered an out-of-scope refusal.",
            "credit": "zero",
        },
        {
            "witness_id": "V6517-M19-WPASS",
            "method_id": "V6517-M19",
            "result": "pass",
            "observed": "The untrimmed parser preserved every owner path and admitted only the exact correction scope.",
            "credit": "bounded status parsing recovery only",
        },
        {
            "witness_id": "V6517-M20-WFAIL",
            "method_id": "V6517-M20",
            "result": "fail",
            "observed": "One of sixty-nine correction-stage tests failed because closeout and correction counts were reversed.",
            "credit": "zero",
        },
        {
            "witness_id": "V6517-M20-WPASS",
            "method_id": "V6517-M20",
            "result": "pass",
            "observed": "The recovered test preserved the immutable closeout count and verified the expanded correction count separately.",
            "credit": "bounded lifecycle assertion recovery only",
        },
    ]
    for index, method in enumerate(methods):
        number = 17 + index
        write_json(f"method-flow/correction-records/m{number}-method.json", method)
        write_json(f"method-flow/correction-records/m{number}-fail.json", witnesses[index * 2])
        write_json(f"method-flow/correction-records/m{number}-pass.json", witnesses[index * 2 + 1])
    write_json(
        "method-flow/correction-summary.json",
        {
            "schema": "ghc.family.v651-v7.correction-method-flow.v1",
            "methods": 4,
            "failed_witnesses": 4,
            "passing_witnesses": 4,
            "preferred_methods": 4,
            "failure_erased": False,
            "methods_detail": methods,
            "witnesses": witnesses,
            "valid": True,
        },
    )
    write_json(
        "validation/failed-canonical-receipt-summary.json",
        {
            "schema": "ghc.family.v651-v7.failed-canonical-summary.v1",
            "failed_head": FAILED_SEAL,
            "tests_run": 3,
            "test_errors": 3,
            "test_failures": 0,
            "detailed": "39/39",
            "minimal": "14/14",
            "json": "151/151",
            "privacy_files": 203,
            "privacy_confirmed_hits": 0,
            "manifest_checks_passed": True,
            "json_parses_passed": True,
            "privacy_scan_passed": True,
            "credit": "zero",
            "failure_retained": True,
            "valid": True,
        },
    )
    write_json(
        "validation/terminal-correction-receipt.json",
        {
            "schema": "ghc.family.v651-v7.terminal-correction.v1",
            "failed_head": FAILED_SEAL,
            "failed_canonical_credit": "zero",
            "correction_scope": [
                "repository import root before unittest discovery",
                "exact expected test-count requirement",
                "transport-safe diagnostic quoting",
                "corrected negative and Method Flow continuity",
            ],
            "scientific_result_added": False,
            "route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "seal/terminal-correction-seal.json",
        {
            "schema": "ghc.family.v651-v7.terminal-correction-seal.v1",
            "expected_parent": FAILED_SEAL,
            "single_parent_required": True,
            "phase_commit_count_expected": 4,
            "phase_commit_cap": 6,
            "zero_merges_required": True,
            "canonical_recovery_allowed_once": True,
            "scientific_result_added": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "checklists/corrected-final-complete-incomplete.json",
        {
            "schema": "ghc.family.v651-v7.corrected-checklist.v1",
            "completed": [
                "failed canonical receipt retained at zero credit",
                "test discovery import root corrected",
                "diagnostic quoting recurrence guard recorded",
                "correction manifests prepared",
                "baton and overview baseline corrected",
            ],
            "incomplete": [
                "successful one-pass exact-head canonical recovery",
                "exact live successor confirmation",
                "acknowledged successor send",
                "eight future CLI launch preflights",
                "independent reproduction",
                "Stage 20 readiness",
            ],
            "route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "orchestration/corrected-final-phase-state.json",
        {
            "schema": "ghc.family.v651-v7.corrected-final-state.v1",
            "owner": "Vesper Arlen",
            "failed_head": FAILED_SEAL,
            "state_at_commit": "TERMINAL_CORRECTION_PREPARED",
            "canonical_recovery": "PENDING_EXTERNAL_EXACT_HEAD_RECEIPT",
            "route": "PREPARED_NOT_SENT",
            "future_cli": "PREPARED_NOT_LAUNCHED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    return baton_words, overview_words


def build_manifests(baton_words: int, overview_words: int) -> tuple[int, int]:
    exclusions = [
        "docs/vesper-arlen/v651-v7/validation/correction-staged-manifest.json",
        "docs/vesper-arlen/v651-v7/validation/correction-staged-privacy.json",
        "docs/vesper-arlen/v651-v7/validation/correction-staged-review.json",
        "docs/vesper-arlen/v651-v7/validation/corrected-owner-manifest.json",
        "docs/vesper-arlen/v651-v7/validation/correction-build-receipt.json",
    ]
    paths = [
        path
        for path in status_paths()
        if path not in exclusions and (REPO / path).is_file()
    ]
    out_of_scope = [
        path
        for path in paths
        if not (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
    ]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope correction paths: {out_of_scope}")
    entries = [filtered_blob(path) for path in paths]
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/]"),
        "private_uri": re.compile(r"(?i)\b(?:codex|thread|task|app|plugin)://"),
        "delegation_markup": re.compile(r"(?i)<codex_delegation"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{8,}"),
    }
    definitions = {
        "scripts/build_ghc_family_v651_v7_preregistration.py",
        "scripts/build_ghc_family_v651_v7_evidence.py",
        "scripts/build_ghc_family_v651_v7_closeout.py",
        "scripts/build_ghc_family_v651_v7_terminal_correction.py",
        "scripts/ghc_family_v651_v7_final_validator.py",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        text = (REPO / relative).read_text(encoding="utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    write_json(
        "validation/correction-staged-privacy.json",
        {
            "schema": "ghc.family.v651-v7.correction-privacy.v1",
            "scanned_file_count": len(paths),
            "pattern_classes": sorted(patterns),
            "candidate_count": len(candidates),
            "candidates": candidates,
            "confirmed_hit_count": 0,
            "confirmed_hits": [],
            "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
        },
    )
    write_json(
        "validation/correction-staged-manifest.json",
        {
            "schema": "ghc.family.v651-v7.correction-staged-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": exclusions,
            "coverage_boundary": "All intended correction paths except five declared manifest outputs.",
        },
    )
    write_json(
        "validation/correction-staged-review.json",
        {
            "schema": "ghc.family.v651-v7.correction-staged-review.v1",
            "intended_path_count": len(entries) + len(exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(exclusions),
            "out_of_scope_paths": [],
            "privacy_confirmed_hits": 0,
            "expected_parent": FAILED_SEAL,
            "route": "PREPARED_NOT_SENT",
            "baton_words": baton_words,
            "overview_words": overview_words,
            "valid": True,
        },
    )
    receipt_path = "docs/vesper-arlen/v651-v7/validation/correction-build-receipt.json"
    tracked = set(git("ls-files").splitlines())
    prospective = tracked | set(status_paths()) | {receipt_path}
    prospective_owner = {
        path
        for path in prospective
        if (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
        and path != "docs/vesper-arlen/v651-v7/validation/corrected-owner-manifest.json"
    }
    owner_count = len(prospective_owner) + 1
    write_json(
        "validation/correction-build-receipt.json",
        {
            "schema": "ghc.family.v651-v7.correction-build.v1",
            "failed_head": FAILED_SEAL,
            "baton_words": baton_words,
            "overview_words": overview_words,
            "correction_manifest_entries": len(entries),
            "correction_manifest_self_exclusions": len(exclusions),
            "owner_files": owner_count,
            "effective_negatives": NEGATIVES,
            "route": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    current = tracked | set(status_paths())
    owner_paths = sorted(
        path
        for path in current
        if (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
        and (REPO / path).is_file()
        and path != "docs/vesper-arlen/v651-v7/validation/corrected-owner-manifest.json"
    )
    owner_entries = [filtered_blob(path) for path in owner_paths]
    write_json(
        "validation/corrected-owner-manifest.json",
        {
            "schema": "ghc.family.v651-v7.corrected-owner-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": ["docs/vesper-arlen/v651-v7/validation/corrected-owner-manifest.json"],
            "owner_file_count": len(owner_entries) + 1,
            "file_threshold": 2000,
            "below_threshold": len(owner_entries) + 1 < 2000,
        },
    )
    return len(entries), len(owner_entries)


def main() -> None:
    if git("rev-parse", "HEAD") != FAILED_SEAL:
        raise RuntimeError(f"correction builder requires failed seal {FAILED_SEAL}")
    if any(
        not (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
        for path in status_paths()
    ):
        raise RuntimeError("correction builder refuses out-of-scope pre-existing changes")
    baton_words, overview_words = write_correction_documents()
    correction_entries, owner_entries = build_manifests(baton_words, overview_words)
    print(
        json.dumps(
            {
                "built": True,
                "failed_head": FAILED_SEAL,
                "baton_words": baton_words,
                "overview_words": overview_words,
                "correction_manifest_entries": correction_entries,
                "owner_manifest_entries": owner_entries,
                "effective_negatives": NEGATIVES,
                "route": "PREPARED_NOT_SENT",
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
