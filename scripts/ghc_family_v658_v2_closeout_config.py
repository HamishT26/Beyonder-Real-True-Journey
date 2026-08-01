#!/usr/bin/env python3
"""Immutable closeout configuration for Sylven Arc v658-v2."""

from __future__ import annotations


SOURCE_COMMIT = "9009c83b898fe11c63a95e4e1153ad388f328d3f"
FIRST_X1_COMMIT = "2254b08806b48bd302a04b6cdba7908ad39514d5"
X1_COMMIT = FIRST_X1_COMMIT
EVIDENCE_COMMIT = "fd928f5d2784d71c5664313883ba77ab47e25f6c"
PHASE_ROOT = "docs/sylven-arc/v658-v2"
BRANCH = "codex/GHC-Family/sylven-arc-v658-v2-full-tools"
EVIDENCE_EFFECTIVE_NEGATIVES = 16830
EVIDENCE_EFFECTIVE_METHODS = 3104
OPEN_GAPS = 114
EXACT_GATES = 113


CLOSEOUT_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6582-CLOSEOUT-N01",
        "slug": "powershell-divergence-tab-literal-comparison",
        "failure_signature": (
            "A post-evidence four-way equality wrapper compared the observed tab-delimited "
            "zero-divergence value against a single-quoted string containing literal backtick-t "
            "characters, so the wrapper exited one after already printing four equal heads, "
            "zero divergence, and a clean lane."
        ),
        "candidate_workaround": (
            "Split the divergence output on whitespace and compare its two fields numerically "
            "while preserving the already-observed local, upstream, tracking, and live values."
        ),
        "recurrence_guard": (
            "Do not assert Git divergence using shell escape spelling; parse the two scalar "
            "counts and compare each integer with zero."
        ),
        "fail_procedure": "Compare the tab-delimited divergence output to a single-quoted escape spelling.",
        "fail_observed": (
            "The wrapper returned exit one after printing the exact evidence head in all four "
            "domains, 0/0 divergence, and clean=true; no repository byte changed."
        ),
        "pass_procedure": "Split the same read-only divergence output and compare both fields as integers.",
        "pass_observed": (
            "The isolated scalar check passed with identical local, upstream, tracking, and "
            "fresh-live heads, ahead=0, behind=0, and clean=true."
        ),
        "scope_boundary": "Owner-local read-only equality-wrapper recovery only; no evidence, route, or completion credit.",
    },
]
