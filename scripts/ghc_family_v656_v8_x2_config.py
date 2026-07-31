#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Vesper v656-v8."""

from __future__ import annotations


SOURCE_COMMIT = "c885a4533b2a73343990039e21d74979acb79c00"
X1_COMMIT = "25c840c4e16a2b414dc6b51f5c529379eb244d1c"
PHASE_ROOT = "docs/vesper-arlen/v656-v8"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 14895
SOURCE_EFFECTIVE_NEGATIVES = 14895
X1_OPERATIONAL_NEGATIVES = 13
SOURCE_OPEN_GAPS = 103
SOURCE_EXACT_GATES = 102
SOURCE_METHODS = 1180
X1_METHODS = 13
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}

# Phase-local x2 operational failures are appended only after they are actually
# observed. Inherited owner failures remain inherited evidence, not Vesper credit.
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6568-X2-N14",
        "slug": "large-script-default-read-timeout",
        "failure_signature": (
            "The first 181-line x2 builder inspection exceeded the thirty-second "
            "outer bound before returning content."
        ),
        "candidate_workaround": (
            "Repeat only the same bounded literal-file slice with a sixty-second "
            "outer bound and no additional filesystem or Git traversal."
        ),
        "recurrence_guard": (
            "Give first-read startup latency its own budget and keep large script "
            "inspection separate from repository traversal."
        ),
        "fail_procedure": (
            "Read the first 181 lines of the large x2 builder under the default "
            "thirty-second tool timeout."
        ),
        "fail_observed": (
            "The command timed out without content and earned zero inspection credit."
        ),
        "pass_procedure": (
            "Reread the identical literal-file slice with a sixty-second outer bound."
        ),
        "pass_observed": (
            "The same 181-line slice returned completely without mutation."
        ),
        "scope_boundary": "Owner-local read-only inspection recovery only.",
    },
    {
        "negative_id": "V6568-X2-N15",
        "slug": "runner-console-maori-unicode-encoding",
        "failure_signature": (
            "The first generated runner wrote its bounded receipt but then raised "
            "UnicodeEncodeError while printing Māori text through the default "
            "Windows cp1252 console."
        ),
        "candidate_workaround": (
            "Retain the failed invocation, render console JSON with ASCII escapes, "
            "regenerate the family-current runners, and rerun the full declared "
            "runner set from its first member."
        ),
        "recurrence_guard": (
            "Use UTF-8 output or ASCII-escaped JSON for Windows console surfaces "
            "that may contain Māori or other non-cp1252 text."
        ),
        "fail_procedure": (
            "Run the generated seed-accession provenance wrapper with its default "
            "ensure_ascii=False console print."
        ),
        "fail_observed": (
            "The receipt write completed, but the process exited nonzero on console "
            "encoding and earned zero runner-pass credit."
        ),
        "pass_procedure": (
            "Regenerate wrappers with ensure_ascii=True for console output and rerun "
            "all ten family-current runner commands."
        ),
        "pass_observed": (
            "All ten wrappers exited zero and retained UTF-8 repository receipts."
        ),
        "scope_boundary": "Owner-local Windows console portability recovery only.",
    }
]
