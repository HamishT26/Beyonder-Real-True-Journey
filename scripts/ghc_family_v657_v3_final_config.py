#!/usr/bin/env python3
"""Final lifecycle constants for Auren Lark v657-v3."""

from __future__ import annotations


SOURCE_COMMIT = "67a5eaa17b2399d52bac5ba45d390d8659cc61cd"
X1_COMMIT = "b40c2f04cd7e51ed9bc5c1174255e9e3d06af4e1"
EVIDENCE_COMMIT = "ecd67debfa384f7d4224a2600cc23a4744f8b0b5"
CLOSEOUT_COMMIT = "9953615057ffea7d9240e1deee25a959c89b600f"
CLOSEOUT_EFFECTIVE_NEGATIVES = 15605
CLOSEOUT_EFFECTIVE_METHODS = 1887
OPEN_GAPS = 107
EXACT_GATES = 106

# Append-only final-preparation failures actually observed before the exact
# final candidate is committed.
FINAL_PREPARATION_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6573-FINAL-N20",
        "slug": "powershell-extended-string-json-overflow",
        "failure_signature": (
            "The first final-source inventory serialized a raw Get-Content string "
            "through ConvertTo-Json with PowerShell provider metadata, overflowing "
            "the useful output and truncating the requested cross-file hits."
        ),
        "candidate_workaround": (
            "Emit raw text directly and run bounded per-file symbol searches instead "
            "of JSON-serializing extended PowerShell string objects."
        ),
        "recurrence_guard": (
            "For source inspection output, coerce provider-decorated values to plain "
            "text or keep file content and metadata in separate scalar probes."
        ),
        "fail_procedure": (
            "Combine the full final config and all cross-file pattern hits in one "
            "ConvertTo-Json payload."
        ),
        "fail_observed": (
            "The command exited successfully but emitted a huge provider-object "
            "serialization whose useful hit section was truncated; it earned zero "
            "inspection credit and changed no repository state."
        ),
        "pass_procedure": (
            "Read only named final symbols and direct text ranges in small bounded "
            "probes, then patch against the exact observed source."
        ),
        "pass_observed": (
            "The bounded probes expose the anchor, lifecycle, route, validation, and "
            "successor-scope surfaces without output truncation."
        ),
        "scope_boundary": "Owner-local read-only final-source inspection recovery only.",
    },
    {
        "negative_id": "V6573-FINAL-N21",
        "slug": "powershell-flattened-range-array",
        "failure_signature": (
            "A multi-range final-validator read flattened nested PowerShell arrays "
            "and attempted subtraction on System.Object[], failing before any source "
            "range was returned."
        ),
        "candidate_workaround": (
            "Read each literal scalar range independently, or calculate the final "
            "integer index before constructing typed range records."
        ),
        "recurrence_guard": (
            "Do not embed arithmetic expressions inside nested untyped PowerShell "
            "range arrays used by foreach inspection wrappers."
        ),
        "fail_procedure": (
            "Construct three nested arrays, with the last endpoint expressed as "
            "the file line-count minus one, then iterate them as range pairs."
        ),
        "fail_observed": (
            "PowerShell raised an op_Subtraction method error, returned no requested "
            "source ranges, changed no state, and earned zero inspection credit."
        ),
        "pass_procedure": (
            "Run separate literal-range reads for the validator selection, checks, "
            "and receipt sections."
        ),
        "pass_observed": (
            "The scalar reads expose the exact branch, test-selection, manifest, "
            "route, count, and terminal-check surfaces without mutation."
        ),
        "scope_boundary": "Owner-local read-only source-range recovery only.",
    },
    {
        "negative_id": "V6573-FINAL-N22",
        "slug": "namespace-import-missing-scripts-path",
        "failure_signature": (
            "The first 60-test pre-final harness imported the validator through the "
            "scripts namespace without placing the scripts directory on sys.path, "
            "so its sibling evidence-receipt import could not resolve."
        ),
        "candidate_workaround": (
            "Insert the exact repository scripts directory on sys.path and import "
            "the validator by its declared module name before constructing the suite."
        ),
        "recurrence_guard": (
            "For inline repository harnesses, mirror the script entrypoint import "
            "path explicitly rather than relying on namespace-package side effects."
        ),
        "fail_procedure": (
            "Import scripts.ghc_family_v657_v3_final_validator with only the repository "
            "root present on sys.path."
        ),
        "fail_observed": (
            "Python raised ModuleNotFoundError for the sibling evidence-receipt module; "
            "zero tests ran, no state changed, and the attempt earned zero credit."
        ),
        "pass_procedure": (
            "Prepend the exact scripts directory, import the validator directly, and "
            "run the unchanged ten x1 plus x2 and closeout selection."
        ),
        "pass_observed": (
            "All 60 context-valid pre-final tests load and pass with no exclusions "
            "beyond the one declared historical x1 absence assertion."
        ),
        "scope_boundary": "Owner-local pre-final test-harness import recovery only.",
    },
]
