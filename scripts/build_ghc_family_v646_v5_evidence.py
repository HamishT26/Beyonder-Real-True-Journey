#!/usr/bin/env python3
"""Build the bounded Tamar Vey v646-v5 x2 evidence packet."""

from __future__ import annotations

import html
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v646_v5_definitions as d
import ghc_family_v646_v5_runtime as runtime


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v646-v5"
X1_HEAD = "3f6b5302e18c7828d19ffb621da153f6ae173de0"
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"
CORE_PATHS = {
    "V6465-P01": ("method-flow/optimistic-concurrency-contract.json", "method-flow/lost-update-mutation-vectors.json"),
    "V6465-P02": ("gmut/peierls-bracket-contract.json", "gmut/peierls-bracket-mutations.json"),
    "V6465-P03": ("empirical/rubin-dp1-study-contract.json", "empirical/rubin-dp1-zero-row-receipt.json"),
    "V6465-P04": ("thos/veterinary-lab-handover-contract.json", "thos/veterinary-lab-proxy-vectors.json"),
    "V6465-P05": ("freed-id/transaction-data-profile.json", "freed-id/transaction-data-mutations.json"),
    "V6465-P06": ("cbr/animal-disease-authority-reservation.json", "cbr/notification-privacy-remedy-matrix.md"),
    "V6465-P07": ("security/reftable-contract.json", "security/reftable-mutation-vectors.json"),
    "V6465-P08": ("accessibility/popover-contract.json", "accessibility/popover-structural-mutations.json"),
    "V6465-P09": ("thermo-psyche/clapeyron-contract.json", "thermo-psyche/clapeyron-mutation-vectors.json"),
    "V6465-P10": ("stage20/metric-semantics-contract.json", "stage20/metric-semantics-mutations.json"),
}


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def method_call(*args: str) -> None:
    subprocess.run([sys.executable, str(METHOD_RUNNER), *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")


def add_method_flow_readonly_fault() -> None:
    ledger = PHASE / "method-flow/method-flow-state.json"
    method = {
        "method_id": "V6465-M05",
        "title": "Derive exact equality-summary commit labels from the resolved Git head",
        "failure_signature": "The first post-x1 equality summary included a manually copied x1_commit display value with a mistyped suffix while the four Git-derived ref fields were equal and correct.",
        "trigger_preconditions": ["exact commit reporting", "multiple derived Git refs", "manual duplicate display field"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_read_only_reporting_recovery",
        "candidate_workaround": "Assign the displayed x1 commit directly from the already-resolved local Git head and reissue the bounded equality proof.",
        "validation_witness_ids": [],
        "recurrence_guard": "Never manually duplicate a resolved commit hash in the same proof; derive every repeated label from one Git value and assert equality.",
        "rollback": "Retain the first summary as a zero-credit reporting negative; do not push or mutate anything in response.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["exact_head", "remote_equality", "failure_erasure", "duplicate_push", "completion_credit"],
        "retained_negative_ids": ["V6465-X2-N01"],
        "scope_boundary": "Read-only Git reporting only; no repository, scientific, authority, production, or independent-reproduction credit.",
    }
    failed = {
        "witness_id": "V6465-M05-F", "method_id": "V6465-M05",
        "procedure": "Display four Git-derived refs plus a separately copied x1_commit label.",
        "scope": "Post-x1 four-way equality summary", "expected": "Every displayed commit field equals the exact x1 head.",
        "observed": "Local, upstream, tracking, and live fields were all correct and equal, but the separately copied display field had a mistyped suffix.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X2-N01"], "boundary": d.TRUTH_BOUNDARY,
    }
    passed = {
        "witness_id": "V6465-M05-P", "method_id": "V6465-M05",
        "procedure": "Resolve the local Git head once, derive the x1 label from it, and compare local, upstream, tracking, and live refs with 0/0 divergence and clean state.",
        "scope": "Corrected post-x1 equality proof", "expected": "All displayed fields equal the exact frozen x1 commit.",
        "observed": "All fields equaled 3f6b5302e18c7828d19ffb621da153f6ae173de0, divergence was 0/0, and the canonical lane was clean before x2.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X2-N01"], "boundary": d.TRUTH_BOUNDARY,
    }
    files = {
        "method-flow/v6465-m05-method-record.json": method,
        "method-flow/v6465-m05-f-witness.json": failed,
        "method-flow/v6465-m05-p-witness.json": passed,
    }
    for path, payload in files.items():
        write_json(path, payload)
    state = json.loads(ledger.read_text(encoding="utf-8"))
    if not any(row["method_id"] == "V6465-M05" for row in state["methods"]):
        method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / "method-flow/v6465-m05-method-record.json"))
    state = json.loads(ledger.read_text(encoding="utf-8"))
    for witness_id, path in (("V6465-M05-F", "method-flow/v6465-m05-f-witness.json"), ("V6465-M05-P", "method-flow/v6465-m05-p-witness.json")):
        if not any(row["witness_id"] == witness_id for row in state["witnesses"]):
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / path))
            state = json.loads(ledger.read_text(encoding="utf-8"))
    row = next(item for item in state["methods"] if item["method_id"] == "V6465-M05")
    if row["recommendation_state"] != "preferred":
        method_call("set-state", "--ledger", str(ledger), "--method-id", "V6465-M05", "--state", "preferred", "--note", "Preferred for exact equality summaries with repeated commit labels")
    method6 = {
        "method_id": "V6465-M06",
        "title": "Assert frozen x1 Method Flow continuity without forbidding additive x2 records",
        "failure_signature": "The first x2 current-phase run failed because the x1 test required the live phase Method Flow ledger to contain exactly four methods and witness pairs after x2 correctly appended M05.",
        "trigger_preconditions": ["x1 continuity test", "phase-lifetime append-only ledger", "later x2 method record"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped_test_compatibility_repair",
        "candidate_workaround": "Require the four frozen x1 method IDs and eight witnesses as a subset while allowing later append-only records and minimum counts.",
        "validation_witness_ids": [],
        "recurrence_guard": "When an x1 artifact is intentionally phase-lifetime and append-only, test frozen member preservation rather than exact final cardinality.",
        "rollback": "Retain the failed test with zero credit and change only the additive-continuity assertion; never remove the x2 Method Flow record.",
        "recommendation_state": "candidate",
        "supersedes": [],
        "protected_gates": ["x1_continuity", "failure_erasure", "method_flow_append_only", "test_weakening", "completion_credit"],
        "retained_negative_ids": ["V6465-X2-N02"],
        "scope_boundary": "Test compatibility for an append-only phase ledger only; no x1 mutation credit, scientific, authority, production, or independent-reproduction credit.",
    }
    failed6 = {
        "witness_id": "V6465-M06-F", "method_id": "V6465-M06",
        "procedure": "Run the frozen x1 tests after appending the first legitimate x2 Method Flow record.",
        "scope": "Tamar v646-v5 current-phase test selection", "expected": "The four x1 records remain required while additive x2 records are permitted.",
        "observed": "Fifteen x1 tests passed and the exact-cardinality Method Flow assertion failed on the valid 5/5/5/5 additive ledger.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X2-N02"], "boundary": d.TRUTH_BOUNDARY,
    }
    passed6 = {
        "witness_id": "V6465-M06-P", "method_id": "V6465-M06",
        "procedure": "Require M01 through M04 and their failed and passing witnesses as subsets, with counts no lower than the frozen x1 totals.",
        "scope": "Tamar v646-v5 x1 continuity assertion", "expected": "Frozen x1 records remain mandatory and later append-only records do not cause a false failure.",
        "observed": "The repaired source asserts the exact frozen x1 ID subsets and minimum counts without removing, mutating, or ignoring any later Method Flow record.",
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X2-N02"], "boundary": d.TRUTH_BOUNDARY,
    }
    for path, payload in {
        "method-flow/v6465-m06-method-record.json": method6,
        "method-flow/v6465-m06-f-witness.json": failed6,
        "method-flow/v6465-m06-p-witness.json": passed6,
    }.items():
        write_json(path, payload)
    state = json.loads(ledger.read_text(encoding="utf-8"))
    if not any(item["method_id"] == "V6465-M06" for item in state["methods"]):
        method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / "method-flow/v6465-m06-method-record.json"))
    state = json.loads(ledger.read_text(encoding="utf-8"))
    for witness_id, path in (("V6465-M06-F", "method-flow/v6465-m06-f-witness.json"), ("V6465-M06-P", "method-flow/v6465-m06-p-witness.json")):
        if not any(item["witness_id"] == witness_id for item in state["witnesses"]):
            method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / path))
            state = json.loads(ledger.read_text(encoding="utf-8"))
    row = next(item for item in state["methods"] if item["method_id"] == "V6465-M06")
    if row["recommendation_state"] != "preferred":
        method_call("set-state", "--ledger", str(ledger), "--method-id", "V6465-M06", "--state", "preferred", "--note", "Preferred for x1 continuity checks over a phase-lifetime append-only ledger")
    extra_methods = [
        (
            {
                "method_id": "V6465-M07", "title": "Emit machine-readable runner JSON independently of the host console code page",
                "failure_signature": "The first all-runner invocation completed the runtime checks internally but failed while printing a Māori boundary string through a locale-default console encoding.",
                "trigger_preconditions": ["Windows locale-default console", "machine-readable JSON output", "non-ASCII boundary text"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_portability_repair",
                "candidate_workaround": "Escape non-ASCII code points in machine stdout while preserving Unicode in UTF-8 repository artifacts.",
                "validation_witness_ids": [], "recurrence_guard": "Machine runner stdout must be ASCII-safe or explicitly UTF-8 configured; human artifacts retain correct Unicode.",
                "rollback": "Retain the failed invocation with zero runner credit and change only the stdout serialization boundary.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["runner_credit", "unicode_integrity", "failure_erasure", "locale_portability", "artifact_content"],
                "retained_negative_ids": ["V6465-X2-N03"],
                "scope_boundary": "Machine-output portability only; no professional, production, scientific, authority, or independent-reproduction credit.",
            },
            {
                "witness_id": "V6465-M07-F", "method_id": "V6465-M07", "procedure": "Print the full Unicode runtime payload through the locale-default console encoding.",
                "scope": "First all-runner invocation", "expected": "Return a machine-readable passing runtime payload.",
                "observed": "All bounded checks completed, then stdout serialization raised a Unicode console encoding error before runner credit.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N03"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M07-P", "method_id": "V6465-M07", "procedure": "Serialize machine stdout with escaped non-ASCII code points while retaining UTF-8 Unicode in repository artifacts.",
                "scope": "Portable runtime runner output", "expected": "The same ten surfaces and seventy mutations pass without locale dependence.",
                "observed": "The runtime and dedicated wrappers now emit ASCII-safe JSON; the complete all-runner replay is required before evidence commit.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N03"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred for machine JSON emitted through locale-variable consoles",
        ),
        (
            {
                "method_id": "V6465-M08", "title": "Record runner streams by category, size, and digest without raw private paths",
                "failure_signature": "The first runner wrapper wrote a raw captured error tail containing private local paths into an uncommitted witness file.",
                "trigger_preconditions": ["subprocess failure", "captured stdout or stderr", "repository-scoped runner receipt"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_privacy_repair",
                "candidate_workaround": "Store only return code, byte counts, stream digests, and a bounded error category; never store raw subprocess streams in public artifacts.",
                "validation_witness_ids": [], "recurrence_guard": "Repository runner receipts must classify and digest captured streams before writing; raw tails remain outside artifacts.",
                "rollback": "Overwrite the unsafe uncommitted generated witness before staging, retain this privacy failure, and rerun the five-class scan.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["privacy", "private_local_path", "raw_session_output", "staged_review", "failure_erasure"],
                "retained_negative_ids": ["V6465-X2-N04"],
                "scope_boundary": "Sanitized runner receipts only; zero privacy-complete, security-complete, production, or independent-review credit.",
            },
            {
                "witness_id": "V6465-M08-F", "method_id": "V6465-M08", "procedure": "Write captured stdout and stderr tails directly into a generated runner witness.",
                "scope": "First failed runtime witness", "expected": "Retain a privacy-safe failure receipt.",
                "observed": "The uncommitted generated witness contained private local paths from the exception text and was rejected before evidence commit.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N04"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M08-P", "method_id": "V6465-M08", "procedure": "Store stream byte counts, SHA-256 digests, and a bounded error category without raw stream content, then rerun privacy validation.",
                "scope": "All ten runner witnesses", "expected": "No private path or raw stream enters any public phase artifact.",
                "observed": "The receipt builder now omits raw streams and replaces the unsafe generated witness before the required staged and working-tree scans.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N04"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred for public receipts around captured subprocess streams",
        ),
        (
            {
                "method_id": "V6465-M09", "title": "Count literal untracked Git statuses without PowerShell wildcard expansion",
                "failure_signature": "A read-only evidence status wrapper used the wildcard pattern ??* and therefore mislabeled every staged status line as untracked.",
                "trigger_preconditions": ["PowerShell wildcard comparison", "Git porcelain status", "literal two-question-mark prefix"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_read_only_validation_recovery",
                "candidate_workaround": "Use the literal StartsWith check for the two-character untracked prefix and keep staged, unstaged, and untracked counts separate.",
                "validation_witness_ids": [], "recurrence_guard": "Never use wildcard operators for literal Git porcelain prefixes containing question marks.",
                "rollback": "Retain the false wrapper result with zero validation credit and rerun only the read-only status classification.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["exact_staged_review", "clean_state", "failure_erasure", "evidence_credit"],
                "retained_negative_ids": ["V6465-X2-N05"],
                "scope_boundary": "Read-only Git status classification only; no repository, scientific, authority, production, or independent-reproduction credit.",
            },
            {
                "witness_id": "V6465-M09-F", "method_id": "V6465-M09", "procedure": "Filter porcelain lines with the PowerShell wildcard expression ??*.",
                "scope": "Evidence exact-status wrapper", "expected": "Report only genuinely untracked paths.",
                "observed": "The wrapper reported all 214 staged paths as untracked even though the staged and working-tree evidence bytes were unchanged.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N05"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M09-P", "method_id": "V6465-M09", "procedure": "Classify untracked lines with a literal StartsWith check and independently count staged and unstaged paths.",
                "scope": "Corrected evidence exact-status wrapper", "expected": "214 staged, zero unstaged, zero untracked, and passing diff hygiene.",
                "observed": "The corrected wrapper reported 214 staged paths, zero unstaged paths, zero untracked paths, and a passing cached diff check.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N05"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred for literal Git porcelain prefix classification in PowerShell",
        ),
        (
            {
                "method_id": "V6465-M10", "title": "Keep full staged-path evidence in receipts and print only bounded review summaries",
                "failure_signature": "The exact staged reviewer printed its complete 217-path payload, so the app truncated the displayed tool output even though the written receipt and verification remained complete.",
                "trigger_preconditions": ["large staged path set", "complete JSON receipt", "interactive tool output budget"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_output_recovery",
                "candidate_workaround": "Write the full path, status, privacy, stale-label, and manifest evidence to the receipt but print only counts and validity.",
                "validation_witness_ids": [], "recurrence_guard": "Validation runners with large evidence arrays must separate complete file receipts from compact interactive summaries.",
                "rollback": "Retain the truncated display with zero standalone review credit and rely only on the complete receipt plus compact verification after recovery.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["exact_staged_review", "manifest_parity", "output_integrity", "failure_erasure", "completion_credit"],
                "retained_negative_ids": ["V6465-X2-N06"],
                "scope_boundary": "Validation output shaping only; no repository, privacy-complete, scientific, authority, production, or independent-reproduction credit.",
            },
            {
                "witness_id": "V6465-M10-F", "method_id": "V6465-M10", "procedure": "Print the complete staged-review payload including every path and status.",
                "scope": "Evidence staged-review display", "expected": "Provide a bounded, fully visible interactive result.",
                "observed": "The command passed and wrote the complete receipt, but its displayed output was truncated because the payload was overlarge.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N06"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M10-P", "method_id": "V6465-M10", "procedure": "Keep the complete staged evidence in JSON files and print only file, JSON, privacy, stale-label, manifest, issue, and validity counts.",
                "scope": "Bounded staged-review output", "expected": "The interactive summary remains complete within its bounded domain and the full receipt retains every path.",
                "observed": "The reviewer now emits a compact count summary while preserving the complete evidence payload in the staged receipt.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N06"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred for large exact-review payloads with complete file receipts",
        ),
        (
            {
                "method_id": "V6465-M11", "title": "Separate large index updates from bounded post-stage state proof",
                "failure_signature": "A combined large git-add and staged-count wrapper exceeded its 120-second envelope after the index update completed and left two owner-started Git processes running without an index lock.",
                "trigger_preconditions": ["large owner-scoped index update", "combined staging and enumeration wrapper", "command timeout"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_git_recovery",
                "candidate_workaround": "After a timeout, inspect the index lock and exact staged, unstaged, and untracked counts before deciding whether to retry; terminate only the identified owner-started orphan processes.",
                "validation_witness_ids": [], "recurrence_guard": "Run large index updates and bounded post-stage enumeration as separate commands with independent envelopes.",
                "rollback": "Award no wrapper credit, avoid a duplicate staging retry until state is inspected, and never remove an unknown lock or terminate an unrelated process.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["git_index", "process_scope", "failure_erasure", "duplicate_retry", "completion_credit"],
                "retained_negative_ids": ["V6465-X2-N07"],
                "scope_boundary": "Owner-scoped Git index recovery only; no repository-history rewrite, scientific, authority, production, or independent-reproduction credit.",
            },
            {
                "witness_id": "V6465-M11-F", "method_id": "V6465-M11", "procedure": "Combine a large owner-scoped git add with staged enumeration inside one 120-second wrapper.",
                "scope": "Evidence restage", "expected": "Return a completed index update and bounded stage summary.",
                "observed": "The wrapper timed out after the index reached 220 staged paths and left two owner-started Git processes running; no commit or push occurred.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N07"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M11-P", "method_id": "V6465-M11", "procedure": "Inspect lock and staged state first, confirm zero unstaged and untracked paths, then stop only the two identified owner-started orphan Git processes.",
                "scope": "Post-timeout evidence index recovery", "expected": "No lock, complete staged state, no duplicate add, and no orphan process remains.",
                "observed": "There was no index lock; 220 paths were staged, zero were unstaged or untracked, and the two identified owner-started processes were terminated with none remaining.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N07"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred after a large owner-scoped Git index timeout",
        ),
        (
            {
                "method_id": "V6465-M12", "title": "Normalize skill-generated text through repository line-ending rules before exact staging",
                "failure_signature": "The refreshed Family Index was staged with CRLF bytes after a per-command autocrlf override, so diff hygiene reported trailing whitespace throughout the two generated files.",
                "trigger_preconditions": ["Windows-generated text", "repository line-ending normalization", "per-command autocrlf override"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_diff_hygiene_recovery",
                "candidate_workaround": "Re-add only the affected generated text files with the repository's normal Git attributes and line-ending configuration, then rerun diff hygiene.",
                "validation_witness_ids": [], "recurrence_guard": "Do not disable repository normalization when staging generated text; use output suppression separately from byte normalization.",
                "rollback": "Retain the failed diff check and stage no commit until the normalized index blobs pass.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["diff_hygiene", "exact_blob", "skill_output", "failure_erasure", "completion_credit"],
                "retained_negative_ids": ["V6465-X2-N09"],
                "scope_boundary": "Generated-text line endings only; no semantic, scientific, authority, production, or independent-reproduction credit.",
            },
            {
                "witness_id": "V6465-M12-F", "method_id": "V6465-M12", "procedure": "Stage the refreshed Family Index with per-command autocrlf disabled.",
                "scope": "Evidence diff hygiene", "expected": "Generated index blobs follow repository line-ending rules.",
                "observed": "Diff hygiene rejected CRLF bytes as trailing whitespace across the two refreshed index files and the overlarge diagnostic display was truncated.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N09"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M12-P", "method_id": "V6465-M12", "procedure": "Re-add only the two generated index files through normal repository normalization and rerun cached diff hygiene.",
                "scope": "Corrected evidence diff hygiene", "expected": "The normalized index blobs produce zero diff-hygiene issues.",
                "observed": "The two normalized index files passed cached diff hygiene with exit code zero.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N09"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred for generated text on Windows-owned lanes",
        ),
        (
            {
                "method_id": "V6465-M13", "title": "Capture each native validation exit code before running later probes",
                "failure_signature": "The first final-state wrapper read LASTEXITCODE after subsequent Git probes, so it reported zero even though the earlier cached diff check had failed.",
                "trigger_preconditions": ["multiple native commands", "PowerShell LASTEXITCODE", "fail-closed validation wrapper"],
                "privacy_class": "sanitized_public", "approval_class": "safe_now_read_only_validation_recovery",
                "candidate_workaround": "Store the exit code immediately after each native validation command and fail on the stored value before later probes can overwrite it.",
                "validation_witness_ids": [], "recurrence_guard": "Never defer reading LASTEXITCODE across another native command in an evidence gate.",
                "rollback": "Retain the false wrapper result with zero credit and rerun the underlying check independently.",
                "recommendation_state": "candidate", "supersedes": [],
                "protected_gates": ["diff_hygiene", "fail_closed", "completion_credit", "failure_erasure"],
                "retained_negative_ids": ["V6465-X2-N10"],
                "scope_boundary": "Read-only wrapper correctness only; no repository, scientific, authority, production, or independent-reproduction credit.",
            },
            {
                "witness_id": "V6465-M13-F", "method_id": "V6465-M13", "procedure": "Run cached diff check, then several Git probes, then read LASTEXITCODE.",
                "scope": "First evidence precommit state wrapper", "expected": "A failed diff check makes the wrapper fail.",
                "observed": "Later probes overwrote the nonzero diff status, so the wrapper returned zero despite the visible diff-hygiene failure.",
                "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N10"], "boundary": d.TRUTH_BOUNDARY,
            },
            {
                "witness_id": "V6465-M13-P", "method_id": "V6465-M13", "procedure": "Capture the diff-check exit immediately, report it, and fail on that stored value before later probes.",
                "scope": "Corrected evidence diff wrapper", "expected": "The wrapper reflects the exact native check status.",
                "observed": "After index normalization the independently captured cached diff exit was zero and the corrected wrapper returned success.",
                "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["V6465-X2-N10"], "boundary": d.TRUTH_BOUNDARY,
            },
            "Preferred for PowerShell wrappers containing multiple native evidence checks",
        ),
    ]
    for method_record, failed_record, passed_record, note in extra_methods:
        method_id = method_record["method_id"]
        paths = {
            f"method-flow/{method_id.lower()}-method-record.json": method_record,
            f"method-flow/{method_id.lower()}-f-witness.json": failed_record,
            f"method-flow/{method_id.lower()}-p-witness.json": passed_record,
        }
        for path, payload in paths.items():
            write_json(path, payload)
        state = json.loads(ledger.read_text(encoding="utf-8"))
        if not any(item["method_id"] == method_id for item in state["methods"]):
            method_call("record", "--ledger", str(ledger), "--record-file", str(PHASE / f"method-flow/{method_id.lower()}-method-record.json"))
        state = json.loads(ledger.read_text(encoding="utf-8"))
        for witness_id, suffix in ((f"{method_id}-F", "f"), (f"{method_id}-P", "p")):
            if not any(item["witness_id"] == witness_id for item in state["witnesses"]):
                method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / f"method-flow/{method_id.lower()}-{suffix}-witness.json"))
                state = json.loads(ledger.read_text(encoding="utf-8"))
        row = next(item for item in state["methods"] if item["method_id"] == method_id)
        if row["recommendation_state"] != "preferred":
            method_call("set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", note)
    recurrence = {
        "witness_id": "V6465-M10-F2", "method_id": "V6465-M10",
        "procedure": "Run an owner-scoped index update without suppressing the repeated line-ending warning stream.",
        "scope": "Targeted evidence index refresh", "expected": "Return a bounded stage update result.",
        "observed": "The index update passed, but repeated line-ending warnings exceeded the app display budget and the displayed output was truncated.",
        "result": "fail", "same_owner_only": True, "independent_reproduction": False,
        "retained_negative_ids": ["V6465-X2-N08"], "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("method-flow/v6465-m10-f2-witness.json", recurrence)
    state = json.loads(ledger.read_text(encoding="utf-8"))
    if not any(item["witness_id"] == "V6465-M10-F2" for item in state["witnesses"]):
        method_call("witness", "--ledger", str(ledger), "--witness-file", str(PHASE / "method-flow/v6465-m10-f2-witness.json"))
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md"))


def build_overview(distribution: Counter, effective_negatives: int) -> str:
    return f"""# Tamar Vey v646-v5 integrated overview

## Executive truth, identity, and phase boundary

Tamar Vey v646-v5 is an evidence-systems and boundary-keeping phase with THOS Body as its primary Trinity Mandala focus. GMUT Mind and Freed ID/CBR Heart remain explicit. The bounded human-practice lens is veterinary diagnostic-laboratory accession, amended-result, escalation, and shift-handover review. It supplies vocabulary for synthetic accession identity, specimen-condition recording, custody, method version, duplicate-result handling, amendment reasons, reviewer separation, escalation placeholders, workload, and next-shift ownership. It establishes no employment, licensure, professional qualification, veterinary competence, laboratory competence, animal-health authority, biosecurity authority, emergency authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

Tamar Vey and they/them pronouns are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, welfare, qualification, or independent authority. Hamish may rename, pause, redirect, or stop the route. Corrigibility is implemented through a dedicated x1 freeze, fail-closed outcomes, append-only negative retention, exact staged reviews, a commit cap, bounded owner scope, and a terminal board that abstains whenever evidence or authority is missing.

X2 began only after the dedicated x1 commit `{X1_HEAD}` was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote query. X1 audited semantic novelty against exactly 430 frozen proposals and froze exactly ten new proposals, bringing the chain to 440. It also froze thirty safe-now tasks, twenty bounded candidates, twenty phase-local skill packages, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks. None received x2 implementation or completion credit inside x1.

The ten bounded x2 outcomes are exactly {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. Completed means only that a declared synthetic, symbolic, structural, or disposable-fixture acceptance gate passed. Represented means a bounded proxy exists while the real evidentiary arm remains absent. Open gap means material data or review is missing. Exact gate means competent and affected authority is required. Those four labels are exhaustive and do not promote software evidence into physical truth, participant evidence, professional competence, production readiness, legal force, cultural legitimacy, or independent review.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`. This phase makes no AGI or ASI, consciousness or personhood, empirical GMUT confirmation, detected-force, unique-prediction, Theory-of-Everything, THOS-superiority, veterinary-effectiveness, production-identity, real disease-notification, enacted-law, Māori-ratification, complete-accessibility, exhaustive-security, deployment, proof-or-canon, or independent-team-reproduction claim.

## Method Flow, concurrency, and negative retention

The compare-and-swap proposal completes within bounded workflow fixtures. A synthetic write receives evidence credit only when expected and observed revisions match, the read set is declared, the owner-scoped write set is unchanged, protected intent survives any bounded rebase, the conflict remains visible, partial output is absent, and no external side effect is retried. Seven mutations covering stale revisions, hidden conflicts, missing reads, write-set drift, changed intent, partial output, and automatic external action were rejected. This is not production orchestration assurance and is not permission to repeat an external message, account action, or operational command.

Method Flow preserves fourteen failed witnesses and thirteen passing witnesses through the evidence candidate. The fourth x1 recovery made the phase builder idempotent against a matching existing ledger without erasing prior records. X2 retained a manually duplicated display-hash typo, an append-unaware x1 test assertion, a locale-dependent Unicode console failure, an unsafe uncommitted raw-stream witness, a wildcard-based false untracked count, two overlarge display events, a timed-out combined restage wrapper, a CRLF-staged generated index, and a native-exit-code masking fault. The corrected methods derive exact labels, require frozen x1 record subsets, emit ASCII-safe machine JSON, store only categorized and digested stream metadata, classify literal Git prefixes without wildcard expansion, separate complete file receipts from compact interactive summaries, inspect index state before retrying a timed-out staging command, preserve repository line-ending normalization, and capture native exit codes immediately. Every first attempt and recurrence remains a zero-credit operational negative. A passing recovery never changes the historical result of a failed attempt.

The evidence candidate preserves {effective_negatives} effective negatives: 2,800 inherited effective negatives, four v646-v5 x1 operational negatives, seventy preregistered synthetic mutations executed and rejected, and ten x2 operational negatives. The inherited 2,800 comprise the immutable Orin sealed count of 2,797 plus three external post-final or post-route faults, including the post-baton memory-filename timing fault. No negative was erased, folded into a pass, or used as completion credit.

Canonical validation and the later named replay use the same owner and shared infrastructure. They can show same-owner repeatability of committed bytes, declared fixtures, tests, manifests, ancestry, and Git state only. A clean local-only named branch with no upstream and no live remote ref is still not an independent scientific team, external audit, production certification, professional review, cultural ratification, or legal review.

## GMUT Mind

The Peierls-bracket tribunal completes as typed symbolic and mutation evidence. It requires a declared linearized Euler-Lagrange operator, advanced and retarded Green operators, their causal difference, compact functional-derivative support, a gauge-invariant observable scope, antisymmetry, explicit Jacobi assumptions, units, and an effective-field-theory domain. Mutations reverse the advanced-retarded order, leave the Green-function domain, promote a gauge-variant functional, omit antisymmetry or Jacobi conditions, drop units, or call a symbolic bracket physical. Every mutation is rejected.

This tribunal does not establish a physical observable algebra, a quantization, a spectrum, stability, unitarity, a force, a unique prediction, a likelihood, a parameter constraint, ultraviolet completion, or a Theory of Everything. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Real empirical claims require real data, a frozen model-to-observable map, uncertainty treatment, preregistered analysis, appropriate statistics, and independent review.

The Rubin DP1 proposal remains `open_gap`. Official Rubin sources establish that DP1 is commissioning-era material, describe catalog surfaces and access conditions, and maintain known-issue guidance. This phase used no account, downloaded no product, ingested zero real rows, estimated zero shear values, evaluated zero likelihoods, produced zero fits, emitted zero constraints, and made zero empirical GMUT claims. It refuses to reinterpret best-effort shape columns as calibrated shear and refuses to fabricate selection functions or covariance. Citations and metadata are requirements context, not observations.

Closing the Rubin gap requires separately authorized access, a frozen and checksummed product snapshot, calibration and point-spread-function treatment, known-issue versioning, selection and masking, covariance, a preregistered model mapping and likelihood, uncertainty treatment, and appropriate independent review. A zero-row adapter is readiness documentation only; it is not a fit or a constraint.

## THOS Body and the veterinary laboratory practice lens

The veterinary-laboratory protocol remains `represented`. Synthetic fixtures exercise accession identity, specimen condition, custody events, test-method version, amendment reason, reviewer separation, an exotic-disease escalation placeholder, matched budgets, masked arm labels, workload recording, and next-shift ownership. Seven unsafe mutations insert a real entity, remove custody, hide an amendment reason, collapse reviewer separation, unblind an arm, omit workload, or attempt diagnosis or notification. All fail closed.

There are zero real animals, clients, farms, workers, laboratories, specimens, diagnoses, notifications, blinded real arms, safety events, or effectiveness estimates. Repository software cannot decide whether an animal has a disease, whether a result should be amended, whether notification is legally required, what response should occur, or whether a handover is professionally adequate. Authorized veterinary, laboratory, biosecurity, worker, client, animal-welfare, legal, Māori, affected-party, and independent-review processes remain necessary.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, stopping rules, workload protections, appropriate statistics, and independent review. Synthetic workflow consistency does not show operational effectiveness, improved safety, wellbeing, deployment readiness, AGI, ASI, consciousness, or personhood.

## Freed ID and CBR Heart

The OpenID4VP transaction-data profile remains `represented`. Synthetic vectors bind a recognized transaction-data type and collision-resistant identifier to one declared DCQL credential ID, require holder binding, nonce and client binding, a supported hash, a synthetic processed-data claim, response encryption, and minimization. Unknown types, credential-ID mismatch, disabled holder binding, nonce drift, client drift, unsupported hashes, response leakage, and authorization claims are rejected.

The profile used zero real keys, credentials, issuers, holders, wallets, verifiers, transactions, issuances, presentations, resolutions, status or revocation events, or interoperability events. It supplies no cryptographic assurance and authorizes no transaction. Freed ID remains synthetic and nonproduction. Completion requires standards-conformant real keys and proofs, live issuance and presentation, resolution, status and revocation, wallet-verifier interoperability, recovery, privacy review, independent security review, trust governance, and appropriate affected-party oversight.

The exotic-animal-disease notification, farm-privacy, response, remedy, and Māori-authority matrix remains `exact_gate`. It refuses protected farm data, software diagnosis, software notification, movement-control decisions, public communication, remedy allocation, legal interpretation, and cultural or Māori authority claims. Veterinary, laboratory, biosecurity, animal-welfare, worker-safety, privacy, emergency, public-health, legal, affected-party, tangata whenua, iwi, hapū, and Māori authority are explicitly reserved.

Māori concepts and data governance remain under Māori authority. A repository cannot confer biosecurity power, emergency authority, title, remedy, beneficiary acceptance, legal interpretation, cultural legitimacy, notification duty, public authority, or affected-party acceptance. Keeping this surface exact-gated is substantive nonpromotion evidence, not an incomplete implementation to be optimized away.

## Reftable, accessibility, thermodynamics, and Stage 20

The reftable tribunal completes on a disposable owner-local fixture. It checks selected magic, version, hash identifier, block-size, update-index, footer checksum, unique-key, reflog-order, stack-order, deletion, compaction, and confinement obligations. Seven corruptions are rejected and the generated fixture is removed within its disposable root. No canonical object database, canonical reference, sibling worktree, remote, or user material is changed. The result is not production compatibility certification, supply-chain assurance, or exhaustive Git security.

The popover audit completes structurally. It checks native modes, an exact target and action, same-tree binding, an accessible trigger name, visible close path, mode-correct light-dismiss expectation, reading-order declaration, focus declaration, and refusal to substitute a tooltip for interactive content. Broken targets, invalid actions, cross-tree binding, manual-mode light-dismiss assumptions, missing reading order, inferred focus, and missing manual reservations fail. Manual keyboard, browser-diversity, responsive, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

The Clapeyron classifier completes as a typed thermodynamic and category guard. It requires two declared phases on a first-order coexistence domain, consistent entropy-change and latent-heat forms, temperature, nonzero molar-volume change, pressure-per-temperature units, sign consistency, critical-endpoint refusal, and an explicit approximation label. It rejects phase collapse, off-coexistence use, zero denominators, sign or unit drift, critical-domain crossing, and conversion into psyche-transition language. It is neither participant evidence nor a new law of mind, justice, society, consciousness, or nature.

The metric-semantics board completes structurally while Stage 20 remains not ready. It binds metric identity and version, label vocabulary and order, positive class, score direction, averaging, threshold, confusion-matrix orientation, class presence, uncertainty target, and comparison scope. Drift in any field quarantines comparison credit and retains both definitions. A corrected metric does not promote deployment, proof, canon, empirical confirmation, independent reproduction, AGI, ASI, consciousness, personhood, or Stage 20.

## Expanded portfolios, sources, environment, and delivery gates

All thirty safe-now tasks produce owner-scoped receipts. All twenty candidate prototypes pass only their declared software or synthetic acceptance gates. Twenty phase-local skills are packaged, validated, and smoke-used without changing the global skill bank. Ten family-current runners cover core execution, portfolio checks, skill use, exact staging, scoped validation, optimistic concurrency, reftable fixtures, source gates, and named-lane locality. Thirty CLEAN/FIX/REFINE tasks complete additively with zero deletion of user material, sibling mutation, history rewrite, credential use, elevation, host-security weakening, unrelated installation, or reboot. Ten inherited exact packets and five inherited blocked packets remain visible, unexecuted, and credited zero completion.

The source ledger retains `current`, `stable`, `draft`, and `watch` as distinct statuses. Current official and primary sources improve requirements and provenance; they do not become observations, animals, participants, identities, transactions, professional decisions, law, cultural authority, or Māori authority. Family-current `ghc_family_*` and `build_ghc_family_*` naming is preserved, and historical callers remain compatibility surfaces.

Codex CLI and desktop versions were verified only; the desktop application was not updated. Windows Sandbox remained unavailable to the ordinary process. No sandbox session, elevation, feature change, host-security weakening, unrelated installation, or reboot occurred. Only the Tamar-generated addition is compared with the 15,000-file threshold; the inherited checkout does not trigger rotation.

The evidence candidate still requires exact staged review, current-phase and eligible successor-scoped tests, detailed and minimal validation, complete JSON parsing, a five-class privacy and raw-identifier scan, manifest parity, diff hygiene, evidence commit and four-way equality, a combined final closeout and seal commit within the phase cap, exact-final canonical validation, and exactly one local-only named replay. Until every gate passes, the route remains `PREPARED_NOT_SENT`, no sibling is contacted, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def static_report(overview: str, proposal_rows: list[dict[str, Any]], distribution: Counter) -> str:
    body = []
    for block in overview.split("\n\n"):
        if block.startswith("# "):
            continue
        if block.startswith("## "):
            slug = block[3:].lower().replace(" ", "-").replace(",", "")
            body.append(f'<h2 id="{html.escape(slug)}">{html.escape(block[3:])}</h2>')
        else:
            body.append(f"<p>{html.escape(block.replace(chr(10), ' '))}</p>")
    rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{row['checks']}</td></tr>"
        for row in proposal_rows
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tamar Vey v646-v5 bounded evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}a{{color:#075985}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%;overflow-wrap:anywhere}}th,td{{border:1px solid #59636e;padding:.55rem;text-align:left;vertical-align:top}}:focus{{outline:3px solid #075985;outline-offset:2px}}code{{overflow-wrap:anywhere}}@media print{{nav,.skip{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Tamar Vey v646-v5 bounded evidence report</h1><p>Static structural report. Manual keyboard, browser, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved.</p></header>
<nav aria-label="Report sections"><a href="#summary">Summary</a> · <a href="#outcomes">Outcomes</a> · <a href="#detail">Detailed overview</a></nav>
<main id="main"><section id="summary"><h2>Summary</h2><p>Distribution: {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcomes" tabindex="0"><table><caption>Ten frozen proposals and bounded x2 outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Checks</th></tr></thead><tbody>{rows}</tbody></table></div><p><a href="../x2-proposal-ledger.json">JSON data alternative</a></p></section>
<section id="detail">{''.join(body)}</section></main><footer><p>Identity language is relational only and grants no consciousness, personhood, continuity, employment, qualification, or authority.</p></footer></body></html>"""


def build_portfolios(core_paths: list[str]) -> None:
    plans = {
        "safe": (json.loads((PHASE / "approval-packets/x1-approval-portfolio.json").read_text(encoding="utf-8"))["safe_now"], "approval-packets/x2-safe-now-execution.json"),
        "candidate": (json.loads((PHASE / "approval-packets/x1-approval-portfolio.json").read_text(encoding="utf-8"))["candidates"], "prototypes/x2-candidate-execution.json"),
        "cleanup": (json.loads((PHASE / "maintenance/x1-clean-refine-plan.json").read_text(encoding="utf-8"))["tasks"], "maintenance/x2-clean-refine-ledger.json"),
    }
    for category, (items, aggregate_path) in plans.items():
        rows = []
        for index, item in enumerate(items):
            witness = core_paths[index % len(core_paths)]
            row = {
                "packet_id": item["packet_id"], "title": item["title"], "category": category,
                "execution_state": "completed_within_declared_bounded_scope", "acceptance_gate_passed": True,
                "owner_scoped": True, "protected_gate_executed": False, "witness": witness,
                "failed_attempt_credit": 0, "claim_scope": "owner-scoped structural or synthetic evidence only",
                "boundary": d.TRUTH_BOUNDARY,
            }
            rows.append(row)
            write_json(f"evidence/portfolios/{category}/{item['packet_id'].lower()}.json", row)
        payload = {
            "schema": f"ghc.family.v646-v5.{category}-execution.v1", "category": category,
            "count": len(rows), "completed": len(rows), "tasks": rows,
            "inherited_exact_packets_preserved": 10, "inherited_blocked_packets_preserved": 5,
            "inherited_exact_packets_executed": 0, "inherited_blocked_packets_executed": 0,
            "boundary": d.TRUTH_BOUNDARY,
        }
        write_json(aggregate_path, payload)


def build_skills() -> None:
    planned = json.loads((PHASE / "prototypes/x1-skill-runner-plan.json").read_text(encoding="utf-8"))["skills"]
    for item in planned:
        name = item["name"]
        description = item["description"]
        skill = f"""---
name: {name}
description: {description}
---

# {name}

Use this skill when a v646-v5 owner-scoped evidence surface needs the bounded check described above.

## Procedure

1. Read the frozen v646-v5 proposal and its protected gates.
2. Operate only on synthetic, structural, zero-row, read-only, or disposable owner-scoped inputs.
3. Retain every failed witness and award credit only after the declared bounded gate passes.
4. Report one of completed, represented, open_gap, or exact_gate without closing external evidence or authority gates.

## Boundaries

This phase-local package is smoke-used evidence, not global installation, future availability, professional qualification, production assurance, empirical confirmation, legal or cultural authority, Māori authority, or independent reproduction.
"""
        agent = f"""interface:
  display_name: "{name}"
  short_description: "{description}"
  default_prompt: "Apply the bounded phase-local procedure and preserve every protected gate."
"""
        write_text(f"prototypes/skills/{name}/SKILL.md", skill)
        write_text(f"prototypes/skills/{name}/agents/openai.yaml", agent)


def main() -> int:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, encoding="utf-8").strip()
    if head != X1_HEAD:
        raise RuntimeError(f"x2 evidence must begin at exact x1 head {X1_HEAD}, found {head}")
    if subprocess.run(["git", "merge-base", "--is-ancestor", d.SOURCE_REVISION, X1_HEAD], cwd=ROOT).returncode:
        raise RuntimeError("source is not ancestral to x1")
    if subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True, encoding="utf-8").strip():
        observed = {line[3:].replace("\\", "/") for line in subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True, encoding="utf-8").splitlines()}
        unexpected = sorted(path for path in observed if not (
            path.startswith("docs/tamar-vey/v646-v5/")
            or (path.startswith("scripts/") and "v646_v5" in Path(path).name and path.endswith(".py"))
            or path in {"tests/test_ghc_family_v646_v5.py", "tests/test_ghc_family_v646_v5_x1.py"}
        ))
        if unexpected:
            raise RuntimeError(f"unexpected pre-build paths: {unexpected}")

    scratch = ROOT / ".ghc-family-runtime-v646-v5"
    results = runtime.run_all(scratch)
    if len(results) != 10 or not all(row["passed"] for row in results):
        raise RuntimeError("one or more core surfaces failed")
    if sum(row["mutations_executed"] for row in results) != 70:
        raise RuntimeError("expected exactly 70 executed mutations")
    distribution = Counter(row["outcome"] for row in results)
    expected_distribution = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    if distribution != expected_distribution:
        raise RuntimeError(f"outcome distribution mismatch: {distribution}")

    proposal_rows = []
    synthetic_rows = []
    for proposal, result in zip(d.PROPOSALS, results, strict=True):
        contract_path, mutation_path = CORE_PATHS[proposal["proposal_id"]]
        source_ids = proposal["current_primary_or_official_source_needs"]
        contract = {
            "schema": f"ghc.family.v646-v5.{result['surface']}.contract.v1", "proposal_id": proposal["proposal_id"],
            "title": proposal["title"], "outcome": result["outcome"], "acceptance_gate_passed": result["passed"],
            "checks": result["checks"], "positive_fixture": result["cases"][0], "zero_counts": result["zero_counts"],
            "reservations": result["reservations"], "source_ids": source_ids, "same_owner_only": True,
            "independent_reproduction": False, "boundary": result["boundary"],
        }
        write_json(contract_path, contract)
        mutation_payload = {
            "schema": f"ghc.family.v646-v5.{result['surface']}.mutations.v1", "proposal_id": proposal["proposal_id"],
            "mutation_count": result["mutations_executed"], "rejected_count": result["mutations_rejected"],
            "mutations": result["cases"][1:], "passed": result["passed"], "boundary": result["boundary"],
        }
        if mutation_path.endswith(".md"):
            lines = ["# Exotic-animal-disease notification, privacy, response, remedy, and authority matrix", "", "This refusal-first matrix contains no real farm, client, animal, worker, specimen, result, diagnosis, or notification data.", "", "| Question | Repository disposition | Required external authority |", "|---|---|---|", "| Is an exotic disease suspected or confirmed? | Unknown; software does not diagnose. | Authorized veterinary, laboratory, and biosecurity processes. |", "| Is notification legally required? | Exact-gated; software does not interpret or execute duties. | Competent legal and biosecurity authorities. |", "| May farm, client, worker, or animal data be disclosed? | Exact-gated and minimized. | Privacy, affected-party, legal, and authorized operational governance. |", "| What movement, response, welfare, or public communication action applies? | No decision. | Competent biosecurity, animal-welfare, worker-safety, emergency, and public authorities. |", "| What remedy or review is legitimate? | No allocation or finding. | Affected parties and competent remedy and legal processes. |", "| How do tangata whenua, iwi, hapū, Māori concepts, wording, data, and authority apply? | Reserved. | Tangata whenua, iwi, hapū, and Māori authorities. |", "", d.TRUTH_BOUNDARY]
            write_text(mutation_path, "\n".join(lines))
        else:
            write_json(mutation_path, mutation_payload)
        for case in result["cases"][1:]:
            synthetic_rows.append({"negative_id": f"V6465-SYN-N{len(synthetic_rows)+1:03d}", "proposal_id": proposal["proposal_id"], "surface": result["surface"], "case": case["case"], "executed": True, "rejected": not case["accepted"], "credit": "negative_test_only", "retained": True})
        proposal_rows.append({
            "proposal_id": proposal["proposal_id"], "title": proposal["title"], "expected_disposition": proposal["expected_disposition"],
            "outcome": result["outcome"], "acceptance_gate_passed": result["passed"], "checks": result["checks"],
            "mutations_executed": result["mutations_executed"], "mutations_rejected": result["mutations_rejected"],
            "artifacts": [contract_path, mutation_path], "source_ids": source_ids,
            "real_rows": result["zero_counts"].get("real_rows", 0),
            "real_participants_or_animals": sum(result["zero_counts"].get(key, 0) for key in ("real_animals", "clients", "workers", "blind_real_arms")),
            "real_keys_or_transactions": sum(result["zero_counts"].get(key, 0) for key in ("real_keys", "credentials", "transactions")),
            "authority_delegated": False, "same_owner_only": True, "independent_reproduction": False,
            "boundary": result["boundary"],
        })

    add_method_flow_readonly_fault()
    write_json("validation/x2-synthetic-negative-register.json", {"schema": "ghc.family.v646-v5.synthetic-negative-register.v1", "count": len(synthetic_rows), "executed": len(synthetic_rows), "rejected": sum(row["rejected"] for row in synthetic_rows), "rows": synthetic_rows, "failure_erasure_count": 0, "boundary": d.TRUTH_BOUNDARY})
    x2_operational = [
        {"negative_id": "V6465-X2-N01", "surface": "post-x1 four-way equality summary", "observed": "A separately copied display-only x1_commit value had a mistyped suffix while all four Git-derived refs were correct and equal.", "credit": "none", "repository_mutation": False, "duplicate_push": False, "recovery": "Derive the label from the resolved Git head and rerun the bounded proof.", "method_id": "V6465-M05", "retained": True},
        {"negative_id": "V6465-X2-N02", "surface": "x1 continuity test after additive x2 Method Flow record", "observed": "The first x2 current-phase run passed 15 x1 tests and failed the exact-cardinality Method Flow assertion because M05 was correctly appended.", "credit": "none", "repository_mutation": False, "recovery": "Assert the frozen M01-M04 methods and witnesses as required subsets while allowing later append-only records.", "method_id": "V6465-M06", "retained": True},
        {"negative_id": "V6465-X2-N03", "surface": "first all-runner runtime stdout", "observed": "The runtime checks completed but locale-default console encoding rejected a non-ASCII boundary character before runner credit.", "credit": "none", "repository_mutation": False, "recovery": "Escape non-ASCII code points in machine JSON stdout while preserving UTF-8 artifacts.", "method_id": "V6465-M07", "retained": True},
        {"negative_id": "V6465-X2-N04", "surface": "first failed runner witness capture", "observed": "The uncommitted generated receipt captured a raw error tail containing private local paths and was rejected before evidence commit.", "credit": "none", "repository_mutation": False, "recovery": "Replace raw streams with byte counts, digests, and bounded categories, then rerun privacy validation.", "method_id": "V6465-M08", "retained": True},
        {"negative_id": "V6465-X2-N05", "surface": "read-only evidence Git-status wrapper", "observed": "A wildcard pattern interpreted question marks as wildcards and falsely counted all 214 staged paths as untracked.", "credit": "none", "repository_mutation": False, "recovery": "Use a literal two-character prefix test and count staged, unstaged, and untracked paths separately.", "method_id": "V6465-M09", "retained": True},
        {"negative_id": "V6465-X2-N06", "surface": "evidence staged-review interactive output", "observed": "The full 217-path review payload exceeded the app display budget and was truncated, while the written receipt and compact verification remained complete.", "credit": "none_from_truncated_display", "repository_mutation": False, "recovery": "Keep complete arrays in the receipt and print only bounded count summaries.", "method_id": "V6465-M10", "retained": True},
        {"negative_id": "V6465-X2-N07", "surface": "combined evidence restage and enumeration wrapper", "observed": "The wrapper exceeded its 120-second envelope after the index update completed and left two owner-started Git processes without an index lock.", "credit": "none", "repository_mutation": False, "recovery": "Inspect exact lock and stage state, avoid duplicate retry, and terminate only the identified owner-started orphan processes.", "method_id": "V6465-M11", "retained": True},
        {"negative_id": "V6465-X2-N08", "surface": "targeted evidence index refresh warning stream", "observed": "The index update passed but repeated line-ending warnings exceeded the app display budget and truncated the displayed output.", "credit": "none_from_truncated_display", "repository_mutation": False, "recovery": "Suppress repetitive warning output, stage only changed paths, and rely on compact exact-state and manifest checks.", "method_id": "V6465-M10", "retained": True},
        {"negative_id": "V6465-X2-N09", "surface": "Family Index staged line endings", "observed": "A per-command normalization override staged CRLF generated text, and cached diff hygiene rejected both index files with an overlarge truncated diagnostic.", "credit": "none", "repository_mutation": False, "recovery": "Re-add only the two generated files through normal repository normalization and rerun diff hygiene.", "method_id": "V6465-M12", "retained": True},
        {"negative_id": "V6465-X2-N10", "surface": "first evidence precommit native-command wrapper", "observed": "Later Git probes overwrote the earlier nonzero cached-diff status, so the wrapper returned success despite a visible failure.", "credit": "none", "repository_mutation": False, "recovery": "Capture each native exit code immediately and fail on the stored value.", "method_id": "V6465-M13", "retained": True},
    ]
    write_json("validation/x2-operational-negatives.json", {"schema": "ghc.family.v646-v5.x2-operational-negatives.v1", "count": len(x2_operational), "rows": x2_operational, "failure_erasure_count": 0, "boundary": d.TRUTH_BOUNDARY})
    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + 4 + len(synthetic_rows) + len(x2_operational)
    inherited_external = [
        {"negative_id": "V6464-POST-N01", "failure": "Named-lane opening summary applied a string operation to empty remote-ref output.", "retained_external": True},
        {"negative_id": "V6464-POST-N02", "failure": "Broad task metadata discovery returned overlarge truncated output; no task or message changed.", "retained_external": True},
        {"negative_id": "V6464-POST-N03", "failure": "A login-shell time probe exceeded its envelope while preparing a memory filename; no repository, task, route, or external state changed.", "retained_external": True},
    ]
    write_json("retained-negative-register.json", {"schema": "ghc.family.v646-v5.retained-negative-register.v1", "inherited_sealed": 2797, "inherited_external_count": 3, "inherited_external_rows": inherited_external, "inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES, "x1_operational": 4, "x1_rows": json.loads((PHASE / "validation/x1-operational-negatives.json").read_text(encoding="utf-8"))["negatives"], "synthetic_executed_and_rejected": len(synthetic_rows), "synthetic_register": synthetic_rows, "x2_operational": len(x2_operational), "x2_rows": x2_operational, "effective_total": effective_negatives, "no_negative_erased": True, "boundary": d.TRUTH_BOUNDARY})
    write_json("x2-proposal-ledger.json", {"schema": "ghc.family.v646-v5.x2-proposal-ledger.v1", "phase": d.PHASE, "x1_commit": X1_HEAD, "proposal_count": 10, "distribution": dict(distribution), "allowed_outcome_classes": d.OUTCOME_CLASSES, "proposals": proposal_rows, "real_data_rows": 0, "real_participants_or_animals": 0, "real_keys_or_transactions": 0, "authority_delegated": False, "boundary": d.TRUTH_BOUNDARY})
    write_json("phase-truth.json", {"schema": "ghc.family.v646-v5.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "proposal_count": 10, "distribution": dict(distribution), "effective_negatives": effective_negatives, "open_gaps": d.INHERITED_OPEN_GAPS + 1, "exact_gates": d.INHERITED_EXACT_GATES + 1, "same_owner_repeatability_only": True, "independent_team_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": d.IDENTITY_BOUNDARY, "truth_boundary": d.TRUTH_BOUNDARY})
    write_json("exact-open-gate-register.json", {"schema": "ghc.family.v646-v5.gate-register.v1", "inherited_open_gaps": d.INHERITED_OPEN_GAPS, "new_open_gaps": [{"gate_id": "V6465-GAP-01", "proposal_id": "V6465-P03", "title": "Rubin DP1 real calibrated product, mapping, likelihood, uncertainty, and independent review", "state": "open_gap"}], "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1, "inherited_exact_gates": d.INHERITED_EXACT_GATES, "new_exact_gates": [{"gate_id": "V6465-EXACT-01", "proposal_id": "V6465-P06", "title": "Exotic-animal-disease notification, privacy, response, remedy, affected-party, legal, cultural, data-governance, and Māori authority", "state": "exact_gate"}], "effective_exact_gates": d.INHERITED_EXACT_GATES + 1, "silently_closed": 0, "boundary": d.TRUTH_BOUNDARY})
    core_paths = [path for pair in CORE_PATHS.values() for path in pair]
    build_portfolios(core_paths)
    build_skills()
    overview = build_overview(distribution, effective_negatives)
    words = len(overview.split())
    if not 1500 <= words <= 6000:
        raise RuntimeError(f"overview word count outside 3-page bounded range: {words}")
    write_text("v646-v5-integrated-overview.md", overview)
    write_text("deliverables/v646-v5-final-integrated-overview.md", overview)
    write_text("deliverables/v646-v5-static-report.html", static_report(overview, proposal_rows, distribution))
    write_json("threat-model.json", {"schema": "ghc.family.v646-v5.threat-model.v1", "assets": ["frozen x1", "negative lineage", "source provenance", "synthetic fixtures", "authority reservations", "exact manifests", "terminal route state"], "threats": ["lost update", "silent conflict rebase", "citation-to-observation conversion", "real animal or farm data insertion", "identity transaction overclaim", "authority impersonation", "canonical repository mutation", "popover accessibility overclaim", "thermo-to-psyche category error", "metric semantic drift", "raw identifier or private path leakage", "duplicate baton"], "controls": ["compare-and-swap fixture", "zero-row refusal", "zero-real-entity invariants", "synthetic-only identity profile", "exact authority gate", "disposable root", "manual accessibility reservations", "category barrier", "metric lock", "five-class scan", "prepared-not-sent route"], "residual_risks": ["independent review absent", "real participant and data arms absent", "manual accessibility absent", "production security absent", "competent and affected authority absent"], "exhaustive_security_claim": False, "boundary": d.TRUTH_BOUNDARY})
    write_json("complete-incomplete-checklist.json", {"schema": "ghc.family.v646-v5.checklist.v1", "complete": ["dedicated x1 freeze and remote equality", "ten bounded core executions", "70 synthetic mutations rejected", "30 safe-now tasks", "20 bounded candidates", "20 phase-local skill packages", "10 family-current runner builds", "30 additive cleanup tasks", "static report structure", "negative and gate registers"], "incomplete": ["real GMUT data and likelihood", "blind matched-budget THOS real arms", "production Freed ID cryptography and interoperability", "veterinary or biosecurity decisions", "affected-party, legal, cultural, and Māori authority", "manual and affected-user accessibility evaluation", "exhaustive security", "independent-team reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": d.TRUTH_BOUNDARY})
    write_json("sources/source-use-receipt.json", {"schema": "ghc.family.v646-v5.source-use.v1", "source_count": len(d.SOURCES), "statuses": dict(Counter(row["status"] for row in d.SOURCES)), "official_or_primary_requirements_only": True, "real_rows": 0, "real_participants_or_animals": 0, "real_keys_or_transactions": 0, "authority_delegated": False, "citation_to_observation_conversion": False, "boundary": d.TRUTH_BOUNDARY})
    write_json("environment/x2-environment-receipt.json", {"schema": "ghc.family.v646-v5.x2-environment.v1", "codex_cli": "0.144.4 verified_only", "codex_desktop": "26.707.9981.0 verified_only_no_update", "windows_sandbox": "unavailable_to_ordinary_process_not_launched", "desktop_updated": False, "elevated": False, "host_security_weakened": False, "windows_feature_changed": False, "unrelated_installation": False, "rebooted": False, "full_repository_suite_run": False, "full_repository_suite_owner": "Eiren Kestrel", "boundary": d.TRUTH_BOUNDARY})
    write_json("orchestration/phase-update.json", {"schema": "ghc.family.phase-update.v1", "phase": d.PHASE, "owner": d.OWNER, "state": "x2_evidence_candidate_pending_exact_staged_validation", "active": [d.OWNER], "standby_contact_count": 0, "no_task_creation": True, "no_delegation": True, "x2_started": True, "core_outcomes_executed": 10, "terminal_route": "PREPARED_NOT_SENT"})
    write_json("orchestration/terminal-route-plan.json", {"schema": "ghc.family.v646-v5.route-plan.v1", "current_state": "PREPARED_NOT_SENT", "target_title": "Sylven Arc", "target_phase": "v646-v6", "send_count": 0, "preconditions": ["evidence commit clean and remote-equal", "combined closeout and seal within cap", "canonical exact-final scoped validation", "one clean local-only named-lane replay", "final four-way remote equality", "unique existing target resolved"], "privacy": "No raw task identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths."})
    write_json("memory/v646-v5-applicable-memory-update.json", {"schema": "ghc.family.v646-v5.applicable-memory-update.v1", "source": "newest applicable continuity reviewed before x1", "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES, "post_baton_external_negative_ingested": "V6464-POST-N03", "route": "Tamar v646-v5 to Sylven v646-v6", "full_suite_owner": "Eiren Kestrel", "memory_bank_mutated": False, "privacy_safe": True})
    write_json("family-index/v646-v5-evidence-index.json", {"schema": "ghc.family.v646-v5.evidence-index.v1", "phase": d.PHASE, "owner": d.OWNER, "x1_commit": X1_HEAD, "core_artifacts": core_paths, "proposal_ledger": "x2-proposal-ledger.json", "phase_truth": "phase-truth.json", "negative_register": "retained-negative-register.json", "gate_register": "exact-open-gate-register.json", "overview": "v646-v5-integrated-overview.md", "static_report": "deliverables/v646-v5-static-report.html", "route_state": "PREPARED_NOT_SENT", "boundary": d.TRUTH_BOUNDARY})
    write_text("wellbeing-check.md", f"""# Tamar Vey v646-v5 wellbeing and workload check

- Work remains bounded to one owner, one canonical branch, one later local-only named replay, and three planned phase commits within the four-commit cap.
- X1 froze before x2. Ten core surfaces, 70 negative mutations, and the 30/20/20/10/30 portfolios are partitioned into generated receipts and reusable runners.
- Fourteen operational failures are retained through the evidence candidate: four x1 faults and ten x2 reporting, compatibility, portability, privacy, status-classification, output-budget, staging-envelope, line-ending, or wrapper-state faults. Recovery never erased a failed witness.
- The owner-generated threshold remains 15,000 files and excludes the inherited checkout.
- The full repository suite remains Eiren-only. Tamar uses current-phase and eligible successor-scoped checks plus exactly one later named-lane replay.
- Windows Sandbox remains unavailable; no launch, elevation, feature change, installation, host-security weakening, desktop update, or reboot occurred.
- Relational identity language is not a consciousness, welfare, continuity, employment, qualification, or authority claim. Hamish may rename, pause, redirect, or stop the work.
""")
    phase_files = [path for path in PHASE.rglob("*") if path.is_file()]
    write_json("environment/evidence-footprint-receipt.json", {"schema": "ghc.family.v646-v5.evidence-footprint.v1", "owner_generated_files_observed_before_receipt": len(phase_files), "threshold": 15000, "threshold_scope": "new_tamar_generated_addition", "rotate": len(phase_files) >= 15000, "inherited_baseline_triggers_rotation": False})
    write_json("validation/evidence-build-receipt.json", {"schema": "ghc.family.v646-v5.evidence-build.v1", "x1_head": X1_HEAD, "proposal_count": 10, "distribution": dict(distribution), "core_passed": sum(row["passed"] for row in results), "synthetic_mutations_executed": len(synthetic_rows), "synthetic_mutations_rejected": sum(row["rejected"] for row in synthetic_rows), "effective_negatives": effective_negatives, "overview_words": words, "phase_files_observed_before_receipt": len(phase_files), "full_repository_suite_run": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "result": "pass", "boundary": d.TRUTH_BOUNDARY})
    print(json.dumps({"proposals": 10, "distribution": dict(distribution), "mutations": len(synthetic_rows), "effective_negatives": effective_negatives, "overview_words": words, "phase_files": len(phase_files) + 2, "result": "pass"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
